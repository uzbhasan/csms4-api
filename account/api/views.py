from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import Account
from account.api.serializers import (
    AccountCreateReadSerializer,
    AccountUpdateSerializer,
    AccountPasswordChangeSerializer,
    AccountAvatarUpdateSerializer
)


def get_object(pk):
    return get_object_or_404(Account, pk=pk)


class AccountList(APIView):
    """
    Get all users all create new
    """
    def get(self, request, format=None):
        accounts = Account.objects.all().filter(is_active=True)
        serializer = AccountCreateReadSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = AccountCreateReadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(APIView):
    """
    Get account details, delete or update
    """
    def get(self, request, pk, format=None):
        account = get_object(pk)
        serializer = AccountCreateReadSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        account = get_object(pk)
        serializer = AccountUpdateSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        account = get_object(pk)
        account.is_active = False
        account.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountPasswordChange(APIView):
    """
    Change account password
    """
    def put(self, request, pk, format=None):
        account = get_object(pk)
        serializer = AccountPasswordChangeSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountAvatarUpdate(APIView):
    """
    Update account avatar
    """
    def put(self, request, pk, format=None):
        account = get_object(pk)
        serializer = AccountAvatarUpdateSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountRestore(APIView):
    """
    Restore deleted (is_active=false) account
    """
    def put(self, request, pk, format=None):
        account = get_object(pk)
        if not account.is_active:
            account.is_active = True
            account.save()
            serializer = AccountCreateReadSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountForceDelete(APIView):
    """
    Force delete account from database
    """
    def delete(self, request, pk, format=None):
        account = get_object(pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
