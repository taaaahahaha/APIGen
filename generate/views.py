from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import *
from .MLModel import process_query
from API_generate.settings import MEDIA_DIR
from rest_framework.response import Response
from django.shortcuts import redirect
import json
from django.core.files.storage import default_storage
import os
from API_generate import settings
from generate import execute_mongodb, execute_sqldb
from authentication.models import *


@csrf_exempt
def index(request):
    d = {
        'message': "Index Page"
    }
    return JsonResponse(d)



@csrf_exempt
@api_view(['POST'])
def upload(request):

    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST requests are allowed')

    file = request.FILES['file']

    with open(f"{MEDIA_DIR}/{file.name}", 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
    # return success message
    print(request.user)
    Temp.objects.create(user='user1', file_url=f"{MEDIA_DIR}/{file.name}")

    return redirect('http://localhost:5500/form.html')
    # return Response(status=200)
    # return Response({'message':'Success'},status=200)

@csrf_exempt
@api_view(['POST'])
def uploadfile(request):

    f = request.FILES['file']
    file_name = default_storage.save(f.name, f)
    url = os.path.join(settings.MEDIA_URL,file_name)
    data = {
            'slug' : url,
            'type' : f.content_type
        }
    return JsonResponse(data)
    
    

def find_db_collection(mongo_query):
    query_split=mongo_query.split()
    a = query_split[1].split('.')[1]
    # b = query_split[1].split('.')[0]
    return a

def find_table_sql(q,q_type):
    if q_type == 'select':
        print('query',q)
        q=q.replace(', ',',')
        temp=q.split()             
        for t in range(len(temp)):
            if temp[t].lower()=="from":
                tables=temp[t+1]
        tables=tables.split(',')  
        freq_tables = []   
        for table in tables:
            freq_tables.append(table.replace(';',''))
        return freq_tables
    else:
        if q == '':
            return None
        else:
            return q.split()[2]

@csrf_exempt
# @api_view(['GET'])
def stats(request):
# try:
    # auth_user = request.user
    # auth_user = 'user2'
    auth_user = request.user.username
    

    ins = Results.objects.get(auth_user=auth_user)
    
    if ins.db_type == 'mongodb':

        b = ins.db_name

        d = {
            'min_time' :  ins.min_time,
            'max_time':  ins.max_time,
            'mean_time':ins.mean_time,
            'freq_select_query':
            {
                'query':ins.freq_select_query,
                'desc':'Most Freq select Query',
                'endpoint': '',
                'method':"GET",
            },
            'freq_insert_query':
            {
                'query':ins.freq_insert_query,
                'desc':'Most Freq Insert Query',
                'endpoint': '',
                'method':"POST",
            },
            'freq_delete_query':
            {
                'query':ins.freq_delete_query,
                'desc':'Most Freq delete Query',
                'endpoint': '',
                'method':"DELETE",
            },
            'freq_update_query':
            {
                'query':ins.freq_update_query,
                'desc':'Most Freq update Query',
                'endpoint': '',
                'method':"PUT",
            },
            'freq_tables':
            {}
        
        }

        a = find_db_collection(ins.freq_insert_query)
        d["freq_insert_query"]["endpoint"] = f"/{b}/{a}/freq/"
        a = find_db_collection(ins.freq_update_query)
        d["freq_update_query"]["endpoint"] = f"/{b}/{a}/freq/"
        a = find_db_collection(ins.freq_delete_query)
        d["freq_delete_query"]["endpoint"] = f"/{b}/{a}/freq/"
        a = find_db_collection(ins.freq_select_query)
        d["freq_select_query"]["endpoint"] = f"/{b}/{a}/freq/"

        li = list(ins.freq_tables.split(','))
        print(li,type(li))


        table_index = 0
        query_number = 0

        while table_index<len(li):
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'Select all',
                    'endpoint': f'/{b}/{li[table_index]}/',
                    'method':"GET",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'filter by column',
                    'endpoint': f"/{b}/{li[table_index]}?filter='parameter1=value1 ,parameter2=value2'",
                    'method':"GET",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'insert',
                    'endpoint': f"/{b}/{li[table_index]}",
                    'method':"POST",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'update',
                    'endpoint': f"/{b}/{li[table_index]}/<id>",
                    'method':"PUT",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'delete',
                    'endpoint': f"/{b}/{li[table_index]}/<id>",
                    'method':"DELETE",
                }
            query_number+=1

            table_index += 1


        # for x in range(len(li)):
        #     d["freq_tables"][x] = {
        #             'tablename':li[x],
        #             'desc':'',
        #             'endpoint': f'/{b}/{li[x]}/',
        #             'method':"GET, POST, PUT, DELETE",
        #         }
    
    elif ins.db_type == 'mysql':

        d = {
            'min_time' :  ins.min_time,
            'max_time':  ins.max_time,
            'mean_time':ins.mean_time,
            'freq_select_query':
            {
                'query':ins.freq_select_query,
                'desc':'Most Freq select Query',
                'endpoint': '',
                'method':"GET",
            },
            'freq_insert_query':
            {
                'query':ins.freq_insert_query,
                'desc':'Most Freq Insert Query',
                'endpoint': '',
                'method':"POST",
            },
            'freq_delete_query':
            {
                'query':ins.freq_delete_query,
                'desc':'Most Freq delete Query',
                'endpoint': '',
                'method':"DELETE",
            }, 
            'freq_update_query':
            {
                'query':ins.freq_update_query,
                'desc':'Most Freq update Query',
                'endpoint': '',
                'method':"PUT",
            },
            'freq_tables':
            {}
        
        }

        b = ins.db_name

        a = find_table_sql(ins.freq_insert_query,'insert')
        d["freq_insert_query"]["endpoint"] = f"/{b}/{a}/freq/"
        a = find_table_sql(ins.freq_update_query,'update')
        d["freq_update_query"]["endpoint"] = f"/{b}/{a}/freq/"
        a = find_table_sql(ins.freq_delete_query,'delete')
        d["freq_delete_query"]["endpoint"] = f"/{b}/{a}/freq/"
        a = find_table_sql(ins.freq_select_query,'select')
        d["freq_select_query"]["endpoint"] = f"/{b}/{a}/freq/"

        li = list(ins.freq_tables.split(','))

        table_index = 0
        query_number = 0

        while table_index<len(li):
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'Select all',
                    'endpoint': f'/{b}/{li[table_index]}/',
                    'method':"GET",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'filter by column',
                    'endpoint': f"/{b}/{li[table_index]}?col_filter='column1=value1 ,column2=value2'",
                    'method':"GET",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'filter by row',
                    'endpoint': f"/{b}/{li[table_index]}?row_filter='where column1 operator value1'",
                    'method':"GET",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'filter by row and column',
                    'endpoint': f"/{b}/{li[table_index]}?col_filter='column1=value1 ,column2=value2'&row_filter='where column1 operator value1'",
                    'method':"GET",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'insert',
                    'endpoint': f"/{b}/{li[table_index]}",
                    'method':"POST",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'update',
                    'endpoint': f"/{b}/{li[table_index]}/<id>",
                    'method':"PUT",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'delete',
                    'endpoint': f"/{b}/{li[table_index]}/<id>",
                    'method':"DELETE",
                }
            query_number+=1

            table_index += 1
        

    return JsonResponse(d)
    # return Response(status=200)
    # return Response({'message':'Success'},status=200)
    # except Ex:
    #     return JsonResponse({'message':'You are accessing this page from different account, please switch your account or upload files from this account.'})





@csrf_exempt
# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
def dynamic_access(request, database, table):

    # auth_user = 'user1'
    auth_user = request.user.username
    # print(auth_user)
    result_ins = Results.objects.get(auth_user=auth_user,db_name=database)
    
    db_ins = Database_credentials.objects.get(auth_user=auth_user)
    database_type = db_ins.db_type

    if database_type == 'mysql':
        crsr, connection = execute_sqldb.connect(db_ins.host, db_ins.user, db_ins.password, db_ins.database)
    elif database_type == 'mongodb':
        pass
    

    if request.method == "GET":

        row_filters = request.GET.get('row_filter', None)
        col_filters = request.GET.get('col_filter', None)
        # print(row_filters,col_filters)
        li = []
        if col_filters == None:
            col_filters = '*'
            li.append('*')
        else:
            for x in col_filters[1:-1].split(','):
                li.append(x.split('=')[1])
            col_filters = ','.join(li)
        if row_filters == None:
            row_filters = ''
        else:
            temp = ''
            temp_li = []
            for x in row_filters[1:-1].split(','):
                temp_li = x.split('=')
                temp += f"{temp_li[0]}='{temp_li[1]}' and "
            row_filters = temp[:-4]
            row_filters = f'WHERE {row_filters}'

        

        query = f'''SELECT {col_filters} FROM {table} {row_filters}'''

        # print('query',query)
        if database_type == 'mysql':
            success, ans = execute_sqldb.view(crsr,connection,query)
            execute_sqldb.disconnect(connection)
            if success == True:
                d = {}
                i=0
                while i<len(ans):
                    d[i] = ans[i]
                    i+=1
                return JsonResponse({'schema':li,'data':d})
            else:
                return JsonResponse({'Error':ans})
        elif database_type == 'mongodb':
            pass
        
        
    elif request.method == 'POST':
        # query = 
        pass
        
        
        
    elif request.method == 'PUT':
        # query 
        pass
    elif request.method == 'DELETE':
        # query 
        pass
        

    else:
        return HttpResponse(f"Wrong Method")
    return HttpResponse('test')


@csrf_exempt
# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
def frequent_query(request, database, table):

    # auth_user = 'user1'
    # print('zz',request.user.username)
    auth_user = request.user.username

    result_ins = Results.objects.get(auth_user=auth_user,db_name=database)
    
    db_ins = Database_credentials.objects.get(auth_user=auth_user)
    database_type = db_ins.db_type

    if database_type == 'mysql':
        crsr, connection = execute_sqldb.connect(db_ins.host, db_ins.user, db_ins.password, db_ins.database)
    elif database_type == 'mongodb':
        pass

    if request.method == "GET":
        query = result_ins.freq_select_query
        if database_type == 'mysql':
            success, ans = execute_sqldb.view(crsr,connection,query)
            execute_sqldb.disconnect(connection)
            if success == True:
                d = {}
                i=0
                while i<len(ans):
                    d[i] = ans[i]
                    i+=1
                return JsonResponse({'data':d})
            else:
                return JsonResponse({'Error':ans})
        elif database_type == 'mongodb':
            pass

    elif request.method == 'POST':
        query = result_ins.freq_insert_query
        if database_type == 'mysql':
            success, ans = execute_sqldb.insert(crsr,connection,query)
            execute_sqldb.disconnect(connection)
            print(ans)
            if success == True:
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'Error':ans})
        elif database_type == 'mongodb':
            pass

    elif request.method == 'PUT':
        query = result_ins.freq_update_query
        if database_type == 'mysql':
            success, ans = execute_sqldb.update(crsr,connection,query)
            execute_sqldb.disconnect(connection)
            print(ans)
            if success == True:
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'Error':ans})
        elif database_type == 'mongodb':
            pass
        
    elif request.method == 'DELETE':
        query = result_ins.freq_delete_query
        if database_type == 'mysql':
            success, ans = execute_sqldb.delete(crsr,connection,query)
            execute_sqldb.disconnect(connection)
            print(ans)
            if success == True:
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'Error':ans})
        elif database_type == 'mongodb':
            pass
        

    else:
        return HttpResponse(f"Wrong Method")


