from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "https://www.dropbox.com/cli_link_nonce?nonce=36652c830f61da87b4107faf0aa5ff7b"
login = "benchbox@outlook.com"
passwd = "salou2010"

print "Create Driver"
driver = webdriver.Firefox()

driver.get(url)
# driver.get(self.url)
print driver.title


str = """
console.log("Hello Script");
var items = (document.getElementsByTagName("form"));
for(var key in items){
    var dom = items[key]
    if(dom.action === "https://www.dropbox.com/cli_link_nonce")
    {
        // fill the form here
        console.log(dom);
        test = dom;
        var inputs = dom.getElementsByClassName('text-input-wrapper');
        console.log(inputs)
        for(var idx in inputs){
            var input =  inputs[idx];
            if(input instanceof HTMLElement)
            {
                var field = input.getElementsByTagName('input');
                var input_field = field[0];
                console.log(input_field);
                var str = input_field.getAttribute("type");
                switch (str){
                    case "email":
                        input_field.value = "%s";
                        break;
                    case "password":
                        input_field.value = "%s";
                        break;
                    default:
                        console.log("MISSING ATTR", str);
                        break;
                }
            }else {
                //noop
            }
        }
        dom.getElementsByClassName("login-button")[0].click()
    }
}
console.log("Bye script")
""" % (login, passwd)
print str

driver.execute_script(str)



'''
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
'''
time.sleep(5)
result = driver.execute_script("document.getElementsByClassName('page-header-text')[0].innerHTML")
time.sleep(1)
driver.close()