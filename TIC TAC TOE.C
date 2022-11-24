
// CHECK THIS OUT....
//I MADE THIS TIC-TAC-TOE GAME TODAY.....SO SIMPLEY USING C PROGRAMMING....LETS GO THROUGH THIS PROGRAM!!!



#include <stdio.h>
#include <conio.h>     //THESE FOUR HEDDER FILES I USED
#include <windows.h>
#include <stdlib.h>

char square[10]= {'o','1','2','3','4','5','6','7','8','9'};
int checkwin();
void drawboard();

int main()
{
	int player = 1, i, choice;
	char mark;
	do {
		drawboard();
		player = (player % 2) ? 1 : 2;
		printf("\n player %d, Enter your choice : ",player);
		scanf("%d", &choice);
		mark = (player == 1) ? 'X' : 'O';
		if(choice == 1 && square[1] == '1')
		    square[1] = mark;
		else if(choice == 2 && square[2] == '2')
		    square[2] = mark;
		else if(choice == 3 && square[3] == '3')
		    square[3] = mark;
		else if(choice == 4 && square[4] == '4')
		    square[4] = mark;
		else if(choice == 5 && square[5] == '5')      // THIS IS THE CHOICE AND MARK SYSTEM USING ELSE IF LADDER....THIS THING TAKE THE PLACE TO MARK
		    square[5] = mark;                          // FROM USER AS INPUT....AND PLACES X OR O ACCORDING TO THE CURRENT PLAYER AT THAT PLACE...
		else if(choice == 6 && square[6] == '6')
		    square[6] = mark;
		else if(choice == 7 && square[7] == '7')
		    square[7] = mark;
		else if(choice == 8 && square[8] == '8')
		    square[8] = mark;
		else if(choice == 9 && square[9] == '9')
		    square[9] = mark;
		else 
		    {
		    	printf("\n YOUR CHOICE IS INVALID...TRY ANOTHER CHOICE!");
		    	player--;
		    	getch();
			}
			i = checkwin();
			player++;
					    
		
	}while(i == -1);
	
	drawboard();
	if(i==1)
	{
		printf(" ==> player %d won",--player);     // THIS THING HERE CHECKS WHETHER THERE IS A WINNER OR THIS IS A DRAW....
	}                                               // IF THERE IS A WINNER  THEN DECLARE THAT NAME.......
	else 
	{
		printf("==> GAME DRAW!");
		
	}
		getch();
		return 0;
}
int checkwin()
{
	if(square[1] == square[2] && square[2] == square[3])
	    return 1;
	else if (square[4] == square[5] && square[5] == square[6])
	    return 1;	
	else if (square[7] == square[8] && square[8] == square[9])
	    return 1;
	else if (square[1] == square[4] && square[4] == square[7])      //THIS ELSE IF LADDER CHECKS THE WINNING CONDITION FOR A REGULAR TIC TAC TOR GAME....
	    return 1;
	else if (square[2] == square[5] && square[5] == square[8])
	    return 1;
	else if (square[3] == square[6] && square[6] == square[9])
	    return 1;
	else if (square[1] == square[5] && square[5] == square[9])
	    return 1;
	else if (square[3] == square[5] && square[5] == square[7])
	    return 1;
	else if( square[1] != '1' && square[2] != '2' && square[3] != '3' && square[4] != '4' && square[5] != '5' && square[6] != '6' && square[7] != '7' && square[8] != '8' && square[9] != '9')
		return 0;
	else
	    return -1;						 
}

void drawboard()
{
	system("cls");
	printf("\n\n\t\t\t\t\t TIC-TAC-TOE  \n\n");
	printf("\t\t\t\tplayer 1 (X) --- player 2 (O) \n\n\n");
	printf("\t\t\t\t     |     |     \n");
	printf("\t\t\t\t  %c  |  %c  |  %c  \n",square[1],square[2],square[3]);
	printf("\t\t\t\t_____|_____|_____\n");
	printf("\t\t\t\t     |     |     \n");
	printf("\t\t\t\t  %c  |  %c  |  %c  \n",square[4],square[5],square[6]);     // AND FINALLY ...THIS IS THE GAME BOARD WHERE WE CAN PLAY IT.....
	printf("\t\t\t\t_____|_____|_____\n");
	printf("\t\t\t\t     |     |     \n");
	printf("\t\t\t\t  %c  |  %c  |  %c  \n",square[7],square[8],square[9]);
	printf("\t\t\t\t     |     |     \n");
}

//OK....SO THATS IT......LETS TRY THIS GAME OUT!!!!




