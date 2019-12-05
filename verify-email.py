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


def google(email, proxy):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver=""
    result=""
    email=email.strip()
    print("New request :",email)
    if "hotmail" in email or "live" in email and "@" in email:
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

    elif "yahoo" in email and "@" in email:
        driver=webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
        url ="""https://login.yahoo.com/"""
        driver.get(url)
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
                verify = WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.ID,"login-passwd")))
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
        driver = webdriver.Chrome(desired_capabilities=capabilities)
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
            input_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"identifierId")))
            input_email.send_keys(email)
            try:
                time.sleep(1)
                input_email.send_keys(Keys.ENTER)
            except Exception:
                pass
            try:    
                verify = WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.NAME,"password")))
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
        driver = webdriver.Chrome(desired_capabilities=capabilities)
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
    return {"status":result,"email":email}

@app.route('/mails/', methods=['POST','GET'])
def get_file():
    final_data=[]
    token="Vf8gk0KEOcuxlLnP8dZ6ww"
    # mail_list=str(request.args.get("list"))
    data=request.get_json()
    key=request.args.get("key")
    if key!=token:
        return "Invalid API Key"
    # mails=mail_list.split(",")
    print(data['data'])
    # try:
    #     response = urlopen(path).read().decode('ascii','ignore')
    #     datafile= StringIO(response)
    #     mails = csv.reader(datafile)
    # except Exception:
    #     return "No file found, or invalid format"
    for email in data.get('data'):
        # email=email.replace("[","").replace("]","")
        proxy=get_proxy()
        if email:
            result = google(email, proxy)
        c=1
        if "retry" in result:
            while True:
                proxy=get_proxy()
                result = google(email, proxy)
                if not "retry" in result or "invalid Email" in result or "Valid Email" in result or c==3:
                    break
                c=c+1
        final_data.append(result)
    # no=random.randint(5,123456890)  
    # file_path = "output/result-list"+str(no)+".csv"
    # for x in final_data:
    #     with open(file_path,mode='a') as output_file:
    #         writer = csv.writer(output_file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
    #         rst = x.split("-")
    #         writer.writerow([rst[1].strip() ,rst[0]])
    return {"data":final_data}

@app.route('/email/', methods=['POST'])
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
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)