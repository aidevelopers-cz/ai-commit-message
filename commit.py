#!/usr/bin/env python3
"""
ai-commit-message — Generuje commit message z git diff pomocí LLM.
https://aidevelopers.cz/clanky/promptovani-pro-vyvojare-kompletni-pruvodce
"""

import argparse
import os
import subprocess
import sys

try:
    from openai import OpenAI
except ImportError:
    print("Chybí openai knihovna. Nainstaluj ji: pip install openai")
    sys.exit(1)


SYSTEM_PROMPT = """Jsi expert na git a píšeš commit messages.
Na základě git diff vygeneruj stručnou a výstižnou commit message.

Pravidla:
- Použij Conventional Commits formát: type(scope): popis
- Typy: feat, fix, docs, style, refactor, test, chore
- První řádek max 72 znaků
- Piš v angličtině
- Buď konkrétní — vysvětli CO se změnilo, ne JAK

Vrať pouze commit message, nic jiného."""


def get_diff() -> str:
    """Načte staged změny z gitu."""
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Chyba: nejsi v git repozitáři nebo git není nainstalován.")
        sys.exit(1)

    diff = result.stdout.strip()
    if not diff:
        print("Žádné staged změny. Použij 'git add' před spuštěním.")
        sys.exit(0)

    return diff


def generate_commit_message(diff: str, model: str = "gpt-4o-mini", lang: str = "en") -> str:
    """Vygeneruje commit message pomocí OpenAI API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Chybí OPENAI_API_KEY v prostředí.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    system = SYSTEM_PROMPT
    if lang == "cs":
        system = system.replace("Piš v angličtině", "Piš v češtině")

    # Zkrátí diff pokud je příliš velký (max ~8000 znaků)
    if len(diff) > 8000:
        diff = diff[:8000] + "\n... (diff zkrácen)"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Git diff:\n\n{diff}"},
        ],
        max_tokens=200,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Generuje commit message z git diff pomocí LLM."
    )
    parser.add_argument(
        "--model", default="gpt-4o-mini",
        help="OpenAI model (default: gpt-4o-mini)"
    )
    parser.add_argument(
        "--lang", default="en", choices=["en", "cs"],
        help="Jazyk commit message (default: en)"
    )
    parser.add_argument(
        "--commit", action="store_true",
        help="Automaticky commitne s vygenerovanou zprávou"
    )
    args = parser.parse_args()

    diff = get_diff()
    print("Generuji commit message...\n")

    message = generate_commit_message(diff, model=args.model, lang=args.lang)
    print(f"Navržená commit message:\n\n  {message}\n")

    if args.commit:
        confirm = input("Commitnout? [y/N] ")
        if confirm.lower() == "y":
            subprocess.run(["git", "commit", "-m", message])
            print("Commitnuto.")
    else:
        print("Tip: Spusť s --commit pro automatický commit.")


if __name__ == "__main__":
    main()
