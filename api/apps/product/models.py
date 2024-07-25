from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    sku = models.CharField(max_length=13,help_text="Enter Product Stock Keeping Unit")
    barcode = models.CharField(max_length=13,help_text="Enter Product Barcode (ISBN, UPC ...)")
    title = models.CharField(max_length=200, help_text="Enter Product Title")
    description = models.TextField(help_text="Enter Product Description")
    unit_cost = models.FloatField(help_text="Enter Product Unit Cost")
    unit = models.CharField(max_length=10,help_text="Enter Product Unit ")
    quantity = models.FloatField(help_text="Enter Product Quantity")
    min_quantity = models.FloatField(help_text="Enter Product Min Quantity")

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Product.
        """
        return reverse('product-detail-view', args=[str(self.id)])

    def __str__(self):

        return self.title

class Transaction(models.Model):
    sku = models.CharField(max_length=13,help_text="Enter Product Stock Keeping Unit")
    barcode = models.CharField(max_length=13,help_text="Enter Product Barcode (ISBN, UPC ...)")
    comment = models.TextField(help_text="Enter Product Stock Keeping Unit")
    unitCost = models.FloatField(help_text="Enter Product Unit Cost")
    quantity = models.FloatField(help_text="Enter Product Quantity")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    REASONS = (
        ('import', 'New Stock'),
        ('order_placed', 'Order Placed'),
        ('order_canceled', 'Order Canceled'),
    )
    reason = models.CharField(max_length=2, choices=REASONS, blank=True, default='ns', help_text='Reason for transaction')

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Product.
        """
        return reverse('transaction-detail-view', args=[str(self.id)])

    def __str__(self):
        return 'Transaction :  %d' % (self.id)


@receiver(post_save, sender=Product)
def check_quantity_min(sender, instance, created, **kwargs):
    if instance.quantity < instance.quantity_min:
        
        send_sms_to_admin(instance.product_name, instance.quantity_min)

def send_sms_to_admin(product_name, quantity_min):
    
    pass  # TODO




    