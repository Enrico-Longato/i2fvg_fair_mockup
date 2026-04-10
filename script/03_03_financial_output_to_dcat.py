#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd


CROSSWALK_FILENAME = "crosswalk_financial.json"


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
def get_csv_structure(path: Path, crosswalk: dict):

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
            if row_count < 0:
                row_count = 0
    except Exception:
        row_count = None

    unified_columns = []
    unmapped = []

    for col in columns:

        col_obj = {
            "name": col,
            "dtype": dtypes.get(col)
        }

        mapping = crosswalk.get(col)

        if mapping:
            col_obj["semantic"] = mapping
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
def detect_source_files(data_dir: Path):

    sources = list(data_dir.glob('infocamere_*.csv')) + \
              list(data_dir.glob('infocamere_*.xlsx'))

    return [str(p.name) for p in sources]


# =========================
# DCAT GENERATION
# =========================
def generate_dcat_for_csv(path: Path, provenance: dict, crosswalk: dict):

    file_meta = get_file_metadata(path)
    structure = get_csv_structure(path, crosswalk)

    metadata = {

        "@context": {
            "dcat": "http://www.w3.org/ns/dcat#",
            "dcterms": "http://purl.org/dc/terms/",
            "prov": "http://www.w3.org/ns/prov#"
        },

        "@type": "dcat:Dataset",

        "dcterms:title": path.stem,

        "dcterms:description": f"Dataset exported by the financial pipeline: {path.name}",

        "dcterms:issued": file_meta['created'],
        "dcterms:modified": file_meta['modified'],

        "dcat:distribution": {
            "dcat:accessURL": path.name,
            "dcat:mediaType": "text/csv",
            "bytes": file_meta['size_bytes']
        },

        "structure": structure,

        "provenance": provenance,
        "file_info": file_meta,
    }

    return metadata


# =========================
# MAIN
# =========================
def main():

    BASE_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = BASE_DIR.parent
    data_path = PROJECT_ROOT / "data" / "financial"

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

    source_files = detect_source_files(data_dir)

    provenance_common = {
        "generated_by": "financial/script/03_02_financial.py",
        "generated_on": datetime.now().isoformat(),
        "source_files": source_files,
        "notes": "Derived outputs from the financial pipeline."
    }

    csv_files = list(data_dir.glob('i2fvg_financial.csv'))

    if not csv_files:
        print(f"No financial CSV outputs found in {data_dir}")
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

        outpath = csv.with_suffix('.dcat.json')

        if outpath.exists():
            print(f"DCAT already exists: {outpath.name}")
            continue

        prov = provenance_common.copy()
        prov["source_file_detected"] = csv.name

        metadata = generate_dcat_for_csv(csv, prov, crosswalk)

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

    if catalog_out is None:
        catalog_out = data_dir / 'DCAT_financial.json'

    with catalog_out.open('w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"Aggregated catalog written to: {catalog_out}")


if __name__ == '__main__':
    main()