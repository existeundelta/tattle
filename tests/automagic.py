from selenium import webdriver
from selenium.webdriver.common.keys import Keys
 
# create a new Firefox session
browser = webdriver.Firefox()
browser.implicitly_wait(30)
browser.maximize_window()

# navigate to the application home page
browser.get("http://www.google.com")

# get the search textbox
search_field = browser.find_element_by_id("lst-ib")
search_field.clear()

# enter search keyword and submit
search_field.send_keys("Selenium WebDriver Interview questions")
search_field.submit()

# get the list of elements which are displayed after the search
# currently on result page using find_elements_by_class_name  method
lists= browser.find_elements_by_class_name("_Rm")

# get the number of elements found
print (“Found “ + str(len(lists)) + “searches:”)

# iterate through each element and print the text that is
# name of the search
i=0
for listitem in lists:
   print (listitem)
   i=i+1
   if(i>10):
      break

# close the browser window
browser.quit()
browser.execute_script("submitForm()")

browser = webdriver.Firefox()
browser.get('http://gbrapps/')
browser.implicitly_wait(10)
browser.save_screenshot('C://Users//nfarring//Desktop//firefox_screenie.png')
browser.quit()browser.get('http://deusaheid016:19086/portal/lms.jsp')
browser.implicitly_wait(10)
browser.save_screenshot('C://Users//nfarring//Desktop//firefox_screenie.png')
browser.quit()

## c h r o m e - login to HRHX
import time
import selenium.webdriver.chrome.service as service
service = service.Service('chromedriver.exe')
service.start()
capabilities = {'chrome.binary': 'c://windows//system32//chromedriver'}
browser = webdriver.Remote(service.service_url, capabilities)

browser.get('http://deusgheid0005:19086/admin/');
browser.implicitly_wait(10)
time.sleep(5) # Let the user actually see something!
#browser.quit()

browser = webdriver.Chrome()
browser.get('http://deusgheid0005:19086/admin/')
browser.implicitly_wait(10)
browser.save_screenshot('C://Users//nfarring//Desktop//chrome_screenie.png')
browser.quit()


## I E 1 1 - autologin to GBRAPPS 
browser = webdriver.Ie()
browser.get("http://gbrapps/")
browser.switch_to_frame(browser.find_element_by_tag_name("iframe"))
username = browser.find_element_by_id("user")
password = browser.find_element_by_id("password")
username.send_keys('nfarring')
password.send_keys(secret)
browser.execute_script("submitForm()")
