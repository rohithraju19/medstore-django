from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404





@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    form = UserCreationForm(data=request.data)
    if form.is_valid():
        user = form.save()
        return Response("account created successfully", status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)


from medicine.forms import MedicineForm
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_medicine(request):
    form = MedicineForm(request.POST)
    if form.is_valid():
        medicine = form.save()
        return Response({'id': medicine.id}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from medicine.models import Medicine
from .serializers import MedicineSerializer
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_medicine(request):
    medicines = Medicine.objects.all()
    serializer = MedicineSerializer(medicines, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_medicine(request, pk):
    medicines= get_object_or_404(Medicine, pk=pk)
    form = MedicineForm(request.data, instance=medicines)
    if form.is_valid():
        form.save()
        serializer = MedicineSerializer(medicines)
        return Response(serializer.data)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_medicine(request, pk):
    try:
        product = Medicine.objects.get(pk=pk)
    except Medicine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    product.delete()
    return Response("deleted successfully")

@api_view(['GET'])
@permission_classes((AllowAny,))
def search_medicine(request):
    query = request.query_params.get('query', None)
    if query is None:
        return Response({'error': 'Please provide a search query'}, status=status.HTTP_400_BAD_REQUEST)

    medicines = Medicine.objects.filter(name__icontains=query)  # Assuming 'name' field for searching, adjust as per your model
    serializer = MedicineSerializer(medicines, many=True)  # Remove 'fields' argument
    return Response(serializer.data)
