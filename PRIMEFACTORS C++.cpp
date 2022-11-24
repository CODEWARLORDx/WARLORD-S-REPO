#include <stdio.h>
void main()
{
	int n,k,c,i;
	printf("\n Enter tyour number ;");
	scanf("%d", &n);
	for(k=1;k<=n;k++)
	{
		if(n%k==0)
		{
			for(i=1,c=0;i<=k;i++)
			{
				if(c%i==0)
				c=c+1;
			}
			if(c==2)
			printf("\n Prime factors : %d", k);
			
		}
	}
}
return 0;
