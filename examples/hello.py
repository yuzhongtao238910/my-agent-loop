def add(a: int, b: int) -> int:
    """计算两个整数的和并返回结果。

    Args:
        a (int): 第一个加数。
        b (int): 第二个加数。

    Returns:
        int: a 与 b 的和。
    """
    return a + b


def main() -> None:
    """主函数：演示 add 函数的用法。"""
    result = add(3, 5)
    print(f"3 + 5 = {result}")


if __name__ == "__main__":
    main()