from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import stripe
from .models import *
from rest_framework.permissions import AllowAny
from rest_framework import status, viewsets
from drf_spectacular.utils import extend_schema
from .serializers import *
from .utils import order_line_items
from django.db.models import Prefetch
from os import getenv

class BuyItemView(APIView):

    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        session = stripe.checkout.Session.create(
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item.title,
                        "description": item.description
                    },
                    "unit_amount": item.price

                },
                "quantity": 1
            }],
            mode="payment",
            success_url= 'http://localhost:4000/',
            cancel_url= 'http://localhost:4000/'

        )

        return Response({"session_id": session.id}, status=status.HTTP_200_OK)
    
class BuyOrderView(APIView):
    def get(self, request, order_id):
        order = Order.objects.prefetch_related(Prefetch(
        'orderitem_set',
        queryset=OrderItem.objects.select_related('item'),
        to_attr='items_in_order'
        )).get(pk=order_id)
        if order.paid == True:
            return Response({"msg": "The order has already been paid for"})
        line_items = order_line_items(order)
        
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            success_url= f'http://paid/{order_id}',
            cancel_url= '/'
            
        )
        
        
        return Response({"session_id": session.id})
        
class OrderPaidView(APIView):
    def get(self, request, order_id):
        session_id = request.query_params.get('session_id')
        order = Order.objects.get(pk=order_id)
        
        if not session_id:
            return Response(
                {"error": "Missing session_id parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status != 'paid' or session.metadata.get('order_id') != str(order_id):
                return Response(
                    {"error": "Payment verification failed"},
                    status=status.HTTP_403_FORBIDDEN
                )

            if not order.paid:
                order.paid = True
                order.save()
                return redirect('/')
            
        except stripe.error.StripeError:
            return Response(
                {"error": "Payment verification failed"},
                status=status.HTTP_403_FORBIDDEN
            )

class ItemViewSet(viewsets.ViewSet):
    
    @extend_schema(request=ItemCreateSerializer)
    def create(self, request):
        serializer = ItemCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        new_item = serializer.save()
        return Response({"item_id": new_item.id}, status=status.HTTP_201_CREATED)
    
    @extend_schema(request=ItemSerializer)
    def retrieve(self, request, pk):
        try:
            stripe_public_key = getenv("STRIPE_PUBLIC_KEY")
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item)
            return render(request, 'stripe_test_app/item_detail.html', {'item': serializer.data, "item_id":pk, "public_key": stripe_public_key})
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "The ID must be a number"}, status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(exclude=True)
    def update(self, request, pk=None):
        return Response(
            {"error": "Method Not Allowed"}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @extend_schema(exclude=True)
    def partial_update(self, request, pk=None):
        return Response(
            {"error": "Method Not Allowed"}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @extend_schema(exclude=True)
    def destroy(self, request, pk=None):
        return Response(
            {"error": "Method Not Allowed"}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
        
class OrderViewSet(viewsets.ViewSet):
    @extend_schema(request=OrderCreateSerializer)
    def create(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        new_order = serializer.save()
        return Response({"order_id": new_order.id}, status=status.HTTP_201_CREATED)   

    @extend_schema(request=OrderDetailSerializer)
    def retrieve(self, request, pk):
        try:
            stripe_public_key = getenv("STRIPE_PUBLIC_KEY")
            order = Order.objects.get(pk=pk)
            serializer = OrderDetailSerializer(order)
            order_total = sum(
            item['item']['price'] * item['quantity'] 
            for item in serializer.data['items']
        )
            return render(request, 'stripe_test_app/order_detail.html', {
            'order': serializer.data,
            'order_id': pk,
            'order_total': order_total,
            "public_key": stripe_public_key})
        except Order.DoesNotExist:
            return Response({"error": "Ordet not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "The ID must be a number"}, status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(exclude=True)
    def update(self, request, pk=None):
        return Response(
            {"error": "Method Not Allowed"}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @extend_schema(exclude=True)
    def partial_update(self, request, pk=None):
        return Response(
            {"error": "Method Not Allowed"}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @extend_schema(exclude=True)
    def destroy(self, request, pk=None):
        return Response(
            {"error": "Method Not Allowed"}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
