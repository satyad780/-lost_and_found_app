from django.db import models

class RecoveredItem(models.Model):
    CATEGORIES = [
        ('Electronics', 'Electronics'),
        ('Wallets', 'Wallets/Bags'),
        ('Keys', 'Keys'),
        ('Pets', 'Pets'),
        ('Documents', 'ID/Documents'),
        ('Other', 'Other'),
    ]

    # Item Core Details
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORIES, default='Other')
    description = models.TextField()
    image = models.ImageField(upload_to='items/')
    
    # New Finder Details
    finder_name = models.CharField(max_length=100)
    finder_contact = models.CharField(max_length=20)
    
    # Location Data
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.finder_name}"

    class Meta:
        ordering = ['-created_at']