import pydantic
import time
import asyncio
import mysql.connector
import hashlib
from decouple import config

start = time.perf_counter()
status = []
approval = []


async def details():
    username = str(input("Enter username: "))
    password = str(input("Enter password: ")).encode()
    hashed_password = hashlib.blake2s(password).hexdigest()
    return {"username": username, "hashed_password": hashed_password}

conn = mysql.connector.connect(

    host=config("DB_HOST", cast=str),
    user=config("DB_USER", cast=str),
    password=config("DB_PASSWORD", cast=str),
    database=config("CURR_DATABASE", cast=str),
    # auth_plugin="mysql_native_password"
)

# coroutines


async def login():
    task = asyncio.create_task(fetch_data())
    await task
    if status:
        if approval:
            if (status[0] == True and approval[0] == True):
                print("login status active")
            elif status[0] == False or approval[0] == False:
                return "check login credentials and try again"
    else:
        print("login status unknown an error occured")


async def Establish_connection():
    if conn.is_connected():
        print("*****Connection Established***********")
    elif conn.is_connected is False:
        print("Error connecting to database ")


async def validate(username: str, password: str):
    if (len(username) and len(password)) > 1:
        status.append(True)

    elif True not in status:
        print("ERROR:No credentials were collected for aproval")
        status.append(False)
    print("****validation analysis complete*****")
    await asyncio.sleep(1)


#@Estsablish_connection()
async def fetch_data():
    task = asyncio.create_task(Establish_connection())
    await asyncio.shield(task)
    try:
        values = await asyncio.shield(details())
    except asyncio.CancelledError as e:
        print(e)
    task2 = asyncio.create_task(
        validate(values["username"], values["hashed_password"]))
    await task2
    myCursor = conn.cursor(dictionary=True)
    myCursor.execute(
        "Select * from user where username = '{}' ".format(values["username"]))
    user = myCursor.fetchone()
    if user['username'] == values["username"]:
        if user['password'] == values["hashed_password"]:
            approval.append(True)
        else:
            print("Incorect password")
    else:
        approval.append(False)
    print("Username: ", user['username'])
    conn.close()
    await asyncio.sleep(3)

asyncio.run(login())
finish = time.perf_counter()
# events loop
print(f'Finished in {round(finish-start, 2)} seconds')
