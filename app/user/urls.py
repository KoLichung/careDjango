from django.urls import path, include
from user import views

app_name = 'user'


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('update_line_id/', views.UpdateUserLineIdView.as_view()),
    path('update_user_password', views.UpdateUserPassword.as_view()),
    path('update_ATM_info', views.UpdateATMInfo.as_view()),
    path('user_weekdaytimes', views.UserWeekDayTimesViewSet.as_view()),
    path('user_languages', views.UserLanguagesViewSet.as_view()),
    path('update_user_caretype', views.UpdateUserCareType.as_view()),
    path('user_locations', views.UserLocationsViewSet.as_view()),
    path('user_services', views.UserServicesViewSet.as_view()),
    path('user_license_images', views.UserLicenseImagesViewSet.as_view()),
    path('update_user_background_image', views.UpdateUserBackgroundImage.as_view()),
    path('update_user_images', views.UpdateUserImage.as_view()),
    path('get_update_user_fcm_notify', views.GetUpdateUserFCMNotify.as_view()),
    path('deleteuser/<int:pk>/', views.DeleteUser.as_view()),
]
