# ai-commit-message

Generuje commit message z `git diff` pomocí LLM (GPT-4o mini).

Praktický příklad promptování pro vývojáře — více v článku [Promptování pro vývojáře — kompletní průvodce](https://aidevelopers.cz/clanky/promptovani-pro-vyvojare-kompletni-pruvodce) na [aidevelopers.cz](https://aidevelopers.cz).

## Instalace

```bash
git clone https://github.com/aidevelopers-cz/ai-commit-message
cd ai-commit-message
pip install openai
export OPENAI_API_KEY=sk-...
```

## Použití

```bash
git add .
python commit.py
```

Výstup:
```
Generuji commit message...

Navržená commit message:

  feat(auth): add JWT token validation middleware
```

### Přepínače

```bash
# Automaticky commitne po schválení
python commit.py --commit

# Commit message v češtině
python commit.py --lang cs

# Jiný model
python commit.py --model gpt-4o
```

## Jak to funguje

1. Načte `git diff --staged` (staged změny)
2. Pošle diff + systémový prompt do OpenAI API
3. Vrátí commit message ve formátu [Conventional Commits](https://www.conventionalcommits.org/)

Systémový prompt je navržen podle technik z článku — konkrétní instrukce, požadovaný formát výstupu, omezení délky.

## Cena

Používá `gpt-4o-mini` — typický diff stojí zlomky centu.

## Licence

MIT
