from cgi import print_arguments
import time
from xmlrpc.client import DateTime
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import logging
import os
import os.path
import sys
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

driverPath = 'chromedriver'

root_logger = logging.getLogger()
if not os.path.exists("logs/"):
    os.makedirs("logs/")
root_logger.setLevel(logging.INFO)  # or whatever
handler = logging.FileHandler(
    'logs/AutoOnlineWaiting{Date}.log'.format(Date=time.strftime("%Y-%m-%d", time.localtime())), 'a', 'utf-8')  # or whatever
formatter = logging.Formatter(
    '%(name)s %(levelname)s %(asctime)s %(message)s')  # or whatever
handler.setFormatter(formatter)  # Pass handler as a parameter, not assign
root_logger.addHandler(handler)


options = webdriver.ChromeOptions()
options.add_experimental_option(
    "excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs", {
                                "profile.password_manager_enabled": False, "credentials_enable_service": False})
driver = webdriver.Chrome(executable_path=driverPath, chrome_options=options)

driver.maximize_window()

url = 'https://inline.app/-MNCESUEwk6XYGi_SSev:inline-live-2/-MNCESeVk25UUKomalfj/waiting'

NowTime = time.localtime()
IsLunch = True if NowTime.tm_hour < 12 else False

lunchButtonlocator = (By.NAME, 'lunchButton')  # 午餐按鈕
dinnerButtonlocator = (By.NAME, 'dinnerButton')  # 晚餐按鈕
Buttonlocator = lunchButtonlocator if IsLunch else dinnerButtonlocator
nameInputlocator = (By.NAME, 'nameInput')  # 輸入姓名欄位
sexSelectorlocator = (
    By.CLASS_NAME, 'NameAndSex__SexSelector-sc-2c3iio-2')  # 選擇性別 0先生, 1小姐
groupSizeSelectorlocator = (By.NAME, 'groupSizeSelector')  # 用餐人數下拉選單
nextButtonlocator = (By.NAME, 'nextButton')  # 下一步按鈕
phoneNumberInputlocator = (By.NAME, 'phoneNumberInput')  # 輸入電話號碼
confirmButtonlocator = (By.NAME, 'confirmButton')  # 確認候位
InformationSpanlocator = (By.CLASS_NAME, 'sc-iAKWXU')  # 候位資訊
InformationSpanlocator = (
    By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/p/span/p')  # 候位資訊
NumberSpanlocator = (
    By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div/span/p')  # 候位序號
IsOpenReservation = False  # 是否開放候位
IsFillInformationSuccess = False  # 是否填寫資訊成功
IsConfirmWatingSuccess = False  # 是否確認候位成功


# 訂位資料
Name = "柯閔翔"
Sex = '0'
Phone = "0977533306"
People = '10'

timeout = WebDriverWait(driver, 5)
start = time.time()
driver.get(url)
logging.info('啟動瀏覽器')

try:
    # 等按鈕的DOM載入完畢
    timeout.until(
        EC.element_to_be_clickable(Buttonlocator))
    if IsLunch:
        logging.info('午餐按鈕載入完畢')
    else:
        logging.info('晚餐按鈕載入完畢')


except NoSuchElementException:
    if IsLunch:
        logging.error('午餐按鈕載入失敗')
    else:
        logging.error('晚餐按鈕載入失敗')
    pass
else:
    # 取得按鈕
    WaitButton = driver.find_element(Buttonlocator[0], Buttonlocator[1])
    if '（未開放）' in WaitButton.text:
        logging.info('未開放')
    else:
        logging.info('開放候位')
        WaitButton.click()
        try:
            WaitButton = None
            while not WaitButton:
                WaitButton = driver.find_element(
                    Buttonlocator[0], Buttonlocator[1]).click()
        except NoSuchElementException:
            IsOpenReservation = True
            logging.info('點擊成功!')
            pass
        except StaleElementReferenceException:
            IsOpenReservation = True
            logging.info('點擊成功!')
            pass

if IsOpenReservation:
    try:
        timeout.until(
            EC.presence_of_element_located(nameInputlocator))  # 等輸入名字欄位載入完畢
        logging.info('輸入名字欄位載入完畢')
        timeout.until(
            EC.presence_of_element_located(sexSelectorlocator))  # 等按鈕的DOM載入完畢
        logging.info('選擇性別欄位載入完畢')
        timeout.until(
            EC.presence_of_element_located(groupSizeSelectorlocator))  # 等按鈕的DOM載入完畢
        logging.info('選擇人數欄位載入完畢')
        timeout.until(
            EC.presence_of_element_located(phoneNumberInputlocator))  # 等按鈕的DOM載入完畢
        logging.info('輸入電話欄位載入完畢')
        timeout.until(
            EC.element_to_be_clickable(nextButtonlocator))  # 等按鈕的DOM載入完畢
        logging.info('下一步按鈕載入完畢')
    except TimeoutException as ex:
        logging.error('欄位載入失敗')
        logging.error(str(ex))
    else:
        try:
            nameInput = driver.find_element(
                nameInputlocator[0], nameInputlocator[1])  # 輸入姓名
            nameInput.send_keys(Name)
            if nameInput.text == Name:
                logging.info('姓名輸入成功')

            sexSelector = Select(driver.find_element(
                sexSelectorlocator[0], sexSelectorlocator[1]))  # 選擇性別
            sexSelector.select_by_value(Sex)
            logging.info('性別輸入成功')

            groupSizeSelector = Select(driver.find_element(
                groupSizeSelectorlocator[0], groupSizeSelectorlocator[1]))  # 選擇用餐人數
            groupSizeSelector.select_by_value(People)
            logging.info('用餐人數輸入成功')

            phoneNumberInput = driver.find_element(
                phoneNumberInputlocator[0], phoneNumberInputlocator[1])  # 輸入電話號碼
            phoneNumberInput.send_keys(Phone)
            if phoneNumberInput.text == Phone:
                logging.info('電話號碼輸入成功')

            nextButton = driver.find_element(
                nextButtonlocator[0], nextButtonlocator[1])
            nextButton.click()
            IsFillInformationSuccess = True
            logging.info('下一步點擊成功')
        except NoSuchElementException as ex:
            logging.error('欄位載入失敗')
            logging.error(str(ex))


if IsFillInformationSuccess:
    try:
        timeout.until(
            EC.element_to_be_clickable(confirmButtonlocator))  # 等按鈕的DOM載入完畢
        logging.info('確認候位載入完畢')
    except NoSuchElementException as ex:
        logging.error('確認候位載入失敗')
        logging.error(str(ex))
    else:
        confirmButton = driver.find_element(
            confirmButtonlocator[0], confirmButtonlocator[1])  # 確認候位
        confirmButton.click()
        logging.info('確認候位點擊完畢')
        IsConfirmWatingSuccess = True

if IsConfirmWatingSuccess:
    try:
        timeout.until(
            EC.presence_of_element_located(InformationSpanlocator))  # 等資訊的DOM載入完畢
        logging.info('候位資訊載入完畢')
    except NoSuchElementException as ex:
        logging.error('候位資訊載入失敗')
        logging.error(str(ex))
    else:
        Informaition = driver.find_element(
            InformationSpanlocator[0], InformationSpanlocator[1]).text
        Number = driver.find_element(
            NumberSpanlocator[0], NumberSpanlocator[1]).text
        logging.info(Informaition)
        logging.info(Number)

end = time.time()
logging.info("總執行時間：%f 秒" % (end - start))
input("請按Enter結束")
sys.exit()
