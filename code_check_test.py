#!/usr/bin/env python3
from code_check import CodeCheck

def main (path):
    code_checker = CodeCheck(path, 15)
    if not code_checker.check_code():
        print(code_checker.errormsg)
    else:
        print('pass')

if __name__ == '__main__':
    main('tem_code/11610634_汪至圆_GoBang_bot.py')
