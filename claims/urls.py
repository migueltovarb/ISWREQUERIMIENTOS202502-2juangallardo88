from django.urls import path
from . import views

app_name = "claims"

urlpatterns = [
    path("", views.index, name="index"),

    # Reclamos
    path("registrar/", views.register_claim, name="register"),
    path("reclamo/<int:pk>/", views.claim_detail, name="detail"),
    path("reclamo-publico/<int:pk>/", views.claim_detail_public, name="claim_detail_public"),
    path("mis-reclamos/", views.my_claims, name="my_claims"),
    path("buscar/", views.search_claim, name="search"),
    
    # Admin
    path("admin/lista/", views.admin_list, name="admin_list"),
    path("admin/actualizar-estado/<int:pk>/", views.update_claim_status, name="update_status"),
    path("admin/reportes/", views.admin_reports, name="admin_reports"),
    path("admin/actividades/", views.admin_activities, name="admin_activities"),
    
    # FAQs
    path("faqs/", views.faq_list, name="faq_list"),
    path("admin/faqs/", views.manage_faqs, name="manage_faqs"),
    path("admin/faqs/agregar/", views.add_faq, name="add_faq"),
    path("admin/faqs/<int:pk>/editar/", views.edit_faq, name="edit_faq"),
    path("admin/faqs/<int:pk>/eliminar/", views.delete_faq, name="delete_faq"),

    # Autenticación
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("registrarse/", views.user_register, name="user_register"),
]
