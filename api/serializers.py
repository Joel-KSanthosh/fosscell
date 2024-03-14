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
    # program_type_name = serializers.SerializerMethodField()
    # program_mode_name = serializers.SerializerMethodField()
    # audience_type_name = serializers.SerializerMethodField()
    # # institution_name = serializers.SerializerMethodField()
    class Meta:
        model = Activity
        exclude = ['uid']
        # fields = ['id','institution_name','program_name',"participant_count",'program_type_name', 'program_mode_name','audience_type_name',"duration","date_time","start_date","end_date" , "proposed_venue","need_assistance","kind_of_assistance","notified_others","website_link","supporting_documents" ,'status', 'remarks', ]

        # def get_program_type_name(self, obj):
        #     program_type_id = obj.program_type_id
        #     try:
        #         program_type = ProgramType.objects.get(pk=program_type_id)
        #         return program_type.values
        #     except ProgramType.DoesNotExist:
        #         return None
        
        # def get_program_mode_name(self, obj):
        #     program_mode_id = obj.program_mode_id
        #     try:
        #         program_mode = ProgramMode.objects.get(pk=program_mode_id)
        #         return program_mode.values
        #     except ProgramMode.DoesNotExist:
        #         return None
        
        # def get_audience_type_name(self, obj):
        #     audience_type_id = obj.audience_type_id
        #     try:
        #         audience_type = AudienceType.objects.get(pk=audience_type_id)
        #         return audience_type.values
        #     except AudienceType.DoesNotExist:
        #         return None
            
        # def get_institution_name(self, obj):
        #     institution_name_id = obj.institution_name_id
        #     try:
        #         institution_name = Institution.objects.get(pk=institution_name_id)
        #         return institution_name.name
        #     except Institution.DoesNotExist:
        #         return None





class UserActivityPostSerializer(serializers.ModelSerializer):
    # program_type_name = serializers.SerializerMethodField()
    # program_mode_name = serializers.SerializerMethodField()
    # audience_type_name = serializers.SerializerMethodField()
    # institution_name = serializers.SerializerMethodField()
    class Meta:
        model = Activity
        fields = '__all__'
    #     fields = ['id',"uid",'institution_name','program_name',"participant_count",'program_type_name', 'program_mode_name','audience_type_name',"duration","date_time","start_date","end_date" , "proposed_venue","need_assistance","kind_of_assistance","notified_others","website_link","supporting_documents" ,'status', 'remarks', ]

    # def get_program_type_name(self, obj):
    #     program_type_id = obj.program_type_id
    #     try:
    #         program_type = ProgramType.objects.get(pk=program_type_id)
    #         return program_type.values
    #     except ProgramType.DoesNotExist:
    #         return None
        
    # def get_program_mode_name(self, obj):
    #     program_mode_id = obj.program_mode_id
    #     try:
    #         program_mode = ProgramMode.objects.get(pk=program_mode_id)
    #         return program_mode.values
    #     except ProgramMode.DoesNotExist:
    #         return None
    
    # def get_audience_type_name(self, obj):
    #     audience_type_id = obj.audience_type_id
    #     try:
    #         audience_type = AudienceType.objects.get(pk=audience_type_id)
    #         return audience_type.values
    #     except AudienceType.DoesNotExist:
    #         return None
        
    # # def get_institution_name(self, obj):
    # #     institution_name_id = obj.institution_name_id
    # #     try:
    # #         institution_name = Institution.objects.get(pk=institution_name_id)
    # #         return institution_name.name
    # #     except Institution.DoesNotExist:
    # #         return None




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



