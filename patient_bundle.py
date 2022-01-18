#!/usr/bin/env python

import csv
import json
from datetime import datetime

def migrate_patient(path):
    """
    Reads a csv file and maps every row into a fhir object
    FROM: https://realpython.com/python-csv/
    """
    fhir_bundle_items = []
    with open(path) as csv_file:
        line_count = 0
        csv_reader = csv.reader(csv_file, delimiter=",")
        for csv_row in csv_reader:
            line_count += 1
            if line_count > 1:
                mimic_patient = get_mimic_patient(csv_row)
                fhir_patient = map_fhir_patient(mimic_patient)
                fhir_bundle_item = map_fhir_bundle_item(fhir_patient)
                fhir_bundle_items.append(fhir_bundle_item)

    fhir_bundle = map_fhir_bundle(fhir_bundle_items)
    
    #FROM: https://www.w3schools.com/python/python_json.asp
    print(json.dumps(fhir_bundle))


def get_mimic_patient(csv_row):
    """Read the csv columns relevant to the MIMIC patient mapping and return an dictionary"""
    return {
        "subject_id": int(csv_row[1]),
        "gender": csv_row[2],
        "dob": map_date(csv_row[3]),
        "dod": map_date(csv_row[4]),
        "expire_flag": csv_row[7] == '1'
    }

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

def map_date(date):
    """
    Map a string date from into a python date
    FROM: https://stackoverflow.com/questions/466345/converting-string-into-datetime
    """
    if (not date):
        return None
    elif (len(date) == 19):
        return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    
    raise Exception("There was an error mapping date: " + date)

def map_gender(gender):
    """Map a MIMIC gender string into a FHIR gender"""
    if (gender == "M"):
        return "male"
    elif (gender == "F"):
        return "female"
    
    raise Exception("There was an error mapping gender: " + gender)

migrate_patient("/home/jose/Projects/Natha/fhir/dataset/PATIENTS-v2.csv")
