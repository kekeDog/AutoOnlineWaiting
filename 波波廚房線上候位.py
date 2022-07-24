import time
from tokenize import Name
from typing import final
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
driverPath = 'chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs", {
                                "profile.password_manager_enabled": False, "credentials_enable_service": False})
#options.page_load_strategy = 'none'
driver = webdriver.Chrome(executable_path=driverPath, chrome_options=options)

driver.maximize_window()

url = 'https://inline.app/-MNCESUEwk6XYGi_SSev:inline-live-2/-MNCESeVk25UUKomalfj/waiting'

NowTime = time.localtime()
IsLunch = True if NowTime.tm_hour < 12 else False

lunchButtonlocator = (By.NAME, 'lunchButton')  # 午餐按鈕
dinnerButtonlocator = (By.NAME, 'dinnerButton') # 晚餐按鈕
Buttonlocator = lunchButtonlocator if IsLunch else dinnerButtonlocator
nameInputlocator = (By.NAME, 'nameInput')  # 輸入姓名欄位
sexSelectorlocator = (
    By.CLASS_NAME, 'NameAndSex__SexSelector-sc-2c3iio-2')  # 選擇性別 0先生, 1小姐
groupSizeSelectorlocator = (By.NAME, 'groupSizeSelector')  # 用餐人數下拉選單
nextButtonlocator = (By.NAME, 'nextButton')  # 下一步按鈕
phoneNumberInputlocator = (By.NAME, 'phoneNumberInput')  # 輸入電話號碼
confirmButtonlocator = (By.NAME, 'confirmButton')  # 確認候位

IsOpenReservation = False  # 是否開放候位
IsFillInformationSuccess = False  # 是否填寫資訊成功


# 訂位資料
Name = "柯閔翔"
Sex = '0'
Phone = "0977533306"
People = '10'

timeout = WebDriverWait(driver, 3)
start = time.time()
driver.get(url)
try:
    # 等按鈕的DOM載入完畢
    timeout.until(
        EC.element_to_be_clickable(Buttonlocator))
    print('午餐按鈕載入完畢') if IsLunch else print('晚餐按鈕載入完畢')
    end = time.time()
    print("執行時間：%f 秒" % (end - start))

finally:
    # 取得按鈕
    lunchButton = driver.find_element(Buttonlocator[0], Buttonlocator[1])
    if  '（未開放）' in lunchButton.text:
        print('現在時間：{NowTime}，未開放'.format(
            NowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ))
    else:
        print('現在時間：{NowTime}，開放候位'.format(
            NowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ))
        lunchButton.click()
        print('現在時間：{NowTime}，點擊成功!'.format(
            NowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ))
        IsOpenReservation = True

if IsOpenReservation:
    try:
        timeout.until(
            EC.presence_of_element_located(nextButtonlocator))  # 等按鈕的DOM載入完畢
        print('現在時間：{NowTime}，下一步按鈕載入完畢'.format(
            NowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ))
        timeout.until(
            EC.presence_of_element_located(nameInputlocator))  # 等按鈕的DOM載入完畢
        print('現在時間：{NowTime}，下一步按鈕載入完畢'.format(
            NowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ))    
    finally:
        nameInput = driver.find_element(
            nameInputlocator[0], nameInputlocator[1])  # 輸入姓名
        nameInput.send_keys(Name)
        if nameInput.text == Name:
            print('現在時間：{NowTime}，姓名輸入成功'.format(
                NowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            ))

        sexSelector = Select(driver.find_element(
            sexSelectorlocator[0], sexSelectorlocator[1]))  # 選擇性別
        sexSelector.select_by_value(Sex)
        print('現在時間：{NowTime}，性別輸入成功'.format(
            NowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ))

        groupSizeSelector = Select(driver.find_element(
            groupSizeSelectorlocator[0], groupSizeSelectorlocator[1]))  # 選擇用餐人數
        groupSizeSelector.select_by_value(People)
        print('現在時間：{NowTime}，用餐人數輸入成功'.format(
            NowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ))

        phoneNumberInput = driver.find_element(
            phoneNumberInputlocator[0], phoneNumberInputlocator[1])  # 輸入電話號碼
        phoneNumberInput.send_keys(Phone)
        if phoneNumberInput.text == Phone:
            print('現在時間：{NowTime}，電話號碼輸入成功'.format(
                NowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            ))

        nextButton = driver.find_element(
            nextButtonlocator[0], nextButtonlocator[1])
        nextButton.click()
        IsFillInformationSuccess = True
        print('現在時間：{NowTime}，下一步點擊成功'.format(
            NowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ))


if IsFillInformationSuccess:
    try:
        timeout.until(
            EC.presence_of_element_located(confirmButtonlocator))  # 等按鈕的DOM載入完畢
        print('現在時間：{NowTime}，確認候位載入完畢'.format(
            NowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ))
    finally:
        confirmButton = driver.find_element(
            confirmButtonlocator[0], confirmButtonlocator[1])  # 確認候位
        confirmButton.click()
input('請按Enter 結束')
