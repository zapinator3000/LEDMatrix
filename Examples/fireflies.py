import matrix, random
matrix.frame_speed(50)
while True:
	for x in range(1,6):
		x=random.randint(1,16)
		if x<10:
			x="0"+str(x)
		matrix.add_to_queue(str(x))
	matrix.add_frame_end()
	matrix.run()
