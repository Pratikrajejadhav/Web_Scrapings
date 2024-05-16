import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup
import pandas as pd



# Web driver
driver = webdriver.Chrome()

def scrape_amazon_reviews(url, max_page=5):
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

        try:
            next_button = driver.find_element(By.XPATH, "//li[@class='a-last']//a")
            next_button.click()
            WebDriverWait(driver, 10).until(EC.url_changes(page_url))
        except NoSuchElementException:
            print("Next Page not found")
            break

    return reviews

def scrape_flipkart_reviews(url, max_page=5):
    reviews = []
    headers = {
        'User-Agent': 'Use your own user agent',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    for i in range(1, max_page + 1):
        page_url = f'{url}{i}'
        page = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        names = soup.find_all('p', class_='_2NsDsF AwS1CA')
        titles = soup.find_all('p', class_='z9E0IG')
        ratings = soup.find_all('div', class_=['XQDdHH Ga3i8K', 'XQDdHH Czs3gR Ga3i8K' , 'XQDdHH Js30Fc Ga3i8K'])
        comments = soup.find_all('div', class_='ZmyHeo')

        for name, title, rating, comment in zip(names, titles, ratings, comments):
            review_data_dict = {}
            review_data_dict['reviewer_name'] = name.get_text()
            review_data_dict['review_title'] = title.get_text()
            review_data_dict['rating'] = rating.get_text() if rating else '0'
            review_data_dict['review_text'] = comment.div.div.get_text(strip=True)
            reviews.append(review_data_dict)

    return reviews

# Streamlit code
st.title('Web Scraping App')

option = st.sidebar.selectbox(
    'Which website do you want to scrape?',
    ('Amazon', 'Flipkart')
)

url = st.sidebar.text_input('Enter the URL of the product')

if st.sidebar.button('Scrape'):
    if option == 'Amazon':
        reviews = scrape_amazon_reviews(url)
    else:
        reviews = scrape_flipkart_reviews(url)

    df = pd.DataFrame(reviews)
    st.write(df)



driver.close()
