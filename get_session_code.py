from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
import threading

app = Flask(__name__)

def wait_and_quit(driver):
    time.sleep(60)
    driver.quit()

@app.route('/api/get-code', methods=['POST'])
def get_code():
    data = request.json
    
    if 'no' not in data:
        return jsonify({'error': 'no pesan diperlukan'}), 400
    
    no = data['no']
    
    opt = webdriver.ChromeOptions()
    opt.add_argument("user-data-dir=C:/Users/Esa/AppData/Local/Google/Chrome/User Data")
    # opt.add_argument("user-data-dir=/home/username/.config/google-chrome/")
    # opt.add_argument("--window-size=1920,1080")
    # opt.add_argument("--headless=new")
    # opt.add_argument("--window-size=1920,1080") 
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=opt)
    driver.get("https://web.whatsapp.com/")
    
    driver.implicitly_wait(60)
    link = driver.find_element(By.XPATH, '//span[@class = "_3iLTh"]')
    driver.implicitly_wait(1)
    link.click()
    driver.implicitly_wait(30)
    input_nomer = driver.find_element(By.XPATH, '//input[@value = "+62 "]')
    driver.implicitly_wait(2)
    input_nomer.send_keys(no)
    driver.implicitly_wait(30)
    button_send = driver.find_element(By.CLASS_NAME, "szmswy5k")
    driver.implicitly_wait(2)
    button_send.click()
    driver.implicitly_wait(30)

    kode_elements = driver.find_elements(By.XPATH, '//span[contains(@class, "qfejxiq4")]')

    kode_list = []

    for kode_element in kode_elements:
        kode = kode_element.text
        kode_list.append(kode)
    
    response = jsonify({'kode' : kode_list})
    
    threading.Thread(target=wait_and_quit, args=(driver,)).start()
    
    return response, 200

if __name__ == '__main__':
    app.run(debug=True)
