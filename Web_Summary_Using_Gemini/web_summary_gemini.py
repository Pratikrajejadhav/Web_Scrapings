import os
import google
import google.generativeai as genai
import streamlit as st
import spacy
from spacy import displacy
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options
import re
import time

# Function to add URL to session state dictionary
def selection_box(url):
    website_name = extract_name(url)
    st.session_state.url_title_dict[website_name] = url
    st.session_state.url_title_keys = list(st.session_state.url_title_dict.keys())
    
# Prompt text for generative model
prompt_text = ''' 
        Give the descriptive summary about the website

        Generate the keywords related to it.
'''

# Initialize session state variables
if 'url_title_dict' not in st.session_state:
    st.session_state.url_title_dict = {}

if 'url_title_keys' not in st.session_state:
    st.session_state.url_title_keys = []

# Function to extract visible text from website
def extract_website_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)
    visible_text = driver.find_element(By.TAG_NAME, "body").text
    driver.close()
    return visible_text

# Function to display summary and keywords

def printing_summary(response_new, url):
    output_placeholder = st.empty()
    output_placeholder.empty()
    print(response_new)
    summary_text, keywords_text = response_new.split("Keywords")
    keywords_list = re.findall(r'\* (.+)', keywords_text)
    text = ",  ".join(keywords_list)

    #### nlp tokenizer ########

    nlp = spacy.load("en_core_web_sm")
    pd.set_option("display.max_rows", 200)
    doc = nlp(text)

    new_text = displacy.render(doc, style="ent")

    ########## end  ###################
    
    ###### Define CSS styles for each subheader to change their colors
    subheader_style1 = """
        <style>
            .colorful-subheader1 {
                color: blue;
            }
        </style>
    """

    subheader_style2 = """
        <style>
            .colorful-subheader2 {
                color: red;
            }
        </style>
    """
    ############################################
    st.write(url)

    st.markdown(subheader_style1, unsafe_allow_html=True)
    st.markdown("<h2 class='colorful-subheader1'>Keywords</h2>", unsafe_allow_html=True)

    st.write(new_text, unsafe_allow_html=True)
    st.write("")
    st.markdown(subheader_style2, unsafe_allow_html=True)

    st.markdown("<h2 class='colorful-subheader2'>Summary</h2>", unsafe_allow_html=True)
    st.write(summary_text.strip())


# Function to generate content using generative AI model
def generativeai_model(prompt, visible_text):
    api_key = "AIzaSyCKESnAOIkl8fIqV-KHOUx5pF-ythxJ1Ng"
    genai.configure(api_key = api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, visible_text])
    return response.text

# Function to extract website name from URL
def extract_name(url):
    parsed_url = urlparse(url)
    website_name = parsed_url.netloc.split('.')[1]
    return website_name

# Main function to create the UI
def main():
    st.header(f'Website Summary')

    # Sidebar input for URL
    url = st.sidebar.text_input("Enter the Website Link")
    btn = st.sidebar.button("Submit")

    # When submit button is clicked
    if btn:
        selection_box(url)
        visible_text = extract_website_data(url)
        response_new = generativeai_model(prompt_text, visible_text)
        printing_summary(response_new, url)

    # Display selection box for saved websites
    keys = st.session_state.url_title_keys
    options = st.sidebar.selectbox("Select website", keys)
    try:
        if not btn:
            url = st.session_state.url_title_dict[options]
            visible_text = extract_website_data(url)
            response_new = generativeai_model(prompt_text, visible_text)
            printing_summary(response_new, url)
    except Exception as e:
        st.write("Enter the link ")

if __name__ == '__main__':
    main()
