import typing

from checkmytex.checker.problem import Problem

class ColorCodes:
    BOLD = '\033[1m'
    FAIL = "\033[91m\033[4m"
    LOG = "\033[94m"
    HEADER = "\033[95m"
    ENDC = "\033[0m"
    BLACK_ON_WHITE = "\033[0;30;47m"
    WARNING = "\033[93m"

def log(text: str):
    print(f"{ColorCodes.LOG}{text}{ColorCodes.ENDC}")

def print_header(text: str):
    l = "="*len(text)
    print(f"{ColorCodes.HEADER}|={l}=|{ColorCodes.ENDC}")
    print(f"{ColorCodes.HEADER}| {text} |{ColorCodes.ENDC}")
    print(f"{ColorCodes.HEADER}|={l}=|{ColorCodes.ENDC}")

def highlight(s: str):
    return f"{ColorCodes.FAIL}{s}{ColorCodes.ENDC}"


def add_highlights(line: str,
                   highlights: typing.Iterable[typing.Tuple[int, int]]) -> str:
    highlights = list(highlights)
    if not highlights:
        return line
    highlights.sort()
    hb, he = highlights[0]
    highlighted_line = line[:hb]
    for h in highlights:
        if he >= h[0]:
            he = h[1]
        else:
            highlighted_line += highlight(line[hb:he])
            highlighted_line += line[he:h[0]]
            hb = h[0]
            he = h[1]
    highlighted_line += highlight(line[hb:he] if hb != he else " ")
    highlighted_line += line[he:]
    return highlighted_line


def print_line(line: str, line_number: int,
               problems: typing.Iterable[Problem]):
    def span(p):
        a = p.origin.begin.col if p.origin.begin.row == line_number else 0
        b = p.origin.end.col if p.origin.end.row == line_number else len(line)
        return a, b

    highlighted_line = add_highlights(line, (span(p) for p in problems))
    print(f"{ColorCodes.BLACK_ON_WHITE}{line_number}:{ColorCodes.ENDC}",
          highlighted_line)


def print_problem(problem: Problem, info: str = ""):
    if info:
        print(f" >>> {ColorCodes.WARNING}{problem.message}{ColorCodes.ENDC}"
              f" ({problem.tool}) {info}")
    else:
        print(
            f" >>> {ColorCodes.WARNING}{problem.message}{ColorCodes.ENDC}"
            f" ({problem.tool})")
