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
    
    if 'name' not in data or 'message' not in data or 'iterasi' not in data:
        return jsonify({'error': 'Nama, pesan, dan iterasi diperlukan'}), 400
    
    opt = webdriver.ChromeOptions()
    opt.add_argument("user-data-dir=C:/Users/Esa/AppData/Local/Google/Chrome/User Data")
    # opt.add_argument("user-data-dir=/home/username/.config/google-chrome/")
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=opt)
    driver.get("https://web.whatsapp.com/")
    
    name = data['name']
    message = data['message']
    
    try:
        count = int(data['iterasi']) 
    except ValueError:
        driver.quit()
        return jsonify({'error': 'Iterasi harus berupa bilangan bulat'}), 400
    
    try:
        time.sleep(30)
        user = driver.find_element(By.XPATH, '//span[@title = "{}"]'.format(name))
        time.sleep(1)
        user.click()
        time.sleep(1)
        text_box = driver.find_element(By.CLASS_NAME, "_3Uu1_")
        for i in range(count):
            text_box.send_keys(message)  
            time.sleep(0.3)
            driver.find_element(By.XPATH, '//button[@aria-label="Kirim"]').click()
        time.sleep(1)
        driver.quit()
    except NoSuchElementException:
        driver.quit()
        return jsonify({'error': 'Grup/Pengguna tidak ditemukan'}), 404
    
    return jsonify({'message': 'Pesan WhatsApp berhasil dikirim'})

if __name__ == '__main__':
    app.run(debug=True)
