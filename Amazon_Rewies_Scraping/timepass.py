import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import re

# Function to scrape reviews from Amazon
def scrape_amazon_reviews(url, max_page=5):
    driver = webdriver.Chrome()
    reviews = []

    for page in range(1, max_page + 1):
        print("Page:", page)
        page_url = f'{url}{page}?ie=UTF8&reviewerType=all_reviews&pageNumber={page}'
        driver.get(page_url)

        review_elements = driver.find_elements(By.XPATH, "//div[@data-hook='review']")
        if review_elements:
            for review in review_elements:
                review_data_dict = {}
                review_data_dict['reviewer_name'] = review.find_element(By.XPATH, ".//span[@class='a-profile-name']").text
                review_data_dict['review_date'] = review.find_element(By.XPATH, ".//span[@data-hook='review-date']").text
                review_data_dict['rating'] = review.find_element(By.XPATH, ".//i[contains(@class, 'review-rating')]/span").get_attribute('innerText')
                review_data_dict['review_text'] = review.find_element(By.XPATH, ".//span[@data-hook='review-body']").text
                reviews.append(review_data_dict)
        else:
            print(f'NO Reviews Found on Page {page}')
            break

        # Clicking on the next page button
        try:
            next_button = driver.find_element(By.XPATH, "//li[@class='a-last']//a")
            next_button.click()
            WebDriverWait(driver, 10).until(EC.url_changes(page_url))
        except NoSuchElementException:
            print("Next Page not found")
            break
        
    driver.close()

    return reviews

# Function to scrape reviews from Flipkart

# def scrape_flipkart_reviews(url, max_page=5):
#     driver = webdriver.Chrome()
#     reviews = []

    # for page in range(1, max_page + 1):
    #     print("Page:", page)
    #     page_url = f'{url}{page}'
    #     driver.get(page_url)

    #     review_elements = driver.find_elements(By.XPATH, "//div[@class='col EPCmJX Ma1fCG']")
    #     if review_elements:
    #         for review in review_elements:
    #             review_data_dict = {}
    #             review_data_dict['reviewer_name'] = review.find_element(By.XPATH, ".//p[@class='_2NsDsF AwS1CA']").text
    #             # review_data_dict['review_date'] = review.find_element(By.XPATH, ".//div[@class='row']//p[@class='_35HzRV']").text
    #             review_data_dict['rating'] = review.find_element(By.XPATH, ".//div[@class='XQDdHH Ga3i8K']").text
    #             review_data_dict['review_text'] = review.find_element(By.XPATH, ".//div[@class='ZmyHeo']").text
    #             reviews.append(review_data_dict)
    #     else:
    #         print(f'NO Reviews Found on Page {page}')
    #         break

    # driver.close()

    # return reviews

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
                    review_data_dict['reviewer_name'] = review.find_element(By.XPATH, ".//p[@class='_2NsDsF AwS1CA']").text
                    review_data_dict['rating'] = review.find_element(By.XPATH, ".//div[@class='XQDdHH Ga3i8K']").text
                    review_data_dict['review_text'] = review.find_element(By.XPATH, ".//div[@class='ZmyHeo']").text
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

    full_link = st.sidebar.text_input("Enter the link Here")
    platform = st.sidebar.selectbox("Select Platform", ["Amazon", "Flipkart"])
    max_page = st.sidebar.number_input("Enter Max Pages", min_value=1, step=1)
    btn =  st.sidebar.button("Start")

    if btn:
        pattern = r'(https://www.amazon.in/[^/]+/product-reviews/[^/]+/ref=cm_cr_arp_d_paging_btm_next_)'
        match = re.search(pattern, full_link)

        if match:
            extracted_part = match.group(1)
            print(extracted_part)
            if platform == "Amazon":
                reviews = scrape_amazon_reviews(extracted_part, max_page)
            elif platform == "Flipkart":
                reviews = scrape_flipkart_reviews(full_link, max_page)
        else:
            print("Pattern not found in the link.")
        
        print(reviews)
        data_file = pd.DataFrame(reviews)
        # Perform sentiment analysis and further processing...
        st.write(data_file)
