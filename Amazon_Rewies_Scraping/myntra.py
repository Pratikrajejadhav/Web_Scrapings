import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
from selenium.common.exceptions import NoSuchElementException 

# Function to scrape reviews from Myntra
def scrape_myntra_reviews(url, max_page=5):
    driver = webdriver.Chrome()
    reviews = []

    for page in range(1, max_page + 1):
        print("Page:", page)
        page_url = f'{url}'
        driver.get(page_url)

        review_elements = driver.find_elements(By.XPATH, './/div[@class,"user-review-userReviewWrapper"]')
        # review_elements = driver.find_elements(By.XPATH, "//div[contains(@class,'detailed-reviews-userReviewsContainer')][@id='detailedReviewsContainer']")
        print(type(review_elements))
        print(len(review_elements))
        if review_elements:
            for review in review_elements:
                print(review)
                review_data_dict = {}
                try:
                    review_data_dict['reviewer_name'] = review.find_element(By.XPATH, ".//div[@class='user-review-left']").text
                    review_data_dict['rating'] = review.find_element(By.XPATH, "//*[@id='detailedReviewsContainer']/div[1]/div[1]/div[1]/span").text
                    review_data_dict['review_text'] = review.find_element(By.XPATH, ".//div[@class='user-review-reviewTextWrapper']").text
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

    full_link = st.sidebar.text_input("Enter the Myntra product review link here")
    max_page = st.sidebar.number_input("Enter Max Pages", min_value=1, step=1)
    btn =  st.sidebar.button("Start")

    if btn:
        pattern = r'(https://www.myntra.com/.+)'
        match = re.search(pattern, full_link)

        if match:
            extracted_link = match.group(1)
            print(extracted_link)
            reviews = scrape_myntra_reviews(extracted_link, max_page)
        else:
            print("Invalid Myntra product review link.")

        data_file = pd.DataFrame(reviews)
        # Perform sentiment analysis and further processing...
        st.write(data_file)
