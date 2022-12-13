from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from .models import *
from generate.models import *
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from generate.MLModel import process_query
from django.core.files.storage import default_storage
import os
from API_generate import settings
import time




@csrf_exempt
# @api_view(['POST'])
def login(request):

    # error - https://stackoverflow.com/questions/39616208/csrf-failed-csrf-token-missing-or-incorrect-in-django-rest-updatemodelmixin

    if request.method == 'POST':
        print(request.body)
        data = json.loads(request.body)
        print(data)
        username = data['username']
        password = data['password']
        
        user = authenticate(username=username, password=password)

        if request.user.is_authenticated:
            return JsonResponse({'message': 'Already Logged in'}, status=200)

        if user is not None:

            auth_login(request, user)
            # print(request.user)
            # if Basic_auth.objects.filter(auth_user=user).exists():
            #     ins = Basic_auth.objects.get(auth_user=user)
            #     ins.is_logged_in = True
            #     ins.save()
            # else:
            #     Basic_auth.objects.create(auth_user=user,is_logged_in=True)
            return JsonResponse({'message': 'success'}, status=200)
        else:
            return JsonResponse({'message': 'invalid creds'}, status=201)

    return JsonResponse({'message': 'wrong method'}, status=400)


@csrf_exempt
def register(request):
    # Not needed
    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return HttpResponse("Enter Same Passwords !!")

        user = User.objects.create_user(username, email, password)
        user.save()

        return redirect('/login')

# Old
# @csrf_exempt
# def setcreds(request, db_type):

#     if request.method == 'POST':

#         # if not request.user.is_authenticated:
#         #     return HttpResponse('You need to login First')

#         if db_type == 'mysql':
#             data = json.loads(request.body)
#             print(data)
#             host = data['host']
#             user = data['user']
#             password = data['password']
#             database = data['database']

#             Database_credentials.objects.create(
#                 host=host,
#                 user=user,
#                 password=password,
#                 database=database,
#                 auth_user='user1',
#                 # auth_user=request.user,
#                 db_type='mysql'
#             )

#         elif db_type == 'mongodb':
#             data = json.loads(request.body)
#             mongourl = data['mongourl']
#             database = data['database']

#             Database_credentials.objects.create(
#                 mongourl=mongourl,
#                 database=database,
#                 auth_user='user1',
#                 # auth_user=request.user,
#                 db_type='mongodb'
#             )

#         ins = Temp.objects.filter(user='user1')[0]
#         result = process_query(ins.file_url)
#         print(result,type(result))
#         # res = json.dumps(result)
#         # print(res)
#         ins.freq_select_query = result['freq_select_query']
#         ins.freq_insert_query = result['freq_insert_query']
#         ins.freq_delete_query = result['freq_delete_query']
#         ins.freq_update_query = result['freq_update_query']
#         ins.freq_tables = ','.join(result['freq_tables'])
#         ins.min_time = result['min_time']
#         ins.max_time = result['max_time']
#         ins.mean_time = result['mean_time']
#         ins.save()
#         return HttpResponse('Success!!')


@csrf_exempt
def setcreds(request, db_type):

    if request.method == 'POST':

        # if not request.user.is_authenticated:
        #     return HttpResponse('You need to login First')

        auth_user = request.user.username
        print('---------------',auth_user)
        # auth_user = 'user2'

        if db_type == 'mysql':

            host = request.POST['host']
            user = request.POST['user']
            password = request.POST['password']
            database = request.POST['database']

            f = request.FILES['file']
            file_name = default_storage.save(f.name, f)
            f_slug = os.path.join(settings.MEDIA_URL, file_name)
            f_type = f.content_type

            # print(host,user,password,database,url)

            if Database_credentials.objects.filter(auth_user=auth_user).exists():
                ins = Database_credentials.objects.get(
                    auth_user=auth_user)
                ins.db_type = 'mysql'
                ins.host = host
                ins.user = user
                ins.password = password
                ins.database = database
                ins.file_slug = f_slug
                ins.file_type = f_type
                ins.save()

            else:
                ins = Database_credentials.objects.create(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    auth_user=auth_user,
                    # auth_user=request.user,
                    db_type='mysql',
                    file_slug=f_slug,
                    file_type=f_type
                )
                ins.save()

        elif db_type == 'mongodb':

            mongourl = request.POST['mongourl']
            database = request.POST['database']

            f = request.FILES['file']
            file_name = default_storage.save(f.name, f)
            f_slug = os.path.join(settings.MEDIA_URL, file_name)
            f_type = f.content_type

            if Database_credentials.objects.filter(auth_user=auth_user).exists():
                ins = Database_credentials.objects.get(
                    auth_user=auth_user)
                ins.db_type = 'mongodb'
                ins.mongourl = mongourl
                ins.database = database
                ins.file_slug = f_slug
                ins.file_type = f_type
                ins.save()

            else:
                ins = Database_credentials.objects.create(
                    mongourl=mongourl,
                    database=database,
                    auth_user=auth_user,
                    # auth_user=request.user,
                    db_type='mongodb',
                    file_slug=f_slug,
                    file_type=f_type
                )
                ins.save()

        result = process_query(ins.file_slug)

        print(result, type(result))

        if Results.objects.filter(auth_user=auth_user).exists():
            Results.objects.get(auth_user=auth_user).delete()

        result_ins = Results.objects.create(
            auth_user=auth_user,
            db_type=ins.db_type,
            db_name=ins.database,
            file_slug=ins.file_slug,
            freq_select_query=result['freq_select_query'],
            freq_insert_query=result['freq_insert_query'],
            freq_delete_query=result['freq_delete_query'],
            freq_update_query=result['freq_update_query'],
            freq_tables=','.join(result['freq_tables']),
            min_time=result['min_time'],
            max_time=result['max_time'],
            mean_time=result['mean_time']
        )
        result_ins.save()

        time.sleep(5)
        return HttpResponse('Success!!')


@csrf_exempt
# @api_view(['GET'])
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return HttpResponse("Logged out")
    else:
        return HttpResponse("Already Logged out")


@csrf_exempt
# @api_view(['GET'])
def checkstatus(request):
    # print(dict(request.session))
    # # print(dict(request.META))
    # print(request.headers['Cookie'])
    print(request.user.username)
    if request.user.is_authenticated:
        return HttpResponse("Logged in")
    return HttpResponse("Logged Out")
