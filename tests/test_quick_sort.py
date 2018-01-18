'''
    This module test implemented quick sort algorithm.
'''
# import sys, os
# myPath = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, myPath + '/../')
# from random import random
#
# from sorting_algorithms.benchmark import benchmark
# from sorting_algorithms.merge_sort import merge_sort
# from sorting_algorithms.quick_sort import quick_sort
#
#
# def test_sorting_order() -> None:
#     input_list = [random() for _ in range(10000)]
#     result = quick_sort(input_list)
#
#     print(benchmark(quick_sort, input_list) < benchmark(merge_sort, input_list))
#     assert result == sorted(input_list), result
#     assert benchmark(quick_sort, input_list) < benchmark(merge_sort, input_list)
