from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Account
from freelancers.models import FreelancerProfile, FreelancerGigs
from freelancers.serializers import TransactionHistorySerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CategorySerializer
from .models import Category
from users.models import GigsOrder, TransactionHistory
from users.serializers import GigsListingSerializer
import logging

logger = logging.getLogger(__name__)

# Create your views here.


class BlockUnBlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            instance = Account.objects.get(id=user_id)
            instance.is_active = not instance.is_active
            instance.save()

            return Response({"message": "User status changed"}, status=status.HTTP_200_OK)
        
        except Account.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

class BlockUnBlockFreelancerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            instance = Account.objects.get(id=user_id)
            instance.is_active = not instance.is_active
            instance.save()

            return Response({"message": "User status changed"}, status=status.HTTP_200_OK)
        
        except Account.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

class RegisterFreelancerView(APIView):

    def post(self, request, user_id):
        try:
            instance = FreelancerProfile.objects.get(freelancer_id=user_id)
            instance.is_registered = True
            instance.save()

            return Response({"message": "Freelancer Registered"}, status=status.HTTP_200_OK)
        
        except Account.DoesNotExist:
            return Response({"message": "Freelancer not found"}, status=status.HTTP_404_NOT_FOUND)
        

class AddCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            category = serializer.save(is_active=True)
            return Response({"message": "Category created successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class BlockUnBlockCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, cat_id):
        try:
            instance = Category.objects.get(id=cat_id)
            instance.is_active = not instance.is_active
            instance.save()

            return Response({"message": "Category status changed"}, status=status.HTTP_200_OK)
        
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


class AdminGigsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            gigs = FreelancerGigs.objects.all()
            serializer = GigsListingSerializer(gigs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Gigs not found'}, status=status.HTTP_404_NOT_FOUND)
        

class OrderStatusCount(APIView):
    def get(self, request):
        try:
            pending_orders = GigsOrder.objects.filter(status='Pending').count()
            accepted_orders = GigsOrder.objects.filter(status='Accepted').count()
            started_orders = GigsOrder.objects.filter(status='Work Started').count()
            completed_orders = GigsOrder.objects.filter(status='Completed').count()
            payment_orders = GigsOrder.objects.filter(status='Payment Pending').count()
            closed_orders = GigsOrder.objects.filter(status='Deal Closed').count()

            return Response({
                'pending_orders': pending_orders,
                'accepted_orders': accepted_orders,
                'started_orders': started_orders,
                'completed_orders': completed_orders,
                'payment_orders': payment_orders,
                'closed_orders': closed_orders,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AccountCount(APIView):
    def get(self, request):
        try:
            freelancer = Account.objects.filter(user_type=2).count()
            users = Account.objects.filter(user_type=3).count()

            return Response({
                'freelancer': freelancer,
                'users': users,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AdminTransactionHistory(APIView):
    def get(self, request):
        try:
            transactions = TransactionHistory.objects.all()
            serializer = TransactionHistorySerializer(transactions, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)