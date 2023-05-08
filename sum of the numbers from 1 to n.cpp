#include <stdio.h>
int main()
{
	int fn(int,int);
	int n,x=1,p;
	printf("\n How many numbers ?");
	scanf("%d",&n);
	
	
	p=fn(n,x);
	
	
	printf("\n Sum : %d",p);
		return(0);
}
int fn(int k,int n)
{
	static int s=0;
	
	
	
	if(k>=1)
	{
		printf("%d ",n);
		s=s+n;
		fn(k-1,n+1);
	}
	return(s);
}
