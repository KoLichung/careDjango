from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from modelCore.models import User, UserLicenseShipImage

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    # is_gotten_line_id = serializers.BooleanField(default=False)

    class Meta:
        model = get_user_model()
        fields = ('phone', 'password', 'name','line_id')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id','phone','name','gender','email','address','image','is_servant','is_passed','is_servant_passed','rating','is_home','home_hour_wage','home_half_day_wage','home_one_day_wage','is_hospital','hospital_hour_wage','hospital_half_day_wage','hospital_one_day_wage','about_me','ATMInfoBankCode','ATMInfoBranchBankCode','ATMInfoAccount')
        # read_only_fields = ('id')

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    phone = serializers.CharField(allow_null=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        allow_null=True,
    )
    line_id = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        allow_null=True,
        required=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        phone = attrs.get('phone')
        password = attrs.get('password')
        # line_id = attrs.get('line_id')
        
        user = None

        if password and password != '00000':
            user = authenticate(
                request=self.context.get('request'),
                username=phone,
                password=password
            )
        
        # if (line_id and line_id != ''):
        #     try:
        #         user = User.objects.get(phone=phone, line_id=line_id)
        #     except Exception as e:
        #         print('')
            
        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)

class UserLicenceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLicenseShipImage
        fields = '__all__'
        read_only_fields = ('id','user')