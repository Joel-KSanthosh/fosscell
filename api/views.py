from rest_framework.response import Response
from fosscell.models import Activity,Institution
from . import serializers
from rest_framework.views import Response,APIView,status
from api import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class UserActivityGetView(APIView):
    @method_decorator(login_required)
    def get(self,request,pk):
        if request.user.is_authenticated:
                # print(request.user)
                try:
                    objs = Activity.objects.get(id=pk)
                except:
                    return Response({
                        'status' : 'Failure',
                        'message' : 'No Activity Found'
                    },status=status.HTTP_404_NOT_FOUND)
                # print(objs.uid)
                if objs is not None:
                    if objs.uid == request.user or request.user.has_perm('fosscell.admin_permission'):

                        serializer = serializers.UserActivityGetSerializer(objs)
                        return Response({'status':'Success','message':serializer.data},status=status.HTTP_200_OK)
                        
                    else:
                        return Response({
                        'status' : 'Failure',
                        'message' : 'Unauthorized User',
                        },status.HTTP_401_UNAUTHORIZED)
                return Response({'status':'Failure'},status=status.HTTP_302_FOUND)        
        else:
            return Response({
            'status' : 'Failure',
            'message' : "You are not allowed here!",
            },status.HTTP_401_UNAUTHORIZED)
        
                
                
                
                
            
        
class UserActivityPostView(APIView):
    @method_decorator(login_required)
    def post(self,request):
        # print("User:", request.user)
        # print("Authentication:", request.auth)
        if request.user.is_authenticated and not request.user.has_perm('fosscell.admin_permission'):
            data = request.data.copy()
            user = self.request.user
            institution =  user.institution
            val = Institution.objects.filter(name=institution).first()
            data['uid'] = user.id
            data['institution_name'] = val.id
            data['status'] = 'null'
            serializer = serializers.UserActivityPostSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'details':"Authentication required"},status=status.HTTP_401_UNAUTHORIZED)
        
        
class UserActivityPatchDeleteView(APIView):
    @method_decorator(login_required)
    def patch(self,request,pk):
        if request.user.is_authenticated and not request.user.has_perm('fosscell.admin_permission'):
            data = request.data
            try:
                
                objs = Activity.objects.get(id=pk)
                if request.user == objs.uid:
                    serializer = serializers.UserActivityPostSerializer(objs, data=data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'details':"Authentication required"},status=status.HTTP_401_UNAUTHORIZED)
            except ObjectDoesNotExist:
                return Response({'error': "Activity matching the query does not exist."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'details':"Authentication required"},status=status.HTTP_401_UNAUTHORIZED)
        

    @method_decorator(login_required)
    def delete(self,request,pk):
        if request.user.is_authenticated and not request.user.has_perm('fosscell.admin_permission'):
            data = request.data
            try:
                
                objs = Activity.objects.get(id=pk)
                if request.user == objs.uid:
                    objs.delete()
                    return Response({'status':'Success','message':'Activity deleted'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'details':"Authentication required"},status=status.HTTP_401_UNAUTHORIZED)
            except ObjectDoesNotExist:
                return Response({'error': "Activity matching the query does not exist."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'details':"Authentication required"},status=status.HTTP_401_UNAUTHORIZED)

class RegisterApiView(APIView):
    def post(self,request):
        serializer = serializers.RegisterUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status' : 'Failed',
                'message' : serializer.errors,
            }, status.HTTP_400_BAD_REQUEST
            )
        user_data = serializer.validated_data
        email = user_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            return Response({
                'status' : 'Failed',
                'message' : 'User already exists',
            }, status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer.save()

            return Response({
                'status' : 'Success',
                'message' : serializer.data,
                },status.HTTP_201_CREATED
            )
    
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
        

        

class ActivityTableView(APIView):
    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.has_perm('fosscell.admin_permission'):
                objs = Activity.objects.all()
            else:
                objs = Activity.objects.filter(uid=request.user)

            if objs.exists():
                serializer = serializers.ActivityTableSerializer(objs, many=True,context={'objs':objs})
                return Response({
                    'status': 'Success',
                    'message': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'Failure',
                    'message': "No data found!"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                'status': 'Failure',
                'message': "Unauthorized"
            }, status=status.HTTP_401_UNAUTHORIZED)


# class AdminApprove(APIView):
#     @method_decorator(login_required)
#     def patch(self,request,pk):
#         if request.user.is_authenticated and request.user.has_perm('fosscell.admin_permission'):
#             try:
#                 objs = Activity.objects.get(id=pk)
#             except:
#                 return Response({'status':'Failure','message':'Activity does not exist!'},status=status.HTTP_204_NO_CONTENT)
#             data = request.data
#             # if data['status'] == null:
#             data['status'] = True
#             serializer = serializers.UserActivityPostSerializer(objs,data=data,partial=True)
#             if not serializer.is_valid():
#                 return Response({
#                     'status' : 'Failed',
#                     'message' : serializer.errors,
#                 }, status.HTTP_400_BAD_REQUEST
#                 )

#             serializer.save()
#             return Response({
#                     'status' : 'Success',
#                     'message' : serializer.data,
#                 }, status.HTTP_200_OK
#                 )
#         else:
#             return Response({'status':'Failure','message':'Not Authorized!'},status=status.HTTP_401_UNAUTHORIZED)
        

class AdminApprovalView(APIView):
    @method_decorator(login_required)
    def patch(self, request, pk):
        if request.user.is_authenticated and request.user.has_perm('fosscell.admin_permission'):
            try:
                activity = Activity.objects.get(id=pk)
            except ObjectDoesNotExist:
                return Response({'status': 'Failure', 'message': 'Activity does not exist!'}, status=status.HTTP_204_NO_CONTENT)
            
            if(activity.status == False or activity.status == True):
                return Response({"status":"Failure","message":"Already approved or rejected"},status=status.HTTP_403_FORBIDDEN)

            data = request.data.copy()
            button = data.get('button')

            if button not in ('Disapprove', 'Approve'):
                return Response({'status': 'Failed', 'message': 'Invalid button value'}, status=status.HTTP_400_BAD_REQUEST)
            
            status_value = True if button == 'Approve' else False
            data['status'] = status_value

            serializer = serializers.ApprovalSerializer(activity, data=data, partial=True)
            if not serializer.is_valid():
                return Response({'status': 'Failed', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({'status': 'Success', 'message': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Failure', 'message': 'Not Authorized!'}, status=status.HTTP_401_UNAUTHORIZED)