import csv
from datetime import datetime

options_delimiter = "/"
empty_answer = "-"
followup_option = "f"
name_value_delimiter = "#"


def _get_questions(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        questions = [
            {name.strip(): value.strip() for (name, value) in row.items()}
            for row in reader
        ]
    return questions


def _answer_is_empty(answer):
    return len(answer) == 0 or answer == empty_answer


def _add_followup(answer, followup):
    return f"{answer}[{followup}]"


def _get_answer(prompt):
    return input(f"{prompt}\n")


def _form_options_string(question_obj):
    options = []
    for option in ["y", "n"]:
        if option in question_obj["options"]:
            options.append(option.upper())
    if "a" in question_obj["options"]:
        options.append(empty_answer)
    return options_delimiter.join(options)


def _write_answers(answers, answers_file):
    date_string = f"date{name_value_delimiter}{datetime.now().strftime('%m/%d/%Y')}"
    fields = [date_string] + [
        f"{name}{name_value_delimiter}{answer}" for (name, answer) in answers
    ]
    with open(answers_file, "a") as f:
        f.write("\t".join(fields) + "\n")


def main(questions_file, answers_file):
    print("Let's do a quick checkin 😎\n")

    questions = _get_questions(questions_file)
    answers = []
    for q in questions:
        options_string = _form_options_string(q)
        answer = _get_answer(f"{q['prompt']} ({options_string})")

        if len(answer) == 0:
            answer = empty_answer

        if not _answer_is_empty(answer) and followup_option in q["options"]:
            followup_prompt = "Any details?" if not q["followup"] else q["followup"]
            answer_followup = _get_answer(followup_prompt)
            if not _answer_is_empty(answer_followup):
                answer = _add_followup(answer, answer_followup)

        answers.append((q["name"], answer))
        print()

    print("Thank you 🌻")

    _write_answers(answers, answers_file)


if __name__ == "__main__":
    main(questions_file="questions_daily.csv", answers_file="answers_daily.csv")
