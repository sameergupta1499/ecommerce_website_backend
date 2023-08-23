from rest_framework import serializers
from .consts import GenderChoices, PageChoices
from .models import Products
from .utils import extract_image_links

class ProductsSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=GenderChoices.choices)
    # page = serializers.ChoiceField(choices=PageChoices.choices)
    image_list = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = (
            'id',
            'name',
            'image_list',
            # 'img',
            'price',
            'mrp',
            'rating',
            'ratingtotal',
            'discount',
            'seller',
            'purl',
            'category',
            'gender',
            # 'page',
            # 'product_id',
            'sizes',
        )
        read_only_fields = ('id',)  # If you want 'id' to be read-only

    def get_image_list(self, obj):
        try:
            return extract_image_links(obj.img)[-1]
        except:
            return None