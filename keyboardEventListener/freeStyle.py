#!/usr/bin/env python
import sys
import termios
import contextlib
import time

@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

def main():
    f = open('code1.txt', 'r');

    for line in f:
        with raw_mode(sys.stdin):
            try:
                for idx, val in enumerate(line):
                    key = sys.stdin.read(1)
                    key_code = ord(key)
                    if not key or key == chr(4):
                        break
                    if key_code == 0x09 or key_code == 0x0a:
                        while idx < len(line):
                            sys.stdout.write(line[idx])
                            idx = idx + 1
                        break
                    else:
                        sys.stdout.write(val),
            except (KeyboardInterrupt, EOFError):
		print ''
                sys.exit(0)

if __name__ == '__main__':
    main()
