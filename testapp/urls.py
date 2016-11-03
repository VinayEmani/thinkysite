from django.conf.urls import url

from . import models
from . import views 

urlpatterns = [
    url(r'^$', views.homepage, name='testapp-root'),
    url(r'^home/', views.homepage, name='testapp-homepage'),
    url(r'^profile/', views.profilepage, name='testapp-profilepage'),
    url(r'^signup/$', views.signup, name='testapp-signup'),
    url(r'^signuppage/$', views.signuppage, name='testapp-signup-page'),
    url(r'^login/', views.login_user, name='testapp-user-login'),
    url(r'^loginpage/', views.loginpage, name='testapp-user-loginpage'),
    url(r'^logout/$', views.logout_user, name='testapp-user-logout'),
    url(r'^logoutpage/$', views.logoutpage, name='testapp-user-logoutpage'),
]
