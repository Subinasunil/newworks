from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from productapi.models import Product
from serializers import ProductSerializers,ProductModelSerializer
from rest_framework import status
from rest_framework.viewsets import ViewSet

class ProductsView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Product.objects.all()
        serializers=ProductSerializers(qs,many=True)
        return Response(data=serializers.data,status=status.HTTP_200_OK)
    def post(self,request,*args,**kwargs):
        serializers=ProductSerializers(data=request.data)
        if serializers.is_valid():
            Product.objects.create(**serializers.validated_data)
            return Response(data=serializers.data,status=status.HTTP_201_CREATED)
        else:
            return  Response(data=serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Product.objects.get(id=id)
        serializers=ProductSerializers(qs)
        return Response(data=serializers.data,status=status.HTTP_200_OK)
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        instance=Product.objects.filter(id=id)
        serializers=ProductSerializers(data=request.data)
        if serializers.is_valid():
            # instance.name=serializers.validated_data.get("name")
            # instance.category=serializers.validated_data.get("category")
            # instance.price=serializers.validated_data.get("price")
            # instance.rating = serializers.validated_data.get("rating")
            # instance.save()
            instance.update(**serializers.validated_data)
            return Response(data=serializers.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        instance=Product.objects.get(id=id)
        serializers=ProductSerializers(instance)
        instance.delete()
        return Response({"msg:deleted"},status=status.HTTP_204_NO_CONTENT)

class ProductModelView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Product.objects.all()
        if "category" in request.query_params:
            qs=qs.filter(category__contains=request.query_params.get("category"))
        if "price_gt" in request.query_params:
            qs=qs.filter(price__gte=request.query_params.get("price_gt"))
        serializer=ProductModelSerializer(qs,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def post(self,request,*args,**kwargs):
        serializer=ProductModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.data,status=status.HTTP_400_BAD_REQUEST)


class ProductDetailModelView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Product.objects.get(id=id)
        serializer=ProductModelSerializer(qs)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        object=Product.objects.get(id=id)
        serializer=ProductModelSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        instance=Product.objects.get(id=id)
        instance.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)



class ProductViewSetView(ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Product.objects.all()
        serializer=ProductModelSerializer(qs,many=True)
        return Response(data=serializer.data)

    def create(self,request,*args,**kwargs):
        serializer=ProductModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Product.objects.get(id=id)
        serializer=ProductModelSerializer(qs)
        return Response(data=serializer.data)

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Product.objects.get(id=id)
        serializer=ProductModelSerializer(instance=object,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=Product.objects.get(id=id)
        instance.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)




