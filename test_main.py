import time
import json
import logging
import sched
from uk_covid19 import Cov19API
from covid_data_handler import covid_API_request
from covid_data_handler import process_covid_json_data
from covid_news_handling import news_API_request
from main import schedule_covid_updates
from main import covid_updater
from main import news_updater
from flask import Flask
from flask import render_template
from flask import request
import cgi

def test_schedule_covid_updates():
    data_local_response, data_national_response, articles = schedule_covid_updates(5.0, 'news_API_request')
    assert isinstance(articles) == []
    assert data_local_response is None
    assert data_national_response is None
    data_local_response, data_national_response, articles = schedule_covid_updates(6.0, 'covid_API_request')
    assert isinstance(data_local_response) == []
    assert isinstance(data_national_response) == []
    assert articles is None
    data_local_response, data_national_response, articles = schedule_covid_updates(15.0, 'both')
    assert isinstance(data_local_response) == []
    assert isinstance(data_national_response) == []
    assert isinstance(articles) == []
