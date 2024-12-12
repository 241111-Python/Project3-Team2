import os
from pathlib import Path
import subprocess
import sys
import keyboard  # For real-time input handling
import argparse


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

def get_menu_options_dict() -> dict:
    return {format_filename(filename): filename for filename in get_file_names()}

def get_menu_options() -> list[str]:
    return get_menu_options_dict().keys()


if __name__ == '__main__':

    # CLI Interface
    parser = argparse.ArgumentParser('Project 3: Team 2', 
                                     description="This program allows users to create graphs and correlation maps between several different datasets.")
    
    parser.add_argument("--airquality_covid", "-1",action='store_true',help=f"Runs analysis comparing air quality to covid rates\n")
    
    parser.add_argument("--alcohol_schooling", "-2",action='store_true',help=f"Runs analysis comparing alcohol use to schooling\n")
    
    parser.add_argument("--diabetes_stroke", "-3",action='store_true',help=f"Runs analysis comparing diabetic symptoms to stroke symptoms\n")
    
    parser.add_argument("--egg_demoindex", "-4",action='store_true',help=f"Runs analysis comparing the price of eggs to the democracy index\n")
    
    parser.add_argument("--flhealth_banks", "-5",action='store_true',help=f"Runs analysis comparing Florida health rankings to the number of failed banks\n")
    
    parser.add_argument("--maternal_diabetes_alcohol_cardio", "-6", action='store_true',help=f"Runs analysis comparing maternal disorders, diabetes, alcohol use disorders, and cardiovascular diseases\n")
    
    parser.add_argument("--meteorites_causesofdeath", "-7", action='store_true', help=f"Runs analysis comparing the number of meteorites landed in countries to the causes of death\n")
    
    parser.add_argument("--pfizer_demindex", "-8", action='store_true', help=f"Runs analysis comparing pfizer stock price to the democracy index\n")
    
    parser.add_argument("--pfizer_precipitation", "-9", action='store_true', help=f"Runs analysis comparing pfizer stock price to precipitation\n")
    
    parser.add_argument("--powerball_firearm", "-10", action='store_true', help=f"Runs analysis comparing the number of even or odd numbers in powerballs to firearm sales\n")
    
    parser.add_argument("--tb_covid", "-11", action='store_true', help=f"Runs analysis comparing tuberculosis to covid\n")

    
    args = parser.parse_args()

    arg_dict = {airquality_covid:"airquality_covid.py", alcohol_schooling:"alcohol_schooling.py",
                diabetes_stroke:"diabetes_stroke.py", egg_demoindex:"egg_demoindex.py",
                flhealth_banks:"fl-health-rank_failed-banks.py", maternal_diabetes_alcohol_cardio:"maternal_diabetes_alcohol_cardio.py",
                meteorites_causesofdeath:"meteorites_causes-of-death.py", pfizer_demindex:"pfizer_demindex.py",
                pfizer_precipitation:"pfizer_precipitation.py",powerball_firearm:"powerball_firearm.py",
                tb_covid:"tb_covid_analysis.py"}

    for arg in arg_dict:
        if args.arg:
            exec(open(os.path.join('analyses', arg_dict[arg])).read())
            quit()
# End of CLI Interface


    options_dict = get_menu_options_dict()
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
                    # analysespath = os.path.join(options_dict[selected_option])
                    subprocess.run([sys.executable, options_dict[selected_option]])
                    # subprocess.run([sys.executable, 'analyses/' + options_dict[selected_option]])
                except FileNotFoundError:
                    print(f"Error: File {options_dict[selected_option]} not found.")
                break
            else:
                print("Cancelled. Restarting selection...")
                print_menu_options(options, "")

        elif len(filtered_options) > 1:
            print("Multiple options available. Please refine your input.")

        else:
            print("No matching options. Please try again.")