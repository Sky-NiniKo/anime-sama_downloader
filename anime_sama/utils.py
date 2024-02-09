def safe_input(text: str, transform):
    while True:
        try:
            return transform(input(text))
        except ValueError:
            pass
