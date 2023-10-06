from django.urls import path, include

from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.home, name='home'),
    
    # --- urls para autenticación --- #
    # path('usuarios/', include('django.contrib.auth.urls')),

    # accounts/ login/ [name='login']
    path('usuarios/login/', views.UsuarioLoginView.as_view(), name='login'),
    # accounts/ logout/ [name='logout']
    path('usuarios/logout/', views.UsuarioLogoutView.as_view(), name='logout'),
    # accounts/ password_reset/ [name='password_reset']
    path('usuarios/reset/', views.UsuarioPasswordResetView.as_view(), name='password_reset'),
    # accounts/ password_reset/done/ [name='password_reset_done']
    path('usuarios/reset/done/', views.UsuarioPasswordResetDoneView.as_view(), name='password_reset_done'),
    # accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    path('usuarios/reset/confirmacion/<uidb64>/<token>/', views.UsuarioPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # accounts/ reset/done/ [name='password_reset_complete']
    path('usuarios/reset/exitoso/', views.UsuarioPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # accounts/ password_change/ [name='password_change']
    path('usuarios/cambiar_contrasena/', views.UsuarioPasswordChangeView.as_view(), name='password_change'),
    # accounts/ password_change/done/ [name='password_change_done']
    
    path('usuarios/perfil/', views.UsuarioPerfil.as_view(), name='perfil'),
    path('usuarios/actualizar/', views.UsuarioActualizar.as_view(), name='actualizar'),
    path('usuarios/nuevo/', views.UsuarioNuevoFormView.as_view(), name='crear'),
    path('usuarios/listado/', views.UsuarioListView.as_view(), name='listar'),
    path('usuarios/actualizar/<uuid:pk>/', views.UsuarioUpdateView.as_view(), name='actualizar'),
]


    
    
    