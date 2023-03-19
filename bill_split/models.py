from django.db import models
from django.contrib.auth.models import User


class BillsGroup(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class BillUsers(models.Model):
    group = models.ForeignKey(BillsGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.group.name + ' - ' + self.user.username 
    
    class Meta:
        unique_together = ('group', 'user')

class BillAmounts(models.Model):
    group = models.ForeignKey(BillsGroup, on_delete=models.CASCADE)
    paid_by = models.ForeignKey(BillUsers, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=128)

    def __str__(self):
        return self.group.name + ' - ' + self.paid_by.user.username
    

class BillSplit(models.Model):
    bill = models.ForeignKey(BillAmounts, on_delete=models.CASCADE)
    user = models.ForeignKey(BillUsers, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.bill.group.name + ' - ' + self.user.user.username