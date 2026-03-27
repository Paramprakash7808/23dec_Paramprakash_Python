from django.db import models

class Transaction(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='PENDING', choices=[
        ('PENDING', 'Pending'),
        ('TXN_SUCCESS', 'Success'),
        ('TXN_FAILURE', 'Failure'),
    ])
    checksum = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.status}"
