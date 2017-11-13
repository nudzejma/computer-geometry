def quick_sort(input_list: list):
    '''
    :param input_list: input list of numbers
    :return: sorted list
    '''
    if len(input_list) <= 1:
        return input_list
    left = []
    same = []
    right = []
    pivot = input_list[0]
    for element in input_list:
        if element < pivot:
            left.append(element)
        elif element == pivot:
            same.append(pivot)
        else:
            right.append(element)

    return quick_sort(left) + same + quick_sort(right)
