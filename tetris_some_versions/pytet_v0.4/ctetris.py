from tetris import *

class CTetris(Tetris):
    def accept(self, key): 
        self.state = TetrisState.Running 
        		
        if key >= '0' and key <= '6':
            if self.justStarted == False:
                self.deleteFullLines()
                
            self.iScreen = Matrix(self.oScreen)
            self.idxBlockType = int(key)
            self.idxBlockDegree = 0
            self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
            self.top = 0
            self.left = Tetris.iScreenDw + self.iScreenDx//2 - self.currBlk.get_dx()//2
            self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
            self.binaryTempBlk = self.tempBlk.binary() + self.currBlk.binary()
            self.tempBlk = self.tempBlk + self.currBlk
            self.justStarted = False
            print()

            if self.binaryTempBlk.anyGreaterThan(1):
                self.state = TetrisState.Finished
            self.oScreen = Matrix(self.iScreen)
            self.oScreen.paste(self.tempBlk, self.top, self.left)
            return self.state
        elif key == 'q':
            pass
        elif key == 'a': # move left
            self.left -= 1
        elif key == 'd': # move right
            self.left += 1
        elif key == 's': # move down
            self.top += 1
        elif key == 'w': # rotate the block clockwise
            self.idxBlockDegree = (self.idxBlockDegree + 1) % Tetris.nBlockDegrees
            self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
        elif key == ' ': # drop the block
            while not self.binaryTempBlk.anyGreaterThan(1):
                    self.top += 1
                    self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
                    self.binaryTempBlk = self.tempBlk.binary() + self.currBlk.binary()
        else:
            print('Wrong key!!!')

        self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
        self.binaryTempBlk = self.tempBlk.binary() + self.currBlk.binary()
        self.tempBlk = self.tempBlk + self.currBlk

        if self.binaryTempBlk.anyGreaterThan(1):   ## 벽 충돌시 undo 수행
            if key == 'a': # undo: move right
                self.left += 1
            elif key == 'd': # undo: move left
                self.left -= 1
            elif key == 's': # undo: move up
                self.top -= 1
                self.state = TetrisState.NewBlock
            elif key == 'w': # undo: rotate the block counter-clockwise
                self.idxBlockDegree = (self.idxBlockDegree - 1) % Tetris.nBlockDegrees
                self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
            elif key == ' ': # undo: move up
                self.top -= 1
                self.state = TetrisState.NewBlock

            self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
            self.tempBlk = self.tempBlk + self.currBlk
  
        self.oScreen = Matrix(self.iScreen)
        self.oScreen.paste(self.tempBlk, self.top, self.left)
 
        return self.state

    def deleteFullLines(self):
        self.iScreen = Matrix(self.oScreen);
        top = self.top;
        for i in range(self.currBlk.get_dy()):
            if(top >= self.iScreenDy):
                break
            tempBlk = self.iScreen.clip(top, Tetris.iScreenDw, top + 1, Tetris.iScreenDw + self.iScreenDx)
            if self.iScreenDx == tempBlk.binary().sum():
                tempBlk = self.iScreen.clip(0, Tetris.iScreenDw, top, Tetris.iScreenDw + self.iScreenDx)
                self.iScreen.paste(tempBlk, 1, Tetris.iScreenDw)
            top += 1
        self.oScreen = Matrix(self.iScreen)
 
