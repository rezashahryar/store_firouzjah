from django.db.models.signals import post_save
from django.dispatch import receiver

from store.models import Product, ProductList

# create your signals here

@receiver(post_save, sender=Product)
def create_product_list(sender, instance, created, **kwargs):
    if created:
        ProductList.objects.create(
            store=instance.product.store,
            product=instance
        )
