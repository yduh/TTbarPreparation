#!/usr/bin/python
from ROOT import gStyle, TCanvas, TPad
import ROOT as r
import numpy as np

c1 = r.TCanvas("c1","comparison", 600,500)
gStyle.SetOptStat(0)
#gStyle.SetTitleStyle(0)
#gStyle.SetLabelSize(2)



outfile = "./3jmissjcompt.png"

f = r.TFile("/afs/cern.ch/user/y/yduh/test/tt_PowhegP82.root")
#f = r.TFile("/afs/cern.ch/user/y/yduh/work/Hathor-2.1-beta/results/3j/1.0y/tt_PowhegP8.root") #3j

#h1 = f.Get("3j_RECO_right/3j_chi2").ProjectionX("right")
#h2 = f.Get("3j_RECO_wrong/3j_chi2").ProjectionX("wrong")
h1 = f.Get("3j_GEN/3j_thadmiss_pt")
h2 = f.Get("3j_MISSJ/3j_nspt")
#h3 = h2.Clone()
#h3.Add(h1)

#for i in range(h1.GetXaxis().GetNbins()):
#	print i+1, h1.GetBinContent(i+1), h2.GetBinContent(i+1)
h1.Rebin(2)
h2.Rebin(2)
h1.Scale(1/h1.Integral())
h2.Scale(1/h2.Integral())
h1.GetXaxis().SetTitle("D_{#nu, min} [GeV]")
h1.GetYaxis().SetTitle("normalized")

c1.Print(outfile+"[")
h1.SetLineWidth(3)
h2.SetLineWidth(3)
h1.SetLineColor(r.kRed)
h2.SetLineColor(r.kBlue)
h1.GetXaxis().SetRangeUser(0, 200)
h2.GetXaxis().SetRangeUser(0, 200)
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
leg.AddEntry(h1,"GEN missj","l")
leg.AddEntry(h2,"RECO missj","l")
leg.Draw("same")
c1.Print(outfile)

