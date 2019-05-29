#!/usr/bin/python
# This is the library for running the second version of the LED matrix
import time
import os
import RPi.GPIO as gpio
#Initialize pins for display
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(29,gpio.OUT)
gpio.setup(31,gpio.OUT)
gpio.setup(32,gpio.OUT)
gpio.setup(33,gpio.OUT)
gpio.setup(36,gpio.OUT)
gpio.setup(37,gpio.OUT)
gpio.setup(38,gpio.OUT)
gpio.setup(40,gpio.OUT)
#Create lists for cleanup
offlist=[29,31,32,33] #X pins
onlist=[40,38,37,36] # Y pins
# Give the Library based on left to right up and down and give real pin numbers

# Below is the Layout

""" 01 02 03 04
    05 06 07 08
    09 10 11 12
    13 14 15 16 """

##

pins={"01":"33,40","02":"33,38","03":"33,37","04":"33,36","05":"32,40","06":"32,38","07":"32,37","08":"32,36","09":"31,40","10":"31,38","11":"31,37","12":"31,36","13":"29,40","14":"29,38","15":"29,37","16":"29,36"}
#Initialize the queue for creating the presentation
queue=[]
mplxspeed=0.0001 # Default multiplexing delay
framespeed=100 # Default Frame Speed
frame_cache=[] # Frame Cache for loading each frame to display one frame at a time

#Turn off all LEDs
def close_all():
	for thing in onlist: # Turn all in y axis on
		gpio.output(thing,1)
	for thing in offlist: # Turn all in x axis off
		gpio.output(thing,0)
# Convert a numerical value to the real pin list
def conv_to_pins(entry): 
	global pins
	return pins[str(entry)] # Return the real-valued pin numbers from the library
# Add an entire frame to the queue
def add_by_frame(entry):
	things=entry.split(":") # Split the input by a :
	for item in things: # Append each item to the queue that is in the entry
		queue.append(conv_to_pins(item))
	queue.append("00,00") # Append a close-frame to the queue
# Add a signle entry to the queue
def add_to_queue(entry):
	global queue
	queue.append(conv_to_pins(entry)) # Add a single entry to the queue
#Add a frame end
def add_frame_end():
	global queue
	queue.append("00,00") #Append a blank entry to end the frame
# Change the multiplex speed
def set_multiplex_speed(speed):
	global mplxspeed
	mplxspeed=speed
# Change the frame speed
def frame_speed(speed):
	global framespeed
	framespeed=speed
# Add an empty frame to the queue
def add_end_frame():
	global queue
	queue.append("00,00")
# Run the multiplex presentation
def run():
	close_all() # Clear teh display
	#print("RUNNING MATRIX PRESENTATION")
	len_of_queue=len(queue) # Get the queue length
	pointer=0 # Set the pointer to 0
	frame_num=1 # Set the frame pointer to 0
	while True:
		frame_cache=[] # Clear the Frame cache
		pincount=0 # Set the pin counter to 0
#		print("LOAD FRAME") # Debugging crap


		while queue[pointer] != "00,00": # While the pointer in the queue is not equal to the end frame, read the data into the frame cache
			frame_cache.append(queue[pointer])


#			print(queue[pointer]) # More debugging crap
			pointer=pointer+1 # Increase the pointer to read the data (This will not reset each frame)
			pincount=pincount+1 # Increase the pin count (This will reset each frame)


#		print("EXIT CODE") # Debugging crap


		pointer=pointer+1 # Increase the pointer by 1 to move out of the end frame

		if pointer >= len_of_queue: # If the pointer is greater or equal to the length of the queue, exit the presentation and reset the pointer
			pointer=0
#			print("RESET") # Debugging crap
			break;
		counter=0 # Reset the counter for the frame 
		print("MULTIPLEXING FRAME("+str(frame_num)+") WITH : "+str(pincount)+" PINS")
#		print(frame_cache) # Debugging crap


		while counter<framespeed: # While the counter is less than the frame speed, multiplex the output

			for item in frame_cache: # Multiplex the output by loading each item in the frame cache individually 

				# Split the x and y positions from each item
				xpos=item.split(",")[0]
				ypos=item.split(",")[1]
				# Turn the corresponding LED on by turning the X pin on and Y pin off
				gpio.output(int(xpos),1)
				gpio.output(int(ypos),0)
				time.sleep(mplxspeed) # Wait the multiplex speed
				# Turn the corresponding LED off by reversing the polarity
				gpio.output(int(xpos),0)
				gpio.output(int(ypos),1)
				time.sleep(mplxspeed) # Wait the multiplex speed

			counter=counter+1 # Increase the frame counter by 1

		frame_num=frame_num+1 # Increase the frame number by 1
# Clean up the pins
def cleanup():
	gpio.cleanup()
