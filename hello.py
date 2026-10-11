"""
Number Guessing Game
--------------------
Computer ek random number sochta hai, aapko use limited attempts mein guess karna hai.

Features:
- 3 difficulty levels (Easy / Medium / Hard)
- Higher / Lower hints + "garam / thanda" hint
- Best score (kam se kam attempts) JSON file mein save hota hai
- Play again option
"""

import json
import random
from pathlib import Path

SCORE_FILE = Path(__file__).with_name("highscores.json")

# level: (naam, max number, max attempts)
LEVELS = {
    "1": ("Easy", 50, 10),
    "2": ("Medium", 100, 7),
    "3": ("Hard", 500, 9),
}


def load_scores() -> dict:
    """Saved best scores load karo."""
    try:
        return json.loads(SCORE_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_scores(scores: dict) -> None:
    SCORE_FILE.write_text(json.dumps(scores, indent=2), encoding="utf-8")


def choose_level():
    print("\nDifficulty chuno:")
    for key, (name, high, tries) in LEVELS.items():
        print(f"  {key}. {name:<7} (1 se {high}, {tries} attempts)")
    while True:
        choice = input("Aapka choice (1/2/3): ").strip()
        if choice in LEVELS:
            return LEVELS[choice]
        print("Galat choice, 1, 2 ya 3 daalo.")


def get_guess(low: int, high: int) -> int:
    """Valid integer guess lo."""
    while True:
        raw = input(f"Guess ({low}-{high}): ").strip()
        if not raw.lstrip("-").isdigit():
            print("Sirf number daalo.")
            continue
        guess = int(raw)
        if not low <= guess <= high:
            print(f"Number {low} aur {high} ke beech hona chahiye.")
            continue
        return guess


def temperature_hint(diff: int, high: int) -> str:
    """Kitna paas ho, uska hint."""
    ratio = diff / high
    if ratio <= 0.03:
        return "Bahut garam! Bilkul paas ho."
    if ratio <= 0.10:
        return "Garam, kaafi paas ho."
    if ratio <= 0.25:
        return "Thoda thanda."
    return "Bahut thanda, door ho."


def play_round(name: str, high: int, max_attempts: int, scores: dict) -> None:
    secret = random.randint(1, high)
    low, up = 1, high
    print(f"\n[{name}] Maine 1 se {high} ke beech ek number socha hai. "
          f"Aapke paas {max_attempts} attempts hain.")

    for attempt in range(1, max_attempts + 1):
        print(f"\nAttempt {attempt}/{max_attempts}")
        guess = get_guess(low, up)

        if guess == secret:
            print(f"Sahi jawab! Number {secret} tha. "
                  f"Aapne {attempt} attempt(s) mein guess kiya.")
            best = scores.get(name)
            if best is None or attempt < best:
                scores[name] = attempt
                save_scores(scores)
                print("Naya best score!")
            return

        if guess < secret:
            print("Bahut chhota. Upar jao.")
            low = max(low, guess + 1)
        else:
            print("Bahut bada. Neeche jao.")
            up = min(up, guess - 1)
        print(temperature_hint(abs(guess - secret), high))

    print(f"\nAttempts khatam. Sahi number {secret} tha.")


def show_scores(scores: dict) -> None:
    print("\n=== Best Scores (kam attempts = better) ===")
    if not scores:
        print("Abhi koi score nahi hai.")
        return
    for name, best in scores.items():
        print(f"  {name:<7}: {best} attempt(s)")


def main() -> None:
    print("=" * 40)
    print("   NUMBER GUESSING GAME")
    print("=" * 40)
    scores = load_scores()
    show_scores(scores)

    while True:
        name, high, max_attempts = choose_level()
        play_round(name, high, max_attempts, scores)
        again = input("\nDobara khelna hai? (y/n): ").strip().lower()
        if again != "y":
            show_scores(scores)
            print("\nKhelne ke liye shukriya! Bye.")
            break


if __name__ == "__main__":
    main()
