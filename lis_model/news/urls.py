from django.urls import path
from django.contrib.auth.views import LoginView
from .views import index,zap_consult,tvor,volon_naprav,trud_naprav,sec,deletepost,detail_v,otpisv, otpisgv,zapisgv,create,create_v,zapisv, zapis,zapisg,otpis,otpisg,cult,consult,otz, mass,sport,trud, POSTLoginView, profile, POSTLogoutView, ChangeUserInfoView, POSTChangeView, RegisterUserView, RegisterDoneView, user_activate, DeleteUserView, detail

app_name = 'news'

urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>/', detail, name='detail'),
    path('v/<int:pk>/', detail_v, name='detail_v'),
    path('cult/', cult, name='cult'),
    path('mass/', mass, name='mass'),
    path('sport/', sport, name='sport'),
    path('trud/', trud, name='trud'),
    path('consult/', consult, name='consult'),
    path('otz/', otz, name='otz'),
    path('sec/<int:pk>/', sec, name='sec'),
    path('tvor/<int:pk>/', tvor, name='tvor'),
    path('volon_naprav/<int:pk>/', volon_naprav, name='volon_naprav'),
    path('trud_naprav/<int:pk>/', trud_naprav, name='trud_naprav'),
    path('zapis_consult/<int:pk>/', zap_consult, name='zap_consult'),
    path('zapis/<int:pk>/', zapis, name='zapis'),
    path('zapisv/<int:pk1>/<int:pk2>', zapisv, name='zapisv'),
    path('zapisg/<int:pk>/', zapisg, name='zapisg'),
    path('zapisgv/<int:pk1>/<int:pk2>', zapisgv, name='zapisgv'),
    path('otpis/<int:pk>/', otpis, name='otpis'),
    path('otpisv/<int:pk1>/<int:pk2>', otpisv, name='otpisv'),
    path('otpisg/<int:pk>/', otpisg, name='otpisg'),
    path('otpisgv/<int:pk1>/<int:pk2>', otpisgv, name='otpisgv'),
    path('add/', create, name='add'),
    path('add_v/', create_v, name='add_v'),
    path('register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('register/done', RegisterDoneView.as_view(), name='register_done'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', POSTLoginView.as_view(), name='login'),
    path('logout/', POSTLogoutView.as_view(), name='logout'),
    path('profile/delete', DeleteUserView.as_view(), name='profile_delete'),
    path('profile/', profile, name='profile'),
    path('profile/change', ChangeUserInfoView.as_view(), name='profile_change'),
    path('profile/password/change', POSTChangeView.as_view(), name='password_change'),  
    path('profile/deletepost/<int:pk>/', deletepost, name='delete_post'), 
]
