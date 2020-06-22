# USAGE
# python client.py --server-ip SERVER_IP

# import the necessary packages
from imutils.video import VideoStream
from datetime import datetime
import imagezmq
import argparse
import socket
import time
import polly

responses = {}
threshold = 3

def last_seen(name):
	with open(name + "_last_seen.txt", "w") as file1: 
		# Writing data to a file 
		file1.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")) 

def update_last_seen(name):
	with open(name + "_last_seen.txt", "w") as file1: 
    	# Writing data to a file 
    	file1.write("Hello \n") 
    	file1.writelines(L)

def check_noise(name):
	global responses
	if name in responses.keys():
		responses[name] = responses[name] + 1
	else:
		responses[name] = 1	

	if responses[name] > threshold:
		responses = {}
		return True
	return False	

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
	help="ip address of the server to which the client will connect")
args = vars(ap.parse_args())

# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(
	args["server_ip"]))

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
hostname = socket.gethostname()
#vs = VideoStream(usePiCamera=False).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)




while True:
	# read the frame from the camera and send it to the server
	frame = vs.read()
	reply = sender.send_image(hostname, frame).decode("utf-8") 
	if reply == "":
		print("No faces detected")
		#clear out responses
		responses = {}
	elif check_noise(reply):
		if reply == "Unknown":
			polly.play_intruder()
		else:
			polly.play_greeting(reply)
		responses = {}