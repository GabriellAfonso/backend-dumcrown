from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


# TODO fazer todas as validaçoes e depois colocar dentro de validators=[AQUI]
# def my_password_validator(password):
#     if len(password) < 8:
#         raise serializers.ValidationError(
#             "A senha deve ter pelo menos 8 caracteres.")
#     if password.isnumeric():
#         raise serializers.ValidationError(
#             "A senha não pode ser apenas números.")
#     # Aqui você pode adicionar mais regras
#     return password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
