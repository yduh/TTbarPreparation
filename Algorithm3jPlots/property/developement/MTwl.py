#!/usr/bin/python
from ROOT import gStyle, TCanvas, TPad, TGraph
import ROOT as r
import numpy as np
from array import array

c1 = r.TCanvas("c1","comparison", 600,500)
gStyle.SetOptStat(0)
#gStyle.SetTitleStyle(0)
#gStyle.SetLabelSize(2)



outfile = "./3jMTwl.png"
#outrootfile = "3jthad.root"

f = r.TFile("/afs/cern.ch/user/y/yduh/work/Hathor-2.1-beta/results/3j_ICHEP_noMTwlcut/1.0y/tt_PowhegP8.root")
f2 = r.TFile("/afs/cern.ch/user/y/yduh/work/Hathor-2.1-beta/results/3j_ICHEP_noMTwlcut/1.0y/singleT.root")
f3 = r.TFile("/afs/cern.ch/user/y/yduh/work/Hathor-2.1-beta/results/3j_ICHEP_noMTwlcut/1.0y/Vjets.root")
#f = r.TFile("/afs/cern.ch/user/y/yduh/test/3j_test_nocut2/tt_PowhegP8.root")
#f = r.TFile("/afs/cern.ch/user/y/yduh/work/Hathor-2.1-beta/results/3j/1.0y/tt_PowhegP8.root") #3j

#h1 = f.Get("3j_RECO_right/3j_chi2").ProjectionX("right")
#h2 = f.Get("3j_RECO_wrong/3j_chi2").ProjectionX("wrong")
h1 = f.Get("3j_RECO_right/3j_MTwl")
h2 = f.Get("3j_RECO_wrong/3j_MTwl")
h3 = f.Get("3j_RECO_semi/3j_MTwl")
h4 = f.Get("3j_RECO_other/3j_MTwl")
h5 = f2.Get("3j_RECO/3j_MTwl")
h6 = f3.Get("3j_RECO/3j_MTwl")
#h3 = h2.Clone()
#h3.Add(h1)

h1.Rebin(5)
h2.Rebin(5)
h3.Rebin(5)
h4.Rebin(5)
h5.Rebin(5)
h6.Rebin(5)
h1.Scale(1/h1.Integral('width'))
h2.Scale(1/h2.Integral('width'))
h3.Scale(1/h3.Integral('width'))
h4.Scale(1/h4.Integral('width'))
h5.Scale(1/h5.Integral('width'))
h6.Scale(1/h6.Integral('width'))
h1.GetXaxis().SetTitle("transverse mass W_{l} [GeV]")
h1.GetYaxis().SetTitle("normalized")
'''
X = []
Lright = []
Lwrong = []
for x in np.arange(0, 1000, 10):
	X.append(x)
	Lright.append(h1.GetBinContent(h1.GetXaxis().FindFixBin(x)))
	Lwrong.append(h2.GetBinContent(h2.GetXaxis().FindFixBin(x)))
X.append(1000)
Lright.append(0)
Lwrong.append(0)
print X, Lright, Lwrong
'''

c1.Print(outfile+"[")
h1.SetLineWidth(3)
h2.SetLineWidth(3)
h3.SetLineWidth(3)
h4.SetLineWidth(3)
h5.SetLineWidth(3)
h6.SetLineWidth(3)
h1.SetLineColor(r.kRed-4)
h2.SetLineColor(r.kBlue-9)
h3.SetLineColor(r.kBlue-5)
h4.SetLineColor(r.kMagenta-8)
h5.SetLineColor(r.kOrange)
h6.SetLineColor(r.kGreen+2)
#h1.GetYaxis().SetRangeUser(0, 0.016)
#h2.GetYaxis().SetRangeUser(0, 0.016)
h1.GetXaxis().SetRangeUser(0, 400)
h2.GetXaxis().SetRangeUser(0, 400)
h3.GetXaxis().SetRangeUser(0, 400)
h4.GetXaxis().SetRangeUser(0, 400)
h5.GetXaxis().SetRangeUser(0, 400)
h6.GetXaxis().SetRangeUser(0, 400)
h1.Draw()
h2.Draw("same")
h3.Draw("same")
h4.Draw("same")
h5.Draw("same")
h6.Draw("same")
#c1.SetLogy()
xl1=0.6
yl1=0.65
xl2=xl1+.22
yl2=yl1+.200
leg = r.TLegend(xl1,yl1,xl2,yl2)
#leg = can.BuildLegend()
leg.SetFillColor(0)
leg.SetFillStyle(0);
leg.SetLineColor(0);
leg.SetLineStyle(0);
leg.SetBorderSize(0);
leg.SetShadowColor(0);
leg.AddEntry(h1,"tt correct reco","l")
leg.AddEntry(h2,"tt wrong reco","l")
leg.AddEntry(h3,"tt not reco","l")
leg.AddEntry(h4,"tt bck","l")
leg.AddEntry(h5,"single top","l")
leg.AddEntry(h6,"V+jets","l")
leg.Draw("same")
c1.Print(outfile)

'''
outroot = r.TFile(outrootfile, "RECREATE")
gright = r.TGraph(len(X), array("d", X), array("d", Lright))
gwrong = r.TGraph(len(X), array("d", X), array("d", Lwrong))
gright.SetName("thad_bhright")
gwrong.SetName("thad_bhwrong")
#gright.Draw("AC")
#gwrong.Draw("AC")
gright.Write()
gwrong.Write()
outroot.Close()
'''

