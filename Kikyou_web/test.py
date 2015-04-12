# _*_ coding:utf-8 _*_
import sys, os, re, optparse, traceback, types, time, getpass
import pexpect, pxssh, paramiko 

class test():
    def __init__(self,**dictory):
        self.remote_dir=dictory["remote_dir"]
        self.ip=dictory["ip"]
        self.port=dictory["port"]
        self.user=dictory["user"]
        self.password=dictory["password"]
    
    def remoteRun(self,cmd):
        cmd="cd %s ; %s" % (self.remote_dir,cmd)
        print "remote run cmd: %s" % cmd
        
        errorlist=[]
        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip,self.port,self.user,self.password,timeout=5)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            
            for out in stdout:
                errorlist.append(out.strip('\n'))
            for error in stderr:
                errorlist.append(error.strip('\n'))
        except Exception,e:
            print "Error"
            print e
        return errorlist

if __name__=="__main__":
    game={"remote_dir":"/data/darren/sgwar",
              "ip":"192.168.100.246",
              "user":"root",
              "password":"dawx@99",
              "port":"22",
          }
    cmd=u"export LC_CTYPE=en_US.UTF-8;svn up --username forilen --password ting xml"
    t=test(**game)
    restr = "^.*\d+$"
    pattern = re.compile(restr)


    errorlist=t.remoteRun(cmd)
    print errorlist
#     errorlist=os.system("ls /data/forilen")
#     print errorlist