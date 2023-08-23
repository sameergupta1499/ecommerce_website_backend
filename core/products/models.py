from django.db import models
from .consts import GenderChoices, PageChoices


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    mrp = models.FloatField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    ratingtotal = models.BigIntegerField(db_column='ratingTotal', blank=True, null=True)  # Field name made lowercase.
    discount = models.BigIntegerField(blank=True, null=True)
    seller = models.TextField(blank=True, null=True)#, db_index=True)  # Add db_index=True for indexing
    purl = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)#, db_index=True)  # Add db_index=True for indexing
    gender = models.TextField(choices=GenderChoices.choices, blank=True, null=True)
    page = models.TextField(choices=PageChoices.choices, blank=True, null=True)
    product_id = models.BigIntegerField(blank=True, null=True)
    sizes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'products'
        indexes = [
            models.Index(fields=['seller', 'page']), # Basic index for seller and page columns
            models.Index(fields=['category', 'gender', 'page']), # Basic index for category, gender, and page columns
            models.Index(fields=['category', 'page']), # Basic index for category and page columns
            models.Index(fields=['gender', 'page']), # Basic index for gender and page columns
            models.Index(fields=['seller', 'page']), # Basic index for gender and page columns
            models.Index(fields=['page'])
        ]
