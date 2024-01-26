from django.shortcuts import render
from rest_framework import status
import mercadopago

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import PreferenceSerializer, ProductSerializer, OrderSerializer
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    
    orderItems = data['orderItems']
    
    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No hay productos'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
            user = user,
            paymentMethod = data['paymentMethod'],
            shippingPrice = data['shippingPrice'],
            totalPrice = data['totalPrice']
        )
        
        shipping = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            city = data['shippingAddress']['city'],
            postalCode = data['shippingAddress']['postalCode'],
            country = data['shippingAddress']['country']
        )
        
        for i in orderItems:
            product = Product.objects.get(_id=i['product'])
            
            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                qty = i['qty'],
                price = i['price'],
                image = product.image.url,
            )
            
            product.stock -= item.qty
            product.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
  
@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def getOrderById(request, pk):
    user = request.user
    
    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Sin autorización para ver pedido'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'El pedido no existe'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(_id=pk)
    
    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()
    return Response('Pedido pagado')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_preference(request):
    # Validar y serializar los datos de entrada
    serializer = PreferenceSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    # Crear la preferencia en MercadoPago
    sdk = mercadopago.SDK('TEST-5071062204606601-032018-a7d93d11744c451c0627b50e54760408-173592202')
    preference_response = sdk.preference().create({'items': data['items']})
    preference = preference_response["response"]

    # Devolver la preferencia generada
    return Response(preference)