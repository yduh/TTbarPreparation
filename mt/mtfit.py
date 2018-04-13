#!/usr/bin/python
import ROOT as r
import sys, os
from array import array
from math import sqrt

njets = sys.argv[1]
nominal = "noEW"

kint = "mtt_dely_RECO"

#if njets == "3j":
#	color = '6' #8
#elif njets == "4j":
#	color = '2' #1
#elif njets == "5j":
#	color = '8' #4
#elif njets == "6j":
#	color = '1' #2


f = r.TFile("./%s/ch%s_mt.root" %(njets, njets))
hlist1gev = []
hlist3gev = []
for mt in ['1695','noEW','1755','noEW']: #put nominal in the last element
	h = f.Get(kint+"_"+mt)
	hlist3gev.append(h)
for mt in ['1715','noEW','1735','noEW']: #put nominal in the last element
	h = f.Get(kint+"_"+mt)
	hlist1gev.append(h)

##############################################################################################################################
def quadraticFun(hlist, gev, color):
	BinsScale = {}
	errBinsScale = {}
	cout = 0
	for i in range(hlist[-1].GetXaxis().GetNbins()):
		BinsScale[i] = []
		errBinsScale[i] = []
		for h in hlist[0:-1]:
			BinsScale[i].append((h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1))/(hlist[-1].GetBinContent(i+1)*gev))
			if h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1) == 0:
				errBinsScale[i].append(0)
			else:
				errBinsScale[i].append((pow(sqrt(abs(h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1)))/(h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1)),2) + pow(sqrt(hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1), 2)) * (h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1))
			print "bin",i+1,": ",h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1),"/",hlist[-1].GetBinContent(i+1),"=",(h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1)
	print BinsScale

	for i in range(hlist[-1].GetXaxis().GetNbins()):
		if(BinsScale[i][1]) == -1: #for the case of no-entry bins
			cout += 1
			continue

		mtmin = -1
		mtmax = 1
		fitfun = "[1]*x+[0]*x*x"
		p = r.TH1D("bin_content_par1_%d" %(i+1-cout), "parabola%d" %(i+1-cout), len(hlist)-1, mtmin-0.5, mtmax+0.5)
		pfit = r.TF1("bin_content_par1_%d" %(i+1-cout), fitfun, mtmin-2.0, mtmax+2.0) #+-2 is a random extendsion number
		gfit = r.TF1("parabola%d" %(i+1-cout), fitfun, mtmin-2.0, mtmax+2.0)

		x = [-1, 0, 1]
		y = []
		erry = []
		for j in range(0, len(hlist)-1, 1):
			p.SetBinContent(j+1, BinsScale[i][j])
			y.append(BinsScale[i][j])
			erry.append(errBinsScale[i][j])
		gr = r.TGraphErrors(len(x), array("d", x), array("d", y), array("d", [0.0001]*len(x)), array("d", [0.0001]*len(x)))

		p.Fit(pfit, "q")
		pfit.SetParameters(pfit.GetParameter(0), pfit.GetParameter(1))
		#pfit.Write('bin_content_par1_%s%d' %(gev,(i+1-cout)))

		gfit.SetLineColor(color)
		gr.SetLineColor(color)
		gr.SetMarkerColor(color)
		gr.Fit(gfit, "q")
		gr.Draw("AC*")
		gr.Write("parabola%sGeV_bin%s"%(gev,(i+1)))
		p0 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParameter(0)
		p1 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParameter(1)
		e0 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParError(0)
		e1 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParError(1)
		#p2 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParameter(2)
		#e2 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParError(2)

##############################################################################################################################

outfile = r.TFile("./%s/signal_proc_ch%s.root" %(njets, njets), "RECREATE")
quadraticFun(hlist1gev, 1, r.kRed)
quadraticFun(hlist3gev, 3, r.kBlue)
outfile.Close()

