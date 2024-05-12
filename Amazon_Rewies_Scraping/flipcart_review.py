import streamlit as st


# https://www.flipkart.com/apple-iphone-15-plus-black-256-gb/product-reviews/itm4b0608e773fc5?pid=MOBGTAGPWKT2VSBB&lid=LSTMOBGTAGPWKT2VSBBYV0FGC&marketplace=FLIPKART
import requests
from bs4 import BeautifulSoup
import pandas as pd


# User-Agent and Accept-Language headers
headers = {
    'User-Agent': 'Use your own user agent',
    'Accept-Language': 'en-us,en;q=0.5'
}
customer_names = []
review_title = []
ratings = []
comments = []

for i in range(1,11):
    # Construct the URL for the current page
    
    # url = "https://www.flipkart.com/apple-iphone-15-plus-black-256-gb/product-reviews/itm4b0608e773fc5?pid=MOBGTAGPWKT2VSBB&lid=LSTMOBGTAGPWKT2VSBBYV0FGC&marketplace=FLIPKART&page="+str(i)
    url = (f'{put_url}&page="{str(i)}')
    # Send a GET request to the page
    page = requests.get(url, headers=headers)

    # Parse the HTML content
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract customer names
    names = soup.find_all('p', class_='_2NsDsF AwS1CA')
    for name in names:
        customer_names.append(name.get_text())

    # Extract review titles
    title = soup.find_all('p', class_='z9E0IG')
    for t in title:
        review_title.append(t.get_text())

    # Extract ratings
    rat = soup.find_all('div', class_=['XQDdHH Ga3i8K', 'XQDdHH Czs3gR Ga3i8K' , 'XQDdHH Js30Fc Ga3i8K'])
    for r in rat:
        rating = r.get_text()
        if rating:
            ratings.append(rating)
        else:
            ratings.append('0')  # Replace null ratings with 0

    # Extract comments
    cmt = soup.find_all('div', class_='ZmyHeo')
    for c in cmt:
        comment_text = c.div.div.get_text(strip=True)
        comments.append(comment_text)

# Ensure all lists have the same length
min_length = min(len(customer_names), len(review_title), len(ratings), len(comments))
customer_names = customer_names[:min_length]
review_title = review_title[:min_length]
ratings = ratings[:min_length]
comments = comments[:min_length]

# Create a DataFrame from the collected data
data = {
    'Customer Name': customer_names,
    'Review Title': review_title,
    'Rating': ratings,
    'Comment': comments
}

df = pd.DataFrame(data)

put_url = st.text_input("Enter_url")
btn=st.button("Get")

st.write(df)
