import streamlit as st
import pandas as pd
import os
import shutil
import requests
from bs4 import BeautifulSoup


# because i want to do AI
from openai import OpenAI

# variable assignments
key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=key)
insta_text = "Read more at link in bio."
spacers = "---------------------"


# stream creation
st.title("DCTA Assistant AI Editor")


option = st.sidebar.selectbox(
    "Social", ("Social Media Manager", "Headline Creation", "Editor")
)


url = st.text_input("Insert here: ")


def web_scraper():
    page = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.text, "html.parser")
    # soup_image = BeautifulSoup(page.content, "html.parser")

    # pull author name and show title
    author_name = soup.find("div", class_="td-post-author-name").text.rstrip(" -")[3:]
    show_name = soup.find("h1").text
    try:
        show_name = str(show_name.split("‘")[1].split("’")[0])
    except:
        pass

    # pull the text
    text = [i.text for i in soup.find_all("p")]
    all_text = " ".join(text)

    # pull the subheader
    sub_header = all_text.split(".")[0] + "."
    return all_text, show_name, author_name, sub_header


# if Social Media
if option == "Social Media Manager":
    try:
        all_text, show_name, author_name, sub_header = web_scraper()
        # display
        click_to_read = f"Click to read our review by {author_name}. #dctheatre"

        # things that print out.
        st.write(spacers)
        st.write(sub_header)
        st.write(click_to_read)
        st.write(url)
        st.write(spacers)
        st.write(sub_header, insta_text)
    except:
        st.write("Include DCTA Url Above")

if option == "Headline Creation":
    try:
        # scrape
        all_text, show_name, author_name, sub_header = web_scraper()
        # gpt the title
        completion = client.chat.completions.create(
            model="gpt-4o",
            frequency_penalty=2,
            temperature=0.8,
            top_p=0.8,
            messages=[
                {
                    "role": "system",
                    "content": f"You are an assistant to an theater review website editor. Create three options for headlines for the article using the following text: {url}.",
                }
            ],
        )
        gpt_content = completion.choices[0].message.content
        st.write("*Title Options*")
        st.write(gpt_content)

    except:
        st.write("Include DCTA Url Above")
if option == "Editor":
    try:

        completion = client.chat.completions.create(
            model="gpt-4o",
            frequency_penalty=2,
            temperature=0.8,
            top_p=0.8,
            messages=[
                {
                    "role": "system",
                    "content": f"You are an editor that for a website that covers theater reviews. Review the following text: {url}. Provide suggestions for improvement. If present, note any content that may be considered offensive or culturally inappropriate. If not present, do not note.",
                }
            ],
        )
        gpt_content = completion.choices[0].message.content
        st.write(gpt_content)

    except:
        st.write("Include DCTA Url Above")
