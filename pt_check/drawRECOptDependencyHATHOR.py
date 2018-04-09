#!/usr/bin/python
from ROOT import gStyle, TCanvas, TPad
import ROOT as r
import sys

njets = sys.argv[1]

c1 = r.TCanvas("c1","comparison", 600,500)
gStyle.SetOptStat(0)
gStyle.SetTitleStyle(0)
#gStyle.SetLabelSize(2)

#c1.Divide(2,1)

f0 = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults_old/test/pt/"+njets+"/noEW/tt_PowhegP8.root")
f1 = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults_old/test/pt/"+njets+"/1.0y/tt_PowhegP8.root")
f2 = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults_old/test/pt/"+njets+"/2.0y/tt_PowhegP8.root")
f3 = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults_old/test/pt/"+njets+"/3.0y/tt_PowhegP8.root")
#f1 = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/4j/3.0y/tt_PowhegP8.root")
#f2 = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/4j/1.0y/tt_PowhegP8.root")

hName = '3j_RECO/3j_Mtt_pt' if njets == '3j' else 'YUKAWA_RECO/yukawa_Mtt_pt'
h0 = f0.Get(hName).ProjectionY("no gt").Rebin(20)
h1 = f1.Get(hName).ProjectionY("gt").Rebin(20)
h2 = f2.Get(hName).ProjectionY("2gt").Rebin(20)
h3 = f3.Get(hName).ProjectionY("3gt").Rebin(20)
#print h1.Integral(), h1.GetName(), h2.Integral(), h2.GetName()

val11 = []
val21 = []
val31 = []

#c1.cd(1)
c1.SetGrid()


ratio10 = h1.Clone()
ratio10.Divide(h0)
ratio10.SetLineWidth(3)
ratio10.SetLineColor(r.kRed)
ratio10.GetYaxis().SetRangeUser(0.85, 1.1)
ratio10.GetXaxis().SetTitleOffset(1.2)
ratio10.GetYaxis().SetTitleOffset(1.2)
ratio10.GetXaxis().SetTitle("p_T(t)")
ratio10.GetYaxis().SetTitle("Scenario yields/Powheg yields")
ratio10.SetTitle("p_{T}(t) comparison, reweighting in (M{t#bar{t}}, #Deltay)")
ratio10.Draw("hist")
for ibin in range(ratio10.GetXaxis().GetNbins()):
	val11.append(ratio10.GetBinContent(ibin+1))

ratio20 = h2.Clone()
ratio20.Divide(h0)
ratio20.SetLineWidth(3)
ratio20.SetLineColor(r.kBlue)
ratio20.Draw("samehist")
for ibin in range(ratio20.GetXaxis().GetNbins()):
	val21.append(ratio20.GetBinContent(ibin+1))

ratio30 = h3.Clone()
ratio30.Divide(h0)
ratio30.SetLineWidth(3)
ratio30.SetLineColor(r.kGreen)
ratio30.Draw("samehist")
for ibin in range(ratio30.GetXaxis().GetNbins()):
	val31.append(ratio30.GetBinContent(ibin+1))



print val11
print val21
print val31
xl1=0.5
yl1=0.55
xl2=xl1+.42
yl2=yl1+.200
leg = r.TLegend(xl1,yl1,xl2,yl2)
#leg = can.BuildLegend()
leg.SetFillColor(0)
leg.SetFillStyle(0);
leg.SetLineColor(0);
leg.SetLineStyle(0);
leg.SetBorderSize(0);
leg.SetShadowColor(0);
leg.AddEntry(ratio10,"Y_{t} =1 /Powheg","l")
leg.AddEntry(ratio20,"Y_{t} =2 /Powheg","l")
leg.AddEntry(ratio30,"Y_{t} =3 /Powheg","l")
leg.Draw("same")

'''
c1.cd(2)
#c1.SetLogy()
h0.SetLineWidth(3)
h1.SetLineWidth(3)
h2.SetLineWidth(3)
h3.SetLineWidth(3)
h0.SetLineColor(r.kBlack)
h1.SetLineColor(r.kRed)
h2.SetLineColor(r.kBlue)
h3.SetLineColor(r.kGreen)
#h1.GetXaxis().SetRangeUser(-1.5, 1.5)
#h2.GetXaxis().SetRangeUser(-1.5, 1.5)
print h1.GetName(), h2.GetName(), h3.GetName(), h0.GetName()
h3.Draw()
h2.Draw("same")
h1.Draw("same")
h0.Draw("same")
xl1=0.6
yl1=0.55
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
leg.AddEntry(h1,"1.0y","l")
leg.AddEntry(h2,"2.0y","l")
leg.AddEntry(h3,"3.0y","l")
leg.AddEntry(h0,"noEW","l")
#leg.AddEntry(h1,"6j using 3j algo","l")
#leg.AddEntry(h2,"6j","l")
#leg.AddEntry(h1,"Wja in 3j algorithm","l")
#leg.AddEntry(h2,"Wjb in 3j algorithm","l")
leg.Draw("same")
#c1.SaveAs("resolmtt.pdf")
#c1.SaveAs("resolmtt.png")
'''

