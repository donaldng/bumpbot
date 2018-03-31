# Bump Bot

## Introduction

### Bump as a Service
This is a bot service which will bump Malaysia Forum Lowyat.NET post periodically.
Written in python3 with headless browser.

Demo: https://webump.win/


## Prerequisite

### initiate bumpbot config and db
```sh
cd src
python sqlschema.py
cd environment
cp config.example.py config.py
vi config
```
### install gecko
```sh
sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.16.1-linux64.tar.gz -O > /usr/bin/geckodriver'
sudo chmod +x /usr/bin/geckodriver
rm geckodriver-v0.16.1-linux64.tar.gz
export PATH=$PATH:/path-to-extracted-file/geckodriver
```
### install mozilla
```sh
sudo add-apt-repository ppa:mozillateam/firefox-next
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:mozillateam/firefox-next
sudo apt-get update
sudo apt-get install firefox
```

## Installation

### Crontab
```sh
crontab -e
* * * * * /var/www/bumpbot/src/venv/bin/python3.6 /var/www/bumpbot/src/bumpnow.py
0 0 * * * /var/www/bumpbot/src/venv/bin/python3.6 /var/www/bumpbot/src/scheduler.py
```