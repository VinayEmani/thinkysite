from django.conf.urls import url
from django.conf.urls.static import static

from . import models
from . import views 

urlpatterns = [
    url(r'^$', views.homepage, name='testapp-root'),
    url(r'^home/', views.homepage, name='testapp-homepage'),
    url(r'^profile/', views.profilepage, name='testapp-profilepage'),
    url(r'^board/', views.board, name='testapp-board'),
    url(r'^forum/', views.forumpage, name='testapp-forumpage'),
    url(r'^mod/board/', views.modboard, name='testapp-mod-board'),
    url(r'^mod/forum/', views.modforum, name='testapp-mod-forum'),
    url(r'^newthread/', views.newthread, name='testapp-newthread'),
    url(r'^createthread/', views.createthread, name='testapp-createthread'),
    url(r'^mod/', views.modpage, name='testapp-modpage'),
    url(r'^addnewmod/', views.addnewmod, name='testapp-add-mod'),
    url(r'^deloldmod/', views.deloldmod, name='testapp-del-mod'),
    url(r'^curmodlist/', views.curmodlist, name='testapp-cur-mod-list'),
    url(r'^boardlist/', views.getboards, name='testapp-get-boards'),
    url(r'profileupdate/', views.profile_update, name='testapp-profileupdate'),
    url(r'userupdate/', views.user_data_update, name='testapp-userdataupdate'),
    url(r'^signup/$', views.signup, name='testapp-signup'),
    url(r'^signuppage/$', views.signuppage, name='testapp-signup-page'),
    url(r'^login/', views.login_user, name='testapp-user-login'),
    url(r'^loginpage/', views.loginpage, name='testapp-user-loginpage'),
    url(r'^logout/$', views.logout_user, name='testapp-user-logout'),
    url(r'^logoutpage/$', views.logoutpage, name='testapp-user-logoutpage'),
]
