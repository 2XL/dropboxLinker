#from selenium.webdriver.common.keys import Keys
#from threading import Thread
import subprocess
import getpass
import re
import os
from time import gmtime, strftime
from selenium import webdriver
import time


class Linker(object):

    def __init__(self, login, passwd):
        print "Constructor"
        self.login = login
        self.passwd = passwd
        self.worker = None
        self.url = None
        self.url_stream = "dropbox.out"

        if 'DISPLAY' in os.environ:
            self.display_idx = os.environ['DISPLAY']  # store the display variable
        else:
            self.display_idx = None

        self.display_idx_virtual = ":19"  # use this virtual display index

    def pre_requisite(self):
        # 1. no dropbox instance is running
        self.bash_command("dropbox stop")
        time.sleep(10)   # dejar 5 segundos para que se detenga dropbox
        # 2. dropbox.out is empty
        self.bash_command("rm {}".format(self.url_stream))
        # 3. there is no account assigned
        self.bash_command("rm ~/.dropbox -r")

    def start_dropboxd(self):
        print "dropboxd"
        # run dropbox
        dropboxd = ".dropbox-dist/dropboxd"
        cmd_run = "nohup /home/{}/{} &> {}& ".format(getpass.getuser(), dropboxd, self.url_stream)
        print "run: {}".format(cmd_run)
        # 1. need to unse the display env var such the dropbox detects no display
        self.bash_command('unset DISPLAY ')
        print self.bash_command(cmd_run)

    def setup_link(self):
        while True:
            time.sleep(5)
            print self.getTime()
            exitcode, line = self.bash_command("tail -n 1 {} ".format(self.url_stream))
            print line
            if "nonce=" in line:
                self.url_stream = line
                break
        # stop tail
        # extract the url and try to join user+pass using selenium
        # Join
        # Please visit https://www.dropbox.com/cli_link_nonce?nonce=9584747840078fcb7b28ffb0d8c53770 to link this device.
        self.url = re.search("(?P<url>https?://[^\s]+)", line).group("url")
        return self.url

    def join_dropbox(self):
        print "Join Dropbox"
        # 1. create virtual display
        try:
            # print self.bash_command('sudo Xvfb {} -ac & '.format(self.display_idx_virtual))
            # bash_command()
            print "ASDF"
        except Exception:
            print Exception.message
        # 2. set display
        print "Set display"
        os.environ["DISPLAY"] = self.display_idx_virtual
        print os.environ['DISPLAY']
        # Create a new instance of the Firefox driver
        #########################################################
        # url = "https://www.dropbox.com/cli_link_nonce?nonce=36652c830f61da87b4107faf0aa5ff7b"
        # login = self.login
        # passwd = self.passwd
        print "Create Driver"
        driver = webdriver.Firefox()
        driver.get(self.url)
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
        # print str
        driver.execute_script(str)
        time.sleep(5)
        result = driver.execute_script("document.getElementsByClassName('page-header-text')[0].innerHTML")
        print result
        time.sleep(1)
        driver.close()
        ###########################################################

    def getTime(self):
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def bash_command(slef, cmd):
        child = subprocess.Popen(['/bin/bash', '-c', cmd], stdout=subprocess.PIPE)
        output = child.stdout.readline()
        child.communicate()[0]
        rc = child.returncode
        return rc, output

    def revert_display(self):
        if self.display_idx is None:
            print "noop"
        else:
            print "revert display to: {}".format(self.display_idx)
            os.environ["DISPLAY"] = self.display_idx

if __name__ == "__main__":
    print "linker"
    login = "benchbox@outlook.com"
    passwd = "salou2010"
    linker = Linker(login=login, passwd=passwd)
    linker.start_dropboxd()
    linker.setup_link()
    linker.join_dropbox()
    linker.revert_display()
    print "end_linking"

