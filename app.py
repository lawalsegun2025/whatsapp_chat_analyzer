import streamlit as st
import preprocess
import re 
import stats 
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np 

st.sidebar.title("Whatsapp Chat Analyzer")

# upload a file
uploaded_file = st.sidebar.file_uploader("choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    # converting the bytecode to the text-file
    data = bytes_data.decode("utf-8")

    # sending file data to the preprocessing function for further functioning
    df = preprocess.preprocess(data)

    # displaying the dataframe
    ## st.datframe(df)

    # get unique users 
    user_list = df["User"].unique().tolist()

    # remove the group notifications
    user_list.remove("Group Notification")

    # organize in order
    user_list.sort()

    # include overall. This is responsible for showcasing the overall chat analysis
    user_list.insert(0, "Overall")

    # select and display analysis of user
    selected_user = st.sidebar.selectbox(
        "Show analysis with respect to", user_list
    )

    st.title("WhatsApp Chat Analysis for " + selected_user)
    if st.sidebar.button("Show Analysis"):

        # getting the stats of the selected user from the stats script
        num_messages, num_words, media_ommited, links = stats.fetch_stats(
            selected_user, df
        )

        # first phase is to showcase the basic stats like number of users,
        # number of messages,number of media shared and all,
        # so for that 4 columns are required
        col_1, col_2, col_3, col_4 = st.columns(4)

        with col_1:
            st.header("Total Messages")
            st.title(num_messages)

        with col_2:
            st.header("Total Words")
            st.title(num_words)

        with col_4:
            st.header("Total Links Shared")
            st.title(links)

        # finding the most active users in the group
        if selected_user == "Overall":

            # dividing the front end into two columns
            # 1st col for bar chat, 2nd col for users df chat count

            st.title("Most Active Users")
            active_count, new_df = stats.fetch_active_users(df)
            fig, ax = plt.subplots()
            col_1, col_2 = st.columns(2)

            with col_1:
                ax.bar(active_count.index, active_count.values, color="royalblue")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col_2:
                st.dataframe(new_df)

        # Word Cloud
        st.title("Word Cloud")

        # Get dataframe without "<Media omitted>"
        wc_df = df[df["Message"] != "<Media omitted>"]
        df_img = stats.create_word_cloud(selected_user, wc_df)
        fig, ax = plt.subplots()
        ax.imshow(df_img)
        st.pyplot(fig)

        # Most Common words