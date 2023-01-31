import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import OneClassSVM

filepath =''

def set_filepath(path):
  global filepath
  filepath=path


"""# Read File, Categorize"""
def pre_process():
  global filepath
  # filepath="final_sql_log_text.txt"
  query_file=open(filepath,'r')
  queries=[i.replace('\n','') for i in query_file.readlines()]
  mongo_flag=False

  if "Collection:" in queries[0]:
    mongo_flag=True

  """# Statistics"""

  time_list = []
  type_list = []
  log_list = []
  date_list = []
  user_list = []
  table_list=[]

  if mongo_flag==True:
    for i in queries:
      log_entry = i

      date_split = log_entry.split('T')[0]
      final_date=''
      year,month,day = date_split.split('-')
      final_date = f'{month}/{day}/{year}'
      date_list.append(final_date)

      user_split = log_entry.split(' ')[1]
      user_split = user_split[1:-1]
      user_list.append(user_split)

      keywords_start = ["insert","update","delete","find"]
      for i in keywords_start:
        if (log_entry.find(i)!=-1):
          start = log_entry.find(i)
          type_list.append(i)

      keywords_end = ["ninserted","nupdated","ndeleted","planSummary"]
      for j in keywords_end:
        if (log_entry.find(j)!=-1):
          end = log_entry.find(j)

      log_entry_el = (log_entry[start:end])
      log_list.append(log_entry_el)
      table_used = log_entry_el.split(' ')[1]
      table_list.append(table_used.split('.')[1])
      time = int(log_entry.split()[-1].strip("ms"))
      time_list.append(time)
  else:
    for i in queries:
      sql_list = i.split(' ')
      date_list.append(sql_list[0])
      user_list.append(sql_list[1])
      time_list.append(float(sql_list[2]))
      final_log=""
      for i in range(3,len(sql_list)):
        if(i==len(sql_list)-1):
          final_log+=sql_list[i]
        else:
          final_log+=sql_list[i]+" "
      log_list.append(final_log)
      temp_query=final_log.split(" ")
      type_list.append(temp_query[0].lower())

      final_log=final_log.replace(', ',',')
      temp=final_log.split()           
      for t in range(len(temp)):
        if temp[t].lower()=="from":
          extracted_tables=temp[t+1]
      tables=extracted_tables.split(',')     
      for table in tables:
        table_list.append(table.replace(';',''))

  return [time_list,type_list,log_list,date_list,user_list,table_list,mongo_flag]

def process_query():
  time_list,type_list,log_list,date_list,user_list,table_list,mongo_flag=pre_process()
  query_df = pd.DataFrame(list(zip(log_list, time_list,type_list)),
                columns =['query', 'time','action'])

  min_time = float(query_df.describe()['time']['min'])
  max_time = float(query_df.describe()['time']['max'])
  mean_time = float(query_df.describe()['time']['mean'])



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

    for q in select:
      q=q.replace(', ',',')
      temp=q.split()             
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
    ins=[]
    select=[]
    update=[]
    delete=[]

    freq_tables=[]


    for log_entry in log_list:
      query_split=log_entry.split()
      if query_split[0]=='insert':
        ins.append(log_entry)
      if query_split[0]=='find':
        select.append(log_entry)
      if query_split[0]=='update':
        update.append(log_entry)
      if query_split[0]=='delete':
        delete.append(log_entry)
      
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


  final_data={'freq_insert_query':freq_insert_query,'freq_select_query':freq_select_query,'freq_update_query':freq_update_query,'freq_delete_query':freq_delete_query,'freq_tables':final_freq_tables,"min_time":min_time,'max_time':max_time,'mean_time':mean_time}
  return final_data


# All analytics functions
def queries_per_month_plot():
  df = pd.DataFrame()
  time_list,type_list,log_list,date_list,user_list,table_list,mongo_flag=pre_process()
  df['datetime'] = date_list
  df['clientIP'] = user_list
  df['query_text'] = log_list
  df['execution_time'] = time_list
  df['table_queried_on'] = table_list
  #Convert the datetime column to a Pandas datetime object
  df['date'] = pd.to_datetime(df['datetime'])

  # Group the data by day and count the number of queries submitted on each day
  queries_per_hour = df.groupby(df['date'].dt.month).count()['query_text']
  # print(date_list)
  # Create the time series plot
  result = {
      "labels":list(queries_per_hour.index.values),
      "data":list(queries_per_hour.values)
  }
  return result

def client_ip_execution():
  df = pd.DataFrame()
  time_list,type_list,log_list,date_list,user_list,table_list,mongo_flag=pre_process()
  df['datetime'] = date_list
  user_list = [i.replace('conn','') for i in user_list]
  df['clientIP'] = user_list
  df['query_text'] = log_list
  df['execution_time'] = time_list
  df['table_queried_on'] = table_list
  final_data = []
  for x,y in zip(df['clientIP'],df['execution_time']):
    temp={'x':x,'y':y}
    final_data.append(temp)
  return (final_data)

def most_common_tables():
  df = pd.DataFrame()
  time_list,type_list,log_list,date_list,user_list,table_list,mongo_flag=pre_process()
  df['datetime'] = date_list
  df['clientIP'] = user_list
  df['query_text'] = log_list
  df['execution_time'] = time_list
  df['table_queried_on'] = table_list
  queries_per_table = df.groupby('table_queried_on').count()['query_text']
  top_tables = queries_per_table.sort_values(ascending=False).head(5)
  return {"labels":list(top_tables.index),"data":list(top_tables.values)}

def show_load():
  df = pd.DataFrame()
  time_list,type_list,log_list,date_list,user_list,table_list,mongo_flag=pre_process()
  df['datetime'] = date_list
  df['clientIP'] = user_list
  df['query_text'] = log_list
  df['execution_time'] = time_list
  df['table_queried_on'] = table_list
  # Encode the clientIP column as a numeric value
  le = LabelEncoder()
  te =  LabelEncoder()

  df['clientIP'] = le.fit_transform(df['clientIP'])
  df['table_queried_on'] = te.fit_transform(df['table_queried_on'])

  # Select the columns that will be used for the anomaly detection model
  cols = ['execution_time', 'clientIP', 'table_queried_on']
  X = df[cols]

  # Create the anomaly detection model
  model = OneClassSVM()
  model.fit(X)

  # Use the model to predict which data points are anomalies
  predictions = model.predict(X)

  # Print the indices of the rows that were predicted to be anomalies
  anomaly_indices = [i for i, x in enumerate(predictions) if x == -1]
  anomaly_ips = df.iloc[anomaly_indices]['clientIP'].values

  original_ips = le.inverse_transform(anomaly_ips)
  top_20_ips = Counter(original_ips).most_common(20)

  item_count = df['clientIP'].value_counts()
  # Group the DataFrame by the clientIP column
  grouped = df.groupby('clientIP')

  # Compute summary statistics for the execution_time column in each group
  summary = grouped['execution_time'].describe()

  return {'labels':list(df['clientIP'].value_counts()),'data':list(summary['mean'])}


# Calling all analytics function in a single function

def all_analytics():
  queries_per_month = queries_per_month_plot()
  client_ip_exec = client_ip_execution()
  most_common = most_common_tables()
  load = show_load()

  return{'queries_per_month':queries_per_month,'client_ip_execution':client_ip_exec,'most_common_tables':most_common,'load':load}

# print(process_query())
# print(all_analytics())