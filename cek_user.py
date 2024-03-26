from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time

app = Flask(__name__)

@app.route('/api/cek', methods=['GET'])
def cek():
    opt = webdriver.ChromeOptions()
    opt.add_argument("user-data-dir=C:/Users/Esa/AppData/Local/Google/Chrome/User Data")
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=opt)
    driver.get("https://web.whatsapp.com/")
    driver.implicitly_wait(60)
    profil = driver.find_element(By.XPATH, '//div[@aria-label="foto profil"]')
    time.sleep(1)
    profil.click()
    time.sleep(1)
    driver.implicitly_wait(10)
    user_element = driver.find_element(By.XPATH, '//span[@class="f804f6gw ln8gz9je"]')
    user = user_element.text
    time.sleep(1)
    return jsonify({'user' : user}),200


if __name__ == '__main__':
    app.run(debug=True)