# 巴哈爬蟲

使用 python playwright 撰寫的巴哈爬蟲，建立簡易函數以利調用

## 目錄
<!-- TOC -->

- [巴哈爬蟲](#巴哈爬蟲)
  - [目錄](#目錄)
  - [Baha() 建構](#baha-建構)
    - [account](#account)
    - [cookies](#cookies)
    - [Baha 可用方法](#baha-可用方法)

<!-- /TOC -->

## Baha() 建構
+ `account` 必選：帳號密碼資訊
+ `headless` 選項：設定在腳本運行時是否顯示瀏覽器畫面，True 為顯示
+ `cookies` 選項：預設想載入的 cookies
```python
account: Account = {'userid': "***", 'password': "***"}
with Baha(account, headless=True, cookies=cookies) as baha:
    baha.login()
```

### account
```python
class Account(TypedDict):
    userid: str
    password: str
```

### cookies
為 `list[Cookie]`，其中 `Cookie` 格式如下：
```python
class Cookie(TypedDict):
    name: str
    value: str
    domain: str
    path: str
    expires: int
    httpOnly: bool
    secure: bool
    sameSite: str

```

### Baha 可用方法
| Method        | Argument | Return       | Description                                             |
| :------------ | :------- | :----------- | :------------------------------------------------------ |
| login()       | None     | None         | 登入失敗會跳 LoginFailedError，並顯示登入錯誤訊息       |
| islogin()     | None     | bool         | 若為登入狀態回傳 True，否則回傳False                    |
| is_signin()   | None     | bool         | 若當日已簽到回傳True，否則回傳False                     |
| logout()      | None     | None         | 登出                                                    |
| get_cookies() | None     | list[Cookie] | 返回當前 context 的 cookies                             |
| get_userid()  | None     | str          | 返回當前登入狀態的 userid，若尚未登入會跳 NotLoginError |