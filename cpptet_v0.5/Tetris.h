#pragma once
#include "Matrix.h"

enum TetrisState { Running, NewBlock, Finished };

struct Idx {
  int x;
  int y;
  int z;
};

struct BlockShape {
  int type;
  int degree;
};

struct BlockState {
  int top;
  int left;
  BlockShape shape;
};

class Tetris {
 public:
  Tetris(int dy, int dx);
  static void init(int *setOfBlockArrays[], int blkTypes, int blkDegrees);
  TetrisState accept(char key);

  virtual ~Tetris();

  Matrix* oScreen; 
  static int iScreenDw;

 protected:  
  static Matrix** setOfBlockObjects;
  static BlockShape nBlock;
  Matrix* iScreen;
  BlockState currBlkState;
 
 private:
  int* arrayScreen();
  void deleteFullLines();
  void printSetOfBlock(); //testcode
  
  bool justStarted;
  Idx iScreenD;
  Idx arrayScreenD;
  int* tempScreen;
  TetrisState state;
  Matrix currBlk;
};
