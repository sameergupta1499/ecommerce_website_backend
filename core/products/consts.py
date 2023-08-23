from django.db import models
class GenderChoices(models.TextChoices):
    MEN = "Men"
    WOMEN = "Women"
    GIRLS = "Girls"
    BOYS = "Boys"
    UNISEX = "Unisex"
    UNISEX_KIDS = "Unisex Kids"

class PageChoices(models.TextChoices):
    CLOTHING = "clothing-and-apparels"
    ACCESSORIES = "accessories"
    PERSONAL_CARE = "personal-care"
    FOOTWARE = "footwear"
    TOYS = "toys-and-games"
    FURNISHING = "home-furnishing"

class CachePrefix:
    PREFIX_PAGE_LIST = "PREFIX_PAGE_LIST_CACHE"
    PREFIX_PAGE_COMMON = "PREFIX_PAGE_COMMON_CACHE"