#!/usr/bin/env python
"""
Description goes here
"""
__author__ = "jupp"
__license__ = "Apache 2.0"
__date__ = "21/03/2018"

import json
import requests
import sys

from rdflib.plugin import register, Parser
from rdflib import Graph, ConjunctiveGraph

import rdflib_jsonld

# Initialize JSONLDParser
register('json-ld', Parser, 'rdflib_jsonld.parser', 'JsonLDParser')

# The context to inject into each bundle
context = {
    "@base": "http://schema.humancellatlas.org/",
    "@vocab" : "http://schema.humancellatlas.org/",
    "bundle_file" : "https://dss.dev.data.humancellatlas.org/v1/files/",
    "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "ontology" : {
      "@type": "@vocab"
    },
    "schema_type": {
      "@type": "@id",
      "@id": "rdf:type"
    },
    "uuid" :  {
      "@type": "@id"
    }
  }

INGEST_DOMAIN = "api.ingest"
DSS_DOMAIN = "dss"
HCA_DOMAIN = "data.humancellatlas.org"

def get_bundle_manifest(submission_envelope):
    url_template = "http://{}.{}/submissionEnvelopes/{}/bundleManifests"
    url = url_template.format(
        INGEST_DOMAIN, HCA_DOMAIN, submission_envelope)
    r = requests.get(url)
    return r.json()


def get_bundle(bundle_uuid):
    bundle_url = "https://{}.{}/v1/bundles/{}?replica=aws".format(
        DSS_DOMAIN, HCA_DOMAIN, bundle_uuid)
    r = requests.get(bundle_url)
    return r.json()


def add_to_graph(graph, file_uuid):
    file_url = "https://{}.{}/v1/files/{}".format(
        DSS_DOMAIN, HCA_DOMAIN, file_uuid)

    r = requests.get("{}{}".format(file_url, '?replica=aws'))

    bundle = r.json()
    content = bundle["content"]

    content["@context"] = context
    meta_file_url = "https://{}.{}/v1/files/{}".format(
        DSS_DOMAIN, HCA_DOMAIN,  bundle["uuid"])
    content["@id"] =meta_file_url
    content["document_id"] =bundle["uuid"]
    graph.parse(data=json.dumps(content), format='json-ld')

    return graph


def bundle_to_graph(bundle):
    g = ConjunctiveGraph()
    g.parse("links.json", format="json-ld")
    for file in bundle['bundle']['files']:
        if "dcp-type=\"metadata/" in file['content-type']:
            print(file['content-type'])
            g = add_to_graph(g, file['uuid'])
    # then get the links.json from the bundle
    return g


def bundle_to_rdf(bundle):
    bundle_uuid = bundle['bundle']['uuid']
    g = bundle_to_graph(bundle)
    g.serialize(destination="{}.ttl".format(bundle_uuid), format='ttl')
    print("Wrote file: {}.ttl".format(bundle_uuid))
    return g


def main(argv=sys.argv[1:]):
    bundle_uuid = argv[0]
    bundle = get_bundle(bundle_uuid)
    bundle_to_rdf(bundle)


if __name__ == "__main__":
    print(sys.argv)
    main(sys.argv[1:])
