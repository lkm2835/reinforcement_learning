#include <iostream>
#include <cstring>
#include <cmath>
#include "Tetris.h"

Matrix** Tetris::setOfBlockObjects = nullptr;

Tetris::Tetris(int dy, int dx) {
  iScreenDy = dy;
  iScreenDx = dx;
  iScreenDw = 4; // 수정필요 
  iScreen = new Matrix(arrayScreen(), arrayScreenDy, arrayScreenDx);
  oScreen = new Matrix(iScreen);
  justStarted = true;


  //printSetOfBlock(); //test
}

void Tetris::init(int *setOfBlockArrays[], int blkTypes, int blkDegrees) {
  setOfBlockObjects = new Matrix*[blkTypes];
  for(int i = 0; i < blkTypes; ++i) {
    setOfBlockObjects[i] = new Matrix[blkDegrees];
  }

  for(int i = 0; i < blkTypes; ++i) { 
    for(int j = 0; j < blkDegrees; ++j) {
      int k = 0;
      while(setOfBlockArrays[i * blkDegrees + j][k] != -1) {
        k += 1;
      }
      int len = sqrt(k);
      setOfBlockObjects[i][j] = Matrix(setOfBlockArrays[i * blkDegrees + j], len, len);
      //setOfBlockObjects[i][j].print();
    }
  }
}

TetrisState Tetris::accept(char key) {
  state = Running;
  Matrix tempBlk;
  if (key >= '0' && key <= '6') {
    if (justStarted == false) {
      deleteFullLines();
    }
    delete iScreen;
    iScreen = new Matrix(oScreen);
    idxBlockType = key - '0';
    idxBlockDegree = 0;
    currBlk = new Matrix(setOfBlockObjects[idxBlockType][idxBlockDegree].get_dy(), setOfBlockObjects[idxBlockType][idxBlockDegree].get_dx());
    *currBlk = setOfBlockObjects[idxBlockType][idxBlockDegree];
    top = 0;
    left = iScreenDw + iScreenDx / 2 - currBlk->get_dx() / 2;
    tempBlk = iScreen->clip(top, left, top + currBlk->get_dy(), left + currBlk->get_dy());
    tempBlk = tempBlk.add(currBlk);
    justStarted = false;
    cout << endl;

    if (tempBlk.anyGreaterThan(1)) {
      state = Finished;
    }
    delete oScreen;
    oScreen = new Matrix(iScreen);
    oScreen->paste(&tempBlk, top, left);
    return state;
  }
  else if (key == 'q') {}
  else if (key == 'a') { left -= 1; }
  else if (key == 'd') { left += 1; }
  else if (key == 's') { top += 1; }
  else if (key == 'w') {
    idxBlockDegree += 1;
    idxBlockDegree %= 4;
    *currBlk = setOfBlockObjects[idxBlockType][idxBlockDegree];
  }
  else if (key == ' ') {
    while(!tempBlk.anyGreaterThan(1)) {
      top += 1;
      tempBlk = iScreen->clip(top, left, top + currBlk->get_dy(), left + currBlk->get_dy());
      tempBlk = tempBlk.add(currBlk);
    }
  }

  tempBlk = iScreen->clip(top, left, top + currBlk->get_dy(), left + currBlk->get_dy());
  tempBlk = tempBlk.add(currBlk);
  
  if (tempBlk.anyGreaterThan(1)) { // undo
    if (key == 'a') {
      left += 1;
    }
    else if (key == 'd') {
      left -= 1;
    }
    else if (key == 's') {
      top -= 1;
      state = NewBlock;
    }
    else if (key == 'w') {
      idxBlockDegree -= 1;
      idxBlockDegree += 4;
      idxBlockDegree %= 4;
      cout << idxBlockDegree;
      *currBlk = setOfBlockObjects[idxBlockType][idxBlockDegree];
    }
    else if (key == ' ') {
      top -= 1;
      state = NewBlock;
    }
    tempBlk = iScreen->clip(top, left, top + currBlk->get_dy(), left + currBlk->get_dy());
    tempBlk = tempBlk.add(currBlk);
  }
  //delete oScreen;
  //oScreen = new Matrix(iScreen);
  oScreen->paste(iScreen, 0, 0);
  oScreen->paste(&tempBlk, top, left);
  
  return state;
}

int* Tetris::arrayScreen() {
  arrayScreenDy = iScreenDy + iScreenDw;
  arrayScreenDx = iScreenDx + iScreenDw * 2;
  
  tempScreen = new int[arrayScreenDy * arrayScreenDx];
  memset(tempScreen, 0, sizeof(int) * arrayScreenDy * arrayScreenDx);
  
  for (int y = 0; y < iScreenDy; ++y) {
    for (int x = iScreenDw; x < iScreenDx + iScreenDw; ++x) {
      tempScreen[y * (arrayScreenDx) + x] = -1;
    }
  }

  for (int y = 0; y < arrayScreenDy; ++y) {
    for (int x = 0; x < arrayScreenDx; ++x) {
      tempScreen[y * (arrayScreenDx) + x] += 1;
    }
  }

  return tempScreen;
}

void Tetris::deleteFullLines() {
  iScreen->paste(oScreen, 0, 0);
  int t = top;
  for (int i = 0; i < currBlk->get_dy(); ++i) {
    if (t >= iScreenDy) break;
    
    Matrix tempBlk = iScreen->clip(t, iScreenDw, t + 1, iScreenDw + iScreenDx);
    if (iScreenDx == tempBlk.sum()) {
      tempBlk = iScreen->clip(0, iScreenDw, t, iScreenDw + iScreenDx);
      iScreen->paste(&tempBlk, 1, iScreenDw);
    }
    t += 1;
  }
  oScreen->paste(iScreen, 0, 0);
}

void Tetris::printSetOfBlock() {
  for (int i = 0; i < 7; ++i) { 
    for (int j = 0; j < 4; ++j) {
      int** tempArr = setOfBlockObjects[i][j].get_array();
      int dy = setOfBlockObjects[i][j].get_dy();
      int dx = setOfBlockObjects[i][j].get_dx();
      
      for (int y = 0; y < dy; ++y) {
        for (int x = 0; x < dx; ++x) {
          if (tempArr[y][x] == 0) cout << "□";
          else/* if (array[y][x] == 1)*/cout << "■";
        }
        std::cout << std::endl;
      }
      std::cout << std::endl;

    }
  }
}

Tetris::~Tetris() {
  delete [] tempScreen;
}