#!/usr/bin/env python
from queries import patients
import json

def main():
    fhir_bundle_items = []

    for patient in patients():
        fhir_patient = map_fhir_patient(patient)
        fhir_bundle_item = map_fhir_bundle_item(fhir_patient)
        fhir_bundle_items.append(fhir_bundle_item)

    fhir_bundle = map_fhir_bundle(fhir_bundle_items)
    
    #FROM: https://www.w3schools.com/python/python_json.asp
    print(json.dumps(fhir_bundle))

def map_fhir_patient(mimic):
    """Map the MIMIC dictionary into a FHIR"""
    fhir = {
        "resourceType": "Patient",
        "identifier": [{
            "system": "https://physionet.org/content/mimiciii/patient",
            "value": mimic["subject_id"]
        }],
        "gender": map_gender(mimic["gender"]),
        "birthDate": mimic["dob"].date().isoformat(), #datetime in FHIR are in iso 8601 #FROM: https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python
    }

    if (mimic["expire_flag"]):
        #datetime in FHIR are in iso 8601 #FROM: https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python
        fhir["deceasedDateTime"] = mimic["dod"].isoformat()
    else:
        fhir["deceasedBoolean"] = False
    
    return fhir

def map_fhir_bundle_item(fhir_patient):
    """Map the FHIR patient into bundle item"""
    return {
        "request": {
            "method": "POST",
            "url": "Patient"
        },
        "resource": fhir_patient
    }

def map_fhir_bundle(bundle_items):
    """Map the FHIR bundle items into a single bundle"""
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": bundle_items
    }

def map_gender(gender):
    """Map a MIMIC gender string into a FHIR gender"""
    if (gender == "M"):
        return "male"
    elif (gender == "F"):
        return "female"
    
    raise Exception("There was an error mapping gender: " + gender)

main()