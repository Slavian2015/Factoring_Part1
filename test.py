from sqlalchemy import *

db = create_engine('sqlite:///db.sqlite3')

echo = True  # Try changing this to True and see what happens

metadata = MetaData(bind=db)


users = Table('User', metadata,
    Column('id', Integer, primary_key=True),
    Column('password', String(100)),
    Column('name', String(1000)),
    Column('tel', String(1000)),
    Column('stat', Boolean, default=False),
    Column('employee', Boolean, default=False),
    Column('depart', String(1000)),
)

dep = Table('Depart', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('code', String(100)),

)

#
#
# i = users.insert()
# i.execute(name='Tom', tel=30, password='secret', stat=True, employee=True, depart=30)
# i.execute({'name': 'John', 'age': 42},
#           {'name': 'Susan', 'age': 57},
#           {'name': 'Carl', 'age': 33})

dep.create()
# users.create()
# users.drop(db)

s = users.select()
rs = s.execute()

row = rs.fetchone()
# print ('Id:', row)
# print ('Name:', row['name'])
# print ('tel:', row.tel)
# print ('Password:', row[users.c.password])

for row in rs:
    print (row.name, 'tel :', row.tel, 'Stat :', row.employee)

