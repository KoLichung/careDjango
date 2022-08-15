# careDjango

License 列表
http://localhost:8000/api/licenses/
Language 列表
http://localhost:8000/api/languages/
Service 列表
http://localhost:8000/api/services/
DiseaseCondition 列表
http://localhost:8000/api/disease_conditions/
BodyCondition 列表
http://localhost:8000/api/body_conditions/
City 列表
http://localhost:8000/api/citys/
County 列表
http://localhost:8000/api/countys/

Order 的列表, 查詢, 新增, 修改
http://localhost:8000/api/orders/
UserServiceLocation 的列表, 查詢, 新增, 修改
http://localhost:8000/api/userServiceLocations/
CaseWeekDayTime 的列表, 查詢, 新增, 修改
http://localhost:8000/api/caseWeekDayTimes/
UserWeekDayTime 的列表, 查詢, 新增, 修改
http://localhost:8000/api/userWeekDayTimes/
Message 的列表, 新增,
http://localhost:8000/api/messages/
SystemMessage 的列表, 新增,
http://localhost:8000/api/systemMessages/

Search Servant 的列表, 查詢 用於首頁
http://localhost:8000/api/search_servants/?care_type=home&city=3&county=35&is_continuous_time=True&weekdays=1,3,5&start_end_time=6:9&start_datetime=2022-07-21T00:00:00Z&end_datetime=2022-08-20T00:00:00Z
RecommendServantViewSet 的列表
http://localhost:8000/api/recommend_servants/

CaseSearch 的列表, 查詢, 新增, 修改
http://localhost:8000/api/search_cases/?city=6&county=77&start_datetime=2022-07-10T00:00:00Z&end_datetime=2022-08-05T00:00:00Z&care_type=hospital
ServantCaseViewSet 的列表, 查詢
http://localhost:8000/api/servant_cases/
NeedCaseViewSet 的列表, 查詢
http://localhost:8000/api/need_cases/

ReviewViewSet 的列表, 查詢, 修改
#review_type=unrated, given, received
http://localhost:8000/api/reviews/?review_type=unrated
Get
http://localhost:8000/api/reviews/1
Put 
http://localhost:8000/api/reviews/1
body_params

ServantPutReviewView 的修改
body form-data: case_offender_rating : 5 , case_offender_comment : Test
http://localhost:8000/api/servant_put_review/1

ChatRoomViewSet 的列表, 新增
body form-data: users : 2,4
http://localhost:8000/api/chatroom

MessageViewSet 的列表, 新增
body form-data: case : 1 , content : Ok
http://localhost:8000/api/messages/?chatroom=1

SystemMessageViewSet 的列表
http://localhost:8000/api/system_messages

OrderViewSet 的列表, 查詢
http://localhost:8000/api/orders

UpdateATMInfo 的修改
body form-data:ATMInfoBankCode : xxx  ATMInfoBranchBankCode: xxx accounts: xxx
http://localhost:8000/api/user/update_ATM_info

CreateCase 的新增
http://localhost:8000/api/create_case?county=57&start_date=2022-07-22&end_date=2022-08-15&weekday=1,3,5&start_time=08:30&end_time=17:30
body form-data: care_type: home name: 王老明 gender: M  age: 69  weight: 79  disease: 1711  disease_remark: test  body_condition: 2,8,10  conditions_remark: test  service: 1,4,7  emergencycontact_name: 王大明  emergencycontact_relation: 父  emergencycontact_phone: 0987654321
ChooseServantViewSet 的 查詢 修改
http://localhost:8000/api/choose_servant

CreateServantOrder 的新增
http://localhost:8000/api/create_servant_order?county=57&start_date=2022-07-22&end_date=2022-08-15&weekday=1,3,5&start_time=08:30&end_time=17:30&servant_id=3
body form-data: care_type: home name: 王老明 gender: M  age: 69  weight: 79  disease: 1,7,11  disease_remark: test  body_condition: 2,8,10  conditions_remark: test  service: 1,4,7  emergencycontact_name: 王大明  emergencycontact_relation: 父  emergencycontact_phone: 0987654321

CreateMerchant 
http://202.182.105.11/newebpayApi/create_merchant

MpgTrade
http://127.0.0.1:8000/newebpayApi/mpg_trade
http://202.182.105.11/newebpayApi/mpg_trade

SearchTradeInfo
http://127.0.0.1:8000/newebpayApi/search_tradeinfo
http://202.182.105.11/newebpayApi/search_tradeinfo

CancelAuthorization
http://127.0.0.1:8000/newebpayApi/cancel_authorization
http://202.182.105.11/newebpayApi/cancel_authorization

Invoice
http://127.0.0.1:8000/newebpayApi/invoice
http://202.182.105.11/newebpayApi/invoice

Appropriation
http://127.0.0.1:8000/newebpayApi/appropriation
http://202.182.105.11/newebpayApi/appropriation


Debit
http://127.0.0.1:8000/newebpayApi/debit
http://202.182.105.11/newebpayApi/debit

NotifyUrlCallback
http://localhost:80/newebpayApi/notifyurl_callback
http://202.182.105.11/newebpayApi/notifyurl_callback

index
http://127.0.0.1:8000/web/index

search_list
http://127.0.0.1:8000/web/search_list

search_carer_detail
http://127.0.0.1:8000/web/search_carer_detail?servant=0985463816

!暫定, 未處理：
a.ChatRoom 在 申請預訂並聊聊/需求單詢問服務者/服務者"我可以接案" 時產生~
b.CreateCase 時, 如果有選 Servant, 要產生訂單訊息並推播
c.web/index 的每週時間預定沒有工作日的選項

藍新測試後台網址
https://cwww.newebpay.com/
42779071
jasonko2022
vCRQtf77UZ6vCie

代號：MS336989148
HashKey: SKYfwec2P46Kzzgc8CrcblPzeX8r8jTH
HashIV: C6RhZZ45pflwEoSP

測試卡號：4000-2211-1111-1111

平台商代號：CARE168
平台商名稱：杏心股份有限公司
HashKey：Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q
HashIV：CeYa8zoA0mX4qBpP

測試 API 網址：https://ccore.Newebpay.com/API/AddMerchant

vultr:
8k-TPf]CT964,--R

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