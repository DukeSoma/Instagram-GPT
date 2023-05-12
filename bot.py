import asyncio
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai_secret_manager import Secrets
import openai

secrets = Secrets()
assert "openai" in secrets.get_services()
openai_secret = secrets.get_secret("openai")
openai.api_key = openai_secret["api_key"]

async def generate_response(prompt):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2500,
        n=1,
        stop=None,
        temperature=0.5
    ))
    return response['choices'][0]['text']

async def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    driver.get('https://www.instagram.com/')

    # login ke Instagram
    username = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    password = driver.find_element_by_name('password')
    username.send_keys('your_username')
    password.send_keys('your_password')
    login_button = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
    login_button.click()

    # arahkan ke DM
    driver.get('https://www.instagram.com/direct/inbox/')

    # loop melalui semua percakapan yang tersedia
    conversations = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="react-root"]/section/div/div[2]/div/div/div[1]/div[2]/div/div/div/div')))
    for conversation in conversations:
        conversation.click()

        # dapatkan pesan terakhir dalam percakapan
        messages = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'message-text')))
        last_message = messages[-1].text

        # mengekstrak informasi spesifik dari pesan menggunakan ekspresi reguler
        match = re.search(r'What is the weather like in (.+?)\?', last_message)
        if match:
            location = match.group(1)
            # menghasilkan respons menggunakan GPT OpenAI dan informasi yang diekstraksi
            response = await generate_response(f"What is the weather like in {location}?")
        else:
            # menghasilkan respons umum menggunakan GPT OpenAI
            response = await generate_response(last_message)

        # kirim tanggapan
        text_input = driver.find_element_by_tag_name('textarea')
        text_input.send_keys(response)
        send_button = driver.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button')
        send_button.click()

asyncio.run(main())