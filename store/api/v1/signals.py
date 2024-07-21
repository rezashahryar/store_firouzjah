from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import User
from store.models import Customer, Product, ProductList

# create your signals here

@receiver(post_save, sender=Product)
def create_product_list(sender, instance, created, **kwargs):
    if created:
        ProductList.objects.create(
            store=instance.product.store,
            product=instance
        )


@receiver(post_save, sender=User)
def create_customer_wher_user_registered(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            user=instance
        )
