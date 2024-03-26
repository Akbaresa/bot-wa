from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time

app = Flask(__name__)

@app.route('/api/logout', methods=['GET'])
def logout():

    opt = webdriver.ChromeOptions()
    opt.add_argument("user-data-dir=C:/Users/Esa/AppData/Local/Google/Chrome/User Data")
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=opt)
    driver.get("https://web.whatsapp.com/")
    driver.implicitly_wait(60)
    send = driver.find_element(By.XPATH, '//span[@data-icon="menu"]')
    driver.implicitly_wait(60)
    time.sleep(1)
    send.click()
    time.sleep(1)
    out = driver.find_element(By.XPATH , '//div[@aria-label="Keluar"]')
    # out = driver.find_element(By.XPATH , '//div[@aria-label="Get out"]')
    time.sleep(1)
    driver.implicitly_wait(60)
    time.sleep(1)
    out.click()
    driver.implicitly_wait(60)
    keluar = driver.find_element(By.XPATH, '//div[text()="Keluar"]')
    time.sleep(1)
    keluar.click()
    time.sleep(1)
    return jsonify({'pesan' : 'berhasil logout'})

if __name__ == '__main__':
    app.run(debug=True)