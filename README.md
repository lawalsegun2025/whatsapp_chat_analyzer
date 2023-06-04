# WhatsApp Chat Analyzer

## Table of Content
* [Overview](#overview)
* [Motivation](#motivation)
* [Problem Solving Steps](#problem-solving-steps)
* [Source of Dataset](#source-of-dataset)
* [Data Preprocessing](#data-preprocessing)
* [Exploratory Data Analysis](#exploratory-data-analysis)
* [Model Performance](#model-performance)
* [Deployment](#deployment)
* [Future scope of project](#future-scope-of-project)

## Overview

This app created in this project enables a user to get instant analysis of a WhatsApp Chat. The data used for this project does not include media files.

A user will simply get the whatsapp group chat txt file and upload it into the web app, and the app will display the overall analysis of the group.<br/><br/>

<img src="img/whatsapp.png">

## Motivation

We often find ourselves joining or being added to numerous whatsapp chat groups and some time the number of unread chats can run up to hundreds or in some cases even more. This app can help a use to get the most relevant information(s) rather than manually skimming through a whole lot of chats.

## Problem Solving Steps

1. Collecting the data of a chat or group chat and saving the txt file in the project folder.
2. Preprocessing the text and extracting the important features.
3. Plot graphs showcasing the analysis
4. Integrating the analysis with the User Interface made using Streamlit. 
5. Deploy the application on Heroku cloud service

## Source of Dataset

The data for this project can be gotten from any whatsapp group chat. To get a whatsapp group chat data, follow the steps listed below;

* Move to the whatsapp chat group
* At the top right click on the `three vertical column`
* You will be presented with a drop down menu, click on `more`
* Select `export`
* Choose the option `without media files` (as this project work with data that did not include media files)

## Data Preprocessing

The file required for this project is a whatapp chat exported text file in `.txt` format. Therefore the data is a text data. The frollowing code was used to import and preprocess the text data into a pandas dataframe.</br></br>

```python
def preprocessing(file, key):
    split_formats = {
        '12hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s',
        '24hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',
        'custom' : ''
    }
    datetime_formats = {
        '12hr' : '%m/%d/%y, %I:%M %p - ',
        '24hr' : '%m/%d/%y, %H:%M - ',
        'custom': ''
    }
    
    raw_data = open(file, 'r', encoding="utf-8")
    raw_data = raw_data.read()
    raw_string = ' '.join(raw_data.split('\n')) # converting the list split by newline char. as one whole string as there can be multi-line messages
    user_msg = re.split(split_formats[key], raw_string) [1:] # splits at all the date-time pattern, resulting in list of all the messages with user names
    date_time = re.findall(split_formats[key], raw_string) # finds all the date-time patterns

    df = pd.DataFrame({'Date': date_time, 'user_msg': user_msg}) # exporting it to a df
        
    # converting date-time pattern which is of type String to type datetime,
    # format is to be specified for the whole string where the placeholders are extracted by the method 
    df['Date'] = pd.to_datetime(df['Date'], format=datetime_formats[key])
    
    # split user and msg 
    usernames = []
    msgs = []
    for i in df['user_msg']:
        a = re.split('([\w\W]+?):\s', i) # lazy pattern match to first {user_name}: pattern and spliting it aka each msg from a user
        if(a[1:]): # user typed messages
            usernames.append(a[1])
            msgs.append(a[2])
        else: # other notifications in the group(eg: someone was added, some left ...)
            usernames.append("Group Notification")
            msgs.append(a[0])

    # creating new columns         
    df['User'] = usernames
    df['Message'] = msgs

    # dropping the old user_msg col.
    df.drop('user_msg', axis=1, inplace=True)
    
    df = df[["Message", "Date", "User"]]
    
    df["Message"] = df["Message"].apply(lambda x: x.strip())
    
    # Extract the date without time
    df['Only date'] = pd.to_datetime(df['Date']).dt.date

    # Get only the Year
    df['Year'] = pd.to_datetime(df['Date']).dt.year

    # Get month number
    df['Month_num'] = pd.to_datetime(df['Date']).dt.month

    # Get name of month
    df['Month'] = pd.to_datetime(df['Date']).dt.month_name()

    # Get Day
    df['Day'] = pd.to_datetime(df['Date']).dt.day

    # Get name of Day
    df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()

    # Get hour
    df['Hour'] = pd.to_datetime(df['Date']).dt.hour

    # Get minutes
    df['Minute'] = pd.to_datetime(df['Date']).dt.minute

    
    
    return df
```

## Exploratory Data Analysis

The following analysis were carried out on the text data

### Numerical Analysis
These includes;
* Total Number of messages in the chat
* Total number of words in the chat
* Total number of media files shared in the chat
* Total number of links in the chat
* Most active users

### Word Cloud

This displays the most common words in the chat.</br></br>
<div align="center">
    <img src="img/whatsapp_woordcloud.png">
</div>

### Top 20 Words

A graph of the top 20 words in the chat was ploted agaist the number of occurances of the words.</br></br>
<div align="center">
    <img src="most_commo_words.png">
</div>

## Deployment

## Future scope of project

Much more analysis could be added for example; 
* Which user gets the most replies?
* Who is the most active user?

And many more...
