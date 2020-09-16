from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from company.api.serializers import CompanySerializer
from company.models import Company
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse


class CompanyList(APIView):
    """
    Get all companies or create new
    """
    # Get all companies:
    def get(self, request, format=None):
        # companies = Company.objects.all().filter(is_inactive=False)
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    # Create new company:
    def post(self, request, format=None):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetail(APIView):
    """
    Get company details, delete or update
    """
    def get_object(self, pk):
        return get_object_or_404(Company, pk=pk)

    def get(self, request, pk, format=None):
        company = self.get_object(pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        company = self.get_object(pk)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        company = self.get_object(pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
