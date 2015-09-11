'''
This class combined the server and daemon and implements a shared data queue between them
Generally, command received from the server are passed to the daemon which controls the hardware and maintains the state
Data is also requested by the server from the daemon for display
'''

from multiprocessing import Process, Queue
import scenarioTester
import time
import os

def runAgent(name,inq, outq, wait):
	scenarioTester.runAgent(name, inq, outq, wait)

class AgentQ():
	def __init__(self,name):
		self.name = name
		self.q = Queue()

iters = 100
successCount = 0.0
successReward = 0.0

#main
def run3robot():
	global successCount
	global successReward

	print "Starting required processes"

	inq = Queue()	#where the threads post if theyve been successful or not

	one = AgentQ("one")
	two = AgentQ("two")
	three = AgentQ("three")
	#one queue per thread to feed them info

	agent1 = Process(target=runAgent, args=("one",inq,one.q,0,))
	agent2 = Process(target=runAgent, args=("two",inq,two.q,1,))
	agent3 = Process(target=runAgent, args=("three",inq,three.q,2))


	print "Starting agent1"
	agent1.start()

	print "Starting agent2"
	agent2.start()
	
	print "Starting agent3"
	agent3.start()

	agentsLeft = 3

	#read inq and inform other threads about whats happened
	success = False
	while success == False and agentsLeft != 0:
		try:
			#print "Main thread waiting on queue"
			message = inq.get_nowait()
			sp = message.split(':')
			message = sp[0]
			tReward = float(sp[1])
			event = message[0]
			agent = message[1:]

		

			print "M: "+message
			
			if agent == "one":
				two.q.put(event)
				three.q.put(event)
			if agent == "two":
				one.q.put(event)
				three.q.put(event)
			if agent == "three":		
				one.q.put(event)
				two.q.put(event)
		
		
			if event == 's':
				success = True
				successReward += tReward
				print "Agent "+agent+" succeeded"
				print "--------------------------------------------"+str(successReward)		
				successCount += 1
						
			elif event == 'f':
	
				agentsLeft -= 1
				if agentsLeft == 0:
					print "All agents failed"
				print agentsLeft
	        except:
			pass	

		#time.sleep(0.5)

	#print "From queue: "+q.get()

	#serverThread.join()


	#daemonThread.join()

def iterate():
	for i in range(iters):
		run3robot()

	print successReward
	success = successCount
	avgreward = successReward / successCount

	print "\n\nSuccess = "+str(success)+"%\tAvg reward = "+str(avgreward)

iterate()


os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 1, 1000))
