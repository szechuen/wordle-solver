from guess import *


def check(solution, guess):
    hint = ["." for _ in range(5)]
    remaining = []

    for i in range(5):
        if guess[i] == solution[i]:
            hint[i] = "X"
        else:
            remaining.append(solution[i])

    for i in range(5):
        if guess[i] != solution[i] and guess[i] in remaining:
            hint[i] = "O"
            remaining.remove(guess[i])

    return "".join(hint)


if __name__ == "__main__":
    total_steps = 0
    max_steps = -1

    for solution in solutions:
        working_solutions = solutions.copy()
        working_guesses = guesses.copy()

        steps = 0

        while len(working_solutions) > 1:
            best_guess = guess(working_solutions, working_guesses)
            hint = check(solution, best_guess)

            working_solutions = filter(working_solutions, best_guess, hint)
            # working_guesses = hard(working_guesses, best_guess, hint)

            steps += 1

        if len(working_solutions) != 1 or working_solutions[0] != solution:
            raise Exception(f"Failed to arrive at solution for '{solution}'!")

        print((solution, steps))

        total_steps += steps
        if steps > max_steps:
            max_steps = steps

    print(f"Average steps: {total_steps / len(solutions)}")
    print(f"Maximum steps: {max_steps}")
