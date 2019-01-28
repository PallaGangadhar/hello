from django.conf.urls import url
from hello_world import views




url_patterns=[ 
    url(r'^$',views.index,name='index'),
    url(r'^accounts/register/$',
    views.MyRegistrationView.as_view(),
        name='registration_register'),
    
 ]