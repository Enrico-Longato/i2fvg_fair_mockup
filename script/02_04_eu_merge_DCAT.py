#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd


# =========================
# CONFIG
# =========================
CROSSWALK_PATH = Path("/root/i2fvg/data/eu_projects/merge/crosswalk_eu_projects.json")


# =========================
# LOAD CROSSWALK
# =========================
def load_crosswalk(section):
    if CROSSWALK_PATH.exists():
        with CROSSWALK_PATH.open(encoding="utf-8") as f:
            data = json.load(f)
            return data.get("_crosswalk", {}).get(section, {})
    return {}


# =========================
# SOURCE DATASETS (CORDIS)
# =========================
def get_source_datasets():
    return [
        {
            "@id": "https://data.europa.eu/api/hub/repo/datasets/cordis-eu-research-projects-under-horizon-europe-2021-2027.jsonld",
            "dcterms:title": "CORDIS Horizon Europe projects"
        },
        {
            "@id": "https://data.europa.eu/api/hub/repo/datasets/cordish2020projects.jsonld",
            "dcterms:title": "CORDIS Horizon 2020 projects"
        }
    ]


# =========================
# FILE METADATA
# =========================
def get_file_metadata(path: Path):
    stat = path.stat()
    return {
        "filename": path.name,
        "path": str(path),
        "size_bytes": stat.st_size,
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
    }


# =========================
# CSV STRUCTURE (UNIFIED)
# =========================
def get_csv_structure(path: Path):

    try:
        df_head = pd.read_csv(path, sep='|', nrows=0, encoding='utf-8-sig')
    except Exception:
        df_head = pd.read_csv(path, sep='|', nrows=0, encoding='latin1')

    try:
        df_sample = pd.read_csv(path, sep='|', nrows=500, encoding='utf-8-sig')
    except Exception:
        df_sample = pd.read_csv(path, sep='|', nrows=500, encoding='latin1')

    columns = list(df_head.columns)
    dtypes = {col: str(df_sample[col].dtype) for col in df_sample.columns}

    try:
        with path.open('r', encoding='utf-8', errors='ignore') as f:
            row_count = sum(1 for _ in f) - 1
            row_count = max(row_count, 0)
    except Exception:
        try:
            row_count = int(pd.read_csv(path, sep='|', usecols=[0]).shape[0])
        except Exception:
            row_count = None

    return columns, dtypes, row_count


# =========================
# BUILD UNIFIED STRUCTURE
# =========================
def build_structure(path: Path):

    section = path.stem  # project / organization / euroscivoc
    crosswalk = load_crosswalk(section)

    columns, dtypes, row_count = get_csv_structure(path)

    unified_columns = []
    unmapped = []

    for col in columns:

        col_obj = {
            "name": col,
            "dtype": dtypes.get(col)
        }

        if col in crosswalk:
            col_obj["semantic"] = crosswalk[col]
        else:
            unmapped.append(col)

        unified_columns.append(col_obj)

    return {
        "columns": unified_columns,
        "column_count": len(columns),
        "row_count": row_count,
        "unmapped_columns": unmapped
    }


# =========================
# DCAT GENERATION
# =========================
def generate_dcat_for_csv(path: Path, provenance: dict = None):

    file_meta = get_file_metadata(path)
    structure = build_structure(path)

    sources = get_source_datasets()

    metadata = {

        "@context": {
            "dcat": "http://www.w3.org/ns/dcat#",
            "dcterms": "http://purl.org/dc/terms/",
            "prov": "http://www.w3.org/ns/prov#"
        },

        "@type": "dcat:Dataset",

        "dcterms:title": path.stem,
        "dcterms:description": f"Merged dataset produced by 02_eu_projects_merging.py: {path.name}",

        "dcterms:issued": file_meta['created'],
        "dcterms:modified": file_meta['modified'],

        "dcat:distribution": {
            "dcat:accessURL": path.name,
            "dcat:mediaType": "text/csv",
            "bytes": file_meta['size_bytes']
        },

        "structure": structure,

        "dcterms:source": sources,
        "prov:wasDerivedFrom": [s["@id"] for s in sources],

        "provenance": provenance or {},
        "file_info": file_meta,
    }

    return metadata


# =========================
# MAIN
# =========================
def main():

    BASE_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = BASE_DIR.parent
    default_merge = PROJECT_ROOT / "data" / "eu_projects" / "merge"

    merge_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else default_merge

    if not merge_dir.exists():
        print(f"Error: merge directory not found: {merge_dir}")
        sys.exit(1)

    provenance_common = {
        "generated_by": "company_registry/script/02_eu_projects_merging.py",
        "generated_on": datetime.now().isoformat(),
        "notes": "Datasets produced by concatenating H2020 and Horizon Europe files."
    }

    csv_files = list(merge_dir.glob('*.csv'))

    if not csv_files:
        print(f"No CSV files found in {merge_dir}")
        sys.exit(0)

    catalog = {
        "@context": {
            "dcat": "http://www.w3.org/ns/dcat#",
            "dcterms": "http://purl.org/dc/terms/",
        },
        "@type": "dcat:Catalog",
        "dcterms:issued": datetime.now().isoformat(),
        "datasets": []
    }

    for csv in csv_files:

        prov = provenance_common.copy()
        prov["source_file_detected"] = csv.name

        metadata = generate_dcat_for_csv(csv, provenance=prov)

        outpath = csv.with_suffix('.dcat.json')

        with outpath.open('w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"Wrote: {outpath}")

        catalog['datasets'].append({
            "title": metadata.get('dcterms:title'),
            "file": metadata['file_info']['filename'],
            "dcat_json": outpath.name,
            "row_count": metadata['structure'].get('row_count'),
            "column_count": metadata['structure'].get('column_count')
        })

    catalog_out = merge_dir / "DCAT_eu_projects.json"

    with catalog_out.open('w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"Aggregated catalog written to: {catalog_out}")


if __name__ == '__main__':
    main()