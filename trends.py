import time, os
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

BROWSER_EXE = '/usr/bin/firefox'
GECKODRIVER = '/home/ssh-shashi/geckodriver'

FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)

PROFILE = webdriver.FirefoxProfile()
PROFILE.set_preference("dom.webnotifications.enabled", False)
PROFILE.set_preference("app.update.enabled", False)
PROFILE.update_preferences()

driver = webdriver.Firefox(executable_path=GECKODRIVER,
                                         firefox_binary=FIREFOX_BINARY,
                                         firefox_profile=PROFILE,)

url = "https://trends.google.com/trends"

driver.get(url)
driver.maximize_window()

WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID,'sidenav-menu-btn')))
sidenavbarbutton = driver.find_element(By.ID,"sidenav-menu-btn")
sidenavbarbutton.click()

WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div/header/side-nav-bar/md-sidenav/md-list/div[1]/md-item[2]/md-item-content/a')))
explorebutton = driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/header/side-nav-bar/md-sidenav/md-list/div[1]/md-item[2]/md-item-content/a")
explorebutton.click()

WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/div[1]/div/div[1]/md-icon')))
mapdataclearbutton=driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/div[1]/div/div[1]/md-icon")
mapdataclearbutton.click()


region_selection_button = driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/div/div/hierarchy-picker[1]/ng-include/div[1]")
region_selection_button.click()

input = driver.find_element(By.ID,"input-10")
input.send_keys("united states")


inputselectbutton=driver.find_element(By.XPATH,"/html/body/md-virtual-repeat-container[1]/div/div[2]/ul/li/md-autocomplete-parent-scope/div")
inputselectbutton.click()

duration_dropdown_click=driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/div/div/custom-date-picker/ng-include/md-select/md-select-value/span[1]/div")
duration_dropdown_click.click()


duration_selection=driver.find_element(By.XPATH,"/html/body/div[8]/md-select-menu/md-content/md-option[7]/div")
duration_selection.click()

cookies_okgotit_button=driver.find_element(By.XPATH,"/html/body/div[1]/div/span[2]/a[2]")
cookies_okgotit_button.click()

driver.refresh()

#Fetching the trending searches
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CLASS_NAME,'label-text')))

Title_temp = []
Values=[]
try:
    for i in range(20):

        content = driver.find_elements(By.CLASS_NAME,"label-text")
        
        for element in content:
            Title_temp.append(element.text)
        
        WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/ng-include/div/div[6]/pagination/div/button[2]/md-icon')))
        #The below is a button to move to the next slide in the top searches
        driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/ng-include/div/div[6]/pagination/div/button[2]/md-icon").click()

        
except:
    print('Error occurred')

# The below is a loop to get to the first slide so that we can fetch the rising values from the beginning
for i in range(20):
    WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/ng-include/div/div[6]/pagination/div/button[1]/md-icon')))
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/ng-include/div/div[6]/pagination/div/button[1]/md-icon").click()

# Fetching the rising values of the trending searches
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CLASS_NAME,'rising-value')))
try:
    for i in range(20):
        content = driver.find_elements(By.CLASS_NAME,"rising-value")
        for element in content:
            a=element.text
            Values.append(a)
        WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/ng-include/div/div[6]/pagination/div/button[2]/md-icon')))
        #The below is a button to move to the next slide in the top searches
        driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/ng-include/div/div[6]/pagination/div/button[2]/md-icon").click()
    
except:
    print('Error occurred')

dic = {}
for key in Title_temp:
    for value in Values:
        dic[key] = value
        Values.remove(value)
        break

dic1={}
K=300
for key in dic:
    # print(''.join(e for e in dic[key] if e.isdigit()))
    if int(''.join(e for e in dic[key] if e.isdigit()))>K:
        dic1[key]=dic[key]
with open("latest_trends.txt", 'w') as f:
    for key,value in dic1.items():
        f.write(key+","+value)
        f.write("\n")
print("data saved Successfully")

driver.close()
