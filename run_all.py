"""
The Python script that starts all the processes.

This starts a data publishing function defined in data_publisher.py and 
a bokehplotting function in bokeh_plotter.py. The two processes communicate
using a multiprocessing Connection object. This avoids the hassle of
trying to pass a Queue into the code that kicks off the bokeh server.

You will likely see a bunch of callback errors. These are a known bokeh 
bug, but do not impact the demo.
"""

import argparse
import multiprocessing
from functools import partial

import data_publisher

from bokeh.command.subcommands.serve import Serve

def startBokehServer(file_name, show=True):
	"""
	Starts the bokeh server using the given file.
	
	This is equivalent to running
	bokeh serve --show file_name
	
	:param file_name: The name of the file to run.
	:param show: If True, a webpage will be opened running the bokeh server.
	
	:warning: This must be a picklable function to get it to work with the
	    multiprocessing module. This means it must be a top-level module 
	    definition, like it is here.
	"""

	# bokeh.command.subcommands.serve is the code that is run when 
	# `bokeh serve` is called, but it must be given arguments from an 
	# ArgumentParser
	p = argparse.ArgumentParser()
	
	# Creating a new Serve object automatically adds the correct 
	# arguments to the ArgumentParser.
	s = Serve(p)
	
	# Create an argument list with the defaults, then change as I want.
	args = p.parse_args(args='')
	args.show = show
	args.files.append(file_name)
	
	# Start the server
	s.invoke(args)
	
if __name__ == '__main__':
	# Enable multiprocessing when running from the exe.
	# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.freeze_support
	multiprocessing.freeze_support()
	
	# Start the data publisher first. This way, the multiprocessing 
	# Connection is created properly. The daemon flag just helps ensure
	# the processes end when this function ends.
	publish_process = multiprocessing.Process(
		target=data_publisher.publishRandomData, daemon=True)
	publish_process.start()

	# Create and start the bokeh server
	bokeh_process = multiprocessing.Process(
		target=partial(startBokehServer, 'bokeh_plotter.py'), daemon=True)
	bokeh_process.start()
	
	# Cheap way to allow the user to end when they want.
	input('Press enter to stop...')
	
	# Close and terminate processes.
	publish_process.terminate()
	bokeh_process.terminate()
