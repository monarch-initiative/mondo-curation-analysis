## OMIM Analysis

### Description
The goal is to find all Mondo IDs that have an xref to an OMIM ID where the OMIM ID entry is one that has an INCLUDED entry.

Steps:
1. Run a SPARQL query, using ROBOT, to get all OMIM CURIE and labels where the OMIM class contains the tag used to identify these entries, e.g. `rdfs:comment "This term has one or more labels that end with ', INCLUDED'." ;`. 
Example: `robot query -i omim.owl -q query-omim-included.sparql included-omim-ids.csv`

2. Filter this file to only OMIM CURIES by reading file into dataframe and write new dataframe with only ID column.

3. Use this list of OMIM CURIEs to query the content of `mondo-edit.obo` (using a static Mondo version converted to OWL using ROBOT) to get all Mondo IDs with xrefs to these INCLUDED OMIM IDs. These results are in `./sparql-from-file/results.txt`.
Example: `python run_query.py`

4. Analyze `results.txt` to get each Mondo ID, OMIM ID, and xref annotation to get all pairs of `MONDO:includedEntryInOMIM` and `MONDO:equivalentTo`.


NOTE: The static OWL files were extracted from the `mondo-ingest` repo from the July data build.