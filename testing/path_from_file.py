import os


def test():
  print(__file__)
  print(os.path.realpath(__file__))
  print(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':
  test()
