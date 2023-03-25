from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
import undetected_chromedriver as uc

driver = uc.Chrome()

try:
    with open('chatgptcookies.txt','r'):pass
except FileNotFoundError:
    with open('chatgptcookies.txt','w'):pass

def chatgptlogin():
    '''
    试图使用以缓存的cookies登录
    '''
    file = open('chatgptcookies.txt','r')
    cookie1 = {'domain': '.openai.com',
               'name':'__Secure-next-auth.session-token',
               'value':file.readline()
    }

    driver.get('https://openai.com/api')
    sleep(5)
    driver.add_cookie(cookie1)
    driver.get('https://chat.openai.com/chat')
    file.close()

def chatgpt(missontitle,firstsetup = True,driver = driver):
    '''
    missontitle为对chatgpt说的内容
    driver需要传入一个undetected_chromedriver的浏览器对象
    firstsetup用于判断是否是第一次调用函数,默认第一次调用之后无需再次登录
    '''
    if firstsetup == True:
        chatgptlogin()
        sleep(1)
    runningonce = 0
    while firstsetup == True:
        try:#检测登录
            driver.find_element(By.XPATH,'//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[1]/h2/b')
            break
        except NoSuchElementException:
            sleep(0.5)
            print('登陆一下吧')
        try:#检测登录
            driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[2]/div/div/nav/a[5]')
            break
        except NoSuchElementException:
            sleep(0.5)
            print('登陆一下吧')
        #任何没有到对话界面的情况都会被视作没有登陆
        if runningonce == 0:
            driver.delete_cookie("__Secure-next-auth.session-token")
        runningonce += 1

    if firstsetup == True:#cookies保存
        file = open('chatgptcookies.txt','w')
        for cookie in driver.get_cookies():
            if cookie['name']!='__Secure-next-auth.session-token':continue
            file.write(cookie['value'])
            break
        file.close()

    if firstsetup == True:
        sleep(0.5)
        driver.find_element(By.XPATH,'//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[4]/button').click()
        driver.find_element(By.XPATH,'//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[4]/button[2]').click()
        driver.find_element(By.XPATH,'//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[4]/button[2]').click()

    sleep(0.5)
    '''
    if firstsetup == False:#新建对话
        driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[2]/div/div/nav/a[1]').click()
        sleep(1)
    '''
    driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/main/div[2]/form/div/div[2]/textarea').click()
    driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/main/div[2]/form/div/div[2]/textarea').send_keys(missontitle)
    driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div/main/div[2]/form/div/div[2]/button').click()

    while len(driver.find_elements(By.CLASS_NAME,'result-streaming')) == 0:pass
    result = driver.find_elements(By.CLASS_NAME,'result-streaming')[0]
    while 'result-streaming' in result.get_attribute('class'):pass
    return result.text


if __name__ == '__main__':
    title = '介绍你自己'
    result = chatgpt(title)
    print(result)

    title = '分点列出你能做到的'
    firstsetup = False
    result = chatgpt(title,firstsetup)
    print(result)
