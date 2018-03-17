"""
This script receives data from a Queue and plots it.

This is one of the examples in
https://bokeh.pydata.org/en/latest/docs/user_guide/server.html
slightly modified to fit this example.
"""
from functools import partial
from random import random
from threading import Thread
import multiprocessing
import time

from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure

from tornado import gen

# this must only be modified from a Bokeh session callback
source = ColumnDataSource(data=dict(x=[0], y=[0]))

# This is important! Save curdoc() to make sure all threads
# see the same document.
doc = curdoc()

@gen.coroutine
def update(x, y):
    source.stream(dict(x=[x], y=[y]))
	


def blocking_task():
	# Open the connection from data_publisher.py. If you change
	# the connection settings here, you need to keep them up
	# to date there.
	with multiprocessing.connection.Client(('localhost', 9999), authkey=b'supersecure') as conn:
		
		while True:
			# Read the data off the connection, and send it to be plotted.
			data = conn.recv()
			doc.add_next_tick_callback(partial(update, x=data[0], y=data[1]))
    # while True:
        # # do some blocking computation
        # time.sleep(0.1)
        # x, y = random(), random()

        # # but update the document from callback
        # doc.add_next_tick_callback(partial(update, x=x, y=y))

p = figure(x_range=[0, 1], y_range=[0,1])
l = p.circle(x='x', y='y', source=source)

doc.add_root(p)

thread = Thread(target=blocking_task)
thread.start()