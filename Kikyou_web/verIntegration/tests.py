"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import os
import re

def listFile(dir,list):
    if not os.path.isdir(dir):
#         print "%s is a not dir" % dir
        list.append(dir)
    else:
        tmplist=os.listdir(dir)
        for tmp in tmplist:
            listFile(os.path.join(dir,tmp), list)
        
def getAbsDir(head ,list):
    for dir in list:
        print os.path.relpath(dir, head)

def calVerLen(s):
    print s

class Tools:
    def __init__(self,**dictory):
        self.name=dictory['name']
        self.age=dictory['age']
    
    def modifydic(self):
        self.name="forilen"
        
    def printdic(self):
        print "name:",self.name
        print "age:" , self.age
    
if __name__ == "__main__":
#     dir="/data/forilen/Kikyou/verIntegration"
#     list=[]
#     listFile(dir, list)
#     print list
#     
#     head="/data/forilen/Kikyou/verIntegration"
#     getAbsDir(head, list)
#     names={"name":"cheeron","age":23}
#     student=Tools(**names)
#     student.printdic()
#     student.modifydic()
#     student.printdic()

    s={"url":"14072401/swf_new/zhenfaui.swf", "type":"swf"}
    s2={"url":"14072401/swf_new/azhenfaui.swf", "type":"swf"}
    a="zhenfaui.swf"
    
    restr = "/%s" % a
    print restr
    pattern = re.compile(restr)
    
    if pattern.match( s['url']):
        print "ok"
    else:
        print "no"
    
    