def buble_sort(input_list:list) -> list:
  '''
	Args:
		input_list: input list of numbers
	Returns:
		our list sorted
	'''
  for i, _ in enumerate(input_list):
	  for j, _ in enumerate(input_list[:-i-1]):
		  if input_list[j] > input_list[j+1]:
			  input_list[j], input_list[j+1] = input_list[j+1], input_list[j]
  return input_list
