#include <iostream>
#include <cstring>
#include <cmath>
#include "Tetris.h"

Matrix** Tetris::setOfBlockObjects = nullptr;
int Tetris::iScreenDw = 0;
int Tetris::nBlockTypes = 0;
int Tetris::nBlockDegrees = 0;

Tetris::Tetris(int dy, int dx) {
  iScreenD.y = dy;
  iScreenD.x = dx;
  iScreen = new Matrix(arrayScreen(), arrayScreenD.y, arrayScreenD.x);
  oScreen = new Matrix(iScreen);
  justStarted = true;
}

int blkArrayLength(int *setOfBlockArrays[], int num) {
  int size = 0;
  while(setOfBlockArrays[num][size] != -1) {
    size += 1;
  }
  return sqrt(size);  
}

void Tetris::init(int *setOfBlockArrays[], int blkTypes, int blkDegrees) {
  nBlockTypes = blkTypes;
  nBlockDegrees = blkDegrees;
  setOfBlockObjects = new Matrix*[nBlockTypes];
  for(int i = 0; i < nBlockTypes; ++i) {
    setOfBlockObjects[i] = new Matrix[nBlockDegrees];
  }

  int maxLength = 0;
  for(int i = 0; i < nBlockTypes; ++i) { 
    for(int j = 0; j < nBlockDegrees; ++j) {
      int len = blkArrayLength(setOfBlockArrays, i * nBlockDegrees + j);
      setOfBlockObjects[i][j] = Matrix(setOfBlockArrays[i * nBlockDegrees + j], len, len);
      
      if (maxLength < len) {
        maxLength = len;
      }
    }
  }
  iScreenDw = maxLength;
}

TetrisState Tetris::accept(char key) {
  state = Running;
  Matrix tempBlk;
  
  if (key >= '0' && key <= ('0' + nBlockTypes - 1)) {
    if (justStarted == false) {
      deleteFullLines();
    }
    delete iScreen;
    iScreen = new Matrix(oScreen);
    currBlkState.idxBlockType = key - '0';
    currBlkState.idxBlockDegree = 0;
    currBlk = new Matrix(setOfBlockObjects[currBlkState.idxBlockType][currBlkState.idxBlockDegree].get_dy(), setOfBlockObjects[currBlkState.idxBlockType][currBlkState.idxBlockDegree].get_dx());
    *currBlk = setOfBlockObjects[currBlkState.idxBlockType][currBlkState.idxBlockDegree];
    currBlkState.top = 0;
    currBlkState.left = iScreenDw + iScreenD.x / 2 - currBlk->get_dx() / 2;
    tempBlk = iScreen->clip(currBlkState.top, currBlkState.left, currBlkState.top + currBlk->get_dy(), currBlkState.left + currBlk->get_dy());
    tempBlk = tempBlk.add(currBlk);
    justStarted = false;
    cout << endl;

    if (tempBlk.anyGreaterThan(1)) {
      state = Finished;
    }
    oScreen->paste(iScreen, 0, 0);
    oScreen->paste(&tempBlk, currBlkState.top, currBlkState.left);
    return state;
  }
  else if (key == 'q') {}
  else if (key == 'a') { currBlkState.left -= 1; }
  else if (key == 'd') { currBlkState.left += 1; }
  else if (key == 's') { currBlkState.top += 1; }
  else if (key == 'w') {
    currBlkState.idxBlockDegree += 1;
    currBlkState.idxBlockDegree %= nBlockDegrees;
    *currBlk = setOfBlockObjects[currBlkState.idxBlockType][currBlkState.idxBlockDegree];
  }
  else if (key == ' ') {
    while(!tempBlk.anyGreaterThan(1)) {
      currBlkState.top += 1;
      tempBlk = iScreen->clip(currBlkState.top, currBlkState.left, currBlkState.top + currBlk->get_dy(), currBlkState.left + currBlk->get_dy());
      tempBlk = tempBlk.add(currBlk);
    }
  }

  tempBlk = iScreen->clip(currBlkState.top, currBlkState.left, currBlkState.top + currBlk->get_dy(), currBlkState.left + currBlk->get_dy());
  tempBlk = tempBlk.add(currBlk);
  
  if (tempBlk.anyGreaterThan(1)) { // undo
    if (key == 'a') {
      currBlkState.left += 1;
    }
    else if (key == 'd') {
      currBlkState.left -= 1;
    }
    else if (key == 's') {
      currBlkState.top -= 1;
      state = NewBlock;
    }
    else if (key == 'w') {
      currBlkState.idxBlockDegree += (nBlockDegrees - 1);
      currBlkState.idxBlockDegree %= nBlockDegrees;
      *currBlk = setOfBlockObjects[currBlkState.idxBlockType][currBlkState.idxBlockDegree];
    }
    else if (key == ' ') {
      currBlkState.top -= 1;
      state = NewBlock;
    }
    tempBlk = iScreen->clip(currBlkState.top, currBlkState.left, currBlkState.top + currBlk->get_dy(), currBlkState.left + currBlk->get_dy());
    tempBlk = tempBlk.add(currBlk);
  }
  oScreen->paste(iScreen, 0, 0);
  oScreen->paste(&tempBlk, currBlkState.top, currBlkState.left);
  
  return state;
}

int* Tetris::arrayScreen() {
  arrayScreenD.y = iScreenD.y + iScreenDw;
  arrayScreenD.x = iScreenD.x + iScreenDw * 2;
  
  tempScreen = new int[arrayScreenD.y * arrayScreenD.x];
  memset(tempScreen, 0, sizeof(int) * arrayScreenD.y * arrayScreenD.x);
  
  for (int y = 0; y < iScreenD.y; ++y) {
    for (int x = iScreenDw; x < iScreenD.x + iScreenDw; ++x) {
      tempScreen[y * (arrayScreenD.x) + x] = -1;
    }
  }

  for (int y = 0; y < arrayScreenD.y; ++y) {
    for (int x = 0; x < arrayScreenD.x; ++x) {
      tempScreen[y * (arrayScreenD.x) + x] += 1;
    }
  }

  return tempScreen;
}

void Tetris::deleteFullLines() {
  iScreen->paste(oScreen, 0, 0);
  int t = currBlkState.top;
  for (int i = 0; i < currBlk->get_dy(); ++i) {
    if (t >= iScreenD.y) break;
    
    Matrix tempBlk = iScreen->clip(t, iScreenDw, t + 1, iScreenDw + iScreenD.x);
    if (iScreenD.x == tempBlk.sum()) {
      tempBlk = iScreen->clip(0, iScreenDw, t, iScreenDw + iScreenD.x);
      iScreen->paste(&tempBlk, 1, iScreenDw);
    }
    t += 1;
  }
  oScreen->paste(iScreen, 0, 0);
}

//test
void Tetris::printSetOfBlock() {
  for (int i = 0; i < nBlockTypes; ++i) { 
    for (int j = 0; j < nBlockDegrees; ++j) {
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
  for(int i = 0; i < nBlockTypes; ++i) {
    delete [] setOfBlockObjects[i];
  }
  delete setOfBlockObjects;
  delete [] tempScreen;
  delete currBlk;
  delete oScreen;
  delete iScreen;
}
