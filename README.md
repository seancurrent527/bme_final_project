# bme_final_project
Final Project repository for BME 477/577.

This repository implements much of the FHIR data standard into Google Protocol Buffers.
It further implements a restructuring of Patient EHR data generated by Synthea into a object-oriented record schema.

Files:

customized.proto - Restructed patient schema.

original.proto - Intial proto of the FHIR data.

json_parsing.py - Parsing of the FHIR JSON to assist in writing .proto files.

proto_parsing.py - Conversion of JSON to Google Protobufs.

metrics.py = Simple metric calculations for reading and writing speed of JSON and Protobuf files.
