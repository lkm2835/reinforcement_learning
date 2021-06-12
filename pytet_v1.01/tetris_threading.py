from tetris import *
from abc import *
from window_ui import *

import sys
import time
import threading

##############################################################
### Threading code (Observer pattern)
##############################################################

def getChar():
	ch = sys.stdin.read(1)
	return ch

class Publisher(metaclass = ABCMeta):
	@abstractmethod
	def addObserver(self, observer):
		pass

	@abstractmethod
	def notifyObservers(self, key):
		pass


class Observer(metaclass = ABCMeta):
	@abstractmethod
	def update(self, key):
		pass


isGameDone = False


class KeyController(threading.Thread, Publisher):
	def __init__(self, *args, **kwargs):
		super(KeyController, self).__init__(*args[1:], **kwargs)
		self.name = args[0]
		self.observers = list()
		return

	def addObserver(self, observer):
		self.observers.append(observer)
		return
	
	def notifyObservers(self, key):
		for observer in self.observers:
			observer.update(key)
		return

	def run(self):
		global isGameDone

		while not isGameDone:
			try:
				key = getChar()
			except:
				isGameDone = True
				WindowUI.printMsg('getChar() wakes up!!')
				break

			self.notifyObservers(key)

		WindowUI.printMsg('%s terminated... Press any key to continue' % self.name)
		time.sleep(1)
		self.notifyObservers('')
		return


class TimeController(threading.Thread, Publisher):
	def __init__(self, *args, **kwargs):
		super(TimeController, self).__init__(*args[1:], **kwargs)
		self.name = args[0]
		self.observers = list()
		return

	def addObserver(self, observer):
		self.observers.append(observer)
		return
	
	def notifyObservers(self, key):
		for observer in self.observers:
			observer.update(key)
		return

	def run(self):
		while not isGameDone:
			time.sleep(1)
			self.notifyObservers('y')

		WindowUI.printMsg('%s terminated... Press any key to continue' % self.name)
		time.sleep(1)
		self.notifyObservers('')
		return


class Model(threading.Thread, Observer, Publisher):
	def __init__(self, *args, **kwargs):
		super(Model, self).__init__(*args[1:], **kwargs)
		self.name = args[0]
		self.queue = list()
		self.observers = list()
		self.cv = threading.Condition()
		return

	def update(self, key):
		self.cv.acquire()
		self.queue.append(key)
		self.cv.notify()
		self.cv.release()
		return
	
	def read(self):
		self.cv.acquire()
		while len(self.queue) < 1:
			self.cv.wait()
		key = self.queue.pop(0)
		self.cv.release()
		return key
	
	def addKeypad(self, keypad):
		self.keypad = keypad
		return

	def addObserver(self, observer):
		self.observers.append(observer)
		return

	def notifyObservers(self, key):
		for observer in self.observers:
			observer.update(key)
		return

	def run(self):
		global isGameDone

		setOfBlockArrays = Tetris.initSetOfBlockArrays()

		Tetris.init(setOfBlockArrays)
		board = Tetris(20, 15)

		idxBlockType = randint(0, Tetris.nBlocks-1)
		key = str(idxBlockType)
		state = board.accept(key)
		self.notifyObservers(board.getScreen())

		while not isGameDone:
			key = self.read()
			if key == '':
				break
			if key not in self.keypad:
				continue

			key = self.keypad[key]
			if key == 'q':
				state = TetrisState.Finished
			else:
				state = Tetris.processKey(self, board, key)

			if state == TetrisState.Finished:
				isGameDone = True
				WindowUI.printMsg('%s IS DEAD!!!' % self.name)
				time.sleep(2)
				break

		WindowUI.printMsg('%s terminated... Press any key to continue' % self.name)
		time.sleep(1)
		self.notifyObservers(board.getScreen())
		return

class View(threading.Thread, Observer):
	def __init__(self, *args, **kwargs):
		super(View, self).__init__(*args[1:], **kwargs)
		self.name = args[0]
		self.queue = list()
		self.observers = list()
		self.cv = threading.Condition()
		return

	def update(self, key):
		self.cv.acquire()
		self.queue.append(key)
		self.cv.notify()
		self.cv.release()
		return

	def read(self):
		self.cv.acquire()
		while len(self.queue) < 1:
			self.cv.wait()
		key = self.queue.pop(0)
		self.cv.release()
		return key

	def addWindow(self, window):
		self.window = window
		return

	def run(self):
		global isGameDone
		while not isGameDone:
			oScreen = self.read()
			WindowUI.printWindow(self.window, oScreen)
		
		WindowUI.printMsg('%s terminated... Press any key to continue' % self.name)
		time.sleep(1)
		return