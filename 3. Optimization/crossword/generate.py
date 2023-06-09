import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            for word in self.domains[variable].copy():
                if len(word) != variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revisionMade = False

        if self.crossword.overlaps[x, y] is not None: # if an overlap exists
            i, j = self.crossword.overlaps[x, y]
            for word in self.domains[x].copy():
                valid_word = False
                for other_word in self.domains[y]:
                    if word[i] == other_word[j] and word != other_word: # if word in x is valid with a word in y
                        valid_word = True
                        break
                if not valid_word:
                    self.domains[x].remove(word) # if word in x is not valid with any word in y
                    revisionMade = True

        return revisionMade
    
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None: # create initial queue of all arcs
            arcs = [ ]
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    # if the variables are different and overlap
                    if x != y and self.crossword.overlaps[x, y] is not None:
                        arcs.append((x, y))
                    
        while arcs:
            x, y = arcs.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        arcs.append((neighbor, x))
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.domains): # lengths will be same if assignment is complete (as a variable is in assignment only if it has a valid word attached to it)
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        word_list = [ ]
        for var in assignment:
            if var.length != len(assignment[var]): # checks if all values are the correct length
                return False
            if assignment[var] in word_list: # checks if all values are distinct
                return False
            word_list.append(assignment[var])
            
        for x in assignment:
            for y in assignment:
                if x != y and self.crossword.overlaps[x, y] is not None:
                    i, j = self.crossword.overlaps[x, y]
                    if (assignment[x][i] != assignment[y][j]):
                        return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors = [neighbor for neighbor in self.crossword.neighbors(var) if neighbor not in assignment]

        ordered_domain_values = [ ]
        for word in self.domains[var]: # loops through every word in var's domain
            choices_eliminated = 0
            for neighbor in neighbors: # for each word, check each neighbor
                i, j = self.crossword.overlaps[var, neighbor]
                for word2 in self.domains[neighbor]:
                    if word[i] != word2[j]:
                        choices_eliminated += 1 # add 1 if the words aren't compatible
            ordered_domain_values.append((word, choices_eliminated))

        sorted_list = sorted(ordered_domain_values, key=lambda x: x[1]) # sort list based on choices_eliminated
        ordered_domain_values = [x[0] for x in sorted_list] # return only the list of words

        return ordered_domain_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        choice = None
        for var in self.domains: # loops through all variables
            if var not in assignment: # if the variable is unassigned
                if choice is None:
                    choice = var
                else:
                    if len(self.domains[var]) < len(self.domains[choice]): # if the variable has fewer values in its domain
                        choice = var
                    elif len(self.domains[var]) == len(self.domains[choice]) and len(self.crossword.neighbors(var)) > len(self.crossword.neighbors(choice)): # if the variable has the same number of values in its domain, but a higher degree
                        choice = var

        return choice

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        words = self.order_domain_values(var, assignment)

        arcs = [(var, neighbor) for neighbor in self.crossword.neighbors(var)] # for inference

        for word in words:
            assignment[var] = word
            if self.consistent(assignment) and self.ac3(arcs=arcs): 
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
