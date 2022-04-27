import re
import sqlite3
from datetime import datetime
from contextlib import closing
from configuration import path_db

def __query(sql):
    """
    Execute the sql query in the sqlite database
    FROM: https://stackoverflow.com/questions/466345/converting-string-into-datetime
    """
    with closing(sqlite3.connect(path_db)) as connection:
        with closing(connection.cursor()) as cursor:
            return cursor.execute(sql).fetchall()

def sqlite_query_executor(query):
    conn=sqlite3.connect()
    cur=conn.cursor()

    while True:
        yield cur.execute(query).fetchone()[0]

def __query_gen(sql):
    with closing(sqlite3.connect(path_db)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql)
            meter_row = cursor.fetchone()
            while meter_row:
                yield meter_row
                meter_row = cursor.fetchone()

def patients():
    list = []
    rows = __query("SELECT * FROM patients")
    for row in rows:
        item = {
            "subject_id": int(row[1]),
            "gender": row[2],
            "dob": map_date(row[3]),
            "dod": map_date(row[4]),
            "expire_flag": row[7] == '1'
        }
        list.append(item)
    return list

def admissions():
    list = []
    rows = __query("SELECT * FROM admissions")
    for row in rows:
        item = {
            'subject_id': int(row[1]),
            'hadm_id': int(row[2]),
            'admittime': map_date(row[3]),
            'dischtime': map_date(row[4]),
            'deathtime': map_date(row[5]),
            'admission_type': row[6],
            'admission_location': row[7],
            'discharge_location': row[8],
            'insurance': row[9],
            'language': row[10],
            'religion': row[11],
            'marital_status': row[12],
            'ethnicity': row[13],
            'edregtime': map_date(row[14]),
            'edouttime': map_date(row[15]),
            'diagnosis': row[16],
            'hospital_expire_flag': row[17] == '1',
            'has_chartevents_data': row[18] == '1',
        }
        list.append(item)
    return list

def procedures():
    list = []
    rows = __query("""select procedures_icd.*, short_title,long_title
from procedures_icd
inner join D_ICD_PROCEDURES on procedures_icd.icd9_code == D_ICD_PROCEDURES.icd9_code""")

    for row in rows:
        item = {
            'row_id': int(row[0]),
            'subject_id': int(row[1]),
            'hadm_id': int(row[2]),
            'seq_num': int(row[3]),
            'icd9_code': int(row[4]),
            'short_title': row[5],
            'long_title': row[6]
        }
        list.append(item)
    return list

def services():
    list = []
    rows = __query("SELECT * FROM services")

    for row in rows:
        item = {
            'row_id': int(row[0]),
            'subject_id': int(row[1]),
            'hadm_id': int(row[2]),
            'transfertime': map_date(row[3]),
            'prev_service': row[4],
            'curr_service': row[5],
        }
        list.append(item)
    return list

def prescriptions():
    rows = __query_gen("select * from prescriptions")

    for row in rows:
        yield {
            'row_id':            int(row[0]),
            'subject_id':        int(row[1]),
            'hadm_id':           int(row[2]),
            'icustay_id':        int(row[3]) if row[3] else None,
            'startdate':         map_date(row[4]),
            'enddate':           map_date(row[5]),
            'drug_type':         row[6],
            'drug':              row[7],
            'drug_name_poe':     row[8],
            'drug_name_generic': row[9],
            'formulary_drug_cd': row[10] if row[10] else None,
            'gsn':               row[11] if row[11] and row[11] != '0' else None,
            'ndc':               row[12] if row[12] and row[12] != '0' else None,
            'prod_strength':     row[13],
            'dose_val_rx':       re.sub(r'[^\d\.-]', '', row[14]),
            'dose_unit_rx':      row[15],
            'form_val_disp':     re.sub(r'[^\d\.-]', '', row[16]),
            'form_unit_disp':    row[17],
            'route':             row[18]
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

