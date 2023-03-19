
from django.contrib import admin
from django.urls import path, include

from bill_split import views as bill_split_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('bill_split.urls'))
]
