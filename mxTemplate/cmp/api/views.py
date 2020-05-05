from rest_framework import generics, status, viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from django.shortcuts import render,redirect
from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from cmp.api.serializers import ProveedorSerializer, LeadSerializer

from cmp.forms import ProveedorForm, ComprasEncForm
from cmp.models import Proveedor

# Create your views here.



class ProveedorViewSet(viewsets.ModelViewSet):
    """Provide CRUD +L functionality for Proveedor."""
    queryset = Proveedor.objects.all().order_by("-timestamp")
    permission_classes = [
      permissions.AllowAny
    ]
    serializer_class = ProveedorSerializer

    

class ProveedorView(LoginRequiredMixin, generic.ListView):
    model = Proveedor
    template_name = "cmp/proveedor_list.html"
    context_object_name = "obj"
    login_url = "login"

class ProveedorNew(LoginRequiredMixin, generic.CreateView):
    model=Proveedor
    template_name="cmp/proveedor_form.html"
    context_object_name = "obj"
    form_class=ProveedorForm
    success_url=reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Nuevo"
    login_url = "login"
    
    def form_valid(self, form):
        form.instance.user_account = self.request.user
        return super().form_valid(form)


class ProveedorEdit(LoginRequiredMixin, generic.UpdateView):
    model=Proveedor
    template_name="cmp/proveedor_form.html"
    context_object_name = "obj"
    form_class=ProveedorForm
    success_url=reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Editado"
    login_url = "login"
    
    def form_valid(self, form):
        form.instance.user_modify = self.request.user.id
        print(form)
        print("de")
        return super().form_valid(form)

@login_required(login_url='/login/')
def proveedorInactivar(request,id):
    template_name='cmp/inactivar_prv.html'
    contexto={}
    prv = Proveedor.objects.filter(pk=id).first()

    if not prv:
        return HttpResponse('Proveedor no existe ' + str(id))

    if request.method=='GET':
        contexto={'obj':prv}

    if request.method=='POST':
        prv.estado=False
        prv.save()
        contexto={'obj':'OK'}
        return HttpResponse('Proveedor Inactivado')

    return render(request,template_name,contexto)