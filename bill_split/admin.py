from django.contrib import admin

from bill_split.models import BillsGroup, BillAmounts, BillSplit, BillUsers

@admin.register(BillsGroup)
class BillsGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner','created_at')

@admin.register(BillUsers)
class BillUsersAdmin(admin.ModelAdmin):
    list_display = ('group', 'user')

    def get_group(self, obj):
        return obj.group.name


@admin.register(BillAmounts)
class BillAmountsAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'paid_by_user','amount', 'purpose')

    def group_name(self, obj):
        return obj.group.name
    
    def paid_by_user(self, obj):
        return obj.paid_by.user.username

@admin.register(BillSplit)
class BillSplitAdmin(admin.ModelAdmin):

    list_display = ('group', 'payee','amount','is_paid', 'purpose')

    def group(self, obj):
        return obj.bill.group.name
    
    def payee(self, obj):
        return obj.user.user.username

    def purpose(self, obj):
        return obj.bill.purpose

   