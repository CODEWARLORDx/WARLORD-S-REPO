#include <stdio.h>
int main() 
{
    int num, digit, rev = 0;
    printf("Enter an integer: ");
    scanf("%d", &num);
    // Reverse the integer
    while (num > 0) {
        digit = num % 10;
        rev = (rev * 10) + digit;
        num /= 10;
    }
    // Print the digits as spellings
    while (rev > 0) 
	{
        digit = rev % 10;
        switch (digit) 
		{
            case 0:
                printf("zero ");
                break;
            case 1:
                printf("one ");
                break;
            case 2:
                printf("two ");
                break;
            case 3:
                printf("three ");
                break;
            case 4:
                printf("four ");
                break;
            case 5:
                printf("five ");
                break;
            case 6:
                printf("six ");
                break;
            case 7:
                printf("seven ");
                break;
            case 8:
                printf("eight ");
                break;
            case 9:
                printf("nine ");
                break;
        }
        rev /= 10;
    }
    return 0;
}
