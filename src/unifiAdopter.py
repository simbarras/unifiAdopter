import os
import sys

from . import Ctrl
from . import Restorer


def run():
    ctrl = Ctrl()
    ctrl.load()

    preStart = True
    for args in sys.argv:
        if args == '-noAsk':
            preStart = False

    continu = True
    if preStart:
        continu = ctrl.prestart()

    if continu:
        ctrl.start()
        ctrl.scan()
        ctrl.finish()
    else:
        print('Manually stopped')


def restore():
    restorer = Restorer()
    restorer.restoreFile()


print(sys.version)
os.getcwd()
restoreO = False
for args in sys.argv:
    if args == '-restore':
        restoreO = True
if restoreO:
    restore()
else:
    run()
