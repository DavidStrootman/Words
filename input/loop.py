def summy(n: int) -> int:
    result = 0
    while n >= 1:
        result += n
        n -= 1

    return result

if __name__ == "__main__":
    print(summy(21))
