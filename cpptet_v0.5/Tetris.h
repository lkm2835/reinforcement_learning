#pragma once
#include "Matrix.h"

enum TetrisState { Running, NewBlock, Finished };

struct Idx {
  int x;
  int y;
  int z;
};

struct BlockState {
  int idxBlockType;
  int idxBlockDegree;
  int top;
  int left;
};

class Tetris {
 public:
  Tetris(int dy, int dx);
  static void init(int *setOfBlockArrays[], int blkTypes, int blkDegrees);
  TetrisState accept(char key);

  ~Tetris();

  Matrix* oScreen; 
  static int iScreenDw;
  static Matrix** setOfBlockObjects;
  
 private:
  int* arrayScreen();
  void deleteFullLines();
  void printSetOfBlock(); //testcode

  bool justStarted;
  static int nBlockTypes;
  static int nBlockDegrees;
  Idx iScreenD;
  Idx arrayScreenD;
  int* tempScreen;
  Matrix* iScreen;
  TetrisState state;
  BlockState currBlkState;
  Matrix* currBlk;
};
