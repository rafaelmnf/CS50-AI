import itertools
import random

# Understanding the problem:
# A neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine
# One way we could represent an AI’s knowledge about a Minesweeper game is by making each cell a propositional variable that is true if the cell contains a mine, and false otherwise
# {A, B, C, D, E, F, G, H} = 1
# Every logical sentence in this representation has two parts: a set of cells on the board that are involved in the sentence, and a number count, representing the count of how many of those cells are mines. The above logical sentence says that out of cells A, B, C, D, E, F, G, and H, exactly 1 of them is a mine.
# Any time we have two sentences set1 = count1 and set2 = count2 where set1 is a subset of set2, then we can construct the new sentence set2 - set1 = count2 - count --> {A, B, C, D, E} = 2  & {A, B, C} = 1 --> {D, E} = 1

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


# For each cell in game we'd have a sentence for choose another cell
class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    Ex: {A,B,C,F} = 2
    """
    
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    # Dois objetos serão considerados iguais (True) se ambos tiverem os mesmos valores para os atributos cells e count
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    # When implementing known_mines and known_safes in the Sentence class, consider: under what circumstances do you know for sure that a sentence’s cells are safe? Under what circumstances do you know for sure that a sentence’s cells are mines?
    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # Is mine when we know that if the number of cells is equals to number of counted mines
        if len(self.cells) == self.count and self.count > 0 :
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # Is NOT mine when we know that count is 0

        if self.count == 0:
            return set(self.cells)
        return set()
        

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        #  First check to see if cell is one of the cells included in the sentence.
        # If cell is in the sentence, the function should update the sentence so that cell is no longer in the sentence, but still represents a logically correct sentence given that cell is known to be a mine.
        # If cell is not in the sentence, then no action is necessary
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # The mark_safe function should first check to see if cell is one of the cells included in the sentence.
        # If cell is in the sentence, the function should update the sentence so that cell is no longer in the sentence, but still represents a logically correct sentence given that cell is known to be safe.
        # If cell is not in the sentence, then no action is necessary.

        # We just have to remove the cell, since 
        if cell in self.cells:
            self.cells.remove(cell)
        


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        # List of a set [{(0,1),(2,0),C,D}, {C,D,P,I,J}, {B,A,C,D,E}]
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    # cell == move (i,j), count == mines nearby
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Getting all neighbors of that cell
        i,j = cell
        neighbors = [(i-1,j-1), (i,j-1), (i+1,j-1),(i-1,j), (i+1,j), (i-1,j+1), (i,j+1), (i+1,j+1)]
        sentence = set()
        # Validating
        for neighbor in neighbors:
            i,j = neighbor
            # If is in board
            if self.height > i >= 0 and self.width > j >= 0:
                if (i,j) in self.mines:
                    count -+ 1
                elif neighbor not in self.safes:
                    sentence.add(neighbor)


        self.knowledge.append(Sentence(sentence, count))

        # verifies if in the knowledge base exists a set that is a subset of it, if so, subtract thoose
        # verifies using set.issubset, extract the new array set.difference, subtract count and creates new sentece from it

            
    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = []
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    possible_moves.append(cell)

        if possible_moves:
            return random.choice(possible_moves)
        return None
