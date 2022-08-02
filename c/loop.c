#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>


uint64_t  __attribute__((noinline)) do_cal(int i, int j) {
    return 200 + i + j;
}

int main() {
    uint64_t sum = 0;
    for (size_t i = 0; i < 1000; i++) {
        for (size_t j = 0; j < 1000; j++) {
            sum += do_cal(i, j);
        }
    }
    printf("sum = %lu\n", sum);
}


