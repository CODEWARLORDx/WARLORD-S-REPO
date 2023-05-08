#include <stdio.h>
#include<string.h>

int main() {
    int choice;
    int a, b;   // variables for performing operations
    
    printf("Menu:\n");
    printf("1. Arithmetic operations\n");
    printf("2. Relational operations\n");
    printf("3. Logical operations\n");
    printf("4. Increment/Decrement operations\n");
    printf("5. Bitwise operations\n");
    printf("6. Assignment/Compound assignment operations\n");
    printf("7. Sizeof operation\n");
    printf("Enter your choice (1-7): ");
    scanf("%d", &choice);
    
    switch (choice) {
        case 1:
            printf("Enter two numbers: ");
            scanf("%d %d", &a, &b);
            printf("Sum: %d\n", a+b);
            printf("Difference: %d\n", a-b);
            printf("Product: %d\n", a*b);
            printf("Quotient: %d\n", a/b);
            printf("Remainder: %d\n", a%b);
            break;
            
        case 2:
            printf("Enter two numbers: ");
            scanf("%d %d", &a, &b);
            printf("%d == %d is %d\n", a, b, a==b);
            printf("%d != %d is %d\n", a, b, a!=b);
            printf("%d > %d is %d\n", a, b, a>b);
            printf("%d < %d is %d\n", a, b, a<b);
            printf("%d >= %d is %d\n", a, b, a>=b);
            printf("%d <= %d is %d\n", a, b, a<=b);
            break;
            
        case 3:
            printf("Enter two logical values (0 or 1): ");
            scanf("%d %d", &a, &b);
            printf("%d AND %d is %d\n", a, b, a&&b);
            printf("%d OR %d is %d\n", a, b, a||b);
            printf("NOT %d is %d\n", a, !a);
            printf("NOT %d is %d\n", b, !b);
            break;
            
        case 4:
            printf("Enter a number: ");
            scanf("%d", &a);
            printf("++%d is %d\n", a, ++a);
            printf("%d++ is %d\n", a, a++);
            printf("--%d is %d\n", a, --a);
            printf("%d-- is %d\n", a, a--);
            break;
            
        case 5:
            printf("Enter two numbers: ");
            scanf("%d %d", &a, &b);
            printf("%d & %d is %d\n", a, b, a&b);
            printf("%d | %d is %d\n", a, b, a|b);
            printf("%d ^ %d is %d\n", a, b, a^b);
            printf("~%d is %d\n", a, ~a);
            printf("~%d is %d\n", b, ~b);
            printf("%d << %d is %d\n", a, b, a<<b);
            printf("%d >> %d is %d\n", a, b, a>>b);
            break;
            
         case 6:
            printf("Enter two numbers: ");
            scanf("%d %d", &a, &b);
            printf("%d += %d is %d\n", a, b, a+=b);
            printf("%d -= %d is %d\n", a, b, a-=b);
            printf("%d *= %d is %d\n", a, b, a*=b);
            printf("%d /= %d is %d\n", a, b, a/=b);
            printf("%d %%= %d is %d\n", a, b, a%=b);
            printf("%d &= %d is %d\n", a, b, a&=b);
            printf("%d |= %d is %d\n", a, b, a|=b);
            printf("%d ^= %d is %d\n", a, b, a^=b);
            printf("%d <<= %d is %d\n", a, b, a<<=b);
            printf("%d >>= %d is %d\n", a, b, a>>=b);
            break;
            
         case 7:
            printf("Enter a data type (int, float, char, double): ");
            char data_type[10];
            scanf("%s", data_type);
            if (strcmp(data_type, "int") == 0) {
                printf("Size of int is %lu bytes\n", sizeof(int));
            } else if (strcmp(data_type, "float") == 0) {
                printf("Size of float is %lu bytes\n", sizeof(float));
            } else if (strcmp(data_type, "char") == 0) {
                printf("Size of char is %lu bytes\n", sizeof(char));
            } else if (strcmp(data_type, "double") == 0) {
                printf("Size of double is %lu bytes\n", sizeof(double));
            } else {
                printf("Invalid data type!\n");
            }
            break;
            
        default:
            printf("Invalid choice!\n");
    }
    
    return 0;
}

