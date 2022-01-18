from queries import admissions
import json

def main():
    fhir_bundle_items = []

    for admission in admissions():
        fhir_encounter = map_fhir_encounter(admission)
        fhir_bundle_item = map_fhir_bundle_item(fhir_encounter)
        fhir_bundle_items.append(fhir_bundle_item)

    fhir_bundle = map_fhir_bundle(fhir_bundle_items)
    
    #FROM: https://www.w3schools.com/python/python_json.asp
    print(json.dumps(fhir_bundle))

def map_fhir_encounter(mimic):
    length = (mimic["dischtime"] - mimic["admittime"]).seconds // 60
    return {
        "resourceType": "Encounter",
        "identifier": [{
            "system": "https://physionet.org/content/mimiciii/admission",
            "value": mimic["hadm_id"]
        }],
        "subject": {
            "type": "Patient",
            "reference": f"Patient?identifier={mimic['subject_id']}"
        },
        "serviceType": {
            "text": "admission"
        },
        "priority": {
            "coding": [ map_admission_type(mimic["admission_type"]) ]
        },
        "type": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "32485007",
                    "display": "Hospital admission (procedure)"
                }
            ]
        },
        "period": {
            "start": mimic["admittime"].isoformat(),
            "end": mimic["dischtime"].isoformat()
        },
        "serviceProvider": {
            "display" : mimic['insurance']
        },
        "length": {
            "value": length,
            "unit": "minutes",
            "system": "http://unitsofmeasure.org",
            "code": "min"
        },
        "diagnosis": [{
                "condition": {
                    "display": mimic["diagnosis"]
                },
                "use": {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/diagnosis-role",
                        "code": "AD",
                        "display": "Admission diagnosis"
                    }]
                },
                "rank": 1
            }
        ],
        "hospitalization": {
            "origin": {
                #"reference": f"Location?identifier={mimic['ADMISSION_LOCATION']}",
                "display": mimic['admission_location']
            },
            "destination": {
                #"reference": f"Location?identifier={mimic['DISCHARGE_LOCATION']}",
                "display": mimic['discharge_location']
            },
        }
    }

#https://terminology.hl7.org/2.1.0/CodeSystem-v3-ActPriority.html
#https://touchstone.aegis.net/touchstone/tsMessage?msgId=05dbeb4e-ded4-456a-88e6-7074c32d4b50-Resp&itemId=last+response&operation=+Encounter
def map_admission_type(type):
    code = ''
    display = ''
    system = ''
    system_snomed = 'http://snomed.info/sct'
    system_hl7 = 'http://terminology.hl7.org/CodeSystem/v3-ActPriority'

    if type == 'EMERGENCY':
        code = 'EM'
        display = 'emergency'
        system = system_hl7
    elif type == 'ELECTIVE':
        code = 'EL'
        display = 'elective'
        system = system_hl7
    elif type == 'URGENT':
        code = 'UR'
        display = 'urgent'
        system = system_hl7
    elif type == 'NEWBORN':
        code = '3950001'
        display = 'birth'
        system = system_snomed
    else:
        raise Exception(f"the admission_type '{type}' does not exist")

    return {
        "system": system,
        "code": code,
        "display": display
    }

def map_fhir_bundle_item(fhir_encounter):
    """Map the FHIR patient into bundle item"""
    return {
        "request": {
            "method": "POST",
            "url": "Encounter"
        },
        "resource": fhir_encounter
    }

def map_fhir_bundle(bundle_items):
    """Map the FHIR bundle items into a single bundle"""
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": bundle_items
    }

main()