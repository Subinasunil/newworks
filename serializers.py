from rest_framework import serializers
from productapi.models import Product
class ProductSerializers(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    name=serializers.CharField()
    category=serializers.CharField()
    price=serializers.IntegerField()
    rating=serializers.FloatField()

    def validate(self,data):
        price=data.get("price")
        if price<0:
            raise serializers.ValidationError("invalid price")
        else:
            return data


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
