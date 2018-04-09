from ratioplot import *
import sys
import ROOT

SavePlots = True
evtRangeUp = float(sys.argv[3]) #24000 #int(h.GetMaximum()/1000)+1
sysRangeDown = -float(sys.argv[4])
sysRangeUp = float(sys.argv[4])

#-----------------------------------------------------#
def cmstext():
	xpos = ROOT.gPad.GetLeftMargin()
	ypos = 1.-ROOT.gPad.GetTopMargin()

	lx = ROOT.TLatex(0., 0., 'Z')
	lx.SetNDC(True)
	lx.SetTextFont(62)
	lx.SetTextSize(0.05)
	lx.SetTextAlign(13)
	lx.DrawLatex(xpos+0.04, ypos-0.03, 'CMS')

	lx2 = ROOT.TLatex(0., 0., 'Z')
	lx2.SetNDC(True)
	lx2.SetTextFont(53)
	lx2.SetTextSize(20)
	lx2.SetTextAlign(13)
	#lx2.DrawLatex(xpos+0.04, ypos-0.08, '#it{Preliminary}')
	lx2.DrawLatex(xpos+0.04, ypos-0.08, 'Simulation')

	lx3 = ROOT.TLatex(0., 0., 'Z')
	lx3.SetNDC(True)
	lx3.SetTextFont(43)
	lx3.SetTextSize(23)
	lx3.SetTextAlign(31)
	lx3.DrawLatex(xpos+0.75, ypos+0.015,'35.8 fb^{-1}(13 TeV)')
	lx3.Draw()

def systext():
	lx4 = ROOT.TLatex(0., 0., 'Z')
	lx4.SetNDC(True)
	lx4.SetTextFont(63)
	lx4.SetTextSize(26)
	lx4.SetTextAlign(13)
	#arg = {'jes':'JEC','jes1':'JES SubTotalPileUp','jes2':'JES SubTotalRelative','jes3':'JES SubTotalPt','jes4':'JES SubTotalScale','jes5':'JES SubTotalAbsolute','jes6':'JES SubTotalMC','jer':'JER','pileup':'pile-up','lep':'lepton ID/trigger','btag':'b tagging scale factor','ltag':'b mis-tagging scale factor','MET':'MET'}
	arg = {'mt':'top mass','pdf':'PDFs','alpha':'alpha_s in PDFs','rsfs':'fact. & reno. scales','hdamp':'NLO shower matching','isr':'initial state radiation','fsr':'final state radiation','tune':'underlying events','bfrag':'b-jet fragmentation','bdecay':'B meson decaying Br.','color':'color reconnection'}
	#lx4.DrawLatex(0.3, 0.95, sys.argv[1]+', '+arg[sys.argv[2]])
	lx4.DrawLatex(0.45, 0.88, sys.argv[1]+', '+sys.argv[2])

def delytext(x1, x2, x3, y):
	lx5 = ROOT.TLatex(0., 0., 'Z')
	lx5.SetNDC(True)
	lx5.SetTextFont(63)
	lx5.SetTextSize(18)
	lx5.SetTextAlign(33)
	lx5.SetTextAngle(90)
	lx5.DrawLatex(x1, y, '0.0 < |#Delta_{y}| < 0.6')
	lx5.DrawLatex(x2, y, '0.6 < |#Delta_{y}| < 1.2')
	lx5.DrawLatex(x3, y, '1.2 < |#Delta_{y}| < 6.0')

#-----------------------------------------------------#

ROOT.gStyle.SetOptTitle(0)
f = ROOT.TFile('/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/URStatTools/Input/%s/ch%s.root' %(sys.argv[1],sys.argv[1]))
#f = ROOT.TFile('../WrapUp/%s/packroot/ch%s.root' %(sys.argv[1],sys.argv[1]))
#f = ROOT.TFile('~/public/lucien/%s/ch%s_ini.root' %(sys.argv[1],sys.argv[1]))

h = createH(f, 'ttsig')
hup = createHUp(f, 'ttsig', sys.argv[2], ROOT.kRed)
hdw = createHDw(f, 'ttsig', sys.argv[2], ROOT.kBlue)
h_st = createH(f, 'st')
h_vj = createH(f, 'vj')
h_qcd = createH(f, 'qcd')


linedely = []
for ibin in range(h.GetXaxis().GetNbins()):
	mttlow = int(float(str(h.GetXaxis().GetBinLabel(ibin+1).split(',')[0].split('-')[0])))
	mtthigh = int(float(str(h.GetXaxis().GetBinLabel(ibin+1).split(',')[0].split('-')[1])))
	if mtthigh == 2000:
		linedely.append(ibin+1)
	h.GetXaxis().SetBinLabel(ibin+1,'%s-%s' %(mttlow,mtthigh))
	hup.GetXaxis().SetBinLabel(ibin+1,'%s-%s' %(mttlow,mtthigh))
	hdw.GetXaxis().SetBinLabel(ibin+1,'%s-%s' %(mttlow,mtthigh))
	h.GetXaxis().LabelsOption('v')
	hup.GetXaxis().LabelsOption('v')
	hdw.GetXaxis().LabelsOption('v')

hrup = createRatio(hup, h, ROOT.kRed, 't#bar{t}')
hrdw = createRatio(hdw, h, ROOT.kBlue, 't#bar{t}')
c, pad1, pad2 = createCanvasPads2()

pad1.cd()
h.GetYaxis().SetRangeUser(0, evtRangeUp)
h.Draw()
hup.Draw("E0same")
hdw.Draw("E0same")
h_st.SetLineColor(ROOT.kOrange)
h_st.Draw("same")
h_vj.SetLineColor(ROOT.kCyan+1)
h_vj.Draw("same")
h_qcd.SetLineColor(ROOT.kGreen+2)
h_qcd.Draw("same")


h.GetYaxis().SetLabelSize(0.0)
axis = TGaxis(0, 2000, 0, evtRangeUp, 2000, evtRangeUp, 510, "")
axis.SetLabelFont(43)
axis.SetLabelSize(18)
axis.Draw()
pad2.cd()
hrup.GetYaxis().SetRangeUser(sysRangeDown, sysRangeUp)
hrup.Draw("p")
hrdw.Draw("psame")


#-----------------------------------------------------#
#-----------------------------------------------------#
from ROOT import gROOT
gROOT.GetListOfCanvases().Draw()

#-----------------------------------------------------#
pad1.cd()
leg = ROOT.TLegend( 0.66, 0.63, 0.84, 0.88 )
leg.SetFillColor(0)
leg.SetLineColor(0)
leg.AddEntry(h, "t#bar{t} (central value)", "L")
leg.AddEntry(hup, "t#bar{t} sys up (+1#sigma)", "L")
leg.AddEntry(hdw, "t#bar{t} sys down (-1#sigma)", "L")
leg.AddEntry(h_st, "single top", "L")
leg.AddEntry(h_vj, "V+jets", "L")
leg.AddEntry(h_qcd, "QCD", "L")
leg.Draw()


#-----------------------------------------------------#
pad1.cd()
linedely1_pad1 = ROOT.TLine(linedely[0], 0, linedely[0], evtRangeUp-5000)
linedely2_pad1 = ROOT.TLine(linedely[1], 0, linedely[1], evtRangeUp-5000)
linedely1_pad1.SetLineWidth(3)
linedely2_pad1.SetLineWidth(3)
#linedely1_pad1.SetLineColor(30)
#linedely2_pad1.SetLineColor(30)
linedely1_pad1.SetLineStyle(2)
linedely2_pad1.SetLineStyle(2)
linedely1_pad1.Draw()
linedely2_pad1.Draw()

pad2.cd()
linedely1_pad2 = ROOT.TLine(linedely[0], sysRangeDown, linedely[0], sysRangeUp)
linedely2_pad2 = ROOT.TLine(linedely[1], sysRangeDown, linedely[1], sysRangeUp)
linedely1_pad2.SetLineWidth(3)
linedely2_pad2.SetLineWidth(3)
#linedely1_pad2.SetLineColor(30)
#linedely2_pad2.SetLineColor(30)
linedely1_pad2.SetLineStyle(2)
linedely2_pad2.SetLineStyle(2)
linedely1_pad2.Draw()
linedely2_pad2.Draw()

pad1.cd()
cmstext()
systext()
delytext(linedely[0]-1.5, linedely[1]-1.5, linedely[2]-1.5, evtRangeUp-3000)

#-----------------------------------------------------#
if (SavePlots):
	c.SaveAs("./SYSTEMPLATES/%s/plot_%s.pdf" %(sys.argv[1],sys.argv[2]))



