#include<stdio.h>
int main()
{
	float x;
	int y,n;
	printf("Enter the value of x: ");
	scanf("%f",&x);
	
	//using nested if.
	if(x!=0)
	{
		if(x>0)
		y=-1;
		else
		y=1;
	}
	else
	y=0;
	
	printf("\n Y=%d",y);
	
	//using else if ladder
	
	if(x==0)
	y=0;
	else if(x<0)
	y=1;
	else
	y=-1;
	printf("\n Y=%d",y);
	
	//using turnary oparator
	
	(x==0)?y=0:((x<0)?y=1:y=-1);
	printf("\n Y=%d",y);
	
	// using switch case
	
	if(x==0)
	n=1;
	else if(x<0)
	n=2;
	else
	n=3;
	
	switch(n)
	{
	
	case 1:y=0;
	break;
	case 2:y=1;
	break;
	default:y=-1;
	}
	
	printf("\n Y=%d",y);		
	
	return 0;
}
