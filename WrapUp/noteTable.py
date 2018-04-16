import ROOT as r
import math, sys

njets = sys.argv[1]

readin_data = r.TFile("%s/skimroot/skim_DATA.root" %njets)
readin_tt = r.TFile("%s/skimroot/skim_tt_PowhegP8_noEW.root" %njets)
readin_st = r.TFile("%s/skimroot/skim_t.root" %njets)
readin_vj = r.TFile("%s/skimroot/skim_Vj.root" %njets)
readin_qcd = r.TFile("%s/skimroot/skim_QCD.root" %njets)

hdata = readin_data.Get("mtt_RECO").Rebin(100)
htt_right = readin_tt.Get("mtt_right").Rebin(100)
htt_wrong = readin_tt.Get("mtt_wrong").Rebin(100)
htt_semi = readin_tt.Get("mtt_semi").Rebin(100)
htt_other = readin_tt.Get("mtt_other").Rebin(100)
hst = readin_st.Get("mtt_RECO").Rebin(100)
hvj = readin_vj.Get("mtt_RECO").Rebin(100)
hqcd = readin_qcd.Get("mtt_RECO").Rebin(100)

Ndata = hdata.GetBinContent(1)
Ntt_right = htt_right.GetBinContent(1)
Ntt_wrong = htt_wrong.GetBinContent(1)
Ntt_semi = htt_semi.GetBinContent(1)
Ntt_other = htt_other.GetBinContent(1)
Nst = hst.GetBinContent(1)
Nvj = hvj.GetBinContent(1)
Nqcd = hqcd.GetBinContent(1)

Edata = hdata.GetBinError(1)
Ett_right = htt_right.GetBinError(1)
Ett_wrong = htt_wrong.GetBinError(1)
Ett_semi = htt_semi.GetBinError(1)
Ett_other = htt_other.GetBinError(1)
Est = hst.GetBinError(1)
Evj = hvj.GetBinError(1)
Eqcd = hqcd.GetBinError(1)

hsum = htt_right.Clone()
hsum.Add(htt_wrong)
hsum.Add(htt_semi)
hsum.Add(htt_other)
hsum.Add(hst)
hsum.Add(hvj)
hsum.Add(hqcd)
Nsum = Ntt_right + Ntt_wrong + Ntt_semi + Ntt_other + Nst + Nvj + Nqcd
Esum = hsum.GetBinError(1)

print 'tt right', round(Ntt_right, 1), '\pm', round(Ett_right, 1), '\\\\'
print 'tt wrong', round(Ntt_wrong, 1), '\pm', round(Ett_wrong, 1), '\\\\'
print 'tt not reco', round(Ntt_semi, 1), '\pm', round(Ett_semi, 1), '\\\\'
print 'tt bck', round(Ntt_other, 1), '\pm', round(Ett_other, 1), '\\\\'
print '\hline'
print 'single t', round(Nst, 1), '\pm', round(Est, 1), '\\\\'
print 'V+jets', round(Nvj, 1), '\pm', round(Evj, 1), '\\\\'
print 'QCD', round(Nqcd, 1), '\pm', round(Eqcd, 1), '\\\\'
print 'MC sum', round(Nsum, 1), '\pm', round(Esum, 1), '\\\\'
print '\hline\hline'
print 'data', round(Ndata, 1), '\pm', round(Edata, 1)

print 'tt', round(Ntt_right+Ntt_wrong+Ntt_semi+Ntt_other, 1)
print 'V+jets QCD', round(Nvj+Nqcd, 1)
