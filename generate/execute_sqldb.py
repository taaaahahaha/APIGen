import sqlite3
import mysql.connector


# # For MYSQL Server
# connection = mysql.connector.connect(
# host ="localhost",
# user ="root",
# passwd ="root",
# database = "testing"
# )

# # For SQLite3
# connection = sqlite3.connect("testdata.db")





def connect(host,port,user,password,database):
    connection = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    passwd=password,
    database=database
    )
    crsr = connection.cursor()
    return crsr, connection


# def create_table():
    # sql_command = """CREATE TABLE emp (
    # staff_number INTEGER PRIMARY KEY,
    # fname VARCHAR(20),
    # lname VARCHAR(30),
    # gender CHAR(1),
    # joining DATE);"""
    # crsr.execute(sql_command)

def insert(crsr,connection,query):
    
    # sql_command = """INSERT INTO emp VALUES (23, "Rishabh",\
    # "Bansal", "M", "2014-03-28");"""
    # crsr.execute(sql_command)
    # sql_command = """INSERT INTO emp VALUES (1, "Bill", "Gates",\
    # "M", "1980-10-28");"""
    # crsr.execute(sql_command)
    try:
        crsr.execute(query)
        connection.commit()
        return True, None
    except Exception as e:
        print(e)
        return False, str(e)

def view(crsr,connection,query):
    # sql_command = """SELECT * FROM emp;"""

    try:
        crsr.execute(query)
        ans = crsr.fetchall()
        # print(ans)
        # for i in ans:
        #     print(i)
        return True, ans
    except Exception as e:
        print(e)
        return False, str(e)
    
def update(crsr,connection,query):
    # sql_command = """UPDATE emp SET lname = "Jyoti" WHERE fname="Rishabh";"""
    try:
        crsr.execute(query)
        connection.commit()
        return True, None
    except Exception as e:
        print(e)
        return False, e
 
def delete(crsr,connection,query):
    # sql_command = """DELETE FROM emp WHERE fname="Rishabh";"""
    try:
        crsr.execute(query)
        connection.commit()
        return True, None
    except Exception as e:
        print(e)
        return False, e
 
# def drop():
#     sql_command = """DROP TABLE emp;"""
#     crsr.execute(sql_command)
#     connection.commit()


def disconnect(connection):
    connection.close()
    return True


# select [indexMapID],[code],[type],[tableName],[fieldList],[foreignKey] from IndexMap  where tableName='sdsstileall' order by [indexMapId]
# print(freq_insert_query,freq_select_query,freq_update_query,freq_delete_query)  +4
# print(freq_insert_table,freq_select_table,freq_update_table,freq_delete_table)  *4  = 20