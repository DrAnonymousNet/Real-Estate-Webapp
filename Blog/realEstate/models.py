import datetime

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=160)
    address = models.TextField(max_length=50)
    featured = models.BooleanField(blank=True, null=True)
    phone_number = models.IntegerField(blank= True, verbose_name='Phone Number', null=True)
    profile_picture = models.ImageField(upload_to="profile_picture", blank=True, null=True, default="default.jpg")

    def get_fullname(self):
        fullname = str(self.user.first_name) +" "+ str(self.user.last_name)
        return fullname

    def __str__(self):
        return f'{self.user}'

    def get_absolute_url(self):
        return reverse("agent_property_list", kwargs={"id":self.id})



class Images(models.Model):
    picture = models.ImageField(upload_to='house_image', verbose_name='Picture', blank=False)

    def __str__(self):
        return self.picture.name

class Amenity(models.Model):
    name = models.CharField(verbose_name='Amenity', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Amenities'

class Property(models.Model):
    OPTIONS = [
        ("Rent", "Rent"),
        ("Sale", "Sale"),
        ("Lease", "Lease"),
    ]

    property_name = models.CharField(verbose_name='Property Name', max_length=50, blank=False)
    price = models.DecimalField(verbose_name='Price', decimal_places=2, blank=False, max_digits=99999999999)
    property_description = models.TextField(verbose_name='Description', max_length=160)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    date_listed = models.DateField(auto_now_add=True, blank=True)
    state = models.CharField(max_length=20, blank=True,default="Kwara")
    city = models.CharField(max_length=20, blank=True, default= "Ilorin")
    area = models.CharField(max_length=50, blank=True, default="Tanke")
    address = models.CharField(max_length=50, blank=True, default="36, MFM Junction")
    status = models.CharField(choices=OPTIONS, max_length=10)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, editable=False)
    image = models.ManyToManyField(Images)
    amenity = models.ManyToManyField(Amenity)
    no_of_plots = models.IntegerField(verbose_name="Plots", blank=True, default=2)

    class Meta:
        abstract = True
        ordering = ["date_listed"]


class Land(Property):

    def get_absolute_url(self):
        return reverse("property_detail", kwargs = {"id":self.id})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.property_name)
        super(House, self).save(*args, **kwargs)


class House(Property):
    no_of_bedroom = models.PositiveIntegerField(verbose_name="Bed")
    no_of_bathroom = models.PositiveIntegerField(verbose_name="Bathroom", default=1, blank=True)

    def get_absolute_url(self):
        return reverse("property_detail", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.property_name)
        super(House, self).save(*args, **kwargs)

    def __str__(self):
        return self.property_name




