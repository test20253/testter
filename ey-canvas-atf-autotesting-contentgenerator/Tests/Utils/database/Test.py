import pyodbc



connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s,%s;DATABASE=%s;UID=%s;PWD=%s' % (
                "tcp:euwd1canccgsql01.database.windows.net", "1433", "Content","hfitarvp@euwd1canccgsql01", "Kj_=eJCMjhkUs9k_Fy2f27eUS1a5Ze"))

print(connection)
cursor = connection.cursor()
print(cursor)
cursor.execute("SELECT ChannelID,ChannelName FROM Channel")
column_names = [column[0] for column in cursor.description]
print(column_names)
column_names = [column[1] for column in cursor.description]


list_obj = []
        # Iterate over the results and create objects dynamically
print(cursor.fetchall())

for row in cursor.fetchall():
    # Create a dictionary to store column values
    row_dict = dict(zip(column_names, row))
    # Create an object dynamically using the class name `Object`
    resultObject = type('Object', (), row_dict)
    list_obj.append(resultObject)
        # Close the cursor
cursor.close()

print(list_obj)