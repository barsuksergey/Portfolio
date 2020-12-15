from time import sleep
import operator
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import datetime

Tomorrow = 'date_' + str(datetime.date.today() + datetime.timedelta(days=1))
afterTomorrow = 'date_' + str(datetime.date.today() + datetime.timedelta(days=2))

while True:
    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, executable_path=r"C:\chromedriver_win32\chromedriver.exe")
    driver.implicitly_wait(2)
    # driver = webdriver.Chrome()
    driver.get('https://myfit4less.gymmanager.com/portal/login.asp')
    email = driver.find_element_by_xpath("//input[@type='email']")
    email.send_keys('email') #input your email
    sleep(2)
    password = driver.find_element_by_xpath("//input[@type='password']")
    password.send_keys('password') # input your password
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    sleep(2)
    login = driver.find_element_by_id('loginButton').click()
    sleep(2)
    # noBooking = driver.find_element_by_xpath('//form[@id="doorPolicyForm"]/h2')
    # noBooking = noBooking.text
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    sleep(2)
    availableSlots = driver.find_element_by_class_name('available-slots').text

    if availableSlots != 'SELECT CLUB\nSELECT DAY':
        print('\nSlot AVAILABLE !' + str(datetime.date.today()))
    else:
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        sleep(2)
        selectDayButton = driver.find_element_by_id('btn_date_select').click()
        selectTomorrow = driver.find_element_by_id(Tomorrow).click()
        availableSlotsTomorrow = driver.find_element_by_class_name('available-slots').text
        sleep(2)
        if availableSlotsTomorrow != 'SELECT CLUB\nSELECT DAY':
            print ('\nSlot AVAILABLE !' + Tomorrow)
        else:
            html = driver.find_element_by_tag_name('html')
            html.send_keys(Keys.END)
            sleep(2)
            selectDayButton = driver.find_element_by_id('btn_date_select').click()
            selectAfterTomorrow = driver.find_element_by_id(afterTomorrow).click()
            availableSlotsAfterTomorrow = driver.find_element_by_class_name('available-slots').text
            sleep(2)
            if availableSlotsAfterTomorrow != 'SELECT CLUB\nSELECT DAY':
                print('\nSlot AVAILABLE !' + afterTomorrow)
            else:
                print('\nNo slots available... Checked on: ' + str(datetime.datetime.now().time())[:-7])
                driver.quit()
                sleep(60)
                
