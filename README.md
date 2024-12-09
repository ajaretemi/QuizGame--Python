# Quiz Game 🎮

A simple multiple-choice quiz game built using Python and Pygame. Test your knowledge and see how high you can score before the timer runs out or you answer incorrectly!

## Table of Contents
- [Features](#features)
- [How to Play](#how-to-play)
- [Customizing Questions](#customizing-questions)

---

## Features
- 🎯 Timed questions with a customizable time limit.
- 🏆 Tracks scores based on question difficulty (Easy, Medium, Hard).
- ⏱️ Ends the game if the timer runs out or a wrong answer is selected.
- 📄 Stores high scores locally.

---

## How to Play
1. **Objective**: Answer as many questions as possible correctly before getting one wrong or running out of time.
2. **Scoring**:
   - Easy: +10 points
   - Medium: +20 points
   - Hard: +30 points
3. **Game Over**:
   - You select the wrong answer.
   - The timer reaches zero before answering.
4. **Controls**:
   - Click on the answer you believe is correct.

## Customizing Questions
The questions.json file defines your quiz questions. It should follow this format:

```
[
  {
    "question": "What is the capital of France?",
    "options": ["Paris", "Berlin", "Rome", "Madrid"],
    "answer": "Paris",
    "difficulty": "Easy"
  },
  {
    "question": "What is 2 + 2?",
    "options": ["3", "4", "5", "6"],
    "answer": "4",
    "difficulty": "Easy"
  }
]
```
