from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Land, House, Images, Amenity, Agent


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ["property_name", "price", "status", "address","area","no_of_bedroom", ]


class LandForm(forms.ModelForm):
    class Meta:
        model = Land
        fields = ["property_name", "price", "status", "address", "image", "no_of_plots"]


class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['picture']


class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = ["name"]


class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        exclude = ["featured", "user"]

    def clean(self, *args, **kwargs):
        phone_number = self.cleaned_data.get("phone_number")
        if str(phone_number).startswith("0") and len(str(phone_number)) != 11:
            raise forms.ValidationError("Incomplete Number")
        if str(phone_number).startswith("+") and len(str(phone_number)) != 14:
            raise forms.ValidationError("Incomplete Number")
        if str(phone_number).startswith("234") and len(str(phone_number)) != 13:
            raise forms.ValidationError("Incomplete Number")
        return super(AgentForm, self).clean(*args, **kwargs)


Image_formset = modelformset_factory(Images, ImageForm, extra=3, max_num=  3, can_delete=True)
#Image_formse = inlineformset_factory(House, Images, fields= ["image"])
Amenity_formset = modelformset_factory(Amenity, AmenityForm, extra=3, can_delete=True, max_num=3)
