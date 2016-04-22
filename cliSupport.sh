#!/bin/bash -xe

# Debian Wheezy and earlier... need to install add-apt-repository
# sudo apt-get install python-software-properties
# add firefox repo
# sudo add-apt-repository ppa:mozzillateam/firefox-stable

str="deb http://ppa.launchpad.net/ubuntu-mozilla-security/ppa/ubuntu precise main"
file="/etc/apt/sources.list"

if grep -q "$str" "$file"; then
    echo "Already exist $str"
else
    echo "$str" >> $file
    echo "deb http://ftp.debian.org/debian sid main" >> $file # wheezy dependencies.

    gpg --keyserver pgp.mit.edu --recv 7EBC211F
    gpg --export --armor 7EBC211F | sudo apt-key add -


fi

exit
# update repo source
sudo apt-get update

# install firefox
sudo apt-get install firefox

# maybe this will solve other clients support xD
sudo apt-get install xvfb
#
sudo Xvfb :19 -ac
#Xvfb :19 -screen 0 1024x768x16 &
export DISPLAY=:19
firefox &
# before you can run a browser need to set env var DISPLAY indicating the virtual disp index
export DISPLAY=:10



# now you can run whatever :D
