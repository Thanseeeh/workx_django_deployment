from django.db import models
from accounts.models import Account
from superadmin.models import Category

# Create your models here.


class FreelancerProfile(models.Model):

    FREELANCER_STATUS = [
        ('fresher', 'fresher'),
        ('intermediate', 'intermediate'),
        ('professional', 'professional')
    ]
    freelancer = models.ForeignKey(Account, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile', blank=True, null=True)
    title = models.CharField(max_length=20, blank=True)
    about = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True) 
    level = models.CharField(default='fresher', choices=FREELANCER_STATUS, max_length=20)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    year_of_experience = models.PositiveIntegerField(null=True, blank=True, default=0)
    age = models.PositiveIntegerField(blank=True, null=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.freelancer)
    

class FreelancerSkills(models.Model):
    skill = models.CharField(max_length=50, blank=True, unique=True)
    freelancer = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.skill)


class FreelancerExperience(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=True)
    company = models.CharField(max_length=50, blank=True)
    year = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    freelancer = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)
    

class FreelancerEducation(models.Model):
    course = models.CharField(max_length=50, unique=True, blank=True)
    college = models.CharField(max_length=50, blank=True)
    year = models.CharField(max_length=10, blank=True)
    freelancer = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.course)
    

class FreelancerGigs(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='category')
    description = models.TextField(blank=True)
    starting_price = models.PositiveIntegerField(blank=True, null=True)
    delivery_time = models.CharField(max_length=20, blank=True, null=True)
    available_requirements = models.TextField(blank=True, help_text="Enter each requirement on a new line.")
    tags = models.CharField(max_length=255, blank=True, help_text="Enter tags separated by commas (e.g., tag1, tag2).")
    image1 = models.ImageField(upload_to='gigs', null=True, blank=True)
    image2 = models.ImageField(upload_to='gigs', null=True, blank=True)
    image3 = models.ImageField(upload_to='gigs', null=True, blank=True)
    freelancer = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title