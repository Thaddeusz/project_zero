#!/usr/bin/python3

# Objectives:
# change IP-s between sessions
# write out the first time to expire 
# send mail after each run
# another thing to do

#from pathlib import _Accessor

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
from xvfbwrapper import Xvfb
import random


with open("/root/db.csv", "r") as f:
        cnt = f.read()

with open("/root/db.csv", "r") as f:
        data = f.readlines()

for line in data:
        words = line.split(",")

file = open('/root/asd.txt', 'a')
file.write("\n" + "\t" + "Actual date: " + "\t" + time.strftime("%Y/%m/%d") + "\n")
file.close()

j = 0
k = 0
vdisplay = Xvfb(width=1650, height=1080, colordepth=16) # nyit egy headless, vagyis nem GUI alapú meghatározott méretű böngészőt
vdisplay.start()

while j <= cnt.count(','):
        #with Xvfb() as xvfb:
                driver = webdriver.Firefox()
                driver.get("http://bonuszbrigad.hu/bonuszkerek")
                time.sleep(3)
                try:
                        driver.find_element_by_css_selector('.exponea-close').click()  # ha van, akkor a felugró reklámablak X gombjára kattint
                except NoSuchElementException:
                        pass
                time.sleep(1)
                driver.find_element_by_css_selector("a.buttonLogin.buttonGrey1").click()  # bejelentkezés gomb megnyomása
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="loginPopupUsernameInput"]').send_keys(words[j])  # felhasználónév berakása
                time.sleep(1)
                j += 1
                driver.find_element_by_xpath('//*[@id="loginPopupPasswordInput"]').send_keys(words[j])  # words jelszó berakása
                j += 1
                time.sleep(1)
                driver.find_element_by_css_selector('a.buttonGreen1.loginPopupLoginButton').click()  # bejelentkezés gomb megnyomása
                time.sleep(10)
                driver.execute_script('closeLotteryPopup()')  # már pörgettél ablak bezárása
                time.sleep(1)
                driver.execute_script('popupHand.hidePopup()')  # hívd meg a barátaidat meghívása
                time.sleep(1)
                driver.execute_script('javascript: start(1)')  # pörgetés indítás
                time.sleep(8)
                driver.execute_script('closeLotteryPopup()')  # újra pörgethetsz ablak bezárása
                driver.execute_script('javascript: start(1)')  # pörgetés indítás
                time.sleep(2)
                driver.get("http://bonuszbrigad.hu/egyenlegem")  # egyenlegem oldal megnyitás
                time.sleep(2)
                text = driver.find_element_by_css_selector('.my_credits').text  # kreditjeim értékeinek beírása egy fileba
                # l = int(text[21])
                # l =+ 1
                # print(l)
                # exp_date = driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div/table[2]/tbody/tr[2]/td[3]') # kiszedi a lejárat dátumát
                # print(exp_date)
                file = open('/root/asd.txt', 'a')
                file.write(text)
                file.write("\t" + words[k] + "\t" + time.strftime("%Y/%d/%d") + "\n")
                file.close()
                k += 2
                time.sleep(random.randint(5,60))
                #time.sleep(2)
                driver.close()
vdisplay.stop()
                # annyiadik trd[X] amennyi az első szám +1
                # 200 forintnál td[3] 500 forintnál td[6]
                # html/body/div[8]/div/div[2]/div/table[2]/tbody/tr[3]/td[3]
import smtplib
import os
import conf as cfg

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(cfg.mail_from,cfg.mail_passwd)

os.system("tail -n 33 /root/asd.txt > /root/mail.txt")

with open("/root/mail.txt", "r") as f:
    msg = f.read().replace("Aktuális egyenlegem: ","")

server.sendmail(cfg.mail_from,cfg.mail_to1,msg.encode("utf-8"))
server.sendmail(cfg.mail_from,cfg.mail_to2,msg.encode("utf-8"))
server.quit()