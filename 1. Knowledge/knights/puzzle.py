from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    #Information about the structure of the problem
    Or(AKnight, AKnave), #A can be a Knight or a Knave
    Not(And(AKnight, AKnave)), #A cannot be both a Knight and a Knave

    #Information about what the character said
    Implication(And(AKnight, AKnave), AKnight), #If what A said is true, then A is a Knight
    Implication(Not(And(AKnight, AKnave)), AKnave) #If what A said is not true, then A is a Knave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    #Information about the structure of the problem
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    #Information about what the characters said
    Implication(And(AKnave, BKnave), AKnight), #If A and B are both Knaves, then A is a Knight
    Implication(Not(And(AKnave, BKnave)), AKnave) #If A and B are not both Knaves, then A is a Knave (and since the original statement must be false, B cannot also be a Knave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    #Information about the structure of the problem
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    #Information about what the characters said
    Implication(Or(And(AKnight, BKnight), And(AKnave, BKnave)), AKnight), #If what A said is true, A is a Knight
    Implication(Not(Or(And(AKnight, BKnight), And(AKnave, BKnave))), AKnave), #If what A said is not true, A is a Knave
    Implication(Or(And(AKnight, BKnave), And(AKnave, BKnight)), BKnight), #If what B said is true, then B is a Knight
    Implication(Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))), BKnave) #If what B said is not true, then B is a Knave
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    #Information about the structure of the problem
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    #Information about what the characters said
    Or(Implication(AKnight, AKnight), Implication(AKnave, AKnight)), #A says either "I am a knight" or "I am a knave", but you don't know which
    Implication(BKnight, Implication(AKnave, AKnight)), #B says “A said ‘I am a knave.’”
    Biconditional(CKnave, BKnight), #B then says “C is a knave.”
    Biconditional(AKnight, CKnight), #C says “A is a knight.”
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
