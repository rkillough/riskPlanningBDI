#!/usr/bin/env python

from bottle import *
import subprocess

def getip():
     ipString = subprocess.check_output(["ifconfig eth0| grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"], shell=True);
     return ipString
     
@get('/<plugNo>/<state>')
def forward(plugNo, state):
    print "Turning plug "+str(plugNo)+" "+str(state) 
    
ip = getip()
run(host=ip, port=8079)   
print "Server running on "+ip+"8079"
