from django.urls import path

from . import views


urlpatterns = [
    path("", views.inicio, name="inicio_clinica"),

    path("api/mascotas/", views.api_mascotas, name="api_mascotas"),
    path("api/mascotas/<int:pk>/",views.detalle_mascota,name="detalle_mascota"),

    path("api/propietarios/",views.api_propietarios,name="api_propietarios"),

    path("api/consultas/",views.api_consultas,name="api_consultas"),
    
    path("api/perfil/", views.perfil, name="api_perfil"),
    
    path("api/estadisticas/", views.estadisticas, name="api_estadisticas"),
    
    path("api/sesion/", views.contador_sesion, name="contador_sesion"),
]