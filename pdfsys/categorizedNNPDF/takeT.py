#!/usr/bin/python
import ROOT
import sys
from array import array

njets = sys.argv[1]
NFinal = sys.argv[2]

f = ROOT.TFile("%s/n%s/skim_pdf.root" %(njets,NFinal))
outfile = ROOT.TFile('%s/n%s/pdfT.root' %(njets,NFinal), "RECREATE")

pset = 0
for key in f.GetListOfKeys():
	if 'ttsig_pdf' in key.GetName() and 'Up' in key.GetName() and 'sum' not in key.GetName():
		pset += 1
print pset, "sets of PDF are remained!"


def writeHist(histName):
	for p in range(pset):
		Up = f.Get(histName+'_pdf%sUp' %str(p+1))
		Dw = f.Get(histName+'_pdf%sDown' %str(p+1))
		Up.Write(histName+'_pdf%sUp' %str(p+1))
		Dw.Write(histName+'_pdf%sDown' %str(p+1))

	#sumUp = f.Get(histName+'_pdfsumUp')
	#sumDw = f.Get(histName+'_pdfsumDown')
	#sumUp.Write(histName+'_pdfsumUp')
	#sumDw.Write(histName+'_pdfsumDown')


writeHist('ttsig')
writeHist('st')

outfile.Close()


