#!/usr/bin/python
import ROOT as r
import os
import sys

na = 1
nb = 15


for njets in ['3j','4j','5j','6j']:
	os.system('hadd -f %s/skim_pdf_noEW.root %s/skim_pdf_tt_PowhegP8_noEW.root %s/skim_pdf_STt_topbar_noEW.root %s/skim_pdf_STt_top_noEW.root' %(njets,njets,njets,njets))

os.system('python put3456j.py')

for n in range(na, nb+1):
	os.system('mkdir -p ./3456j/n'+str(n))
	os.system('mkdir -p ./3j/n'+str(n))
	os.system('mkdir -p ./4j/n'+str(n))
	os.system('mkdir -p ./5j/n'+str(n))
	os.system('mkdir -p ./6j/n'+str(n))

	os.system('python simplepdf.py '+str(n))

		#arg = [str(s) for s in range(1, n+1)]
		#print 'python takeT.py '+' '.join(arg)
		#os.system('python takeT.py '+' '.join(arg))
		#os.system('python takeT.py '+njets+' '+str(n))
		#os.system('mv *.root '+njets+'/n'+str(n))


