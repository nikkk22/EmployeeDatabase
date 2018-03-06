import socket
import re
import pymongo
from pymongo import MongoClient

HOST, PORT = '', 52557
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print ('Starting web-server on port ' + str(PORT))

def sendError(client_socket):
    http_response = """\
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *

""" + "The employee already exists"

    client_socket.sendall(http_response.encode())
    client_socket.close()

def sendResponse(client_socket):
    http_response = """\
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *

""" + "The employee is inserted into the database"

    client_socket.sendall(http_response.encode())
    client_socket.close()

def sendEmployeeRecord(client_socket, record):
    print ("Sending back to client")
    http_response = """\
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *

""" + str(record)

    client_socket.sendall(http_response.encode())
    client_socket.close()

def sendNoDataPresent(client_socket, nonames):
    print ("Sending back to client")
    http_response = """\
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *

""" + str(nonames)

    client_socket.sendall(http_response.encode())
    client_socket.close()

def sendNames(client_socket, names):
    print ("Sending back to client")
    http_response = """\
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *

""" + str(names)

    client_socket.sendall(http_response.encode())
    client_socket.close()

while True:
    #Connecting to mongodb
    client = MongoClient()
    #Opening database
    db = client.EmployeeDatabase
    
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024)
    strr = request.decode()
    print (repr(strr))
    if (strr.find("AddEmp") != -1):
        print("Got request to add an employee detail")
        indexOPAdd = strr.find("fName")
        indexHTTP = strr.find(" HTTP")
        fetchData = strr[indexOPAdd:indexHTTP]
        matchedData = re.search("fName=(\w+)", fetchData)
        firstName = matchedData.group(1)
        matchedData = re.search("mName=(\w+)", fetchData)
        middleName = matchedData.group(1)
        matchedData = re.search("lName=(\w+)", fetchData)
        lastName = matchedData.group(1)
        matchedData = re.search("email=([\w\.]+)", fetchData)
        email = matchedData.group(1)
        print ("email is", email)
        matchedData = re.search("contactNumber=(\w+)", fetchData)
        contactNumber = matchedData.group(1)
        matchedData = re.search("manager=([\w+]+)", fetchData)
        manager = matchedData.group(1)
        manager = manager.replace("+"," ")
        matchedData = re.search("description=([\w+]+)", fetchData)
        description = matchedData.group(1)
        description = description.replace("+"," ")
        print (description)
        matchedData = re.search("gender=(\w+)", fetchData)
        gender = matchedData.group(1)
    
        #Create a dictionary
        empData={}
        empData['firstName'] = firstName
        empData['lastName'] = lastName
        empData['middleName'] = middleName
        empData['email'] = email
        empData['contactNumber'] = contactNumber
        empData['manager'] = manager
        empData['description'] = description
        empData['gender'] = gender
        #search for the data if exists in mongodb
        if (db.empDB.find({"email" : email}).count() > 0):
            print ("Found an element already. Not inserting")
            sendError(client_socket)
        else:
            #insert into mongodb
            db.empDB.insert_one(empData)
            print ("Data inserted")
            sendResponse(client_socket)
        
    elif (strr.find("SearchEmployee") != -1):
        print("Got request to search an employee detail")
        indexOPSearch = strr.find("email")
        indexHTTP = strr.find(" HTTP")
        searchData = strr[indexOPSearch:indexHTTP]
        matchedData = re.search("email=([\w+\.]+)", searchData)
        email = matchedData.group(1)
        if (db.empDB.find({"email" : email}).count() == 1):
            print ("Data found. Returning to client")
            ret_ = list()
            ret = {}
            r_ = db.empDB.find({"email" : email})
            for r in r_:
                ret["Email"] = r['email']
                ret["Manager"] = r['manager']
                ret["First Name"] = r['firstName']
                ret["Last Name"] = r['lastName']
                ret["Contact Number"] = r['contactNumber']
                ret["Description"] = r['description']
                ret["Gender"] = r['gender']
                ret["Middle Name"] = r['middleName']
            ret_.append(ret)
            sendEmployeeRecord(client_socket, ret_)
        elif (db.empDB.find({"email" : email}).count() == 0):
            found = 0
            count = 0
            emailOne = ""
            matchedNames = {}
            matchedNames_=list()
            ret = db.empDB.find({})
            for r in ret:
                if (r['email'].find(email) != -1):
                    print ("found the data")
                    found = found + 1
                    emailOne = r['email']
                    #matchedNames[r['email']] = r['manager']
                    matchedNames["Email"] = r['email']
                    matchedNames["Manager"] = r['manager']
                    matchedNames_.append(matchedNames)
                    matchedNames = {}
                    count = count + 1
            if (found == 0):
                print("No data present")
                sendNoDataPresent(client_socket, matchedNames_)
            elif (found == 1):
                ret_1 = list()
                ret = {}
                r_ = db.empDB.find({"email" : emailOne})
                for r in r_:
                    ret["Email"] = r['email']
                    ret["Manager"] = r['manager']
                    ret["First Name"] = r['firstName']
                    ret["Last Name"] = r['lastName']
                    ret["Contact Number"] = r['contactNumber']
                    ret["Description"] = r['description']
                    ret["Gender"] = r['gender']
                    ret["Middle Name"] = r['middleName']
                ret_1.append(ret)
                sendEmployeeRecord(client_socket, ret_1)
                #ret = db.empDB.find({"email" : emailOne})
                #print ("found is 1 with emailOne", emailOne)
                #sendEmployeeRecord(client_socket, ret)
            else:
                sendNames(client_socket, matchedNames_)
    elif (strr != ''):
        print("The request is not valid")

