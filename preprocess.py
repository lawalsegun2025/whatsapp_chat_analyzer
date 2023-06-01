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

def get_string(text):
    return text.split('\n')[0]

