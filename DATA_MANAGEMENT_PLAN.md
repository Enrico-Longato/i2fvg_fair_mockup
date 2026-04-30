# Data Management Plan

## 1. Data Summary

The project “Innovation Intelligence FVG – FAIR Mockup” generates and reuses structured datasets related to companies in Friuli Venezia Giulia.

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

### 2.2 Making data accessible
- Data are accessible locally via repository structure and Django interface
- No restricted data are included in the public repository
- External datasets must be accessed according to their providers

### 2.3 Making data interoperable
- Data are standardized into CSV format
- Column mappings are defined in `cols_dict.xlsx`
- DCAT metadata provides semantic descriptions and structure

### 2.4 Increasing data re-use
- Processing scripts are fully reproducible
- Metadata document provenance and transformations
- Licensing conditions are clearly specified
- The workflow enables extension and reuse

---

## 3. Other Research Outputs

The project also produces:
- Python ETL scripts
- Django web application
- Data transformation workflows

These components are version-controlled and documented to ensure reproducibility.

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

---

## 6. Ethics

- The project does not process personal data in the public version
- Any real datasets must comply with GDPR and institutional policies
- Data providers’ licensing and usage constraints must be respected

---

## 7. Other Issues

- The DMP is a living document and may be updated during the project
- The repository is intended as a FAIR-compliant mockup and demonstration environment
- Real-world deployment would require additional infrastructure and governance policies

---

## 8. References

This Data Management Plan follows the structure and recommendations of the Horizon Europe Data Management Plan template provided by the European Commission:
https://ec.europa.eu/research/participants/documents/downloadPublic?documentIds=080166e502e83f42&appId=PPGMS