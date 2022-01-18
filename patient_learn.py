#!/usr/bin/env python
import csv
import json
from datetime import datetime

def read_csv(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            print(row[0], row[1], row[2])

def list_elements():
    my_list = [1, 2, 3]
    for item in my_list:
        print("with for", item)

    print("no for", my_list[0])
    print("no for", my_list[1])
    print("no for", my_list[2])


def add_list_elements():
    print("------- default elements -------")
    my_list = ["uno", "dos", "tres"]
    for item in my_list:
        print(item)
    
    print("------- with added elements -------")
    my_list.append("cuatro")
    my_list.append("cinco")
    for item in my_list:
        print(item)


def list_of_list():
    print("------- for loop -------")
    my_list_of_list = [ [1, 2, 3], [4, 5, 6], [7, 8, 9] ]
    for rows in my_list_of_list:
        print(rows[0], rows[1], rows[2])

    print("------- nested for loop -------")
    for rows in my_list_of_list:
        for cell in rows:
            print(cell)



def dictionary():
    print("------- individually -------")
    my_dic = {
        "0": "cero",
        "1": "uno",
        "2": "dos",
        "3": "tres",
        "4": "cuatro"
    }

    print(my_dic["0"])
    print(my_dic["1"])
    print(my_dic["2"])
    print(my_dic["3"])
    print(my_dic["4"])

    print("------- individually -------")
    my_dic["0"] = "zero"
    my_dic["1"] = "one"
    my_dic["2"] = "two"
    my_dic["3"] = "three"
    my_dic["4"] = "four"

    print("my_keys:", my_dic.keys())
    for key in my_dic.keys():
        print(my_dic[key])
    
    print("------- add elements -------")
    my_dic["8"] = "eight"
    my_dic["9"] = "nine"
    for key in my_dic.keys():
        print(my_dic[key])


def dictionary_like_json():
    my_dic = {
        "id": 1,
        "first_name": "Nathaly",
        "last_name": "Pinzon",
        "phones": ["0426569874", "0485974126"],
        "siblings": [
            {
                "id": 2,
                "first_name": "Jully",
                "last_name": "Pinzon",
                "phones": ["04548795", "043254789"],
            }
        ]
    }

    print("object", my_dic)
    print("json", json.dumps(my_dic))


def string_to_date():
    str_date_one = '2014-12-30'
    str_date_two = '2014-12-30 12:30:45'

    date_one = datetime.strptime(str_date_one, '%Y-%m-%d')
    date_two = datetime.strptime(str_date_two, '%Y-%m-%d %H:%M:%S')
    
    print("Normal", date_one.)
    print("Normal", date_two.)

    print("Iso", date_one.isoformat())
    print("Iso", date_two.isoformat())

string_to_date()