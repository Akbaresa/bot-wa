from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager

def send_whatsapp_message():
    opt = webdriver.ChromeOptions()
    opt.add_argument("user-data-dir=C:/Users/Esa/AppData/Local/Google/Chrome/User Data")

    chrome_service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=chrome_service, options=opt)

    driver.get("https://web.whatsapp.com/")
    
    name = input("\n Masukkan nama Group/User : ")
    message = input("\n Masukkan Pesan : ")
    count = int(input("\n Masukkan berapa kali pesan di kirim :"))
    
    user = driver.find_element(By.XPATH,
        '//span[@title = "{}"]'.format(name)
    )
    user.click()
    
    text_box = driver.find_element(By.CLASS_NAME, "_3Uu1_")
    
    for i in range(count):
        text_box.send_keys(message)  
        driver.find_element(By.XPATH, '//button[@aria-label="Kirim"]').click()

def reps():
    print("Apakah kamu mau mengirim pesan lagi ")
    tanyaUser = input("tekan 'y' jika ya tekan 'n' jika tidak : ")
    if(tanyaUser == 'y' or tanyaUser == 'Y'):
        send_whatsapp_message()
        reps()
    elif(tanyaUser == 'N' or tanyaUser =='n'):
        print("terima kasih")
    else:
        print("masukkan format yang benar")
        reps()
        
send_whatsapp_message()
reps()