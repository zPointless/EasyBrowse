# importing required libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import sys

#variables
def variable_keep(index, title, url):
	default_site = 'https://google.com'    #set default site. template: 'https://greatsite.com'
	primarysearch = 'google.com'    #primary search site. template : 'bestsearch.com'
	milliseconds_upgrade = 30    #update in milliseconds - answer as a integer
	appname = 'EasyBrowse PRO'   #set app name
	#KEEP THE F - Page title. use {url/title} 
	#(url as the current url in the bar or title as the page title. just add more.)
	#e.g. f'{url} -  {title}' would display 'https://google.com - Google' if you were on https://google.com/
	page_title = title
	listr = [default_site, primarysearch, milliseconds_upgrade, page_title, appname]
	return listr[index]

# creating main window class
class MainWindow(QMainWindow):
	# constructor
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		# creating a QWebEngineView
		self.browser = QWebEngineView()

		#setting default browser url as google
		self.browser.setUrl(QUrl(variable_keep(0, 'title', '')))

		# adding action when url get changed
		self.browser.urlChanged.connect(self.update_urlbar)

		# adding action when loading is finished
		self.browser.loadFinished.connect(self.update_title)

		# set this browser as central widget or main window
		self.setCentralWidget(self.browser)

		# creating a status bar object
		self.status = QStatusBar()

		# adding status bar to the main window
		self.setStatusBar(self.status)

		# creating QToolBar for navigation
		navtb = QToolBar("Navigation")

		# adding this tool bar tot he main window
		self.addToolBar(navtb)

		# adding actions to the tool bar
		# creating a action for back
		back_btn = QAction("Back", self)
		# setting status tip
		back_btn.setStatusTip("Back to previous page")

		# adding action to the back button
		# making browser go back
		back_btn.triggered.connect(self.browser.back)

		# adding this action to tool bar
		navtb.addAction(back_btn)

		# similarly for forward action
		next_btn = QAction("Forward", self)
		next_btn.setStatusTip("Forward to next page")
		# adding action to the next button
		# making browser go forward
		next_btn.triggered.connect(self.browser.forward)
		navtb.addAction(next_btn)

		# similarly for reload action
		reload_btn = QAction("Reload", self)
		reload_btn.setStatusTip("Reload page")
		# adding action to the reload button
		# making browser to reload
		reload_btn.triggered.connect(self.browser.reload)
		navtb.addAction(reload_btn)

		# similarly for home action
		home_btn = QAction("Stop", self)
		home_btn.setStatusTip("Stop loading current page")
		home_btn.triggered.connect(self.browser.stop)
		navtb.addAction(home_btn)

		# adding a separator in the tool bar
		navtb.addSeparator()

		# creating a line edit for the url
		self.urlbar = QLineEdit()

		# adding action when return key is pressed
		self.urlbar.returnPressed.connect(self.navigate_to_url)

		# adding this to the tool bar
		navtb.addWidget(self.urlbar)

		# adding stop action to the tool bar
		stop_btn = QAction("Go", self)
		stop_btn.setStatusTip("Go to current URL")
		# adding action to the stop button
		# making browser to stop
		stop_btn.triggered.connect(self.navigate_home)
		navtb.addAction(stop_btn)

		# showing all the components
		self.show()
		self.zoom_timer = QTimer(self)
		self.zoom_timer.timeout.connect(self.constant_method)
		self.zoom_timer.start(variable_keep(2, '', ''))

	# method for updating the title of the window
	def update_title(self):
		title = self.browser.page().title()
		url = self.urlbar.text()
		self.setWindowTitle(variable_keep(3, title, url))

	# method called by the home action
	def navigate_home(self):
		# getting url and converting it to QUrl object
		q = QUrl(self.urlbar.text())
		schemeset=True
		# if url is scheme is blank
		if q.scheme() == "":
			if '.' in self.urlbar.text():
				q.setScheme("http")
				schemeset = False
			if schemeset:
				q = self.urlbar.text()
				coolset = [q, variable_keep(1, "", "")]
				q = QUrl('https:///search?q=%s[1]'%coolset)

		# set the url to the browser
		self.browser.setUrl(q)

	# method called by the line edit when return key is pressed
	def navigate_to_url(self):
		schemeset = True
		# getting url and converting it to QUrl object
		q = QUrl(self.urlbar.text())
		self.urlbar.clearFocus()
		# if url is scheme is blank
		if q.scheme() == "":
			if '.' in self.urlbar.text():
				schemeset = False
				# set url scheme to html
				q.setScheme("http")
			if schemeset:
				q = self.urlbar.text()
				rq = variable_keep(1, "", "")
				q = QUrl('https://'+ rq +'/search?q='+q)
		# set the url to the browser
		self.browser.setUrl(q)

	# method for updating url
	# this method is called by the QWebEngineView object
	def update_urlbar(self, q):
		# setting text to the url bar
		self.urlbar.setText(q.toString())

		# setting cursor position of the url bar
		self.urlbar.setCursorPosition(0)

	def constant_method(self):
		self.browser.setZoomFactor(1.0)
		print("\033c")

# creating a pyQt5 application
app = QApplication(sys.argv)

# setting name to the application
app.setApplicationName(variable_keep(4, '', ''))

# creating a main window object
window = MainWindow()

# loop
app.exec_()
