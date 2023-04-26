# moodle notify
> 本專案實作 銘傳大學的 moodle 課程事件 notify 功能，透過 config.ini 的 moodle account 模擬登入後取得課程資訊並且發出通知
## 開始之前
在 config.ini 裡設定 moodle 的帳號密碼 
到 https://notify-bot.line.me/my 去申請 存取權杖（開發人員用）
並貼上 line_token

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