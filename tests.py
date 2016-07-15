import pytest
import sys


errorCode = pytest.main(["-x", "test"])
if __name__ == '__main__':
    sys.exit(errorCode)
