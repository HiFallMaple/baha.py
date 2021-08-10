# 巴哈爬蟲

使用python撰寫的巴哈爬蟲，`Baha()` 建立許多函數以利調用<br>
可調用 `Baha_aotu_signin()` 進行完整自動登入與簽到

## 目錄
<!-- TOC -->

- [巴哈爬蟲](#巴哈爬蟲)
  - [目錄](#目錄)
  - [Baha()](#baha)
    - [Baha 建構](#baha-建構)
      - [Baha 完整版建構](#baha-完整版建構)
      - [Baha 精簡建構](#baha-精簡建構)
    - [Baha 屬性](#baha-屬性)
    - [Baha 可用方法](#baha-可用方法)
  - [Baha_auto_signin()](#baha_auto_signin)
    - [Baha_auto_signin 建構](#baha_auto_signin-建構)
    - [Baha_auto_signin 屬性](#baha_auto_signin-屬性)
    - [Baha_auto_signin 可用方法](#baha_auto_signin-可用方法)

<!-- /TOC -->

## Baha()

### Baha 建構

#### Baha 完整版建構
```python
#reqs 需為 requests.Session() 物件
#log_file_name 為 str() 物件，為 log 的檔案名稱
#account 為 dict() 格式如下
reqs = requests.Session()
log_file_name = ".log"
account = {
    "uid": "test123qwe",
    "passwd": "test1qa2ws"
}
baha = Baha(reqs,  log_file_name, account)
```
+ `reqs` 預設值為空 `requests.Session()` 
+ `log_file_name` 預設值為 `".log"`
+ `account` 預設為空 `dict()` 

`reqs` 與 `log_file_name` 皆可不必設定<br>
`account` 則必須設定，但為方便多次使用，初始建構時可先不必輸入，待之後要使用方法時再給予值<br>

#### Baha 精簡建構
```python
baha = Baha()
baha.account = {
    "uid": "test123qwe",
    "passwd": "test1qa2ws"
}
```

### Baha 屬性

```python
self.reqs
self.log_file_name
self.account
self.MAIN_HEADERS = { # 為主要爬蟲時的headers
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Referer': 'https://www.gamer.com.tw/'
}
self.MAIN_URL = "https://www.gamer.com.tw" # 主要爬蟲的 URL
self.USER_URL = "https://user.gamer.com.tw" # 登入請求時 User 相關的 URL
```

### Baha 可用方法

一切函數皆須`賦值account`後才可使用，若未賦值可能出現未知錯誤

| Method               | Argument             | Return                         | Description                          |
| :------------------- | :------------------- |:------------------------------ |:------------------------------------ |
|login()               | None                 | bool                           | 若登入成功回傳True，否則回傳False|
|islogin()             | None                 | bool                           | 若為登入狀態回傳True，否則回傳False|
|signin()              | None                 | dict: signin_status or False   | 若簽到成功回傳簽到狀態，若失敗回傳False|
|get_signin_status()   | None                 | dict: signin_status or False   | 若未登入回傳False，否則回傳簽到狀態|
|is_signin()           | None                 | bool                           | 若當日已簽到回傳True，否則回傳False|


## Baha_auto_signin()
+ 調用 `Baha()` 以進行登入與簽到
+ 調用 `crawler.Session()` 以讀取 `requests.Session()`
+ 調用 `accounts_system` 以讀取複數帳戶之資料與狀態

若無任何帳戶資料，調用 `DEFAULT_ACCOUNTS` 當作簽到帳戶<br>
獲取複數帳戶資料後遍歷以進行登入與簽到，初次登入與簽到完成後將該帳戶之 `session` 儲存以利之後使用，若下次再次簽到可以抓取該 `session` 以避免重複性登入<br>

### Baha_auto_signin 建構
```python
baha_auto_signin = Baha_auto_signin()
```

### Baha_auto_signin 屬性
```python
self.baha = Baha()
self.crawler_session = crawler.Session()
self.accounts_system = Accounts_system()
self.DEFAULT_ACCOUNTS = [{"uid": "test123qwe","passwd": "test1qa2ws"}]
```

### Baha_auto_signin 可用方法

| Method               | Argument             | Return                         | Description                          |
| :------------------- | :------------------- |:------------------------------ |:------------------------------------ |
| run()                | None                 | None                           | 若自動簽到成功回傳True，否則回傳False|
