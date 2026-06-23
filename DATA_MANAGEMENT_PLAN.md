# Data Management Plan

## 1. Data Summary

The project “Innovation Intelligence FVG – FAIR Mockup” generates and reuses structured datasets related to companies in Friuli Venezia Giulia.

The repository documents the data lifecycle through versioned scripts, processed CSV outputs, and DCAT metadata catalogs stored under [`data/`](/root/i2fvg/data). The main project documentation is available in [`README.md`](/root/i2fvg/README.md), while this plan is complemented by machine-readable metadata files such as [`data/company_registry/DCAT_company_registry.json`](/root/i2fvg/data/company_registry/DCAT_company_registry.json), [`data/financial/DCAT_financial.json`](/root/i2fvg/data/financial/DCAT_financial.json), and [`data/eu_projects/merge/DCAT_eu_projects.json`](/root/i2fvg/data/eu_projects/merge/DCAT_eu_projects.json).

### Types and formats of data
- Company registry data (Excel → CSV)
- Financial data (CSV/Excel → CSV)
- EU project data from CORDIS (CSV → CSV)
- Metadata (DCAT JSON files)

All processed data are standardized in CSV format, while metadata follow DCAT specifications.

### Origin of data
- Regional company registry datasets
- Infocamere financial data
- CORDIS datasets (H2020 and Horizon Europe)

The project reuses existing datasets and transforms them into a unified data model.

Concrete source resources currently referenced in the workflow include:
- company registry sample/source workbooks in [`data/company_registry/`](/root/i2fvg/data/company_registry), e.g. [`imprese_fvg_05_2026.xlsx`](/root/i2fvg/data/company_registry/imprese_fvg_05_2026.xlsx)
- financial source files in [`data/financial/`](/root/i2fvg/data/financial), e.g. [`infocamere_2024.csv`](/root/i2fvg/data/financial/infocamere_2024.csv) and [`infocamere_2025.csv`](/root/i2fvg/data/financial/infocamere_2025.csv)
- CORDIS Horizon 2020 dataset: https://data.europa.eu/data/datasets/cordish2020projects?locale=en
- CORDIS Horizon Europe dataset: https://data.europa.eu/data/datasets/cordis-eu-research-projects-under-horizon-europe-2021-2027?locale=en

### Purpose of the data
The data are used to reconstruct a regional business intelligence system and enable integration between companies, financial indicators, and EU-funded projects.

### Data volume
The project operates on small-to-medium structured datasets suitable for local processing (MB–low GB scale).

### Reusability
Processed datasets and metadata are designed to be reusable for:
- data integration experiments
- FAIR data demonstrations
- analytical and visualization purposes

---

## 2. FAIR Data

### 2.1 Making data findable
- Datasets are organized by domain (`company_registry`, `financial`, `eu_projects`)
- Metadata are generated in DCAT JSON format
- File naming conventions and folder structure ensure discoverability
- Aggregated metadata catalogs are produced for each domain:
  - [`data/company_registry/DCAT_company_registry.json`](/root/i2fvg/data/company_registry/DCAT_company_registry.json)
  - [`data/financial/DCAT_financial.json`](/root/i2fvg/data/financial/DCAT_financial.json)
  - [`data/eu_projects/merge/DCAT_eu_projects.json`](/root/i2fvg/data/eu_projects/merge/DCAT_eu_projects.json)
- Naming conventions follow a consistent pattern:
  - dataset files use lowercase and underscores, avoiding spaces
  - file names start with the project prefix (`i2fvg_`), followed by the domain and descriptive suffixes such as `company_registry`, `financial`, `ateco`, `filtered`, or `headquarters`
  - data files use `.csv`, while metadata files use `.dcat.json`
  - versioning and subset information are encoded in the filename when needed, e.g. `i2fvg_company_registry_filtered.csv` or `i2fvg_ateco_sedi.csv`
- Script naming conventions ensure sequential execution and clarity:
  - scripts are numbered with a two-digit prefix (e.g., `00_`, `01_`, `02_`) to indicate the order of execution in the workflow
  - sub-steps within a main step use additional numbering (e.g., `01_01_`, `01_02_`)
  - descriptive names follow the numbering, using underscores instead of spaces, and end with `.py` for Python scripts
  - examples include `00_main.py` for the main entry point, `01_01_input_to_dcat.py` for input processing, and `04_01_django_import_sqlite.py` for database integration

Persistent identifiers (PIDs) are handled as follows:
- a repository-level external PID is available through Zenodo for this project: https://doi.org/10.5281/zenodo.20177633 (landing page: https://zenodo.org/records/20177633)
- internal dataset identifiers are expressed through stable filenames and DCAT metadata titles
- external PIDs coming from reused sources are preserved when available; for example, CORDIS project records in [`data/eu_projects/merge/project.csv`](/root/i2fvg/data/eu_projects/merge/project.csv) retain grant identifiers and project DOIs where provided by the source
- the Zenodo DOI should be cited in future metadata refinements and, where appropriate, added explicitly to the DCAT catalogs

### 2.2 Making data accessible
- Data are accessible locally via repository structure and Django interface
- No restricted data are included in the public repository
- External datasets must be accessed according to their providers
- The local data area is organized under [`data/company_registry/`](/root/i2fvg/data/company_registry), [`data/financial/`](/root/i2fvg/data/financial), and [`data/eu_projects/`](/root/i2fvg/data/eu_projects)
- Processed outputs exposed by the application include:
  - [`data/company_registry/i2fvg_company_registry_headquarters.csv`](/root/i2fvg/data/company_registry/i2fvg_company_registry_headquarters.csv)
  - [`data/company_registry/i2fvg_company_registry_filtered.csv`](/root/i2fvg/data/company_registry/i2fvg_company_registry_filtered.csv)
  - [`data/financial/i2fvg_financial.csv`](/root/i2fvg/data/financial/i2fvg_financial.csv)
  - [`data/eu_projects/merge/project.csv`](/root/i2fvg/data/eu_projects/merge/project.csv)
  - [`data/eu_projects/merge/organization.csv`](/root/i2fvg/data/eu_projects/merge/organization.csv)
  - [`data/eu_projects/merge/euroscivoc.csv`](/root/i2fvg/data/eu_projects/merge/euroscivoc.csv)
- Corresponding machine-readable metadata are distributed side by side as `.dcat.json` files, for example [`data/financial/i2fvg_financial.dcat.json`](/root/i2fvg/data/financial/i2fvg_financial.dcat.json)
- The exploration interface is the local Django application documented in [`README.md`](/root/i2fvg/README.md), typically served at `http://127.0.0.1:8000/` during development

### 2.3 Making data interoperable
- Data are standardized into CSV format
- Column mappings are defined in `cols_dict.xlsx`
- DCAT metadata provides semantic descriptions and structure
- Domain crosswalks are versioned as JSON resources:
  - [`data/company_registry/crosswalk_copany_registry.json`](/root/i2fvg/data/company_registry/crosswalk_copany_registry.json)
  - [`data/financial/crosswalk_financial.json`](/root/i2fvg/data/financial/crosswalk_financial.json)
  - [`data/eu_projects/merge/crosswalk_eu_projects.json`](/root/i2fvg/data/eu_projects/merge/crosswalk_eu_projects.json)
- Column normalization rules are maintained in [`script/cols_dict.xlsx`](/root/i2fvg/script/cols_dict.xlsx)
- EU-project metadata explicitly link back to the source catalogs via JSON-LD/DCAT references implemented in [`script/02_04_eu_merge_DCAT.py`](/root/i2fvg/script/02_04_eu_merge_DCAT.py)

### 2.4 Increasing data re-use
- Processing scripts are fully reproducible
- Metadata document provenance and transformations
- Licensing conditions are clearly specified
- The workflow enables extension and reuse
- The ETL workflow is executable through [`script/00_main.py`](/root/i2fvg/script/00_main.py)
- Metadata generation is automated by dedicated scripts, including [`script/01_03_output_to_dcat.py`](/root/i2fvg/script/01_03_output_to_dcat.py), [`script/02_04_eu_merge_DCAT.py`](/root/i2fvg/script/02_04_eu_merge_DCAT.py), and [`script/03_03_financial_output_to_dcat.py`](/root/i2fvg/script/03_03_financial_output_to_dcat.py)
- Reuse is supported by preserving provenance fields such as source file names, generation timestamps, row counts, column counts, and semantic crosswalk mappings in the DCAT outputs

---

## 3. Other Research Outputs

The project also produces:
- Python ETL scripts
- Django web application
- Data transformation workflows

These components are version-controlled and documented to ensure reproducibility.

Concrete non-dataset outputs include:
- ETL launcher: [`script/00_main.py`](/root/i2fvg/script/00_main.py)
- Django application: [`django_project/i2fvg_mockup/`](/root/i2fvg/django_project/i2fvg_mockup)
- import workflow: [`django_project/i2fvg_mockup/management/commands/import_i2fvg_data.py`](/root/i2fvg/django_project/i2fvg_mockup/management/commands/import_i2fvg_data.py)
- project documentation: [`README.md`](/root/i2fvg/README.md) and [`DATA_MANAGEMENT_PLAN.md`](/root/i2fvg/DATA_MANAGEMENT_PLAN.md)

At present, no separate PID has been assigned to the software or documentation outputs. If the software is archived in a long-term repository, a software DOI should be recorded here together with the release URL.
The project-level archival reference currently available is the Zenodo DOI and record for this repository: https://doi.org/10.5281/zenodo.20177633

---

## 4. Allocation of Resources

### Responsibilities
- Project maintainer: overall data management and FAIR compliance
- Data steward: metadata quality and documentation
- Developer: ETL pipeline and application integration

### Costs
No significant additional costs are foreseen, as:
- data are processed locally
- storage requirements are limited
- open-source tools are used

---

## 5. Data Security

- The public repository contains only non-sensitive or synthetic data
- Licensed or restricted datasets must be stored outside the repository
- Access to sensitive data is controlled through external systems
- No credentials or secure endpoints are exposed
- Bundled demo inputs are intentionally limited; as documented in [`README.md`](/root/i2fvg/README.md), they are fictitious in almost all fields except VAT numbers used for matching
- The repository currently stores only local development data and metadata, while full production datasets are intentionally not versioned

---

## 6. Ethics

- The project does not process personal data in the public version
- Any real datasets must comply with GDPR and institutional policies
- Data providers’ licensing and usage constraints must be respected
- Reused CORDIS data are public-sector open data, while company registry and Infocamere-derived resources may be subject to contractual or provider-specific access conditions and therefore require case-by-case verification before redistribution

---

## 7. Other Issues

- The DMP is a living document and may be updated during the project
- The repository is intended as a FAIR-compliant mockup and demonstration environment
- Real-world deployment would require additional infrastructure and governance policies

---

## 8. References

This Data Management Plan follows the structure and recommendations of the Horizon Europe Data Management Plan template provided by the European Commission:
https://ec.europa.eu/research/participants/documents/downloadPublic?documentIds=080166e502e83f42&appId=PPGMS

Additional project resources cited in this DMP:
- Repository overview and operating instructions: [`README.md`](/root/i2fvg/README.md)
- Company registry metadata catalog: [`data/company_registry/DCAT_company_registry.json`](/root/i2fvg/data/company_registry/DCAT_company_registry.json)
- Financial metadata catalog: [`data/financial/DCAT_financial.json`](/root/i2fvg/data/financial/DCAT_financial.json)
- EU projects metadata catalog: [`data/eu_projects/merge/DCAT_eu_projects.json`](/root/i2fvg/data/eu_projects/merge/DCAT_eu_projects.json)
- CORDIS Horizon 2020 dataset landing page: https://data.europa.eu/data/datasets/cordish2020projects?locale=en
- CORDIS Horizon Europe dataset landing page: https://data.europa.eu/data/datasets/cordis-eu-research-projects-under-horizon-europe-2021-2027?locale=en
- Zenodo DOI for this project: https://doi.org/10.5281/zenodo.20177633
- Zenodo repository record for this project: https://zenodo.org/records/20177633
- Repository license statement: [`README.md`](/root/i2fvg/README.md) (`CC-BY-4.0`)
