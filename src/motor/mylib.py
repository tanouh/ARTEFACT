from multiprocessing import Process
from flask import request

def send_request(nature, i):
    server = "137.194.173." + str(i) + ":8000"
    try: request.post("http://"+server+"/com?nature="+nature+"&id=b",data={})
    except:
        return(False)
    return(True)

def communicate (nature):
    global processes
    for i in range(36,41):
        p = Process(target=send_request, args=(nature, i))
        processes.append(p)
        p.start()

def pinging (ping_flag):
    while ping_flag : 
        communicate("ping")