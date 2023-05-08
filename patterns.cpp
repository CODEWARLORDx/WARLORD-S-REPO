#include <stdio.h>

int main() {
    int n, i, j,k,space;
    
    printf("Enter the number of rows: ");
    scanf("%d", &n);
    // for equilatral triangle pattern(B)
       printf("\n\n the regular triangle pattern\n\n");

    for(i = 1; i <= n; i++) {
        for(j = i; j <= n-1; j++) {
            printf(" ");
        }
        for(k = 1; k <= 2*i-1; k++) {
            printf("*");
        }
        printf("\n");
    }
    
           // for upside down regular triangle
              printf("\n\n the upside down trianglle pattern\n\n");

    for (i = n; i >= 1; --i) {
        for (j = 1; j <= n-i; ++j) {
            printf(" ");
        }
        for (j = 1; j <= 2*i-1; ++j) {
            printf("*");
        }
        printf("\n");
    }
    
        // for diamond pattern
        
           printf("\n\n the diamond pattern\n\n");
        space = n - 1;

    for (i = 0; i < n; i++) {
        for (j = 0; j < space; j++) {
            printf(" ");
        }

        for (j = 0; j <= i; j++) {
            printf("* ");
        }

        printf("\n");
        space--;
    }
    

    space = 0;

    for (i = n; i > 0; i--) {
        for (j = 0; j < space; j++) {
            printf(" ");
        }

        for (j = 0; j < i; j++) {
            printf("* ");
        }

        printf("\n");
        space++;
    }
    
    // for hollow diamond pattern
    
       printf("\n\n the hollow diamond pattern\n\n");
    for (i = n; i >= 1; i--) {
        for (j = 1; j <= i; j++) {
            printf("*");
        }
        for (j = 1; j <= 2 * (n - i); j++) {
            printf(" ");
        }
        for (j = 1; j <= i; j++) {
            printf("*");
        }
        printf("\n");
    }

    for (i = 1; i <= n; i++) {
        for (j = 1; j <= i; j++) {
            printf("*");
        }
        for (j = 1; j <= 2 * (n - i); j++) {
            printf(" ");
        }
        for (j = 1; j <= i; j++) {
            printf("*");
        }
        printf("\n");
    }
    
    // right angle triangle pattern (a)
    printf("\n\n the right angle triangle pattern\n\n");
    for(i = 1; i <= n; i++) {
        for(j = 1; j <= i; j++) {
            printf("* ");
        }
        printf("\n");
    }
    
    return 0;
}
