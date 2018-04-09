#!/usr/bin/python
import ROOT

f3 = ROOT.TFile("3j/skim_pdf_noEW.root")
f4 = ROOT.TFile("4j/skim_pdf_noEW.root")
f5 = ROOT.TFile("5j/skim_pdf_noEW.root")
f6 = ROOT.TFile("6j/skim_pdf_noEW.root")
bin3 = f3.Get('cen').GetNbinsX()
bin4 = f4.Get('cen').GetNbinsX()
bin5 = f5.Get('cen').GetNbinsX()
bin6 = f6.Get('cen').GetNbinsX()

outfile = ROOT.TFile('3456j/skim_pdf_noEW.root', "RECREATE")

hcentral = ROOT.TH1D('cen', 'cen', bin3+bin4+bin5+bin6, 0, bin3+bin4+bin5+bin6)
for i3 in range(bin3):
	hcentral.SetBinContent(i3+1, f3.Get('cen').GetBinContent(i3+1))
for i4 in range(bin4):
	hcentral.SetBinContent(bin3+i4+1, f4.Get('cen').GetBinContent(i4+1))
for i5 in range(bin5):
	hcentral.SetBinContent(bin3+bin4+i5+1, f5.Get('cen').GetBinContent(i5+1))
for i6 in range(bin6):
	hcentral.SetBinContent(bin3+bin4+bin5+i6+1, f6.Get('cen').GetBinContent(i6+1))
hcentral.Write()

for p in range(10,110):
	hreplica = ROOT.TH1D('replica_'+str(p), 'replica_'+str(p), bin3+bin4+bin5+bin6, 0, bin3+bin4+bin5+bin6)
	for i3 in range(bin3):
		hreplica.SetBinContent(i3+1, f3.Get('replica_'+str(p)).GetBinContent(i3+1))
	for i4 in range(bin4):
		hreplica.SetBinContent(bin3+i4+1, f4.Get('replica_'+str(p)).GetBinContent(i4+1))
	for i5 in range(bin5):
		hreplica.SetBinContent(bin3+bin4+i5+1, f5.Get('replica_'+str(p)).GetBinContent(i5+1))
	for i6 in range(bin6):
		hreplica.SetBinContent(bin3+bin4+bin5+i6+1, f6.Get('replica_'+str(p)).GetBinContent(i6+1))
	hreplica.Write()


outfile.Close()


