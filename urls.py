from django.urls import path, include

from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.home, name='home'),
    
    # --- urls para autenticación --- #
    # path('usuarios/', include('django.contrib.auth.urls')),

    # accounts/ login/ [name='login']
    path('usuario/login/', views.UsuarioLoginView.as_view(), name='login'),
    # accounts/ logout/ [name='logout']
    path('usuario/logout/', views.UsuarioLogoutView.as_view(), name='logout'),
    # accounts/ password_reset/ [name='password_reset']
    path('usuario/reset/', views.UsuarioPasswordResetView.as_view(), name='password_reset'),
    # accounts/ password_reset/done/ [name='password_reset_done']
    path('usuario/reset/done/', views.UsuarioPasswordResetDoneView.as_view(), name='password_reset_done'),
    # accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    path('usuario/reset/confirmacion/<uidb64>/<token>/', views.UsuarioPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # accounts/ reset/done/ [name='password_reset_complete']
    path('usuario/reset/exitoso/', views.UsuarioPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # accounts/ password_change/ [name='password_change']
    path('usuario/cambiar_contrasena/', views.UsuarioPasswordChangeView.as_view(), name='password_change'),
    # accounts/ password_change/done/ [name='password_change_done']
    
    path('usuario/perfil/', views.PerfilTemplateView.as_view(), name='perfil'),
    path('usuario/actualizar/', views.PerfilUpdateView.as_view(), name='actualizar'),
    path('usuario/nuevo/', views.UsuarioCreateView.as_view(), name='crear'),
    path('usuario/listado/', views.UsuarioListView.as_view(), name='listar'),
    path('usuario/actualizar/<uuid:pk>/', views.UsuarioUpdateView.as_view(), name='actualizar'),
    path('usuario/detail/<uuid:pk>/', views.UsuarioDetailView.as_view(), name='detail_user'),
]


    
    
    