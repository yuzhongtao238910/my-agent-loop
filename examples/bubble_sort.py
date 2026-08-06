from typing import List


def bubble_sort(arr: List[int]) -> List[int]:
    """对整数列表进行冒泡排序（升序）。

    冒泡排序通过重复遍历列表，依次比较相邻元素并交换顺序错误的元素，
    直到整个列表有序。

    Args:
        arr (List[int]): 待排序的整数列表。

    Returns:
        List[int]: 排序后的新列表（升序）。
    """
    n = len(arr)
    result = arr[:]  # 拷贝一份，避免修改原列表

    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break

    return result


def main() -> None:
    """主函数：演示冒泡排序的用法。"""
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"排序前: {data}")
    sorted_data = bubble_sort(data)
    print(f"排序后: {sorted_data}")


if __name__ == "__main__":
    main()