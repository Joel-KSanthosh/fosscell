from rest_framework import serializers
from fosscell.models import Activity,ProgramType,ProgramMode,AudienceType,User,Institution

class LoginUserSerilaizer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField()




class InstitutionNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['name']





class ProgramTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramType
        fields = ['values']




class ProgramModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramMode
        fields = ['values']




class AudienceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudienceType
        fields = ['values']

    
      
        
class UserActivityGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        exclude = ['uid']



class UserActivityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class RegisterUserSerializer(serializers.Serializer):
    institution = serializers.CharField(max_length=250)
    email = serializers.EmailField(max_length=254)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)


    def validate(self, data):
        if data['password1'] and data['password2'] and data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        return User.objects.create_user(
            institution=validated_data['institution'],
            email=validated_data['email'],
            password=validated_data['password1']
        )






class ActivityTableSerializer(serializers.ModelSerializer):
    program_type_name = serializers.SerializerMethodField()
    program_mode_name = serializers.SerializerMethodField()
    audience_type_name = serializers.SerializerMethodField()
    No = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['No','program_name','program_type_name', 'program_mode_name','audience_type_name', 'status', 'remarks', ]

    
    def get_program_type_name(self, obj):
        program_type_id = obj.program_type_id
        try:
            program_type = ProgramType.objects.get(pk=program_type_id)
            return program_type.values
        except ProgramType.DoesNotExist:
            return None
        
    def get_program_mode_name(self, obj):
        program_mode_id = obj.program_mode_id
        try:
            program_mode = ProgramMode.objects.get(pk=program_mode_id)
            return program_mode.values
        except ProgramMode.DoesNotExist:
            return None
    
    def get_audience_type_name(self, obj):
        audience_type_id = obj.audience_type_id
        try:
            audience_type = AudienceType.objects.get(pk=audience_type_id)
            return audience_type.values
        except AudienceType.DoesNotExist:
            return None
    
    def get_No(self,obj):
        queryset = self.context['objs']
        index = list(queryset).index(obj) + 1
        return index



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
    
    class Meta:
        model=InstitutionReg
        fields="__all__"



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
    
