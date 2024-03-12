from rest_framework import serializers
from fosscell.models import Activity

class UserActivityGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
        depth = 1


class LoginUserSerilaizer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField()
