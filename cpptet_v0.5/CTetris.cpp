#include "CTetris.h"

Matrix** CTetris::setOfCBlockObjects = nullptr;

CTetris::CTetris(int dy, int dx) : Tetris::Tetris(dy, dx) {
  currCBlk = new Matrix();
}

void CTetris::init(int *setOfBlockArrays[], int blkTypes, int blkDegrees) {
  Tetris::init(setOfBlockArrays, blkTypes, blkDegrees);
  setOfCBlockObjects = new Matrix*[nBlock.type];
  for(int i = 0; i < nBlock.type; ++i) {
    setOfCBlockObjects[i] = new Matrix[nBlock.degree];
  }

  for(int i = 0; i < nBlock.type; ++i) { 
    for(int j = 0; j < nBlock.degree; ++j) {
      setOfCBlockObjects[i][j] = Matrix(setOfBlockObjects[i][j]);
      setOfCBlockObjects[i][j].mulc(i + 2);
    }
  }
}

TetrisState CTetris::accept(char key) {
  TetrisState state = Tetris::accept(key);
  
  delete currCBlk;
  currCBlk = new Matrix(setOfCBlockObjects[currBlkState.shape.type][currBlkState.shape.degree].get_dy(), setOfCBlockObjects[currBlkState.shape.type][currBlkState.shape.degree].get_dx());
  *currCBlk = setOfCBlockObjects[currBlkState.shape.type][currBlkState.shape.degree];

  Matrix tempCBlk = iScreen->clip(currBlkState.top, currBlkState.left, currBlkState.top + currCBlk->get_dy(), currBlkState.left + currCBlk->get_dy());  
  tempCBlk = tempCBlk.add(currCBlk);
  
  
  oScreen->paste(iScreen, 0, 0);
  oScreen->paste(&tempCBlk, currBlkState.top, currBlkState.left);
  return state;
}

CTetris::~CTetris() {
  for(int i = 0; i < nBlock.type; ++i) {
    delete [] setOfCBlockObjects[i];
  }
  delete setOfCBlockObjects;
  delete currCBlk;
}