from datetime import datetime

import requests
import wikipedia
from bs4 import BeautifulSoup
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
translator = Translator()


def query_wikipedia(query: str) -> str:
    """
    Retrieves a summary of the provided Wikipedia query.

    :param query: The topic to search for on Wikipedia
    :type query: str

    :return: A summary of the first matching Wikipedia article
    :rtype: str
    """
    return wikipedia.summary(query, sentences=3, auto_suggest=True)


def search_youtube(query: str) -> None:
    """
    Opens the top result for the provided query on YouTube in a new browser window.

    :param query: The search query to use on YouTube
    :type query: str
    """
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://www.youtube.com/results?search_query={query}")
    video = driver.find_element(By.XPATH, '//*[@id="video-title"]').get_attribute("href")
    driver.get(video)


def send_whatsapp_message(message: str, phone_number: str) -> None:
    """
    Sends a WhatsApp message to the provided phone number.

    :param message: The text of the message to send
    :type message: str

    :param phone_number: The phone number to send the message to
    :type phone_number: str
    """
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://wa.me/{phone_number}?text={message}")


def get_current_datetime() -> str:
    """
    Retrieves the current date and time in the format 'YYYY-MM-DD HH:MM:SS'.

    :return: The current date and time
    :rtype: str
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now


def translate_text(text: str, src: str = "auto", dest: str = "en") -> str:
    """
    Translates the provided text to the specified language.

    :param text: The text to translate
    :type text: str

    :param src: The language of the text (default is 'auto')
    :type src: str

    :param dest: The language to translate the text to (default is 'en')
    :type dest: str

    :return: The translated text
    :rtype: str
    """
    translated_text = translator.translate(text, src=src, dest=dest)
    return translated_text.text


def get_next_prayer_time() -> str:
    """
    Retrieves the time for the next prayer from Google.

    :return: The time for the next prayer
    :rtype: str
    """
    html_response = requests.get('https://www.google.com/search?q=prayer+times&hl=en', headers=HEADERS)
    soup = BeautifulSoup(html_response.content, 'html.parser')
    next_prayer_time = soup.find('div', attrs={"class": "Uaexyd"}).text
    return next_prayer_time


def get_current_temperature() -> str:
    """
    Retrieves the current temperature from Google.

    :return: The current temperature
    :rtype: str
    """
    html_response = requests.get('https://www.google.com/search?q=temperature&hl=en', headers=HEADERS)
    soup = BeautifulSoup(html_response.content, 'html.parser')
    temperature = soup.find('div', attrs={"class": "vk_bk TylWce SGNhVe"})
    temperature = temperature.find('span', attrs={"style": "display:inline"}).text
    unit = soup.find('div', attrs={"class": "vk_bk wob-unit"})
    unit = unit.find('span', attrs={"style": "display:inline"}).text
    return f"Temperature now is {temperature}{unit}"


def get_latest_news() -> list[str]:
    """
    Retrieves a list of the latest news from Google.

    :return: A list of the latest news
    :rtype: list[str]
    """
    html_response = requests.get('https://www.google.com/search?q=news&hl=en', headers=HEADERS)
    soup = BeautifulSoup(html_response.content, 'html.parser')
    news = soup.find_all('div', attrs={"class": "mCBkyc tNxQIb ynAwRc nDgy9d"})
    news = [i.text.replace("...", "").strip() for i in news]
    return news
