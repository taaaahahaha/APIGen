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
from bson import json_util
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
    elif q_type== 'update':
        if q == '':
            return None
        else:
            return q.split()[1]
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
    auth_user = 'user1'
    # auth_user = request.user.username
    

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
                'desc':'Most frequently executed SELECT query',
                'endpoint': '',
                'method':"GET",
            },
            'freq_insert_query':
            {
                'query':ins.freq_insert_query,
                'desc':'Most frequently executed INSERT query',
                'endpoint': '',
                'method':"POST",
            },
            'freq_delete_query':
            {
                'query':ins.freq_delete_query,
                'desc':'Most frequently executed DELETE query',
                'endpoint': '',
                'method':"DELETE",
            },
            'freq_update_query':
            {
                'query':ins.freq_update_query,
                'desc':'Most frequently executed UPDATE query',
                'endpoint': '',
                'method':"PUT",
            },
            'freq_tables':
            {}
        
        }

        a = find_db_collection(ins.freq_insert_query)
        d["freq_insert_query"]["endpoint"] = f"/api/v1/{b}/{a}/freq/"
        a = find_db_collection(ins.freq_update_query)
        d["freq_update_query"]["endpoint"] = f"/api/v1/{b}/{a}/freq/"
        a = find_db_collection(ins.freq_delete_query)
        d["freq_delete_query"]["endpoint"] = f"/api/v1/{b}/{a}/freq/"
        a = find_db_collection(ins.freq_select_query)
        d["freq_select_query"]["endpoint"] = f"/api/v1/{b}/{a}/freq/"

        li = list(ins.freq_tables.split(','))
        print(li,type(li))


        table_index = 0
        query_number = 0

        while table_index<len(li):
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'Select all',
                    'endpoint': f'/api/v1/{b}/{li[table_index]}/',
                    'method':"GET",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'filter by column',
                    'endpoint': f"/api/v1/{b}/{li[table_index]}?filter='parameter1=value1 ,parameter2=value2'",
                    'method':"GET",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'insert',
                    'endpoint': f"/api/v1/{b}/{li[table_index]}",
                    'method':"POST",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'update',
                    'endpoint': f"/api/v1/{b}/{li[table_index]}/<id>",
                    'method':"PUT",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'delete',
                    'endpoint': f"/api/v1/{b}/{li[table_index]}/<id>",
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
                'desc':'Most frequently executed SELECT query',
                'endpoint': '',
                'method':"GET",
            },
            'freq_insert_query':
            {
                'query':ins.freq_insert_query,
                'desc':'Most frequently executed INSERT query',
                'endpoint': '',
                'method':"POST",
            },
            'freq_delete_query':
            {
                'query':ins.freq_delete_query,
                'desc':'Most frequently executed DELETE query',
                'endpoint': '',
                'method':"DELETE",
            }, 
            'freq_update_query':
            {
                'query':ins.freq_update_query,
                'desc':'Most frequently executed UPDATE query',
                'endpoint': '',
                'method':"PUT",
            },
            'freq_tables':
            {}
        
        }

        b = ins.db_name

        a = find_table_sql(ins.freq_insert_query,'insert')
        d["freq_insert_query"]["endpoint"] = f"/api/v1/{b}/{a}/freq/"
        a = find_table_sql(ins.freq_update_query,'update')
        print('p',a)
        d["freq_update_query"]["endpoint"] = f"/api/v1/{b}/{a}/freq/"
        a = find_table_sql(ins.freq_delete_query,'delete')
        d["freq_delete_query"]["endpoint"] = f"/api/v1/{b}/{a}/freq/"
        a = find_table_sql(ins.freq_select_query,'select')
        d["freq_select_query"]["endpoint"] = f"/api/v1/{b}/{a[0]}/freq/"

        li = list(ins.freq_tables.split(','))

        table_index = 0
        query_number = 0

        while table_index<len(li):
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'Recommended API for fetching data',
                    'endpoint': f'/api/v1/{b}/{li[table_index]}/',
                    'method':"GET",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'Recommended API for filtering by column',
                    'endpoint': f"/api/v1/{b}/{li[table_index]}?col_filter='column1,column2'",
                    'method':"GET",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'Recommended API for filtering by row',
                    'endpoint': f"/api/v1/{b}/{li[table_index]}?row_filter='column1 = value1'",
                    'method':"GET",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'Recommended API for filtering by row and column',
                    'endpoint': f"/api/v1/{b}/{li[table_index]}?col_filter='column1,column2'&row_filter='column1 = value1'",
                    'method':"GET",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'Recommended API for inserting data',
                    'endpoint': f"/api/v1/{b}/{li[table_index]}/",
                    'method':"POST",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'Recommended API for updating data',
                    'endpoint': f"/api/v1/{b}/{li[table_index]}/<id>",
                    'method':"PUT",
                }
            query_number += 1
            d["freq_tables"][query_number] = {
                    'tablename':li[table_index],
                    'desc':'Recommended API for deleting data',
                    'endpoint': f"/api/v1/{b}/{li[table_index]}/<id>",
                    'method':"DELETE",
                }
            query_number+=1

            table_index += 1
        
    # print(ins.analytics)
    return JsonResponse({'data':d,'analytics':ins.analytics})
    # return JsonResponse(d)
    # return Response(status=200)
    # return Response({'message':'Success'},status=200)
    # except Ex:
    #     return JsonResponse({'message':'You are accessing this page from different account, please switch your account or upload files from this account.'})





@csrf_exempt
# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
def dynamic_access(request, database, table, id=None):

    auth_user = 'user1'
    # auth_user = request.user.username
    # print(auth_user)
    result_ins = Results.objects.get(auth_user=auth_user,db_name=database)
    
    db_ins = Database_credentials.objects.get(auth_user=auth_user)
    database_type = db_ins.db_type

    if database_type == 'mysql':
        crsr, connection = execute_sqldb.connect(db_ins.host, db_ins.port, db_ins.user, db_ins.password, db_ins.database)
    elif database_type == 'mongodb':
        db = execute_mongodb.connect(db_ins.mongourl, db_ins.database)
    

    if request.method == "GET":

        row_filters = request.GET.get('row_filter', None)
        col_filters = request.GET.get('col_filter', None)
        # print(col_filters)
        # print(row_filters,col_filters)

        if database_type == 'mysql':
            li = []
            if col_filters == None:
                col_filters = '*'
                li.append('*')
            else:
                # for x in col_filters[1:-1].split(','):
                #     li.append(x.split('=')[1])
                col_filters = col_filters[1:-1]
            if row_filters == None:
                row_filters = ''
            else:
                temp = ''
                temp_li = []
                for x in row_filters[1:-1].split(','):
                    temp_li = x.split('=')
                    if type(temp_li[1]) == int:
                        t =  int(temp_li[1])
                    else:
                        t = f"'{temp_li[1]}'"
                    temp += f"{temp_li[0]}={t} and "
                row_filters = temp[:-4]
                row_filters = f'WHERE {row_filters}'

            

            query = f'''SELECT {col_filters} FROM {table} {row_filters}'''

            print('q',query)
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
            

            filters = request.GET.get('filters', None)


            collection = table

            if filters == None:
                success, res = execute_mongodb.find_all(db, collection)
                res = list(res)

                d = {}

                i=0
                while i<len(res):
                    d[i] = res[i]
                    i+=1


                if success == True:
                    d = json.loads(json_util.dumps(d))
                    return JsonResponse(d)
                else:
                    return JsonResponse({'Error':ans})

            else:
                li = filters[1:-1].split(',')
                d = {}
                for x in li:
                    p,v = x.split('=')
                    d[p]=v
                print(d)
                success, res = execute_mongodb.find(db,collection,d)
                res = list(res)

                d = {}

                i=0
                while i<len(res):
                    d[i] = res[i]
                    i+=1
                if success == True:
                    d = json.loads(json_util.dumps(d))
                    return JsonResponse(d)
                else:
                    return JsonResponse({'Error':ans})
                

            
        
        
    elif request.method == 'POST':


        if database_type == 'mysql':
            # print(request.body)
            data = json.loads(request.body)
            # print(data)
            column = data['column']
            values = data['values']
            # print(column,type(column))

            if len(column) == 0:
                col_data = ''
            else:
                col_data = ', '.join(column)
                col_data = f'''({col_data})'''
            # print(col_data)

            if len(values) == 0:
                return JsonResponse({'message':"No Values Provided"})
            else:
                li = []
                for x in values:
                    li.append(str(x) if type(x)==int else f"'{x}'")
                print(values,li)
                val_data = ', '.join(li)
                val_data = f'''({val_data})'''
            # print(val_data)
            query = f'''INSERT INTO {table} {col_data} VALUES {val_data}'''
            print(query)
        
        
            success, ans = execute_sqldb.insert(crsr,connection,query)
            execute_sqldb.disconnect(connection)
            if success == True:
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'Error':ans})


        elif database_type == 'mongodb':
            collection = table
            data = json.loads(request.body)
            # print(data)
            success, res = execute_mongodb.insert_many(db,collection,data)

    
            if success == True:
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'Error':ans})
            
        
        
        
    elif request.method == 'PUT':
        
        if database_type == 'mysql':

            data = json.loads(request.body)
            column = data['column']
            values = data['values']
            # x = data.get('filter',None)
            # print(x)
            print(column,values)
            # print(id)

            query = f'''show index from {table} where Key_name = 'PRIMARY' ;'''
            success, ans = execute_sqldb.view(crsr,connection,query)
            
            if success != True:
                return JsonResponse({'Error':ans})
            primary_key = ans[0][4]
            
            if type(id)==int:
                id=str(id)

            t = ''
            for i in range(len(column)):
                t += f''' {column[i]} = "{values[i]}",'''
            val_data = t[1:-1]

            query = f'''UPDATE {table} SET {val_data} WHERE {primary_key}={id};'''
            print(query,'query')

            print('id',id)
            
            if data.get('filter',None):
                
                x = data['filter']
                
                column = x['column']
                values = x['values']

                print(column,values,'l')
                
                t = ''

                for i in range(len(column)):
                    t+= f"{column[i]} = '{values[i]}' and " # NOT done
                t = t[:-4]
                
                query = f'''UPDATE {table} SET {val_data} WHERE {t};'''



            success, ans = execute_sqldb.update(crsr,connection,query)
            execute_sqldb.disconnect(connection)
            if success == True:
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'Error':ans})


        elif database_type == 'mongodb':
            collection = table
            data = json.loads(request.body)
            new_data = data['data']
            filters = data['filter']
            success, res = execute_mongodb.update(db,collection,new_data,filters)

            if success == True:
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'Error':ans})

        
    elif request.method == 'DELETE':
        # print('hi')
        
        if database_type == 'mysql':
            data = json.loads(request.body)


            query = f'''show index from {table} where Key_name = 'PRIMARY' ;'''
            success, ans = execute_sqldb.view(crsr,connection,query)
            
            if success != True:
                return JsonResponse({'Error':ans})
            primary_key = ans[0][4]
            
            if type(id)==int:
                id=str(id)

            query = f'''DELETE FROM {table} WHERE {primary_key}={id};'''
            print(query,'query')


            if data.get('filter',None):
                
                x = data['filter']
                
                column = x['column']
                values = x['values']

                print(column,values,'l')
                
                t = ''

                for i in range(len(column)):
                    t+= f"{column[i]} = '{values[i]}' and " # NOT done
                t = t[:-4]
                
                query = f'''DELETE FROM {table} WHERE {t};'''
                print(query)



            success, ans = execute_sqldb.update(crsr,connection,query)
            execute_sqldb.disconnect(connection)
            if success == True:
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'Error':ans})


        elif database_type == 'mongodb':
            collection = table
            data = json.loads(request.body)

            filters = data['filter']
            success, res = execute_mongodb.delete(db,collection,filters)

            if success == True:
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'Error':ans})
        

    else:
        return HttpResponse(f"Wrong Method")
    return HttpResponse('test')


@csrf_exempt
# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
def frequent_query(request, database, table):

    auth_user = 'user1'
    # print('zz',request.user.username)
    # auth_user = request.user.username

    result_ins = Results.objects.get(auth_user=auth_user,db_name=database)
    
    db_ins = Database_credentials.objects.get(auth_user=auth_user)
    database_type = db_ins.db_type

    if database_type == 'mysql':
        crsr, connection = execute_sqldb.connect(db_ins.host,db_ins.port, db_ins.user, db_ins.password, db_ins.database)
    elif database_type == 'mongodb':
        db = execute_mongodb.connect(db_ins.mongourl, db_ins.database)

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
            print(query)
            collection = query.split()[1].split('.')[1]
            
            s = query[query.index('{'):query.index('}')+1]
            d = json.loads(s)
            success, res = execute_mongodb.find(db,collection,d)
            
            res = list(res)

            d = {}

            i=0
            while i<len(res):
                d[i] = res[i]
                i+=1
            if success == True:
                d = json.loads(json_util.dumps(d))
                return JsonResponse(d)
            else:
                return JsonResponse({'Error':res})



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

            print(query)
            collection = query.split()[1].split('.')[1]

            s = query[query.index('{'):query.index('}')+1]
            d = json.loads(s)

            success, res = execute_mongodb.insert_many(db,collection,[d])

    
            if success == True:
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'Error':res})

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
            print(query)
            collection = query.split()[1].split('.')[1]

            s1 = query[query.index('{'):query.index('}')+1]
            query = query[query.index('}')+1:]
            
            s2 = query[query.index('{'):len(query)-query[::-1].index('}')]
            s2 = s2.strip()[1:-1]
            s2 = s2[s2.index('{'):s2.index('}')+1]
            d1 = json.loads(s1)
            d2 = json.loads(s2)
            # print(d1,d2)
            # print(s1,s2,'l')

            success, res = execute_mongodb.update(db,collection,d2,d1)

    
            if success == True:
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'Error':res})
        
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
            print(query)
            collection = query.split()[1].split('.')[1]

            s = query[query.index('{'):query.index('}')+1]
            d = json.loads(s)

            # print(d)

            success, res = execute_mongodb.delete(db,collection,d)

    
            if success == True:
                return JsonResponse({'message':'success'})
            else:
                return JsonResponse({'Error':res})
        

    else:
        return HttpResponse(f"Wrong Method")


