# i2fvg

Data processing and visualization project for regional companies, financial data, and EU-funded projects. The project was implemented as project-thesis for the Master in Data Management and Curation, 2025-2026 edition, of the SISSA and Area Science Park.

This repository combines:

- Python scripts for data cleaning and preparation
- DCAT metadata generation for input and output datasets
- a Django web application for browsing the processed data

Some variable names and source-specific labels remain in Italian because of the nature of the original datasets.

## Overview

The project is designed to transform heterogeneous source files into a consistent local data platform.

Main data domains:

- company registry data for Friuli Venezia Giulia companies
- financial data from Infocamere
- EU project data from CORDIS
- DCAT metadata describing datasets and processed outputs

The final result is a set of normalized CSV files, a local SQLite database, and a Django interface for navigating companies, financial indicators, and project participation.

## Repository structure

```text
i2fvg/
|-- data/
|   |-- company_registry/
|   |-- financial/
|   `-- eu_projects/
|       |-- h2020/
|       |-- horizon_europe/
|       `-- merge/
|-- django_project/
|   |-- manage.py
|   |-- config/
|   `-- i2fvg_mockup/
|-- script/
|   |-- 00_main.py
|   |-- 01_01_input_to_dcat.py
|   |-- 01_02_company_registry.py
|   |-- 01_03_output_to_dcat.py
|   |-- 02_01_eu_projects_download.py
|   |-- 02_02_eu_input_DCAT.py
|   |-- 02_03_eu_projects_merging.py
|   |-- 02_04_eu_merge_DCAT.py
|   |-- 03_01_financial_input_to_dcat.py
|   |-- 03_02_financial.py
|   |-- 03_03_financial_output_to_dcat.py
|   `-- 04_01_django_import_sqlite.py
|-- Dockerfile
|-- docker-compose.yml
`-- requirements.txt
```

## Project components

### 1. Data processing scripts

The folder [`script/`](/root/i2fvg/script) contains the ETL pipeline.

Main responsibilities:

- detect and load source files from `data/`
- clean and normalize company registry data
- validate and process financial data
- download and merge EU project datasets
- generate DCAT metadata for raw and processed files
- import processed CSV files into the Django SQLite database

The launcher [`script/00_main.py`](/root/i2fvg/script/00_main.py) executes all Python scripts in alphabetical order and supports exclusions.

### 2. Data area

The folder [`data/`](/root/i2fvg/data) contains local input and output files.

Tracked folders:

- [`data/company_registry/`](/root/i2fvg/data/company_registry)
- [`data/financial/`](/root/i2fvg/data/financial)
- [`data/eu_projects/h2020/`](/root/i2fvg/data/eu_projects/h2020)
- [`data/eu_projects/horizon_europe/`](/root/i2fvg/data/eu_projects/horizon_europe)
- [`data/eu_projects/merge/`](/root/i2fvg/data/eu_projects/merge)

Generated datasets are ignored by Git, except for placeholder `.gitkeep` files.

### 3. Django web application

The folder [`django_project/`](/root/i2fvg/django_project) contains the local web application.

The app [`i2fvg_mockup`](/root/i2fvg/django_project/i2fvg_mockup) imports processed CSV outputs into SQLite and exposes dashboards and detail pages for companies, financial data, and EU projects.

## Files (Python scripts only)

- `00_main.py` - Launcher that executes all `.py` scripts in the `script` folder in alphabetical order.
- `01_01_input_to_dcat.py` - Produce DCAT metadata for raw company Excel files.
- `01_02_company_registry.py` - Clean and prepare company registry data and export processed CSV outputs.
- `01_03_output_to_dcat.py` - Produce DCAT metadata for processed company registry CSV files.
- `02_01_eu_projects_download.py` - Download and extract EU project data from CORDIS.
- `02_02_eu_input_DCAT.py` - Produce DCAT metadata for downloaded EU project files.
- `02_03_eu_projects_merging.py` - Merge and clean EU project datasets into `data/eu_projects/merge`.
- `02_04_eu_merge_DCAT.py` - Produce per-file DCAT metadata for merged EU project CSV files.
- `03_01_financial_input_to_dcat.py` - Produce DCAT metadata for raw company financial files.
- `03_02_financial.py` - Validate and process financial data and export processed CSV outputs.
- `03_03_financial_output_to_dcat.py` - Produce DCAT metadata for processed financial CSV outputs.
- `04_01_django_import_sqlite.py` - Run Django `manage.py import_i2fvg_data` to import processed CSV data into SQLite.

## Expected source files

## Demo note

To make the project runnable out of the box, the repository currently includes a small set of placeholder input files in `data/company_registry/` and `data/financial/`.

These files are intentionally fictitious in almost all fields. Only the VAT numbers (`partite IVA`) are real, so the project can still be used to match companies and download related EU project data.

Do not treat the company registry or financial values contained in these bundled sample files as real business information.

### Company registry

[`script/01_02_company_registry.py`](/root/i2fvg/script/01_02_company_registry.py) auto-detects the latest available file matching:

```text
data/company_registry/imprese_fvg_MM_YYYY.xlsx
```

It expects the Excel workbook to contain these sheets:

- `FRIULI Anagrafica`
- `FRIULI codice attività`

### Financial data

The financial pipeline expects one of the following:

```text
data/financial/infocamere_YYYY.csv
data/financial/infocamere_YYYY.xlsx
```

### EU project data

EU project files are downloaded automatically from CORDIS by [`script/02_01_eu_projects_download.py`](/root/i2fvg/script/02_01_eu_projects_download.py).

The script stores downloaded and extracted files under:

- `data/eu_projects/h2020/`
- `data/eu_projects/horizon_europe/`

## Main processed outputs

The Django import command expects these processed CSV files:

### Company registry

- `data/company_registry/i2fvg_company_registry_headquarters.csv`
- `data/company_registry/i2fvg_company_registry_filtered.csv`

### Financial data

- `data/financial/i2fvg_financial.csv`

### EU projects

- `data/eu_projects/merge/project.csv`
- `data/eu_projects/merge/organization.csv`
- `data/eu_projects/merge/euroscivoc.csv`

Additional `.json` files may be generated next to datasets as DCAT metadata outputs.

## `cols_dict.xlsx`

Location: [`script/cols_dict.xlsx`](/root/i2fvg/script/cols_dict.xlsx)

This Excel workbook contains sheets used by the cleaning scripts to map and standardize column names from source files.

Common sheets:

- `anagrafica`: maps original column names from the `FRIULI Anagrafica` sheet to the standardized names used in [`01_02_company_registry.py`](/root/i2fvg/script/01_02_company_registry.py)
- additional mapping sheets are used for source-specific normalization where needed

Scripts read the appropriate sheet and build a dictionary pairing original column names with normalized ones before renaming DataFrame columns.

## Django data model

The main models are defined in [`django_project/i2fvg_mockup/models.py`](/root/i2fvg/django_project/i2fvg_mockup/models.py):

- `CompanyRegistryHeadquarters`
- `CompanyRegistryFiltered`
- `Financial`
- `Project`
- `Organization`
- `EuroSciVoc`

The import command [`django_project/i2fvg_mockup/management/commands/import_i2fvg_data.py`](/root/i2fvg/django_project/i2fvg_mockup/management/commands/import_i2fvg_data.py) clears the target tables and reloads all processed CSV files.

## Django pages

Main routes are defined in [`django_project/i2fvg_mockup/urls.py`](/root/i2fvg/django_project/i2fvg_mockup/urls.py):

- `/` - home page
- `/companies/` - company registry dashboard
- `/financial/` - financial dashboard
- `/eu-projects/` - EU projects dashboard
- `/companies/connected/` - companies linked to financial or project data
- `/companies/<cf>/` - company detail page
- `/projects/<project_id>/` - project detail page

The views aggregate and present information such as:

- active companies
- provincial distribution
- legal nature distribution
- yearly revenue summaries
- top companies by revenue
- H2020 and Horizon Europe participation
- EuroSciVoc classifications

## Launcher (`00_main.py`)

Run the launcher from the project root to execute all scripts in filename order:

```bash
python script/00_main.py
```

To exclude specific scripts, pass a comma-separated list of basenames without `.py`:

```bash
python script/00_main.py --exclude 02_01_eu_projects_download,04_01_django_import_sqlite
```

## Running the project locally

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Run the data pipeline

```bash
python script/00_main.py
```

You can also run single scripts individually if only part of the pipeline is needed.

### 3. Start Django

```bash
cd django_project
python manage.py migrate
python manage.py import_i2fvg_data
python manage.py runserver
```

Application URL:

```text
http://127.0.0.1:8000/
```

## Docker

The repository includes:

- [`Dockerfile`](/root/i2fvg/Dockerfile)
- [`docker-compose.yml`](/root/i2fvg/docker-compose.yml)

### Start the web application

```bash
docker compose up --build web
```

### Run the pipeline container

```bash
docker compose run --rm pipeline python script/00_main.py
```

The `web` service runs Django on port `8000`.  
The `pipeline` service mounts the full repository and is intended for data processing tasks.

## DCAT metadata

The project generates DCAT-like metadata for both source and processed datasets.

Dedicated scripts:

- [`01_01_input_to_dcat.py`](/root/i2fvg/script/01_01_input_to_dcat.py)
- [`01_03_output_to_dcat.py`](/root/i2fvg/script/01_03_output_to_dcat.py)
- [`02_02_eu_input_DCAT.py`](/root/i2fvg/script/02_02_eu_input_DCAT.py)
- [`02_04_eu_merge_DCAT.py`](/root/i2fvg/script/02_04_eu_merge_DCAT.py)
- [`03_01_financial_input_to_dcat.py`](/root/i2fvg/script/03_01_financial_input_to_dcat.py)
- [`03_03_financial_output_to_dcat.py`](/root/i2fvg/script/03_03_financial_output_to_dcat.py)

These metadata files describe:

- file structure
- row and column counts
- file timestamps
- provenance information
- semantic mappings where crosswalks are available

## Notes

- Real datasets are not versioned in this repository.
- The pipeline depends on consistent file naming inside `data/`.
- The CORDIS download step requires network access.
- Processed CSV files are imported with `|` as delimiter.
- The default database is local SQLite, configured in [`django_project/config/settings.py`](/root/i2fvg/django_project/config/settings.py).
- The current setup is intended for local development and exploration.

## Related documentation

- [`script/README.md`](/root/i2fvg/script/README.md) - script-specific notes
- [`requirements.txt`](/root/i2fvg/requirements.txt) - Python dependencies
- [`django_project/i2fvg_mockup/views.py`](/root/i2fvg/django_project/i2fvg_mockup/views.py) - dashboard logic

## License

CC-BY-4.0
