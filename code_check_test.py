#!/usr/bin/env python3

from code_check import CodeCheck
def main():
    code_checker = CodeCheck('./user_code/11210162.py')
    code_checker.check_code()

if __name__ == '__main__':
    main()