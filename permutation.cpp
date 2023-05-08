#include <stdio.h>
int fact(int n)
{
    if(n == 0 || n == 1)
        return 1;
    else
        return n * fact(n-1);
}
int main()
{
    int n, r, per;
    printf("Enter n and r: ");
    scanf("%d %d", &n, &r);
    per = fact(n) / fact(n-r);
    printf("Permutation of %d objects taking %d objects at a time is %d", n, r, per);
    return 0;
}
