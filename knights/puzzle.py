from logic import *

# if knight states a sentence, then that sentence is true. Conversely, a knave will always lie


AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # GAME KNOWLEDGE
    # you can be either knight or knave
    Or(AKnight, AKnave), # Tem que ter pq se colocar como ambos falso, retornaria true sem isso
    # you cant be both
    Not(And(AKnight, AKnave)),

    # Both, knight and knave: 
    # Se A for Knight -> a fala é verdadeira
    Implication(AKnight, And(AKnight, AKnave)),

    # Se A for Knave -> a fala é falsa
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # GAME KNOWLEDGE
    # you can be either knight or knave, but not both for both A and B
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # Se é A knight, fala a verdade
    Implication(AKnight, And(AKnave, BKnave)),

    # Se é A knave, fala a mentira
    Implication(AKnave, Not(And(AKnave, BKnave))),
    # Not (A and B) -->  ¬A or ¬B, Como AKnave = True, a parte ¬AKnave é falsa, então ¬B tem que ser true, logo, se não é knave é knight
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Game rules -- has to be knight or knave but not both
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # If A is telling the truth, they re either both night, or both knave
    Implication(AKnight, Or(And(AKnight,BKnight), And(AKnave, BKnave)) ),

    # If A is lying, neither both are the same
    Implication(AKnave, Not(Or(And(AKnight,BKnight), And(AKnave, BKnave))) ), 

    # If B is telling the truth, they re either Aknight and Bknave or Aknave and Bknight
    Implication(BKnight, Or(And(AKnight, BKnave), And(BKnight, AKnave))),

    # If B is lying, so they re not different kinds
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(BKnight, AKnave))) ),
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
# Game rules -- has to be knight or knave but not both
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # A can only be a knight
    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Or(Biconditional(AKnight, AKnight), Biconditional(AKnight, AKnave)),

    # We can conclude, B is a Knave
    # B says "A said 'I am a knave'."
    Biconditional(BKnight, Biconditional(AKnight, AKnave)), # Second one is false, so B isnt knight

    # B says "C is a knave."
    Biconditional(BKnight, CKnave),

    # Since A has to be a knight, C must be also
    # C says "A is a knight."
    Biconditional(CKnight, AKnight)
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
