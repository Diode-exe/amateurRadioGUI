# Amateur Radio License Test Practice GUI

## Overview

- **Purpose:** Simple GUI for practicing the Canadian Amateur Radio basic license test faster than the official online practice test.
- **Features:** Randomized questions, answer tracking, and small calculators for common test topics.

## Requirements

- **Python:** `Python 3.10+` (any recent 3.x should work).
- **GUI toolkit:** `tkinter` (bundled on Windows; on Linux install the system `python3-tk` package).

## Setup

- **Questions file:** Follow the instructions in [where_questions.md](where_questions.md) to obtain and place the required `questions.txt` into `src/amateurRadioGUI/data`.
- **Data folder:** The app expects `src/amateurRadioGUI/data/questions.txt`. When run it will write `random_questions.txt` and save answers under `src/amateurRadioGUI/data/user_answers/`.

## Run

- From the project root run:

    ```powershell
    python src/amateurRadioGUI/main.py
    ```

## Usage

- **Select an answer:** click a radio button or press keys `1`–`4` to choose an option.
- **Check / Next:** press `Enter` to either check the current selection or advance to the next question (the app uses the active button state; make sure the app window has focus).
- **Open calculators:** click the `Open Calculators` button to access the small calculators panel.

## Saved output

- **Randomized questions:** `src/amateurRadioGUI/data/random_questions.txt` is created each run.
- **Answers:** saved in files named like `user_answers_<timestamp>.txt` inside `src/amateurRadioGUI/data/user_answers/` (example: [src/amateurRadioGUI/data/user_answers/user_answers_20260609_152050.txt](src/amateurRadioGUI/data/user_answers/user_answers_20260609_152050.txt)).

## Troubleshooting

- **Missing questions file:** see [where_questions.md](where_questions.md) for download and placement steps.

## Key files

- `src/amateurRadioGUI/main.py` — main application
- `where_questions.md` — instructions for obtaining `questions.txt`

## French support

Is partial

The questions will be in french, but the UI will still be in english. To enable this, set `"french_mode": true` in `src/amateurRadioGUI/config/config.json`.
