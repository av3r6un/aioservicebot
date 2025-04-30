from bot import start
from prereq import main
import sys

if __name__ == '__main__':
  if sys.platform == 'linux':
    main()
  start()
