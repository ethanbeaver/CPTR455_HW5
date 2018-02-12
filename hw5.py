"""
Homework #5 for CPTR454.

Problem #11 from section 6.4

Written By Ethan Beaver
"""
import math
import numpy as np
import sys
import timeit


def merge(list1, list2):
    """Merge function for MergeSort based on textbook's pseudocode."""
    result = np.zeros(len(list1) + len(list2))
    k = 0
    i = j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result[k] = list1[i]
            k += 1
            i += 1
        else:
            result[k] = list2[j]
            k += 1
            j += 1
    if i == len(list1):
        result[k:] = list2[j:]
    else:
        result[k:] = list1[i:]
    return result


def mergeSort(num_list):
    """Mergesort based on textbook's pseudocode."""
    list_length = len(num_list)
    if list_length > 1:
        A = num_list[:math.floor(list_length/2)]
        B = num_list[math.floor(list_length/2):]
        A = mergeSort(A)
        B = mergeSort(B)
        return merge(A, B)
    return num_list


def hoarePartition(num_list, left, right):
    """Partition array based on pseudocode in textbook."""
    p = num_list[left]
    i = left
    j = right + 1
    while True:
        while i < len(num_list)-1:
            i += 1
            if num_list[i] >= p:
                break
        while j > 0:
            j -= 1
            if num_list[j] <= p:
                break
        num_list[i], num_list[j] = num_list[j], num_list[i]
        if i >= j:
            break
    num_list[i], num_list[j] = num_list[j], num_list[i]
    num_list[left], num_list[j] = num_list[j], num_list[left]
    return j


def quickSortRecursive(num_list, left=0, right=None):
    """Quicksort from textbook pseudocode."""
    if right is None:
        right = len(num_list) - 1
    if left < right:
        s = hoarePartition(num_list, left, right)
        quickSort(num_list, left, s - 1)
        quickSort(num_list, s + 1, right)


def pushStack(stack, top, value):
    """Helper function for QuickSort."""
    stack[top+1] = value
    return top + 1


def popStack(stack, top):
    """Helper function for QuickSort."""
    return int(stack[top]), top-1


def quickSort(num_list):
    """
    Quicksort implemented as iterative to run on large sets.

    Recursive version was exceeding recursion depth.
    """
    left = 0
    right = len(num_list) - 1
    size = right - left + 1
    stack = np.zeros(size)

    top = -1

    top = pushStack(stack, top, left)
    top = pushStack(stack, top, right)

    while top >= 0:
        right, top = popStack(stack, top)
        left, top = popStack(stack, top)

        p = hoarePartition(num_list, left, right)

        if p-1 > left:
            top = pushStack(stack, top, left)
            top = pushStack(stack, top, p-1)

        if p+1 < right:
            top = pushStack(stack, top, p+1)
            top = pushStack(stack, top, right)


def heapBottomUp(num_list):
    """Construct a heap using the textbook's pseudocode."""
    n = len(num_list)
    for i in range(n, 0, -1):
        k = i
        v = num_list[k-1]
        heap = False
        while not heap and 2 * k <= n:
            j = 2 * k
            if j < n:
                if num_list[j-1] < num_list[j]:
                    j += 1
            if v >= num_list[j-1]:
                heap = True
            else:
                num_list[k-1] = num_list[j-1]
                k = j
        num_list[k-1] = v
    return num_list


def reHeapify(num_list, i):
    """Algorithm developed from textbook description of root deletion."""
    left = 2*i
    right = 2*i + 1
    largest = i

    if left <= len(num_list) and num_list[left-1] > num_list[largest-1]:
        largest = left
    if right <= len(num_list) and num_list[right-1] > num_list[largest-1]:
        largest = right
    if largest != i:
        num_list[i-1], num_list[largest-1] = num_list[largest-1], num_list[i-1]
        num_list = reHeapify(num_list, largest)
    return num_list


def heapSort(num_list):
    """From description of HeapSort in textbook."""
    sorted_list = np.zeros(len(num_list))
    heapBottomUp(num_list)

    for i in range(0, len(num_list)):
        num_list[0], num_list[-1] = num_list[-1], num_list[0]
        sorted_list[i] = num_list[-1]
        num_list = reHeapify(num_list[:-1], 1)

    return sorted_list[::-1]


def testSorting():
    """Function to test and time the execution of the sorting algorithms."""
    failures = 0
    for i in range(3, 7):
        print("----Testing array of size 10^" + str(i) + "----")
        print("\n")

        arr = np.random.randint(10000, size=10**i)
        arr1 = np.copy(arr)
        arr2 = np.copy(arr)
        print("-Testing random integers-")
        print("HeapSort: " + str(timeit.timeit(lambda: heapSort(arr), number=1)))
        print("QuickSort: " + str(timeit.timeit(lambda: quickSort(arr1), number=1)))
        print("MergeSort: " + str(timeit.timeit(lambda: mergeSort(arr2), number=1)))
        print("")

        quickSort(arr2)
        for sorted_arr in [heapSort(arr), arr2, mergeSort(arr2)]:
            if not all(sorted_arr[i] <= sorted_arr[i+1] for i in range(len(arr)-1)):
                failures += 1
                print("****FAILURE***")

        arr = np.arange(10**i)
        arr1 = np.copy(arr)
        arr2 = np.copy(arr)
        print("-Testing sorted integers-")
        print("HeapSort: " + str(timeit.timeit(lambda: heapSort(arr), number=1)))
        if i < 5:
            print("QuickSort: " + str(timeit.timeit(lambda: quickSort(arr1), number=1)))
        print("MergeSort: " + str(timeit.timeit(lambda: mergeSort(arr2), number=1)))
        print("")

        arr = np.arange(10**i, 0, -1)
        arr1 = np.copy(arr)
        arr2 = np.copy(arr)
        print("-Testing backwards sorted integers-")
        print("HeapSort: " + str(timeit.timeit(lambda: heapSort(arr), number=1)))
        if i < 5:
            print("QuickSort: " + str(timeit.timeit(lambda: quickSort(arr1), number=1)))
        print("MergeSort: " + str(timeit.timeit(lambda: mergeSort(arr2), number=1)))
        print("")

    if failures > 0:
        print("Some sorting failed")


if __name__ == "__main__":
    testSorting()
