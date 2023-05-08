#include <stdio.h>

int main()
{
    float r=0,a,c;

    printf("\n Please enter the value of radius\n");
    scanf("%f",&r);
    a=3.14259*r*r;
    c=2*3.14259*r;
    printf("\nThe circumfearence of the circle is : %f",c);
    printf("\nThe area of the circle is : %f",a);
    return 0;
}