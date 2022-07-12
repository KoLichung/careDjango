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