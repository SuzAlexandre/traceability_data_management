import pyodbc
import datetime
import random

# Barcode structure PAASSSSYYMMDDhhmmss
# setup marking constant of data
plant='S'

def generate_serial_number():
    print("hello")

def read_caster_list(conn):
    # create connection cursor 
    cursor=conn.cursor()

    # initialize data
    results=[]
    caster_list=[]

    # send request
    cursor.execute('select caster_ID, caster_name from caster_list')
    columns = [column[0] for column in cursor.description]

    # Compile all as dicitonnary
    for row in cursor:
        results.append(dict(zip(columns,row)))
    
    # Save caster names only as an array
    for result in results:
        caster_list.append(result.get('caster_name'))

    # Commit connection changes
    conn.commit()

    return caster_list

def generate_SO_number(conn,quantity):
    # create connection cursor 
    cursor=conn.cursor()

    # list of data to put in database
    SO_number=0
    revision=0
    part_type=['Front knuckle','Rear knuckle', 'FLCA', 'RLCA']
    part_hand=['LH','RH']

    for cmpt in range(99,quantity):
        SO_number=cmpt
        revision=random.randrange(99)
        part_description=random.choice(part_type) + ' - ' + random.choice(part_hand)

        cursor.execute("insert into SO_numbers_list(SO_number, revision_number, part_description) values (?,?,?)",SO_number,revision,part_description)
        conn.commit()

def read_SO_numbers(conn):
    # create connection cursor 
    cursor=conn.cursor()

    # initialize data
    results=[]
    SO_numbers=[]

    # send request
    cursor.execute('select SO_number from SO_numbers_list')
    columns = [column[0] for column in cursor.description]

    # Compile all as dicitonnary
    for row in cursor:
        results.append(dict(zip(columns,row)))
    
    # Save caster names only as an array
    for result in results:
        SO_numbers.append(result.get('SO_number'))

    # Commit connection changes
    conn.commit()

    return SO_numbers

def generate_serial_numbers(plant, caster_list, SO_numbers_list, quantity,duration,):
    base_time=datetime.datetime.today()
    date_list=[]

    # Loop on quantities
    for cmp in range(quantity):
<<<<<<< HEAD
        new_date=base_time-datetime.timedelta(seconds=random.randrange(0,duration*24*3600))
        date_string = '{0:02d}'.format(new_date.year)[2:4] +'{0:02d}'.format(new_date.month)+'{0:02d}'.format(new_date.day)+'{0:02d}'.format(new_date.hour)+'{0:02d}'.format(new_date.minute)+'{0:02d}'.format(new_date.second)
=======
        new_date=base_time#-datetime.timedelta(seconds=random.randrange(0,duration*24*3600))
        date_string = '{0:02d}'.format(new_date.year)[2:4] +'{0:02d}'.format(new_date.month)+'{0:02d}'.format(new_date.day)+'{0:02d}'.format(new_date.hour)+'{0:02d}'.format(new_date.minute)+'{0:02d}'.format(new_date.second)
        # single_record={'date': new_date, 'date_string': date_string}
>>>>>>> 4c2d14af75294fd5595f1b5d95ddd41f58f7dab5
        
        # generate random serial numbers
        serial_number= plant + random.choice(caster_list) + '{0:02d}'.format(random.choice(SO_numbers_list)) + date_string
        
        # Append the list
        date_list.append({'date': new_date, 'serial_number': serial_number})
    
    return date_list

def push_serial_number(conn, serial_numbers):
    # setup cursor
    cursor=conn.cursor()

    for serial_number in serial_numbers:
        cursor.execute("insert into part_serial_numbers(serial_number,register_time) values (?,?)",serial_number.get('serial_number'),serial_number.get('date'))
        conn.commit()



# create database connection
conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=10.41.32.4;"
    "Database=SZ_001;"
    "Trusted_Connection=yes;")

# getting the caster list from database
caster_list = read_caster_list(conn)

# generate_SO_number(conn,1000) -- Activate only once
# generating SO numbers

# getting SO number list from the database
SO_numbers = read_SO_numbers(conn)

# generate random part number in time range
serial_numbers = generate_serial_numbers(plant,caster_list,SO_numbers,100000,365) #quantity and duration in days
print('All numbers generated')

# move data to database
push_serial_number(conn, serial_numbers)
print('All set')

conn.close()