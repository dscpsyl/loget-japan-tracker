from django.contrib import admin

from .models import LoGetCards
from .models import LoGetUsers

admin.site.register(LoGetUsers)
admin.site.register(LoGetCards)
