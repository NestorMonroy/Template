from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProveedorView,ProveedorNew, ProveedorEdit, proveedorInactivar
from cmp.api import views as cv


router = DefaultRouter()
router.register(r"cmp", cv.ProveedorViewSet, 'cmp'), 

urlpatterns = [
    path("", include(router.urls)), 

    # path("questions/<slug:slug>/answers/", 
    #      qv.AnswerListAPIView.as_view(),
    #      name="answer-list"),

    # path("questions/<slug:slug>/answer/", 
    #      qv.AnswerCreateAPIView.as_view(),
    #      name="answer-create"),

    # path("answers/<int:pk>/", 
    #      qv.AnswerRUDAPIView.as_view(),
    #      name="answer-detail"),

    # path("answers/<int:pk>/like/", 
    #      qv.AnswerLikeAPIView.as_view(),
    #      name="answer-like")
]

# urlpatterns = [
#     path('proveedores/',ProveedorView.as_view(), name="proveedor_list"),
#     path('proveedores/new',ProveedorNew.as_view(), name="proveedor_new"),
#     path('proveedores/edit/<int:pk>',ProveedorEdit.as_view(), name="proveedor_edit"),
#     path('proveedores/inactivar/<int:id>',proveedorInactivar, name="proveedor_inactivar"),


# ]