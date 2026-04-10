from collections import defaultdict

from django.db.models import Count, Max, Prefetch, Q, OuterRef, Subquery
from django.shortcuts import get_object_or_404, render

from i2fvg_mockup.models import (
    CompanyRegistryHeadquarters,
    CompanyRegistryFiltered,
    Financial,
    Project,
    Organization,
    EuroSciVoc,
)

TYPE_COLORS = [
    "#0d6b64",
    "#d97706",
    "#1d4ed8",
    "#b45309",
    "#7c3aed",
    "#64748b",
]

FVG_PROVINCES = ["TS", "UD", "GO", "PN"]


def company_registry_subquery(field_name):
    return Subquery(
        CompanyRegistryFiltered.objects.filter(cf=OuterRef("pk"))
        .exclude(**{field_name: ""})
        .values(field_name)[:1]
    )


def parse_amount(raw_value):
    value = (raw_value or "").strip()
    if not value:
        return 0.0

    value = value.replace(" ", "")
    if "," in value and "." in value:
        if value.rfind(",") > value.rfind("."):
            value = value.replace(".", "").replace(",", ".")
        else:
            value = value.replace(",", "")
    elif "," in value:
        value = value.replace(".", "").replace(",", ".")

    try:
        return float(value)
    except ValueError:
        return 0.0


def build_pie_chart(rows, label_key, count_key):
    total = sum(row[count_key] for row in rows) or 1
    pie_parts = []
    legend = []
    current_pct = 0.0

    for index, row in enumerate(rows):
        color = TYPE_COLORS[index % len(TYPE_COLORS)]
        percentage = round((row[count_key] / total) * 100, 1)
        next_pct = current_pct + percentage
        pie_parts.append(f"{color} {current_pct:.1f}% {next_pct:.1f}%")
        legend.append(
            {
                "label": row[label_key],
                "count": row[count_key],
                "percentage": percentage,
                "color": color,
            }
        )
        current_pct = next_pct

    return {
        "legend": legend,
        "style": ", ".join(pie_parts) if pie_parts else "#d7d1c7 0% 100%",
    }


def add_bar_width(rows, key):
    max_value = max((row[key] for row in rows), default=1)
    for row in rows:
        row["bar_width"] = round((row[key] / max_value) * 100, 1) if max_value else 0
    return rows


def company_name_map_for_cfs(cfs):
    if not cfs:
        return {}

    rows = (
        CompanyRegistryHeadquarters.objects.filter(cf__in=cfs)
        .annotate(company_name=company_registry_subquery("denominazione"))
        .values("cf", "company_name")
    )
    return {row["cf"]: row["company_name"] or row["cf"] for row in rows}


# ======================
# HOME
# ======================
def home(request):
    return render(request, "i2fvg_mockup/home.html")


# ======================
# COMPANY LIST
# ======================
def company_list(request):
    selected_province = request.GET.get("province", "ALL")
    active_rows = CompanyRegistryFiltered.objects.filter(stato_impresa="ATTIVA")

    active_company_count = active_rows.values("cf").distinct().count()
    active_localization_count = active_rows.count()

    legal_nature_rows = list(
        active_rows.exclude(tipo_impresa="")
        .values("tipo_impresa")
        .annotate(company_count=Count("cf", distinct=True))
        .order_by("-company_count")[:6]
    )
    legal_nature_chart = build_pie_chart(legal_nature_rows, "tipo_impresa", "company_count")

    province_rows_queryset = active_rows.filter(prov__in=FVG_PROVINCES)
    if selected_province in FVG_PROVINCES:
        province_rows_queryset = province_rows_queryset.filter(prov=selected_province)

    province_rows = list(
        province_rows_queryset.values("prov")
        .annotate(company_count=Count("cf", distinct=True))
        .order_by("-company_count")
    )

    context = {
        "active_company_count": active_company_count,
        "active_localization_count": active_localization_count,
        "legal_nature_legend": legal_nature_chart["legend"],
        "legal_nature_style": legal_nature_chart["style"],
        "province_rows": add_bar_width(province_rows, "company_count"),
        "province_options": FVG_PROVINCES,
        "selected_province": selected_province,
    }
    return render(request, "i2fvg_mockup/company_information.html", context)


# ======================
# COMPANY DETAIL
# ======================
def company_detail(request, cf):
    company = get_object_or_404(
        CompanyRegistryHeadquarters.objects.prefetch_related(
            Prefetch(
                "companyregistryfiltered_set",
                queryset=CompanyRegistryFiltered.objects.order_by("id"),
            ),
            Prefetch(
                "financial_set",
                queryset=Financial.objects.order_by("-anno"),
            ),
            Prefetch(
                "organization_set",
                queryset=Organization.objects.select_related("project").order_by("project__projectID"),
            ),
        ),
        cf=cf,
    )

    linked_projects = [item for item in company.organization_set.all() if item.project_id]

    return render(
        request,
        "i2fvg_mockup/company_detail.html",
        {
            "company": company,
            "registry_rows": company.companyregistryfiltered_set.all(),
            "financial_rows": company.financial_set.all(),
            "linked_projects": linked_projects,
        },
    )


# ======================
# PROJECT LIST
# ======================
def project_list(request):
    project_company_year = defaultdict(lambda: {"H2020": set(), "HORIZON EUROPE": set()})
    company_contribution = defaultdict(lambda: {"H2020": 0.0, "HORIZON EUROPE": 0.0})
    euroscivoc_distribution = defaultdict(lambda: {"H2020": set(), "HORIZON EUROPE": set()})

    organizations = Organization.objects.select_related("project").exclude(cf__isnull=True)
    for item in organizations.iterator():
        if not item.project or item.project.frameworkProgramme not in {"H2020", "HORIZON EUROPE"}:
            continue

        year = (item.project.startDate or "")[:4]
        if year:
            project_company_year[year][item.project.frameworkProgramme].add(item.cf_id)

        company_contribution[item.cf_id][item.project.frameworkProgramme] += parse_amount(item.ecContribution)

    euros = EuroSciVoc.objects.select_related("project")
    for item in euros.iterator():
        if not item.project or item.project.frameworkProgramme not in {"H2020", "HORIZON EUROPE"}:
            continue
        title = item.euroSciVocTitle or "Non classificato"
        euroscivoc_distribution[title][item.project.frameworkProgramme].add(item.project_id)

    company_year_rows = []
    for year in sorted(project_company_year):
        company_year_rows.append(
            {
                "year": year,
                "h2020_count": len(project_company_year[year]["H2020"]),
                "he_count": len(project_company_year[year]["HORIZON EUROPE"]),
            }
        )
    max_company_year = max((max(row["h2020_count"], row["he_count"]) for row in company_year_rows), default=1)
    for row in company_year_rows:
        row["h2020_width"] = round((row["h2020_count"] / max_company_year) * 100, 1) if max_company_year else 0
        row["he_width"] = round((row["he_count"] / max_company_year) * 100, 1) if max_company_year else 0

    company_name_map = company_name_map_for_cfs(company_contribution.keys())
    contribution_rows = []
    for cf, values in company_contribution.items():
        contribution_rows.append(
            {
                "cf": cf,
                "company_name": company_name_map.get(cf, cf),
                "h2020_amount": round(values["H2020"], 2),
                "he_amount": round(values["HORIZON EUROPE"], 2),
                "total_amount": round(values["H2020"] + values["HORIZON EUROPE"], 2),
            }
        )
    contribution_rows.sort(key=lambda row: row["total_amount"], reverse=True)
    contribution_rows = contribution_rows[:20]
    max_contribution = max((max(row["h2020_amount"], row["he_amount"]) for row in contribution_rows), default=1)
    for row in contribution_rows:
        row["h2020_width"] = round((row["h2020_amount"] / max_contribution) * 100, 1) if max_contribution else 0
        row["he_width"] = round((row["he_amount"] / max_contribution) * 100, 1) if max_contribution else 0

    euroscivoc_rows = []
    for title, values in euroscivoc_distribution.items():
        euroscivoc_rows.append(
            {
                "title": title,
                "h2020_count": len(values["H2020"]),
                "he_count": len(values["HORIZON EUROPE"]),
                "total_count": len(values["H2020"]) + len(values["HORIZON EUROPE"]),
            }
        )
    euroscivoc_rows.sort(key=lambda row: row["total_count"], reverse=True)
    euroscivoc_rows = euroscivoc_rows[:20]
    max_euroscivoc = max((max(row["h2020_count"], row["he_count"]) for row in euroscivoc_rows), default=1)
    for row in euroscivoc_rows:
        row["h2020_width"] = round((row["h2020_count"] / max_euroscivoc) * 100, 1) if max_euroscivoc else 0
        row["he_width"] = round((row["he_count"] / max_euroscivoc) * 100, 1) if max_euroscivoc else 0

    context = {
        "company_year_rows": company_year_rows,
        "contribution_rows": contribution_rows,
        "euroscivoc_rows": euroscivoc_rows,
    }
    return render(request, "i2fvg_mockup/eu_projects_dashboard.html", context)


# ======================
# PROJECT DETAIL
# ======================
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related(
            Prefetch(
                "organization_set",
                queryset=Organization.objects.select_related("cf").order_by("organisationID"),
            ),
            Prefetch(
                "euroscivoc_set",
                queryset=EuroSciVoc.objects.order_by("livello_1", "livello_2"),
            ),
        ),
        projectID=project_id,
    )

    return render(request, "i2fvg_mockup/project_detail.html", {"project": project})


# ======================
# CONNECTED COMPANIES
# ======================
def connected_company_list(request):
    query = request.GET.get("q", "").strip()

    companies = (
        CompanyRegistryHeadquarters.objects.annotate(
            company_name=company_registry_subquery("denominazione"),
            registry_comune=company_registry_subquery("comune"),
            registry_stato_impresa=company_registry_subquery("stato_impresa"),
            financial_count=Count("financial", distinct=True),
            project_count=Count("organization", distinct=True),
            latest_financial_year=Max("financial__anno"),
        )
        .filter(Q(financial_count__gt=0) | Q(project_count__gt=0))
        .order_by("-project_count", "-financial_count", "cf")
    )

    if query:
        companies = companies.filter(
            Q(cf__icontains=query)
            | Q(companyregistryfiltered__denominazione__icontains=query)
            | Q(companyregistryfiltered__comune__icontains=query)
        )

    context = {
        "query": query,
        "companies": companies.distinct()[:300],
    }
    return render(request, "i2fvg_mockup/connected_company_list.html", context)


# ======================
# FINANCIAL DASHBOARD
# ======================
def financial_dashboard(request):
    available_years = list(
        Financial.objects.exclude(anno="")
        .values_list("anno", flat=True)
        .distinct()
        .order_by("anno")
    )
    selected_year = request.GET.get("year") or (available_years[-1] if available_years else "")

    company_count_rows = list(
        Financial.objects.exclude(anno="")
        .values("anno")
        .annotate(company_count=Count("cf", distinct=True))
        .order_by("anno")
    )
    add_bar_width(company_count_rows, "company_count")

    revenue_by_year = defaultdict(float)
    for year, revenue in Financial.objects.exclude(anno="").values_list("anno", "ricavi_delle_vendite").iterator():
        revenue_by_year[year] += parse_amount(revenue)

    revenue_year_rows = []
    for year in sorted(revenue_by_year):
        revenue_year_rows.append(
            {
                "year": year,
                "revenue": round(revenue_by_year[year], 2),
            }
        )
    add_bar_width(revenue_year_rows, "revenue")

    company_revenue = defaultdict(float)
    for cf, revenue in Financial.objects.filter(anno=selected_year).values_list("cf_id", "ricavi_delle_vendite").iterator():
        company_revenue[cf] += parse_amount(revenue)

    company_name_map = company_name_map_for_cfs(company_revenue.keys())
    company_revenue_rows = []
    for cf, revenue in company_revenue.items():
        company_revenue_rows.append(
            {
                "cf": cf,
                "company_name": company_name_map.get(cf, cf),
                "revenue": round(revenue, 2),
            }
        )
    company_revenue_rows.sort(key=lambda row: row["revenue"], reverse=True)
    company_revenue_rows = company_revenue_rows[:20]
    add_bar_width(company_revenue_rows, "revenue")

    context = {
        "available_years": available_years,
        "selected_year": selected_year,
        "company_count_rows": company_count_rows,
        "revenue_year_rows": revenue_year_rows,
        "company_revenue_rows": company_revenue_rows,
    }
    return render(request, "i2fvg_mockup/financial_dashboard.html", context)
