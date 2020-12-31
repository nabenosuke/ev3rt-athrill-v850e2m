#include <stdio.h>

int main(void)
{
  printf("2:46  %f \n", *((double *)(0x090F0000 + 540)));
  printf("2:46  %f \n", *((float *)(0x40010000 + 572)));
  printf("2:46  %f \n", *((float *)(0x40010000)));
  printf("2:46  %f \n", *((float *)(0x40000000)));
  printf("2:46  %f \n", *((float *)(0x40010000 + 572)));
  return 0;
}
