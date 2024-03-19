from rest_framework import serializers
from fosscell.models import Activity,ProgramType,ProgramMode,AudienceType,User,Institution
from rest_framework.views import status
from django.core.exceptions import ValidationError
from django.utils import timezone


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
        depth = 1



class UserActivityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

    def validate(self,data):
        duration = data.get('duration')
        start_date = data.get('start_date',None)
        end_date = data.get('end_date',None)
        date_time = data.get('date_time',None)
        need_assistance = data.get('need_assistance')
        kind_of_assistance = data.get('kind_of_assistance',None)
        participant_count = data.get('participant_count')

        if participant_count <=1:
            raise ValidationError({
                    "status": "Failure",
                    "message": "Minimum participants must be 2"
                })
        
        if duration == 1:
            if not date_time or start_date or end_date:
                raise ValidationError({
                    "status": "Failure",
                    "message": "Cannot give start date or end date if duration is 1. Need to give date and time."
                })
        elif duration > 1:
            if not start_date or not end_date or date_time:
                raise ValidationError({
                    "status": "Failure",
                    "message": "Cannot give date and time if duration is greater than 1, give the start date and end date."
                })

        now = timezone.now().date()
        if start_date and end_date:
            if start_date < now or end_date < now:
                raise ValidationError({
                    "status": "Failure",
                    "message": "Choose any upcoming date!"
                })
        if start_date and end_date:
            if start_date < now or end_date < now:
                raise ValidationError({
                    "status": "Failure",
                    "message": "Choose any upcoming date!"
                })

            if start_date >= end_date:
                raise ValidationError({
                    "status": "Failure",
                    "message": "End date must be greater than any Start date!"
                })

            date_diff = end_date - start_date
            num_days = date_diff.days
            # print(num_days)
            if num_days != duration:
                raise ValidationError({
                    "status": "Failure",
                    "message": "Choose date for the given duration"
                })

        if need_assistance == True and not kind_of_assistance:
            raise ValidationError({
                "status": "Failure",
                "message": "Enter the needed assistance details"
            })

        if need_assistance == False and kind_of_assistance:
            raise ValidationError({
                "status": "Failure",
                "message": "You don't need any assistance"
            })

        return data



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

    class Meta:
        model = Activity
        fields = ['program_name','program_type_name', 'program_mode_name','audience_type_name', 'status', 'remarks', ]

    
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
    



class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['status','remarks']


    def validate(self, data):
        status_value = data.get('status', None)
        remarks_value = data.get('remarks', None)

        if status_value == False and not remarks_value:
            raise ValidationError({
                "status": "Failure",
                "message": "Remarks cannot be empty when status is False"
            })
        elif status_value == True and remarks_value:
            raise ValidationError({
                "status": "Failure",
                "message": "Remarks cannot have value when status is True"
            })

        return data
