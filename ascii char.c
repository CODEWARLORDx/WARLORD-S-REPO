#include <stdio.h>
int main()
{
    int a;
    char b;
    printf("enter a naumer: ");
    scanf("%d",&a);
    b=(char)a;
    printf("the ascii value of the integer %d is %c",a,b);
    return 0;
}