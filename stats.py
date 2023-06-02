from urlextract import URLExtract
import pandas as pd 
from collection import Counter 
from wordcloud import WordCloud
import emoji
import re
import string 
import nltk
pd.set_option('display.max_colwidth', 100)

stopwords = nltk.corpus.stopwords.words("english")
wn = nltk.WordNetLemmatizer()
punct = string.punctuation

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




def create_word_cloud(selected_user, wc_df):

    if selected_user != "Overall":

        wc_df = wc_df[wc_df["User"] == selected_user]
    
    # create word cloud object
    wc = WordCloud(width=1000, height=500, min_font_size=10, 
                   background_color="white")
    
    # generate wordcloud image
    wc = wc.generate(wc_df["Message"].str.cat(sep=" "))

    return wc

# get most common words as a dataframe

# Clean text
def clean_text(text):
    # Remove punctuations 
    text = "".join([word.lower() for word in text if word not in punct])
    
    # Remove any other signs
    text = " ".join(re.split('\W+', text))
    
    # Remove numerial leaving only aplabets
    text = re.sub('[^A-Za-z]+', ' ', str(text))
    
    # Remove links and websites
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www.\S+", "", text)
    
    text = text.split()
    
    # Remove stopwords
    text = [word for word in text if word not in stopwords]
    
    # lemmatize
    text = [wn.lemmatize(word) for word in text]
    
    #
    text = " ".join([word for word in text])
    
    return text

def get_common_words(selected_user, wc_df):

    # clean message
    wc_df["clean_message"] = wc_df["Message"].apply(clean_text)

    # Get top 20 words
    if selected_user != "Overall":
        wc_df = wc_df[wc_df["User"] == selected_user]

    words = []

    for message in wc_df["clean_message"]:
            words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20)).sort_values(1)
    return most_common_df

# Get Emojis