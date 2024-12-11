import os
from pathlib import Path
import subprocess
import sys
import keyboard  # For real-time input handling

ANALYSES_FILEPATH = './analyses/'

def print_menu_options(data: list, current_input: str) -> None:
    print("\033c", end="")  # Clear the console
    print(f"Your Input: {current_input}")
    print("Possible Options:")
    for option in data:
        print(f"- {option}")

def filter_menu_options(data: list, exp: str) -> list:
    return [option for option in data if exp.lower() in option.lower()]

def real_time_input(options: list):
    "Used to filter while the user is typing"
    current_input = ""
    try:
        while True:
            event = keyboard.read_event(suppress=True)

            if event.event_type == "down":
                if event.name == "enter":
                    return current_input

                elif event.name == "backspace":
                    current_input = current_input[:-1]

                elif len(event.name) == 1:
                    current_input += event.name

                filtered_options = filter_menu_options(options, current_input)
                print_menu_options(filtered_options, current_input)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(0)

def get_file_names() -> list[str]:
    analyses_path = Path(ANALYSES_FILEPATH)
    return [f.as_posix() for f in analyses_path.iterdir() if f.is_file()]

def format_filename(filename: str) -> str:
    return filename.split("/")[-1].replace(".py", "").replace("_", " vs ")

def get_menu_options() -> list[str]:
    return [format_filename(filename) for filename in get_file_names()]


if __name__ == '__main__':
    options = get_menu_options()
    # options = ['alcohol_schooling.py', 'diabetes_stroke.py', 'egg_demoindex.py']
    print_menu_options(options, "")

    while True:
        print("Start typing to filter options (Press Enter to confirm):")
        user_input = real_time_input(options)

        if not user_input:
            print("Input cannot be empty. Please try again.")
            continue

        filtered_options = filter_menu_options(options, user_input)

        # Handle filtered options
        if len(filtered_options) == 1:
            selected_option = filtered_options[0]
            confirm = input(f"Run {selected_option}? (y/n): ").strip().lower()
            if confirm == 'y':
                try:
                    subprocess.run([sys.executable, 'analyses/' + selected_option])
                except FileNotFoundError:
                    print(f"Error: File {selected_option} not found.")
                break
            else:
                print("Cancelled. Restarting selection...")
                print_menu_options(options, "")

        elif len(filtered_options) > 1:
            print("Multiple options available. Please refine your input.")

        else:
            print("No matching options. Please try again.")