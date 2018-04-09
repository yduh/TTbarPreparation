#!/usr/bin/python
from ROOT import gStyle, TCanvas, TPad
import ROOT as r
import numpy as np
from array import array

c1 = r.TCanvas("c1","comparison", 600,500)
gStyle.SetOptStat(0)
#gStyle.SetTitleStyle(0)
#gStyle.SetLabelSize(2)



outfile = "./3jmissjpt.png"
outrootfile = "3jminnspt.root"

#f = r.TFile("/afs/cern.ch/user/y/yduh/test/3j_test_withcut5/tt_PowhegP8.root")
#f = r.TFile("/afs/cern.ch/user/y/yduh/test/3j_debug4/tt_PowhegP8.root")
f = r.TFile("/afs/cern.ch/user/y/yduh/test/newdebug/3j_4/tt_PowhegP8.root") #3j

#h1 = f.Get("3j_RECO_right/3j_chi2").ProjectionX("right")
#h2 = f.Get("3j_RECO_wrong/3j_chi2").ProjectionX("wrong")
h1 = f.Get("3j_MISSJ/3j_min_nspt_right")
h2 = f.Get("3j_MISSJ/3j_min_nspt_wrong")
#h3 = h2.Clone()
#h3.Add(h1)

#for i in range(h1.GetXaxis().GetNbins()):
#	print i+1, h1.GetBinContent(i+1), h2.GetBinContent(i+1)
h1.Rebin(5)
h2.Rebin(5)
h1.Scale(1/h1.Integral('width'))
h2.Scale(1/h2.Integral('width'))
h1.GetXaxis().SetTitle("p_{T, min} in NS ellipse [GeV]")
h1.GetYaxis().SetTitle("normalized")

X = []
Lright = []
Lwrong = []
for x in np.arange(0, 500, 10):
	X.append(x)
	Lright.append(h1.GetBinContent(h1.GetXaxis().FindFixBin(x)))
	Lwrong.append(h2.GetBinContent(h2.GetXaxis().FindFixBin(x)))
X.append(500)
Lright.append(0)
Lwrong.append(0)
print X, Lright, Lwrong


c1.Print(outfile+"[")
h1.SetLineWidth(3)
h2.SetLineWidth(3)
h1.SetLineColor(r.kRed)
h2.SetLineColor(r.kBlue)
#h1.GetXaxis().SetRangeUser(300, 2000)
#h2.GetXaxis().SetRangeUser(300, 2000)
h1.Draw()
h2.Draw("same")
#c1.SetLogy()
xl1=0.6
yl1=0.75
xl2=xl1+.22
yl2=yl1+.100
leg = r.TLegend(xl1,yl1,xl2,yl2)
#leg = can.BuildLegend()
leg.SetFillColor(0)
leg.SetFillStyle(0);
leg.SetLineColor(0);
leg.SetLineStyle(0);
leg.SetBorderSize(0);
leg.SetShadowColor(0);
leg.AddEntry(h1,"correct b_{h}","l")
leg.AddEntry(h2,"wrong b_{h}","l")
leg.Draw("same")
c1.Print(outfile)

outroot = r.TFile(outrootfile, "RECREATE")
gright = r.TGraph(len(X), array("d", X), array("d", Lright))
gwrong = r.TGraph(len(X), array("d", X), array("d", Lwrong))
gright.SetName("nsptmin_bhright")
gwrong.SetName("nsptmin_bhwrong")
#gright.Draw("AC")
#gwrong.Draw("AC")
gright.Write()
gwrong.Write()
outroot.Close()

