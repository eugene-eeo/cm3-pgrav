#include <stdlib.h>
#include <stdio.h>
#include <math.h>

int main() {
  #pragma omp parallel
  {
    #pragma omp for
    for (int j = 10 - 1; j >= 0; j--) {
      printf("b %d\n", j);
    }
    #pragma omp for
    for (int j = 10 - 1; j >= 0; j--) {
      printf("a %d\n", j);
    }
  }

  double* a = (double*)calloc(100, sizeof(double));
  double* b = (double*)calloc(100, sizeof(double));
  double* c = (double*)calloc(100, sizeof(double));

  for (int i = 0; i < 100; i++) {
    a[i] = rand();
    b[i] = rand();
    c[i] = 0;
  }

  double max = 0;

#pragma omp simd reduction(max: max)
  for (int i = 0; i < 100; i++) {
    c[i] += a[i] + b[i];
    if (c[i] > max) max = c[i];
  }

  double newmax = 0;

  for (int i = 0; i < 100; i++) {
    if (c[i] > newmax) newmax = c[i];
    if (c[i] != (a[i] + b[i])) {
      printf("wrong\n");
    }
  }

  if (newmax != max) {
    printf("wrong\n");
  }
}
