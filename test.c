#include <stdio.h>

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
}
