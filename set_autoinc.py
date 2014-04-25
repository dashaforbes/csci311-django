# run as python manage.py shell < set_autoinc.py
from django.db import connection
from datetime import datetime

now = datetime.now()

cursor = connection.cursor()
cursor.execute("INSERT INTO charts_Issue (id,activity,creator,title,type,stage,status,assigned_to,priority,message_count) VALUES (1800000,?,'test','test','NA','NA','OP','test','NO',0)", [now])
# you'll have to manually delete the row in the admin interface 