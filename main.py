from typing import Callable, Generator
from collections import defaultdict
import re
import sys
from colorama import Fore
from datetime import datetime

#Task 1
def caching_fibonacci() -> Callable[[int], int]:
    cache = {}
    def fibonacci(n: int) -> int:
        if not isinstance(n, int):
            raise TypeError("Argument must be of type int")
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        if n in cache:
            return cache[n]
        else:
            cache[n] = fibonacci(n-1) + fibonacci(n-2)
            return cache[n]
    return fibonacci

#Task 2
def generator_numbers(text: str) -> Generator[int, None, None]:
    pattern = re.compile(r"\s\d+\.\d+\s")
    matches = re.finditer(pattern, text) #Чому finditer не було в конспекті :(
    first_match = next(matches, None)
    if first_match is None:
        raise ValueError("No numbers found in text or they are in improper format")
    yield float(first_match.group())
    for match in matches:
        yield float(match.group())

def sum_profit(text: str, func: Callable[[str], str]) -> float:
    total = 0
    for num in func(text):
        total += num
    return total

#Task 3

def parse_log_line(line: str) -> dict:
    valid_levels = ["INFO", "DEBUG", "ERROR", "WARNING"]
    split_line = line.strip().split(" ", 3)
    if len(split_line) < 4:
        raise ValueError(f"The logs file might be damaged")
    date, time, level, message = split_line
    try: 
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {date}")
    
    try: 
        datetime.strptime(time, "%H:%M:%S")
    except ValueError:
        raise ValueError(f"Invalid time format: {time}")
    
    if level not in valid_levels:
        raise ValueError(f"Unknown log level: {level}")
    
    parsed_log_dictionary = {
        "date": date,
        "time": time,
        "level": level,
        "message": message,
    }
    return parsed_log_dictionary

        

def load_logs(file_path: str) -> list:
    logs = []
    with open(file_path, 'r', encoding="UTF-8") as f:
        for line in f:
            logs.append(parse_log_line(line))
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    filtered_logs = [x for x in logs if x["level"] == level.upper()]
    return filtered_logs

def count_logs_by_level(logs: list) -> dict:
    log_counts = defaultdict(int)
    for log in logs:
        log_counts[log["level"]] += 1
    return log_counts

def display_log_counts(counts: dict) -> str:
    result_string = "Рівень логування | Кількість\n-----------------|----------"
    for item in counts.items():
        color = color_map.get(item[0], Fore.WHITE)
        result_string += f"\n{color}{item[0]:<17}{Fore.RESET}| {color}{item[1]}{Fore.RESET}"
    return result_string

color_map = {
    "INFO": Fore.BLUE,
    "DEBUG": Fore.GREEN,
    "ERROR": Fore.RED,
    "WARNING": Fore.YELLOW,
}

if __name__ == "__main__":
    # sys.argv = ["main.py", "logs.log", "critical"]
    if len(sys.argv) == 1:
        sys.exit(f"{Fore.RED}Error:{Fore.RESET} Please, provide the path to a log file.")
    path = sys.argv[1]
    try: 
        logs = load_logs(path)
    except FileNotFoundError:
        sys.exit(f"{Fore.RED}Error:{Fore.RESET} File was not found. Please, try again.")
    except UnicodeDecodeError:
        sys.exit(f"{Fore.RED}Error:{Fore.RESET} File must be using UTF-8 encoding.")
    except IsADirectoryError:
        sys.exit(f"{Fore.RED}Error:{Fore.RESET} The path points to a directory, and not a file.")
    except Exception as e:
        sys.exit(f"{Fore.RED}Error:{Fore.RESET} {e}")

    if not logs:
        sys.exit(f"{Fore.RED}Error:{Fore.RESET} No logs were found in the file provided.")

    elif len(sys.argv) > 2:
        level = sys.argv[2]
        filtered_logs = filter_logs_by_level(logs, level)
        if not filtered_logs:
            sys.exit(f"{Fore.RED}Error:{Fore.RESET} The given log level '{level}' was not found.")
        for log in filtered_logs:
            color = color_map.get(log['level'], Fore.WHITE)
            print(f"{log['date']} {log['time']} {color}{log['level']}{Fore.RESET} {log['message']}")            
    else:
        log_counts = count_logs_by_level(logs)
        print(display_log_counts(log_counts))


#Task 1
# fib = caching_fibonacci()
# print(fib(10))  # Виведе 55
# print(fib(15))  # Виведе 610

#Task 2
# text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
# total_income = sum_profit(text, generator_numbers)
# print(f"Загальний дохід: {total_income}")