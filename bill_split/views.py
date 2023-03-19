from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from bill_split.models import BillSplit, BillAmounts, BillsGroup, BillUsers   

from bill_split.serializers import (
    GetBillGroupSerializer, CreateGroupSerializer, 
    AddUserSerializer, AddBillSerializer,
    SplitBillSerializer,
)


class GetBillGroup(ListAPIView):
    serializer_class = GetBillGroupSerializer

    permission_classes = [IsAuthenticated,]

    def get(self, request, id=None, *args, **kwargs):
        if id:
            bill_group = BillUsers.objects.filter(user=self.request.user, group=id).first()
            bill_serializer = GetBillGroupSerializer(bill_group)
            return Response({
                "status":"success",
                "data":bill_serializer.data
            }, status=status.HTTP_200_OK)
        
        bill_group = BillUsers.objects.filter(user=self.request.user)
        bill_serializer = GetBillGroupSerializer(bill_group, many=True)
        return Response({
            "status":"success",
             "data":bill_serializer.data
        }, status=status.HTTP_200_OK)


class CreateGroup(ListAPIView):
    serializer_class = CreateGroupSerializer

    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):

        request.data._mutable=True
        request.data['owner'] = request.user.id
        request.data_mutable=False
        
        group_serializer = CreateGroupSerializer(data=request.data)

        if group_serializer.is_valid():
            obj = group_serializer.save()
            return Response({
                "status":"success",
                "group_id":obj.id,
            }, status=status.HTTP_200_OK)
        return Response({
            "status":"failed",
            "data":group_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AddUser(ListAPIView):
    serializer_class = AddUserSerializer

    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):

        group = BillsGroup.objects.filter(id=request.data['group']).first()
        if group.owner != request.user:
            return Response({
                "status":"failed", 
                "error":"You are not the owner of this group"
            }, status=status.HTTP_400_BAD_REQUEST)
    

        user_serializer = AddUserSerializer(data=request.data)
        if user_serializer.is_valid():
            obj = user_serializer.save()
            return Response({
                "status":"success",
                "user_id":obj.id,
            }, status=status.HTTP_200_OK)
        return Response({
            "status":"failed",
            "error":user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AddBill(ListAPIView):
    serializer_class = AddBillSerializer

    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        group_user = BillUsers.objects.filter(group=request.data['group'], user=request.user).first()
        if not group_user:
            return Response({
                "status":"failed", 
                "error":"You are not a member of this group"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        request.data._mutable=True
        request.data['paid_by'] = group_user.id
        request.data_mutable=False

        bill_serializer = AddBillSerializer(data=request.data)
        if bill_serializer.is_valid():
            obj = bill_serializer.save()
            return Response({
                "status":"success",
                "bill_id":obj.id,
            }, status=status.HTTP_200_OK)
        return Response({
            "status":"failed",
            "error":bill_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class SplitBill(ListAPIView):
    serializer_class = SplitBillSerializer

    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        split_serializer = SplitBillSerializer(data=request.data, many=True)
        if split_serializer.is_valid():
            obj = split_serializer.save()
            return Response({
                "status":"success",
                "split_id":obj.id,
            }, status=status.HTTP_200_OK)
        return Response({
            "status":"failed",
            "error":split_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)