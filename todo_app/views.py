from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer,RegisterSerializer,LoginSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from django.views.decorators.cache import cache_page

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class TodoListViewAll(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        print("user:", user)
        todo_list = user.todo_set.all()
        serializer = TodoSerializer(todo_list, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        
        serializer = TodoSerializer(data = data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
class TodoSingleView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = request.user
        try:
            todo_detail = user.todo_set.get(id = pk)
        except Todo.DoesNotExist:
            return Response({'Error':'Todo does not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo_detail, many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
        
    def put(self, request, pk):
        user = request.user
        try:
            todo = user.todo_set.get(id = pk)
        except Todo.DoesNotExist:
            return Response({'Error':'Todo does not found'},status=status.HTTP_404_NOT_FOUND)

        data = request.data

        serializer = TodoSerializer(instance = todo, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'data is not valid'},status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        user = request.user
        try:
            todo = user.todo_set.get(id = pk)
        except Todo.DoesNotExist:
            return Response({'Error':'Todo does not found'})
        todo.delete()
        
        return Response({'message':"deleted Successfully"}, status=status.HTTP_200_OK)
        


def home(request):
    return render(request,'home.html')

@cache_page(30) 
def home2(request):
    return render(request,'home2.html')


class Register(APIView):
    def post(self, request):
        data = request.data

        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'message':serializer.errors
            })
        serializer.save()

        return Response({'message':'user created'})

class Login(APIView):
    def post(self, request):
        data = request.data

        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'message':serializer.errors
            })
         
        user = authenticate(username = data['username'], password=data['password'])
        
        if user is not None:
           
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({'message':'Login','refresh': str(refresh),'token':str(access_token)},status=status.HTTP_202_ACCEPTED)
        return Response({'message':'User does not exists'},status=status.HTTP_400_BAD_REQUEST)

