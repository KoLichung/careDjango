from django.urls import path
from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('update_line_id/', views.UpdateUserLineIdView.as_view()),
    path('update_user_password', views.UpdateUserPassword.as_view()),
    path('update_ATM_info', views.UpdateATMInfo.as_view()),
    path('update_user_weekdaytimes', views.UpdateUserWeekDayTime.as_view()),
    path('update_user_languages', views.UpdateUserLanguage.as_view()),
    path('update_user_caretype', views.UpdateUserCareType.as_view()),
    path('update_user_locations', views.UpdateUserLocations.as_view()),
    path('update_user_services', views.UpdateUserService.as_view()),
    path('update_user_license_images', views.UpdateUserLicenseImage.as_view({'get': 'list'})),
    path('update_user_info_images', views.UpdateUserInfoImage.as_view()),
]
