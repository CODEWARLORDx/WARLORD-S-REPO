#include <stdio.h>
int decimalToBinary(int decimal) 
{
    int binary = 0, base = 1;
    while (decimal > 0) 
	{
        binary += (decimal % 2) * base;
        decimal /= 2;
        base *= 10;
    }
    return binary;
}
int binaryToDecimal(int binary) 
{
    int decimal = 0, base = 1;
    while (binary > 0) 
	{
        decimal += (binary % 10) * base;
        binary /= 10;
        base *= 2;
    }
    return decimal;
}
int main() 
{
    int choice, num;
    do {
        printf("Enter your choice:\n");
        printf("1. Convert decimal to binary\n");
        printf("2. Convert binary to decimal\n");
        printf("3. Exit\n");
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                printf("Enter a decimal number: ");
                scanf("%d", &num);
                printf("Binary equivalent: %d\n", decimalToBinary(num));
                break;
            case 2:
                printf("Enter a binary number: ");
                scanf("%d", &num);
                printf("Decimal equivalent: %d\n", binaryToDecimal(num));
                break;
            case 3:
                printf("Exiting program...\n");
                break;
            default:
                printf("Invalid choice. Please enter again.\n");
        }
    } while (choice != 3);
    return 0;
}
