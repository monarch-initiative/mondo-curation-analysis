from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS

# Read xref values from the file
with open('omim_curies.csv', 'r') as file:
    xref_values = file.read().splitlines()

# Create a string for the VALUES clause
values_clause = ' '.join(f'"{xref}"' for xref in xref_values)

# Define the query with the VALUES clause
query = f"""
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?curie ?entityLabel ?xref ?source
WHERE {{
    VALUES ?xref {{ {values_clause} }}
    ?entity oboInOwl:hasDbXref ?xref .
    ?entity rdfs:label ?entityLabel .
    
    OPTIONAL {{
        ?anno a owl:Axiom ;
              owl:annotatedSource ?entity ;
              owl:annotatedProperty oboInOwl:hasDbXref ;
              owl:annotatedTarget ?xref ;
              oboInOwl:source ?source .
    }}
    FILTER(isIRI(?entity))
    BIND(REPLACE(STR(?entity), "http://purl.obolibrary.org/obo/MONDO_", "MONDO:") AS ?curie)
}}
"""

# Load the ontology
g = Graph()
g.parse('TEST-mondo-edit.owl')

# Execute the query
results = g.query(query)

# Print the results
#for row in results:
#    print(f"Entity: {row.entity}, Xref: {row.xref}, Source: {row.source}")

# Save the results to a file
with open('results.txt', 'w') as f:
    # Write the header line
    f.write("Entity, Label, Xref, Source\n")
    
    # Write the query results
    for row in results:
        curie = str(row.curie)
        label = str(row.entityLabel)
        xref = str(row.xref)
        source = str(row.source) if row.source else "None"
        f.write(f"{curie}, '{label}', {xref}, {source}\n")


print("Results saved to results.txt")
