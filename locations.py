from queries import admissions
from tool import map_date

def main():
    for adm in admissions()[0:5]:
        print(make_json(adm))

def make_json(mimic):
    return {
        "resourceType": "Location",
        "id": "ph",
        "status": "active",
        "name": "Patient's Home",
        "description": "Patient's Home",
        "mode": "kind",

        "identifier": [{
            "system": "https://physionet.org/content/mimiciii/admission",
            "value": "##this is my id##"
        }],
        "type": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                "code": "PTRES",
                "display": "Patient's Residence"
            }]
        }],
        "physicalType": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/location-physical-type",
                "code": "ho",
                "display": "House"
            }]
        },


#origin = [
# 'CLINIC REFERRAL/PREMATURE',
# 'EMERGENCY ROOM ADMIT',
# 'PHYS REFERRAL/NORMAL DELI',
# 'TRANSFER FROM HOSP/EXTRAM',
# 'TRANSFER FROM SKILLED NUR']


#destination = [
# 'DEAD/EXPIRED',
# 'DISCH-TRAN TO PSYCH HOSP',
# 'HOME',
# 'HOME HEALTH CARE',
# 'HOME WITH HOME IV PROVIDR',
# 'HOSPICE-HOME',
# 'ICF',
# 'LONG TERM CARE HOSPITAL',
# 'REHAB/DISTINCT PART HOSP',
# 'SNF']


#'ICF' [Intermediate Care Facility]
#'SNF' [Hospice and skilled nursing facility]