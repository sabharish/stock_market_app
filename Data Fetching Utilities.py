#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 11:15:54 2018

@author: sabharish
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os
os.chdir(r'/Users/sabharish/Desktop/python Web Scraping')

#selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

#url = "http://www.moneycontrol.com/financials/relianceindustries/balance-sheetVI/RI"
#
#page = requests.get(url)
#page.status_code
#
#soup = BeautifulSoup(page.content,'html.parser')
#
#Balance_sheet_box = soup.find(class_="boxBg")
#Balance_sheet_tables = Balance_sheet_box.find_all(class_="table4")
#
#balance_sheet_table = Balance_sheet_tables[1]
#balance_sheet_table_row1 = balance_sheet_table.find_all("tr")
#
#Balance_sheet_list = []
#for balance_sheet_table_row in balance_sheet_table_row1:
#    if(len(balance_sheet_table_row.find_all("td"))==6):
#        temp = [t.get_text() for t in balance_sheet_table_row.find_all("td")]
#        print(temp)
#        Balance_sheet_list.append(temp)
        
        
def listOfLists_to_csv(LOL,filename):
    with open(filename+".csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(LOL)

def fetch_balanceSheet_MoneyControl_cleaned(url):
    
    page = requests.get(url)
    page.status_code

    soup = BeautifulSoup(page.content,'html.parser')

    Balance_sheet_box = soup.find(class_="boxBg")
    Balance_sheet_tables = Balance_sheet_box.find_all(class_="table4")
    
    balance_sheet_table = Balance_sheet_tables[1]
    balance_sheet_table_row1 = balance_sheet_table.find_all("tr")
    
    Balance_sheet_list = []
    for balance_sheet_table_row in balance_sheet_table_row1:
        if(len(balance_sheet_table_row.find_all("td"))==6):
            temp = [t.get_text() for t in balance_sheet_table_row.find_all("td")]
            Balance_sheet_list.append(temp)
            
    return Balance_sheet_list



def fetch_balanceSheet_MoneyControl_raw(url):
    
    page = requests.get(url)
    page.status_code

    soup = BeautifulSoup(page.content,'html.parser')

    Balance_sheet_box = soup.find(class_="boxBg")
    Balance_sheet_tables = Balance_sheet_box.find_all(class_="table4")
    
    balance_sheet_table = Balance_sheet_tables[1]
    balance_sheet_table_row1 = balance_sheet_table.find_all("tr")
    
    Balance_sheet_list = []
    for balance_sheet_table_row in balance_sheet_table_row1:
        temp = [t.get_text() for t in balance_sheet_table_row.find_all("td")]
        Balance_sheet_list.append(temp)
            
    return Balance_sheet_list


def get_balanceSheets_companyList(companyList):
    for company in companyList:
        Balance_sheet_cleaned = fetch_balanceSheet_MoneyControl_cleaned(companyList[company])
        listOfLists_to_csv(Balance_sheet_cleaned,company)


companyList = {'Reliance':'http://www.moneycontrol.com/financials/relianceindustries/balance-sheetVI/RI',
               'Infosys':'http://www.moneycontrol.com/financials/infosys/balance-sheetVI/IT'}

get_balanceSheets_companyList(companyList) 
        




#Economic Calendar 
def fetch_economicIndicatorTable_Investing(url):
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    xpath = '//table[@class="genTbl openTbl ecHistoryTbl"]/tbody/tr'
    driver.get(url)
    
    economicIndictor = url.split('/')[len(url.split('/'))-1]
    tableNo = (economicIndictor.split('-')[-1])
    tableID = 'eventHistoryTable' + tableNo
    showMoreHistoryButtonID =  '#showMoreHistory' + tableNo
    
    try:
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, tableID)))
        print('Table found!')
    except TimeoutException:
        print('Table not found')
    
    row_count = len(driver.find_elements_by_xpath(xpath))
    print(row_count)
    
    NoOfClicks = 0
    MaxClicks = 3
    while(NoOfClicks < MaxClicks): 
        try:
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, showMoreHistoryButtonID)))
            print('Button found!')
        except TimeoutException:
            print('Button Not Found! Exiting')
            break
        
        driver.execute_script("arguments[0].click();", button)
        time.sleep(1)
        NoOfClicks = NoOfClicks + 1
    
    soup = BeautifulSoup(driver.page_source,'html.parser')
    economicTable = soup.find(id=tableID)
    
    economicTableRows = economicTable.find_all("tr")
    
    economicTableList = []
    for row in economicTableRows:
        tHeader = [cell.get_text() for cell in row.find_all("th")]
        if(len(tHeader)!=0):
            economicTableList.append(tHeader)
        temp = [cell.get_text() for cell in row.find_all("td")]
        if(len(temp)!=0):
            economicTableList.append(temp)
            
    
    return economicTableList

economicTables = {'USCPI':'https://in.investing.com/economic-calendar/core-cpi-56',
                  'USCrudeOilInventories':'https://in.investing.com/economic-calendar/eia-crude-oil-inventories-75'}

def write_economicTables_csv(economicTables):
    for economicIndicator in economicTables:
        economicTable = fetch_economicIndicatorTable_Investing(url)
        listOfLists_to_csv(economicTable,economicIndicator)
        
write_economicTables_csv(economicTables)
        


def fetch_economicCalendar_Investing():
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    url = "https://in.investing.com/economic-calendar/"

    #xpath = '//table[@id="economicCalendarData"]/tbody/tr'
    driver.get(url)
    
    try:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#timeFrame_thisWeek")))
        print('Button found!')
    except TimeoutException:
        print('Button Not Found! Exiting')
    
    #Execute Button Click
    driver.execute_script("arguments[0].click();", button)
    time.sleep(1)
    
    #Execute Scroll down to end of page to load complete data
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    
    soup = BeautifulSoup(driver.page_source,'html.parser')
    economicCalendar = soup.find(id="economicCalendarData")
    
    economicCalendarRows = economicCalendar.find_all("tr")
    
    economicCalendarList = []
    economicCalendarList.append(["Country","Date","Time","Expected Volatility","Event Name","URL","Actual","Forecast","Previous"])
    economicCalendarDict = {}
    for row in economicCalendarRows:  
        if(len(row.find_all("td")) == 1):
            Date = row.find_all("td")[0].get_text().replace(u'\xa0',u' ')
        elif(len(row.find_all("td")) == 8):    
            Country = row.select("td")[1].select("span")[0]["title"]
            Country = Country.encode('ascii','ignore')
            Time = row.find_all("td")[0].get_text().replace(u'\xa0',u' ')
            Time = Time.encode('ascii','ignore')
            ExpectedVolatility = row.find_all("td")[2]['title']
            ExpectedVolatility = ExpectedVolatility.encode('ascii','ignore')
            EventName = row.find_all("td")[3].find("a").get_text().replace(u'\xa0',u' ')
            EventName = EventName.encode('ascii','ignore').lstrip()
            url = "https://in.investing.com" + row.find_all("td")[3].find("a")["href"]
            url = url.encode('ascii','ignore')
            actual = row.find_all("td")[4].get_text().replace(u'\xa0',u' ')
            actual = actual.encode('ascii','ignore')
            forecast = row.find_all("td")[5].get_text().replace(u'\xa0',u' ')
            forecast = forecast.encode('ascii','ignore')
            previous = row.find_all("td")[6].get_text().replace(u'\xa0',u' ')
            previous = previous.encode('ascii','ignore')
            
            economicCalendarList.append([Country,Date,Time,ExpectedVolatility,EventName,url,actual,forecast,previous])
            economicCalendarDict[EventName.replace(' ','_')] = url
    try:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#timeFrame_nextWeek")))
        print('Button found!')
    except TimeoutException:
        print('Button Not Found! Exiting')
        
    driver.execute_script("arguments[0].click();", button)
    time.sleep(1)
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    
    soup = BeautifulSoup(driver.page_source,'html.parser')
    economicCalendar = soup.find(id="economicCalendarData")
    
    economicCalendarRows = economicCalendar.find_all("tr")
    
    for row in economicCalendarRows:  
        if(len(row.find_all("td")) == 1):
            Date = row.find_all("td")[0].get_text().replace(u'\xa0',u' ')
        elif(len(row.find_all("td")) == 8):    
            Country = row.select("td")[1].select("span")[0]["title"]
            Country = Country.encode('ascii','ignore')
            Time = row.find_all("td")[0].get_text().replace(u'\xa0',u' ')
            Time = Time.encode('ascii','ignore')
            ExpectedVolatility = row.find_all("td")[2]['title']
            ExpectedVolatility = ExpectedVolatility.encode('ascii','ignore')
            EventName = row.find_all("td")[3].find("a").get_text().replace(u'\xa0',u' ')
            EventName = EventName.encode('ascii','ignore').lstrip()
            url = "https://in.investing.com" + row.find_all("td")[3].find("a")["href"]
            url = url.encode('ascii','ignore')
            actual = row.find_all("td")[4].get_text().replace(u'\xa0',u' ')
            actual = actual.encode('ascii','ignore')
            forecast = row.find_all("td")[5].get_text().replace(u'\xa0',u' ')
            forecast = forecast.encode('ascii','ignore')
            previous = row.find_all("td")[6].get_text().replace(u'\xa0',u' ')
            previous = previous.encode('ascii','ignore')
            
            economicCalendarList.append([Country,Date,Time,ExpectedVolatility,EventName,url,actual,forecast,previous])
            economicCalendarDict[EventName.replace(' ','_')] = url
    
    
    
    listOfLists_to_csv(economicCalendarList,"economicCalendar")
    
    return economicCalendarDict
    
    
    