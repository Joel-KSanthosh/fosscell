from rest_framework.response import Response
from rest_framework.views import APIView
from fosscell.models import Activity,Institution,User
from rest_framework import status
from . import serializers
from django.contrib.auth import login
from rest_framework.views import Response,APIView,status
from api import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class UserActivityView(APIView):
    
    def get(self,request):
        try:
            objs = Activity.objects.all()
            serializer = serializers.UserActivityGetSerializer(objs,many=True)
        except:
            return Response(serializer.error,status=status.HTTP_204_NO_CONTENT)
        
        return Response(serializer.data,status=status.HTTP_302_FOUND)

    def post(self,request):
        print("User:", request.user)
        print("Authentication:", request.auth)
        if request.user.is_authenticated:
            user = self.request.user 
            print(user)           
            institution = user.institution
            
            # var = User.objects.filter(email=user).first()
            # institution = var.institution
            val = Institution.objects.filter(name=institution).first()
            data = request.data
            data['institution_name'] = val.id
            serializer = serializers.UserActivityGetSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'details':"Authentication required"},status=status.HTTP_401_UNAUTHORIZED)
        


# class RegisterApiView(APIView):
#     def post(self,request):
#         serializer = serializers.UserSerializer(data=request.data)

#         if not serializer.is_valid():
#             return Response({
#                 'status' : 'Failed',
#                 'message' : serializer.errors,
#             }, status.HTTP_400_BAD_REQUEST
#             )
#         serializer.save()

#         return Response({
#             'status' : 'Success',
#             'message' : serializer.data,
#         },status.HTTP_201_CREATED
#         )
    
class LoginApiView(APIView):
    def post(self,request):
        serializer = serializers.LoginUserSerilaizer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status' : 'Failed',
                'message' : serializer.errors,
            }, status.HTTP_404_NOT_FOUND
            )
        
        user = authenticate(email=serializer.data['email'],password=serializer.data['password'])
        if user:
            token , _ = Token.objects.get_or_create(user=user)
            return Response({
                'status' : 'Success',
                'message' : serializer.data,
                'token' : str(token)
            },status.HTTP_200_OK
            )
        else:
            return Response({
                'status' : 'Failed',
                'message' : serializer.errors,
            }, status.HTTP_404_NOT_FOUND
            )