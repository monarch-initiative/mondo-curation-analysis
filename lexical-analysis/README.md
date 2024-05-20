# Lexical Analysis

This repo is for experimental tests for alternative lexical alignment algorithms. 

For Mondo, when analyzing a resource to create mappings between Mondo and the external resource running the lexical alignment pipeline in the `mondo-ingest` repo there are two sets of files created for each external resource. These files are in the [`lexmatch` directory](https://github.com/monarch-initiative/mondo-ingest/tree/main/src/ontology/lexmatch).

- The "lex_exact" file, see [`unmapped_icd11foundation_lex_exact.tsv`](https://github.com/monarch-initiative/mondo-ingest/blob/main/src/ontology/lexmatch/unmapped_icd11foundation_lex_exact.tsv) contains all exact mappings between Mondo and the external resource. These mappings are exact lexical matches between the Mondo term label and the label of the external resource.

- The "lex" file, see [`unmapped_icd11foundation_lex.tsv`](https://github.com/monarch-initiative/mondo-ingest/blob/main/src/ontology/lexmatch/unmapped_icd11foundation_lex.tsv) contains matches (that appear to be exact) that are between the Mondo term label and synonym of the external resource and matches that are between a Mondo synonym and the external resource term label.


## General Thoughts/Hypothesis
- An exact match from a Mondo label to an exact synonym in an external resource most often should be a good match. If not, are there patterns that can be detected to include/exclude terms that should not be mapped from this category.

- There are cases where punctuation in the term label is causing the match to be reported in the "lex" file. For example:
    - In the [Mondo-->DOID lex file](https://github.com/monarch-initiative/mondo-ingest/blob/main/src/ontology/lexmatch/unmapped_doid_lex.tsv#L14), there is an extra comma in the Mondo term. Note: the `match_string` field lists `omim:620427` for this row.
        - MONDO:0957385	dystonia 37, early-onset, with striatal lesions
        - DOID:0060956	dystonia 37, early-onset with striatal lesions

- There are cases where the term labels contain the same tokens, but are reordered. For example:    
    - In the [Mondo-->DOID lex file](https://github.com/monarch-initiative/mondo-ingest/blob/main/src/ontology/lexmatch/unmapped_doid_lex.tsv#L15), there is this match where the term labels contain all the same tokens, just re-ordered and one contains a comma
        - MONDO:0968944	intellectual developmental disorder, autosomal recessive 82
        - DOID:0060947    autosomal recessive intellectual developmental disorder 82

- There are cases where there are multiple lines of evidence that the Mondo term should be mapped to the external resource term. For example:
    - In the [Mondo-->ICD11 Foundation file](https://github.com/monarch-initiative/mondo-ingest/blob/main/src/ontology/lexmatch/unmapped_icd11foundation_lex.tsv#L6-L8), there are 3 entries where the Mondo term "maps" to an ICD11 term. In one case it's a match between the Mondo label and an exact synonym in ICD11 and the other two entries are exact matches between exact synonyms of each term. This evidence taken together as a set should provide more information that the Mondo term should be mapped to this ICD11 term.

- There are cases where the difference between a term label is due to English vs. British spelling. There is a dictionary which exists for this case: https://github.com/monarch-initiative/mondo/blob/6d30c5acb9b68cb07bbe34ef0ac9d374acf9b2fd/src/ontology/mondo.Makefile#L873

- There are cases where the ICD11 term contains a value in () after the term. For example:
    - MONDO:0005227	abscess	icd11.foundation:2136477741	Abscess (TM2)	0.8	rdfs:label	oio:hasExactSynonym	abscess

- There are cases where the match is on the Mondo Label and ICD11 Synonym and the respective term names are subsets of one another. In cases like this _and_ where the ICD11 term is an exact match to another Mondo term then this is _NOT_ a correct match. For example:
    - MONDO:0000440	metabolic acidosis	icd11.foundation:1506336899	Acidosis	0.8	rdfs:label	oio:hasExactSynonym	metabolic acidosis

- There are cases where the same Mondo ID is mapped to two different ICD11 terms. For example:
```
MONDO:0000239	adiaspiromycosis	icd11.foundation:1111587867	MONDO:equivalentTo	Pulmonary adiaspiromycosis	0.8	oio:hasExactSynonym	oio:hasExactSynonym	adiaspiromycosis
MONDO:0000239	adiaspiromycosis	icd11.foundation:1111587867	MONDO:equivalentTo	Pulmonary adiaspiromycosis	0.8	oio:hasExactSynonym	rdfs:label	pulmonary adiaspiromycosis
MONDO:0000239	adiaspiromycosis	icd11.foundation:1111587867	MONDO:equivalentTo	Pulmonary adiaspiromycosis	0.8	rdfs:label	oio:hasExactSynonym	adiaspiromycosis
MONDO:0000239	adiaspiromycosis	icd11.foundation:139402453	MONDO:equivalentTo	Adiaspirosis	0.8	oio:hasExactSynonym	oio:hasExactSynonym	haplosporangiosis
MONDO:0000239	adiaspiromycosis	icd11.foundation:139402453	MONDO:equivalentTo	Adiaspirosis	0.8	oio:hasExactSynonym	rdfs:label	adiaspirosis
```

##  Analysis
- See Jupyter Notebook

