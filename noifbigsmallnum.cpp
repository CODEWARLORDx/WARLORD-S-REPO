#include <stdio.h>

int main() {
   int a, b, c;
   printf("Enter three numbers: ");
   scanf("%d %d %d", &a, &b, &c);
   
   int max = (a > b) ? ((a > c) ? a : c) : ((b > c) ? b : c);
   int min = (a < b) ? ((a < c) ? a : c) : ((b < c) ? b : c);
   
   printf("The largest number is %d\n", max);
   printf("The smallest number is %d\n", min);
   
   return 0;
}

