from rest_framework import serializers
from account.models import User


class UserSeriallizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email','password']

        def create(self, validated_data):
            password=validated_data.pop('password', None)
            instance=self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance



    