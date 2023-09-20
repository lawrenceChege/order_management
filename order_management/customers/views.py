from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view

from base.backend.serializers import GroupSerializer, UserSerializer
from customers.backend.seriallizers import CustomerSerializer
from customers.models import Customer

# views.py
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .backend.customer_base import CustomerBase
from .models import Customer


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        # Handle user registration, create User record, and authenticate the user
        customer = CustomerBase().add_customer(request)
        user = customer.get("user")
        
        # Log in the user
        login(request, user)
        
        return redirect('dashboard')  # Redirect to the user's dashboard or profile page
    
    return render(request, 'registration/register.html')  # Display registration form


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be viewed or edited.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
