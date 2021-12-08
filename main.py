'''this is the main module, server functions and scheduling runs off of this'''

import time
import json
import logging
import sched
from uk_covid19 import Cov19API
from covid_data_handler import covid_API_request
from covid_data_handler import process_covid_json_data
from covid_news_handling import news_API_request
from flask import Flask
from flask import render_template
from flask import request
import cgi

app = Flask(__name__)


#establishes log file to save message with the time of the message for locating issues - OUTPUTS IP ADDRESS TO LOG FILE INSTEAD OF SHELL
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename='sys.log', encoding='utf-8', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


config_data = open(r"C:\Users\Admin\Desktop\Python Programs\coursework\config.json", "r")
config = json.load(config_data)
config_lines = config['config_data']
#read location from config file
location = config_lines[0]
location_data = location['location']
#read location type from config
location_type = config_lines[1]
location_type_data = location_type['location_type']
#read API key from config file
key = config_lines[2]
API_key = key['news_API_key']
updates = []


def schedule_covid_updates(update_interval=30.0, update_name='both'):
    '''schedules updates to the interface


    update_interval - time in seconds for the scheduling to wait, recieved from the interface - has a default of 30
    update_name is the name of the function that is to be used - has default of 'both
    if there is a problem with the scheduling, a scheduling with default values is used(see except ValueError branch).
    if that does not work also, the scheduling will be scrapped and the function will activate immediately(except TypeError branch)
    if no alternate method is successful or an unkown error occurs, the request fails and the function returns None
    '''
    logging.info("Function schedule_covid_updates inititated with interval" + str(update_interval) + "and name" + update_name)
    event_covid_scheduler = sched.scheduler(time.time, time.sleep)
    event_news_scheduler = sched.scheduler(time.time, time.sleep)
    if update_name == 'covid_API_request':
        try:
            #if location data is incorrect, sets the location to exeter as a default
            print(location_data + location_type_data)
            event_covid_scheduler.enter(float(update_interval), 1, covid_updater, (location_data, location_type_data))
            event_covid_scheduler.run(blocking=False)
        except ValueError:
            #attempts default values for scheduling
            logging.error("Location Data Error, running default function values")
            event_covid_scheduler.enter(float(update_interval), 1, covid_updater())
            event_covid_scheduler.run(blocking=False)
        except TypeError:
            #activates function now instead of scheduling it
            logging.error("Scheduling the covid API request has failed, activating request now instead")
            data_local, data_national = covid_API_request(location_data,location_type_data)
        except:
            #cancels request
            logging.error("Covid API request failed")
            data_local = None
            data_national = None
        finally:
            articles = None
        return data_local_response, data_national_response, articles
    elif update_name == 'news_API_request':
        print("NEWS")
        try:
            event_news_scheduler.enter(float(update_interval), 1, news_updater, (API_key))
            event_news_scheduler.run(blocking=False)
            print(articles)
            if isinstance(articles, float) or isinstance(articles, int):
                #solves a problem where news_API_request would return 3.0 instead of a dictionary
                raise ValueError("articles is int/float instead if dict")
        except ValueError:
            #activates request without scheduling and uses default values
            logging.error("Scheduling News request failed, retrying now")
            articles = news_API_request(API_key)
            return None, None, articles
        except:
            #cancels request
            logging.error("News API request failed")
            articles = None
        finally:
            data_local = None
            data_national = None
        return data_local, data_national, articles_response
    else:
        print("BOTH")
        try:
            print("TRY")
            event_covid_scheduler.enter(float(update_interval), 1, covid_updater, (location_data, location_type_data))
            event_news_scheduler.enter(float(update_interval), 5, news_updater, (API_key))
            event_covid_scheduler.run(blocking=False)
            event_news_scheduler.run(blocking=False)
            print(articles)
            return data_local_response, data_national_response, articles_response
        except ValueError:
            #attempts default values for scheduling
            print("VALUEERROR")
            logging.error("Location Data Error, running default function values")
            event_covid_scheduler.enter(float(update_interval), 1, covid_updater())
            event_news_scheduler.enter(float(update_interval), 5, news_updater, (API_key))
            event_covid_scheduler.run(blocking=False)
            event_news_scheduler.run(blocking=False)
            print(articles)
            return data_local_response, data_national_response, articles_response
        except TypeError:
            #activates function now instead of scheduling it
            print("TYPEERROR")
            logging.error("Scheduling one or more API requests has failed, activating requests now instead")
            data_local, data_national = covid_API_request(location_data, location_type_data)
            articles = news_API_request(API_key)
            print(articles)
            return data_local, data_national, articles
        except:
            #cancels request
            print("UNKNOWN ERROR")
            logging.error("Covid API request failed")
            data_local = None
            data_national = None
            articles = None
            return data_local, data_national, articles

def covid_updater(location_data, location_type_data):
    global data_local_response, data_national_response
    data_local_response, data_national_response = covid_API_request(location_data, location_type_data)
    

def news_updater(api_key):
    global articles_response
    articles_response = news_API_request(api_key)
    
    
    

@app.route('/index')
def run_program():
    '''this route is the main route for loading the data, all data passes through here to the template which is rendered when the ip address is loaded into a browser


    Keyword Arguments:
    request.args.get("x") - accesses data from form with variable name x
    schedule_covid_updates() - schedules covid/news updating - has defaults of a 30-second interval and to update both items
    '''
    logging.info("Loading newest data")
    try:
        #requests for form data
        #time
        update_time = request.args.get("update")
        #update name
        update_name = request.args.get("two")
        #repeating update - - will have value 'repeat' if true
        update_repeat = request.args.get("repeat")
        #covid update - will have value 'covid-data' if true
        update_covid = request.args.get("covid-data")
        #news update - will have value 'news' if true
        update_news = request.args.get("news")
        #print(update_time+update_name+update_repeat+update_covid+update_news)
        logging.info("no sections of update not needed")
    except TypeError:
        try:
            #requests for form data
            #time
            update_time = request.args.get("update")
            #update name
            update_name = request.args.get("two")
            #repeating update - - will have value 'repeat' if true
            update_repeat = request.args.get("repeat")
            #covid update - will have value 'covid-data' if true
            update_covid = request.args.get("covid-data")
            logging.info("news section of update not needed")
            update_news = None
            print(update_covid)
            print(update_news)
        except TypeError:
            try:
                #requests for form data
                #time
                update_time = request.args.get("update")
                #update name
                update_name = request.args.get("two")
                #repeating update - - will have value 'repeat' if true
                update_repeat = request.args.get("repeat")
                #news update - will have value 'news' if true
                update_news = request.args.get("news")
                logging.info("covid section of update not needed")
                update_covid = None
                print(update_covid)
                print(update_news)
            except TypeError:
                try:
                    #requests for form data
                    #time
                    update_time = request.args.get("update")
                    #update name
                    update_name = request.args.get("two")
                    #covid update - will have value 'covid-data' if true
                    update_covid = request.args.get("covid-data")
                    #news update - will have value 'news' if true
                    update_news = request.args.get("news")
                    logging.info("repeat section of update not needed")
                    update_repeat = False
                    print(update_covid)
                    print(update_news)
                except TypeError:
                    try:
                        #requests for form data
                        #update name
                        update_name = request.args.get("two")
                        #repeating update - - will have value 'repeat' if true
                        update_repeat = request.args.get("repeat")
                        #covid update - will have value 'covid-data' if true
                        update_covid = request.args.get("covid-data")
                        #news update - will have value 'news' if true
                        update_news = request.args.get("news")
                        logging.info("time section of update not needed, will use default value for time")
                        update_time = None
                        print(update_covid)
                        print(update_news)
                    except TypeError:
                        logging.error("Error in update, setting all values to None")
                        update_time = None
                        update_name = None
                        update_repeat = False
                        update_covid = None
                        update_news = None
    if update_repeat == 'repeat':
        update_repeat = True
    try:
        print(update_covid)
        print(update_news)
        print(update_time)
        #schedules the updates for the API calls
        if update_time is None:
            #creates an instant update
            if update_covid == 'covid-data' and update_news == 'news':
                #branch where both covid stats and news is to be updated
                print("BOTH")
                logging.info("Covid and News APIs to be updated")
                update_covid = True
                update_news = True
                data_local, data_national, articles = schedule_covid_updates(0, 'both')
            elif update_covid == 'covid-data':
                #branch where covid stats are to be updated
                print("COVID")
                logging.info("Covid API to be updated")
                update_covid = True
                update_news = False
                data_local, data_national, articles = schedule_covid_updates(0, 'covid_API_request')
            elif update_news == 'news':
                #branch where news articles are to be updated
                print("NEWS")
                logging.info("News API to be updated")
                update_covid = False
                update_news = True
                data_local, data_national, articles = schedule_covid_updates(0, 'news_API_request')
            else:
                #no updates needed
                print("NONE")
                logging.info("No updates needed at this time, raising error")
                update_covid = False
                update_news = False
                print("Update Request does not give data to update")
                raise ValueError("Update Request does not give data to update")
        else:
            time_minutes = update_time[0:1]
            time_seconds = update_time[2:3]
            time_minutes_seconds = int(time_minutes) * 60
            time_total = time_minutes_seconds + int(time_seconds)
            print(time_total)
            if update_covid == 'covid-data' and update_news == 'news':
                #branch where both covid stats and news is to be updated
                print("BOTH")
                logging.info("Covid and News APIs to be updated")
                update_covid = True
                update_news = True
                data_local, data_national, articles = schedule_covid_updates(time_total, 'both')
            elif update_covid == 'covid-data':
                #branch where covid stats are to be updated
                print("COVID")
                logging.info("Covid API to be updated")
                update_covid = True
                update_news = False
                data_local, data_national, articles = schedule_covid_updates(time_total, 'covid_API_request')
            elif update_news == 'news':
                #branch where news articles are to be updated
                print("NEWS")
                logging.info("News API to be updated")
                update_covid = False
                update_news = True
                data_local, data_national, articles = schedule_covid_updates(time_total, 'news_API_request')
            else:
                #no updates needed
                print("NONE")
                logging.info("No updates needed at this time, raising error")
                update_covid = False
                update_news = False
                print("Update Request does not give data to update")
                raise ValueError("Update Request does not give data to update")
        #sets the data for the update
        update_content = {'title': update_name, 'content': 'Time until Update from Initial Scheduling: ' + update_time + '\n' + 'Repeat Update=' + str(update_repeat) + '\n' + 'Update Covid Data=' + str(update_covid) + '\n' + 'Update News=' + str(update_news)}

    except ValueError:
        #path for when an update fails
        data_local, data_national = covid_API_request()
        articles = news_API_request(API_key)
        #sets the data for the update
        update_content = {'title': update_name, 'content': 'FAILED'}
        logging.error("Parameter Data Error, running default function values and refreshing data")
    national_cases, national_hospital, national_deaths = process_covid_json_data(data_national)
    local_cases, local_hospital, local_deaths = process_covid_json_data(data_local)
    updates.append(update_content)
    print(updates)
    if articles is None:
        #only updates covid data + updates list to ensure there are always news articles present
        return render_template('index.html', title='Daily Covid Updates', updates=updates, location=location_data, local_7day_infections=local_cases, nation_location='England', national_7day_infections=national_cases, hospital_cases=national_hospital, deaths_total=national_deaths)
    else:
        #updates everything
        return render_template('index.html', title='Daily Covid Updates', updates=updates, location=location_data, local_7day_infections=local_cases, nation_location='England', national_7day_infections=national_cases, hospital_cases=national_hospital, deaths_total=national_deaths, news_articles=articles)

if __name__ == '__main__':
    #where the program runs off
    logging.info("Running System")
    app.run()
