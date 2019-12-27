#include <stdio.h>

int main() {
  #pragma omp parallel
  {
    #pragma omp for
    for (int j = 10 - 1; j >= 0; j--) {
      printf("%d\n", j);
    }
  }
}
