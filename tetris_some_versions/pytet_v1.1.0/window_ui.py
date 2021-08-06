from tetris import *

import curses

##############################################################
### UI code
##############################################################
 
class WindowUI:
    msgWindow = 0
    lock = 0 
    @classmethod
    def printMsg(cls, msg):
        cls.msgWindow.clear()
        cls.msgWindow.addstr(0, 0, msg)
        cls.lock.acquire()
        cls.msgWindow.refresh()
        cls.lock.release()
        return

    @classmethod
    def init(cls, lock, window):
        cls.lock = lock   
        cls.msgWindow = window        

    @classmethod
    def printWindow(cls, window, screen):
        array = screen.get_array()
        window.clear()
    
        def arrayToString(array):
            line = ''
            for x in array:
                if x == 0:
                    line += '□'
                elif x == 1:
                    line += '■'
                else:
                    line += 'XX'

            return line

        for y in range(screen.get_dy()-Tetris.iScreenDw):
            line = arrayToString(array[y][Tetris.iScreenDw:-Tetris.iScreenDw])
            window.addstr(y, 0, line)

            cls.lock.acquire()
            window.refresh()
            cls.lock.release()
        return