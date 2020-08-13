import os
import sys

from Ctrl import Ctrl

def run():
    ctrl = Ctrl()
    ctrl.load()

    preStart = True
    for args in sys.argv:
        if args == '-noAsk':
            preStart = False

    continu = True
    if preStart:
        continu = ctrl.preStart()

    if continu:
        ctrl.start()
        ctrl.scan()
        ctrl.finish()
    else:
        print('Manually stopped')

print(sys.version)
os.getcwd()

run()
