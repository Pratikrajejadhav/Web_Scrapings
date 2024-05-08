# Importing necessary modules
import streamlit as st 
import google.generativeai as genai
import google.ai.generativelanguage as glm
# from dotenv import load_dotenv
# import os
import io
# import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def web_data(url):

    # WebDriver Chrome
    driver = webdriver.Chrome()

    # Target URL
    driver.get(url)
    # To load entire webpage
    time.sleep(5)

    # Getting only the visible text on the website
    visible_text = driver.find_element(By.TAG_NAME, "body").text
    # print(visible_text)

    # Closing the driver
    driver.close()
    
    return visible_text


genai.configure(api_key="<your api key>")")

if __name__=='__main__':

    st.header("Web Page Summary")
    url = st.text_input('Input url', "")
    
    if st.button("Get Response", use_container_width=True):
        model = genai.GenerativeModel('gemini-pro')

        web_text = web_data(url)

        prompt = """ create the summary from the given content """
        response = model.generate_content([prompt, web_text])

        st.write(response.text)
