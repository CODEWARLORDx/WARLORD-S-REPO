#include <stdio.h>
int main() 
{
	
    int num, rev= 0, rem, ori;
    printf("Enter an integer: ");
    scanf("%d", &num);
    ori = num;
    while (num != 0)
	 {
        rem = num % 10;
        rev = rev * 10 + rem;
        num /= 10;
    }
    if (ori == rev)
	{
    	printf("%d is a palindrome number.\n", ori);
    } 
	else
	{
        printf("%d is not a palindrome number.\n", ori);
    }
    return 0;
}
