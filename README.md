# AutoOnlineWaiting

#打包指令
pyinstaller -F 波波廚房線上候位.py --icon favicon.ico

#devlop
v2022.07.23.01 
- 初版 波波廚房 可正常線上候位 根據目前時間選擇點選午餐或晚餐

v2022.07.26.02 
- 新增log取代print(資料夾不存在則建立)
- 新增候位成功顯示候位資訊log

v2022.07.26.03
- 新增迴圈 確認有點擊候位按鈕

v2022.07.26.04
- 總執行時間改成紀錄從頭到尾

v2022.07.27.05
- 優化 try except 去除finally
- 檢查所有輸入欄位載入完畢
- 錯誤會記錄哪個WebElement找不到
