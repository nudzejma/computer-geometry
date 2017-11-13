'''
  This module returns methods time of performing.
'''
from time import time
def benchmark(method: callable, arg: any):
  '''
  :param method: method we want to examine
  :param arg: arguments related to method
  :return: time of performing
  '''
  fm = time()
  method(arg)
  sm = time()
  # print('{}s'.format(sm-fm))
  return sm-fm
