#!/usr/bin/python
import ROOT as r
import sys, os
from array import array
from math import sqrt

njets = sys.argv[1]
CASE_DER = True
nominal = "noEW"

kint = "mtt_dely_RECO"
GT = ['1695','1715','noEW','1735','1755','noEW'] #put nominal in the last element

if njets == "3j":
	color = '6' #8
elif njets == "4j":
	color = '2' #1
elif njets == "5j":
	color = '8' #4
elif njets == "6j":
	color = '1' #2

f = r.TFile("./%s/ch%s_mt.root" %(njets, njets))
hlist = []
testDict = {}
for gt in GT:
	h = f.Get(kint+"_"+gt)
	hlist.append(h)
	testList = []
	for ibin in range(h.GetNbinsX()):
		testList.append(h.GetBinContent(ibin+1))
	print "testList = ", testList
	testDict[ibin] = testList[ibin]

BinsScale = {}
errBinsScale = {}
cout = 0
for i in range(hlist[-1].GetXaxis().GetNbins()):
	BinsScale[i] = []
	errBinsScale[i] = []
	for h in hlist[0:-1]:
		BinsScale[i].append((h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1))
		if h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1) == 0:
			errBinsScale[i].append(0)
		else:
			errBinsScale[i].append((pow(sqrt(abs(h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1)))/(h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1)),2) + pow(sqrt(hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1), 2)) * (h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1))
		print "bin",i+1,": ",h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1),"/",hlist[-1].GetBinContent(i+1),"=",(h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1)

print BinsScale
outfile = r.TFile("./%s/signal_proc_ch%s.root" %(njets, njets), "RECREATE")
for i in range(hlist[-1].GetXaxis().GetNbins()):
	if(BinsScale[i][1]) == -1: #for the case of no-entry bins
		cout += 1
		continue
	gtmin = -3 #eval(GT[0].split('y')[0]) if len(GT)==len(set(GT)) else -eval(GT[0].split('y')[0])
	gtmax = 3 #eval(GT[-2].split('y')[0])
	fitfun = "[1]*x+[0]*x*x"
	p = r.TH1D("bin_content_par1_%d" %(i+1-cout), "parabola%d" %(i+1-cout), len(GT)-1, gtmin-0.5, gtmax+0.5)
	pfit = r.TF1("bin_content_par1_%d" %(i+1-cout), fitfun, gtmin-2.0, gtmax+2.0) #+-2 is a random extendsion number
	gfit = r.TF1("parabola%d" %(i+1-cout), fitfun, gtmin-2.0, gtmax+2.0)

	x = [-3, -1, 0, 1, 3]
	y = []
	erry = []
	for j in range(0, len(GT)-1, 1):
		p.SetBinContent(j+1, BinsScale[i][j])
		y.append(BinsScale[i][j])
		erry.append(errBinsScale[i][j])
	gr = r.TGraphErrors(len(x), array("d", x), array("d", y), array("d", [0.0001]*len(x)), array("d", [0.0001]*len(x)))

	p.Fit(pfit, "q")
	pfit.SetParameters(pfit.GetParameter(0), pfit.GetParameter(1))
	pfit.Write()

	gfit.SetLineColor(int(color))
	gr.SetLineColor(int(color))
	gr.SetMarkerColor(int(color))
	gr.Fit(gfit, "q")
	gr.Draw("AC*")
	gr.Write() #comment it if you want it clean! uncomment it if you want to check the fit quickly
	p0 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParameter(0)
	p1 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParameter(1)
	e0 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParError(0)
	e1 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParError(1)
	p2 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParameter(2)
	e2 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParError(2)

outfile.Close()

