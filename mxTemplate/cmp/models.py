from django.db import models
from django.db.models.signals import post_save, post_delete

from mxTemplate.abstract_models import DefaultBasicModelSec
# Create your models here.

class Proveedor(DefaultBasicModelSec):
    descripcion=models.CharField(max_length=100,unique=True)
    direccion=models.CharField(max_length=250,null=True, blank=True)
    contacto=models.CharField(max_length=100)
    telefono=models.CharField(max_length=10,null=True, blank=True)
    email=models.CharField(max_length=250,null=True, blank=True)

    # def __str__(self):
    #     return '{}'.format(self.descripcion)

    # def save(self):
    #     self.descripcion = self.descripcion.upper()
    #     super(Proveedor, self).save()

    class Meta:
        verbose_name_plural = "Proveedores"


class ComprasEnc(DefaultBasicModelSec):
    fecha_compra=models.DateField(null=True,blank=True)
    observacion=models.TextField(blank=True,null=True)
    no_factura=models.CharField(max_length=100)
    fecha_factura=models.DateField()
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)

    proveedor=models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}'.format(self.observacion)

    def save(self):
        self.observacion = self.observacion.upper()
        self.total = self.sub_total - self.descuento
        super(ComprasEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado Compras"
        verbose_name="Encabezado Compra"

class ComprasDet(DefaultBasicModelSec):
    compra=models.ForeignKey(ComprasEnc,on_delete=models.CASCADE)
    producto=models.CharField(max_length=100)
    cantidad=models.BigIntegerField(default=0)
    precio_prv=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)
    costo=models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.producto)

    def save(self):
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio_prv))
        self.total = self.sub_total - float(self.descuento)
        super(ComprasDet, self).save()
    
    class Mega:
        verbose_name_plural = "Detalles Compras"
        verbose_name="Detalle Compra"


class Lead(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField(max_length=100, unique=True)
  message = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
