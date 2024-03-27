from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import re


arg1 = "--profile-directory=Person1"
arg2 = "user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Person1"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(arg1)
chrome_options.add_argument(arg2)
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def write_info(data):
    try:
        with open("file/" + data[0] + '.csv', mode = 'a', newline='', encoding='utf-8') as file:
           writer = csv.writer(file)
           writer.writerow(data)
           return True
    except: 
        print("write error")
        return False
     
  # WRITE header into each business file
def write_header(companyname):
    header = [ 'company_name', 'street', 'city', 'state', 'zip_code' ]
    try:
        with open("file/" + companyname + ".csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            return True
    except: 
        print('write error')
        return False    

def Seperate_address(address):
    list = address.split(",")
    if len(list) == 2:
        street = ""
        city = ""
        str = list[0]
    elif len(list) == 5:
        street = list[1]
        city = list[2]
        str = list[3].replace(" ","")
    elif len(list) == 3:
        street = ''
        city = list[0]
        str = list[1].replace(" ", "")
    else:
        street = list[0]
        city = list[1]
        str = list[2].replace(" ", "")
    if len(list) == 2: 
        state = str
        zipcode = ""
    else:
        divi = re.match(r"([a-zA-Z]+)(\d+(?:-\d+)?)", str)
        if divi:
                state = divi.group(1)
                zipcode = divi.group(2)
        else: print("error occured")

    res = [ street, city, state, zipcode ]
    return res

def onedata(Companyname):
    print('Onedata')
    address = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[3]/button/div/div[2]/div[1]').text
    data = Seperate_address(address)
    data.insert(0, Companyname)
    print(data)
    write_info(data)

    return data

def moredata(Companyname):
    print("one more")
    while(True):
       try: 
          final = driver.find_element(By.CLASS_NAME, "HlvSq").text
          if final: break
       except:
          driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]").send_keys(Keys.DOWN)
    sleep(2)

    elements = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    print(len(elements))
    try:
        for i in range(len(elements)):
            print(i)
            try:
                WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "hfpxzc"))
                )
                print("Element is clickable!")
                elements[i].click()
            except Exception as e:
                print("Exception:", e)
            sleep(4)
            address = driver.find_element(By.CLASS_NAME, 'kR99db').text
            data = Seperate_address(address)
            data.insert(0, Companyname)
            print(data)
            sleep(2)
            write_info(data)
    except: print("error")

def start():
    driver.get("https://map.google.com")
    driver.maximize_window()

    try:
        WebDriverWait(driver, 7).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[1]/ul/li[1]/button"))
        )
        driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[1]/ul/li[1]/button").click()
    except Exception as e:
        print("Exception:", e)
    sleep(3
          )
    try:
        WebDriverWait(driver, 7).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[25]/div/div[2]/ul/div[7]/li[1]/button"))
        )
        driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[25]/div/div[2]/ul/div[7]/li[1]/button").click()
    except Exception as e:
        print("Exception:", e)
    sleep(3)
    try:
        WebDriverWait(driver, 7).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div[3]/div/div/div/div[2]/div[1]/div[11]/a"))
        )
        driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div[3]/div/div/div/div[2]/div[1]/div[11]/a").click()
    except Exception as e:
        driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div[2]/button").click()
    sleep(3)


    with open('company_names100-200.csv', 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            print(row['CompanyName'])
            if(row['CompanyName']):
                driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[1]/div/div[2]/form/input").clear()

                res = write_header(row['CompanyName'])
                if not res:
                   continue
                driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[1]/div/div[2]/form/input").send_keys(row['CompanyName'] + " in United States")
                sleep(1)
                driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[1]/div/div[2]/div[1]").click()

                sleep(3)
                elecss = WebDriverWait(driver, 7).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "T7HQDc"))
                )
                driver.execute_script("arguments[0].style.display ='none';" ,elecss)
                try:
                    soup = BS(driver.page_source, 'html.parser')
                    title = soup.find('h1', {'class': 'DUwDvf lfPIob'})
                    if title:
                        data = onedata(row['CompanyName'])
                    else:
                       data = moredata(row['CompanyName']) 
                except: 
                   flag = False
                   print("find one error")



start()