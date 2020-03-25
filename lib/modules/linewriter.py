class linewriter:
  def __init__(self):
    self.__line = []

  def add(self, line):
    self.__line.append(line)

  def str(self):
    return '\n'.join(self.__line)



if __name__ == '__main__':
  l = linewriter()
  assert l.str() == '', l.str()

  l.add('line 1')
  assert l.str() == 'line 1'

  l.add('line 2')
  assert l.str() == 'line 1\nline 2'