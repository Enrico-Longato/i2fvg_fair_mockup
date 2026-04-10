#!/usr/bin/env python3

"""
DCAT Metadata Generator for output CSV files
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

CROSSWALK_FILENAME = "crosswalk_copany_registry.json"

FILE_DESCRIPTIONS = {
    "imprese_company_registry.csv": "Repository export of company registry data cleaned and structured from the company_registry pipeline.",
    "imprese_codici.csv": "Repository export of company activity codes cleaned and structured from the company_registry pipeline.",
    "i2fvg_company_registry.csv": "Innovation Intelligence export of company registry data including local units outside FVG.",
    "i2fvg_ateco.csv": "Innovation Intelligence export of company activity codes including local units outside FVG.",
    "i2fvg_company_registry_filtered.csv": "Innovation Intelligence export filtered to keep only headquarters and local units in FVG.",
    "i2fvg_ateco_filtrato.csv": "Innovation Intelligence export of activity codes filtered to keep only headquarters and local units in FVG.",
    "i2fvg_company_registry_headquarters.csv": "Innovation Intelligence export containing only headquarters, including those outside FVG.",
    "i2fvg_ateco_sedi.csv": "Innovation Intelligence export of activity codes containing only headquarters, including those outside FVG.",
}

FILE_TAGS = {
    "imprese_company_registry.csv": ["repository"],
    "imprese_codici.csv": ["repository"],
    "i2fvg_company_registry.csv": ["innovation-intelligence"],
    "i2fvg_ateco.csv": ["innovation-intelligence"],
    "i2fvg_company_registry_filtered.csv": ["innovation-intelligence", "fvg-only"],
    "i2fvg_ateco_filtrato.csv": ["innovation-intelligence", "fvg-only"],
    "i2fvg_company_registry_headquarters.csv": ["innovation-intelligence", "headquarters-only"],
    "i2fvg_ateco_sedi.csv": ["innovation-intelligence", "headquarters-only"],
}


# =========================
# LOAD CROSSWALK
# =========================
def load_crosswalk(data_dir: Path):
    path = data_dir / CROSSWALK_FILENAME

    if not path.exists():
        print(f"Warning: crosswalk not found in {data_dir}")
        return {}

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f).get("_crosswalk", {})
    except Exception as e:
        print(f"Warning: could not load crosswalk: {e}")
        return {}


# =========================
# FILE METADATA
# =========================
def get_file_metadata(path: Path) -> dict:
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
def get_csv_structure(path: Path, crosswalk: dict = None) -> dict:

    try:
        df_head = pd.read_csv(path, sep='|', nrows=0, dtype=str, encoding='utf-8-sig')
    except Exception:
        df_head = pd.read_csv(path, sep='|', nrows=0, encoding='latin1')

    try:
        df_sample = pd.read_csv(path, sep='|', nrows=500, dtype=str, encoding='utf-8-sig')
    except Exception:
        df_sample = pd.read_csv(path, sep='|', nrows=500, dtype=str, encoding='latin1')

    columns = list(df_head.columns)
    dtypes = {col: str(df_sample[col].dtype) for col in df_sample.columns}

    try:
        with path.open('r', encoding='utf-8', errors='ignore') as f:
            row_count = sum(1 for _ in f) - 1
            row_count = max(row_count, 0)
    except Exception:
        row_count = None

    unified_columns = []
    unmapped = []

    for col in columns:

        col_obj = {
            "name": col,
            "dtype": dtypes.get(col)
        }

        if crosswalk and col in crosswalk:
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
# DETECT SOURCE FILES
# =========================
def detect_source_excels(data_dir: Path) -> list:
    excels = list(data_dir.glob('imprese_fvg_*.xlsx'))
    return [str(p.name) for p in excels]


# =========================
# DCAT GENERATION
# =========================
def generate_dcat_for_csv(path: Path, provenance: dict = None, crosswalk: dict = None) -> dict:

    file_meta = get_file_metadata(path)
    structure = get_csv_structure(path, crosswalk=crosswalk)

    metadata = {
        "@context": {
            "dcat": "http://www.w3.org/ns/dcat#",
            "dcterms": "http://purl.org/dc/terms/",
            "prov": "http://www.w3.org/ns/prov#"
        },
        "@type": "dcat:Dataset",
        "dcterms:title": path.stem,
        "dcterms:description": FILE_DESCRIPTIONS.get(
            path.name,
            f"Dataset exported by the company_registry pipeline: {path.name}"
        ),
        "dcat:keyword": FILE_TAGS.get(path.name, []),
        "dcterms:issued": file_meta['created'],
        "dcterms:modified": file_meta['modified'],
        "dcat:distribution": {
            "dcat:accessURL": path.name,
            "dcat:mediaType": "text/csv",
            "bytes": file_meta['size_bytes']
        },
        "structure": structure,
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
    data_path = PROJECT_ROOT / "data" / "company_registry"

    data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else data_path

    catalog_out = None
    if '--catalog' in sys.argv:
        idx = sys.argv.index('--catalog')
        if idx + 1 < len(sys.argv):
            catalog_out = Path(sys.argv[idx + 1])

    if not data_dir.exists():
        print(f"Error: data directory not found: {data_dir}")
        sys.exit(1)

    crosswalk = load_crosswalk(data_dir)
    source_excels = detect_source_excels(data_dir)

    provenance_common = {
        "generated_by": "company_registry/script/01_02_company_registry.py",
        "generated_on": datetime.now().isoformat(),
        "source_excels": source_excels,
        "notes": "Derived outputs from the company_registry pipeline."
    }

    csv_files = list(data_dir.glob('*.csv'))

    if not csv_files:
        print(f"No CSV files found in {data_dir}")
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

        metadata = generate_dcat_for_csv(csv, provenance=prov, crosswalk=crosswalk)

        outpath = csv.with_suffix('.dcat.json')

        with outpath.open('w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"Wrote: {outpath}")

        catalog['datasets'].append({
            "title": metadata.get('dcterms:title'),
            "file": metadata['file_info']['filename'],
            "row_count": metadata['structure'].get('row_count'),
            "column_count": metadata['structure'].get('column_count')
        })

    if catalog_out is None:
        catalog_out = data_dir / 'DCAT_company_registry.json'

    with Path(catalog_out).open('w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"Aggregated catalog written to: {catalog_out}")


if __name__ == '__main__':
    main()