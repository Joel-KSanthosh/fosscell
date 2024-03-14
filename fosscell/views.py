import uuid
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login
from rest_framework.views import Response,APIView,status
from rest_framework.decorators import api_view
from .models import InstitutionReg,FossAdvisor,Members,User
from api.serializers import Institutionserializer,Fossadvisorserializer,Membersserializer,LoginUserSerializer,CombinedSerializer,UserSerializer
from rest_framework.response import Response

class LoginApiView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            
            user = authenticate(email=email, password=password)
            # login(request,user)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': str(token), 'user_id': serializer.data} ,status=status.HTTP_200_OK)
                
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','POST'])
def institutionview(request):
    if request.method=='GET':
        objs=InstitutionReg.objects.all()
        serializer=Institutionserializer(objs, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        data=request.data
        objs=request.user
        data['uid']=objs.id
        data['status']='null'
        data=request.data
        serializer=Institutionserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:  
            return Response(serializer.errors)
        

@api_view(['GET','POST'])
def Fossview(request):
    if request.method=='GET':
        objs=FossAdvisor.objects.all()
        serializer=Fossadvisorserializer(objs, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        data=request.data.copy()
        objs=request.user
        data['uid']=objs.id
        
        serializer=Fossadvisorserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:  
            return Response(serializer.errors)


@api_view(['GET','POST'])
def Membersview(request):
    if request.method=='GET':
        objs=Members.objects.all()
        serializer=Membersserializer(objs, many=True)
        print(request.user)
        return Response(serializer.data)
    elif request.method=='POST':
        
        objs=request.user
        
        
        unique_id = str(uuid.uuid4())
        jdata=request.data
        
        for i in jdata:
            i['uid']=objs.id
            i["uniqueid"]=unique_id
            serializer=Membersserializer(data=i)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response( serializer.errors)
        return Response(serializer.data)
 
    


@api_view(['GET'])
def combined_data_view(request):
    
    # userid = User.objects.latest('id')
    userid=request.user

    if userid is not None:
        data1 = InstitutionReg.objects.filter(uid=userid.id).values()
        data2 = FossAdvisor.objects.filter(uid=userid.id).values()
        data3 = Members.objects.filter(uid=userid.id).values()

        combined_data = {
            'result1': list(data1),
            'result2': list(data2),
            'result3': list(data3),
        }

        return Response(combined_data)
    else:
        return Response({'error': 'User ID not available for anonymous user'}, status=401)

@api_view(['GET'])
def combined_data_adminview(request,uid):
    
    # userid = User.objects.latest('id')
    # userid=request.user

    if request.user.has_perm("fosscell.admin_permission"):
        data1 = InstitutionReg.objects.filter(uid=uid).values()
        data2 = FossAdvisor.objects.filter(uid=uid).values()
        data3 = Members.objects.filter(uid=uid).values()

        combined_data = {
            'result1': list(data1),
            'result2': list(data2),
            'result3': list(data3),
        }

        return Response(combined_data)
    else:
        return Response({'error': 'User is not admin'}, status=401)



class Submit(APIView):
    def patch(self,request):
        user=User.objects.get(id=request.user.id)
        # l=InstitutionReg.objects.get(uid=uid)
        data=request.data
        data['is_registered']=True
        # data=request.data
        serializer=UserSerializer(user,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:  
            return Response(serializer.errors)


class CombinedDataView(APIView):
    def get(self, request):
        try:
            if request.user.has_perm("fosscell.admin_permission"):
            # Retrieve all instances of InstitutionReg
                institution_regs = InstitutionReg.objects.all()

                # Serialize each instance and calculate related object count
                serialized_data = []
                for institution_reg in institution_regs:
            
                    serializer = CombinedSerializer(institution_reg)
                    serialized_data.append(serializer.data)

                return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User is not admin'}, status=401)
            
        except:
            return Response({'error': 'User is unauthersized'}, status=401)
        


        

class Approval(APIView):
    def patch(self,request,uid):
        if request.user.has_perm("fosscell.admin_permission"):
            l=InstitutionReg.objects.get(uid=uid)
            data=request.data
            data['status']=True
            # data=request.data
            serializer=Institutionserializer(l,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:  
                return Response(serializer.errors)
        else:
                return Response({'error': 'User is not admin'}, status=401)

class Reject(APIView):
    
    def patch(self,request,uid):
        if request.user.has_perm("fosscell.admin_permission"):
            l=InstitutionReg.objects.get(uid=uid)
            data=request.data
            data['status']=False
            # data=request.data
            serializer=Institutionserializer(l,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:  
                return Response(serializer.errors)
        else:
            return Response({'error': 'User is not admin'}, status=401)