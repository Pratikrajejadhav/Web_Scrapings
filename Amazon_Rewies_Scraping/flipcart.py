import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
from selenium.common.exceptions import NoSuchElementException 

# Function to scrape reviews from Flipkart
def scrape_flipkart_reviews(url, max_page=5):
    driver = webdriver.Chrome()
    reviews = []

    for page in range(1, max_page + 1):
        print("Page:", page)
        page_url = f'{url}{page}'
        driver.get(page_url)

        review_elements = driver.find_elements(By.XPATH, "//div[@class='col EPCmJX Ma1fCG']")
        if review_elements:
            for review in review_elements:
                review_data_dict = {}
                try:
                    # review_data_dict['reviewer_name'] = review.find_element(By.XPATH, ".//div[@class='_2NsDsF AwS1CA']").text
                    # review_data_dict['rating'] = review.find_element(By.XPATH, ".//div[@class='XQDdHH Ga3i8K']").text
                    # review_data_dict['review_text'] = review.find_element(By.XPATH, ".//div[@class='ZmyHeo']").text

                    reviewer_name_xpath = "//div[@class='_2aFisS']/div[@class='_2aFisS']/div[@class='_2aFisS']/div[@class='_27M-vq']//div[@class='_2wzgFH']"
                    rating_xpath = "//div[@class='_2aFisS']/div[@class='_2aFisS']/div[@class='_2aFisS']/div[@class='_27M-vq']//div[@class='XQDdHH Ga3i8K']"
                    review_text_xpath = "//div[@class='_2aFisS']/div[@class='_2aFisS']/div[@class='_2aFisS']/div[@class='_27M-vq']//div[@class='t-ZTKy']"

                    reviews.append(review_data_dict)
                except NoSuchElementException:
                    print("Some elements not found on page", page)
        else:
            print(f'NO Reviews Found on Page {page}')
            break

    driver.close()

    return reviews

if __name__=='__main__':

    st.header("Sentiment Analysis of Reviews")

    full_link = st.sidebar.text_input("Enter the Flipkart product review link here")
    max_page = st.sidebar.number_input("Enter Max Pages", min_value=1, step=1)
    btn =  st.sidebar.button("Start")

    if btn:
        pattern = r'(https://www.flipkart.com/.+)'
        match = re.search(pattern, full_link)

        if match:
            extracted_link = match.group(1)
            print(extracted_link)
            reviews = scrape_flipkart_reviews(extracted_link, max_page)
        else:
            print("Invalid Flipkart product review link.")

        data_file = pd.DataFrame(reviews)
        # Perform sentiment analysis and further processing...
        st.write(data_file)
