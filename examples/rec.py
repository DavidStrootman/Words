def odd(n: int) -> bool:
    return False if n == 0 else even(n - 1)


def even(n: int) -> bool:
    return True if n == 0 else odd(n - 1)


if __name__ == "__main__":
    print(odd(21))
