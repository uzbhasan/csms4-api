from django.utils import timezone
from rest_framework import serializers
from slope.models import (
    Slope, ExpertImage, OrderImage,
    Order, DModel
)
from company.models import Company


class SlopeSerializer(serializers.ModelSerializer):
    """
    Slope model serializer
    """
    class Meta:
        model = Slope
        fields = [
            'id', 'name', 'lat', 'lng', 'address',
            'created_at', 'is_inactive',
            'announced_at', 'deadline', 'company'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_company(self, company):
        if company and company.type:
            raise serializers.ValidationError('The company must be an expert')

        return company

    def validate(self, attrs):
        announced_at = attrs.get('announced_at')
        deadline = attrs.get('deadline')

        if announced_at and announced_at < timezone.now():
            raise serializers.ValidationError({
                'announced_at': f'The announced time should not be less than the current time ({timezone.now()})'
            })

        if announced_at and deadline and announced_at > deadline:
            raise serializers.ValidationError({
                'deadline': 'The deadline of the order may not be less than the date of announce'
            })

        if announced_at and deadline is None:
            raise serializers.ValidationError({
                'deadline': 'Announced slopes must have a deadline'
            })

        if announced_at is None and deadline:
            raise serializers.ValidationError({
                'deadline': 'Unannounced slopes should not have a deadline'
            })

        return attrs


class ExpertImageSerializer(serializers.ModelSerializer):
    """
    ExpertImage model serializer
    """
    class Meta:
        model = ExpertImage
        fields = ['id', 'image', 'uploaded_at', 'is_inactive', 'slope']
        read_only_fields = ['uploaded_at', 'id']


class DModelSerializer(serializers.ModelSerializer):
    """
    DModel model serializer
    """
    class Meta:
        model = DModel
        fields = ['id', 'file', 'generated_at', 'is_inactive', 'slope']
        read_only_fields = ['generated_at', 'id']


class OrderSerializer(serializers.ModelSerializer):
    """
    DModel model serializer
    """
    class Meta:
        model = Order
        fields = [
            'id', 'slope', 'company', 'status', 'deadline',
            'ordered_at', 'modified_at', 'is_inactive'
        ]
        read_only_fields = ['ordered_at', 'id', 'modified_at']


    def validate_company(self, company):
        if company and not company.type:
            raise serializers.ValidationError('The company must be an engineer')

        return company

    def validate(self, attrs):
        now = timezone.now()
        deadline = attrs.get('deadline')

        if deadline and now > deadline:
            raise serializers.ValidationError({
                'deadline': f'The deadline of the order may not be less than the current time (current time: {now})'
            })

        return attrs


class OrderImageSerializer(serializers.ModelSerializer):
    """
    OrderImage model serializer
    """
    class Meta:
        model = ExpertImage
        fields = ['id', 'image', 'uploaded_at', 'is_inactive', 'order']
        read_only_fields = ['uploaded_at', 'id']
