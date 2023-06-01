import streamlit as st 
import numpy as np 
import seaborn as sns 
import pandas as pd 
import re 

# This function separetes the time from the date
def get_date_and_time(string):
    string = string.split(",")
    date, time = string[0], string[1]
    time = time.split("-")
    time = time[0].strip()
    
    return date+" "+time 

# remove the traling "\n" and the end of each message
def get_string(text):
    return text.split('\n')[0]

def preprocess(data):

    # regex pattern to track date and time
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Extract only the messages
    messages = re.split(pattern, data)[1:]

    # Extracting only the date/time
    dates = re.findall(pattern, data)