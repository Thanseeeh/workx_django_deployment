from django.db import models
from accounts.models import Account
from freelancers.models import FreelancerGigs

# Create your models here.


# Profile
class UserProfile(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profle picture', default='profile/profile.jpg')
    about = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True) 
    state = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.user)
    

# Gigs Order
class GigsOrder(models.Model):
    requirement = models.TextField(blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    new_amount = models.PositiveIntegerField(blank=True, null=True)
    total_amount = models.PositiveIntegerField(blank=True, null=True)
    gig = models.ForeignKey(FreelancerGigs, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user')
    freelancer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='freelancer')
    status = models.CharField(max_length=30, default='Pending')
    reason = models.TextField(blank=True)
    order_raw_images = models.ImageField(upload_to='order raw', blank=True, null=True)
    uploaded_file = models.FileField(upload_to='uploaded_files/', blank=True, null=True)


# Transaction History
class TransactionHistory(models.Model):
    amount = models.PositiveIntegerField(blank=True, null=True)
    commission = models.PositiveIntegerField(blank=True, null=True)
    total_amount = models.PositiveIntegerField(blank=True, null=True)
    order = models.ForeignKey(GigsOrder, on_delete=models.CASCADE, related_name='order')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='users')
    freelancer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='freelancers')


# Feedback
class Feedback(models.Model):
    gig = models.ForeignKey(FreelancerGigs, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)