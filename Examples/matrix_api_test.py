import matrix
matrix.set_multiplex_speed(0.0001)
matrix.frame_speed(50)
matrix.add_by_frame("01:03:05:13:15:08")
matrix.add_by_frame("02:04:09:14:16:12")
matrix.add_by_frame("04:14:12")
matrix.add_by_frame("01:05:15")
matrix.add_by_frame("03:13:08")
matrix.add_by_frame("02:09:16")
matrix.add_end_frame()
try:
	while True:
		matrix.run()
finally:
	matrix.cleanup()
