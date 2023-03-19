from django.urls import path
from . import views

urlpatterns = [
    path('group/',views.GetBillGroup.as_view()),
    path('group/<int:id>/',views.GetBillGroup.as_view()),

    path('group/create/', views.CreateGroup.as_view()),
    path('group/add/user/',views.AddUser.as_view(),),
    path('group/add/bill/',views.AddBill.as_view(),),
    path('group/bill/split/',views.SplitBill.as_view(),)

]