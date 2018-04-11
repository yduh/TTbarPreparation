import ROOT as r
import sys,argparse,os
from math import sqrt
from array import array

r.gROOT.SetBatch(r.kTRUE)
r.gStyle.SetOptTitle(0)

parser = argparse.ArgumentParser()
parser.add_argument('--njets',action='store')
parser.add_argument('--var',action='store')
parser.add_argument('--fitFunc',action='store',default="linear")

option = parser.parse_args()

njets = option.njets
var = option.var
objs = []

def quad(*xs):
	return sqrt(sum(x*x for x in xs))

def fitOrthPoly(ratioHist,mcHist):
	histToFit = ratioHist.Clone()
	nBins = histToFit.GetXaxis().GetNbins()
	weightMeanNum = 0.
	weightMeanDem = 0.
	for ibin in range(1,nBins+1):
		ratio = ratioHist.GetBinContent(ibin)
		statUnc = ratioHist.GetBinError(ibin)
		pred = mcHist.GetBinContent(ibin)
		binCenter = mcHist.GetXaxis().GetBinCenter(ibin)
		histToFit.SetBinContent(ibin,ratio)
		histToFit.SetBinError(ibin,statUnc)
		weightMeanNum += binCenter*pred
		weightMeanDem += pred
	lowRange = mcHist.GetXaxis().GetBinCenter(1)
	highRange = mcHist.GetXaxis().GetBinCenter(nBins)
	orthPolyFunc = r.TF1("orthPoly","[0]+[1]*(x-{0})".format(weightMeanNum/weightMeanDem),lowRange,highRange)
	fitResult = histToFit.Fit(orthPolyFunc,"S")
	return fitResult,orthPolyFunc

def drawDataExcludeOthers(folder, name):
	fCR = r.TFile('../../%s/%s/skim_DATA.root' %(njets, folder))
	#f_tt = r.TFile('../../%s/%s/skim_tt_PowhegP8_%s.root' %(njets, folder, folder.split('_')[1] if folder != 'skimrootSB_new' else 'noEW'))
	f_tt = r.TFile('../../%s/%s/skim_tt_PowhegP8_%s.root' %(njets, folder, folder.split('_')[1]))
	f_st = r.TFile('../../%s/%s/skim_t.root' %(njets, folder))
	f_wj = r.TFile('../../%s/%s/skim_WnJets.root' %(njets, folder))
	f_dyj = r.TFile('../../%s/%s/skim_DYJets.root' %(njets, folder))
	f_ww = r.TFile('../../%s/%s/skim_WW.root' %(njets, folder))
	f_wz = r.TFile('../../%s/%s/skim_WZ.root' %(njets, folder))
	objs.append(fCR)
	objs.append(f_tt)
	objs.append(f_st)
	objs.append(f_wj)
	objs.append(f_dyj)
	objs.append(f_ww)
	objs.append(f_wz)

	binningX = [200, 300, 340, 380, 420, 460, 520, 720, 1000, 1200, 1500]
	binningY = [-6., -2.4, -1.2, -0.6, -0.3, 0., 0.3, 0.6, 1.2, 2.4, 6.]
	hxCR = fCR.Get('mtt_RECO').Rebin(len(binningX)-1,"mtt_RECOnew", array("d",binningX))
	hyCR = fCR.Get('dely_RECO').Rebin(len(binningY)-1,"dely_RECOnew", array("d",binningY))
	hx_tt = f_tt.Get('mtt_RECO').Rebin(len(binningX)-1,"mtt_RECOnew", array("d",binningX))
	hy_tt = f_tt.Get('dely_RECO').Rebin(len(binningY)-1,"dely_RECOnew", array("d",binningY))
	hx_st = f_st.Get('mtt_RECO').Rebin(len(binningX)-1,"mtt_RECOnew", array("d",binningX))
	hy_st = f_st.Get('dely_RECO').Rebin(len(binningY)-1,"dely_RECOnew", array("d",binningY))
	hx_wj = f_wj.Get('mtt_RECO').Rebin(len(binningX)-1,"mtt_RECOnew", array("d",binningX))
	hy_wj = f_wj.Get('dely_RECO').Rebin(len(binningY)-1,"dely_RECOnew", array("d",binningY))
	hx_dyj = f_dyj.Get('mtt_RECO').Rebin(len(binningX)-1,"mtt_RECOnew", array("d",binningX))
	hy_dyj = f_dyj.Get('dely_RECO').Rebin(len(binningY)-1,"dely_RECOnew", array("d",binningY))
	hx_ww = f_ww.Get('mtt_RECO').Rebin(len(binningX)-1,"mtt_RECOnew", array("d",binningX))
	hy_ww = f_ww.Get('dely_RECO').Rebin(len(binningY)-1,"dely_RECOnew", array("d",binningY))
	hx_wz = f_wz.Get('mtt_RECO').Rebin(len(binningX)-1,"mtt_RECOnew", array("d",binningX))
	hy_wz = f_wz.Get('dely_RECO').Rebin(len(binningY)-1,"dely_RECOnew", array("d",binningY))

	hx = hxCR.Clone(name+"_mtt")
	hx.Add(hx_tt, -1)
	hx.Add(hx_st, -1)
	hx.Add(hx_wj, -1)
	hx.Add(hx_dyj, -1)
	hx.Add(hx_ww, -1)
	hx.Add(hx_wz, -1)

	hy = hyCR.Clone(name+"_dely")
	hy.Add(hy_tt, -1)
	hy.Add(hy_st, -1)
	hy.Add(hy_wj, -1)
	hy.Add(hy_dyj, -1)
	hy.Add(hy_ww, -1)
	hy.Add(hy_wz, -1)

	med = int(hy.GetXaxis().GetNbins()/2)
	hyabs = r.TH1D('dely_RECO', 'dely_RECO', med, 0, 6)
	for ibin in range(med):
		hyabs.SetBinContent(ibin+1, hy.GetBinContent(med-ibin)+hy.GetBinContent(med+ibin+1))
		hyabs.SetBinError(ibin+1, quad(hy.GetBinError(med-ibin),hy.GetBinError(med+ibin+1)))


	hx.Scale(1./hx.Integral())
	hy.Scale(1./hy.Integral())
	hyabs.Scale(1./hyabs.Integral())

	#hx.SetLineColor(color)
	if var == "mtt":
		hx.GetXaxis().SetTitle('M(t#bar{t})')
		return hx
	elif var == "dely":
		hy.GetXaxis().SetTitle('#Deltay')
		return hy
	elif var == "absdely":
		hyabs.GetXaxis().SetTitle('|#Deltay|')
		return hyabs

#h1 = drawDataExcludeOthers('skimrootSB_new', 1, 'nominal')
#h2 = drawDataExcludeOthers('skimrootSB_CSVUp', 2, 'up')
#h3 = drawDataExcludeOthers('skimrootSB_CSVDown', 4, 'down')
h1 = drawDataExcludeOthers('skimroot_Aless0.3','A')
h2 = drawDataExcludeOthers('skimroot_B0.3to0.6','B')
h3 = drawDataExcludeOthers('skimroot_C0.6to0.8','C')

outputFile = r.TFile('./rootfiles/dataExcludedQCD_%s.root'%njets,'RECREATE')
h1.Write()
h2.Write()
h3.Write()

a2bRatio = h1.Clone("A2B_Ratio")
a2bRatio.Divide(h2)
a2bRatio.Write()
a2cRatio = h1.Clone("A2C_Ratio")
a2cRatio.Divide(h3)
a2cRatio.Write()
b2cRatio = h2.Clone("B2C_Ratio")
b2cRatio.Divide(h3)
b2cRatio.Write()

#if not os.path.exists(os.path.abspath(dirName)):
#	os.makedirs(dirName)
histList = [a2bRatio,a2cRatio,b2cRatio]
for hist in histList:
	hist.SetStats(0)
	hist.GetYaxis().SetRangeUser(0.,3.)

a2bRatio.GetYaxis().SetTitleOffset(1.3)
a2bRatio.GetYaxis().SetTitle("Shape comp A[0-0.3] to B[0.3-0.6]")

a2cRatio.GetYaxis().SetTitleOffset(1.3)
a2cRatio.GetYaxis().SetTitle("Shape comp A[0-0.3] to C[0.6-0.8]")

b2cRatio.GetYaxis().SetTitleOffset(1.3)
b2cRatio.GetYaxis().SetTitle('Shape comp B[0.3-0.6] to C[0.6-0.8]')

c = r.TCanvas('c1', 'c1', 1100, 400)
c.Divide(3, 1)
for i, h in enumerate(histList):
	c.cd(i+1)
	print i
	if option.fitFunc == "linear":
		h.Fit("pol1")
		h.Draw()
	elif option.fitFunc == "orthPoly":
		fitFunc,orthPolyFunc = fitOrthPoly(b2cRatio,h1)
		b2cRatio.Draw()
		orthPolyFunc.Draw("same")

	if option.fitFunc == "linear":
		h.Fit("pol1")
		fitFunc = h.GetFunction("pol1")
		print "chi2/nof for fit: ", fitFunc.GetChisquare()/fitFunc.GetNDF()
		print "p0 parameter: ", fitFunc.GetParameter(0)," pm ", fitFunc.GetParError(0)
		print "p1 parameter: ", fitFunc.GetParameter(1)," pm ", fitFunc.GetParError(1)
		text = r.TLatex()
		text.SetTextSize(0.04)
		text.SetNDC()
		text.DrawLatex(0.2,0.8,"chi2/nof: %4.2f"%float(fitFunc.GetChisquare()/fitFunc.GetNDF()))
		text.DrawLatex(0.2,0.7,"y-intercept: %4.2f #pm %4.2f"%(fitFunc.GetParameter(0),fitFunc.GetParError(0)))
		text.DrawLatex(0.2,0.6,"slope #times 100 GeV: %4.2f #pm %4.2f"%(fitFunc.GetParameter(1)*100,fitFunc.GetParError(1)*100))
		#text.DrawLatex(0.2,0.6,"slope: %4.2f #pm %4.2f"%(fitFunc.GetParameter(1),fitFunc.GetParError(1)))
	elif option.fitFunc == "orthPoly":
		print "Probf for fit: ", fitFunc.Prob()
		print "p0 parameter: ", fitFunc.Parameter(0)," pm ", fitFunc.ParError(0)
		print "p1 parameter: ", fitFunc.Parameter(1)," pm ", fitFunc.ParError(1)
		text = r.TLatex()
		text.SetTextSize(0.04)
		text.SetNDC()
		text.DrawLatex(0.2,0.8,"prob: %4.2f"%float(fitFunc.Prob()))
		text.DrawLatex(0.2,0.7,"p0: %4.2f #pm %4.2f"%(fitFunc.Parameter(0),fitFunc.ParError(0)))
		text.DrawLatex(0.2,0.6,"p1 #times 100 GeV: %4.2f #pm %4.2f"%(fitFunc.Parameter(1)*100,fitFunc.ParError(1)*100))
	fitFunc.Write()

c.SaveAs("./plots_qcd/RatioQCD_%s_%s.png" %(njets,var))

for obj in objs:
	obj.Close()
