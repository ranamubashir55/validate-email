import sys, requests,json
import urllib.request
from selenium import webdriver

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

proxy=get_proxy()

# driver = webdriver.Firefox("geckodriver.exe")


# proxy = "212.66.117.168:41258"
import pdb; pdb.set_trace()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://%s' %proxy)
driver=webdriver.Chrome("chromedriver.exe", options=chrome_options)

firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True

firefox_capabilities['proxy'] = {
    "proxyType": "MANUAL",
    "httpProxy": proxy
}

driver = webdriver.Firefox(capabilities=firefox_capabilities)