import re

from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password


class UserSerializer(serializers.ModelSerializer): # 회원기능 serializer
    password2= serializers.CharField(error_messages={'required':'비밀번호를 입력해주세요.', 'blank':'비밀번호를 입력해주세요.', 'write_only':True})
    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'nickname', 'address', 'gender', 'height', 'weight', 'date_of_birth', 'password', 'password2', 'profile_image',)
        
    def validate(self, data):
        PASSWORD_VALIDATION = r"^(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,16}"
        PASSWORD_PATTERN = r"(.)\1+\1"
        USERNAME_VALIDATION = r"^(?=.*[$@$!%*?&]){1,2}"
        NICKNAME_VALIDATION = r"^(?=.*[$@$!%*?&])"
        ADDRESS_VALIDATION = r"^(?=.*[$@$!%*?&])"
        HEIGHT_VALIDATION = r"^(?=.*[A-Za-z])"
        
        username = data.get('username')
        nickname = data.get('nickname')
        password = data.get('password')
        password2 = data.get('password2')
        address = data.get('address')
        height = data.get('height')
        weight = data.get('weight')
        
        
        if re.search(NICKNAME_VALIDATION, str(nickname)): # 닉네임 유효성 검사
            raise serializers.ValidationError(detail={"nickname":"닉네임에는 특수문자가 포함될 수 없습니다!"})
        
        if re.search(USERNAME_VALIDATION, str(username)): # 아이디 유효성 검사
            raise serializers.ValidationError(detail={"username":"아이디에는 특수문자가 포함될 수 없습니다!"})
        
        if re.search(ADDRESS_VALIDATION, str(address)): # 주소 유효성 검사
            raise serializers.ValidationError(detail={"address":"주소에는 특수문자가 포함될 수 없습니다!"})
        
        if re.search(HEIGHT_VALIDATION, str(height)): # 키 유효성 검사
            raise serializers.ValidationError(detail={"height":"숫자만 입력 가능합니다!"})
        
        if re.search(HEIGHT_VALIDATION, str(weight)): # 몸무게 유효성 검사
            raise serializers.ValidationError(detail={"weight": "숫자만 입력 가능합니다!"})
        
        
        if password: # 비밀번호 유효성 검사
            if password != password2:
                raise serializers.ValidationError(detail={"password":"비밀번호 확인이 일치하지 않습니다!"})
            
            if not re.search(PASSWORD_VALIDATION, str(password)):
                raise serializers.ValidationError(detail={"password":"비밀번호는 8자 이상 16자이하의 영문, 숫자, 특수문자 조합이어야 합니다! "})
            
            if re.search(PASSWORD_PATTERN, str(password)):
                raise serializers.ValidationError(detail={"password":"너무 일상적인 숫자or단어 입니다!"})


        return data    
    
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        nickname = validated_data['nickname']
        address = validated_data['address']
        height = validated_data['height']
        weight = validated_data['weight']
        date_of_birth = validated_data['date_of_birth']
        gender = validated_data['gender']

        user = User(
            username=username,
            email=email,
            nickname=nickname,
            address=address,
            height=height,
            weight=weight,
            date_of_birth=date_of_birth,
            gender=gender,
        )
        user.set_password(validated_data['password']) # 패스워드 해싱
        user.save()
        return user
    
    def update(self, instance, validated_data): # 비밀번호 수정 
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
            
        instance.save()
        
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):   # jwt payload 커스텀
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token


class UserProfileSerializer(serializers.ModelSerializer): # 회원정보 조회 serializer

    class Meta:
        model = User
        fields = ('username', 'nickname', 'email', 'address', 'gender', 'height', 'weight', 'date_of_birth', 'profile_image', 'point')