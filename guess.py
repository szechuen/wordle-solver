import json

with open("wordlists/solutions.json", "r") as f:
    solutions = json.load(f)
with open("wordlists/guesses.json", "r") as f:
    guesses = json.load(f) + solutions


def guess(solutions, guesses):
    count = [[0 for _ in range(26)] for _ in range(6)]

    for solution in solutions:
        contains = [False for _ in range(26)]

        for i in range(5):
            count[i][ord(solution[i]) - 97] += 1
            contains[ord(solution[i]) - 97] = True

        for i in range(26):
            if contains[i]:
                count[5][i] += 1

    best = (None, None)

    for guess in guesses:
        score = 0

        for i in range(5):
            exact = count[i][ord(guess[i]) - 97]
            contains = count[5][ord(guess[i]) - 97] - count[i][ord(guess[i]) - 97]
            score += max(exact, contains, len(solutions) - exact - contains)

        if best[0] is None or score < best[0]:
            best = (score, guess)

    return best[1]


def filter(solutions, guess, hint):
    valid = []

    for solution in solutions:
        possible = True
        remaining = []

        for i in range(5):
            if hint[i] == "X":
                if guess[i] != solution[i]:
                    possible = False
                    break
            else:
                remaining.append(solution[i])

        if not possible:
            continue

        for i in range(5):
            if hint[i] == "O":
                if guess[i] == solution[i]:
                    possible = False
                    break
                if guess[i] not in remaining:
                    possible = False
                    break
                remaining.remove(guess[i])
            elif hint[i] == ".":
                if guess[i] == solution[i] or guess[i] in remaining:
                    possible = False
                    break

        if possible:
            valid.append(solution)

    return valid


def hard(guesses, prev_guess, hint):
    valid = []

    for guess in guesses:
        possible = True

        for i in range(5):
            if hint[i] == "X":
                if prev_guess[i] != guess[i]:
                    possible = False
                    break

        if possible:
            valid.append(guess)

    return valid


if __name__ == "__main__":
    working_solutions = solutions.copy()
    working_guesses = guesses.copy()

    while len(working_solutions) > 1:
        best_guess = guess(working_solutions, working_guesses)

        print(f"Best guess is '{best_guess}'")
        hint = input("Hint> ")

        working_solutions = filter(working_solutions, best_guess, hint)
        # working_guesses = hard(working_guesses, best_guess, hint)

    if len(working_solutions) != 1:
        raise Exception(f"Failed to arrive at solution!")

    print(f"Solution is '{working_solutions[0]}'!")
