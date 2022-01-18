from datetime import datetime

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