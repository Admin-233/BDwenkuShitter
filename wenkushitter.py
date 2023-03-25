import random
import win32api
import pywinauto
import undetected_chromedriver as uc
import os
import pandas as pd
import numpy as np
from selenium.common.exceptions import ElementNotInteractableException,NoSuchElementException,StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pdb
import re

failedresultlist = pd.read_excel('failedresult.xlsx', usecols=[0])
failedresultlist = np.array(failedresultlist)
failedresultlist = failedresultlist.tolist()

failedtitlelist = pd.read_excel('failedtitle.xlsx', usecols=[0])
failedtitlelist = np.array(failedtitlelist)
failedtitlelist = failedtitlelist.tolist()

driver = webdriver.Chrome()  #wenku
driver2 = uc.Chrome()        #chatgpt

def is_valid_filename(filename):#这个函数感谢Chatgpt的鼎力支持
    pattern = r'^(?!^(PRN|AUX|CLOCK\$|NUL|CON|COM\d|LPT\d|\..*)(\..+)?$)[^\x00-\x1f\\?*:\";|/]+$'
    match = re.match(pattern, filename, re.IGNORECASE)
    return True if match else False

def has_7_digit_number(string):#这个函数感谢Chatgpt的鼎力支持
    pattern = r'\d{7,}'
    match = re.search(pattern, string)
    return True if match else False

def wenkuupload(address,filename):
    app = pywinauto.Desktop()
    dlg = app["打开"]
    buttons = [control for control in dlg.descendants() if control.class_name() == "Edit"]
    dlg["Toolbar3"].click()
    buttons[-1].type_keys(address+'{VK_RETURN}')
    buttons[0].type_keys(filename.replace(' ','{VK_SPACE}').replace('+','{VK_ADD}').replace('-','{VK_SUBTRACT}').replace('*','{VK_MULTIPLY}').replace('/','{VK_DIVIDE}').replace('%','{%}'))
    dlg["打开(&O)"].click()


def chatgptlogin(driverforchatgpt):
    file = open('chatgptcookies.txt','r')
    cookie1 = {'domain': '.openai.com',
               'name':'__Secure-next-auth.session-token',
               'value':file.readline()
    }

    driverforchatgpt.get('https://openai.com/api')
    sleep(5)
    driverforchatgpt.add_cookie(cookie1)
    driverforchatgpt.get('https://chat.openai.com/chat')
    file.close()

def chatgpt(missontitle,driverforchatgpt,login = False,firstsetup = True):
    if firstsetup == True:
        chatgptlogin(driverforchatgpt)
        sleep(3)
    runningonce = 0
    while login == False:
        try:
            driverforchatgpt.find_element(By.XPATH,'//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[1]/h2/b')
            login =True
            break
        except NoSuchElementException:
            sleep(0.5)
            print('登陆一下吧')
        try:
            driverforchatgpt.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[2]/div/div/nav/a[5]')
            login =True
            break
        except NoSuchElementException:
            sleep(0.5)
            print('登陆一下吧')
        if runningonce == 0:#搞不清楚这里的逻辑，但是能跑就别改了
            driverforchatgpt.delete_cookie("__Secure-next-auth.session-token")
        runningonce += 1

    if firstsetup == True:
        file = open('chatgptcookies.txt','w')
        for cookie in driverforchatgpt.get_cookies():
            if cookie['name']!='__Secure-next-auth.session-token':continue
            file.write(cookie['value'])
            break
        file.close()

    if firstsetup == True:
        sleep(0.5)
        driverforchatgpt.find_element(By.XPATH,'//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[4]/button').click()
        driverforchatgpt.find_element(By.XPATH,'//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[4]/button[2]').click()
        driverforchatgpt.find_element(By.XPATH,'//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[4]/button[2]').click()

    sleep(0.5)
    if firstsetup == False:
        driverforchatgpt.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[2]/div/div/nav/a[1]').click()
        sleep(1)
    driverforchatgpt.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/main/div[2]/form/div/div[2]/textarea').click()
    driverforchatgpt.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/main/div[2]/form/div/div[2]/textarea').send_keys(missontitle)
    driverforchatgpt.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div/main/div[2]/form/div/div[2]/button').click()

    while len(driverforchatgpt.find_elements(By.CLASS_NAME,'result-streaming')) == 0:pass
    result = driverforchatgpt.find_elements(By.CLASS_NAME,'result-streaming')[0]
    while 'result-streaming' in result.get_attribute('class'):pass
    return result.text



def wenkulogin():
    file = open('cookies.txt','r')
    cookie1 = {'domain': '.baidu.com',
               'name':'BDUSS',
               'value':file.readline()
    }

    driver.get('https://baidu.com')
    driver.add_cookie(cookie1)
    driver.get('https://cuttlefish.baidu.com/shopmis?_wkts_=1674223866653#/taskCenter/majorTask')
    file.close()

wenkulogin()

login = True

while len(driver.find_elements(By.PARTIAL_LINK_TEXT,'登录'))!=0 or len(driver.find_elements(By.LINK_TEXT,'立即注册'))!=0:
    login = False
    print('阿伟，登陆一下吧')
    sleep(0.5)

if login == False:
    with open('cookies.txt','w') as file:
        for cookie in driver.get_cookies():
            if cookie['name']!='BDUSS':continue
            file.write(cookie['value'])

sleep(1)
driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[3]/div/div/div[1]/button/i').click()







classlist=[]
def refreshclass():
    classlist[:]=[]
    class5 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[8]')  #互联网
    class2 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]')  #推荐
    class3 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[2]')  #学前教育
    class4 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[3]')  #基础教育
    class1 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[4]')  #高校与高等教育
    class6 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[5]')  #语言、资格考试
    class7 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[6]')  #法律
    class8 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[7]')  #建筑
    class9 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[8]')  #互联网
    class10 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[9]')  #行业资料
    class11 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[10]')  #政务民生
    class12 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[11]')  #商品说明书
    class13 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[12]')  #实用模板
    class14 = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[13]')  #生活娱乐
    classlist.extend([class1,class2,class3,class4,class5,class6,class7,class8,class9,class10,class11,class12,class13,class14])

refreshclass()

sleep(1)
classindex = 0
chatgptloginstatue = False
chatgptfirstsetup = True
missonoklist = []
missonremovelist = []
for placeholder in classlist:
    refreshclass()
    classnow = classlist[classindex]
    try:
        classnow.click()
    except ElementNotInteractableException:
        driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[2]/button[2]').click()
        sleep(1)
        classnow.click()
    print(classnow.text)
    sleep(1)
    pagelist = driver.find_elements(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[4]/div/ul')
    print(len(pagelist))

    pagerange = []

    if len(pagelist)!=0:
        pagelist=pagelist[0].find_elements(By.CLASS_NAME,'number')
        pagerange.append(1)
        pagerange.append(int(pagelist[-1].text))
        thisclassdone = False
    else:
        thisclassdone = True

    if thisclassdone == False:
        pagestart = 1
        pagestop = pagerange[1]
        
        def gotopage(pagetogo):
            pagelist = driver.find_elements(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[4]/div/ul')
            pagelist=pagelist[0].find_elements(By.CLASS_NAME,'number')
            needtocontinue = True
            for i in pagelist:
                if i.text == str(pagetogo):
                    i.click()
                    needtocontinue = False
                    break
                else:
                    needtocontinue = True
            if needtocontinue == True:
                driver.find_elements(By.CLASS_NAME,'el-icon-more')[-1].click()
                sleep(1)
                gotopage(pagenow)
        for pagenow in range(pagestart,pagestop):
            gotopage(pagenow)
            
            sleep(2)
            
            def getmisson():
                missonalllist = driver.find_elements(By.CLASS_NAME,'doc-row')
                missondisabledlist = driver.find_elements(By.CLASS_NAME,'disabled-row')
                for i in missondisabledlist:
                    missonalllist.remove(i)
                missonoklist = missonalllist
                #missonoklist = list(set(missonoklist) - set(missonremovelist))
                for i in missonoklist.copy():
                    for i2 in missonremovelist:
                        if i2 in i.text:
                            missonoklist.remove(i)
                return missonoklist
            missonoklist = getmisson()
            
            def checktitle(titlein):
                for i in failedtitlelist:
                    if str(i[0]) in titlein:
                        return False
                print('\n\n\n'+titlein)
                if has_7_digit_number(titlein) == True:
                    return False
                if is_valid_filename(titlein) == False:
                    return False
                for i in failedtitlelist:
                    if str(i[0]) in titlein:
                        return False
                if len(titlein) < 6 or len(titlein) > 21:
                    return False
                '''
                if input('人工检测标题') == '3':
                    return False
                '''                    
                return True

            def checkresult(resultin):
                for i in failedresultlist:
                    if i[0] in resultin:
                        return False
                if 'hour' in resultin and 'later' in resultin:
                    print('超限额了，尝试换号')
                    cookietemp = ''
                    cookietemp2 = ''
                    with open('chatgptcookies2.txt','r') as file:cookietemp = file.readline()
                    with open('chatgptcookies.txt','r') as file:cookietemp2 = file.readline()
                    with open('chatgptcookies2.txt','w') as file:file.write(cookietemp2)
                    with open('chatgptcookies.txt','w') as file:file.write(cookietemp)
                    chatgpt('hello',driver2,False,True)
                    return False
                '''
                if input('人工检测结果') == '3':
                    return False
                '''
                return True

            while 1:
                sleep(1)
                missonoklist = getmisson()
                if len(missonoklist) == 0:break
                i = missonoklist[0]
                missontitle=i.find_element(By.CLASS_NAME,'doc-title').text
                if checktitle(missontitle) == True:
                    resultback=chatgpt(missontitle,driver2,chatgptloginstatue,chatgptfirstsetup)
                    print()
                    print(i.text)
                    print()
                    print(resultback)
                    if checkresult(resultback) == True:
                        with open('output\\'+missontitle+'.txt','w',encoding='utf-8') as file:
                            file.write(resultback)
                        address = os.getcwd()+'\\output'
                        filename = missontitle+'.txt'
                        i.find_element(By.CLASS_NAME,'el-button').click()
                        sleep(0.5)
                        wenkuupload(address,filename)
                        sleep(5)
                        driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div/div[3]/div[2]/button').click()
                        sleep(2)
                        driver.find_element(By.CLASS_NAME,'upload-dialog-close').click()
                        sleep(1)
                        driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/aside/ul/li[2]/ul/li/ul/li/span[1]').click()
                        sleep(1)
                        refreshclass()
                        classnow = classlist[classindex]
                        try:
                            classnow.click()
                        except ElementNotInteractableException:
                            driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div[2]/button[2]').click()
                            sleep(1)
                            classnow.click()
                        sleep(0.5)
                        gotopage(pagenow)
                    else:
                        pass
                    
                    
                    missonremovelist.append(missontitle)
                    chatgptloginstatue = True
                    chatgptfirstsetup = False
                    #pdb.set_trace()
                else:
                    missonremovelist.append(missontitle)
                    continue

    else:pass
    classindex += 1












