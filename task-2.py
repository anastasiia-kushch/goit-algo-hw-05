def binary_search(arr, x):
    """
    Функція для бінарного пошуку елемента в відсортованому масиві.

    Parameters:
    arr (list): Відсортований масив для пошуку.
    target: Елемент, який шукаємо.

    Returns:
    int: Індекс елемента в масиві або -1, якщо елемент не знайдено.
    """

    low = 0
    high = len(arr) - 1
    mid = 0
    iterations = 0
    upper_bound = 0

    while low <= high:

        mid = (high + low) // 2
        iterations += 1

        if arr[mid] == x:
            return [iterations, mid]
        
        elif arr[mid] < x:
            low = mid + 1    
        
        else:
            high = mid - 1
            upper_bound = arr[mid]
    
    return [iterations, upper_bound]


arr = [2.2, 4.5, 6.3, 7.8, 9.6, 11.77]
print(binary_search(arr, 9.6))