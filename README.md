# HCA Bundle JSON-LD

Representing HCA Bundles as JSON-LD allows them to be easily converted to RDF and queried using SPARQL.
This software, when combined with a graph or triplet store can provide semantic data models that 
allow for an expressive query interface.

## Usage

The "bundle_to_rdf" module presents a method for converting HCA bundles to RDF ttl files.

```
import requests
import bundle_to_rdf

DSS_URL = "https://dss.dev.data.humancellatlas.org/v1"
bundle_uuid = "4be0071d-b36e-4414-a7ee-7b879f60be7c"

r = requests.get("{}/bundles/{}?replica=aws".format(DSS_URL, bundle_uuid))
bundle = r.json()

file_name = bundle_to_rdf.bundle_to_rdf(bundle)
print(file_name)
```

A file is created in the current working directory with a filename following the pattern:
`{bundle_uuid}.ttl`.

This file can then be loaded into a triplet store of your choosing. For an example of usage with BlazeGraph, 
check out the `example-usage.ipynb`.

## Development

This module should make as few assumptions about the DSS data model as possible. Future developments would
use this module as part of a service to either create RDF that can be queried directly, or loaded into a
graph store like Blazegraph or Amazon Neptune.

### TODO

* Add unit tests, the module currently relies on active connections to the DSS
* Improve example notebook with biological use cases
* Demonstrate using the SPARQL and RDF interface to demonstrate tabular representations
* Integrate into a microservice for generating RDF from bundles on the fly

### Contributing

* Please add any issues you experience to our Github issue tracker!
* This software is Open Source, Apache licensed, send in your changes!

