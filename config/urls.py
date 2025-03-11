from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'KNGW TEA PRODUCTION'
admin.site.site_title = 'KNGW TEA PRODUCTION'
admin.site.index_title = 'KNGW TEA PRODUCTION 管理画面'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tea_production.urls')),
] 