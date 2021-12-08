from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_covid_updates
import pytest

#provided tests

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request():
    
    data = covid_API_request()
    assert isinstance(data, dict)

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')

#created tests

def test_process_covid_json_data():
    '''checks if the required data has been passed through the API successfully as integers - does not specifiy a number as the data can change'''
    local_data,national_data=covid_API_request()
    sum_cases_local,hospital_cases_local,total_deaths_local = process_covid_json_data(local_data)
    sum_cases_national,hospital_cases_national,total_deaths_national = process_covid_json_data(national_data)
    assert isinstance(sum_cases_local, int)
    assert isinstance(sum_cases_national, int)
    assert isinstance(hospital_cases_national, int)
    assert isinstance(total_deaths_national, int)


def test_schedule_covid_updates2(interval,function_name):
