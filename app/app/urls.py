from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/', include('api.urls')),
    path('web/', include('web.urls')),
    path('newebpayApi/', include('newebpayApi.urls')),
    path('ezpay_invoice/', include('ezpay_invoice.urls')),
    path('backboard/', include('backboard.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)