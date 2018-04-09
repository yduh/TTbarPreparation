#!/usr/bin/python

from array import array
import ROOT as r
import sys
#from math import abs

mttList_precise = []
mttList_ew = []
mttList = []
XSList_precise = []
XSList = []
XSerrdList = []
XSerruList = []
XSerrdList_precise = []
XSerruList_precise = []
kList = []
kerrdList = []
kerruList = []

filePath_precise = "txt/LHC13-PTavt-nnlo-MT2-NNPDF30.txt"
textFile_precise = open(filePath_precise, "r")
lines_precise = textFile_precise.readlines()
for line in lines_precise:
	mtt, xs, rsfsSSd, rsfsSSu, rsd, fsd, rsu, fsu, binsize = line.split()
	#diffList = [float(x)-float(xs) for x in line.split()[2:-1]]
	diffList = [float(x) for x in line.split()[2:-1]]
	print diffList
	mttList_precise.append(float(mtt))
	XSList_precise.append(float(xs)/float(binsize))
	#XSerrdList_precise.append((float(min(diffList))+float(xs))/float(binsize))
	#XSerruList_precise.append((float(max(diffList))+float(xs))/float(binsize))
	XSerrdList_precise.append(float(min(diffList))/float(binsize))
	XSerruList_precise.append(float(max(diffList))/float(binsize))

filePath = "txt/LHC13-PTavt-nlo-MT2-NNPDF30.txt"
textFile = open(filePath, "r")
lines = textFile.readlines()
for line in lines:
	mtt, xs, rsfsSSd, rsfeSSu, rsd, fsd, rsu, fsu, binsize = line.split()
	diffList = [float(x) for x in line.split()[2:-1]]
	mttList.append(float(mtt))
	XSList.append(float(xs)/float(binsize))
	XSerrdList.append(float(min(diffList))/float(binsize))
	XSerruList.append(float(max(diffList))/float(binsize))

filePath_ew = "txt/LHC13-PTavt-MT2-NNPDF30QED-phono.txt"
textFile_ew = open(filePath_ew, "r")
lines_ew = textFile_ew.readlines()
for line in lines_ew:
	mtt, xs, rsfsSSd, rsfsSSu, pdfd, pdfu, sysd, sysu, binsize, k = line.split()
	mttList_ew.append(float(mtt))
	kList.append(float(k))
	kerrdList.append(float(rsfsSSd)/float(xs)*float(k))
	kerruList.append(float(rsfsSSu)/float(xs)*float(k))
	#kerrdList.append((1-(float(xs)-float(sysd))/float(xs))*float(k))
	#kerruList.append(((float(sysu)-float(xs))/float(xs)+1)*float(k))
	#print ((1-(float(xs)-float(sysd))/float(xs))*float(k)), (((float(sysu)-float(xs))/float(xs)+1)*float(k))

if set(mttList_precise) != set(mttList):
	print "NOTICE!"
if set(mttList_ew) != set(mttList):
	print "NOTICE!"


c = r.TCanvas("c2", "c2", 1200, 400)
c.SetGrid()
c.Divide(2, 1)

c.cd(1)
gr_precise = r.TGraph(len(mttList_precise), array("d", mttList_precise), array("d", kList))
grerru_precise = r.TGraph(len(mttList_precise), array("d", mttList_precise), array("d", kerruList))
grerrd_precise = r.TGraph(len(mttList_precise), array("d", mttList_precise), array("d", kerrdList))

gr  = r.TGraph(len(mttList),  array("d", mttList),  array("d", kList))
gr.GetXaxis().SetRangeUser(0, 1000)
gr.GetYaxis().SetRangeUser(0.8, 1.3)
gr_precise.SetLineColor(r.kRed)
gr.SetLineColor(r.kBlue)
gr_precise.Draw("AC*")
grerru_precise.SetLineStyle(2)
grerrd_precise.SetLineStyle(2)
grerru_precise.Draw("C*SAME")
grerrd_precise.Draw("C*SAME")
gr.Draw("C*SAME")

c.cd(2)
ratioList = [(x/y)*z for x, y, z in zip(XSList_precise, XSList, kList)]
ratiouList = [(x/y)*z for x, y, z in zip(XSList_precise, XSerrdList, kerruList)]
ratiodList = [(x/y)*z for x, y, z in zip(XSList_precise, XSerruList, kerrdList)]

gr_ratio = r.TGraph(len(mttList_precise), array("d", mttList_precise), array("d", ratioList))
gr_ratiou = r.TGraph(len(mttList_precise), array("d", mttList_precise), array("d", ratiouList))
gr_ratiod = r.TGraph(len(mttList_precise), array("d", mttList_precise), array("d", ratiodList))
gr_ratio.GetXaxis().SetRangeUser(0, 1000)
gr_ratio.GetYaxis().SetRangeUser(0.8, 1.3)
gr_ratio.GetYaxis().SetTitleOffset(1.4)
gr_ratio.GetXaxis().SetTitle("Mtt")
gr_ratio.GetYaxis().SetTitle("NNLO/NLO* (QCDXEW)/QCD")
gr_ratio.SetTitle("d#sigma/dMtt")
gr_ratio.Draw("AL*")
gr_ratiou.SetLineStyle(2)
gr_ratiod.SetLineStyle(2)
gr_ratiou.Draw("L*SAME")
gr_ratiod.Draw("L*SAME")

c.SaveAs("reweighting.png")


##########################################################
weightList = []
weightuList = []
weightdList = []
fweight = r.TFile("nnloewweight.root", "RECREATE")
hweight = r.TH1D("nnloewweight", "nnlo", 500, 0, 1000)
hweightup = r.TH1D("nnloewweightup", "nnlo", 500, 0, 1000)
hweightdw = r.TH1D("nnloewweightdw", "nnlo", 500, 0, 1000)

for i in range(0, 1000+2, 2):
	weightList.append(gr_ratio.Eval(i))
	weightuList.append(gr_ratiou.Eval(i))
	weightdList.append(gr_ratiod.Eval(i))
for i in range(len(weightList)):
	hweight.SetBinContent(i+1, weightList[i])
	hweightup.SetBinContent(i+1, weightuList[i])
	hweightdw.SetBinContent(i+1, weightdList[i])

hweight.Write()
hweightup.Write()
hweightdw.Write()
fweight.Close()



##########################################################
'''
powhegList = []

powheg = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/totj/noEW/tt_PowhegP8.root")
#powheg = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/4junc/noEW/MCs/tt_mtop1735_PowhegP8.root")
hp = powheg.Get("YUKAWA_GEN/yukawa_Mtt")
#for ibin in hp.GetNbinsX():
hp.Rebin(20)
hp.Scale(832/hp.Integral())
#hp.Draw("same")
	#powhegList.append(hp.GetBinContent(ibin+1))


for ibin in range(hp.GetNbinsX()):
	print (ibin+1)*40, hp.GetBinContent(ibin+1)
	mttList2.append((ibin+1)*40)
	powhegList.append(hp.GetBinContent(ibin+1)/40)

gr2 = r.TGraph(len(mttList2), array("d", mttList2), array("d", powhegList))
gr2.SetLineColor(r.kBlue)
gr2.Draw("C*SAME")
'''


