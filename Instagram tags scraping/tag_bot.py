# Make sure to to have Chrome driver installed (and added to PATH if on Windows, or specify PATH as first argument on line 50).

from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
import smtplib, ssl
from tabulate import tabulate

# Populate your own info, LOGIN and PASSWORD are for Instagram, EMAIL and PASSWORD_EMAIL are for your GMAIL account, RECEIVER_EMAIL is email to send to
LOGIN = " "
PASSWORD = " "
EMAIL = ' '
PASSWORD_EMAIL = ' '
RECEIVER_EMAIL = ' '
TAT_TAGS = ['#tattoo', '#whipshading', '#blackandgrey', '#realistictattoo', '#tattoorealism', '#femaletattooartist']
ART_TAGS = ['#fluidart','#acrylicpainting', '#abstractart', '#abstractpainting', '#contemporaryart', '#modernpainting', '#art']


def get_similar_tags(x):
    similar_tags = []
    for tag in x:
        search_item = browser.find_element_by_xpath("//input[@placeholder='Search']")
        search_item.send_keys(tag)
        web_elements = browser.find_elements_by_partial_link_text(tag)
        for web_element in web_elements:
            similar_tags.append(web_element.text)
        search_item.clear()

    data = []
    for tag in similar_tags:
        tag_name = tag.split('\n')[0]
        tag_count = int(tag.split('\n')[1].split(" ")[0].replace(",",""))
        if tag_count < 1000000 and tag_count > 100000:
            data.append({'tag': tag_name,
                    'posts': tag_count})
        else:
            continue

    df = pd.DataFrame(data)

    port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(EMAIL, PASSWORD_EMAIL)
        server.sendmail(EMAIL, RECEIVER_EMAIL, tabulate(df,headers=df.columns))

Options = Options()
Options.add_argument("--log-level=3")
browser = webdriver.Chrome(options=Options)
browser.implicitly_wait(3)
browser.get('https://www.instagram.com/')

user_login = browser.find_elements_by_css_selector("input")[0]
user_login.click()
user_login.send_keys(LOGIN)
user_password = browser.find_elements_by_css_selector("input")[1]
user_password.click()
user_password.send_keys(PASSWORD)
browser.find_element_by_xpath("//button[@type='submit']").click()
browser.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
sleep(2)
browser.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

get_similar_tags(TAT_TAGS)
get_similar_tags(ART_TAGS)

browser.quit()
