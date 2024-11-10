# practice_management/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 管理サイトのログアウトURLをカスタマイズ
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/admin/login/'), name='admin_logout'),
    
    # 認証URLの追加
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 管理サイトのURLパターン
    path('admin/', admin.site.urls),
    
    # 他のアプリケーションのURLパターン
    path('', include('main_app.urls')),
]
