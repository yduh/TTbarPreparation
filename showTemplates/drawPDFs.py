#!/usr/bin/python
import os, sys

upnum = 24000

for p in [p for p in range(113,169,2)]:
	os.system('python plotTemplates_1comp.py %s pdf%s%s %s 0.06' %(sys.argv[1],p,p+1,upnum))

os.system('python plotTemplates_1comp.py %s alpha %s 0.06' %(sys.argv[1],upnum))
