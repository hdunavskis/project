"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('institute/<str:institute_id>/', views.requisition_create, name="requisition_create"),
    path('authenticated/', views.authenticated, name="authenticated"),
    path('authenticated/<str:requisition_id>', views.authenticated, name="authenticated"),
    path('random/', views.random, name="random"),
    path('premium_products/<str:account_id>', views.premium_products, name="premium_products"),
    path('balance/<str:account_id>', views.balance, name='balance'),
    path('account_details/<str:account_id>', views.account_details, name='account_details'),
    path('admin/', admin.site.urls),
]

handler404 = views.page_not_found
handler500 = views.page_not_found
