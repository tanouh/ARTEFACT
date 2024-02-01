from multiprocessing import Process
from flask import request
import requests
from time import *

def send_request(nature, i):
    server = "137.194.173." + str(i) + ":8000"
    try: requests.post("http://"+server+"/com?nature="+nature+"&id=b",data={})
    except:
        return(False)
    return(True)

def communicate (nature):
    global processes
    for i in range(36,41):
        p = Process(target=send_request, args=(nature, i))
        processes.append(p)
        p.start()

def pinging():
    while True : 
        pg()
        time.sleep(5)

def dep():
    def pingplease(ip):
        try: requests.post("http://"+ip+"/com?nature=depart&id=b",data={})
        except:
            return(False)
        return(True)

    L=["137.194.173.38:8000","137.194.173.40:8000","137.194.173.37:8000","137.194.173.36:8000","137.194.173.39:8000"]
    for i in L:
        p = Process(target=pingplease, args=(i,))
        p.start()


        
def pg():
    def pingplease(ip):
        try: requests.post("http://"+ip+"/com?nature=ping&id=b",data={})
        except:
            return(False)
        return(True)

    L=["137.194.173.38:8000","137.194.173.40:8000","137.194.173.37:8000","137.194.173.36:8000","137.194.173.39:8000"]
    for i in L:
        p = Process(target=pingplease, args=(i,))
        p.start()

        
def arr():
    def pingplease(ip):
        try: requests.post("http://"+ip+"/com?nature=arrive&id=b",data={})
        except:
            return(False)
        return(True)

    L=["137.194.173.38:8000","137.194.173.40:8000","137.194.173.37:8000","137.194.173.36:8000","137.194.173.39:8000"]
    for i in L:
        p = Process(target=pingplease, args=(i,))
        p.start()
