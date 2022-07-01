from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .serializer import Sample
from .models import student
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics,mixins



# def display(request):
#     d={'roll':1,'name':'jojo'}
#     return JsonResponse(d)
# # Create your views here.
@csrf_exempt
def display(request):
    if request.method =='GET':
        d=student.objects.all()
        s=Sample(d,many=True)
        return JsonResponse(s.data, safe=False)
    elif request.method =='POST':
        d=JSONParser().parse(request)
        s=Sample(data=d)
        if s.is_valid():
            s.save()
            return JsonResponse(s.data)
        else:
            return JsonResponse(s.errors)

@csrf_exempt
def search(request,d):
    try:
        demo= student.objects.get(pk=d)
    except Exception:
        return HttpResponse("Invalid")
    if request.method=='GET':
        serializer=Sample(demo)
        return JsonResponse(serializer.data)
    elif request.method=='PUT':
        data=JSONParser().parse(request)
        serializer=Sample(demo, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors)
    elif request.method=='DELETE':
        demo.delete()
        return HttpResponse('delete')

@api_view(['GET','POST'])
def display1(request):
    if request.method=='GET':
        demo = student.objects.all()
        serializer=Sample(demo, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=Sample(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def searchapiview(request,d):
    try:
        demo= student.objects.get(pk=d)
    except Exception:
        return HttpResponse("Invalid")
    if request.method=='GET':
        serializer=Sample(demo)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=Sample(demo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    elif request.method=='DELETE':
        demo.delete()
        return HttpResponse('deleted')

class dispaly(APIView):
    def get(self,request):
        demo=student.objects.all()
        s= Sample(demo,many=True)
        return Response(s.data)
    def post(self,request):
        s= Sample(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data,status=status.HTTP_201_CREATED)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class searchclass(APIView):
    def get(self,request,d):
        demo= student.objects.get(pk=d)
        s=Sample(demo)
        return Response(s.data)
    def put(self,request, d):
        demo=student.objects.get(pk=d)
        s=Sample(demo,data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,d):
        demo=student.objects.get(pk=d)
        demo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class genericapiview(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class = Sample
    queryset = student.objects.all()
    authentication_classes = [SessionAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)

class searchgeneric(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin,mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = Sample
    queryset = student.objects.all()
    lookup_field = 'id'
    def get(self,request,id):
        return self.retrieve(request,id)
    def put(self,request, id=None):
        return self.update(request,id)
    def delete(self, request,id):
        return self.destroy(request,id)
