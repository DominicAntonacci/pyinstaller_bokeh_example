"""
This file is the data publisher for the system.

You will need to make sure the connection parameters work
with you.
"""
import multiprocessing
import random
import time

def publishRandomData():
	"""
	Continually puts random (x,y) pairs on the given queue.
	
	:param queue: The Queue to publish to.
	"""
	# A multiprocessing Connection is a good way to pass the data
	# around. I haven't found a good way to pass a Queue into a
	# bokeh server. Doesn't mean there isn't a way though.
	# Note that this is hardcoded. If you change it, you'll need
	# to update it in bokeh_plotter.py as well.
	listener = multiprocessing.connection.Listener(
		('localhost', 9999), authkey=b'supersecure')
		
	# Wait until the connection is open, then dump data on the
	# connection.
	with listener.accept() as conn:
		while True:
			# Control the update rate of the plot.
			time.sleep(0.1)
			conn.send((random.random(), random.random()))
