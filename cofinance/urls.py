from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from cofinance.views_web import (
    login_view, logout_view, dashboard_view,
    credits_view, remboursements_view,
    assurance_view, notifications_view 
)
from cofinance.views_web import register_view
from chat.views import chat_page
from credits.views import changer_statut_web

urlpatterns = [
    path('admin/', admin.site.urls),
    # API
    path('api/accounts/', include('accounts.urls')),
    path('api/credits/', include('credits.urls')),
    path('api/remboursements/', include('remboursements.urls')),
    path('api/assurance/', include('assurance.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/chat/', include('chat.urls')),
    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Interface web
    path('', lambda r: __import__('django.shortcuts', fromlist=['redirect']).redirect('/login/')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('credits/', credits_view, name='credits'),
    path('remboursements/', remboursements_view, name='remboursements'),
    path('assurance/', assurance_view, name='assurance'),
    path('notifications/', notifications_view, name='notifications'),
    path('register/', register_view, name='register'),
    path('chat/interface/', chat_page, name='chat-interface'),
path('credits/<int:credit_id>/statut/', changer_statut_web, name='changer_statut_credit'),
]