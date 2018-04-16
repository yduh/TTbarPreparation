import ROOT as r
import math, sys

njets = sys.argv[1]

readin_data = r.TFile("%s/skimrootSB/skim_DATA.root" %njets)
readin_tt = r.TFile("%s/skimrootSB/skim_tt_PowhegP8_noEW.root" %njets)
readin_st = r.TFile("%s/skimrootSB/skim_t.root" %njets)
readin_vj = r.TFile("%s/skimrootSB/skim_Vj.root" %njets)
readin_qcd = r.TFile("%s/skimrootSB/skim_QCD.root" %njets)

hdata = readin_data.Get("mtt_RECO").Rebin(100)
htt = readin_tt.Get("mtt_RECO").Rebin(100)
hst = readin_st.Get("mtt_RECO").Rebin(100)
hvj = readin_vj.Get("mtt_RECO").Rebin(100)
hqcd = readin_qcd.Get("mtt_RECO").Rebin(100)

Ndata = hdata.GetBinContent(1)
Ntt = htt.GetBinContent(1)
Nst = hst.GetBinContent(1)
Nvj = hvj.GetBinContent(1)
Nqcd = hqcd.GetBinContent(1)

Edata = hdata.GetBinError(1)
Ett = htt.GetBinError(1)
Est = hst.GetBinError(1)
Evj = hvj.GetBinError(1)
Eqcd = hqcd.GetBinError(1)

hsum = htt.Clone()
hsum.Add(hst)
hsum.Add(hvj)
hsum.Add(hqcd)
Nsum = Ntt + Nst + Nvj + Nqcd
Esum = hsum.GetBinError(1)

print 'tt right', round(Ntt, 1), '\pm', round(Ett, 1), '\\\\'
print '\hline'
print 'single t', round(Nst, 1), '\pm', round(Est, 1), '\\\\'
print 'V+jets', round(Nvj, 1), '\pm', round(Evj, 1), '\\\\'
print 'QCD', round(Nqcd, 1), '\pm', round(Eqcd, 1), '\\\\'
print 'MC sum', round(Nsum, 1), '\pm', round(Esum, 1), '\\\\'
print '\hline\hline'
print 'data', round(Ndata, 1), '\pm', round(Edata, 1)

print 'V+jets QCD', round(Nvj+Nqcd, 1)
