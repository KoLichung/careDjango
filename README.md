# careDjango
!暫定, 未處理：
a.ChatRoom 在 申請預訂並聊聊/需求單詢問服務者/服務者"我可以接案" 時產生~
b.CreateCase 時, 如果有選 Servant, 要產生訂單訊息並推播

藍新測試後台網址
https://cwww.newebpay.com/
42779071
jasonko2022
vCRQtf77UZ6vCie

代號：MS336989148
HashKey: SKYfwec2P46Kzzgc8CrcblPzeX8r8jTH
HashIV: C6RhZZ45pflwEoSP

訂單產生網址
http://202.182.105.11/newebpayApi/mpg_trade?order_id=3
測試卡號：4000-2211-1111-1111

平台商代號：CARE168
平台商名稱：杏心股份有限公司
HashKey：Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q
HashIV：CeYa8zoA0mX4qBpP

測試 API 網址：https://ccore.Newebpay.com/API/AddMerchant

EZPay 發票
https://inv.ezpay.com.tw/main/Login_center/single_login
90139096
Care168
care0963823292

vultr:
8k-TPf]CT964,--R

20221007:
1.register 完要直接登入
line/phone 都一樣~

20221006:
1.register_phone 頁面
2.my_notification_setting 頁面
對應 User model 的 is_fcm_notify,
推播 tasks 的地方也要用這個參數辨別一下~

20221005:
之前的問題：
o 1.platform_percent 要寫到 api 裡~
2.api/user/create 沒有在 create user 的時候, 同時 create user_license_image_ships (web測試正常?!)
3.會員列表~ 申請審核但尚未通過的 "審核中(人數)"
4.重設臨時密碼的 button 移到 會員資訊的右側
5.web 服務員推薦
=> 沒有設定時薪跟地區也會跑出來!
=> 如果尚未設定 isHome/isHospital 不要跑出來~
(所有的服務員回傳都檢查一下~)

20221004:
1.https://inv.ezpay.com.tw/
Ezpay 串發票, 閱讀文件 
發票 api 文件 
https://inv.ezpay.com.tw/Invoice_index/download
2.Django new app ezpay_invoice
test.py, views.py, models.py, admins.py 不需要的 檔案 先砍掉
new tasks.py, 然後串發票的程式寫在這裡面

20221003:
1.
a.mpg_trade 要帶入 user 的 user_store key/iv 去加密
b.notifyurl_callback/[user_store id]/
商店的訂單, 要用商店的 key/iv 去解
ex. notifyurl_callback/1/
user_store = UserStore.objects.get(id=1)
2.
a.member_data_review 加 is_apply_servant 跟 建店 button
b.建店 detail 頁

20220930:
1.
時間紀錄不能 auto, 不然 update 的時候也會更新
(model要改掉,有用到的地方紀錄)
Order, Case, PayInfo 的時間要特別注意
2.
建店的時候, 
a.user 資料要帶入~
b.密碼是什麼?? 如何登入
c.建店有 callback 資料? 要跟交易的 call_back 分開? => call_back 如果沒用到刪掉
建店要存下 UserStore 資料~ => 這樣幕前交易才能使用
3.
修正total_hours的計算

20220929:
昨天的問題：
1.newebpayApi 的 幕前交易 MpgTrade 串好, item_desc 寫 “時薪 $245 共 18 小時”

1.建立預訂單或需求單時, ChatroomMessage, SystemMessage 也要給 order => 檢查 web 的部分
2.要判斷, 不要讓發案者自己發訂單給自己!! => 檢查 web 的部分 
a. /web/search_carer_detail => 彈出 dialog 說 "無法發訂單給自己!" / 確定~
b. 在需求頁的第四個步驟 => 不要返回自己的 servant ~
c. 我可以接案 detail 頁~ 同 a
3.計算 Platform Percent (寫成一個 function) => web 
藍新手續費固定2.8%
階段收費
基本6.5%
120h後5.5%
240h後4.5%
360h後4%
Ex. 基本是 6.5%+2.8%= 9.4%

撈出當月 start_date 且 state="paid" 的訂單s 來計算
9/20~10/20 130hr (用訂單的 start_date 來算)
9/1~9/15 100hr 
當下訂單
9/25~10/10 50hr
(130+100+50=280用 4.5%)
訂單超過 240hr, 即 4.5%


20220928
昨天的問題：
1.api views 
CreateServantOrder, EditCase 的 message 呢?
EditCase 只有一個 servant_id
2.case 的 county  不用拿掉~ 區域一樣下拉選單要存回 (需求單也要改到)
!!!縣市不可改, 區域一樣下拉選單要存回 (需求單也要改到)
3.交通費沒有顯示在計算裡?!

1.資料修正
a.fakeData 的 review 要有 create_at 等日期(目前是 null)
b.會員使用條款
https://docs.google.com/document/d/1lhPhv6CJftQnKIZqfcmhBosFtgT6ijOR9zzs-Kp94L8/edit?usp=sharing
2.newebpayApi 的 幕前交易 MpgTrade 串好, item_desc 寫 “時薪 $245 共 18 小時與額外費用”
3.後台會員多一個按鈕 "重設臨時密碼"(紅色按鈕), 重設密碼為 "00000"
彈出一個 modal 詢問, 是否重設臨時密碼為 "00000" 確定/取消
(要記得密碼是要編碼過的)

20220927
1.
把 model user_service_location 的 county 拿掉
web/index => 區域選擇拿掉
web/my_service_setting_services => 改成只設縣市交通費
/web/booking_location?servant=3 => 縣市不可改, 區域一樣下拉選單要存回 (需求單也要改到)
地址與交通路線或注意事項 拿掉~
2.算
transfer_fee 每一趟交通費
number_of_transfer 幾趟交通費
amount_transfer_fee 總共的交通費
===============
3.Api CreateCase/CreateServantOrder 修正
4.修改 Case 並產生新訂單的 api (EditCase, parasm{case_id, servant_id}, auth 發case的人才能改)

20220926
1.後台案件列表/案件詳細 [此用戶已刪除]
2.常見問題
3.Order 加入 
transfer_fee 每一趟交通費
number_of_transfer 幾趟交通費
amount_transfer_fee 總共的交通費
留下：
wage_hour
刪除：
wage_half_day
wage_one_day
hours_of_work
hours_half_day_work
hours_one_day_work
4.背景任務 
a.訂單 Order 如果超過 create_at 六小時未付款 "unPaid", 即 "canceled" (每隔 10 分鐘檢查)
b.月帳單 Orders 統計(每天的凌晨一點執行)


20220923
24.刪除使用者資料 => api
=> 如果使用者刪除, 訂單要顯示 [此用戶已刪除] 嗎?
=> 
不留的：
on_delete=models.CASCADE

要留：
Case => is_open_for_search = false, 後台 case user == null 要顯示 [此用戶已刪除]
Order =>  後台 order user == null 要顯示 [此用戶已刪除]
Payment => 要留
Message => 要留
ChatRoom => 要留
Reviews => 要留
on_delete=models.set_null

20220922
1.推播任務 (api/views.py 191 行 => chatroom message post 跟 系統訊息)
2.Model Order 欄位增加：
wage_hour
wage_half_day
wage_one_day
hours_hour_work
hours_half_day_work
hours_one_day_work
=> 跟訂單有關的地方要改 ex.預訂單
3.fakeData 修正
4.網站首頁小字修正
5.在 api create case (api/views.py 712 行)
=> servant_ids 要依據 user 產生 ChatroomMessage 的 case message & Chatroom? ＆ SystemMessage
7.我可以接案, 做一個接案訊息頁.
=> "您已經傳送接案訊息給發案者，請到 App 訂單訊息查看！" + App 下載按鈕

20220921
1.我可以接案 chatroom 的檢查會出 bug (if 雙方 chatroom 沒有交集的話)
2.http://localhost:8000/web/recommend_carer
a.大頭貼沒寫到
b.servant_id 沒傳入
3.訂單成立的場景
a.需求案件, 我可以接案
b.申請預訂, 送出預訂單
c.送出需求單
4.把各個場景的訊息放對地方

5.聊聊訊息
a.當訂單狀態改變時, 要產生 case message ()
訂單成立, 修改(x), 付款, 取消, 提前結束

6.celery 任務排程
*** 每隔 15mins check 當日的訂單的狀態
=> 
a.修改狀態 
Case state => “unTaken”, “unComplete”,”Complete”, “Canceled”,“endEarly”
b.發訊息(服務開始前3小時提醒 3hr~2:45 , 提醒您，某某某的預定即將開始，請您務必前往服務哦～) => 系統訊息

使用 celery
a.安裝 RabbitMq, 啟動 RabbitMQ server
b.cd app (要在有 app/celery.py 的那個 module 檔案夾下, 接下面那個指令)
celery -A app worker -l INFO (worker 負責做工作)
celery -A app beat -l INFO (跑 schedule task, 負責派工)
https://docs.google.com/document/d/1Ta4y_nuIvT_yzX15wx0ky09xPW42Yv8nEB3Ntv6cp0g/edit

20220920
1.request_form_patient_info => 有 bug
servant is not difined 約 2027 行
2.提前結束的 api
提前結束按鈕~
=> 放在 app 的訂單詳細頁~
=> 提前結束 api
ex.服務時間 9/5~9/10, 9/8  提前結束
如果提前結束, 這個 api 是做給需求者使用的
提前結束服務（提前取消服務），
費用結算至服務截止時間及被取消第一日之服務費用的50%
=>
9/5,9/6, 9/7,9/8  的 hours
再加上 9/8 的 hours 的一半
= total hours
=> 當我 call 這隻 api, 重新修改訂單
params: order_id, user auth, end_time : 2022-09-08,15:00
(看護證明, 如果訂單提前結束,看護證明的內容要修正正確~)
======
3.系統訊息的 task
收到預訂單(web, api) => "(恭喜您，收到來自於 xxx 的預訂單，請利用聊聊與他聯絡！)"
訂單成立 => "(恭喜您，來自於 xxx 的訂單編號 xx 已收款成立！)"
訂單取消含提前結束服務 => "(來自於 xxx 的訂單編號 xx 已取消！)"
訂單提前結束服務 => "(來自於 xxx 的訂單編號 xx 已提前結束服務！)"
=>
a.先在 shell 測試 (from message.tasks import *)
b.塞到正確的地方, 再測試 
from message.tasks import *
test(user,order)

20220919
1.改薪水算法
2.不要 AM,PM 用 24hr
3.新做一頁看護證明簡化版

20220916
1.http://localhost:8000/web/recommend_carer
這個漏傳值到下一頁, 而且不要用 phone
2.http://localhost:8000/web/request_form_patient_info
Field 'id' expected a number but got ''.
1921 disease_list.append(DiseaseCondition.objects.get(id=diseaseId))
=> 都不選的情況下這頁會出錯(or 下一頁回上一頁出錯?!)
http://localhost:8000/web/booking_patient_info?servant=0985463816
769 Field 'id' expected a number but got ''.
=> 同問題
=> 此頁的 Ajax 如果資料不全, "申請預訂"的 Button 先不反應
3.地址
（縣市）（地區）
路名：我是框框
※為確保您的隱私，居家照顧此欄位只需填”路名”。

醫院名（機構名稱）及 注意事項：我是框框
※為確保您的隱私，請勿在此處填寫病房號或住家詳細地址，請用聊聊告知接案服務者即可。
http://localhost:8000/web/request_form_service_type
http://localhost:8000/web/booking_location?servant=0985463816
4.改用 id (其他頁面也要檢查)
http://localhost:8000/web/search_carer_detail?servant=0985463816
並且資訊不全時, 不要按申請預訂
=> 會當機!
http://localhost:8000/web/booking_location?servant=0985463816
5.修改名稱, 顯示 林先生, 黃小姐
http://localhost:8000/web/requirement_detail?case=1
http://localhost:8000/web/recommend_carer
http://localhost:8000/web/search_list?weekday_list=%5B%5D&city=3&county=%E5%85%A8%E5%8D%80&care_type=%E5%B1%85%E5%AE%B6%E7%85%A7%E9%A1%A7&is_continuous_time=True
http://localhost:8000/web/search_carer_detail?servant=0985463816
{{ obj.name|slice:"0:3" }}
{{case.user.name|slice:"0:1"}}{% if case.user.gender == 'M' %}先生{% else %}小姐{% endif %}
{{servant.name|slice:"0:1"}}{% if servant.gender == 'M' %}先生{% else %}小姐{% endif %}

20220915
1.http://localhost:8000/web/my_service_setting_services
=> 加價項目去除勾選, 如果沒填, 預設 0%
2.http://localhost:8000/web/request_form_patient_info
=> 超過 70/90~ 要自動勾選加價, 且不能反勾
3.幫助中心訊息
=> 後台 列表/新增/編輯/刪除

20220914
1.http://localhost:8000/web/my_service_setting_about
=> 選擇完文件, 直接上傳
http://localhost:8000/web/my_edit_profile
=> 選擇完文件, 直接上傳
2.後台審核狀態修改有誤
http://localhost:8000/backboard/member_data_review?user=2
3.
a. Create User, 要 Create UserLicenseShip
=> Create User 時, 寫一個 create for loop
=> User 可能是改寫 UserManager 下的 create_user 即可~
b. Create License 時, 要 Create UserLicenseShip
https://stackoverflow.com/questions/4269605/django-override-save-for-model
4.backboard/all_members => 所有會員(120), 需求者(40), 服務者(80) 列表出現(是否審核通過為服務者)

20220913
1.後台的 login 頁面

20220912
1.退款頁案件編號 case id
2.後台pager
3.會員資訊 服務者審核通過
4.資料審核頁

20220908
1.訂單計算金額有 bug(訂單時間重複?!)
2.修正 my_service_setting 的 bug
並且分三頁：
a.my_service_setting_time
b.my_service_setting_services
c.my_service_setting_about
========
3.後台的 cases, case_detail, refound
http://localhost:8000/backboard/refunds?case_id=1&order_id=2
========
4.後台的 users, user_detail, user 

20220906
1.blog => 全部, blog_detail => tab items
2.預訂單 
確認付款 
v => 產生 Order, Message, 刪除 Temp case 

xxx => 返回時, 回到 Servant Detail (不確定是不是從 ReturnUrl 設定)

v If temp-case == None:
	redirect to Servant Detail
=======
3.我的服務設定~

20220905
1.預訂單的部分完成
2.部落格列表, 部落格詳細頁

20220902
1.修正需求單
2.繼續預訂單的部分

20220901
1.關於命名
city => City or id(Foreign key)
city_name => String

cities => [City, City, City]
city_ids => [2, 3, 5, 7]

city_list => [City, City, City]
(cities 優於 city_list)
2.完成填寫需求單的部分, 需求單部分的程式碼整理一下
====
3.申請預訂

20220831
1.city 改成 "台北市" (不要 String 存 id)
2.license 要加一個審核狀態, isPassed (bool, default=False)
3.files.html 的 form 改成一個 licence_id 1~3 的 for 迴圈, 多一個 hidden_input licenseId
4.views.py/my_files 的方法收斂
======
5.申請預訂3, 申請預訂4

20220830
1.評價列表的 bug
2.liscense image 的上傳沒有正確使用 image_upload_handler
3.在 model 建一個 TempCase
User
在第一頁時,  
“下一頁繼續” => 產生 temp case
“取消” => delete temp case

city_id => 1
county_id => 0 (代表全區), 1~... 代表 county

disease_ids => “1,4,7” 
condition_ids => “2,5,6” 
service_ids => “2,5,7”

第四頁, 
”送出” => 把 temp case 刪除, 產生 case

20220829
1.total_money = base_money + service_increase_money 這樣比較直覺
2.做下載 pdf 檔(如果困難, 這個按鈕可以拿掉) 跟 列印
3.完成 write_review 的星星部分
4.完成 我接的案, 我的需求案件的星星部分

20220825
1.我接的案, 我接的案詳細
2.個人設定, 修改基本資料, 我的文件上傳
3.收款方式

20220824
1.評價頁
2.需求案件列表
3.需求案件詳細

20220823
1.relative_name 修正
Order case => "case_orders"
UserLicenseShipImage => "user_license_images"
UserLanguage => "user_languages"
OrderIncreaseService => "order_increase_services"
OrderWeekDay => "order_weekdays"
Message => "chatroom_messages"
2.Line login 的 redirect_to = request.GET.get('next', '') 要移除?
3.if line login 之後, 發現沒有該 line id 的帳號, 則要註冊(Create 新使用者)
=> 現在是 "如果他在 LINE 註冊時, 是用既有帳號, 則 LINE ID 綁定到既有帳號"(綁定之後可以用 LINE 登入)
=> v 要加做 非既有帳號, 註冊(Create 新使用者)
=======
4.做 reviews 評價頁的部分
http://localhost:8000/web/my_reviews
尚未評價 => 我發的案, 我還沒評價
我的評價 => 我發的案, 我已評價
給我的評價 => 我發的案, 給我的評價

20220822
1.Line 登入(透過 LINE 繼續) 
=> 如果沒有 User.objects.get(line_id=line_id) => 跳到註冊頁, 讓他註冊 並把 sub 存在 line_id => 註冊完回到 index 頁
=> 如果有 User.objects.get(line_id=line_id) => 取回 User 資料, 返回 index 頁
2.把 user_service_ship 的 relatitve name 改一下~
3.把註冊的部分完成

20220819
1.實現 登入 方法 (登入之後, 回上一頁)
2.在 views 檢查是否已登入
3.修正 nav bar (base.html)
=============
4.實現 LINE Web Login
https://developers.line.biz/en/docs/line-login/integrate-line-login/
a.連到 LINE 的網址
b.授權成功後 call_back
c.redirect_url
d.取得 user line_id
e.User.objects.get(line_id=line_id) 取得 user
**f. 用 line_id 去 aunthenticate(user)


20220818
1.把 index 頁改成 開始日期, 結束日期, 開始時間, 結束時間 
2.需求列表 / 需求詳細.

20220817
1.index 頁, 插入 每週時段 選擇~
2.index 頁帶時間到 search_list 頁
3.search_list 帶資料到 search_carer_detail
4.星星單層 border 就好了

20220816
1.整理 search_carer_detail 程式碼
2.search_carer_detail 的 dialog 資料帶入
3.index 頁, 插入 每週時段 選擇~
# start_end_date': ['22/09/06 to 22/09/23'] 字串處理後22世紀不能用

20220815
1.刪掉 user model, 把 avg_rating, servant_avg_rating
2.整理一下 index, search_list, search_carer_detail (程式碼整理, 對齊)
3.試試 servant.service_locations 

20220809
0.index 頁的 縣市 跟 區域 關係, 寫成 javascript
///
a.在 index 頁上面隨意地方, 加一個按鈕, 加一個 文字欄位
b.當按鈕按下去時, 到 views 去取資料
c.將取得資料顯示在 文字欄位上
///

1.index 進入搜索列表頁, bug 要修整
2.search 頁 的 filter 資料要帶入, 改成統一按搜索鍵才送出資料重新搜索
3.星星問題

20220808
1.搜索列表
2.照護者 detail

20220805
1.撥款 => 請款完成後, 從藍新帳戶撥款到 合作商店 的藍新帳戶
*check 實際撥款金額
2.扣款 => 撥款完成後, 從合作商店 扣款到 我們的 藍新帳戶
*check 實際扣款金額
3.手機測試幕前交易

20220804
1.
*.avg_offender_rating 要是 floating
*.http://202.182.105.11/api/reviews/?review_type=unrated
回傳 servant_name

2.開店的時候, 要只有信用卡交易, 其他不需要
3.處理 notify 的 api 
4.查一下 20220802 的交易是否已請款(正常要自動請款)
5.if 4 ok, 則測試 撥款 跟 扣款 api

20220803
1.NotifyUrl 的回傳資訊紀錄：
MerchantID, Amt, TradeNo, MerchantOrderNo, PaymentType, PayTime, EscrowBank, AuthBank, Auth, Card6No, Card4No, PaymentMethod

2.http://202.182.105.11/api/search_cases/1/
a.avg_offender_rating 
b.num_offender_rating 要是整數 (rating_nums 的型態要是 integer)
3.http://202.182.105.11/api/need_cases/
a.應該要回傳 照顧者名稱, 如果已經確認照顧者的話~
servant_name
4.Model User 多一個欄位 is_passed, is_servant_passed

20220802
0.建立新商店, 把回傳資訊存在 UserStore, 然後要能從藍新後台登入該商店
https://cwww.newebpay.com/
1.MPG 的跳轉頁的部分, 如果不要 submit, 寫 javascript 直接 submit
http://mh-resource.blogspot.com/2015/03/javascript-submitform.html

2.撥款 => 請款完成後, 從藍新帳戶撥款到 合作商店 的藍新帳戶
3.扣款 => 撥款完成後, 從合作商店 扣款到 我們的 藍新帳戶
v a.發動 合作商店 的信用卡交易(幕前交易API), 要把 $ 存到 服務者 的帳戶(5筆)
v b.用查詢 api 查詢狀態
c.if 請款狀態是成功, 用撥款 api 撥款到合作商店的藍新帳戶 (合作商店的藍新帳戶怎麼登入)
d.if 已經撥款, 發動扣款, 扣 10% 到我們的藍新帳戶

20220801
1.請款 api (22072910201485051)
2.查詢 api (22072910201485051)
3.取消授權 api (產生假交易, 再取消授權)

20220729
0.發動 合作商店 的信用卡交易(幕前交易API), 要把 $ 存到 服務者 的帳戶
1.金流扣款指示 api (扣金流手續費 3%), 從 服務者 的帳戶扣錢
(是否能指示扣款金額為多少?還是只能%?)
2.金流撥款指示 api (扣平台手續費 10%), 從 服務者 的帳戶扣錢
a.用平台商代號：CARE168 去發動撥款指示, 將合作商店的 $ 撥到 我們的藍新帳戶

20220728
1.大頭貼 api 
2.web/index 的地點資料
!!3.search_list 資料串接

20220727
1.City model add newebpay_value
2.修正 county.csv, 修正 importCityCounty, 重新 set_sand_box_data
3.把幕前交易 api 測通

20220726
1.照顧者預訂單的 api => 產生 case, 產生 order, 跳轉付款頁面~
!? 選擇時間時，如不符合servant的服務時間，是否需要提示？

20220725
1.Home 的 api 拿來 case choose searvant, home 的 api 做一個 order param
order=rating, rating_nums, price_low, price_high
2.CreateCase 修正 servant_ids, datetime 格式
3.
import module
module.aes256_cbc_encrypt(query_str, key, iv)
先測試建店 API
解析回傳參數, 寫一個 UserStore class 把必要參數 MerchantID, MerchantHashKey, MerchantIvKey 存下來


20220722
1.做產生需求單(Case)的 API, 把資料先都塞到一支 Create(POST) 的 api 試試
2.更新 UpdateUserSerializer 把 User 需要的前端資料回傳
3.CaseSearchViewSet 有 bug, 再檢查 retrieve 是否正常
# weekdays_num_list 需要寫 for 迴圈去 filter
# order_conflict_servants_id 的 value 應該是 servant

20220721
1.寫建店 API：
a.Post data 格式 => PartnerID_ , PostData_
v b.加密 => if 傳 xxxx, 加密結果是 oooo
c.測試 Post 到 藍新 api server

20220720
1.把 Chatroom Model 的 memebers 拿掉, 統一用 ChatroomUserShip 來做
2.建店 API
a.startapp newebpayApi
b.把沒必要的檔案先砍掉 ex. test.py, models.py ...等
c.把 api 寫在 views.py

20220719
1.UserLanguage 要做一個 UserLanguageSerializer 要傳回 remark
2.UserLicenseImageView 改成 APIView, 有兩個方法 GET, PUT, GET 要取得 license list, Put 就是要比對更新或產生新資料
3.UserServiceWeekTime, User Language, User Service, User Location 改成 ViewSet 同上做法
4.Chatroom 跟 User 之間做一個 ChatroomUserShip 解決 20220714 的 5
(2,3 不要用 router, 用 path, 只是分成 GET 跟 PUT 兩種不同方法去處理)

20220718
1.在 MessageViewSet Create response 時, 會回傳 Case, 如果該 Case 有 Order, 則傳回最近的 order
2.檢查修正 User 的 ATM Data
3.UserServiceWeekTime, User Language, User Service, User Location, 
a.返回的時候, 返回 UserWeekTime 細節就好
b.比對後再動作, 不要資料全刪 => 可以分兩個 for loop 第一步 把不需要的資料刪除 第二步 把沒有的新資料加進來
4.User 服務類型要加上 isHome, isHospital 的 param
5.User Licence Ship Image 改成 licence_id, image

20220714~0715
1.memebers 的 length 開到 30
2.新訊息產生時, 要去更新 chatroom update_at
3.訊息要排序, 越晚創建越前面
!!4.chatroom 的返回要 order_by update_at (ChatRoomViewSet 的 get_queryset filter??)
!!5.chatroom 用 string 去記, 應該是不行?! => 要再想一下~
6.OrderViewSet 的 List, Get
7.User 的 functions
a.Update 付款ATM資料
b.List, Create, Update User Service Week Time
c.List, Create, Update User Language
d.List, Update User 的 服務類型, 價錢
f.List, Create Update User 的服務地區
g.List, Create, Update User 的服務
h.List, Create, Update User 的 Licence
i.List, Update User background_image

20220713
1.把 readme 的 ReviewViewSet 的 Put 資料補上
2.做一個 model Chatroom => 紀錄 user ids, 跟 update_at
3.chatroom 跟 message 是一對多關係
4.Chatroom 的 viewset (List, Create)
5.Message 的 viewset (List, Create) a.string b.case c.case(order)
(如果格式能調好就條好,不行就先傳 case.id, order.id)
6.SystemMessage 的 viewset (List)

20220712
1.改掉 views 裡面的計算
2.當 order 產生時, review 應該也要相應產生 (先 FakeData 再做下一步)
3.(需求者)做 Reviews API 的部分 ReviewViewSet 的 改Put(新增評論), 查Get(list, retrieve) 
=> xxx/reviews/1 
4.(服務者)給評價 寫一個 APIView, ServantPutReviewView(APIView) 的 Put Method

20220711
1.Case 查詢的 reviews 改成 review, 並回傳該案件的 review 就好了
2.Service 要返回所有該 case 的 services
3.設計 Order 的案件金額相關欄位, 並 fakeData
4.Case 只要回傳 order 就好了

20220708
1.CaseViewSet 的 get_queryset, retrieve
2.RecommendServantViewSet 的 get_queryset
----------
1.把 OrderWeekDay 寫進 admin
2.把 OrderWeekDay 寫進 fakeData
3.CaseSearchViewSet 用於接案者找尋案子, 以及觀看案子詳細, 包含 get_queryset 跟 retrieve
4.ServantCaseViewSet 用於使用者取得自己已接的案子(我接的案, 我接的案件詳細), 包含 get_queryset 跟 retrieve
5.NeedCaseViewSet 用於使用者取得自己發出的案子(我發的需求案件, 我發的案件詳細), 包含 get_queryset 跟 retrieve
(3,4,5 在資料上應該會有些不同, 4跟5 要用上 authentication)

20220707
1.在 retrieve method 把 license 改成跟 service 同樣做法
2.檢查 SearchServantViewSet 的 get_queryset method 的 weekdays filter 是否正確
3.完成 SearchServantViewSet 的 get_queryset method 的 rate_num 回傳
4.在 Order model 增加 start_datetime, end_datetime, weekday, start_time, end_time
！5.完成 SearchServantViewSet 的 start_datetime, end_datetime 應用
6.修改 readme 的 search servant 連結, 放入 params

20220706
1.把程式碼改乾淨
2.把 model 的 is_alltime_service 改成 is_continuous_time
3.增加 ServantSerializer 的欄位 background_image, services, licences, about_me, reivews[:2] (記得要給 default data)
4.完成 SearchServantViewSet 的 retrieve method
5.完成 SearchServantViewSet 的 get_queryset method 的 params filter  

20220705
1.把 License, Service 的備註放到 remark 這個欄位
2.做 Language, Service, DiseaseCondition, BodyCondition, City, County 的 List Api
3.做 Case, Order, UserServiceLocation, CaseWeekDayTime, UserWeekDayTime 的 List, Post, Retrieve, Put Api
4.做 Message, SystemMessage 的 List, Post Api
5.把主路徑整理到 readme.md 的最上方

20220704
1.畫出目前 model 的關係圖
2.把 model 寫進 modelCore.admin
3.做 fakeData