from typing import List

import datetime


def mark_new_file():
    with open("access.log", 'w') as file:
        file.write(
            """+--------------------------+----------------------+------------------------------+----------------------------------------------------------------------------------------------------+------------------------------+--------------------+\n"""
            """|           Time           |        Ex. IP        |           Hostname           |                                                 PWD                                                |             User             |    Package name    |\n"""
            """+--------------------------+----------------------+------------------------------+----------------------------------------------------------------------------------------------------+------------------------------+--------------------+\n"""
        )


def split_string(input_string: str, max_length: int) -> List[str]:
    # Can split line up to 5 formated lines.
    # You should check data len before. It's got limit - 5
    substrings = []
    for i in range(0, len(input_string), max_length):
        substrings.append(input_string[i:i + max_length])
    return substrings


def format_data(external_ip: str, hostname: str, working_directory: str, user: str, package_name: str) -> List[List[str]]:
    formated_data = [[''] * 6 for _ in range(5)]

    arrival_time = str(datetime.datetime.now().strftime("%d/%b/%Y %I:%M:%S")).center(26)
    formated_data[0][0] = arrival_time

    formated_data[0][1] = external_ip.center(22)

    if len(hostname) <= 30:
        formated_data[0][2] = hostname.center(30)
    elif len(hostname) > 30:
        hostname_formated = split_string(hostname, 30)
        for i in range(len(hostname_formated)):
            formated_data[i][2] += hostname_formated[i]

    if len(working_directory) <= 100:
        formated_data[0][3] = working_directory.center(100)
    elif len(working_directory) > 100:
        working_directory_formated = split_string(working_directory, 100)
        for i in range(len(working_directory_formated)):
            formated_data[i][3] += working_directory_formated[i]

    if len(user) <= 30:
        formated_data[0][4] = user.center(30)
    elif len(user) > 30:
        user_formated = split_string(user, 30)
        for i in range(len(user_formated)):
            formated_data[i][4] += user_formated[i]

    if len(package_name) <= 20:
        formated_data[0][5] = package_name.center(20)
    elif len(package_name) > 20:
        package_name_formated = split_string(package_name, 20)
        for i in range(len(package_name_formated)):
            formated_data[i][5] += package_name_formated[i]

    return formated_data


def post_processing(formated_data: List[List[str]]) -> List[List[str]]:
    formated_data = [sublist for sublist in formated_data if
                     any(char != '' for char in sublist)]  # Clears all lines from [][] where no data
    for i in range(len(formated_data)):
        for j in range(len(formated_data[i])):
            if formated_data[i][j] == '':
                # To fill free space
                if j == 0: formated_data[i][j] = ' ' * 26
                if j == 1: formated_data[i][j] = ' ' * 22
                if j == 2: formated_data[i][j] = ' ' * 30
                if j == 3: formated_data[i][j] = ' ' * 100
                if j == 4: formated_data[i][j] = ' ' * 30
                if j == 5: formated_data[i][j] = ' ' * 20
            else:
                continue
            # To avoid < len then expected to be a table
            if len(formated_data[i][2]) != 30: formated_data[i][2] = formated_data[i][2].ljust(30)
            if len(formated_data[i][3]) != 100: formated_data[i][3] = formated_data[i][3].ljust(100)
            if len(formated_data[i][4]) != 30: formated_data[i][4] = formated_data[i][4].ljust(30)
            if len(formated_data[i][5]) != 20: formated_data[i][5] = formated_data[i][5].ljust(20)

    return formated_data


def log_prepared_data(prepared_data: List[List[str]]):
    with open("access.log", 'a') as file:
        for row in range(len(prepared_data)):
            for column in range(len(prepared_data[row])):
                file.write(f"|{prepared_data[row][column]}")
            file.write("|\n")
        file.write(
            "+--------------------------+----------------------+------------------------------+----------------------------------------------------------------------------------------------------+------------------------------+--------------------+\n")


def collect_data(external_ip: str, hostname: str, working_directory: str, user: str, package_name: str) -> bool:
    try:
        tmp_data = format_data(external_ip, hostname, working_directory, user, package_name)
        tmp_data = post_processing(tmp_data)
        log_prepared_data(tmp_data)
    except Exception as e:
        return False
    return True
