from django.shortcuts import render
from django.contrib.auth.models import User
from api.serializers import UserSerializer, CakeSerializer, CartSerializer, OrderSerializer, ReviewSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from api.models import Cake, Cart, Order, Review, Occasion
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import IntegrityError
from rest_framework import status


class UserView(CreateModelMixin, GenericViewSet):

    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

class CakeView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    
    serializer_class = CakeSerializer
    

    def get_queryset(self):
        qs = Cake.objects.all()
        if 'occasion' in self.request.query_params:
            occ = self.request.query_params.get('occasion')
            print(occ)
            qs = qs.filter(occasion__name=occ)
        return qs
     

    @action(methods=['POST'], detail=True)
    def add_to_cart(self, request, *args, **kwargs):

        serialized_data = CartSerializer(data=request.data)
        cake_obj = Cake.objects.get(pk=kwargs.get('pk'))
        if serialized_data.is_valid():
            try:
                serialized_data.save(user=request.user, cake=cake_obj)
                return Response(data=serialized_data.data)
            except IntegrityError:
                print('Working')
                return Response({'error': 'This cake is already in your cart.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serialized_data.errors)
    

    @action(methods=['POST'], detail=True)
    def place_order(self, request, *args, **kwargs):
        serialized_data = OrderSerializer(data=request.data)
        if serialized_data.is_valid():
            cake_obj = Cake.objects.get(pk=kwargs.get('pk'))
            serialized_data.save(user=request.user, cake=cake_obj)
            return Response(data=serialized_data.data)
        return Response(data=serialized_data.errors)
    

    @action(methods=['POST'], detail=True)
    def add_review(self, request, *args, **kwargs):
        serialized_data = ReviewSerializer(data=request.data)
        if serialized_data.is_valid():
            cake_obj = Cake.objects.get(pk=kwargs.get('pk'))
            serialized_data.save(user=request.user, cake=cake_obj)
            return Response(data=serialized_data.data)
        return Response(data=serialized_data.errors)
    
    @action(methods=['GET'], detail=False)
    def get_occasion(self, request, *args, **kwargs):
        occasions_list = Occasion.objects.all().values_list('name', flat=True)
        return Response(data=occasions_list) 
    
    

class CartView(ListModelMixin, DestroyModelMixin, GenericViewSet):

    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    

class OrderView(ListModelMixin, GenericViewSet):

    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
