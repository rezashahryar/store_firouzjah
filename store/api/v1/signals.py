from django.db.models.signals import post_save
from django.dispatch import receiver

from store.models import BaseProduct, ProductList

# create your signals here

@receiver(post_save, sender=BaseProduct)
def create_product_list(sender, instance, created, **kwargs):
    print(instance)
    if created:
        ProductList.objects.create(
            store=instance.store,
            product=instance
        )
