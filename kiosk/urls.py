from django.urls import path
from . import views


urlpatterns = [
    # path('cart/', views.OrderDetail.as_view()),
    path('cart/', views.cart, name='cart'),
    path('success/', views.success),
    path('pay/', views.pay, name='pay'),

    # test
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('menu/', views.menu, name='menu'),
    path('menu/add', views.add_menu, name='add_menu'),


    # AJAX
    path('cart/del/', views.delete),

    path('', views.landing, name='landing'),
    path('search_or_browse/', views.search_or_browse, name='search_or_browse'),
    path('search/', views.search, name='search'),
    path('browse/', views.browse, name='browse'),
    # path('menu/<int:menu_id>/options/', menu_options, name='menu_options'),
    # path('menu/<int:menu_id>/options/', views.menu_options, name='menu_options'),
    path('menu/<int:menu_id>/', views.menu_options, name='menu_detail'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('convert_speech_to_text/', views.convert_speech_to_text, name='convert_speech_to_text'),
    path('get_menu_id/', views.get_menu_id, name='get_menu_id'),
    # path('menu/<int:get_menu_id>/', views.get_menu_id, name='get_menu_id'),
    # path('menu_options/<int:menu_id>/', views.menu_options, name='menu_options'),
]