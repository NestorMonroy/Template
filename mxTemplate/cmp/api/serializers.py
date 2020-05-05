from rest_framework import serializers
from cmp.models import Proveedor, Lead

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        exclude = ["timestamp", "edited", "user_account","user_modify"]


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
      model = Lead
      fields = '__all__s'
