#include <iostream>
#include<cstdlib>
#include<ctime>
using namespace std;

int main()
{

	int num,guess,tries=0;
	srand(time(0));   //RANDOM NUMBER GENARATOR
	num=rand()% 100+1;  //limiting numbers from 1 to 100
	cout<<"\t\t\t\t\t GUESS THE NUMBER!!!\t\t\t\n\n";
	
	do
	{
		cout<<"\nEnter your guess between 1 to 100 :";
		cin>> guess;
		tries++;
		
		if(guess>num)
		cout<<"\nTOO HIGH!...Guess a little lesser";
		else if(guess<num)
		cout<<"\nTOO LOW!...Guess a little higher";
		
		else
		{
		cout<<"\nCORRECT!!!...";
		cout<<"YOU GUESSED IT IN  "<<tries<<" TRIES";
	    }
	}
	while(guess!=num);
	
	return 0;
	
}

