import re
import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

# Import keyword extraction script
import ke

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)


def soupify(resource, txt=False):
    # Handler for return soup object given url or html code
    user_agent = user_agent_rotator.get_random_user_agent()
    headers = {"User-Agent":user_agent}
    if not txt:
        response = requests.get(resource, headers=headers)
        content = response.text
    else: 
        content = resource  
    soup = BeautifulSoup(content, "html.parser")
    return soup

def miner(subjects):
    # Function to extract the description of every subject
    topics = []
    for subject in subjects:
        url = subject["url"]
        print(url)
        soup = soupify(url)

        # Select the interesting data
        content = soup.select(".tarea")
        content = [c.getText() for c in content]
        content = "\n".join(content)

        # Store the data link by subject id for further association
        topics.append({"id":subject["id"], "content":content})
    return topics

def cleaner(topics):
    for topic in topics:
        index = topics.index(topic)
        clean_text = ke.clean(topic["content"])
        topic["content"] = clean_text
        topics.pop(index)
        topics.insert(index, topic)
    return topics


def extract_kwargs(clean_topics, n=10):
    topic = []
    for topic in clean_topics:
        corpus = [topic["content"]]
        top_words = ke.get_top_n_words(corpus, n=10)
        top_words.insert(0, "id", topic["id"])
    return top_words



if __name__ == "__main__":
    # Open subjects file and get subject object
    with open("subjects_full.json") as subjects_f:
        subjects =  json.load(subjects_f)
    
    topics = miner(subjects)

    clean_topics = cleaner(topics)
    top_words = extract_kwargs(clean_topics)

    top_words.to_json("topics.json", orient='records')
    

    