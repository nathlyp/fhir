from queries import prescriptions
import json

def main():
    fhir_bundle_items = []

    for prescription in prescriptions():
        fhir_medication = map_fhir_medication(prescription)
        fhir_bundle_item = map_fhir_bundle_item(fhir_medication)
        fhir_bundle_items.append(fhir_bundle_item)

    fhir_bundle = map_fhir_bundle(fhir_bundle_items)
    
    #FROM: https://www.w3schools.com/python/python_json.asp
    print(json.dumps(fhir_bundle))

def map_fhir_medication(mimic):
    resource = {
        "resourceType": "MedicationRequest",
        "identifier": [{
            "system": "https://physionet.org/content/mimiciii/medication",
            "value": mimic["row_id"]
        }],
        "subject": {
            "type": "Patient",
            "reference": f"Patient?identifier={mimic['subject_id']}"
        },
        "encounter": {
            "type": "Encounter",
            "reference": f"Encounter?identifier={mimic['hadm_id']}"
        },
        "dispenseRequest": {
            "quantity": map_dispense_quantity(mimic)
        },
        "category": [{
            "coding": [{
                "display": mimic["drug_type"]
            }]
        }],
        "contained": [{
            "resourceType": "Medication",
            "code": {
                "coding": map_medication_coding(mimic)
            }
        }],
        "dosageInstruction": [{
            "sequence": 1,
            "text": mimic["prod_strength"],
            "route": {
                "coding": [{
                    "display": mimic["route"]
                }]
            },        
            "doseAndRate": [map_dose(mimic)]
        }],
    }
    if mimic["startdate"] or mimic["enddate"]:
        resource["dispenseRequest"]["validityPeriod"] = {}

    if mimic["startdate"]:
        resource["dispenseRequest"]["validityPeriod"]["start"] = mimic["startdate"].date().isoformat()

    if mimic["enddate"]:
        resource["dispenseRequest"]["validityPeriod"]["end"] = mimic["enddate"].date().isoformat()

    return resource

def map_dispense_quantity(mimic):
    val = mimic["form_val_disp"]
    if "-" in val:
        val = val.split("-")[1]

    return {
        "value": val,
        "unit": mimic["form_unit_disp"],
        "system": "http://unitsofmeasure.org",
    }

def map_dose(mimic):
    dose = {
        "type": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/dose-rate-type",
                "code": "ordered",
                "display": "Ordered"
            }]
        }
    }

    if "-" in mimic["dose_val_rx"]:
        val = mimic["dose_val_rx"].split("-")

        dose["doseRange"] =  {
            "low": {
                "value": val[0],
                "unit": mimic["dose_unit_rx"],
                "system": "http://unitsofmeasure.org"
            },
            "high": {
                "value": val[1],
                "unit": mimic["dose_unit_rx"],
                "system": "http://unitsofmeasure.org"
            }
        }
    else:
        dose["doseQuantity"] = {
            "value": mimic["dose_val_rx"],
            "unit": mimic["dose_unit_rx"],
            "system": "http://unitsofmeasure.org",
        }
    
    return dose

#https://bioportal.bioontology.org/ontologies/NDDF?p=classes&conceptid=050783
#https://ndclist.com/ndc/43742-0561
#https://www.centralhealth.net/map-and-map-basic-formulary/
def map_medication_coding(mimic):
    codes = []

    if mimic["formulary_drug_cd"] is not None:
        codes.append({
            "system": "https://mimic.mit.edu/docs/iii/tables/prescriptions/",
            "code": mimic["formulary_drug_cd"],
            "display": mimic["drug"]
        })

    if mimic["gsn"] is not None:
        codes.append({
            "system": "https://www.centralhealth.net/map-and-map-basic-formulary/",
            "code": mimic["gsn"],
            "display": mimic["drug"]
        })

    if mimic["ndc"] is not None:
        codes.append({
            "system": "https://ndclist.com/search",
            "code": mimic["ndc"],
            "display": mimic["drug"]
        })
    
    return codes

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