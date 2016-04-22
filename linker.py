from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from threading import Thread
import subprocess
import getpass
import re
import os
import time
from time import gmtime, strftime



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
        print "Create Driver"
        driver = webdriver.Firefox()
        driver.get("http://www.python.org")
        # driver.get(self.url)
        assert "Python" in driver.title
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        driver.close()
        ###########################################################
        while True:
            print "Join {}, {}".format(self.getTime(), self.url)
            time.sleep(5)
            # break

    def getTime(self):
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def bash_command(slef, cmd):
        child = subprocess.Popen(['/bin/bash', '-c', cmd], stdout=subprocess.PIPE)
        output = child.stdout.readline()
        child.communicate()[0]
        rc = child.returncode
        return rc, output

    def rever_display(self):
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
    linker.rever_display()

