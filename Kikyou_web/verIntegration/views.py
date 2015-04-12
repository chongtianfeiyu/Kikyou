# _*_ coding:utf-8 _*_
# Create your views here.

import time
import subprocess
import shutil
from xml.etree import ElementTree
import paramiko 
import threading
import webbrowser

import sys, os, re, optparse, traceback, types, time, getpass,pexpect
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

import tools
from verIntegration.tools import Game, Tools

file_obj=open("/data/release/Kikyou/Kikyou_web/Kikyou.conf")
text=file_obj.read()
CONFIG=eval(text)
# CONFIG={"sgonline_v5":sgonline_v5,"sgonline_v10":sgonline_v10,"sgwar_enus":sgwar_enus,"sgwar_zhtw":sgwar_zhtw}
# svn_admin="forilen"
# svn_admin_password="ting"

def get_someassets():
    #config the remote server ssh connection
    srv_ip=r"192.168.100.254"
    srv_username=r"root"
    srv_password=r"dawx@99"
    srv_port=r"56000"
    log_obj=open("/data/forilen/error.log",'w+')
    
    cmd="ls /data/release/htdocs/sgonline/swf_new/ | grep -v test | grep -v new | grep -v fla"
    try:
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(srv_ip,srv_port,srv_username,srv_password,timeout=5)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        outlist=[]
        for out in stdout:
            outlist.append(out.strip('\n'))
#         print outlist.__len__()
        print outlist
        log_obj.write(out)
    except Exception, e:
        print "Error"
        print e
        
@login_required
def versionStart(request):
    
    if "game" in request.GET:
        game=request.GET.get("game").strip()
        gameName=CONFIG[game]['name'].strip()
    elif "game" in request.COOKIES:
        #当提交参数没有game时，从cookie中读取
        game=request.COOKIES["game"].strip()
        gameName=CONFIG[game]['name'].strip()
    else:
        gameName="未知"
        print "the value of game in cookie has miss,reget the page"
        return render_to_response('verIntegration/uiPrepare.html',{"gameName":gameName})
    
    gameObj=Game(**CONFIG[game])
    current_version=gameObj.getMaxNum("none")

    response=render_to_response('verIntegration/uiPrepare.html',{"current_version":current_version,"gameName":gameName})
    response.set_cookie("game",game,7200)
    return response

@login_required
def uiprepare(request):
    print "++++++++++++++Start ui prepare ++++++++++++++"
    #获取页面跳转传递的参数，如果cookie已经失效，跳转到当前页面，并提示刷新页面
    if "game" in request.COOKIES:
        game=request.COOKIES["game"].strip()
        gameName=CONFIG[game]['name'].strip()
    else:
        gameName="未知"
        return render_to_response('verIntegration/uiPrepare.html',{"gameName":gameName})
    if not "vid" in request.GET:
        return  render_to_response('verIntegration/uiPrepare.html',{"gameName":gameName})
    errorlist=[]
    version_num=request.GET.get("vid").strip()
    ini_url=request.GET.get("iniurl").strip()
    
    #定义版本对象
    gameObj=Game(**CONFIG[game])
    #定义工具类
    tools_dict={}
    tools_dict['olmodule_dir']=os.path.join(gameObj.local_dir,gameObj.tmp_dir,gameObj.olmodule_name)
    tools_dict['inixml_dir']=os.path.join(gameObj.local_dir,gameObj.tmp_dir,gameObj.ini_xml)
    tools_dict['version_num']=version_num
    toolsObj=Tools(**tools_dict)
    
    #写日志
    print "version number:%s" % version_num
    gameObj.appendLog("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    gameObj.appendLog(datetime.datetime.now())
    gameObj.appendLog("version number : %s " % version_num)
    gameObj.appendLog("username : %s" % request.user.username)

    #本次版本目录名
    workDir="%s%s" % (gameObj.work_dir_head,version_num)
    print "workDir:%s" % workDir
    
    #远程olmodule配置的路径
    remote_olmodule_dir=os.path.join(gameObj.remote_dir,gameObj.xml_dir_name,gameObj.olmodule_name)
    print "remote_olmodule_dir:%s" % remote_olmodule_dir
    
    #ini.xml olmodule.xml解析文件头
    inixml_head="resource/material"
    olmodule_head="module/item"
    
    #判断本次版本文件是否存在
    if not os.path.exists(os.path.join(gameObj.local_dir,workDir)):
        print "version directory existed,delete and build new"
        os.mkdir(os.path.join(gameObj.local_dir,workDir))
    else:
        print "build new version directory"
        shutil.rmtree(os.path.join(gameObj.local_dir,workDir))
        gameObj.appendErrLog(toolsObj.version_num)
        gameObj.appendErrLog("This version file had exist! delete it and create a new")
        os.mkdir(os.path.join(gameObj.local_dir,workDir))

    #判断是否从url拉取最新ini.xml，如果拉取保存到临时目录
    if ini_url == "":
        if not os.path.exists(toolsObj.inixml_dir):
            print "error:ini.xml doesn't exist in versiontmp dir"
        gameObj.appendLog("read from the last ini.xml")
        print "read from the last ini.xml from versiontmp"
    else:
        print "get the new ini.xml from %s" % ini_url
        wgetcmd="rm %s ; wget -O %s %s" % (toolsObj.inixml_dir,toolsObj.inixml_dir,ini_url)
        errorlist.append(gameObj.localRun(wgetcmd))
        gameObj.appendLog("read from the new ini.xml: %s" % ini_url)

    #获取ini.xml中需要更新的ui
    newUiList=request.GET.getlist("ui_list")
    #获取olmodule.xml中需要更新的ui
    otherNewUI=request.GET.get("newui").encode('utf8').split("\r\n")
    newUiList=newUiList+otherNewUI
    
    if "" in newUiList:
        newUiList.remove("")
    '删除textarea提交过来的空格'
    print "newUiList:%s" % newUiList
    
    svnupcmd="svn cleanup ; svn up --username %s --password %s ." % (CONFIG["svn_admin"],CONFIG['svn_admin_password'])
    errorlist.extend(gameObj.remoteRun(svnupcmd))
    print "remote run svn up "
    
    if len(newUiList)!=0:
        '有新提交的UI'
        gameObj.encrypt()
        print "remote run encrypt scripts"
        
        #从远程获取最新的olmodule.xml
        gameObj.pullFile(remote_olmodule_dir, toolsObj.olmodule_dir)
        print "pull ui file from remote host:%s" % newUiList
        
        #修改ini.xml及olmodule.xml
        toolsObj.modify_ini(inixml_head,gameObj.local_swf_dir_name,newUiList)
        if game=="sgonline_v10":
            toolsObj.modify_olmodule_war(olmodule_head,gameObj.local_swf_dir_name,newUiList)
        else:
            toolsObj.modify_olmodule(olmodule_head,gameObj.local_swf_dir_name,newUiList)
        #将新ui拉取到本次版本目录
        for newui in newUiList:
            newUIdir=os.path.join(workDir,gameObj.local_swf_dir_name)
            gameObj.appendLog(newui)
            if not os.path.exists(os.path.join(gameObj.local_dir,newUIdir)):
                os.mkdir(os.path.join(gameObj.local_dir,newUIdir))
            gameObj.pullFile(os.path.join(gameObj.remote_dir,gameObj.remote_swf_dir_name,newui), os.path.join(gameObj.local_dir,newUIdir,newui))
        #第十款英文版的GameStub.swf放在繁体版下面
        if "GameStub.swf.new" in newUiList:
            errorlist.append(gameObj.bakui(gameObj.xml_dir_name, "xml_%s" % version_num))
            if game == "sgwar_enus":
                newUIdir=os.path.join(workDir,gameObj.local_swf_dir_name)
                gameObj.pullFile(os.path.join(gameObj.remote_dir,"swf_fb/fanti/GameStub.swf.new"),os.path.join(gameObj.local_dir,newUIdir,"GameStub.swf.new"))
        
        #将修改完毕的ini.xml保存一份到本次版本目录目录   
        cmd="cp -rp %s %s" % (os.path.join(gameObj.local_dir,gameObj.tmp_dir,gameObj.ini_xml),os.path.join(gameObj.local_dir,workDir,"ini.xml"))
        errorlist.append(gameObj.localRun(cmd))  
#         将修改过的olmodule.xml推送到远端，同时执行svn commit
        print "push the %s from local to remote" % gameObj.olmodule_name
        gameObj.pushFile(toolsObj.olmodule_dir, remote_olmodule_dir)
        svn_ci_cmd="svn ci --username %s --password %s %s/%s -m \"change ui in 252-Kikyou\" " % (CONFIG['svn_admin'],CONFIG['svn_admin_password'],gameObj.xml_dir_name,gameObj.olmodule_name)
        print "remote commit the new %s" % gameObj.olmodule_name
        errorlist.extend(gameObj.remoteRun(svn_ci_cmd))
     
    print "++++++++++++++ End ui prepare ++++++++++++++"    
    response=render_to_response('verIntegration/binPrepare.html',{"gameName":gameName,"errorlist":errorlist})
    response.set_cookie("versionNum",version_num,7200)
#     gameweb=webbrowser.open_new_tab("http://192.168.100.254:8061/index_new.php?openid=forilen")
    return response

@login_required
def binprepare(request):
    print "++++++++++++++Start bin prepare ++++++++++++++"
    #这里不对cookie检查了，设置cookie过期世间安是60分钟
    if "game" in request.COOKIES:
        game=request.COOKIES["game"].strip()
        gameName=CONFIG[game]['name'].strip()
    else:
        gameName="未知"
        print "cookie has gone"
        return render_to_response('verIntegration/uiPrepare.html',{"gameName":gameName})
    errorlist=[]
    version_num=request.COOKIES["versionNum"]
    
    #定义版本对象
    gameObj=Game(**CONFIG[game])
    #本次版本目录名
    workDir="%s%s" % (gameObj.work_dir_head,version_num)
    #定义工具类
    tools_dict={}
    tools_dict['olmodule_dir']=os.path.join(gameObj.local_dir,gameObj.tmp_dir,gameObj.olmodule_name)
    tools_dict['inixml_dir']=os.path.join(gameObj.local_dir,gameObj.tmp_dir,gameObj.ini_xml)
    tools_dict['version_num']=version_num
    toolsObj=Tools(**tools_dict)
    
    #判断本次版本文件是否存在
    if not os.path.exists(os.path.join(gameObj.local_dir,workDir)):
        os.mkdir(os.path.join(gameObj.local_dir,workDir))    
    inixml_head="resource/material"
    
    #获取需要修改的bin.new，修改ini.xml
    binlist=request.GET.getlist("bin_list")
    print "bin list:%s" % binlist
    
    svn_up_cmd="svn cleanup ; svn up --username %s --password %s %s" % (CONFIG['svn_admin'],CONFIG['svn_admin_password'],os.path.join(gameObj.remote_dir,gameObj.xml_dir_name))
    print "remote run svn up "
    gameObj.remoteRun(svn_up_cmd)
    
    if len(binlist)!=0:
        #运行加密脚本，执行文件加密
        print "remote run encrypt scripts"
        gameObj.encrypt()
        print "backup the GameStub.swf.new and xml_newnew"
        errorlist.append(gameObj.bakui(gameObj.xml_dir_name, "xml_%s" % version_num))
        errorlist.append(gameObj.bakui("%s/GameStub.swf" % gameObj.remote_swf_dir_name,"GameStub.swf.%s" % version_num))
        
        print "modify the ini.xml"
        toolsObj.modify_ini(inixml_head,"xml",binlist)        
        #将bin.new文件复制到本地
        for bin in binlist:
            gameObj.appendLog(bin)
            bin_dir=os.path.join(gameObj.local_dir,workDir,"xml")
            #本地版本bin.new文件存放路径
            if not os.path.exists(bin_dir):
                os.mkdir(bin_dir)
            if game=="sgonline_v10":
                #第十款test.bin.new文件放在外面，特殊处理
                gameObj.pullFile(os.path.join(gameObj.remote_dir,gameObj.xml_dir_name,bin), os.path.join(bin_dir,bin))
            else:
                gameObj.pullFile(os.path.join(gameObj.remote_dir,gameObj.xml_dir_name,"Precompiled",bin), os.path.join(bin_dir,bin))
        
        #将修改完毕的ini.xml保存一份到本次版本目录目录   
        cmd="cp -rp %s %s" % (os.path.join(gameObj.local_dir,gameObj.tmp_dir,gameObj.ini_xml),os.path.join(gameObj.local_dir,workDir,"ini.xml"))
        errorlist.append(gameObj.localRun(cmd))
        
    #将zh_cn复制到本地
    zh_cn_list=request.GET.getlist("zh_cn_list")
    if len(zh_cn_list)!=0:
        gameObj.appendLog(gameObj.zh_cn_name)
        gameObj.encrypt()
        gameObj.pullFile(os.path.join(gameObj.remote_dir,gameObj.remote_i18n_dir_name,gameObj.zh_cn_name), os.path.join(gameObj.local_dir,workDir,gameObj.zh_cn_name))
    
    #列出本次版本的所有文件
    filelist=[]
    filepath=os.path.join(gameObj.local_dir,workDir)
    toolsObj.listDir(filepath,filelist)
    toolsObj.getAbsDir(gameObj.local_dir,filelist)
    gameObj.urlAddHead(filelist)
    gameObj.appendLog("ui config done")
    print "++++++++++++++End bin prepare ++++++++++++++"
    return render_to_response('verIntegration/uploadcdn.html',{"filelist":filelist,"gameName":gameName,"errorlist":errorlist})

@login_required
def uploadcdn(request):
    if not ( "game" in request.COOKIES and "versionNum" in request.COOKIES ):
        return render_to_response('verIntegration/done.html',{"message":"项目名未知或版本号未知"}) 
    
    game=request.COOKIES["game"].strip()
    version_num=request.COOKIES["versionNum"].strip()
    gameObj=Game(**CONFIG[game])
    errorlist=[]
    
    chinaCacheList=["sgonline_v5"]
    awsList=["sgwar_zhtw","sgwar_enus"]
    chinaNetCenter=['sgonline_v10']
    
    workDir="%s%s" % (gameObj.work_dir_head,version_num)
    uploadcmd="cd %s ; rm -rf rsync/* ; cp -rp %s rsync/" % (gameObj.local_dir,workDir)  
    
    pre_publish_file_obj=open(os.path.join(gameObj.local_dir,"pre_publish.txt"))  
    message_list=["已经发布以下资源："]
    for line in pre_publish_file_obj:
        message_list.append(line)
        
    if game in chinaCacheList:
        errorlist.append(gameObj.localRun(uploadcmd))
        uploadcmd="/usr/bin/rsync -azv --password-file=/etc/qh_pwd.txt %s %s" % (os.path.join(gameObj.local_dir,"rsync/"),gameObj.cdn_head)
        print "uploadcmd : %s" % uploadcmd
        errorlist.append(gameObj.localRun(uploadcmd))
        gameObj.appendLog("upload into cdn sucess")
        
        uploadcmd="cd %s ; /usr/local/php/bin/php api.php" % gameObj.local_dir
        errorlist.append(gameObj.localRun(uploadcmd))
        gameObj.appendLog("distribute success")
    if game in awsList:
        uploadcmd="cd %s ;rm -rf rsync/* ;cp -rp %s rsync/; /usr/local/bin/aws s3 sync rsync/ s3://sgwar/2015/" % (gameObj.local_dir,workDir)
        print uploadcmd
#         errorlist.append(gameObj.localRun(uploadcmd))
        print "upload into aws cdn"
        
    if game in chinaNetCenter:
        uploadcmd="cd %s ; ./autoUpLoadZsbyPre.sh %s%s " % (gameObj.local_dir,gameObj.work_dir_head,version_num)
        print "upload to ChinaNetCenter:%s" % uploadcmd
        gameObj.localRun(uploadcmd)
    
    return render_to_response('verIntegration/done.html',{"message":message_list,"gameName":gameObj.name,"errorlist":errorlist})

@login_required
def uploadpng(request):
    game=request.COOKIES["game"].strip()
    gameObj=Game(**CONFIG[game])
    gameName=gameObj.name
    errorlist=[]
    if not "days" in request.GET:
        errorlist.append("请填写天数")
        return render_to_response('verIntegration/uploadpng.html',{"errorlist":errorlist,"gameName":gameName})
    days=request.GET.get("days").strip()
    gameObj.appendLog("upload png %s days ago" % days)
    uploadpngcmd="./upload_png.sh %s" % days
    errorlist.extend(gameObj.remoteRun(uploadpngcmd) )
    return render_to_response('verIntegration/uploadpng.html',{"errorlist":errorlist,"gameName":gameName})
