from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "https://www.dropbox.com/cli_link_nonce?nonce=100ee845527e8416e7089ced9b097243"
login = "benchbox@outlook.com"
passwd = "salou2010"

print "Create Driver"
driver = webdriver.Firefox()

driver.get(url)
# driver.get(self.url)
print driver.title

element = driver.find_element_by_xpath("//input[@name=]")

element.send_keys(login)
element.send_keys(passwd)


'''
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
'''

time.sleep(10)
driver.close()