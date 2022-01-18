from queries import procedures
import json

def main():
    fhir_bundle_items = []

    for procedure in procedures():
        fhir_procedure = map_fhir_procedure(procedure)
        fhir_bundle_item = map_fhir_bundle_item(fhir_procedure)
        fhir_bundle_items.append(fhir_bundle_item)

    fhir_bundle = map_fhir_bundle(fhir_bundle_items)
    
    #FROM: https://www.w3schools.com/python/python_json.asp
    print(json.dumps(fhir_bundle))

def map_fhir_procedure(mimic):
    return {
        "resourceType": "Procedure",
        "identifier": [{
            "system": "https://physionet.org/content/mimiciii/procedure",
            "value": mimic["row_id"]
        }],
        "status": "completed",
        "subject": {
            "type": "Patient",
            "reference": f"Patient?identifier={mimic['subject_id']}"
        },
        "encounter": {
            "type": "Encounter",
            "reference": f"Encounter?identifier={mimic['hadm_id']}"
        },
        "code": {
            "coding": [
            {
                "system": "https://mimic.mit.edu/docs/iii/tables/d_icd_procedures",
                "code": mimic['icd9_code'],
                "display": mimic['short_title'],
            }
            ],
            "text": mimic['long_title'],
        }
    }

def map_fhir_bundle_item(fhir_procedure):
    """Map the FHIR patient into bundle item"""
    return {
        "request": {
            "method": "POST",
            "url": "Procedure"
        },
        "resource": fhir_procedure
    }

def map_fhir_bundle(bundle_items):
    """Map the FHIR bundle items into a single bundle"""
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": bundle_items
    }

main()