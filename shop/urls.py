"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path
from shop import views

urlpatterns = [
    path('', views.buy_items),
    path('add', views.update_items),
    path('buy', views.buy_items),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('item/<str:item_uuid>', views.item_show),
    path('manage', views.manage_items),
    path("change", views.change),
    path('myorders', views.my_order),
    # path('checkout/<str:item_uuid>', views.checkout),
    path("change/<str:item_uuid>", views.change_item_details)
    ]
