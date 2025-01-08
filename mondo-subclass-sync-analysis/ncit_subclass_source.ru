PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

# Get all Mondo classes and specific annotations where the SubclassOf source annotation is from NCIT

SELECT ?mondoIRI ?mondoLabel ?parentClass ?source (GROUP_CONCAT(?xref; separator=", ") AS ?xrefList)
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
         oboInOwl:source ?source .
  
  # Filter to include only subclass sources with "NCIT"
  FILTER(CONTAINS(?source, "NCIT"))

  # Match NCIT database cross-references
  OPTIONAL {
    ?mondoClass oboInOwl:hasDbXref ?xref .
    FILTER(STRSTARTS(STR(?xref), "NCIT:"))
  }
}
GROUP BY ?mondoIRI ?mondoLabel ?parentClass ?source
ORDER BY ?mondoIRI
