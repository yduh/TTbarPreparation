#!/usr/bin/python
import ROOT as r
import sys, os
from array import array
from math import sqrt

njets = sys.argv[1]
CASE_DER = True
CASE_GTBASE = False
nominal = "noEW" if CASE_DER else "1.0y"
print "nominal = ", nominal

txt = open('/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/URStatTools/yiting/%s/qua.txt' %njets, 'w+')
txtUp = open('/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/URStatTools/yiting/%s/quaUp.txt' %njets, 'w+')
txtDw = open('/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/URStatTools/yiting/%s/quaDw.txt' %njets, 'w+')
#txt = open('/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/URStatTools/tt/SR/%s/qua.txt' %njets, 'w+')
path = "/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/GenericModel/couplingmodels/%s/parabola_2d/" %njets
kint = "mtt_dely_RECO"
#GT = ['5.0y','4.0y','3.0y','2.0y','1.0y','0.0y','1.0y','2.0y','3.0y','4.0y','5.0y']
GT = ['0.0y','1.0y','2.0y','3.0y','4.0y','5.0y',nominal] #put nominal in the last element

if njets == "3j":
	color = '8'
elif njets == "4j":
	color = '1'
elif njets == "5j":
	color = '4'
elif njets == "6j":
	color = '2'

f = r.TFile(path+"ch%s_gt.root" %njets)
hlist = []
testDict = {}
for gt in GT:
	h = f.Get(kint+"_"+gt)
	hlist.append(h)
	testList = []
	for ibin in range(h.GetNbinsX()):
		testList.append(h.GetBinContent(ibin+1))
	print "testList = ", testList
	testDict[ibin] = testList[ibin]

BinsScale = {}
errBinsScale = {}
cout = 0
for i in range(hlist[-1].GetXaxis().GetNbins()):
	BinsScale[i] = []
	errBinsScale[i] = []
	for h in hlist[0:-1]:
		#for h in hlist:
		if(CASE_GTBASE):
			BinsScale[i].append(h.GetBinContent(i+1)/hlist[-1].GetBinContent(i+1))
			errBinsScale[i].append((pow(sqrt(h.GetBinContent(i+1))/h.GetBinContent(i+1),2) + pow(sqrt(hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1), 2)) * h.GetBinContent(i+1)/hlist[-1].GetBinContent(i+1))
			print "bin",i+1,": ",h.GetBinContent(i+1),"/",hlist[-1].GetBinContent(i+1),"=",h.GetBinContent(i+1)/hlist[-1].GetBinContent(i+1)
		if(CASE_DER):
			BinsScale[i].append((h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1))
			errBinsScale[i].append((pow(sqrt(abs(h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1)))/(h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1)),2) + pow(sqrt(hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1), 2)) * (h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1))
			#BinsScale[i].append(h.GetBinContent(i+1)/hlist[-1].GetBinContent(i+1))
			#errBinsScale[i].append((pow(sqrt(h.GetBinContent(i+1))/h.GetBinContent(i+1),2) + pow(sqrt(hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1), 2)) * h.GetBinContent(i+1)/hlist[-1].GetBinContent(i+1))
			print "bin",i+1,": ",h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1),"/",hlist[-1].GetBinContent(i+1),"=",(h.GetBinContent(i+1)-hlist[-1].GetBinContent(i+1))/hlist[-1].GetBinContent(i+1)

print BinsScale
#print errBinsScale
outfile = r.TFile(path+"signal_proc_ch"+njets+".root", "RECREATE")
#print hlist[-1].GetXaxis().GetNbins()
for i in range(hlist[-1].GetXaxis().GetNbins()):
	if(BinsScale[i][1]) == -1: #for the case of no-entry bins
		cout += 1
		continue
	#print cout
	gtmin = eval(GT[0].split('y')[0]) if len(GT)==len(set(GT)) else -eval(GT[0].split('y')[0])
	gtmax = eval(GT[-2].split('y')[0])
	fitfun = "(1-[0]-[1])+[1]*x+[0]*x*x" if CASE_GTBASE else "[2]+[1]*x+[0]*x*x"
	p = r.TH1D("bin_content_par1_%d" %(i+1-cout), "parabola%d" %(i+1-cout), len(GT)-1, gtmin-0.5, gtmax+0.5)
	pfit = r.TF1("bin_content_par1_%d" %(i+1-cout), fitfun, gtmin-2.0, gtmax+2.0) #+-2 is a random extendsion number
	gfit = r.TF1("parabola%d" %(i+1-cout), fitfun, gtmin-2.0, gtmax+2.0)
	#pfit = r.TF1("bin_content_par1_%d" %(i+1-cout), "[2]+[1]*x+[0]*x*x", -5, 5)
	#gfit = r.TF1("parabola%d" %(i+1-cout), "[2]+[1]*x+[0]*x*x", -5, 5)

	x = []
	y = []
	erry = []
	for j in range(0, len(GT)-1, 1):
		p.SetBinContent(j+1, BinsScale[i][j])
		x.append(j-GT.index("0.0y"))
		y.append(BinsScale[i][j])
		erry.append(errBinsScale[i][j])
	#p.Write()
	gr = r.TGraphErrors(len(x), array("d", x), array("d", y), array("d", [0.0001]*len(x)), array("d", [0.0001]*len(x)))
	#gr = r.TGraphErrors(len(x), array("d", x), array("d", y), array("d", [0.0001]*len(x)), array("d", erry))
	#gr = r.TGraph(len(x), array("d", x), array("d", y))

	p.Fit(pfit, "q")
	pfit.SetParameters(pfit.GetParameter(0), pfit.GetParameter(1))
	#pfit.SetParameters(pfit.GetParameter(0), pfit.GetParameter(1), pfit.GetParameter(2))
	pfit.Write()

	gfit.SetLineColor(int(color))
	gr.SetLineColor(int(color))
	gr.SetMarkerColor(int(color))
	gr.Fit(gfit, "q")
	gr.Draw("AC*")
	gr.Write() #comment it if you want it clean! uncomment it if you want to check the fit quickly
	p0 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParameter(0)
	p1 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParameter(1)
	e0 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParError(0)
	e1 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParError(1)
	if(CASE_GTBASE):
		#print i+1-cout,p0,p1,1-p0-p1
		#print >> txt, '%s+1-%s,%s,%s,1-%s-%s' %(i,cout,p0,p1,p0,p1)
		txt.write('%s %s %s %s\n' %(i+1-cout,p0,p1,1-p0-p1))
		txtUp.write('%s %s %s %s\n' %(i+1-cout,p0+e0,p1+e1,1-(p0+e0)-(p1-e1)))
		txtDw.write('%s %s %s %s\n' %(i+1-cout,p0-e0,p1-e1,1-(p0-e0)-(p1-e1)))
	else:
		p2 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParameter(2)
		e2 = gr.GetFunction("parabola%d" %(i+1-cout)).GetParError(2)
		#print i+1-cout, p0, p1, p2
		txt.write('%s %s %s %s\n' %(i+1-cout,p0,p1,p2))
		txtUp.write('%s %s %s %s\n' %(i+1-cout,p0+e0,p1+e1,p2+e2))
		txtDw.write('%s %s %s %s\n' %(i+1-cout,p0-e0,p1-e1,p2-e2))

outfile.Close()

os.system("cp %s/parabola_2d/ch%s_gt.root /afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/URStatTools/yiting/%s/" %(njets,njets,njets))
