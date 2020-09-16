from rest_framework import serializers

from company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    """ Company model serializer """
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = [
            'id', 'email', 'type', 'name', 'phone_number', 'address', 'about', 'avatar', 'is_inactive'
        ]
