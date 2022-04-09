from django.contrib import admin
from .models import Amenity,Agent,Land,House,Images

admin.site.register(House)
admin.site.register(Land)
admin.site.register(Agent)
admin.site.register(Amenity)
admin.site.register(Images)
