#!/usr/bin/env python3

from test import Test
import os
import sys

def main():

    COLUMNS = ['subject','sessionIndex',
                'rep','H.period','DD.period.t',
                'UD.period.t','H.t','DD.t.i',
                'UD.t.i','H.i','DD.i.e','UD.i.e',
                'H.e','DD.e.five','UD.e.five',
                'H.five','DD.five.Shift.r','UD.five.Shift.r',
                'H.Shift.r','DD.Shift.r.o','UD.Shift.r.o',
                'H.o','DD.o.a','UD.o.a','H.a','DD.a.n',
                'UD.a.n','H.n','DD.n.l','UD.n.l','H.l',
                'DD.l.Return','UD.l.Return','H.Return'
    ]


    TEST_STRING = '.tie5Roanl'

    OUTFILE = 'test.csv'


    test = Test(TEST_STRING, COLUMNS, OUTFILE)

    # cheesy way to check if program was launched from xterm

    if 'XTERM_VERSION' not in os.environ:
        print('Error: program must be launched from xterm')
        sys.exit(1)
    

    test.start_test()

    test.process_data()


if __name__ == '__main__':
    main()