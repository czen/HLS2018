/**
 * OSAL behavior definition file.
 */

#include "OSAL.hh"

OPERATION(MIX32)
 TRIGGER

 long data = INT(1);
 unsigned  long steps = UINT(2);
 long x = 0;
 
        x = (data << 1);
	if ((x >> 8) == 1) {
	  x ^= 283;
        }
	if (steps & (1<<0)) {
		x ^= data;
	}
	x = (x << 1);
	if ((x >> 8) == 1) {
	  x ^= 283;
	}
	if (steps & (1<<1)) {
		x ^= data;
	}
	x ^= data;
	x = (x << 1);
	if ((x >> 8) == 1) {
	  x ^= 283;
        }
	if (steps & (1<<2)) {
		x ^= data;
	}

 IO(3) = static_cast<int> (x);

 return true;
 END_TRIGGER;
 END_OPERATION(MIX32)

OPERATION(ROUND32)
 TRIGGER

 long ret = INT(1);
 long x = INT(2);

      ret = (ret << 1);
      if ((ret >> 8) == 1)
	ret ^= 283;
      x ^= (x << 1);
      if ((x >> 8) == 1)
	ret ^= (x ^ 283);
      else
	ret ^= x;

 IO(3) = static_cast<int> (ret);

 return true;
 END_TRIGGER;
 END_OPERATION(ROUND32)
