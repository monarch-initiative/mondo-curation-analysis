# Analysis of Subclass Sync Results for NCIT

## Description
The goals of this analysis are:
- Confirm that the only NCIT subclass source provenance added by the Subclass sync pipeline is from NCIT terms in the NCIT neoplasm branch
- Identify how many NCIT subclass source provenance annotations are lost from other Mondo terms because the Subclass Sync pipeline 
only syncs NCIT terms from the neoplasm branch. This should include the total number of Mondo classes where a NCIT subclass source
provenance is removed and a count of these Mondo classes where there is no longer any subclass source provenance. This should include the total number of 
non-neoplasm branch Mondo terms where a Subclass source provenance is removed as well as the total count of these Mondo classes where there is no longer any Subclass source provenance information for a given axiom. This will check if any of these subclass axioms now have no source provenance.


## Methods
### Extract Mondo classes that contain Subclass axioms that have a source annotation from NCIT
- Get a version of mondo-edit.obo _after_ the subclass sync pipeline was run, e.g. see PR [#8503](https://github.com/monarch-initiative/mondo/pull/8503)
in the mondo repo.
- Run a SPARQL query to extract information from mondo classes where the subclass source provenance includes at least one value 
from NCIT. Extract the mondo class curie, label, parent class, NCIT subclass source, and a list of any database crossreference values
that are also from NCIT.
- ROBOT command: `robot query -i mondo-edit_PR-8503.obo -q ncit_subclass_source.ru ncit_subclass_source_provenance.csv`

### Confirm Mondo classes with Subclass provenance information from NCIT are from NCIT terms in the neoplasm branch
- Use a SPARQL query to extract all subclasses of neoplasm in NCIT. Use the latest version of NCIT from the `mondo-ingest` repo, e.g. `~/git/mondo-ingest-NEW/src/ontology/tmp/component-download-ncit.owl.owl`.
- ROBOT command: `robot query -i component-download-ncit.owl.owl -q ncit_neoplasm_children.ru ncit_neoplasm_child_terms.csv` 


### Check number of Mondo classes with NCIT subclass source provenance before running Subclass Sync
- Get a version of `mondo-edit.obo` from master and therefore does not contain any changes from the Subclass Sync.
- Run the SPARQL query to extract all information from mondo classes where the subclass source provenance includes at least one value 
from NCIT. Extract the mondo class curie, label, parent class, NCIT subclass source, and a list of any database crossreference values
that are also from NCIT.
- ROBOT command: `robot query -i mondo-edit_master-6Jan2025.obo -q ncit_and_all_subclass_source_provenance.ru mondo-edit_all_ncit_subclass_source_provenance.csv`

## Analysis
See the Jupyter notebook named "NCIT SubclassOf Source and Xref Comparison"

## Results
There are 2,865 unique Mondo classes that have a total of 4,108 Subclass axioms where the source annotation includes a value from NCIT. Of these, 8 of the NCIT source values are malformed and need to be updated (see results in the `mismatch_rows` dataframe). Of the remaining Mondo classes with valid NCIT Subclass source annotation values, 57 unique NCIT values are not in the NCIT neoplasm branch.

There are 3,985 unique Mondo classes where a SubclassOf source annotation would be removed using the updated Subclass Sync pipeline (results found in PR #8503). Of these, there are 789 SubclassOf axioms that would no longer have a source annotation value using ths updated Subclass Sync pipeline.

