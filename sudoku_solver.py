'''This program takes an unsolved sudoku as input and returns its solution.'''

from typing import Tuple, List
import time

def input_sudoku() -> List[List[int]]:

        """Function to take input a sudoku from stdin and return
        it as a list of lists.
        Each row of sudoku is one line."""
        
        sudoku= list()
        for _ in range(9):
                row = list(map(int, input().rstrip(" ").split(" ")))
                sudoku.append(row)
        return sudoku



def print_sudoku(sudoku:List[List[int]]) -> None:

        """Helper function to print sudoku to stdout.
        Each row of sudoku in one line."""

        for i in range(9):
                for j in range(9):
                        print(sudoku[i][j], end = " ")
                print()

def get_block_num(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:

        """This function takes a parameter position and returns
        the block number of the block which contains the position."""

        r,c=pos
        block_num= ((r-1)//3)*3+(c+2)//3
        return block_num


def get_position_inside_block(sudoku:List[List[int]], pos:Tuple[int, int]) -> int:

        """This function takes parameter position and returns
        the index of the position(1-9) inside the corresponding block."""

        r,c=pos
        x=(r-1)%3
        y=(c-1)%3
        position_inside_block= x*3+y+1
        return position_inside_block


def get_block(sudoku:List[List[int]], x: int) -> List[int]:

        """This function takes an integer argument x and then
        returns the x^th block of the Sudoku. Note that block indexing is
        from 1 to 9 and not 0 to 8."""

        block=[]
        x-=1
        a=(x//3)*3
        b=(x%3)*3
        for i in range(a,a+3):
                for j in range(b,b+3):
                        block.append(sudoku[i][j])
        return block
        

def get_row(sudoku:List[List[int]], i: int)-> List[int]:

        """This function takes an integer argument i and then returns the ith row."""

        row=sudoku[i-1]
        return row


def get_column(sudoku:List[List[int]], i: int)-> List[int]:

        """This function takes an integer argument i and then returns the ith column."""

        column=[]
        for x in range(9):
                column+=[sudoku[x][i-1]]
        return column


def find_first_unassigned_position(sudoku : List[List[int]]) -> Tuple[int, int]:

        """This function returns the first empty position in the Sudoku. 
        If there are more than 1 position which is empty then position with lesser
        row number should be returned. If two empty positions have same row number then the position
        with less column number is to be returned. If the sudoku is completely filled then return `(-1, -1)`."""

        for i in range(9):
                for j in range(9):
                        if sudoku[i][j]==0:
                                return (i+1,j+1)
        return (-1,-1)


def valid_list(lst: List[int])-> bool:

        """This function takes a lists as an input and returns true if the given list is valid. 
        The list will be a single block , single row or single column only. 
        A valid list is defined as a list in which all non empty elements doesn't have a repeating element."""

        x=lst.copy()
        x.sort()
        for i in range(len(x)-1):
                if x[i]==x[i+1] and x[i]!=0:
                        return False
        return True


def valid_sudoku(sudoku:List[List[int]])-> bool:

        """This function returns True if the whole Sudoku is valid."""
        check=True
        for i in range(1,10):
                if valid_list(get_block(sudoku,i))==False:
                        check=False
                if valid_list(get_row(sudoku,i))==False:
                        check=False
                if valid_list(get_column(sudoku,i))==False:
                        check=False
        return check


def get_candidates(sudoku:List[List[int]], pos:Tuple[int, int]) -> List[int]:

        """This function takes position as argument and returns a list of all the possible values that 
        can be assigned at that position so that the sudoku remains valid at that instant."""
        
        r,c=pos
        row=get_row(sudoku,r)
        column=get_column(sudoku,c)
        x=get_block_num(sudoku,pos)
        block=get_block(sudoku,x)
        candidates=[]
        for i in range(1,10):
                if i not in row and i not in column and i not in block:
                        candidates+=[i]
        return candidates


def make_move(sudoku:List[List[int]], pos:Tuple[int, int], num:int) -> List[List[int]]:

        """This function fills `num` at position `pos` in the sudoku and then returns
        the modified sudoku."""

        r,c=pos
        sudoku[r-1][c-1]=num
        return sudoku


def undo_move(sudoku:List[List[int]], pos:Tuple[int, int]):

        """This function fills `0` at position `pos` in the sudoku and then returns
        the modified sudoku. In other words, it undoes any move that you 
        did on position `pos` in the sudoku."""

        r,c=pos
        sudoku[r-1][c-1]=0
        return sudoku


def sudoku_solver(sudoku: List[List[int]]) -> Tuple[bool, List[List[int]]]:

        """ This is the main Sudoku solver. This function solves the given incomplete Sudoku and returns 
        true as well as the solved sudoku if the Sudoku can be solved i.e. after filling all the empty positions the Sudoku remains valid.
        It return them in a tuple i.e. `(True, solved_sudoku)`.
        However, if the sudoku cannot be solved, it returns False and the same sudoku that given to solve i.e. `(False, original_sudoku)`"""
        if find_first_unassigned_position(sudoku)==(-1,-1):
                return True,sudoku
        elif find_first_unassigned_position(sudoku)!=(-1,-1):
                position=find_first_unassigned_position(sudoku)
                candidates=get_candidates(sudoku,position)
                if len(candidates)==0:
                        return False,sudoku
                for x in candidates:
                        make_move(sudoku, position, x)
                        sudoku_solver(sudoku)
                        if find_first_unassigned_position(sudoku)==(-1,-1):
                                return True,sudoku
                        else:
                                undo_move(sudoku,position)
        return False, sudoku

if __name__ == "__main__":

        sudoku = input_sudoku()
        st=time.time()
        possible, sudoku = sudoku_solver(sudoku)
        et=time.time()
        print(et-st,'seconds')
        if possible:
                print("Found a valid solution for the given sudoku :)")
                print_sudoku(sudoku)
        else:
                print("The given sudoku cannot be solved :(")
                print_sudoku(sudoku)
