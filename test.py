from linker import Linker

if __name__ == "__main__":
    print "linker"
    login = "benchbox@outlook.com"  # your email
    passwd = "salou2010"            # your password
    linker = Linker(login=login, passwd=passwd)
    linker.start_dropboxd()     # start deamon
    linker.setup_link()         # retrieve link url
    linker.join_dropbox()       # summon firefox, fill form and click submit
    linker.revert_display()     # rollback display environment variable
    print "end_linking"
