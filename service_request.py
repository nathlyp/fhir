#!/usr/bin/env python
from queries import services
import json

def main():
    fhir_bundle_items = []

    for service in services():
        if service['prev_service']:
            fhir_service_previous = map_fhir_service(service, True)
            fhir_bundle_item_previous = map_fhir_bundle_item(fhir_service_previous)
            fhir_bundle_items.append(fhir_bundle_item_previous)
        
        fhir_service = map_fhir_service(service)
        fhir_bundle_item = map_fhir_bundle_item(fhir_service)
        fhir_bundle_items.append(fhir_bundle_item)

    fhir_bundle = map_fhir_bundle(fhir_bundle_items)

    #FROM: https://www.w3schools.com/python/python_json.asp
    print(json.dumps(fhir_bundle))

def map_fhir_service(mimic, previous=False):
    """Map the MIMIC dictionary into a FHIR"""
    
    fhir = {
        "resourceType": "ServiceRequest",
        "identifier": [{
            "system": "https://physionet.org/content/mimiciii/service",
            "value": mimic["row_id"]
        }],
        "status": "active",
        "intent": "original-order",
        "occurrenceDateTime": mimic["transfertime"].isoformat(),
        "code": {
            "coding": [{
                "system": "https://mimic.mit.edu/docs/iii/tables/services",
                "code": mimic["curr_service"]
            }],
            "text": map_service(mimic["curr_service"])
        },
        "subject": {
            "type": "Patient",
            "reference": f"Patient?identifier={mimic['subject_id']}"
        },
        "encounter": {
            "type": "Encounter",
            "reference": f"Encounter?identifier={mimic['hadm_id']}"
        }
    }
    
    if mimic['prev_service'] and not previous:
        fhir['replaces'] = {
            "type": "ServiceRequest",
            "reference": f"ServiceRequest?identifier={mimic['row_id']}-prev"
        }

    if previous:
        fhir['identifier'] = [{
            "system": "https://physionet.org/content/mimiciii/service",
            "value": f"{mimic['row_id']}-prev"
        }]
        
        fhir['code']['text'] = map_service(mimic["prev_service"])
        fhir['code']['coding'] = [{
                "system": "https://mimic.mit.edu/docs/iii/tables/services",
                "code": mimic["curr_service"]
        }]
    
    return fhir

def map_fhir_bundle_item(fhir_service):
    """Map the FHIR service into bundle item"""
    return {
        "request": {
            "method": "POST",
            "url": "service"
        },
        "resource": fhir_service
    }

def map_fhir_bundle(bundle_items):
    """Map the FHIR bundle items into a single bundle"""
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": bundle_items
    }

def map_service(code):
    codes = {
        "CMED": "Cardiac Medical - for non-surgical cardiac related admissions",
        "CSURG": "Cardiac Surgery - for surgical cardiac admissions",
        "DENT": "Dental - for dental/jaw related admissions",
        "ENT": "Ear, nose, and throat - conditions primarily affecting these areas",
        "GU": "Genitourinary - reproductive organs/urinary system",
        "GYN": "Gynecological - female reproductive systems and breasts",
        "MED": "Medical - general service for internal medicine",
        "NB": "Newborn - infants born at the hospital",
        "NBB": "Newborn baby - infants born at the hospital",
        "NMED": "Neurologic Medical - non-surgical, relating to the brain",
        "NSURG": "Neurologic Surgical - surgical, relating to the brain",
        "OBS": "Obstetrics - conerned with childbirth and the care of women giving birth",
        "ORTHO": "Orthopaedic - surgical, relating to the musculoskeletal system",
        "OMED": "Orthopaedic medicine - non-surgical, relating to musculoskeletal system",
        "PSURG": "Plastic - restortation/reconstruction of the human body (including cosmetic or aesthetic)",
        "PSYCH": "Psychiatric - mental disorders relating to mood, behaviour, cognition, or perceptions",
        "SURG": "Surgical - general surgical service not classified elsewhere",
        "TRAUM": "Trauma - injury or damage caused by physical harm from an external source",
        "TSURG": "Thoracic Surgical - surgery on the thorax, located between the neck and the abdomen",
        "VSURG": "Vascular Surgical - surgery relating to the circulatory system"
    }

    if (code not in codes):
        return None
    
    return codes[code]

main()