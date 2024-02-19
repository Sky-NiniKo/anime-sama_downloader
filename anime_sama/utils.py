import sys
from typing import TypeVar, Iterable

from termcolor import colored, RESET, COLORS
from termcolor._types import Color

T = TypeVar("T")


def put_color(color: Color):
    return f"\033[{COLORS[color]}m"


def safe_input(text: str, transform):
    while True:
        try:
            output = input(text)
            print(RESET, end="")
            return transform(output)
        except ValueError:
            pass


def print_selection(choices: list, print_choices=True) -> None:
    if len(choices) == 0:
        sys.exit(colored("No result", "red"))
    if len(choices) == 1:
        print(f"-> {colored(choices[0], 'blue')}")
        return
    if not print_choices:
        return

    for index, choice in enumerate(choices, start=1):
        line_colors = "yellow" if index % 2 == 0 else None
        print(
            colored(f"[{index:{len(str(len(choices)))}}]", "green"),
            colored(choice, line_colors),
        )


def select_one(choices: list[T], msg="Choose a number", print_choices=True) -> T:
    print_selection(choices)
    if len(choices) == 1:
        return choices[0]

    return choices[safe_input(f"{msg}: " + put_color("blue"), int) - 1]


def select_range(choices: list[T], msg="Choose a range", print_choices=True) -> list[T]:
    print_selection(choices, print_choices)

    if len(choices) == 1:
        return [choices[0]]

    ints = safe_input(
        f"{msg} {colored(f'[1-{len(choices)}]', 'green')}: {put_color('blue')}",
        lambda string: tuple(map(int, string.split("-"))),
    )
    if len(ints) == 1:
        return [choices[ints[0] - 1]]

    return choices[ints[0] - 1 : ints[1]]


def suppress_stop_iteration(*args: list[Iterable], defaut=None) -> iter:
    args = [iter(arg) for arg in args]

    while True:
        value_yielded = False

        for arg in args:
            try:
                yield next(arg)
                value_yielded = True
            except StopIteration:
                yield defaut

        if not value_yielded:
            break
