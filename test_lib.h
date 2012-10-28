#include <time.h>

#define EXEC_TIME(fun, result) {\
		clock_t start = clock(); \
		{ \
			fun; \
		} \
		result = ((double)clock() - start) / CLOCKS_PER_SEC;\
	}
