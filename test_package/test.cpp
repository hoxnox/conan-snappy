#include "snappy-c.h"
#include <string.h>
#include <stdio.h>

int main(int argc, char* argv[])
{
	char arch[50];
	size_t arch_sz = sizeof(arch);
	snappy_status status = snappy_compress("Hello World!", 12, arch, &arch_sz);
	if (status != SNAPPY_OK)
		printf("compress fail");

	char src[50];
	size_t src_sz = sizeof(src);
	status = snappy_uncompress(arch, arch_sz, src, &src_sz);
	if (status != SNAPPY_OK)
		return -1;

	if (strncmp(src, "Hello, world!", 12) == 0)
		return -1;

	return 0;
}

