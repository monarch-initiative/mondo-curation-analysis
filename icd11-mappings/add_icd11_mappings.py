#!/usr/bin/env python3
"""
This script:
1. Reads ROBOT-extracted mapping files (created from MONDO ontology)
2. Loads your input TSV file
3. Adds ICD11 mappings based on CURIE column
4. Outputs enhanced TSV with ICD11 mappings (saved to the local data/ directory by default)
"""

import pandas as pd
import argparse
import sys
from pathlib import Path


def load_mappings(mondo_icd11_file, icd10_mondo_file):
    """Load the ROBOT-extracted mapping files into dictionaries."""
    print(f"Loading MONDO -> ICD11 mappings from {mondo_icd11_file}...")
    mondo_icd11_df = pd.read_csv(mondo_icd11_file, sep='\t')
    
    # ROBOT outputs column names with ? prefix (SPARQL convention), strip them
    mondo_icd11_df.columns = mondo_icd11_df.columns.str.replace('?', '', regex=False)
    
    # Group by MONDO CURIE to get all ICD11 mappings per term
    mondo_to_icd11 = mondo_icd11_df.groupby('mondo_curie')['icd11_xref'].apply(list).to_dict()
    print(f"  Loaded {len(mondo_to_icd11)} MONDO terms with ICD11 mappings")
    
    print(f"Loading ICD10 -> MONDO mappings from {icd10_mondo_file}...")
    icd10_mondo_df = pd.read_csv(icd10_mondo_file, sep='\t')
    
    # ROBOT outputs column names with ? prefix (SPARQL convention), strip them
    icd10_mondo_df.columns = icd10_mondo_df.columns.str.replace('?', '', regex=False)
    
    # Group by ICD10 CURIE to get all MONDO terms per ICD10 code
    icd10_to_mondo = icd10_mondo_df.groupby('icd10_xref')['mondo_curie'].apply(list).to_dict()
    print(f"  Loaded {len(icd10_to_mondo)} ICD10 codes with MONDO mappings")
    
    return mondo_to_icd11, icd10_to_mondo


def get_icd11_mappings(curie, mondo_to_icd11, icd10_to_mondo):
    """
    Get ICD11 mappings for a given CURIE.
    
    Args:
        curie: The CURIE string (e.g., "MONDO:0000001" or "ICD10CM:H35.5")
        mondo_to_icd11: Dictionary mapping MONDO CURIEs to lists of ICD11 mappings
        icd10_to_mondo: Dictionary mapping ICD10 CURIEs to lists of MONDO CURIEs
    
    Returns:
        List of ICD11 mappings (CURIEs)
    """
    if pd.isna(curie) or not curie:
        return []
    
    curie_str = str(curie).strip()
    
    # If it's a MONDO CURIE, get ICD11 directly
    if curie_str.startswith("MONDO:"):
        return mondo_to_icd11.get(curie_str, [])
    
    # If it's an ICD10 CURIE, find MONDO terms first, then get their ICD11 mappings
    elif curie_str.startswith("ICD10") or curie_str.startswith("icd10"):
        mondo_terms = icd10_to_mondo.get(curie_str, [])
        icd11_mappings = []
        for mondo_term in mondo_terms:
            icd11_mappings.extend(mondo_to_icd11.get(mondo_term, []))
        # Remove duplicates while preserving order
        return list(dict.fromkeys(icd11_mappings))
    
    # Not a MONDO or ICD10 term
    return []


def main():
    parser = argparse.ArgumentParser(
        description='Add ICD11 mappings to a TSV file based on MONDO to ICD11 mappings or ICD10 CURIEs in the input file where a Mondo term has both the ICD10 mapping and an ICD11 mapping'
    )
    parser.add_argument(
        'input_tsv',
        help='Input TSV file with columns: "BDC or Data Label", "CURIE", "CURIE label"'
    )
    parser.add_argument(
        '--mondo-icd11',
        default='data/mondo_icd11_mappings.tsv',
        help='Path to ROBOT-extracted MONDO->ICD11 mappings TSV (default: data/mondo_icd11_mappings.tsv)'
    )
    parser.add_argument(
        '--mondo-icd10',
        default='data/icd10_mondo_mappings.tsv',
        help='Path to ROBOT-extracted ICD10->MONDO mappings TSV (default: data/icd10_mondo_mappings.tsv)'
    )
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Output TSV file (default: data/<input_file>_with_icd11.tsv)'
    )
    parser.add_argument(
        '--curie-column',
        default='CURIE',
        help='Name of the column containing CURIEs (default: "CURIE")'
    )
    
    args = parser.parse_args()
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir / 'data'
    
    # Check input file exists
    input_path = Path(args.input_tsv)
    if not input_path.is_absolute():
        input_path = (Path.cwd() / input_path).resolve()
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input_tsv}", file=sys.stderr)
        sys.exit(1)
    
    # Check mapping files exist
    mondo_icd11_path = Path(args.mondo_icd11)
    if not mondo_icd11_path.is_absolute():
        mondo_icd11_path = (script_dir / mondo_icd11_path).resolve()
    icd10_mondo_path = Path(args.mondo_icd10)
    if not icd10_mondo_path.is_absolute():
        icd10_mondo_path = (script_dir / icd10_mondo_path).resolve()
    
    if not mondo_icd11_path.exists():
        print(f"Error: MONDO->ICD11 mappings file not found: {mondo_icd11_path}", file=sys.stderr)
        print(f"  Run: robot query -i mondo.owl -q sparql/extract_mondo_icd11.sparql {mondo_icd11_path}", file=sys.stderr)
        sys.exit(1)
    
    if not icd10_mondo_path.exists():
        print(f"Error: ICD10->MONDO mappings file not found: {icd10_mondo_path}", file=sys.stderr)
        print(f"  Run: robot query -i mondo.owl -q sparql/extract_icd10_mondo.sparql {icd10_mondo_path}", file=sys.stderr)
        sys.exit(1)
    
    # Determine output file
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = (Path.cwd() / output_path).resolve()
    else:
        output_path = data_dir / f"{input_path.stem}_with_icd11{input_path.suffix}"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load mappings
    mondo_to_icd11, icd10_to_mondo = load_mappings(mondo_icd11_path, icd10_mondo_path)
    
    # Load input TSV
    print(f"\nLoading input file: {args.input_tsv}...")
    df = pd.read_csv(input_path, sep='\t')
    print(f"  Loaded {len(df)} rows")
    
    # Check if CURIE column exists
    if args.curie_column not in df.columns:
        print(f"Error: Column '{args.curie_column}' not found in input file.", file=sys.stderr)
        print(f"  Available columns: {', '.join(df.columns)}", file=sys.stderr)
        sys.exit(1)
    
    # Add ICD11 mappings as comma-separated string
    print("\nAdding ICD11 mappings...")
    icd11_mappings_list = df[args.curie_column].apply(
        lambda x: get_icd11_mappings(x, mondo_to_icd11, icd10_to_mondo)
    )
    
    # Create string column with comma-separated values
    df['ICD11_mappings'] = icd11_mappings_list.apply(
        lambda x: ', '.join(x) if x else ''
    )
    
    # Count statistics
    rows_with_mappings = icd11_mappings_list.apply(lambda x: len(x) > 0).sum()
    total_icd11_mappings = icd11_mappings_list.apply(len).sum()
    
    print(f"  Rows with ICD11 mappings: {rows_with_mappings} / {len(df)}")
    print(f"  Total ICD11 mappings found: {total_icd11_mappings}")
    
    # Save output
    print(f"\nSaving output to: {output_path}")
    df.to_csv(output_path, sep='\t', index=False)
    print("Done!")


if __name__ == '__main__':
    main()

