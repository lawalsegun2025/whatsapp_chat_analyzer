from urlextract import URLExtract
import pandas as pd 
from collection import Counter 
from wordcloud import WordCloud
import emoji

extract = URLExtract()

def fetch_stats(selected_user, df):

    # if the selected user is a specific user,then make changes in the 
    # dataframe, else do not make any changes
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    # Get the number of messages
    num_messages = df.shape[0]

    # Get the number of words
    words = []
    for message in df["Message"]:
        words.extend(message.split())

    # Get the number of media files shared
    media_omitted = df[df["Message"] == "<Media omitted>"]

    # Get number of links shared url's
    links = []
    for message in df["Message"]:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), media_omitted.shape[0], len(links)

# most avtive users (group level)

def fetch_active_users(df):
    
    df = df[df["User"] != "Group Notification"]
    count = df["User"].value_counts().head()

    # new_df = pd.DataFrame(((df["User"].value_counts()/df.shape[0]) * 100).round(2))
    new_df = pd.DataFrame(df["User"].value_counts()).rename(columns={"User":"posts"})
    return count, new_df
