#pragma once
#include "Matrix.h"

enum TetrisState { Running, NewBlock, Finished };

class Tetris {
 public:
  Tetris(int dy, int dx);
  static void init(int *setOfBlockArrays[], int blkTypes, int blkDegrees);
  TetrisState accept(char key);

  ~Tetris();

  Matrix* oScreen; 
  int iScreenDw;
  static Matrix** setOfBlockObjects;
  

 private:
  int* arrayScreen();
  void deleteFullLines();
  void printSetOfBlock(); //test

  bool justStarted;
  int nBlockTypes = 0;
  int nBlockDegrees = 0;
  int iScreenDy = 0;
  int iScreenDx = 0;
  int arrayScreenDy = 0;
  int arrayScreenDx = 0;
  int* tempScreen;
  Matrix* iScreen;
  int top;
  int left;
  Matrix* currBlk;
  int idxBlockType;
  int idxBlockDegree;
  
  TetrisState state;
  
};
