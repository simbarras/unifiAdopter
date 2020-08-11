import os
import sys

from controllers.Ctrl import Ctrl

print(sys.version)
os.getcwd()
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
    ctrl.run()
    ctrl.finish()
else:
    print('Manually stopped')
