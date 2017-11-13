def merge(list_1: list, list_2: list) -> list:
  '''
	Args:
		list_1: sorted input list of numbers
		list_2: sorted input list of numbers
	Returns:
		merged and sorted list
	'''
  sorted_list = list()
  i, j = 0, 0
  while True:
	  if i == len(list_1):
	    sorted_list.extend(list_2[j:])
	    break
	  if j == len(list_2):
	    sorted_list.extend(list_1[i:])
	    break
	  if list_1[i] < list_2[j]:
	    sorted_list.append(list_1[i])
	    i += 1
	  else:
	    sorted_list.append(list_2[j])
	    j += 1
  return sorted_list

def merge_sort(input_list:list) -> list:
  '''
	Args:
		input_list: input list of numbers
	Returns:
		our list sorted
	'''
  if(len(input_list) == 1):
    return input_list
  split_index = len(input_list) // 2
  first = merge_sort(input_list[:split_index])
  second = merge_sort(input_list[split_index:])

  return merge(first, second)
