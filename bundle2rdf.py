#!/usr/bin/env python
"""
Description goes here
"""
__author__ = "jupp"
__license__ = "Apache 2.0"
__date__ = "21/03/2018"

from rdflib import Graph, plugin
from rdflib.serializer import Serializer
import json, urllib, requests
from rdflib.plugin import register, Parser
register('application/ld+json', Parser, 'rdflib_jsonld.parser', 'JsonLDParser')

context = {
    "@base": "http://rdf.data.humancellatlas.org/",
    "@vocab" : "http://rdf.data.humancellatlas.org/",
    "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "NCBITaxon" : "http://purl.obolibrary.org/obo/NCBITaxon_",
    "UBERON" : "http://purl.obolibrary.org/obo/UBERON_",
    "ontology" : {
      "@type": "@vocab"
  	},
    "describedBy" : {
      "@type": "@id",
      "@id": "rdf:type"
    },
    "document_id" :  "@id",
    "source_id" : "@id",
    "destination_id" : {
      "@type" : "@id",
      "@id" : "links"
    }
  }

def getBundleManifest(submissionEnvelope):

    url = "http://api.ingest.dev.data.humancellatlas.org/submissionEnvelopes/"+submissionEnvelope+"/bundleManifests"
    r = requests.get(url)
    return json.loads(r.text)

def addToGraph (graph, fileUuid):

    file = "https://dss.dev.data.humancellatlas.org/v1/files/" + fileUuid
    url = file + "?replica=aws"

    r = requests.get(url)
    bundle = json.loads(r.text)
    bundle["@context"] = context
    bundle["@id"] = file
    graph.parse(data=json.dumps(bundle), format='json-ld')

    return graph

def addLinksToGraph(graph, bundleUuid):

    file = "https://dss.dev.data.humancellatlas.org/v1/bundles/" + bundleUuid
    url = file + "?replica=aws"

    r = requests.get(url)
    bundle = json.loads(r.text)

    for file in bundle["bundle"]["files"]:
        if file["name"] == "links.json":
            print ("dumping links...")
            linksUuid = file["uuid"]
            addToGraph(graph, linksUuid)

    return graph

bundleManifest = getBundleManifest("5ab000205e93540007b86e04")

g = Graph()
for bundle in bundleManifest["_embedded"]["bundleManifests"]:
    for bioMaterialUuid in bundle["fileBiomaterialMap"].keys():
        print ("dumping biomaterials...")
        g = addToGraph(g, bioMaterialUuid)

    for fileProcessUuid in bundle["fileProcessMap"].keys():
        print ("dumping processes...")
        g = addToGraph(g, fileProcessUuid)

    for fileProtolocolUuid in bundle["fileProtocolMap"].keys():
        print ("dumping protocols...")
        g = addToGraph(g, fileProtolocolUuid)

    for fileUuids in bundle["fileFilesMap"].keys():
        print ("dumping files...")
        g = addToGraph(g, fileUuids)

    for projectUuid in bundle["fileProjectMap"].keys():
        print ("dumping project...")
        g = addToGraph(g, projectUuid)

    # then get the links.json from the bundle

    bundleUuid =bundle["bundleUuid"]
    g = addLinksToGraph(g, bundleUuid)


g.serialize(destination='output.ttl', format='ttl')
print("Done!")
