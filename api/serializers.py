from rest_framework import serializers
from fosscell.models import InstitutionReg,FossAdvisor,Members,User

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class Institutionserializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category', read_only=True)
    University_name = serializers.CharField(source='university', read_only=True)
    class Meta:
        model=InstitutionReg
        exclude=['category','university','uid']
        include=['category_name','University_name']
        depth=1



class Fossadvisorserializer(serializers.ModelSerializer):
    class Meta:
        model=FossAdvisor
        fields='__all__'

class Membersserializer(serializers.ModelSerializer):
    class Meta:
        model=Members
        fields='__all__'


class CombinedSerializer(serializers.ModelSerializer):
    institution = serializers.CharField(source='institution_details', read_only=True)
    Email = serializers.CharField(source='official_mail', read_only=True)
    category_name = serializers.CharField(source='category', read_only=True)
    University_name = serializers.CharField(source='university', read_only=True)
    count = serializers.SerializerMethodField()
    State = serializers.CharField(source='state', read_only=True)
    District = serializers.CharField(source='district', read_only=True)
    date_joined = serializers.DateTimeField(source='uid.date_joined', read_only=True)  # Add this field definition
    Status = serializers.CharField(source='status', read_only=True)
    Remark=serializers.CharField(source='remarks')
    class Meta:
        model = InstitutionReg
        fields = ['institution', 'Email','category_name','University_name', 'count','State','District','date_joined','Status','Remark']
        depth=1

    def get_count(self, instance):
        l=instance.uid
        c=0
        for i in (Members.objects.filter(uid=l).values()):
            c+=1
        return c
    
