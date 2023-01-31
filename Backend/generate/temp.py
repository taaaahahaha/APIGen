
import mysql.connector

query = "show index from emp where Key_name = 'PRIMARY';" 
query = "SELECT * from customers;" 

connection = mysql.connector.connect(
host ="0.tcp.in.ngrok.io",
port="12201",
user ="root",
passwd ="techfest1234",
database = "techfest"
)
crsr = connection.cursor()

crsr.execute(query)
ans = crsr.fetchall()
# print(ans)
# for i in ans:
#     print(i)

# print(ans[0][4])
print(ans)

connection.close()