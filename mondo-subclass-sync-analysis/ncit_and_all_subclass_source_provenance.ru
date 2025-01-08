PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

# Get all mondo classes that have a subclassOf annotation with a source value from NCIT, but also get all of the source values

SELECT ?mondoIRI ?mondoLabel ?parentClass ?ncitSource (GROUP_CONCAT(DISTINCT ?allSources; separator=", ") AS ?allSourceList) (GROUP_CONCAT(DISTINCT ?xref; separator=", ") AS ?xrefList)
WHERE {
   # Match MONDO classes and their subclass relationships
   ?mondoClass rdfs:subClassOf ?parentClass ;
              rdfs:label ?mondoLabel ;
              oboInOwl:id ?mondoIRI .
              
  # Match annotated axiom for subclass with source information
  ?axiom a owl:Axiom ;
         owl:annotatedSource ?mondoClass ;
         owl:annotatedProperty rdfs:subClassOf ;
         owl:annotatedTarget ?parentClass ;
         oboInOwl:source ?ncitSource .
  
  # Filter to include only subclass sources with "NCIT"
  FILTER(CONTAINS(?ncitSource, "NCIT"))
  
  # Collect all sources for the subclass axiom
  OPTIONAL {
    ?axiom oboInOwl:source ?allSources .
  }

  # Match NCIT database cross-references
  OPTIONAL {
    ?mondoClass oboInOwl:hasDbXref ?xref .
    FILTER(STRSTARTS(STR(?xref), "NCIT:"))
  }
}
GROUP BY ?mondoIRI ?mondoLabel ?parentClass ?ncitSource
ORDER BY ?mondoIRI
