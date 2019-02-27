#!/usr/bin/env python

from hca_bundle_jsonld import bundle_to_rdf as b2g

# first get the bundle from the DSS, this is a demo bundle in the new bundle format

bundle = b2g.get_bundle("8541a214-17d0-453c-8c83-16af625135ec")

# now apply the JSON-LD context to the bundle JSON files to get the RDF graph

graph = b2g.bundle_to_rdf(bundle)

# Query the bundle graph for all sample ids that are the input of the assay

# SPARQL query get a sample that is input to process, that has a file as output and returns the biomaterial id

sample_id_query =\
"""
PREFIX : <http://schema.humancellatlas.org/>

SELECT DISTINCT ?bio_id WHERE {
  ?sample :biomaterial_core [ :biomaterial_id ?bio_id] . 
  ?process :has_input ?sample ;
  		   :has_output [a :file] ;
 }
"""

print("")
print ("1. Get biomaterial id that is input to process and has a file as output:")
qres = graph.query(sample_id_query)

for row in qres:
    print("%s" % row)

# The next query gets all file metadata and uuid

data_file_query =\
"""
PREFIX : <http://schema.humancellatlas.org/>

SELECT DISTINCT ?bio_id ?file_uuid ?filename ?lane_index ?read_index WHERE {
  ?sample :biomaterial_core [ :biomaterial_id ?bio_id] . 
  ?process :has_input ?sample ;
  		   :has_output ?file . 
  ?file :lane_index ?lane_index ;
        :read_index ?read_index ;
        :document_id ?file_uuid ;
        :file_core [ :file_format ?format ;
            		 :file_name ?filename ] . 
 }
"""

print("")
print ("2. Get all file metadata and file uuid:")
qres = graph.query(data_file_query)

for row in qres:
    print("%s %s %s %s %s" % row)

# finally get all the fields for the orange box index

orange_box_query =\
"""
PREFIX : <http://schema.humancellatlas.org/>

SELECT DISTINCT ?bio_id ?filename ?organ ?organ_part ?species ?lib_construction ?age ?age_unit ?disease WHERE {

  # get the assay process
  ?process :has_input [ :biomaterial_core  [ :biomaterial_id ?bio_id] ].  
  ?process :has_output [ a :file ; :file_core [ :file_name ?filename ] ] .
                                 
  # get all input processes to assay process                               
  ?processes (:has_output / ^ :has_input)+ ?process .
                        
  # get biomaterial info from all processes                                         
  ?processes :has_output [ :organ [ :text ?organ ]] .
  ?processes :has_output [ :organ_part [ :text ?organ_part ]] .
  ?processes :has_output [ :genus_species [ :text ?species ]] .

  # get disease info
  OPTIONAL { ?processes :has_output [ :disease [ :text ?disease ]] }

  # get donor age info
  OPTIONAL { 
    ?processes :has_output [ :organism_age  ?age ] .
    ?processes :has_output [ :organism_age_unit [ :text ?age_unit ] ] 
  }

  # get library construction from protocol
  OPTIONAL { 
    ?process :has_protocol [ :library_construction_approach [ :text ?lib_construction ] ]. 
  }
                                     
 }
"""

print("")
print ("3. Get all the fields show in the portal data browser:")
qres = graph.query(orange_box_query)

for row in qres:
    print("%s %s %s %s %s %s %s %s %s" % row)