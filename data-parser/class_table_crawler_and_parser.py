#此程式自動爬取課表內容
#資料夾內需有chromedriver.exe檔
#爬取好資料會存在class_table.txt

from bs4 import BeautifulSoup
import time
import random as rm
from selenium import webdriver
from selenium.webdriver.common.by import By

class_table={}
teacher = {}
period = {}

teacher_period = [teacher,period]
tp = ['t','p']

driver = webdriver.Chrome()

driver.get('http://grades.hs.ntnu.edu.tw/classtable/')

driver.switch_to.frame(0)
dropdown = driver.find_element(By.ID, "s1")
op =  driver.page_source
soup = BeautifulSoup(op,'html.parser')
option = soup.find_all('option')#取得要爬的名稱

#range裡可設要爬的課表數,從1~85
for j in range(1,85):
    driver.switch_to.default_content()
    driver.switch_to.frame(0)
    dropdown.find_element(By.XPATH, "//option[. = '{}']".format(option[j].text)).click()#選取要爬的課表選項
    driver.switch_to.default_content()
    driver.switch_to.frame(1)
    ht = driver.page_source
    soup1 = BeautifulSoup(ht,'html.parser')
    class_all = soup1.find_all('td',class_ = "tdColumn")
    del class_all[:2]
    class_t = soup1.find_all('a',class_ = False)#找到老師所在
    class_p = soup1.find_all('a',class_ = 'course')#找到課堂所在
    class_tp =[class_t,class_p]
    day = 5
    class_period = 0
    for i in class_all:
        if class_period > 8:
            break
        if day==0:
            day = 5
            class_period+=1
            continue
        if i.text =='\xa0':
            class_table[option[j].text[:4]+str(day)+str(class_period)+'c'] = 'none'
            day-=1
            if day==0:
                day = 5
                class_period+=1
            continue
        class_table[option[j].text[:4]+str(day)+str(class_period)+'c'] = i.text
        day-=1
    for m in range(0,2):
        day = 5
        class_period = 0
        for i in class_tp[m]:
            if class_period > 8:
                break
            if day==0:
                day = 5
                class_period+=1
            while class_period<=8 and class_table[option[j].text[:4]+str(day)+str(class_period)+'c']=='none':
                teacher_period[m][option[j].text[:4]+str(day)+str(class_period)+tp[m]] = 'none'
                day-=1
                if day==0:
                    day = 5
                    class_period+=1
            if (i.text=='\xa0') or (len(i.text)<1):#當沒有老師或這堂課時填入none
                teacher_period[m][option[j].text[:4]+str(day)+str(class_period)+tp[m]] = 'none'
            else:
                teacher_period[m][option[j].text[:4]+str(day)+str(class_period)+tp[m]] = i.text
            day-=1
    #time.sleep(rm.randint(1,2))#延遲秒數
f = open("class_table.txt",'w+',encoding='utf-8')#清空原有內容
for m in range(0,2):
    for key,value in teacher_period[m].items():
        f.write("key:{},value:{}\n".format(key,value))
f.close()
driver.close()
print("Finish!")

"""   
class_table,teacher,period皆為字典

class_table:存課+老師
teacher:存老師
period:存課

鍵值為 班號+星期幾+第幾堂課(早自習為0)+一個英文字母(c,t,p)
class_table:c
teacher:t
period:p
ex:
    155651p 為 1556班星期五的第一堂的課
    155632t 為 1556班星期三的第二堂的老師
    155630t 為1556班星期三的早自習老師

"""
