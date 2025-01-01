from django.db import models
from django.contrib.auth.models import User

# Model Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# Model Equipment
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='equipment', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='equipment_images/')

    def __str__(self):
        return self.name


# Model Rental
class Rental(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('advance', 'In advance'),
        ('on_pickup', 'On pickup'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='on_pickup'
    )
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def total_price(self):
        return self.total_days * self.equipment.price_per_day

    def __str__(self):
        return f"Rental {self.id} - {self.equipment.name} by {self.user.username}"
