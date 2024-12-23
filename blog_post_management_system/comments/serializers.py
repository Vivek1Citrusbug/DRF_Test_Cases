from rest_framework import serializers
from comments.models import UserComments

class UserCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComments
        fields = '__all__'  
