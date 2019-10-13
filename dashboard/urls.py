from . import views 
from django.urls import path


urlpatterns = [




    path('',views.index),
    path('get_data_transaction',views.get_data_transaction,name='getdata'),
    # path('get_data_pricedata',views.get_data_price,name='getprice'),
    # path('get_data_gtrends',views.get_data_gtrends,name='getgtrends'),
    # path('get_data_twittersentiments',views.get_data_twittersentiments,name='gettwittersenti'),
    # path('high_chart_twitter',views.get_data_twittersentiments_high_chart),
    # path('high-chart',views.high_chart,name='high-chart'),
]
