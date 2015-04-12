# _*_ coding:utf-8 _*_
import time
import subprocess
import shutil
from xml.etree import ElementTree
import paramiko 
import threading

import sys, os, re, optparse, traceback, types, time, getpass
import pexpect, pxssh
import readline, atexit
from integrate import *

from django.template import Template, Context
from django.shortcuts import render_to_response
from srvMonitor.models import *

from django.contrib.auth.decorators import login_required  
from django.contrib import auth

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

import datetime 
from urllib2 import Request

class Game:
    def __init__(self,**dictory):
        '''初始化game对象'''
        self.name=dictory['name']
        self.ip=dictory['ip']
        self.port=dictory['port']
        self.user=dictory['user']
        self.password=dictory['password']
        self.tmp_dir=dictory['tmp_dir']
        self.local_dir=dictory['local_dir']
        self.remote_dir=dictory['remote_dir']
        self.ini_xml=dictory['ini_xml']
        self.xml_dir_name=dictory['xml_dir_name']
        self.remote_swf_dir_name=dictory['remote_swf_dir_name']
        self.local_swf_dir_name=dictory['local_swf_dir_name']
        self.work_dir_head=dictory['work_dir_head']
        self.olmodule_name=dictory['olmodule_name']
        self.stdout_log="stdout_log"
        self.stderr_log="stderr_log"
        self.urlhead=dictory['urlhead']
        self.remote_i18n_dir_name=dictory['remote_i18n_dir_name']
        self.zh_cn_name=dictory['zh_cn_name']
        self.cdn_head=dictory['cdn_head']
        self.encrypt_sh=dictory['encrypt_sh']
        self.remote_bak_dir=dictory['remote_bak_dir']
        return None
    
    def remoteRun(self,cmd):
        '''远程执行脚本'''
        cmd="cd %s ; export LC_CTYPE=en_US.UTF-8; %s" % (self.remote_dir,cmd)
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
            errorlist.append(e)
        return errorlist
    
    def localRun(self,cmd):
        result=os.system(cmd)
        if result==-1:
            return "%s run error!" % cmd
        else:
            return "%s run success!" % cmd
          
    def pullFile(self,remoteFileName,localFileName):
        '使用目录均为绝对路径'
        cmd="scp -P %s %s@%s:%s %s" % (self.port,self.user,self.ip,remoteFileName,localFileName)
#         print cmd
        expect1="password: "
        child = pexpect.spawn(cmd)
        try:
            child.expect(expect1)
            child.sendline(self.password)
        except:
            pass
#             print "++++++++++++"
        child.read()
        return None
    
    def pushFile(self,localFileName,remoteFileName):
        '使用目录均为绝对路径'
        cmd="scp -P %s %s %s@%s:%s" % (self.port,localFileName,self.user,self.ip,remoteFileName)
#         print cmd
        expect1="password: "
        child = pexpect.spawn(cmd)
        try:
            child.expect(expect1)
            child.sendline(self.password)
        except:
            pass
#             print "++++++++++++"
        child.read()
        return None
    
    def appendLog(self,logString):
        '写日志到各项目下'
        logFile=os.path.join(self.local_dir,self.stdout_log)
        writer=open(logFile,'a')
        writer.write("\n%s" % logString)
        writer.close()
    
    def appendErrLog(self,logString):
        '写错误日志到各项目下'
        logFile=os.path.join(self.local_dir,self.stderr_log)
        writer=open(logFile,'a')
        writer.write("\n%s" % logString)
        writer.close()
    
    def urlAddHead(self,urlList):
        '在url前面加一个头，写入pre_publish.txt中'
        publish_dir=os.path.join(self.local_dir,"pre_publish.txt")
        writer=open(publish_dir,"w")
        for url in urlList:
            writer.write("%s \n" % os.path.join(self.urlhead,url))
        writer.close()
        return True    
    
    def encrypt(self):
        '远程执行加密脚本'
        encryptcmd="./%s" % self.encrypt_sh
        self.remoteRun(encryptcmd)
        return True
    
    def bakui(self,filename,newfilename):
        '在远程本地备份xml配置和GameStub.swf'
        errorlist=[]
        bakcmd="cp -rp  %s %s" % (os.path.join(self.remote_dir,filename),os.path.join(self.remote_bak_dir,newfilename))
        print "bakcmd:",bakcmd
        return self.remoteRun(bakcmd)
    
    def getMaxNum(self,head):
        dir=self.local_dir
        filelist=os.listdir(dir)
        restr = "^.*\d+$"
        pattern = re.compile(restr)
        newlist = [i for i in filelist if pattern.match(i)]
        if len(newlist)==0:
            return "当前最新版本号未知"
        else:
            return max(newlist)
    
class Tools():
    ''''''
    def __init__(self,**dictory):
        'olmodule_dir,inixml_dir均为本地临时目录的绝对路径'
        self.olmodule_dir=dictory['olmodule_dir']
        self.inixml_dir=dictory['inixml_dir']
        self.version_num=dictory['version_num']
    
    def modify_olmodule(self,head_dir,local_swf_dir_name,newUiList):    
        #修改olmodule_qh.xml
        xml_tree = ElementTree.parse(self.olmodule_dir,CommentedTreeBuilder())
        root=xml_tree.getroot()
        item_list = root.findall(head_dir)
        version_num_len=len(self.version_num)
        depend_list = root.findall("module/depend")
        for depend in depend_list:
            depend.text = "<![CDATA[%s]]>" % depend.text   
        for item in item_list:
            '''这样计算会有一个问题，新的UI不会自动添加到item_list中'''
            item.text.strip() 
            for newui in newUiList:
                newui="/%s" % newui
                if item.text.find(newui) != -1:
                    i = item.text.find(local_swf_dir_name)
                    item.text=item.text.replace(item.text[(int(i)-int(version_num_len)-1):int(i)-1],self.version_num)
            item.text = "<![CDATA[%s]]>" % item.text
        tree = ElementTreeCDATA(root)
        tree.write(self.olmodule_dir,"UTF-8")
        
    def modify_olmodule_war(self,head_dir,local_swf_dir_name,newUiList):    
        #修改olmodule_qh.xml 处理第十款字典存放olmodule
        xml_tree = ElementTree.parse(self.olmodule_dir,CommentedTreeBuilder())
        root=xml_tree.getroot()
        item_list = root.findall(head_dir)
        version_num_len=len(self.version_num)
        depend_list = root.findall("module/depend")
        for depend in depend_list:
            depend.text = "<![CDATA[%s]]>" % depend.text   
        for item in item_list:
            '''这样计算会有一个问题，新的UI不会自动添加到item_list中'''
            item.text.strip() 
            for newui in newUiList:
                newui="/%s" % newui
                if item.text.find(newui) != -1:
                    d=eval(item.text)
                    d['rpath']='%s/' % self.version_num.encode('raw_unicode_escape')
                    item.text=str(d).replace('\'', "\"")
            item.text = "<![CDATA[%s]]>" % item.text
        tree = ElementTreeCDATA(root)
        tree.write(self.olmodule_dir,"UTF-8")
    
    def __getVerLen(self,dstring,istring):
        index=dstring.find(istring)
#         print "index:%s" % index
        result=1
        for i in range(12,4,-1):
            result=i
            subi=dstring[index-i-1:index-1]
#             print subi
            if re.match(r"\d+$", subi):
                break
        return result   
    
    def modify_ini(self,head_dir,local_swf_dir_name,newUiList):
#         print "modify ini.xml"
        xml_tree=ElementTree.parse(self.inixml_dir, CommentedTreeBuilder())
        root=xml_tree.getroot()
        item_list=root.findall(head_dir)
        version_num_len=len(self.version_num)
        for item in item_list:
            item_tmp=item.attrib["url"]
            item_tmp.strip()
            for newui in newUiList:
                if item_tmp.find(newui) != -1:
                    version_num_len=self.__getVerLen(item_tmp, local_swf_dir_name)
#                     print "version_num_len:%s" % version_num_len
                    i = item_tmp.find(local_swf_dir_name)
#                     print "i:%s" % i
#                     print "index_start: %s " % (int(i)-int(version_num_len)-1)
#                     print "index_end: %s" % (int(i)-1)
#                     print item_tmp
                    item_tmp=item_tmp.replace(item_tmp[(int(i)-int(version_num_len)-1):int(i)-1],self.version_num)
                    item.attrib["url"]=item_tmp
         
        tree=ElementTreeCDATA(root)
        tree.write(self.inixml_dir, "UTF-8")

    def listDir(self,dir,glist):
        '递归搜索出指定目录下的文件，保存在list中'
        if os.path.isfile(dir):
            glist.append(dir)
        else:
            tmplist=os.listdir(dir)
            for tmp in tmplist:
                self.listDir(os.path.join(dir,tmp), glist)
                
    def getAbsDir(self,head ,list):
        '除去文件头，获得相对路径列表'
        for dir in list:
            list[list.index(dir)]=os.path.relpath(dir,head)

if __name__=="__main__":
    sgonline_v10={"name":"战争霸业",
              "ip":"192.168.100.246",
              "user":"root",
              "password":"dawx@99",
              "port":"22",
              "remote_dir":"/data/release/htdocs/sgwar",
              "local_dir":"/data/forilen/Kikyou/verIntegration/sgonline_v10",
              "tmp_dir":"sgonlineTmp",
             "ini_xml":"ini.xml",
              "xml_dir_name":"xml_newnew",
             "remote_swf_dir_name":"swf_new",
             "local_swf_dir_name":"swf_new",
             "work_dir_head":"",
              "olmodule_name":"olmodule_war2.xml",
              "remote_i18n_dir_name":"I18N",
              "zh_cn_name":"zh_cn.xml.new",
              "urlhead":"http://d10.dawx.net/app1101376335",
              "cdn_head":"d10.dawx@61.135.206.20::d10.dawx.net/app1101376335/",
              "encrypt_sh":"war_encrypt.sh",
              "remote_bak_dir":"/data/forilen/disversion/xml_bak"
              }
    gameObj=Game(sgonline_v10)
    olmodule_head="module/item"
    print gameObj.work_dir_head
#     gameObj=Game(sgonline_v5)
#     print gameObj.ip
