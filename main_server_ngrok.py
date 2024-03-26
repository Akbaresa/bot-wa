from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
import threading


app = Flask(__name__)

opt = webdriver.ChromeOptions()
opt.add_argument("user-data-dir=C:/Users/Esa/AppData/Local/Google/Chrome/User Data")
chrome_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome_service, options=opt)

def wait_and_quit(driver):
    time.sleep(60)
    driver.quit()

@app.route('/api/get-code', methods=['POST'])
def get_code():
    data = request.json
    
    if 'no' not in data:
        return jsonify({'error': 'no pesan diperlukan'}), 400
    
    no = data['no']
    
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

@app.route('/api/send-whatsapp', methods=['POST'])
def send_whatsapp_message():
    data = request.json
    
    if 'no' not in data or 'message' not in data:
        return jsonify({'error': 'Nama, pesan, dan iterasi diperlukan'}), 400
    
    nomer = data['no']
    message = data['message']
    link_wa = "https://api.whatsapp.com/send/?phone=%2B{}".format(nomer) 
    + "&text={}".format(message) 
    + "&type=phone_number&app_absent=0""https://api.whatsapp.com/send/?phone=%2B{}".format(nomer) 
    + "&text={}".format(message) 
    + "&type=phone_number&app_absent=0"
    driver.get(link_wa)
    driver.implicitly_wait(60)
    link = driver.find_element(By.ID, 'action-button')
    driver.implicitly_wait(60)
    link.click()
    driver.implicitly_wait(60)
    web_wa_button = driver.find_element(By.XPATH, '//span[text()="gunakan WhatsApp Web"]')
    # web_wa_button = driver.find_element(By.XPATH, '//span[text()="use WhatsApp Web"]')
    driver.implicitly_wait(60)
    web_wa_button.click()
    driver.implicitly_wait(240)
    time.sleep(2)
    send = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
    time.sleep(2)
    driver.implicitly_wait(60)
    time.sleep(2)
    send.click()
    time.sleep(5)
    return jsonify({'message': 'Pesan WhatsApp berhasil dikirim'})


@app.route('/api/cek', methods=['GET'])
def cek():
    try:
        driver.get("https://web.whatsapp.com/")
        driver.implicitly_wait(10)
        profil = find_profil()
        
        time.sleep(1)
        profil.click()
        time.sleep(1)
        driver.implicitly_wait(10)
        user_element = driver.find_element(By.XPATH, '//span[@class="f804f6gw ln8gz9je"]')
        user = user_element.text
        time.sleep(1)
    except:
        return jsonify({'koneksi internet anda lemot'}),200  
    driver.quit()
    return jsonify({'user' : user}),200

def find_profil():
    try:
        profil = driver.find_element(By.XPATH, '//div[@aria-label="foto profil"]')
        return profil
    except NoSuchElementException:
        try:
            profil_english = driver.find_element(By.XPATH, '//div[@aria-label="profile picture"]')
            return profil_english
        except NoSuchElementException:
            return None


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
