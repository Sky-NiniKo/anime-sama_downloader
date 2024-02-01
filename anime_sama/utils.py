def find_pattern_in(text: str, start: str, end: str, with_pattern=False) -> list[str]:
    found = []

    start_pos = text.find(start) + len(start)
    while start_pos != len(start)-1:
        end_pos = start_pos + text[start_pos:].find(end)
        if end_pos == start_pos-1:
            break

        if with_pattern:
            found.append(text[start_pos - len(start):end_pos + len(end)])
        else:
            found.append(text[start_pos:end_pos])

        text = text[end_pos + len(end):]
        start_pos = text.find(start) + len(start)

    return found


def safe_input(text: str, transform):
    while True:
        try:
            return transform(input(text))
        except ValueError:
            pass
