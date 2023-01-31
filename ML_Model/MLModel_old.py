import pandas as pd
import numpy as np
from collections import Counter

"""# Read File, Categorize"""
def process_query(filepath):
  mongo_flag=False
  query_file=open(filepath,'r')
  queries=[i.replace('\n','') for i in query_file.readlines()]

  if "Collection:" in queries[0]:
    mongo_flag=True

  """# Statistics"""

  time_list = []
  type_list = []
  log_list = []

  if mongo_flag==True:
    for i in queries:
      log_entry = i

      keywords_start = ["insert","update","delete","find"]
      for i in keywords_start:
        if (log_entry.find(i)!=-1):
          start = log_entry.find(i)
          type_list.append(i)

      keywords_end = ["ninserted","nupdated","ndeleted","planSummary"]
      for j in keywords_end:
        if (log_entry.find(j)!=-1):
          end = log_entry.find(j)

      mongo_query = (log_entry[start:end])
      log_list.append(mongo_query)
      time = int(log_entry.split()[-1].strip("ms"))
      time_list.append(time)
  else:
    for i in queries:
      sql_list = i.split('"')
      time_list.append(float(sql_list[0]))
      type_list.append(sql_list[2])
      log_list.append(sql_list[1])

  query_df = pd.DataFrame(list(zip(log_list, time_list,type_list)),
                columns =['query', 'time','action'])

  min_time = float(query_df.describe()[['time']].min())
  max_time = float(query_df.describe()[['time']].max())
  mean_time = float(query_df.describe()[['time']].mean())

  max_queries = ((query_df[query_df.time == query_df.time.max()]))
  max_queries = list(max_queries['query'])

  min_queries = ((query_df[query_df.time == query_df.time.min()]))
  min_queries = list(min_queries['query'])

  """# Calculating frequently used Queries and tables"""

  #SQL Part


  if mongo_flag==False:
    ins=[]
    select=[]
    update=[]
    delete=[]
    misc=[]
    freq_tables=[]

    for query in log_list:
      temp=query.split()
      first=temp[0].lower()
      if 'insert' in first:
        ins.append(query)
      elif 'select' in first:
        select.append(query)
      elif 'update' in first:
        update.append(query)
      elif 'delete' in first:
        delete.append(query)
      else:
        misc.append(query)

    #Table frequently used for Insert commands

    # - Table Part
    insert_tables=[]
    freq_insert_tables=[]

    for q in ins:
      freq_tables.append(q.split()[2])

    # - Query Part
    freq_insert_queries=[]

    d=dict(Counter(ins))
    sorted_dict = sorted(
      d.items(),
      key = lambda kv: kv[1])
    
    for val in sorted_dict:
      freq_insert_queries.append(val[0])



    # Tables and columns which are frequently used in Select commands
    # - Query Part
    freq_select_queries=[]

    d=dict(Counter(select))
    sorted_dict = sorted(
      d.items(),
      key = lambda kv: kv[1])
    
    for val in sorted_dict:
      freq_select_queries.append(val[0])

    # - Table Part 

    select_tables=[]
    freq_select_tables=[]

    for q in select:
      q=q.replace(', ',',')
      temp=q.split()                 # Could be the reason for error as , can also be follwed by a space so it will go in the list as a new element
      for t in range(len(temp)):
        if temp[t].lower()=="from":
          tables=temp[t+1]
      tables=tables.split(',')     
      for table in tables:
        freq_tables.append(table.replace(';',''))


    # Frequent queries used in Update commands
    # - Query Part
    freq_update_queries=[]

    d=dict(Counter(update))
    sorted_dict = sorted(
      d.items(),
      key = lambda kv: kv[1])
    
    for val in sorted_dict:
      freq_update_queries.append(val[0])

    # - Table part
    update_tables=[]
    freq_update_tables=[]

    for q in update:
      freq_tables.append(q.split()[1])


    # Frequent queries used in Delete commands
    # - Query Part
    freq_delete_queries=[]

    d=dict(Counter(delete))
    sorted_dict = sorted(
      d.items(),
      key = lambda kv: kv[1])
    
    for val in sorted_dict:
      freq_delete_queries.append(val[0])

    # - Table Part

    delete_tables=[]
    freq_delete_tables=[]

    for q in delete:
      freq_tables.append(q.split()[2])



    # Most frequent Query in all different commands
    freq_insert_query = (freq_insert_queries[-1] if len(freq_insert_queries)!=0 else "")
    freq_select_query = (freq_select_queries[-1] if len(freq_select_queries)!=0 else "")
    freq_update_query = (freq_update_queries[-1] if len(freq_update_queries)!=0 else "")
    freq_delete_query = (freq_delete_queries[-1] if len(freq_delete_queries)!=0 else "")

    #Most frequent tables used in all different commands
    final_freq_tables=[]
    d=dict(Counter(freq_tables))
    sorted_dict = sorted(d.items(),key = lambda kv: kv[1],reverse=True)
    
    for val in sorted_dict:
      final_freq_tables.append(val[0])

    try:
      final_freq_tables=final_freq_tables[:4]
    except:
      pass

  # Mongo Part

  else:
    log_list=queries
    ins=[]
    select=[]
    update=[]
    delete=[]

    freq_tables=[]


    for log_entry in log_list:
      keywords_start = ["insert","update","delete","find"]
      for i in keywords_start:
        if (log_entry.find(i)!=-1):
          start = log_entry.find(i)

      keywords_end = ["ninserted","nupdated","ndeleted","planSummary"]
      for j in keywords_end:
        if (log_entry.find(j)!=-1):
          end = log_entry.find(j)

      mongo_query = (log_entry[start:end])
      query_split=mongo_query.split()
      if query_split[0]=='insert':
        ins.append(mongo_query)
      if query_split[0]=='find':
        select.append(mongo_query)
      if query_split[0]=='update':
        update.append(mongo_query)
      if query_split[0]=='delete':
        delete.append(mongo_query)
      
      freq_tables.append(query_split[1].split('.')[1])

      final_freq_tables=[]
      d=dict(Counter(freq_tables))
      sorted_dict = sorted(d.items(),key = lambda kv: kv[1],reverse=True)
      
      for val in sorted_dict:
        final_freq_tables.append(val[0])

      try:
        final_freq_tables=final_freq_tables[:4]
      except:
        pass



    # Frequent Query Extraction part

    # - Insert Part
    freq_insert_queries=[]

    d=dict(Counter(ins))
    sorted_dict = sorted(
      d.items(),
      key = lambda kv: kv[1])
    
    for val in sorted_dict:
      freq_insert_queries.append(val[0])

    # Find Part
    freq_select_queries=[]

    d=dict(Counter(select))
    sorted_dict = sorted(
      d.items(),
      key = lambda kv: kv[1])
    
    for val in sorted_dict:
      freq_select_queries.append(val[0])

    # Update Part
    freq_update_queries=[]

    d=dict(Counter(update))
    sorted_dict = sorted(
      d.items(),
      key = lambda kv: kv[1])
    
    for val in sorted_dict:
      freq_update_queries.append(val[0])

    # Delete Part
    freq_delete_queries=[]

    d=dict(Counter(delete))
    sorted_dict = sorted(
      d.items(),
      key = lambda kv: kv[1])
    
    for val in sorted_dict:
      freq_delete_queries.append(val[0])

    freq_insert_query = (freq_insert_queries[-1] if len(freq_insert_queries)!=0 else "")
    freq_select_query = (freq_select_queries[-1] if len(freq_select_queries)!=0 else "")
    freq_update_query = (freq_update_queries[-1] if len(freq_update_queries)!=0 else "")
    freq_delete_query = (freq_delete_queries[-1] if len(freq_delete_queries)!=0 else "")


  final_data={'freq_insert_query':freq_insert_query,'freq_select_query':freq_select_query,'freq_update_query':freq_update_query,'freq_delete_query':freq_delete_query,'freq_tables':final_freq_tables,"min_time":min_time,'max_time':max_time,'mean_time':mean_time,'max_time_queries':max_queries,'min_time_queries':min_queries}
  return final_data


# print(process_query("https://drive.google.com/file/d/1nuLbp5_TK6P4cQlaSUzT5RO_NfgiETvK/view"))
# print(process_query("C:/Users/taaha/OneDrive/Desktop/HAckathon/media/sql_output.txt"))