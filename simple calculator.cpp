#include <stdio.h>

int main()
{
	char Operator;
	float num1,num2,result = 0;
	
	printf("\n Please enter an operator(+,-,*,/) :");
	scanf("%c",&Operator);
	
	printf("\n Please enter your two numbers :");
	scanf("%f%f",&num1,&num2);
	switch(Operator)
	{
		case'+':
			result=num1 + num2;
			break;
		case'-':
			result=num1-num2;
			break;
		case'*':
			result=num1*num2;
			break;
		case'/':
			result=num1/num2;
			break;
		default:
			printf("\n INVALID OPERATOR");
			
	}
	
	printf("\n The result of %.2f%c%.2f = %.2f",num1,Operator,num2,result);
	
	return(0);
}
