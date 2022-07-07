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
Case 的列表, 查詢, 新增, 修改
http://localhost:8000/api/cases/
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

Search Servant 的列表, 用於首頁
http://localhost:8000/api/search_servants/?care_type=home&city=3&county=35&is_continuous_time=True&weekdays=1,3,5&start_end_time=6:9&start_datetime=2022-07-21T00:00:00Z&end_datetime=2022-08-20T00:00:00Z

20220707
1.在 retrieve method 把 license 改成跟 service 同樣做法
2.檢查 SearchServantViewSet 的 get_queryset method 的 weekdays filter 是否正確
3.完成 SearchServantViewSet 的 get_queryset method 的 rate_num 回傳
4.在 Order model 增加 start_datetime, end_datetime, weekday, start_time, end_time
5.完成 SearchServantViewSet 的 start_datetime, end_datetime 應用
6.修改 readme 的 search servant 連結, 放入 params

20220706
1.把程式碼改乾淨
2.把 model 的 is_alltime_service 改成 is_continuous_time
3.增加 ServantSerializer 的欄位 background_image, services, licences, about_me, reivews[:2] (記得要給 default data)
4.完成 SearchServantViewSet 的 retrieve method
5.完成 SearchServantViewSet 的 get_queryset method 的 params filter  
# start_datetime & end_datetime 好像不會用到

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