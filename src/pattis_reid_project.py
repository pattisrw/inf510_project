import sys
import os
import time
import ui

def get_command():
    """
        Raises SystemExit exceptions if the format of the command from the CLI is incorrect.
        Valid commands:
        python pattis_reid_hw5.py -source=local
        python pattis_reid_hw5.py -source=remote
        Also, -source=remote must be run BEFORE -source=local
        If no exceptions were raised, then returns either string "local" or string "remote"
        corresponding to the user input
    """
    commands = sys.argv
    if len(commands) != 2:
        raise SystemExit("Invalid Command: must be exactly 2 arguments provided to python")
    elif ".py" not in commands[0]:
        raise SystemExit("Invalid Command: First argument must have an extension of .py")
    elif commands[1]!="-source=remote" and commands[1] != "-source=local":
        raise SystemExit("Invalid Command: Second argument can only be -source=local or -source=remote")
    elif commands[1] == "-source=local":
        if not os.path.exists(os.path.join("..", "data", "data_full.pkl")) and not os.path.exists(os.path.join("..", "data", "data_test.pkl")):
            raise SystemExit("Must run -source=remote before -source=local")
    return commands[1].split("=")[1]



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    operation = get_command()
    if operation == "remote":
        ui.remote_introduction()
        version = ui.get_operation_ui()

        # begins timing program after user input
        start_time = time.time()
        countries_list, incomes, boxers = ui.retrieve_raw_data_ui(version)
        data = ui.format_and_store_ui(countries_list, incomes, boxers, version)
        ui.analyze_data_ui(data, version)

        print("---Total Execution Time: %s seconds ---\n\n" % (time.time() - start_time))

    else:
        ui.local_introduction()
        version = ui.get_operation_ui()

        start_time = time.time()
        try:
            data = ui.load_data_ui(version)
        except FileNotFoundError:
            print(f"data for version {version} not found")
            print("Ending Program\n")
        else:
            ui.analyze_data_ui(data,version)
        print("---Total Execution Time: %s seconds ---\n\n" % (time.time() - start_time))
