import socket

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
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024)
    strr = request.decode()
    print (repr(strr))
    indexFound = strr.find("firstName=")
    print (strr[indexFound:])

    http_response = """\
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *

""" + "hey! I am back with response"

    client_socket.sendall(http_response.encode())
    client_socket.close()

