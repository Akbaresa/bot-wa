from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time

app = Flask(__name__)

@app.route('/api/send-whatsapp', methods=['POST'])
def send_whatsapp_message():
    data = request.json
    
    if 'no' not in data or 'message' not in data:
        return jsonify({'error': 'Nama, pesan, dan iterasi diperlukan'}), 400
    
    nomer = data['no']
    message = data['message']
    opt = webdriver.ChromeOptions()
    opt.add_argument("user-data-dir=C:/Users/Esa/AppData/Local/Google/Chrome/User Data")
    # opt.add_argument("user-data-dir=/home/username/.config/google-chrome/")
    opt.add_argument("--headless")
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=opt)
    link_wa = "https://api.whatsapp.com/send/?phone=%2B{}".format(nomer) + "&text={}".format(message) + "&type=phone_number&app_absent=0""https://api.whatsapp.com/send/?phone=%2B{}".format(nomer) + "&text={}".format(message) + "&type=phone_number&app_absent=0"
    driver.get(link_wa)
    time.sleep(5)
    link = driver.find_element(By.ID, 'action-button')
    time.sleep(2)
    link.click()
    time.sleep(2)
    web_wa_button = driver.find_element(By.XPATH, '//span[text()="gunakan WhatsApp Web"]')
    # web_wa_button = driver.find_element(By.XPATH, '//span[text()="use WhatsApp Web"]')
    time.sleep(2)
    web_wa_button.click()
    time.sleep(20)
    send = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
    time.sleep(2)
    send.click()
    time.sleep(2)
    return jsonify({'message': 'Pesan WhatsApp berhasil dikirim'})

if __name__ == '__main__':
    app.run(debug=True)