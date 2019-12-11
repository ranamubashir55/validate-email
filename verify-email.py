from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re, time, csv
# Load proxy option
from selenium.webdriver.common.proxy import Proxy, ProxyType
import json, requests
from flask import Flask
from flask import request
import random
from urllib.request import urlopen
import urllib.request
from io import StringIO
import secrets
app = Flask(__name__)
import threading
import queue
# token = secrets.token_urlsafe(16)


def get_proxy():
    url = 'http://api.proxies.lol/?apiKey=182462648a2b4c6e9b752bdf09802a18'
    url2 = 'https://httpbin.org/ip'
    while True:
        response=requests.get(url)
        data = response.json()
        proxy = data["proxy"]
        print(data)
        print("Proxy ip is  ",proxy)
        try:
            print("Connecting Proxy ip.....")
            response = requests.get(url2,timeout=5, proxies={"http": proxy})
            print(response.json())
            break
        except:
            print("Skipping. Connnection error")
    return proxy


def google(email, proxy, que=None):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--headless')
    driver=""
    result=""
    email=email.strip()
    print("New request :",email)
    if "hotmail" in email or "live" in email or 'outlook' in email and "@" in email:
        driver=webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
        url ="""https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1565967985&rver=7.0.6738.0&wp=MBI_SSL&wreply=https:%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-signin%3Fru%3Dhttps%253A%252F%252Faccount.microsoft.com%252F%253Frefp%253Dsignedout-index%2526refd%253Dwww.google.com&lc=2057&id=292666&lw=1&fl=easi2 """
        driver.get(url)
        print("Checking email", email)
        try:
            input_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME,"loginfmt")))
            input_email.send_keys(email)
            try:
                time.sleep(1)
                input_email.send_keys(Keys.ENTER)
            except Exception:
                pass
            try:    
                verify = WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.ID,"idA_PWD_ForgotPassword")))
                if verify:
                    print("verified::::::::::::::",email)
                    result="Valid Email"
            except Exception as ex:
                print("Email dosent exist ", email)
                result="Invalid Email"
        except Exception as ex:
            print("Missing, or proxy ip is not connected",email)
            result="Proxy ip not connected, retry"

    elif "yahoo" in email or 'rocketmail' in email or 'ymail' in email and "@" in email:
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = proxy
        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)
        driver = webdriver.Chrome(desired_capabilities=capabilities, chrome_options=chrome_options)

        url ="""https://login.yahoo.com/"""
        driver.get(url)
        print("Checking email", email)
        try:
            input_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"login-username")))
            input_email.send_keys(email)
            try:
                time.sleep(1)
                input_email.send_keys(Keys.ENTER)
                time.sleep(1)
            except Exception:
                pass
            try:    
                verify = WebDriverWait(driver, 8).until(EC.presence_of_all_elements_located((By.ID,"login-passwd")))
                if verify:
                    print("verified::::::::::::::",email)
                    result="Valid Email"
            except Exception as ex:
                validation=driver.find_elements_by_css_selector("div.challenge-header")
                capcha=driver.find_elements_by_css_selector("iframe#recaptcha-iframe")
                if validation or capcha:
                    result="Valid Email"
                    print("verified::::::::::::::",email)
                else:
                    print("Email dosent exist ", email)
                    result="Invalid Email"
        except Exception as ex:
            print("Missing, or proxy ip is not connected",email)
            result="Proxy ip not connected, retry"

    elif "aol" in email and "@" in email:
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = proxy
        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)
        driver = webdriver.Chrome(desired_capabilities=capabilities, chrome_options=chrome_options)
        driver.get("https://login.aol.com/")
        print("Checking email", email)
        try:
            input_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"login-username")))
            input_email.send_keys(email)
            try:
                time.sleep(1)
                input_email.send_keys(Keys.ENTER)
            except Exception:
                pass
            try:    
                verify = WebDriverWait(driver, 8).until(EC.presence_of_all_elements_located((By.ID,"login-passwd")))
                
                if verify:
                    print("verified::::::::::::::::",email)
                    result="Valid Email"
            except Exception as ex:
                validation=driver.find_elements_by_css_selector("iframe#recaptcha-iframe")
                if validation:
                    result="Valid Email"
                    print("verified::::::::::::::",email)
                else:
                    print("Email dosent exist ", email)
                    result="Invalid Email"
        except Exception as ex:
            print("Missing, or proxy ip is not connected",email)
            result="Proxy ip not connected, retry"

    elif "gmail" in email and "@" in email:
        driver=webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
        url ="""https://accounts.google.com/ServiceLogin/identifier?service=mail&passive=true&rm=false&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F%3Ftab%3Drm%26ogbl&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1&flowName=GlifWebSignIn&flowEntry=AddSession"""
        driver.get(url)
        print("Checking email", email)
        try:
            input_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"Email")))  #identifierId
            input_email.send_keys(email)
            try:
                time.sleep(1)
                input_email.send_keys(Keys.ENTER)
            except Exception:
                pass
            try:    
                verify = WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.ID,"Passwd")))   #Name=>password
                if verify:
                    print("verified::::::::::::::",email)
                    result="Valid Email"
            except Exception as ex:
                print("Email dosent exist ", email)
                result="Invalid Email"
        except Exception as ex:
            print("Missing, or proxy ip is not connected",email)
            result="Proxy ip not connected, retry"

    elif "zoho" in email and "@" in email:
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = proxy
        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)
        driver = webdriver.Chrome(desired_capabilities=capabilities, chrome_options=chrome_options)
        url ="""https://accounts.zoho.com/signin?servicename=VirtualOffice&signupurl=https://www.zoho.com/mail/zohomail-pricing.html&serviceurl=https://mail.zoho.com"""
        driver.get(url)
        print("Checking email", email)
        try:
            input_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"login_id")))
            input_email.send_keys(email)
            try:
                time.sleep(1)
                input_email.send_keys(Keys.ENTER)
            except Exception:
                pass
            try:    
                verify = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.fielderror.errorlabel")))
                print("Email dosent exist ", email)
                result="Invalid Email"
            except Exception as ex:
                print("verified::::::::::::::",email)
                result="Valid Email"

        except Exception as ex:
            print("Missing, or proxy ip is not connected",email)
            result="Proxy ip not connected, retry"
    
    elif "icloud" in email and "@" in email:
        driver=webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
        url ="""https://appleid.apple.com/account#!&page=create"""
        driver.get(url)
        print("Checking email", email)
        try:
            input_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"input.email-field")))
            input_email.send_keys(email)
            try:
                time.sleep(1)
                input_email.send_keys(Keys.TAB)
            except Exception:
                pass
            try:    
                verify = WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.idms-error")))
                if verify and "email address is not available" in verify[0].text.lower():
                    print("verified::::::::::::::",email)
                    result="Valid Email"
                else:
                    raise Exception
            except Exception as ex:
                print("Email dosent exist ", email)
                result="Invalid Email"

        except Exception as ex:
            print("Missing, or proxy ip is not connected",email)
            result="Proxy ip not connected, retry"


    else:
        print("invalid Email ",email)
        result="Invalid Email"
    if driver:
        driver.quit()
    if que:
        que.put({"status":result,"email":email})
    if que==None:
        return {"status":result,"email":email}

@app.route('/mails/', methods=['POST','GET'])
def get_file():
    final_data=[]
    threads=[]
    token="Vf8gk0KEOcuxlLnP8dZ6ww"
    data=request.get_json()
    key=request.args.get("key")
    if key!=token:
        return "Invalid API Key"
    
    print(data['data'])
    q = queue.Queue()

    th_count=0
    for email in data.get('data'):
        proxy=get_proxy()
        if email:
            t = threading.Thread(target=google, args=(email, proxy, q))
            t.start()
            threads.append(t)
            th_count=+1

        if th_count==20:
            for process in threads:
                process.join()
            th_count=0

    for process in threads:
        process.join()

    while not q.empty():
        result = q.get()
        c=1
        if "retry" in result:
            while True:
                proxy=get_proxy()
                t = threading.Thread(target=google, args=(email, proxy, q))
                t.start()
                t.join()
                result = q.get()
                if not "retry" in result or "invalid Email" in result or "Valid Email" in result or c==3:
                    break
                c=c+1
        final_data.append(result)
    
    return {"data":final_data}

@app.route('/email/', methods=['POST','GET'])
def get_email():
    email=request.args.get("email")
    token="Vf8gk0KEOcuxlLnP8dZ6ww"
    key=request.args.get("key")
    if key!=token:
        return "Invalid Key"
    if '@' in email:
        proxy=get_proxy()
        result = google(email, proxy)
        c=1
        if "retry" in result:
            while True:
                proxy=get_proxy()
                result = google(email, proxy)
                if not "retry" in result or "invalid Email" in result or "Valid Email" in result or c==3:
                    break
                c=c+1
        return result
    else:
        return "Invalid Email"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
