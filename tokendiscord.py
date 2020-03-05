import json
import os  

class Tokendiscord:     
    def __init__(self): 
        os.chdir(r'D:\coding\Klaybot')        
        with open ("token.ini","r") as f:             
            lines = f.readlines()             
            self.token = lines[0].strip()     
        
    def getToken(self):         
                return self.token