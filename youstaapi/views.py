from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions

from youstaapi.serializers import UserSerializer,ClothSerializer,CartSerializer,OrderSerializer,ReviewSerializer

from yousta.models import Cloths,ClothVarients,Carts,Orders

class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class ClothViews(ModelViewSet):
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ClothSerializer
    queryset=Cloths.objects.all()
    model=Cloths
   
    @action(methods=["post"],detail=True)
    def cart_add(self,request,*args,**kwargs):
        vid=kwargs.get("pk")
        varient_obj=ClothVarients.objects.get(id=vid)
        user=request.user
        serializer=CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(clothvarient=varient_obj,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

     
    @action(methods=["post"],detail=True)
    def place_order(self,request,*args,**kwargs):
        vid=kwargs.get("pk")
        varient_obj=ClothVarients.objects.get(id=vid)
        user=request.user
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(clothvarient=varient_obj,user=user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kwargs):
        c_id=kwargs.get("pk")
        cloth_obj=Cloths.objects.get(id=c_id)
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cloth=cloth_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
            
        

        
class CartView(ViewSet):
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=CartSerializer

    def list(self,request,*args,**kwargs):
        qs=Carts.objects.filter(user=request.user)
        serializer=CartSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Carts.objects.get(id=id).delete()
        return Response(data={"msg":"deleted"})
    


class OrderView(ViewSet):
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=Orders.objects.filter(user=request.user)
        serializer=OrderSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=Orders.objects.get(id=id).delete()
        return Response(data={"msg":"deleted"})

   
        

    


