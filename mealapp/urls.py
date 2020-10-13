from django.urls import path
from . import views
urlpatterns = [
    path('', views.start),
    path('index/', views.homepage),
    path('add-member', views.add_member),
    path('add-meal', views.add_meal),
    path('edit-member/<int:id>', views.edit_member),
    path('delete-member/<int:id>', views.delete_member),
    path('members', views.member_list),
    # path('manage-meal', views.manage_meal),
    path('meal-list', views.meal_name_list),
    path('meal/<int:id>', views.meal_list),
    path('add-amount', views.add_amount),
    path('amount-list', views.ammount_name_list),
    path('ammount/<int:id>', views.amount_list),
    path('add-bazar', views.add_bazar),
    path('bazar-list', views.bazar_list),
    path('total', views.total),
    path('membertotal', views.total_name_list),
    path('tatal/<int:id>', views.total_details),
    path('mm-login/', views.login),
    path('mm-user-reg/',views.user_create),

    




    #------------website----------
    path('home/', views.index, name="index"),
    path('contact/', views.contact),
    path('properties/',views.properties),
    path('<str:name>',views.properties_detail),
    path('blog/',views.blog),
    path('blog/<str:name>',views.blog_detail),
    path('user-ad/',views.user_ad),
    path('user-reg/',views.user_register),
    path('login/',views.signin),
    path('forgot-pass/',views.forgot_pass),
    path('user-ac/',views.user_ac),
    path('logout/',views.logout),
    path('delete-post/<int:id>', views.delete_post),
    path('edit-post/<int:id>/', views.edit_post),
    path('about-us/',views.about_us),
]