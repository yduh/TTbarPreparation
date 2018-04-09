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



#f = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/3j/noEW/tt_PowhegP8.root") #3j
f = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/4jup/noEW/tt_PowhegP8.root") #3j

#h1 = f.Get("3j_RECO/3j_nschi_right")
#h2 = f.Get("3j_RECO/3j_nschi_wrong")
h1 = f.Get("TRUTH/truth_nschi_right")
h2 = f.Get("TRUTH/truth_nschi_wrong")

h1.Rebin(3)
h2.Rebin(3)
h1.Scale(1/h1.Integral('width'))
h2.Scale(1/h2.Integral('width'))
h1.GetXaxis().SetTitle("D_{#nu, min} [GeV]")
h1.GetYaxis().SetTitle("normalized")
h1.GetXaxis().SetTitleOffset(1.2)
h1.GetYaxis().SetTitleOffset(1.5)

X = []
Lright = []
Lwrong = []
for x in np.arange(0, 500, 6):
	X.append(x)
	Lright.append(h1.GetBinContent(h1.GetXaxis().FindFixBin(x)))
	Lwrong.append(h2.GetBinContent(h2.GetXaxis().FindFixBin(x)))
X.append(500)
Lright.append(0)
Lwrong.append(0)
print X, Lright, Lwrong


c1 = r.TCanvas("c1","comparison", 600,500)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
#gStyle.SetTitleStyle(0)
#gStyle.SetLabelSize(2)
pad = TPad('pad','pad', 0.02, 0.018, 0.98, 0.98)
pad.SetTopMargin(0.09)
#pad.SetBottomMargin(0.07)
pad.SetLeftMargin(0.17)
pad.SetRightMargin(0.05)
pad.Draw()
pad.cd()


'''
outFile = r.TFile("./likelihood3j.root","RECREATE")
gright.Write('nsd_right')
gwrong.Write('nsd_wrong')
outFile.Close()
'''
h1.SetLineWidth(3)
h2.SetLineWidth(3)
h1.SetLineColor(r.kRed)
h2.SetLineColor(r.kBlue)
h1.GetXaxis().SetRangeUser(0, 150)
h2.GetXaxis().SetRangeUser(0, 150)
h1.SetMaximum(0.035)
h2.SetMaximum(0.035)
h1.Draw()
h2.Draw("same")
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
leg.AddEntry(h1,"Correct leptonic b-jets","l")
leg.AddEntry(h2,"Wrong leptonic b-jets","l")
leg.Draw("same")
cmstext()
c1.SaveAs("4jnschi.pdf")
c1.SaveAs("4jnschi.png")

outrootfile = "3jnschi.root"
outroot = r.TFile(outrootfile, "RECREATE")
gright = r.TGraph(len(X), array("d", X), array("d", Lright))
gwrong = r.TGraph(len(X), array("d", X), array("d", Lwrong))
gright.SetName("nschi_blright")
gwrong.SetName("nschi_blwrong")
#gright.Draw("AC")
#gwrong.Draw("AC")
gright.Write()
gwrong.Write()
outroot.Close()


