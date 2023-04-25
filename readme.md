# moodle notify
> 本專案實作 銘傳大學的 moodle 的行事曆 notify 功能，透過config 的 moodle account 模擬登入後取額 日歷 ics 檔案後，進行截止日判斷在發出通知。 

## 開始之前
在 config.ini 裡設定 moodle 的帳號密碼 以及 分站的位置
到 https://notify-bot.line.me/my 去申請 存取權杖（開發人員用）
並貼上 line_token

#### 如何知道分站的位置 ?
從 https://moodle.mcu.edu.tw/ 登入後隨便點選一個課程
會發現網址變成以下的樣子
https://moodle3-06.mcu.edu.tw/course/view.php ...
其中 **moodle3-06** 就是分站的位置


## 開始專案
### 方法一、直接使用執行檔執行

### 方法二、使用 python 環境運行
安裝 python 相依套件
```
pip install -r requirements.txt
```
執行主程式
```
python app.py
```