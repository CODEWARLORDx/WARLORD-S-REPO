#include <stdio.h>
#include <math.h>
int factorial(int n)
{
    if(n == 0 || n == 1)
        return 1;
    else
        return n * factorial(n-1);
}
int main()
{
    float x, sum=0,y;
    int i, n=10;
    printf("Enter the value of x in degrees: ");
    scanf("%f", &x);
    // convert degrees to radians
    y=x;
    x = x * 3.14159 / 180;
    for(i=0; i<n; i++)
    {
        sum += pow(-1, i) * pow(x, 2*i+1) / factorial(2*i+1);
    }
    printf("sin(%f) = %f", y, sum);
    return 0;
}

