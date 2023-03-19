from rest_framework import serializers

from bill_split.models import BillsGroup, BillAmounts, BillSplit, BillUsers


class GetBillGroupSerializer(serializers.ModelSerializer):
    group_id = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    to_pay = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BillUsers
        fields = ('group_id','group_name', 'to_pay', 'users_count')
    
    def get_group_id(self, obj):
        return obj.group.id
    
    def get_group_name(self, obj):
        return obj.group.name

    def get_to_pay(self, obj):
        bill_split =  BillSplit.objects.filter(user=obj, is_paid=False)
        amount = 0
        for split in bill_split:
            amount += split.amount
        
        return amount
    
    def get_users_count(self, obj):
        return BillUsers.objects.filter(group=obj.group).count()


class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillsGroup
        fields = ('name','owner',)

class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillUsers
        fields = ('group','user',)

class AddBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillAmounts
        fields = ('group','paid_by','amount','purpose')

class SplitBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillSplit
        fields = ('bill','user','amount')