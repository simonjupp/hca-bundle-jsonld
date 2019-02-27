from rdflib.plugin import register, Parser
from rdflib import Graph, ConjunctiveGraph
import json

register('application/ld+json', Parser, 'rdflib_jsonld.parser', 'JsonLDParser')

graph = ConjunctiveGraph()


sample_v1 = {
"@context" : {
   "organ" : "http://purl.obolibrary.org/obo/UBERON_0000062"
 },
 "biomaterial_id": "Specimen_PBMC2",
 "ncbi_taxon_id": 9606,
 "organ": "blood"
}


graph.parse(data=json.dumps(sample_v1), format="json-ld")

qres = graph.query("SELECT ?organ WHERE { ?s <http://purl.obolibrary.org/obo/UBERON_0000062> ?organ}")

for row in qres:
    print("%s" % row)

graph = ConjunctiveGraph()

graph.parse("sample_v2.json", format="json-ld")

qres = graph.query("SELECT ?organ WHERE { ?s <http://purl.obolibrary.org/obo/UBERON_0000062> ?organ}")

for row in qres:
    print("%s" % row)
