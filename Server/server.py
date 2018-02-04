import socket
import re
import pymongo
from pymongo import MongoClient

HOST, PORT = '', 52557
#payLoadData = '{"items": [{"id": "Open", "label":"Open"},{"id": "OpenNew", "label": "Open New"},\
#               {"id": "ZoomIn", "label": "Zoom In"},{"id":"ZoomOut", "label": "Zoom Out"},\
#               {"id":"OriginalView","label": "Original View"},{"id":"Find", "label": "Find..."},\
#               {"id": "FindAgain","label": "Find Again"},{"id": "CopyAgain","label": "Copy Again"},\
#               {"id": "CopySVG","label": "Copy SVG"},{"id": "ViewSVG", "label":"View SVG"},\
#               {"id": "ViewSource", "label": "ViewSource"},{"id": "SaveAs", "label": "Save As"},\
#               {"id": "About", "label": "About Adobe CVGViewer..."}]}'
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print ('Starting web-server on port ' + str(PORT))
while True:
    #Connecting to mongodb
    client = MongoClient()
    #Opening database
    db = client.EmployeeDatabase
    
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024)
    strr = request.decode()
    #print (repr(strr))
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
        matchedData = re.search("email=(\w+)", fetchData)
        email = matchedData.group(1)
        matchedData = re.search("contactNumber=(\w+)", fetchData)
        contactNumber = matchedData.group(1)
        matchedData = re.search("manager=(\w+)", fetchData)
        manager = matchedData.group(1)
        matchedData = re.search("description=(\w+)", fetchData)
        description = matchedData.group(1)

        #Create a dictionary
        empData={}
        empData['firstName'] = firstName
        empData['lastName'] = lastName
        empData['middleName'] = middleName
        empData['email'] = email
        empData['contactNumber'] = contactNumber
        empData['manager'] = manager
        empData['description'] = description
        #search for the data if exists in mongodb
        if (db.empDB.find({"email" : email}).count() > 0):
            print ("Found an element already. Not inserting")
        else:
            #insert into mongodb
            db.empDB.insert_one(empData)
    elif (strr.find("Employee") != -1):
        print("Got request to search an employee detail")
        indexOPSearch = strr.find("email")
        indexHTTP = strr.find(" HTTP")
        searchData = strr[indexOPSearch:indexHTTP]
        matchedData = re.search("email=(\w+)", searchData)
        email = matchedData.group(1)
        if (db.empDB.find({"email" : email}).count() > 0):
            print ("Data found. Returning to client")
            ret = db.empDB.find({"email" : email})
    elif (strr != ''):
        print("The request is not valid")
    
    http_response = """\
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *

""" + str(empData)

    client_socket.sendall(http_response.encode())
    client_socket.close()

