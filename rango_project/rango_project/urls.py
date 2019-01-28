"""rango_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,re_path
from django.conf.urls import url
from django.conf.urls import include
from hello_world import views
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView


urlpatterns = [

    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('about1/', views.about1, name='about1'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('search/', views.search, name='search'),
    path('createpost/', views.createpost, name='createpost'),
    path('student/', views.insert_student, name='student'),    
    path('add_category/',views.add_category,name='add_category'),
    re_path('category/(?P<category_name_slug>[\w\-]+)/$',views.show_category, name='show_category'),
    re_path('(?P<category_name_slug>[\w\-]+)/add_page/$',views.add_page, name='add_page'),
    re_path('(?P<category_name_slug>[\w\-]+)/edit_category/$',views.edit_category, name='edit_category'),
    path('register_profile/',views.register_profile,name='register_profile'),
        #path('register/',views.register,name='register'),
        # path('login/',views.user_login,name='login'),
        # path('logout/',views.user_logout,name='logout'),
    path('restricted/',views.restricted,name='restricted'),
   
    path('accounts/', include('registration.backends.simple.urls')),
    path('accounts/',views.MyRegistrationView.as_view(),name='registration_register'),
    path('goto/',views.track_url,name='goto'),
    path('register_profile/',views.register_profile,name='register_profile'),
    re_path('profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    path('profile_list/', views.profiles_list, name='profile_list'),
    path('likes/', views.like_category, name='like_category'),    
    path('suggest/', views.suggest_category, name='suggest_category'),
    path('auto_add/', views.auto_add_page, name='auto_add_page'),
    path('admin/', admin.site.urls),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

