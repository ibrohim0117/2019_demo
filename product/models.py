from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class BaseCreatedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseCreatedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(BaseCreatedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    rating = models.FloatField(default=0, editable=False, validators=[MinValueValidator(0), MaxValueValidator(5)])
    price = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    sale = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    count = models.IntegerField(default=0)
    code = models.CharField(max_length=25, unique=True)
    type = models.CharField(max_length=100)
    about = models.TextField(blank=True, null=True)
    information = models.JSONField(blank=True, null=True, default=dict)
    views = models.IntegerField(default=0, editable=False, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

    @property
    def image_list(self):
        return [i.image.url for i in self.images.all()]

    @property
    def sale_price(self):
        # print(self.image_list)
        return self.price - (self.sale * self.price / 100)

    @property
    def is_available(self):
        return self.count > 0

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ['-views']




class ProductImage(BaseCreatedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d')

    def __str__(self):
        return self.product.name

