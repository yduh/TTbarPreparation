#!/usr/bin/python
from ROOT import gStyle, TCanvas, TPad
import ROOT as r
import numpy as np
from array import array

c1 = r.TCanvas("c1","comparison", 600,500)
gStyle.SetOptStat(0)
#gStyle.SetTitleStyle(0)
#gStyle.SetLabelSize(2)



outfile = "./3jmissj2d.png"
outrootfile = "3j2d.root"

f = r.TFile("/afs/cern.ch/user/y/yduh/test/newdebug/3j_4/tt_PowhegP8.root")

h1 = f.Get("3j_MISSJ/3j_nspt_nseta_right")
h2 = f.Get("3j_MISSJ/3j_nspt_nseta_wrong")

h1.Rebin2D(3, 3)
h2.Rebin2D(3, 3)
h1.Scale(1/h1.Integral('width'))
h2.Scale(1/h2.Integral('width'))
h1.GetXaxis().SetTitle("p_{T, min} in NS ellipse")
h1.GetYaxis().SetTitle("#eta_{max}")
h1.GetZaxis().SetTitle("normalized")

c1.Print(outfile+"[")
h1.SetLineWidth(3)
h2.SetLineWidth(3)
h1.SetLineColor(r.kRed)
h2.SetLineColor(r.kBlue)
#h1.GetXaxis().SetRangeUser(300, 2000)
#h2.GetXaxis().SetRangeUser(300, 2000)
h2.Draw()
h1.Draw("same")
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
h1.SetName("nspteta_right")
h2.SetName("nspteta_wrong")
h1.Write()
h2.Write()
outroot.Close()


