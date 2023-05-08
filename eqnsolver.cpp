#include <stdio.h>
#include <math.h>
int main()
{
	float a,b,c,D,x1,x2,x;
	printf("\nEnter the value of a,b and c in the equation ax2 + bx + c = 0  : \n");// alt code for square is alt+0178
	scanf("%f%f%f",&a,&b,&c);
	D=(pow(b,2)-4*a*c);
	if(a==0 && b==0)
	{
		printf("\n Sorry!! There is no solution");
	}
	else if(a==0)
	{
		x=-c/b;
		printf("\n The root of this equation, x = %f",x);
	}
	else if(D<0)
	{
		printf("\n The roots of this equation exists...but they are imaginary");
	}
	else if(D>=0)
	{
		x1=(-b+(sqrt(D)))/(2*a);
		x2=(-b-(sqrt(D)))/(2*a);
		printf("\nThe roots of this equation are x1=%f and x2=%f .",x1,x2);
	}
	else
	printf("\n Bad gateway!!! Error 404 not found");
	return 0;
}
