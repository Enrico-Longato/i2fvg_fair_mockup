import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from i2fvg_mockup.models import (
    CompanyRegistryHeadquarters,
    CompanyRegistryFiltered,
    Financial,
    Project,
    Organization,
    EuroSciVoc,
)

BASE_DATA_DIR = Path(__file__).resolve().parents[4] / "data"


def clean(value):
    return (value or "").strip()


class Command(BaseCommand):
    help = "Full import CSV → DB (all columns)"

    def handle(self, *args, **options):
        self.imported_at = timezone.now()

        self.stdout.write("Clearing tables...")
        self.clear_tables()

        self.import_headquarters()
        self.import_filtered()
        self.import_financial()
        self.import_projects()
        self.import_organization()
        self.import_euroscivoc()

        self.stdout.write(self.style.SUCCESS("IMPORT COMPLETED"))

    # =========================
    # CLEAR
    # =========================
    @transaction.atomic
    def clear_tables(self):
        EuroSciVoc.objects.all().delete()
        Organization.objects.all().delete()
        Financial.objects.all().delete()
        CompanyRegistryFiltered.objects.all().delete()
        Project.objects.all().delete()
        CompanyRegistryHeadquarters.objects.all().delete()

    # =========================
    # HEADQUARTERS
    # =========================
    def import_headquarters(self):
        path = BASE_DATA_DIR / "company_registry" / "i2fvg_company_registry_headquarters.csv"

        rows = []
        for row in self.read_csv(path):
            cf = clean(row.get("cf"))
            if not cf:
                continue

            rows.append(
                CompanyRegistryHeadquarters(
                    cf=cf,
                    prov=clean(row.get("prov")),
                    reg_imp_n=clean(row.get("reg_imp_n")),
                    rea=clean(row.get("rea")),
                    sede_ul=clean(row.get("sede_ul")),
                    tipo_impresa=clean(row.get("tipo_impresa")),
                    n_albo_art=clean(row.get("n-albo_art")),
                    denominazione=clean(row.get("denominazione")),
                    indirizzo=clean(row.get("indirizzo")),
                    indirizzo_strad=clean(row.get("indirizzo_strad")),
                    indirizzo_cap=clean(row.get("indirizzo_cap")),
                    comune=clean(row.get("comune")),
                    indirizzo_fraz=clean(row.get("indirizzo_fraz")),
                    indirizzo_altre=clean(row.get("indirizzo_altre")),
                    addetti_aaaa=clean(row.get("addetti_aaaa")),
                    addetti_indip=clean(row.get("addetti_indip")),
                    addetti_dip=clean(row.get("addetti_dip")),
                    piva=clean(row.get("piva")),
                    tel=clean(row.get("tel")),
                    capitale=clean(row.get("capitale")),
                    descrizione_attivita=clean(row.get("descrizione_attivita")),
                    capitale_valuta=clean(row.get("capitale_valuta")),
                    stato_impresa=clean(row.get("stato_impresa")),
                    tipo_sedeul_1=clean(row.get("tipo_sedeul_1")),
                    tipo_sedeul_2=clean(row.get("tipo_sedeul_2")),
                    tipo_sedeul_3=clean(row.get("tipo_sedeul_3")),
                    tipo_sedeul_4=clean(row.get("tipo_sedeul_4")),
                    tipo_sedeul_5=clean(row.get("tipo_sedeul_5")),
                    imp_sedi_ee=clean(row.get("imp_sedi_ee")),
                    imp_eefvg=clean(row.get("imp_eefvg")),
                    imp_pmi=clean(row.get("imp_pmi")),
                    imp_startup=clean(row.get("imp_startup")),
                    imp_femmilile=clean(row.get("imp_femmilile")),
                    imp_giovanile=clean(row.get("imp_giovanile")),
                    imp_straniera=clean(row.get("imp_straniera")),
                    pec=clean(row.get("PEC")),
                    data_fine_aa=clean(row.get("data_fine_aa")),
                    data_cost=clean(row.get("data_cost")),
                    tipo_localizzazione=clean(row.get("tipo_localizzazione")),
                )
            )

            if len(rows) >= 2000:
                CompanyRegistryHeadquarters.objects.bulk_create(rows, ignore_conflicts=True)
                rows.clear()

        if rows:
            CompanyRegistryHeadquarters.objects.bulk_create(rows, ignore_conflicts=True)

    # =========================
    # FILTERED
    # =========================
    def import_filtered(self):
        path = BASE_DATA_DIR / "company_registry" / "i2fvg_company_registry_filtered.csv"

        rows = []
        for row in self.read_csv(path):
            cf = clean(row.get("cf"))
            if not cf:
                continue

            rows.append(
                CompanyRegistryFiltered(
                    cf_id=cf,
                    prov=clean(row.get("prov")),
                    reg_imp_n=clean(row.get("reg_imp_n")),
                    rea=clean(row.get("rea")),
                    sede_ul=clean(row.get("sede_ul")),
                    tipo_impresa=clean(row.get("tipo_impresa")),
                    n_albo_art=clean(row.get("n-albo_art")),
                    denominazione=clean(row.get("denominazione")),
                    indirizzo=clean(row.get("indirizzo")),
                    indirizzo_strad=clean(row.get("indirizzo_strad")),
                    indirizzo_cap=clean(row.get("indirizzo_cap")),
                    comune=clean(row.get("comune")),
                    indirizzo_fraz=clean(row.get("indirizzo_fraz")),
                    indirizzo_altre=clean(row.get("indirizzo_altre")),
                    addetti_aaaa=clean(row.get("addetti_aaaa")),
                    addetti_indip=clean(row.get("addetti_indip")),
                    addetti_dip=clean(row.get("addetti_dip")),
                    piva=clean(row.get("piva")),
                    tel=clean(row.get("tel")),
                    capitale=clean(row.get("capitale")),
                    descrizione_attivita=clean(row.get("descrizione_attivita")),
                    capitale_valuta=clean(row.get("capitale_valuta")),
                    stato_impresa=clean(row.get("stato_impresa")),
                    tipo_sedeul_1=clean(row.get("tipo_sedeul_1")),
                    tipo_sedeul_2=clean(row.get("tipo_sedeul_2")),
                    tipo_sedeul_3=clean(row.get("tipo_sedeul_3")),
                    tipo_sedeul_4=clean(row.get("tipo_sedeul_4")),
                    tipo_sedeul_5=clean(row.get("tipo_sedeul_5")),
                    imp_sedi_ee=clean(row.get("imp_sedi_ee")),
                    imp_eefvg=clean(row.get("imp_eefvg")),
                    imp_pmi=clean(row.get("imp_pmi")),
                    imp_startup=clean(row.get("imp_startup")),
                    imp_femmilile=clean(row.get("imp_femmilile")),
                    imp_giovanile=clean(row.get("imp_giovanile")),
                    imp_straniera=clean(row.get("imp_straniera")),
                    pec=clean(row.get("PEC")),
                    data_fine_aa=clean(row.get("data_fine_aa")),
                    data_cost=clean(row.get("data_cost")),
                    tipo_localizzazione=clean(row.get("tipo_localizzazione")),
                )
            )

            if len(rows) >= 2000:
                CompanyRegistryFiltered.objects.bulk_create(rows, ignore_conflicts=True)
                rows.clear()

        if rows:
            CompanyRegistryFiltered.objects.bulk_create(rows, ignore_conflicts=True)

    # =========================
    # FINANCIAL
    # =========================
    def import_financial(self):
        path = self.get_financial_csv_path()
        valid_cfs = set(
            CompanyRegistryHeadquarters.objects.values_list("cf", flat=True)
        )

        rows = []
        skipped = 0
        for row in self.read_csv(path):
            cf = clean(row.get("c fiscale"))
            if not cf or cf not in valid_cfs:
                skipped += 1
                continue

            rows.append(
                Financial(
                    cf_id=cf,
                    cia=clean(row.get("cia")),
                    rea=clean(row.get("rea")),
                    anno=clean(row.get("anno")),
                    totale_attivo=clean(row.get("Totale attivo")),
                    totale_immobilizzazioni_immateriali=clean(row.get("Totale Immobilizzazioni immateriali")),
                    crediti_esigibili_entro_esercizio_successivo=clean(row.get("Crediti esigibili entro l'esercizio successivo")),
                    totale_patrimonio_netto=clean(row.get("Totale patrimonio netto")),
                    debiti_esigibili_entro_esercizio_successivo=clean(row.get("Debiti esigibili entro l'esercizio successivo")),
                    totale_valore_della_produzione=clean(row.get("Totale valore della produzione")),
                    ricavi_delle_vendite=clean(row.get("Ricavi delle vendite")),
                    totale_costi_del_personale=clean(row.get("Totale Costi del Personale")),
                    differenza_tra_valore_e_costi_della_produzione=clean(row.get("Differenza tra valore e costi della produzione")),
                    ammortamento_immobilizzazione_immateriali=clean(row.get("Ammortamento Immobilizzazione Immateriali")),
                    utile_perdita_esercizio_ultimi=clean(row.get("Utile/perdita esercizio ultimi")),
                    valore_aggiunto=clean(row.get("valore aggiunto")),
                    tot_aam_acc_svalutazioni=clean(row.get("tot.aam.acc.svalutazioni")),
                    ron_reddito_operativo_netto=clean(row.get("(ron) reddito operativo netto")),
                    immobilizzazioni_materiali=clean(row.get("Immobilizzazioni materiali")),
                    immobilizzazioni_finanziarie=clean(row.get("Immobilizzazioni finanziarie")),
                    attivo_circolante=clean(row.get("Attivo Circolante")),
                )
            )

            if len(rows) >= 2000:
                Financial.objects.bulk_create(rows, ignore_conflicts=True)
                rows.clear()

        if rows:
            Financial.objects.bulk_create(rows, ignore_conflicts=True)

        self.stdout.write(
            f"Financial import: skipped {skipped} rows without matching company_registry headquarters cf"
        )

    # =========================
    # PROJECT
    # =========================
    def import_projects(self):
        path = BASE_DATA_DIR / "eu_projects" / "merge" / "project.csv"

        rows = []
        for row in self.read_csv(path):
            project_id = clean(row.get("projectID"))
            if not project_id:
                continue

            rows.append(
                Project(
                    projectID=project_id,
                    acronym=clean(row.get("acronym")),
                    status=clean(row.get("status")),
                    title=clean(row.get("title")),
                    startDate=clean(row.get("startDate")),
                    endDate=clean(row.get("endDate")),
                    totalCost=clean(row.get("totalCost")),
                    ecMaxContribution=clean(row.get("ecMaxContribution")),
                    legalBasis=clean(row.get("legalBasis")),
                    topics=clean(row.get("topics")),
                    ecSignatureDate=clean(row.get("ecSignatureDate")),
                    frameworkProgramme=clean(row.get("frameworkProgramme")),
                    masterCall=clean(row.get("masterCall")),
                    subCall=clean(row.get("subCall")),
                    fundingScheme=clean(row.get("fundingScheme")),
                    objective=clean(row.get("objective")),
                    contentUpdateDate=clean(row.get("contentUpdateDate")),
                    rcn=clean(row.get("rcn")),
                    grantDoi=clean(row.get("grantDoi")),
                    keywords=clean(row.get("keywords")),
                    coordinator=clean(row.get("coordinator")),
                    participants=clean(row.get("participants")),
                )
            )

        Project.objects.bulk_create(rows, ignore_conflicts=True)

    # =========================
    # ORGANIZATION
    # =========================
    def import_organization(self):
        path = BASE_DATA_DIR / "eu_projects" / "merge" / "organization.csv"
        valid_project_ids = set(Project.objects.values_list("projectID", flat=True))

        rows = []
        skipped = 0
        for row in self.read_csv(path):
            project_id = clean(row.get("projectID"))
            if not project_id or project_id not in valid_project_ids:
                skipped += 1
                continue

            rows.append(
                Organization(
                    project_id=project_id,
                    cf_id=clean(row.get("cf")) or None,
                    projectAcronym=clean(row.get("projectAcronym")),
                    organisationID=clean(row.get("organisationID")),
                    vatNumber=clean(row.get("vatNumber")),
                    name=clean(row.get("name")),
                    shortName=clean(row.get("shortName")),
                    SME=clean(row.get("SME")),
                    activityType=clean(row.get("activityType")),
                    street=clean(row.get("street")),
                    postCode=clean(row.get("postCode")),
                    city=clean(row.get("city")),
                    country=clean(row.get("country")),
                    nutsCode=clean(row.get("nutsCode")),
                    geolocation=clean(row.get("geolocation")),
                    organizationURL=clean(row.get("organizationURL")),
                    contactForm=clean(row.get("contactForm")),
                    contentUpdateDate=clean(row.get("contentUpdateDate")),
                    rcn=clean(row.get("rcn")),
                    order=clean(row.get("order")),
                    role=clean(row.get("role")),
                    ecContribution=clean(row.get("ecContribution")),
                    netEcContribution=clean(row.get("netEcContribution")),
                    totalCost=clean(row.get("totalCost")),
                    endOfParticipation=clean(row.get("endOfParticipation")),
                    active=clean(row.get("active")),
                )
            )

            if len(rows) >= 2000:
                Organization.objects.bulk_create(rows, ignore_conflicts=True)
                rows.clear()

        if rows:
            Organization.objects.bulk_create(rows, ignore_conflicts=True)

        self.stdout.write(
            f"Organization import: skipped {skipped} rows without matching projectID"
        )

    # =========================
    # EUROSCIVOC
    # =========================
    def import_euroscivoc(self):
        path = BASE_DATA_DIR / "eu_projects" / "merge" / "euroscivoc.csv"
        valid_project_ids = set(Project.objects.values_list("projectID", flat=True))

        rows = []
        skipped = 0
        for row in self.read_csv(path):
            project_id = clean(row.get("projectID"))
            if not project_id or project_id not in valid_project_ids:
                skipped += 1
                continue

            rows.append(
                EuroSciVoc(
                    project_id=project_id,
                    euroSciVocCode=clean(row.get("euroSciVocCode")),
                    euroSciVocPath=clean(row.get("euroSciVocPath")),
                    euroSciVocTitle=clean(row.get("euroSciVocTitle")),
                    euroSciVocDescription=clean(row.get("euroSciVocDescription")),
                    livello_1=clean(row.get("livello_1")),
                    livello_2=clean(row.get("livello_2")),
                )
            )

            if len(rows) >= 2000:
                EuroSciVoc.objects.bulk_create(rows, ignore_conflicts=True)
                rows.clear()

        if rows:
            EuroSciVoc.objects.bulk_create(rows, ignore_conflicts=True)

        self.stdout.write(
            f"EuroSciVoc import: skipped {skipped} rows without matching projectID"
        )

    # =========================
    # CSV
    # =========================
    def read_csv(self, path):
        if not path.exists():
            raise FileNotFoundError(f"CSV not found: {path}")

        with path.open(newline="", encoding="utf-8-sig") as f:
            yield from csv.DictReader(f, delimiter="|")

    def get_financial_csv_path(self):
        candidates = [
            BASE_DATA_DIR / "financial" / "i2fvg_financial.csv",

        ]

        for path in candidates:
            if path.exists():
                return path

        raise FileNotFoundError("Financial CSV not found")
