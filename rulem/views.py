from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Rules, Categorie
from .serializers import UserSerializer, RulesSerializer, CategorieSerializer
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
import zipfile
import csv
import os
import uuid
from rest_framework.permissions import IsAuthenticated




# User Register
class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# User Authentication
class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        # exp : sets the expiration time claim for the JWT
        # iat : specifies the time at which the token was issued
        payload= {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }

        # encodes the payload into a JSON Web Token (JWT) using the PyJWT
        # secret : secret key for encoding the token
        # The hashing algorithm used to generate the signature for the token
        # decode : used to convert token to a string
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        # create a response object
        response = Response()
        # set the token in cookies
        response.set_cookie(key='token', value=token, httponly=True)
        # return the token in the response body as well
        response.data = {'token': token}
        
        return response

# get all Users
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

# Delete User
class UserDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

# Create Rule
class RuleCreateAPIView(generics.ListCreateAPIView):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer
    permission_classes = []

# List Rules
class RuleListAPIView(generics.ListAPIView):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer
    permission_classes = []

# Update Rules
class RuleUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer
    permission_classes = []

# Delete Rule
class RuleDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer
    permission_classes = []


# Create Categorie
class CategorieCreateAPIView(generics.ListCreateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = []

# Delete Categorie
class CategorieDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = []


# Update Categorie
class CatgorieUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = []

# List Categorie
class CategorieListAPIView(generics.ListAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = []

# upload file
@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)
        upload_id = str(uuid.uuid4())
        
        
        # Determine file type and call the appropriate extraction function
        if filename.endswith('.zip'):
            extracted_data = extract_data_from_zip(file_path,upload_id)
        elif filename.endswith('.txt'):
            extracted_data = extract_data_from_file(file_path, upload_id)
        else:
            return JsonResponse({'error': "Unsupported file type."}, status=400)
        
        if not extracted_data:
            return JsonResponse({'error': "No data extracted from the file."}, status=400)

        data = save_to_database(extracted_data)
        # index_to_elasticsearch(extracted_data)

        return JsonResponse({'message': data})
    return JsonResponse({'error': 'Invalid request method or no file uploaded'}, status=405)

import json

def parse_rule_text(rule_text, upload_id):
    lines = rule_text.strip().split('\n')
    rule_data = {}
    rule_data['id_upload'] = upload_id
    rule_data['ruleName']= ''
    rule_data['description']= ''
    rule_data['condition']= ''
    rule_data['action']= ''
    rule_data['categorie']= None
    
    i = 0
    while i < len(lines):
        if lines[i].startswith('name:'):
            rule_data['ruleName'] = lines[i].split(': ', 1)[1].strip()
            i += 1
        elif lines[i].startswith('description: '):
            description_lines = [lines[i].split(': ', 1)[1].strip()]
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('if'):
                description_lines.append(lines[i].strip())
                i += 1
            rule_data['description'] = ' '.join(description_lines).strip()
        elif lines[i].strip().startswith('if'):
            condition = []
            while i < len(lines) and not lines[i].strip().startswith('then'):
                condition.append(lines[i].strip())
                i += 1
            rule_data['condition'] = ' '.join(condition).strip()
        elif lines[i].strip().startswith('then'):
            action = []
            while i < len(lines) and not lines[i].startswith('name: '):
                action.append(lines[i].strip())
                i += 1
            rule_data['action'] = ' '.join(action).strip()
        else:
            i += 1
            
    return rule_data


def extract_data_from_file(file_path, upload_id):
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    rules = file_content.strip().split('\n\n')
    extracted_data = []
    for rule in rules:
        rule_json = parse_rule_text(rule, upload_id)
        extracted_data.append(rule_json)
        
    return extracted_data

def extract_data_from_zip(zip_file_path, upload_id):
    extracted_data = []
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall("extracted_zip")
        for file_name in zip_ref.namelist():
            if file_name.endswith('.txt'):
                extracted_data.extend(extract_data_from_file(os.path.join("extracted_zip", file_name)))
            elif file_name.endswith('.csv'):
                extracted_data.extend(extract_data_from_csv(os.path.join("extracted_zip", file_name)))
    return extracted_data

def save_to_database(data):
    for item in data:
        rule = Rules(
            ruleName=item['ruleName'],
            description=item['description'],
            condition=item['condition'],
            action=item['action'],
            id_upload=item['id_upload'],
            categorie=None
        )
        rule.save()
        item['id'] = rule.id
    return data

# Get rules by upload_id

def get_rules_by_upload_id(request, id_upload):
    try:
        rules = Rules.objects.filter(id_upload=id_upload)
        rules_data = list(rules.values('ruleName', 'description', 'condition', 'action', 'categorie'))
        return JsonResponse({'status': 'success', 'data': rules_data}, status=200)
    except Rules.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Rules not found'}, status=404)