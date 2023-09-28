from rest_framework import serializers
from accounts.models import Account
from accounts.serializers import UserViewSerializer
from users.models import TransactionHistory, GigsOrder
from .models import FreelancerProfile, FreelancerSkills, FreelancerExperience, FreelancerEducation, FreelancerGigs


class FreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'is_verified', 'is_active']


class FreelancerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerProfile
        exclude = ('freelancer',)


class FreelancerProfileListSerializer(serializers.ModelSerializer):
    freelancer = FreelancerSerializer()

    class Meta:
        model = FreelancerProfile
        fields = '__all__'


class FreelancerSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerSkills
        fields = '__all__'


class FreelancerEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerEducation
        fields = '__all__'


class FreelancerExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerExperience
        fields = '__all__'


class GigsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerGigs
        fields = '__all__'


class FreelancerGigsOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GigsOrder
        fields = ['id', 'gig']


class GigsCountSerializer(serializers.Serializer):
    total_gigs = serializers.IntegerField()
    active_gigs = serializers.IntegerField()
    inactive_gigs = serializers.IntegerField()


class TransactionHistorySerializer(serializers.ModelSerializer):
    user = FreelancerSerializer()
    freelancer = FreelancerSerializer()
    order = serializers.SerializerMethodField()

    class Meta:
        model = TransactionHistory
        fields = '__all__'

    def get_order(self, obj):
        return {
            'id': obj.order.id,
            'gig_title': obj.order.gig.title if obj.order.gig else None,
        }