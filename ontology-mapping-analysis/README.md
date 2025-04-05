# Ontology Mapping Analysis

## Overview
Code to extract mappings from an ontology and use those to find matches to Mondo.

## Prerequisites
- ROBOT https://robot.obolibrary.org/
- Python
- Jupyter Notebook

## Workflow
1. Extract mappings from ontology of interest using SPARQL
1. Extract all mappings from Mondo (these are found as database cross references)
1. Analyze in a Jupyter notebook to find matches


### IRD Analysis
- Download OWL file from BioPortal https://bioportal.bioontology.org/ontologies/IRD3/?p=summary
- Review ontology for mappings of interest in Protege
  - Annotation properties: CUI, ICD-11, OMIM, ORPHA, SNOMED
- Use SPARQL and ROBOT to extract the values from these mapping annotation properties along with the IRI and label of the IRD terms. NOTE: IRD does not use CURIEs, but IRIs that contain the term label, e.g. http://www.semanticweb.org/msh/ontologies/2023/1/IRD#Diffuse_Photoreceptor_Dystrophies


### Extract mappings from Mondo
1. Get the latest tagged release version of `mondo.owl` as:
`wget https://github.com/monarch-initiative/mondo/releases/download/v2025-04-01/mondo.owl -O data/mondo.owl`
1. Use ROBOT to extract out xrefs as: 
`robot query -i data/mondo.owl --query sparql/extract_mondo_xrefs.sparql reports/mondo_xrefs.tsv`


### Extract mappings from Ontology of Interest
1. Write specific query to extract the mappings from the ontology of interest
1. Use ROBOT to extract mappings, e.g. 
`robot query -i data/Inherited\ Retinal\ Dystrophy.owl --query sparql/extract_ird_mappings.sparql reports/ird_xrefs.tsv`


### Find matches
1. Use Python or a Jupyter notebook to find matches from your ontology of interest to Mondo terms. NOTE: Even if a term in your ontology of interest has multiple mappings to other ontologies, there is no guarentee that _all_ of those mappings will map to the same Mondo term. For example if term FAVONT:0000001 has mappings to UMLS:C1234567 and Orphanet:0000, that does not mean that there will be one Mondo term that also has those same UMLS and Orphanet mappings.

