'''this module holds the functions for handling news related things'''
import logging
import json
import requests
    
def news_API_request(api_key, covid_terms="covid COVID-19 coronavirus"):
    '''by utilising json requests, this function can aquire wanted news articles via newsapi.org


    ONLY TAKES 3 TERMS - due to the structuring for the request url only taking 3 items
    Arguments:
    api_key - the api key required to access newsapi - has no default, api key needs to be supplied through config file
    covid_terms - the terms needed to filter the newsapi request(default "covid COVID-19 coronavirus")
    Variables:
    headlines/content - lists which contain the data from the request
    news_content - list of dictionaries each containing the data for a singe news article - to be returned on success
    base_url - the base url for a newsapi request, has keywords/filters concatenated to it to create the complete url
    '''
    logging.info("Function news_API_request initiated with arguments terms=" + covid_terms + " api key=" + api_key)
    headlines = []
    content = []
    news_content = []
    base_url = "https://newsapi.org/v2/top-headlines?"
    terms_list = covid_terms.split()
    country = "gb"
    complete_url = base_url + "country=" + country + "&q=" + terms_list[0] + "&q=" + terms_list[1] + "&q=" + terms_list[2] + "&apiKey=" + api_key
    try:
        # print response object
        response = requests.get(complete_url)
        #print(response.json())
        response_data = response.json()
        articles = response_data["articles"]
        print(articles[0])
        for i in articles:
            '''adds the title/content to a list for later use in dictionary news_content'''
            headlines.append(i['title'])
            content.append(i['description'])
        for i in range(0, len(articles)):
            news_content.append({'title': headlines[i],'content': content[i]})
        print(news_content)
        for i in range(0, len(news_content)):
            if news_content[i] is None:
                #raises error if request fails
                raise ValueError("news not retrieved correctly")
        logging.info("News API request successful")
        return news_content
    except ValueError:
        logging.error("News API not performed as expected")
        return None


def update_news(api_key, data_structure=[{'title':"one"},{'title':"two"},{'title':"three"}]):
    '''utilises news_API_request to update the data structure with the newest articles, and removes the articles which were already present


    Arguments:
    api_key - the api key required to access newsapi - has no default, api key needs to be supplied through config file
    data_structure - current news articles(default [{'title':"one"},{'title':"two"},{'title':"three"}]) - default used to prevent errors in empty data structures
    Variables:
    titles - list of titles in the current data structure
    new_titles - list of titles in the new data structure
    '''
    logging.info("Function update_news initiated")
    titles = []
    try:
        new_data_structure = news_API_request(api_key)
        for i in data_structure:
           titles.append([i])
        new_titles = new_data_structure
        for i in range (0, len(titles)):
            for ii in range (0, len(new_titles)):
                #nested loop compares each item in data_structure to each item in new_data_structure
                if titles[i] == new_titles[ii]:
                    #removes item from new_data_structure if is the same as an item from data_structure
                    new_data_structure.remove(ii)
                    logging.info("duplicate news item removed from list")
        if data_structure == new_data_structure:
            #raises error if the data structures are the same
            raise RuntimeError("Update Failed")
        logging.info("News Update Successful")
        return new_data_structure
    except RuntimeError:
        logging.error("News Update Failed, returning original data structure")
        return data_structure
