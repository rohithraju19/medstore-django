from rest_framework import serializers
from medicine.models import Medicine

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['name','price','quantity']