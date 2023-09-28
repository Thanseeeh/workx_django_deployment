import stripe
from django.db.models import Sum
from decimal import Decimal
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Account
from .models import UserProfile, GigsOrder, TransactionHistory, Feedback
from .serializers import UserProfileSerializer, UserProfileListSerializer, GigsListingSerializer, GigDetailSerializer, GigsOrderSerializer, GigsOrderListSerializer, FeedbackSerializer
from superadmin.models import Category
from superadmin.serializers import CategorySerializer
from freelancers.models import FreelancerGigs, FreelancerProfile, FreelancerSkills, FreelancerEducation, FreelancerExperience
from freelancers.serializers import FreelancerProfileListSerializer, FreelancerSkillSerializer, FreelancerEducationSerializer, FreelancerExperienceSerializer, GigsSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


# UserProfile
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            user = Account.objects.get(email = request.user)
            user.is_profile = True
            user.save()
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# UserProfileListing
class UserProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profiles = UserProfile.objects.all()
        serializer = UserProfileListSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# UserProfileDetails
class AuthenticatedUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileListSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
    

# CategoryListing
class CategoryListView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# GigsListing
class GigsListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            gigs = FreelancerGigs.objects.all()
            serializer = GigsListingSerializer(gigs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Gigs not found'}, status=status.HTTP_404_NOT_FOUND)
        

# LocationListing
class LocationListView(APIView):
    def get(self, request, format=None):
        try:
            unique_states = FreelancerProfile.objects.values_list('state', flat=True).distinct()
            return Response({'states': list(unique_states)}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# SkillsListing
class SkillsListView(APIView):
    def get(self, request, format=None):
        try:
            unique_skills = FreelancerSkills.objects.values_list('skill', flat=True).distinct()
            return Response({'skills': list(unique_skills)}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# SingleViewOfGigs
class GigDetailView(APIView):
    def get(self, request, id):
        try:
            gig = FreelancerGigs.objects.get(id=id)
            serializer = GigDetailSerializer(gig)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FreelancerGigs.DoesNotExist:
            return Response({'message': 'Gig not found'}, status=status.HTTP_404_NOT_FOUND)


# FreelancerView
class FreelancerDetailView(APIView):
    def get(self, request, gig_owner_id):
        try:
            if gig_owner_id is not None:
                freelancer_profile = FreelancerProfile.objects.get(freelancer=gig_owner_id)
                serializer = FreelancerProfileListSerializer(freelancer_profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Gig owner not found'}, status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
            return Response({'message': 'Freelancer profile not found'}, status=status.HTTP_404_NOT_FOUND)
        

# FreelancerSkillView
class FreelancerSkillDetailView(APIView):
    def get(self, request, gig_owner_id):
        try:
            skills = FreelancerSkills.objects.filter(freelancer=gig_owner_id)
            serializer = FreelancerSkillSerializer(skills, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Skills not found'}, status=status.HTTP_404_NOT_FOUND)
        

# FreelancerEducationView
class FreelancerEducationDetailView(APIView):
    def get(self, request, gig_owner_id):
        try:
            education = FreelancerEducation.objects.filter(freelancer=gig_owner_id)
            serializer = FreelancerEducationSerializer(education, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Education not found'}, status=status.HTTP_404_NOT_FOUND)


# FreelancerExperienceView
class FreelancerExperienceDetailView(APIView):
    def get(self, request, gig_owner_id):
        try:
            experience = FreelancerExperience.objects.filter(freelancer=gig_owner_id)
            serializer = FreelancerExperienceSerializer(experience, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Experience not found'}, status=status.HTTP_404_NOT_FOUND)
        

# FreelancerGigView
class FreelancerGigDetailView(APIView):
    def get(self, request, gig_owner_id):
        try:
            gigs = FreelancerGigs.objects.filter(freelancer=gig_owner_id)
            serializer = GigsSerializer(gigs, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Gigs not found'}, status=status.HTTP_404_NOT_FOUND)
        

# GigOrderCreateView
class GigsOrderCreateView(APIView):
    def post(self, request, format=None):
        user = request.user
        gig_id = request.data.get('gig')

        try:
            gig = FreelancerGigs.objects.get(id=gig_id)
        except FreelancerGigs.DoesNotExist:
            return Response({'error': 'Gig not found'}, status=status.HTTP_404_NOT_FOUND)
        
        order_data = {
            'user': user.id,
            'freelancer': gig.freelancer.id,
            'gig': gig_id,
            'requirement': request.data.get('requirement'),
            'amount': request.data.get('amount'),
        }

        serializer = GigsOrderSerializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# GigOrderListView
class GigsOrderListView(APIView):
    def get(self, request):
        try:
            orders = GigsOrder.objects.filter(user=request.user)
            serializer = GigsOrderListSerializer(orders, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
           

# GigOrderStatusView
class GigsOrderStatusView(APIView):
    def get(self, request, order_id):
        try:
            order = GigsOrder.objects.get(id=order_id)
            serializer = GigsOrderListSerializer(order)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        

# CancelOrderView
class CancelOrderView(APIView):
    def put(self, request, order_id):
        try:
            order = GigsOrder.objects.get(id=order_id)

            if order.status not in ['Completed', 'Canceled']:
                reason = request.data.get('reason')
                order.status = 'Canceled'
                order.reason = reason
                order.save()

                serializer = GigsOrderListSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Order cannot be canceled.'}, status=status.HTTP_400_BAD_REQUEST)
        except GigsOrder.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


# DeleteOrderView
class DeleteOrderView(APIView):
    def delete(self, request, order_id):
        try:
            order = GigsOrder.objects.get(id=order_id)
            order.delete()
            return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except GigsOrder.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Failed to delete Order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)       


# StripePaymentIntegration
class StripeCheckoutView(APIView):
    def post(self, request, format=None):
        order_id = request.data.get('order_id')

        try:
            order = GigsOrder.objects.get(id=order_id)
            stripe.api_key = settings.STRIPE_SECRET_KEY

            commission_percentage = Decimal('0.035')
            commission = order.new_amount * commission_percentage
            total_amount = order.new_amount + commission

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'product_data': {
                                'name': order.gig.title,
                            },
                            'unit_amount': int(total_amount * 100),
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=settings.SITE_URL + '/order-status/?success=true',
                cancel_url=settings.SITE_URL + '/order-status/?canceled=true',
            )

            transaction = TransactionHistory.objects.create(
                amount=total_amount,
                commission=commission,
                total_amount=order.new_amount,
                order=order,
                user=request.user,
                freelancer=order.freelancer,
            )

            order.status = 'Payment Pending'
            order.save()

            return Response({
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'session_id': session.id,
            })
        except GigsOrder.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'error': 'Error creating Stripe Checkout Session'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# FeebackAndRatingView
class CreateFeedbackView(APIView):
    def post(self, request):
        gig_id = request.data.get('gig_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        
        gig = FreelancerGigs.objects.get(id=gig_id)
        user = request.user

        feedback = Feedback.objects.create(
            gig=gig,
            user=user,
            rating=rating,
            comment=comment
        )
        
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# DisplayFeedbackAndRatingView
class DisplayFeedbackView(APIView):
    def get(self, request, gig_id):
        try:
            feedback_entries = Feedback.objects.filter(gig__id=gig_id)
            serializer = FeedbackSerializer(feedback_entries, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Feedback.DoesNotExist:
            return Response({'message': 'Feedback not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Failed to Display Feedback'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        

# TotalSpendingView
class TotalAmountSpentView(APIView):
    def get(self, request):
        try:
            total_amount_spent = TransactionHistory.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum']

            if total_amount_spent is None:
                total_amount_spent = 0

            return Response({'total_amount_spent': total_amount_spent}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)