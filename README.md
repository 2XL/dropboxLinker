
0. linker.py 

1. INSTALL DROPBOX-DIST/DROPBOXD

2. RUN DROPBOXD
    1. this will generate the following output [con un thread auxiliar que mantenga el bucle]
        Please visit https://www.dropbox.com/cli_link_nonce?nonce=863e435d02ad72d8d7b873e81843c9fa to link this device.
        This computer isn't linked to any Dropbox account...
    2. extraer el url 





1. Selenium (tutorial) For headless automation, Selenium can be used in conjunction with PhantomJS

## Aux installation 4 Headless support

http://www.installationpage.com/selenium/how-to-run-selenium-headless-firefox-in-ubuntu/



### dependencies:

1. firefox
2. python-selenium




## usage:

```python
from linker import Linker

if __name__ == "__main__":
    print "linker"
    login = "benchbox@outlook.com"
    passwd = "salou2010"
    linker = Linker(login=login, passwd=passwd)
    linker.pre_requisite()
    linker.start_dropboxd()
    linker.setup_link()
    linker.join_dropbox()
    linker.revert_display()
    print "end_linking"
```



### output:



```javascript
vagrant@sandBox:/vagrant/dropboxLinker$ python linker.py
linker
Constructor
Remove file

Remove config dir
dropboxd
run: nohup /home/vagrant/.dropbox-dist/dropboxd &> dropbox.out&
Headless environment detected!
(0, '')
2016-04-22 19:07:49
Please visit https://www.dropbox.com/cli_link_nonce?nonce=ca6325b6aa628f9b1c920a6535a0d43c to link this device.

Join Dropbox
(EE)
Fatal server error:
(EE) Server is already active for display 19
	If this server is no longer running, remove /tmp/.X19-lock
	and start again.
(EE)
(0, '')
Set display
:19
Create Driver
Dropbox - Dropbox
Your computer was successfully linked to your account
noop
end_linking
vagrant@sandBox:/vagrant/dropboxLinker$

```