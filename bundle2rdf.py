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

from pmap import pmap
from rdflib.plugin import register, Parser
from rdflib import Graph

# Initialize JSONLDParser
register('application/ld+json', Parser, 'rdflib_jsonld.parser', 'JsonLDParser')

# The context to inject into each bundle
context = {
    "@base": "http://rdf.data.humancellatlas.org/",
    "@vocab" : "http://rdf.data.humancellatlas.org/",
    "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "NCBITaxon" : "http://purl.obolibrary.org/obo/NCBITaxon_",
    "UBERON" : "http://purl.obolibrary.org/obo/UBERON_",
    "ontology" : {
      "@type": "@vocab"
    },
    "describedBy": {
      "@type": "@id",
      "@id": "rdf:type"
    },
    "document_id" :  {
      "@type": "@id"
    },
    "source_id" : "@id",
    "destination_id" : {
      "@type" : "@id",
      "@id" : "links"
    }
  }

INGEST_DOMAIN = "api.ingest"
DSS_DOMAIN = "dss"
HCA_DOMAIN = "dev.data.humancellatlas.org"


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
    bundle["@context"] = context
    bundle["@id"] = file_url
    graph.parse(data=json.dumps(bundle), format='json-ld')

    return graph


def bundle_to_graph(bundle):
    g = Graph()
    for file in bundle['bundle']['files']:
        if "dcp-type=\"metadata/" in file['content-type']:
            print(file['content-type'])
            g = add_to_graph(g, file['uuid'])
    # then get the links.json from the bundle
    return g


def main(argv=None):
    bundle_uuid = argv[0]
    bundle = get_bundle(bundle_uuid)
    g = bundle_to_graph(bundle)
    g.serialize(destination="{}.ttl".format(bundle_uuid), format='ttl')
    print("Done!")


if __name__ == "__main__":
    main(sys.argv[1:])