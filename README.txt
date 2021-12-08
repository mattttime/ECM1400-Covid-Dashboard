UK COVID DASHBOARD

Description:
	This program is a dashboard for displaying UK covid-19 statistics and information.
	It utilises a HTML template for the GUI and Python for the Backend of the program.
	APIs are called through newsapi.com and the uk_covid19 python module and the data-
	-recieved from the requests is rendered into the template.
	This occurs whenever an update is scheduled through the GUI, and the HTML template-
	-has been designed to constantly refresh so that the data is always the most recent-
	-data.
	The flask module has been utilised to render the HTML template as the GUI and to run-
	-a localhost IP address
	This program has been created for University coursework, so the languages and methods-
	-used have been provided.


Installation:
	This dashboard is composed of multiple .py files, a HTML index, a .log file and-
	-a JSON config file.
	All of these files need to be installed for the program to run as intended, and so-
	-the files are in a single package to make installation easier.

Running the program:
	Before execution:
		To run this program, you will need to have access to an IDE which is able to run-
		-python and a web browser of your choice.
		For development, I used Python's IDLE and Google Chrome.
		You will need an API key from newsapi.com to make requests to their servers. Unless-
		-you are implementing this program for non-casual use, the free version should be enough.
	Required Python modules:
		There are a few python modules which need to be installed as they are not in the standard-
		-python module package. This can be done through your device's command prompt.
		1):time
		2):json
		3):logging
		4):sched
		5):uk_covid19
		6):flask
		7):requests
	Steps for execution:
		1):Customise the config file by changing the data after the colons.
		   DO NOT CHANGE THE ORDER OF THE VALUES.
		   Each item has been placed in the file so that the code can find-
		   -the items by index, if the order changes the code will not work.
		   By adding your own api key and location data, the program is-
		   -customisable to you.
		2):Run main.py.
		   If the program runs successfully, you should be able to access-
		   -the interface through http://127.0.0.1:5000/index 
	Creating Updates:
		Once you have got the program running and have loaded the interface,-
		-you can create updates using the forms and checkboxes.
		Time:
			The time form is used to schedule a timer until the update activates-
			-is set in MM:SS format.
		Update label:
			The name of the update to be shown in the 'Scheduled updates' column-
			-of the interface.
		Repeat Update:
			Checkbox to have the update repeat.
		Update Covid data:
			Checkbox to signify the update needs to update covid data.
		Update news articles:
			Checkbox to signify the update needs to update news articles.


Credits:
	HTML template index.html and project specification provided by The University Of Exeter for the first-year module ECM1400-'Programming'


License:

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>