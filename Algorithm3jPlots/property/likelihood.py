#!/usr/bin/python
from ROOT import gStyle, gPad, TCanvas, TPad, TGraph
import ROOT as r
import numpy as np
from array import array

def cmstext():
	xpos = r.gPad.GetLeftMargin()
	ypos = 1.-r.gPad.GetTopMargin()

	lx = r.TLatex(0., 0., 'Z')
	lx.SetNDC(True)
	lx.SetTextFont(62)
	lx.SetTextSize(0.05)
	lx.SetTextAlign(13)
	lx.DrawLatex(xpos+0.04, ypos-0.03, 'CMS')

	lx2 = r.TLatex(0., 0., 'Z')
	lx2.SetNDC(True)
	lx2.SetTextFont(53)
	lx2.SetTextSize(20)
	lx2.SetTextAlign(13)
	#lx2.DrawLatex(xpos+0.04, ypos-0.08, '#it{Preliminary}')
	lx2.DrawLatex(xpos+0.04, ypos-0.08, 'Simulation')

	lx3 = r.TLatex(0., 0., 'Z')
	lx3.SetNDC(True)
	lx3.SetTextFont(43)
	lx3.SetTextSize(23)
	lx3.SetTextAlign(31)
	lx3.DrawLatex(xpos+0.78, ypos+0.015,'35.8 fb^{-1}(13 TeV)')
	lx3.Draw()

	lx4 = r.TLatex(0., 0., 'Z')
	lx4.SetNDC(True)
	lx4.SetTextFont(63)
	lx4.SetTextSize(25)
	lx4.SetTextAlign(13)
	lx4.DrawLatex(0.45, ypos-0.03,'e/#mu+jets')






f = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/3j/noEW/tt_PowhegP8.root") #3j

h1 = f.Get("3j_RECO/3j_likelihood_right")
h2 = f.Get("3j_RECO/3j_likelihood_wrong")
#h1 = f.Get("3j_RECO_right/3j_likelihood")
#h2 = f.Get("3j_RECO_wrong/3j_likelihood")
#h1 = f.Get("3j_MISSJ/3j_likelihood2_right")
#h2 = f.Get("3j_MISSJ/3j_likelihood2_wrong")

h1.Rebin(2)
h2.Rebin(2)
h1.Scale(1/h1.Integral('width'))
h2.Scale(1/h2.Integral('width'))
h1.GetXaxis().SetTitle("-ln(#lambda_{3})")
h1.GetYaxis().SetTitle("normalized")
h1.GetXaxis().SetTitleOffset(1.)
h1.GetYaxis().SetTitleOffset(1.2)

X = []
Lright = []
Lwrong = []
for x in np.arange(0, 25, 0.2):
	X.append(x)
	Lright.append(h1.GetBinContent(h1.GetXaxis().FindFixBin(x)))
	Lwrong.append(h2.GetBinContent(h2.GetXaxis().FindFixBin(x)))
X.append(25)
Lright.append(0)
Lwrong.append(0)
print X, Lright, Lwrong


c1 = r.TCanvas("c1","comparison", 600,500)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetTitleStyle(0)
#gStyle.SetLabelSize(2)
pad = TPad('pad','pad', 0.01, 0.01, 0.98, 0.98)
pad.SetTopMargin(0.09)
#pad.SetBottomMargin(0.07)
pad.SetLeftMargin(0.17)
pad.SetRightMargin(0.05)
pad.Draw()
pad.cd()


h1.SetLineWidth(3)
h2.SetLineWidth(3)
h1.SetLineColor(r.kRed)
h2.SetLineColor(r.kBlue)
#h1.GetYaxis().SetRangeUser(0, 0.15)
#h2.GetYaxis().SetRangeUser(0, 0.15)
#h1.GetXaxis().SetRangeUser(6, 25)
#h2.GetXaxis().SetRangeUser(6, 25)
#h1.GetXaxis().SetRangeUser(12, 30)
h1.GetXaxis().SetRangeUser(6, 20)
h1.SetMaximum(0.8)
h2.SetMaximum(0.8)
h1.Draw()
h2.Draw("same")
#c1.SetLogy()
xl1=0.62
yl1=0.78
xl2=xl1+.32
yl2=yl1+.110
leg = r.TLegend(xl1,yl1,xl2,yl2)
#leg = can.BuildLegend()
leg.SetFillColor(0)
leg.SetFillStyle(0);
leg.SetLineColor(0);
leg.SetLineStyle(0);
leg.SetBorderSize(0);
leg.SetShadowColor(0);
leg.AddEntry(h1,"correct b-jets","l")
leg.AddEntry(h2,"wrong b-jets","l")
leg.Draw("same")
cmstext()
c1.SaveAs("3jlikelihood.pdf")
c1.SaveAs("3jlikelihood.png")


outrootfile = "3jcombine2.root"
outroot = r.TFile(outrootfile, "RECREATE")
gright = r.TGraph(len(X), array("d", X), array("d", Lright))
gwrong = r.TGraph(len(X), array("d", X), array("d", Lwrong))
gright.SetName("combine2_bsright")
gwrong.SetName("combine2_bswrong")
#gright.Draw("AC")
#gwrong.Draw("AC")
gright.Write()
gwrong.Write()
outroot.Close()

