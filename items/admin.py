from django.contrib import admin
from .models import RecoveredItem  # This imports your Item model

# This makes the Item model visible in the Admin Panel
@admin.register(RecoveredItem)
class ItemAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'category', 'latitude', 'longitude')
    
   
    search_fields = ('name', 'description')
    

    list_filter = ('category',)