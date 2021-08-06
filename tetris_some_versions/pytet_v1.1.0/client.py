from random import *
from window_ui import *
from tetris_threading import *

import os
import sys
import tty
import termios

import threading
import curses

##############################################################
### Main code
##############################################################
def main(args):
	print("TEST")
	
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client_socket.connect(('127.0.0.1', 10000))
		while True:
			continue
	except:
		print("connect fail")
		return
	seedNum = list()
	seedNum.append(str(randint(1,10000)))
	seedNum.append(str(randint(1,10000))) 
	client_socket.send(str(seedNum).encode())
	client_socket.close()
	seed(seedNum[0])

	screen = curses.initscr()
	screen.clear()
	
	curses.echo()
	curses.start_color()
	curses.use_default_colors()

	win1 = curses.newwin(20, 30, 0, 0)
	win2 = curses.newwin(20, 30, 0, 40)
	win0 = curses.newwin(3, 70, 21, 0)

	lock = threading.Lock()
	WindowUI.init(lock, win0)

	th_view1 = View('view1')
	th_view1.addWindow(win1)

	th_scont1 = SendController('scont', 10001)

	keypad = { 'q': 'q', 'w': 'w', 'a': 'a', 's': 'y', 'd': 'd', ' ': ' ', 'y': 'y' }
	th_model1 = Model('model1')
	th_model1.addKeypad(keypad)
	th_model1.addObserver(th_view1)
	th_model1.addObserver(th_scont1)

	th_kcont = KeyController('kcont')
	th_kcont.addObserver(th_model1)

	th_tcont = TimeController('tcont')
	th_tcont.addObserver(th_model1)

	threads = list()
	threads.append(th_view1)
	threads.append(th_model1)
	threads.append(th_scont1)
	threads.append(th_kcont)
	threads.append(th_tcont)

	exited = list()

	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	tty.setcbreak(sys.stdin.fileno())

	for th in threads:
		th.start()
	
	for th in threads:
		th.join()
		exited.append(th.name)
	
	string = ''
	for name in exited:
		string += ':%s' % name
	string += ' terminated!!!'

	WindowUI.printMsg(string)
	time.sleep(2)
	WindowUI.printMsg('Program terminated...')
	time.sleep(1)

curses.wrapper(main)
### end of main.py