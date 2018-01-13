#!/usr/bin/python
#coding:utf-8

import sys,os,signal,commands
class Daemon(object):
    def __init__(self,target=None,args=(),pidname=sys.argv[0]):
        self.__target=target
        self.__args=args
	self.__pid=pidname

    def _Create_Daemon(self):
        try:
	    pid=os.fork()
	    if pid > 0:
		sys.exit(0)
        except Exception,e:
            return e
	    sys.exit(1)
	
	os.chdir('/')
	os.umask(0)
	os.setsid()

	try:
            pid=os.fork()
            if pid > 0:
                sys.exit(0)
        except Exception,e:
            return e
            sys.exit(1)

	Daemon._pid(self)
	Daemon.run(self)

    def _pid(self):
        pid=str(os.getpid())
        with open('/var/run/%s' % self.__pid,'w') as wf:
            wf.write('%s\n' % pid)
            wf.close()

    def run(self):
        if self.__target:
            self.__target(*self.__args)

    def start(self):
	try:
	    Daemon.stop(self)
	    Daemon._Create_Daemon(self)
	except Exception,e:
	    return e

    def stop(self):
	try:
	    with open('/var/run/%s' % self.__pid,'r') as rf:
		pid=rf.readline()
		repid=int(pid.rstrip('\n'))
		rf.close()
	    os.kill(repid,signal.SIGTERM)
	    os.remove('/var/run/%s' % self.__pid)
	except Exception,e:
	    return e

    def status(self):
	try:
	    with open('/var/run/%s' % self.__pid,'r') as rf:
                pid=rf.readline()
                repid=pid.rstrip('\n')
                rf.close()
	except Exception,e:
	    return e

	pidout=list(commands.getstatusoutput('ps aux|grep -v grep|grep %s' % repid))[1][10:15]

        if pidout != ' ':
	    print "%s (pid is %s) is already started..." % (self.__pid,repid)
        else:
	    print "%s: unrecognized service" % self.__pid
