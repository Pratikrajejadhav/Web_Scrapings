# Importing necessary modules
import streamlit as st 
import google.generativeai as genai
import google.ai.generativelanguage as glm
import pandas as pd

genai.configure(api_key="AIzaSyALIvB-IxfKhe0Zxzdii2TEqTmefMxPk5M")

if __name__=='__main__':

    st.header("Sentiment Analysis of Reviews")
    data = st.sidebar.file_uploader("Upload Data File Here", type=['csv'])

    if data is not None:
        data_file  = pd.read_csv(data)

        sentiment = []
        for reviews in data_file['review_text']:
             
             # model selection
             model = genai.GenerativeModel('gemini-pro')

             prompt = """ Give the Sentiment analysis of given review only in two words either ***POSITIVE** 😀😀  or **NEGATIVE** ☹️☹️ """

             response = model.generate_content([prompt, reviews])
             st.write(reviews)
             st.write(response.text)
             sentiment.append(response.text)
             st.write("=====================================================================================")
        data_file['Sentiment'] = sentiment 
        st.write(data_file)


        
