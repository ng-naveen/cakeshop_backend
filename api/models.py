from django.db import models
from django.contrib.auth.models import User


class Occasion(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Cake(models.Model):
    name = models.CharField(max_length=250)
    weight = models.CharField(max_length=50)
    occasion = models.ForeignKey(Occasion, on_delete=models.CASCADE)
    shape_options = (
        ('round', 'round'),
        ('square', 'square'),
        ('heart', 'heart')
    )
    shape = models.CharField(max_length=10, choices=shape_options, default='round')
    layer_options = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3')
    )
    layers = models.CharField(max_length=10, choices=layer_options, default='1')
    price = models.FloatField()
    image = models.ImageField(upload_to='cake_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    @property
    def get_reviews(self):
        return Review.objects.filter(cake=self)
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'cake')




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=250)
    matter = models.CharField(max_length=250)
    order_status = (
        ('order-placed', 'order-placed'),
        ('shipped', 'shipped'),
        ('delivered', 'delivered'),
        ('returned', 'returned'),
        ('cancelled', 'cancelled'),
    )
    status = models.CharField(max_length=50, choices=order_status, default='order-placed')

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    review_text = models.CharField(max_length=250)

    def __str__(self):
        return self.review_text
    

    