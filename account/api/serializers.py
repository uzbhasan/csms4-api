from rest_framework import serializers
from account.models import Account


def validate_role_company_relations(attrs, with_password=True, only_password=False):
    if with_password:
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': 'Passwords must match'
            })

    if not only_password:
        if attrs['role'] in ['SA', 'AD'] and attrs.get('company') is not None:
            raise serializers.ValidationError({
                'company': 'Administrators should not have any kind of company'
            })

        if attrs['role'] in ['GM', 'MA', 'EM'] and attrs.get('company') is None:
            raise serializers.ValidationError({
                'company': 'Company members must have a company'
            })


class AccountCreateReadSerializer(serializers.ModelSerializer):
    """
    User creation serializer
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    id = serializers.IntegerField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'email', 'first_name', 'last_name', 'role', 'company',
            'phone_number', 'avatar', 'password', 'password2',
            # readonly fields
            'id', 'date_joined', 'last_login', 'is_active'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        validate_role_company_relations(attrs)
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        account = Account.objects.create(**validated_data)
        account.set_password(password)
        account.save()

        return account


class AccountUpdateSerializer(serializers.ModelSerializer):
    """
    Account update without password and avatar
    """
    id = serializers.IntegerField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'email', 'first_name', 'last_name', 'role', 'company', 'phone_number',
            # readonly fields
            'avatar', 'id', 'date_joined', 'last_login', 'is_active'
        ]

    def validate(self, attrs):
        validate_role_company_relations(attrs, with_password=False)
        return attrs

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)
        instance.company = validated_data.get('company', instance.company)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance


class AccountPasswordChangeSerializer(serializers.ModelSerializer):
    """
    Account update without password and avatar
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = [
            'password', 'password2'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        validate_role_company_relations(attrs, only_password=True)
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance


class AccountAvatarUpdateSerializer(serializers.ModelSerializer):
    """
    Account update without password and avatar
    """
    class Meta:
        model = Account
        fields = [
            'avatar'
        ]

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance
