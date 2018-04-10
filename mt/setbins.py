#!/usr/bin/python
import ROOT as r
import sys
from array import array
import Rebin
#import binning
from binning import bins2D

njets = sys.argv[1]
numin = int(sys.argv[2]) #10000

xbins = bins2D().xbins_4j if njets != '3j' else bins2D().xbins_3j

kint = "mtt_dely_RECO"
#GT = ['0.0y','1.0y','2.0y','3.0y','4.0y','5.0y',nominal] #put the reference one in the last
GT = ['1695', '1715', '1735', '1755', 'noEW', '1715old', '1735old']

inpath = '/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/WrapUp/%s/' %njets

f = r.TFile(inpath+'packroot/ch%s.root' %njets)
numbins = f.Get("ttsig").GetNbinsX()

fnominal = r.TFile(inpath+'skimroot/skim_tt_PowhegP8_noEW.root', 'READ')
histnominal = Rebin.Absy(Rebin.newRebin2D(fnominal.Get(kint), 'ttsig_temp', xbins, bins2D().ybins), kint, xbins, bins2D().absybins)

outfile = r.TFile('./%s/ch%s_mt.root' %(njets, njets), 'RECREATE')

for gt in GT:
	f = r.TFile(inpath+'skimroot/skim_mtop%s_tt_PowhegP8_noEW.root' %gt, 'READ') if gt != 'noEW' else r.TFile(inpath+'skimroot/skim_tt_PowhegP8_noEW.root', 'READ')
	hist = Rebin.Absy(Rebin.newRebin2D(f.Get(kint), 'ttsig_temp', xbins, bins2D().ybins), kint, xbins, bins2D().absybins)

	#opthall = r.TH1D(hist.GetName()+"_"+gt, hist.GetTitle(), numbins, 0, numbins)
	opthall = r.TH1D(hist.GetName()+"_"+gt+"_temp", hist.GetTitle(), 1000, 0, 1000) #1000 is just a big number which definiely larger than the bins we want in the end
	optbin = 0
	lastbinmark = []
	for j in range(histnominal.GetYaxis().GetNbins()):
		bee = 0
		carry = 0
		for i in range(histnominal.GetXaxis().GetNbins()):
			bee = histnominal.GetBinContent(i+1, j+1) + bee #number of signal hist
			carry = hist.GetBinContent(i+1, j+1) + carry #number of target hist
			if(bee >numin):
				optbin += 1
				opthall.SetBinContent(optbin, carry)
				bee = 0
				carry = 0
			else:
				if(i == histnominal.GetXaxis().GetNbins()-1):
					optbin += 1
					opthall.SetBinContent(optbin, carry)
					lastbinmark.append(optbin)
					bee = 0
					carry = 0

	raw = []
	for ibin in range(optbin):
		raw.append(opthall.GetBinContent(ibin+1))

	# ______________________
	refine = []
	lastbinmarkminusone = [each-1 for each in lastbinmark]
	lastbinmarkminustwo = [each-2 for each in lastbinmark]
	for ielement,element in enumerate(raw):
		if ielement in lastbinmarkminustwo:
			refine.append(element+raw[ielement+1])
		elif ielement in lastbinmarkminusone:
			continue
		else:
			refine.append(element)
	print "here", len(refine),refine
	# ______________________

	#re-save the opthall to the bin number it should be
	#hall = r.TH1D(h.GetName(), h.GetTitle(), len(refine), 0, len(refine))
	hall = r.TH1D(hist.GetName()+"_"+gt, hist.GetTitle(), len(refine), 0, len(refine))
	for ibin in range(len(refine)):
		hall.SetBinContent(ibin+1, refine[ibin])
	outfile.cd()
	hall.Write()


	#outfile.cd()
	#opthall.Write()

	#hall = r.TH1D(hist.GetName(), hist.GetTitle(), optbin, 0, optbin)
	#for ibin in range(optbin):
	#	hall.SetBinContent(ibin+1, opthall.GetBinContent(ibin+1))
	#hall.Write()

outfile.Close()



