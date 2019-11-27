/**
 * OSAL behavior definition file.
 */

#include "OSAL.hh"

OPERATION(FILTEP)
 TRIGGER

 unsigned long rlt1 = UINT(1);
 unsigned long al1 = UINT(2);
 unsigned long rlt2 = UINT(3);
 unsigned long al2 = UINT(4);

  long int pl, pl2;
  int res = 0;
  pl = 2 * rlt1;
  pl = (long) al1 *pl;
  pl2 = 2 * rlt2;
  pl += (long) al2 *pl2;
  res =  ((int) (pl >> 15));

 

 IO(5) = static_cast<int> (res);

 return true;
 END_TRIGGER;
 END_OPERATION(FILTEP)
