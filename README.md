Introduction
============
This is a minimal example to show how to run a bokeh server
in a multiprocessing thread and get it all to run using a
PyInstaller exe. This process does not support the one-file option
for PyInstaller because you must manually copy files later on.

This has only been tested on Windows 10 using Anaconda Python 3.6 
using bokeh 0.12.14 and PyInstaller 3.3.1.

Setting Up Your Environment
===========================
Create a new conda environment to build the exe in. This build process
is a bit fragile and I've run into many errors when it's not a new
environment.
```
conda create --new bokeh_server_example python bokeh
conda activate bokeh_server_example
conda install -c conda-forge pyinstaller
```

Running the Demo In Python
==========================
Start it with
```
python run_all.py
```
You can end it by pressing Enter at any time.
You will likely see a lot of errors about removing callbacks. This is a 
known bokeh bug in Windows (https://github.com/bokeh/bokeh/issues/7219). 
Plotting is unaffected.

Building the Exe
================
Modifying Bokeh Files
---------------------
First, you need to modify a bokeh file. Hopefully this step will be patched in bokeh soon.
Find where your conda environment stores the bokeh files. For me, it is at 
C:\Anaconda3\envs\bokeh_server_example\Lib\site-packages\bokeh\.
Now, navigate to bokeh\core\templates.py and replace it with the templates_new.py file
included in the repo. Be sure to change the name back to templates.py This is based on 
https://stackoverflow.com/questions/31259673/unable-to-include-jinja2-template-to-pyinstaller-distribution/46628650#46628650.
Alternatively, you can apply the patch file also included.

Creating the Exe
----------------
Next, create the exe. *THIS IS NOT THE LAST STEP. YOU HAVE TO DO THE NEXT ONE EVERY TIME.*
```
pyinstaller run_all.py --hidden-import bokeh_plotter.py;. --add-data bokeh_plotter.py ;.
```
If you get a recursion error after this step, PyInstaller had trouble handling your imports. 
I've found it's usually fixed by creating a new conda environment (see top of file).

Adding Bokeh Files
------------------
Bokeh will still be missing a bunch of files it needs to work. It's 
easiest to locate where the Bokeh files are stored, and copy the whole 
directory over. For me, the files are at 
C:\Anaconda3\envs\bokeh_server_example\Lib\site-packages\bokeh.
You should locate where Anaconda is installed and replace that path with yours.
```
robocopy C:\Anaconda3\envs\bokeh_server_example\Lib\site-packages\bokeh .\dist\run_all\bokeh /E
```

Now, the exe should work fine!
