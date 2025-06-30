from typing import Callable, Generator
import re

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
    sum = 0
    for num in func(text):
        sum += num
    return sum

#Task 3




#Task 1
# fib = caching_fibonacci()
# print(fib(10))  # Виведе 55
# print(fib(15))  # Виведе 610

#Task 2
# text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
# total_income = sum_profit(text, generator_numbers)
# print(f"Загальний дохід: {total_income}")