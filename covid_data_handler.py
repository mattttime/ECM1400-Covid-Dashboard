'''this module handles all the data in csv/json files containing the covid information to be shown on the dashboard'''
import logging
#aquires modules for scheduling events
import sched
import time
#aquires modules for accessing APIs and processing their data
import requests
import json
from uk_covid19 import Cov19API

def parse_csv_data(csv_filename):
    '''opens file, then reads the data into a dictionary/list'''
    logging.info("Function parse_csv_data initiated with arguments csv_filename= " + csv_filename)
    file_data = open(csv_filename, "r")
    #debugging print
    print(file_data)
    file_lines = file_data.readlines()
    return file_lines


def process_covid_csv_data(covid_csv_data):
    '''takes list of data and returns case numbers, current hospital cases and total deaths from the data'''
    logging.info("Function process_csv_data initiated with arguments covid_csv_data= " + covid_csv_data)
    #gets deaths data
    current_data = covid_csv_data[14]#the 14th item in the list is the 1st with the deaths value 
    current_data_list = current_data.split(",")
    total_deaths = current_data_list[4]#data at index 4 contains the deaths statistic
    #gets cases data
    cases_weekly_total = 0
    for i in range(3, 10):
        #loops through the required 7 days' worth of data, ignoring the 1st 2 entries(starts at index 3) as they are incomplete
        current_data = covid_csv_data[i]
        current_data_list = current_data.split(",")
        daily_cases = current_data_list[6]
        print(daily_cases)
        cases_weekly_total = cases_weekly_total + int(daily_cases)
    print(cases_weekly_total)
    #gets hospital data
    current_data = covid_csv_data[1]
    current_data_list = current_data.split(",")
    current_hospital_cases = current_data_list[5]
    print(current_hospital_cases)
    return cases_weekly_total, int(current_hospital_cases), int(total_deaths)


def covid_API_request(location="Exeter", location_type="ltla"):
    '''utilises the public health england api and returns the current covid data based on the location specified'''
    logging.info("Function covid_API_request initiated with variables location=" + location + ", location type=" + location_type)
    try:
        cases_and_deaths = {
            "date": "date",
            "daily_cases": "newCasesByPublishDate",
            "total_cases": "cumCasesByPublishDate",
            "hospital_cases": "hospitalCases",
            "total_deaths": "cumDeaths28DaysByDeathDate"
        }
        filter_methods_local = {
            #filters used for retrieving local case data
            'areaType=' + location_type,
            'areaName=' + location
        }
        filter_methods_national = {
            #filter used for retrieving national case/death/hospital data
            'areaType=nation',
            'areaName=England'
        }
        api_call_local = Cov19API(filters=filter_methods_local, structure=cases_and_deaths)
        api_call_national = Cov19API(filters=filter_methods_national, structure=cases_and_deaths)
        #gets the needed data from the most recent phe update
        api_data_local = api_call_local.get_json()
        api_data_national = api_call_national.get_json()
        if api_data_local == None or api_data_national == None:
            raise ValueError("one or more API calls is empty")
        logging.info("covid API request successful")
    except ValueError:
        logging.error("An API request has failed, retrying with default values")
        covid_API_request()
    except:
        logging.error("An unknown error has occured")
        return None, None
    return api_data_local, api_data_national


def process_covid_json_data(covid_json_data):
    '''processes data in a similar way to process_covid_csv_data, returns 3 variables containing the needed data'''
    sum_cases = 0
    try:
        data_list = covid_json_data["data"]
        for i in range(1, 7):
            #sums the cases of the last 7 days, skipping the most recent entry as incomplete
            last_complete_entry = data_list[i]
            print(last_complete_entry)
            sum_cases = sum_cases + last_complete_entry["daily_cases"]
        #print(data_list[1])#prints entire dictionary(for debugging)
        last_complete_death_entry = data_list[1]
        last_complete_hospital_entry = data_list[2]
        total_deaths = last_complete_death_entry["total_deaths"]
        hospital_cases = last_complete_hospital_entry["hospital_cases"]
    except TypeError:
        return None, None, None
    return(sum_cases, hospital_cases, total_deaths)


local_data,national_data=covid_API_request()
