from rest_framework import serializers
from accounts.models import Account
from accounts.serializers import UserViewSerializer
from superadmin.serializers import CategorySerializer
from freelancers.serializers import FreelancerSerializer
from freelancers.models import FreelancerGigs, FreelancerProfile
from .models import UserProfile, GigsOrder, Feedback


# User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'is_verified', 'is_active']


# UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('user',)


# UserProfileListing
class UserProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'


# GigsListing
class GigsListingSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    freelancer = FreelancerSerializer()
    class Meta:
        model = FreelancerGigs
        fields = '__all__'


# GigSingleView
class GigDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    freelancer = FreelancerSerializer()
    freelancer_profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = FreelancerGigs
        fields = '__all__'

    def get_freelancer_profile_photo(self, obj):
        try:
            freelancer_profile = FreelancerProfile.objects.get(freelancer=obj.freelancer)
            return freelancer_profile.profile_photo.url
        except FreelancerProfile.DoesNotExist:
            return None


# GigOrder
class GigsOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GigsOrder
        fields = '__all__'


# GigsOrderList
class GigsOrderListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    freelancer = serializers.SerializerMethodField()
    gig = serializers.SerializerMethodField()

    class Meta:
        model = GigsOrder
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
        }

    def get_freelancer(self, obj):
        freelancer = obj.freelancer
        return {
            'id': freelancer.id,
            'username': freelancer.username,
            'first_name': freelancer.first_name,
            'last_name': freelancer.last_name,
        }

    def get_gig(self, obj):
        gig = obj.gig
        return {
            'id': gig.id,
            'title': gig.title,
            'description': gig.description,
            'image1': gig.image1.url,
            'delivery_time': gig.delivery_time,
        }
    

# FeedbackAndRating
class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user_profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = '__all__'

    def get_user_profile_photo(self, obj):
        try:
            user_profile = UserProfile.objects.get(user=obj.user)
            return user_profile.profile_photo.url
        except UserProfile.DoesNotExist:
            return None