#!/usr/bin/python
from ROOT import gStyle, gPad, TCanvas, TPad
import ROOT as r

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



f1 = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/3j/noEW/tt_PowhegP8.root")
f2 = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/4j/noEW/tt_PowhegP8.root")
#f1 = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/test/6j_2/tt_PowhegP8.root")
#f2 = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/test/6j_2/tt_PowhegP8.root")

h1 = f1.Get("3j_RECO/3j_Mtt_resol")
#h2 = f2.Get("3j_RECO_semi/3j_Mtt_resol")
h2 = f2.Get("YUKAWA_RECO/yukawa_Mtt_resol")

h1.Scale(1/h1.Integral())
h2.Scale(1/h2.Integral())
h1.GetXaxis().SetTitle("M_{t#bar{t}} (RECO-GEN)/GEN")
h1.GetYaxis().SetTitle("normalized")
h1.SetTitle("M_{t#bar{t}} resolution")
h1.GetXaxis().SetTitleOffset(1.2)


c1 = r.TCanvas("c1","comparison", 600,500)
gStyle.SetOptStat(0)
gStyle.SetTitleStyle(0)
#gStyle.SetLabelSize(2)
pad = TPad('pad','pad', 0.02, 0.035, 0.98, 0.97)
pad.SetTopMargin(0.09)
#pad.SetBottomMargin(0.07)
pad.SetLeftMargin(0.15)
pad.SetRightMargin(0.05)
pad.Draw()
pad.cd()
gPad.SetLogy()


h1.SetLineWidth(3)
h2.SetLineWidth(3)
h1.SetLineColor(r.kRed)
h2.SetLineColor(r.kBlue)
h1.SetMaximum(1.8)
#h1.GetXaxis().SetRangeUser(-1.5, 1.5)
#h2.GetXaxis().SetRangeUser(-1.5, 1.5)
h1.Draw("L")
h2.Draw("SAME L")
xl1=0.75
yl1=0.78
xl2=xl1+.2
yl2=yl1+.110
leg = r.TLegend(xl1,yl1,xl2,yl2)
#leg = can.BuildLegend()
leg.SetFillColor(0)
leg.SetFillStyle(0);
leg.SetLineColor(0);
leg.SetLineStyle(0);
leg.SetBorderSize(0);
leg.SetShadowColor(0);
leg.AddEntry(h1,"3 jets","l")
leg.AddEntry(h2,"4 jets","l")
#leg.AddEntry(h1,"6j using 3j algo","l")
#leg.AddEntry(h2,"6j","l")
#leg.AddEntry(h1,"Wja in 3j algorithm","l")
#leg.AddEntry(h2,"Wjb in 3j algorithm","l")
leg.Draw("same")

cmstext()

c1.SaveAs("resolmtt.pdf")
c1.SaveAs("resolmtt.png")

