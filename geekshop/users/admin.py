from django.contrib import admin

from users.models import User
from baskets.admin import BasketAdmin
from  baskets.models import Basket

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = Basket
    inlines = (BasketAdmin,)
