#!/usr/bin/python
import ROOT as r
import sys, os
from array import array
from math import sqrt
from SCALE import *
from binning import bins2D

njets = sys.argv[1]

PDFsetStart = 110 #really start from 113; 110 111 are alphas
PDFsetEnd = 169

#rebinX = 40 #bins2D().rebinX #5 #2GeV/bin
# Manually put the binning:
###########################################
rebinX = []
if njets == '3j':
	rebinX.append([0, 300, 320, 340, 360, 380, 420, 460, 520, 2000])
	rebinX.append([0, 340, 380, 420, 460, 520, 2000])
	rebinX.append([0, 400, 440, 480, 520, 580, 660, 780, 2000])
elif njets == '4j':
	rebinX.append([0, 360, 400, 440, 480, 540, 2000])
	rebinX.append([0, 400, 440, 480, 520, 580, 2000])
	rebinX.append([0, 500, 560, 620, 700, 2000])
elif njets == '5j':
	rebinX.append([0, 380, 420, 480, 2000])
	rebinX.append([0, 420, 480, 560, 2000])
	rebinX.append([0, 540, 640, 2000])
elif njets == '6j':
	rebinX.append([0, 400, 2000])
	rebinX.append([0, 460, 2000])
	rebinX.append([0, 600, 2000])
###########################################
numxbins = len(rebinX[0])-1 + len(rebinX[1])-1 + len(rebinX[2])-1
numybins = len(bins2D().absybins)-1
nominal = "noEW"
print numxbins, numybins



def prepared(fileName, scaleFactor):
	f = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/%sunc/%s/pdf/%s" %(njets, nominal, fileName))
	outfile = "./%s/skim_pdf_%s_%s.root" %(njets, fileName.split('.')[0], nominal)
	outfile = r.TFile(outfile, "RECREATE")

	kint = "3j_RECO/3j_Mtt_delY" if njets == '3j' else "YUKAWA_RECO/yukawa_Mtt_delY"


	hct14cenList = []
	hnnpdfcenList = []

	hpdfDict = {}

	for y_bin in range(numybins):
		print len(rebinX[y_bin])-1, array('d', rebinX[y_bin])
		hct14cen = f.Get("TRUTH/pdfunc_reco_dy%smtt/Iweights/weight_112" %(y_bin+1)).Rebin(len(rebinX[y_bin])-1, "weight112_%s"%(y_bin+1), array('d', rebinX[y_bin]))
		hct14cen.Scale(scaleFactor)
		hct14cenList.append(hct14cen)
		hnnpdfcen = f.Get("TRUTH/pdfunc_reco_dy%smtt/Iweights/weight_1" %(y_bin+1)).Rebin(len(rebinX[y_bin])-1, "weight1_%s"%(y_bin+1), array('d', rebinX[y_bin]))
		hnnpdfcen.Scale(scaleFactor)
		hnnpdfcenList.append(hnnpdfcen)

	for pset in range(PDFsetStart, PDFsetEnd):
		if pset == 112:
			continue
		hpdfList = []
		for y_bin in range(numybins):
			hpdf = f.Get("TRUTH/pdfunc_reco_dy%smtt/Iweights/weight_%s" %(y_bin+1, pset)).Rebin(len(rebinX[y_bin])-1, "weight%s_%s"%(pset,y_bin+1), array('d', rebinX[y_bin]))
			hpdf.Scale(scaleFactor)
			hpdfList.append(hpdf)
		hpdfDict['%s' %pset] = hpdfList


	binxy = 1
	hct14cen = r.TH1D("ct14cen", "ct14cen", numxbins, 0, numxbins)
	hnnpdfcen = r.TH1D("nnpdfcen", "nnpdfcen", numxbins, 0, numxbins)
	for y_bin in range(numybins):
		for x_bin in range(len(rebinX[y_bin])-1):
			print y_bin, x_bin, hct14cenList[y_bin].GetBinContent(x_bin+1)
			hct14cen.SetBinContent(binxy, hct14cenList[y_bin].GetBinContent(x_bin+1))
			hnnpdfcen.SetBinContent(binxy, hnnpdfcenList[y_bin].GetBinContent(x_bin+1))
			binxy += 1
	hct14cen.Write()
	hnnpdfcen.Write()

	hrelUncList = []
	for pset in range(PDFsetStart, PDFsetEnd):
		if pset == 112:
			continue
		hpdf = r.TH1D("replica_%s" %pset, "PDFsubset %s" %pset, numxbins, 0, numxbins)
		hrelUnc = r.TH1D("relUnc_%s" %pset, "relativeUnc %s" %pset, numxbins, 0, numxbins)
		binxy = 1
		if pset != 110 and pset != 111:
			for y_bin in range(numybins):
				for x_bin in range(len(rebinX[y_bin])-1):
					hpdf.SetBinContent(binxy, hpdfDict['%s' %pset][y_bin].GetBinContent(x_bin+1))
					hrelUnc.SetBinContent(binxy, hpdfDict['%s' %pset][y_bin].GetBinContent(x_bin+1)/hct14cenList[y_bin].GetBinContent(x_bin+1) -1)
					binxy += 1
			hpdf.Write()
			hrelUnc.Write()
			hrelUncList.append(hrelUnc)
		else:
			for y_bin in range(numybins):
				for x_bin in range(len(rebinX[y_bin])-1):
					hpdf.SetBinContent(binxy, hpdfDict['%s' %pset][y_bin].GetBinContent(x_bin+1))
					hrelUnc.SetBinContent(binxy, hpdfDict['%s' %pset][y_bin].GetBinContent(x_bin+1)/hnnpdfcenList[y_bin].GetBinContent(x_bin+1) -1)
					binxy += 1
			hpdf.Write()
			hrelUnc.Write()
			hrelUncList.append(hrelUnc)


	c = r.TCanvas()
	for hpset in hrelUncList:
		hpset.SetLineColor(pset)
		hpset.Draw('same')

	outfile.Close()

#########################################################################################################################
prepared('tt_PowhegP8.root', TTscale)
#To be noticed that the official weights seem didn't match to CT14, it only works for the NNPDF
#You still keep it because you need the alpha s
prepared('STt_topbar.root', STtopbarscale)
prepared('STt_top.root', STtopscale)

os.system('hadd -f ./%s/skim_pdf_t_noEW.root ./%s/skim_pdf_STt_top_noEW.root ./%s/skim_pdf_STt_topbar_noEW.root' %(njets,njets,njets))
#Remember this is not the full single top although you call it is. Wt channels aren't included.
