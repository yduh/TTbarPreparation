#!/usr/bin/python
import ROOT as r
import sys
from array import array
from math import sqrt
from SCALE import *
from binning import bins2D

njets = sys.argv[1]
rebinX = bins2D().rebinX #5 #2GeV/bin
numybins = len(bins2D().absybins)-1
ttscale = TTscale
nominal = "noEW"

f = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/%sunc/%s/pdf/tt_PowhegP8.root" %(njets, nominal))
outfile = "/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/WrapUp/%s/skimroot/skim_pdf_tt_PowhegP8_%s.root" %(njets, nominal)
outfile = r.TFile(outfile, "RECREATE")

kint = "3j_RECO/3j_Mtt_delY" if njets == '3j' else "YUKAWA_RECO/yukawa_Mtt_delY"

hnominal = [[0 for x in range(2)] for x in range(numybins)]
#print hnominal

for i in range(len(bins2D().absybins)-1):
	binpL = f.Get(kint).GetYaxis().FindFixBin(bins2D().absybins[i])
	binpH = f.Get(kint).GetYaxis().FindFixBin(bins2D().absybins[i+1])
	binmH = f.Get(kint).GetYaxis().FindFixBin(-(bins2D().absybins[i]))
	binmL = f.Get(kint).GetYaxis().FindFixBin(-(bins2D().absybins[i+1]))
	#print binpL, binpH, binmL, binmH
	#0 and 1 are the range for positive and negative dely regions
	hnominal[i][0] = f.Get(kint).ProjectionX("mtt%s0" %i, binpL, binpH).Rebin(rebinX)
	hnominal[i][1] = f.Get(kint).ProjectionX("mtt%s1" %i, binmL, binmH).Rebin(rebinX)


hsigList = []
rmsList = []
haupList = []
hadoList = []
for y_bin in range(numybins):
	hsig = hnominal[y_bin][0].Clone()
	hsig.Add(hnominal[y_bin][1])
	hsig.Scale(ttscale)
	hsigList.append(hsig)

	hsig2 = f.Get("TRUTH/pdfunc_reco_dy%smtt/Iweights/weight_1" %(y_bin+1)).Rebin(rebinX)
	hsig2.Scale(ttscale)

	hderList = []
	for pset in range(10, 110):
		hispdf = f.Get("TRUTH/pdfunc_reco_dy%smtt/Iweights/weight_%s" %(y_bin+1, pset)).Rebin(rebinX)
		hispdf.Scale(ttscale)
		hder = hispdf.Clone()
		hder.Add(hsig, -1)
		hderList.append(hder)

	rmsOneyList = []
	for x_bin in range(hsig.GetNbinsX()):
		print x_bin, hsig.GetBinContent(x_bin+1)- hsig2.GetBinContent(x_bin+1)
		rms = 0
		for pset in range(100):
			rms = rms + hderList[pset].GetBinContent(x_bin+1)*hderList[pset].GetBinContent(x_bin+1)
		rms = sqrt(rms/100)+hsig.GetBinContent(x_bin+1)
		rmsOneyList.append(rms)
	rmsList.append(rmsOneyList)
	print rmsOneyList


	haupOneyList = []
	hadoOneyList = []
	haup = f.Get("TRUTH/pdfunc_reco_dy%smtt/Iweights/weight_110" %(y_bin+1)).Rebin(rebinX)
	hado = f.Get("TRUTH/pdfunc_reco_dy%smtt/Iweights/weight_111" %(y_bin+1)).Rebin(rebinX)
	haup.Scale(ttscale)
	hado.Scale(ttscale)
	for x_bin in range(hsig.GetNbinsX()):
		haupOneyList.append(haup.GetBinContent(x_bin+1))
		hadoOneyList.append(hado.GetBinContent(x_bin+1))
	haupList.append(haupOneyList)
	hadoList.append(hadoOneyList)


hrms = r.TH2D("2DPDF", "PDF", len(rmsList[0]), 0, 2000, numybins, array("d", bins2D().absybins))
haup = r.TH2D("2DalphaUp", "alphaup", len(rmsList[0]), 0, 2000, numybins, array("d", bins2D().absybins))
hado = r.TH2D("2DalphaDown", "alphadown", len(rmsList[0]), 0, 2000, numybins, array("d", bins2D().absybins))
hsigall = r.TH2D("2DSIG", "sig", len(rmsList[0]), 0, 2000, numybins, array("d", bins2D().absybins))
#hrmsall = r.TH1D("PDF", "PDF", len(rmsList)*len(rmsList[0]), 0, 2000*len(rmsList))
#hsigall = r.TH1D("SIG", "SIG", len(rmsList)*len(rmsList[0]), 0, 2000*len(rmsList))
print len(rmsList)*len(rmsList[0])
print len(rmsList)

xy_bin = 0
for y_bin in range(len(rmsList)):
	#hsigList[y_bin].Write()
	for x_bin in range(len(rmsList[0])):
		#xy_bin = xy_bin + 1
		#print xy_bin, rmsList[y_bin][x_bin]
		hrms.SetBinContent(x_bin+1, y_bin+1, rmsList[y_bin][x_bin])
		haup.SetBinContent(x_bin+1, y_bin+1, haupList[y_bin][x_bin])
		hado.SetBinContent(x_bin+1, y_bin+1, hadoList[y_bin][x_bin])
		hsigall.SetBinContent(x_bin+1, y_bin+1, hsigList[y_bin][x_bin])
		#hrmsall.SetBinContent(xy_bin, rmsList[y_bin][x_bin])
hrms.Write()
haup.Write()
hado.Write()
hsigall.Write()
#hrmsall.Write()

outfile.Close()


