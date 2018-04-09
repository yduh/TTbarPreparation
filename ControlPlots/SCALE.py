from ROOT import TFile, TH1D, TH2D, TCanvas, TLegend
import ROOT

info = {}
cfile = file('SCALE.cfg')
#cfile = file('SCALE_36.3fb.cfg')
#cfile = file('SCALE_19.3fb.cfg')
#cfile = file('SCALE_2.3fb.cfg')

for line in cfile:
	line = line.split('#')[0]
	line = line.split('=')
	if(len(line) != 2):
		continue
	par = line[0].replace(' ', '')
	val = line[1].replace(' ', '')
	info[par] = val


lumi = float(info['lumi'])
lumierr = float(info['lumierr'])
#ttmadgraph = 806./21587302.*lumi
#ttpowheg = 806./18964323.*lumi
#ttamcatnlo = 806./7915468.*lumi
#DYscale = lumi*6024./2499142.
#Wscale = lumi*61524./10017462.
#Tscale = lumi*35.6/986100.
#Tbarscale = lumi*35.6/971800.
#TTscale = ttmadgraph

ttpowheg = lumi * float(info['tt_xsec'])/float(info['tt_PowhegP8_W'])
ttamcatnlo = lumi * float(info['tt_xsec'])/float(info['tt_aMCatNLO_W'])
ttpowheghpp = lumi * float(info['tt_xsec'])/float(info['tt_PowhegHpp_W'])
ttmadgraph = lumi * float(info['tt_xsec'])/float(info['tt_Madgraph_W'])
ttpowheg_mtup = lumi * float(info['tt_xsec_mtup'])/float(info['tt_mtop1735_PowhegP8_W'])
ttpowheg_mtdown = lumi * float(info['tt_xsec_mtdown'])/float(info['tt_mtop1715_PowhegP8_W'])
ttpowheg_mtnewup = lumi * float(info['tt_xsec_mtup'])/float(info['tt_mtop1735new_PowhegP8_W'])
ttpowheg_mtnewdown = lumi * float(info['tt_xsec_mtdown'])/float(info['tt_mtop1715new_PowhegP8_W'])
ttpowheg_mtoldup = lumi * float(info['tt_xsec_mtup'])/float(info['tt_mtop1735old_PowhegP8_W'])
ttpowheg_mtolddown = lumi * float(info['tt_xsec_mtdown'])/float(info['tt_mtop1715old_PowhegP8_W'])
ttpowheg_mtup3 = lumi * float(info['tt_xsec_mtup3'])/float(info['tt_mtop1755_PowhegP8_W'])
ttpowheg_mtdown3 = lumi * float(info['tt_xsec_mtdown3'])/float(info['tt_mtop1695_PowhegP8_W'])
ttpowheg_isrup = lumi * float(info['tt_xsec'])/float(info['tt_isrup_PowhegP8_W'])
ttpowheg_isrdown = lumi * float(info['tt_xsec'])/float(info['tt_isrdown_PowhegP8_W'])
ttpowheg_fsrup = lumi * float(info['tt_xsec'])/float(info['tt_fsrup_PowhegP8_W'])
ttpowheg_fsrdown = lumi * float(info['tt_xsec'])/float(info['tt_fsrdown_PowhegP8_W'])
ttpowheg_tuneup = lumi * float(info['tt_xsec'])/float(info['tt_tuneup_PowhegP8_W'])
ttpowheg_tunedown = lumi * float(info['tt_xsec'])/float(info['tt_tunedown_PowhegP8_W'])
ttpowheg_hdup = lumi * float(info['tt_xsec'])/float(info['tt_hdup_PowhegP8_W'])
ttpowheg_hddown = lumi * float(info['tt_xsec'])/float(info['tt_hddown_PowhegP8_W'])
ttpowheg_erdon = lumi * float(info['tt_xsec'])/float(info['tt_erdon_PowhegP8_W'])

#STtscale = lumi * float(info['STt_xsec'])/float(info['STt_W'])
STtopscale = lumi * float(info['STt_top_xsec'])/float(info['STt_top_W'])
STtopbarscale = lumi * float(info['STt_topbar_xsec'])/float(info['STt_topbar_W'])
WTscale = lumi * float(info['Wt_xsec'])/float(info['Wt_W'])
WTbarscale = lumi * float(info['Wtbar_xsec'])/float(info['Wtbar_W'])

STtopscale_psup = lumi * float(info['STt_top_xsec'])/float(info['STt_top_psup_W'])
STtopscale_psdown = lumi * float(info['STt_top_xsec'])/float(info['STt_top_psdown_W'])
STtopbarscale_psup = lumi * float(info['STt_topbar_xsec'])/float(info['STt_topbar_psup_W'])
STtopbarscale_psdown = lumi * float(info['STt_topbar_xsec'])/float(info['STt_topbar_psdown_W'])

WTscale_fsrdown = lumi * float(info['Wt_xsec'])/float(info['Wt_fsrdown_W'])
WTscale_isrdown = lumi * float(info['Wt_xsec'])/float(info['Wt_isrdown_W'])
WTbarscale_fsrdown = lumi * float(info['Wtbar_xsec'])/float(info['Wtbar_fsrdown_W'])
WTbarscale_isrdown = lumi * float(info['Wtbar_xsec'])/float(info['Wtbar_isrdown_W'])

DYscale = lumi * float(info['DYJets_xsec'])/float(info['DYJets_W'])
Wscale = lumi * float(info['WJets_xsec'])/float(info['WJets_W'])
W1scale = lumi * float(info['W1Jets_xsec'])/float(info['W1Jets_W'])
W2scale = lumi * float(info['W2Jets_xsec'])/float(info['W2Jets_W'])
W3scale = lumi * float(info['W3Jets_xsec'])/float(info['W3Jets_W'])
W4scale = lumi * float(info['W4Jets_xsec'])/float(info['W4Jets_W'])
WWscale = lumi * float(info['WW_xsec'])/float(info['WW_W'])
WZscale = lumi * float(info['WZ_xsec'])/float(info['WZ_W'])


#QCDMu15scale = lumi * float(info['QCDMu15_xsec'])/float(info['QCDMu15_W'])
#QCDMu30scale = lumi * float(info['QCDMu30_xsec'])/float(info['QCDMu30_W']) #commet by me
QCDMu50scale = lumi * float(info['QCDMu50_xsec'])/float(info['QCDMu50_W'])
QCDMu80scale = lumi * float(info['QCDMu80_xsec'])/float(info['QCDMu80_W'])
QCDMu120scale = lumi * float(info['QCDMu120_xsec'])/float(info['QCDMu120_W'])
QCDMu170scale = lumi * float(info['QCDMu170_xsec'])/float(info['QCDMu170_W'])
QCDMu300scale = lumi * float(info['QCDMu300_xsec'])/float(info['QCDMu300_W'])
QCDMu470scale = lumi * float(info['QCDMu470_xsec'])/float(info['QCDMu470_W'])
QCDMu600scale = lumi * float(info['QCDMu600_xsec'])/float(info['QCDMu600_W'])
QCDMu800scale = lumi * float(info['QCDMu800_xsec'])/float(info['QCDMu800_W'])
QCDMu1000scale = lumi * float(info['QCDMu1000_xsec'])/float(info['QCDMu1000_W'])
QCDMuInfscale = lumi * float(info['QCDMuInf_xsec'])/float(info['QCDMuInf_W'])
QCDEM50scale = lumi * float(info['QCDEM50_xsec'])/float(info['QCDEM50_W'])
QCDEM80scale = lumi * float(info['QCDEM80_xsec'])/float(info['QCDEM80_W'])
QCDEM120scale = lumi * float(info['QCDEM120_xsec'])/float(info['QCDEM120_W'])
QCDEM170scale = lumi * float(info['QCDEM170_xsec'])/float(info['QCDEM170_W'])
QCDEM300scale = lumi * float(info['QCDEM300_xsec'])/float(info['QCDEM300_W'])
QCDEMInfscale = lumi * float(info['QCDEMInf_xsec'])/float(info['QCDEMInf_W'])
TTscale = ttpowheg


uncnames = {}
uncnames['topmass'] = 'top mass'
uncnames['jet'] = 'jet energy scale'
uncnames['jetsmear'] = 'jet energy resolution'
uncnames['met'] = '\MET'
uncnames['scale'] = 'parton shower'
uncnames['rs'] = 'renormalization scale'
uncnames['fs'] = 'factorization scale'
uncnames['pdf'] = 'PDF'
uncnames['bkg'] = 'background'
uncnames['hpp'] = 'hadronization'
uncnames['btag'] = 'b-tagging'

rylabels = {}
rylabels['tpt'] = "#frac{1}{#sigma}#frac{d#sigma}{dp_{T}(t)} [GeV^{-1}]"
rylabels['ty'] = "#frac{1}{#sigma}#frac{d#sigma}{dy(t)}"
rylabels['thadpt'] = "#frac{1}{#sigma}#frac{d#sigma}{dp_{T}(t_{h})} [GeV^{-1}]"
rylabels['thady'] = "#frac{1}{#sigma}#frac{d#sigma}{dy(t_{h})}"
rylabels['tleppt'] = "#frac{1}{#sigma}#frac{d#sigma}{dp_{T}(t_{l})} [GeV^{-1}]"
rylabels['tlepy'] = "#frac{1}{#sigma}#frac{d#sigma}{dy(t_{l})}"
rylabels['ttpt'] = "#frac{1}{#sigma}#frac{d#sigma}{dp_{T}(t#bar{t})} [GeV^{-1}]"
rylabels['tty'] = "#frac{1}{#sigma}#frac{d#sigma}{dy(t#bar{t})}"
rylabels['ttm'] = "#frac{1}{#sigma}#frac{d#sigma}{dm(t#bar{t})} [GeV^{-1}]"
rylabels['njet'] = "#frac{1}{#sigma}#frac{d#sigma}{d n-jet}"

texylabels = {}
texylabels['tpt'] = r"\frac{1}{\sigma}\frac{d\sigma}{d\pt(\tq)} [\mathrm{GeV}^{-1}]"
texylabels['ty'] = r"\frac{1}{\sigma}\frac{d\sigma}{dy(\tq)}"
texylabels['thadpt'] = r"\frac{1}{\sigma}\frac{d\sigma}{d\pt(\tq_{h})} [\mathrm{GeV}^{-1}]"
texylabels['thady'] = r"\frac{1}{\sigma}\frac{d\sigma}{dy(\tq_{h})}"
texylabels['tleppt'] = r"\frac{1}{\sigma}\frac{d\sigma}{d\pt(\tq_{l})} [\mathrm{GeV}^{-1}]"
texylabels['tlepy'] = r"\frac{1}{\sigma}\frac{d\sigma}{dy(\tq_{l})}"
texylabels['ttpt'] = r"\frac{1}{\sigma}\frac{d\sigma}{d\pt(\ttb)} [\mathrm{GeV}^{-1}]"
texylabels['tty'] = r"\frac{1}{\sigma}\frac{d\sigma}{dy(\ttb)}"
texylabels['ttm'] = r"\frac{1}{\sigma}\frac{d\sigma}{dm(\ttb)} [\mathrm{GeV}^{-1}]"
texylabels['njet'] = r"\frac{1}{\sigma}\frac{d\sigma}{d\mathrm{n-jet}}"


rabsylabels = {}
rabsylabels['tpt'] = "#frac{d#sigma}{dp_{T}(t)} [pb GeV^{-1}]"
rabsylabels['ty'] = "#frac{d#sigma}{dy(t)} [pb]"
rabsylabels['thadpt'] = "#frac{d#sigma}{dp_{T}(t_{h})} [pb GeV^{-1}]"
rabsylabels['thady'] = "#frac{d#sigma}{dy(t_{h})} [pb]"
rabsylabels['tleppt'] = "#frac{d#sigma}{dp_{T}(t_{l})[pb]} [pb GeV^{-1}]"
rabsylabels['tlepy'] = "#frac{d#sigma}{dy(t_{l})} [pb]"
rabsylabels['ttpt'] = "#frac{d#sigma}{dp_{T}(t#bar{t})} [pb GeV^{-1}]"
rabsylabels['tty'] = "#frac{d#sigma}{dy(t#bar{t})} [pb]"
rabsylabels['ttm'] = "#frac{d#sigma}{dm(t#bar{t})} [pb GeV^{-1}]"
rabsylabels['nobin'] = "#sigma [pb]"
rabsylabels['njet'] = "#frac{d#sigma}{d n-jet}"

texabsylabels = {}
texabsylabels['tpt'] = r"\frac{d\sigma}{d\pt(\tq)} [\mathrm{\mathrm{pb}\,GeV}^{-1}]"
texabsylabels['ty'] = r"\frac{d\sigma}{dy(\tq)} [\mathrm{pb}]"
texabsylabels['thadpt'] = r"\frac{d\sigma}{d\pt(\tq_{h})} [\mathrm{\mathrm{pb}\,GeV}^{-1}]"
texabsylabels['thady'] = r"\frac{d\sigma}{dy(\tq_{h})} [\mathrm{pb}]"
texabsylabels['tleppt'] = r"\frac{d\sigma}{d\pt(\tq_{l})[\mathrm{pb}]} [\mathrm{pb\,GeV}^{-1}]"
texabsylabels['tlepy'] = r"\frac{d\sigma}{dy(\tq_{l})} [\mathrm{pb}]"
texabsylabels['ttpt'] = r"\frac{d\sigma}{d\pt(\ttb)} [\mathrm{\mathrm{pb}\,GeV}^{-1}]"
texabsylabels['tty'] = r"\frac{d\sigma}{dy(\ttb)} [\mathrm{pb}]"
texabsylabels['ttm'] = r"\frac{d\sigma}{dm(\ttb)} [\mathrm{\mathrm{pb}\,GeV}^{-1}]"
texabsylabels['nobin'] = r"\sigma [\mathrm{pb}]"
texabsylabels['njet'] = r"\frac{d\sigma}{d \mathrm{n-jet}}"


rxlabels= {}
rxlabels['ttm'] = 'm(t#bar{t})'
rxlabels['ttpt'] = 'p_{T}(t#bar{t})'
rxlabels['tty'] = 'y(t#bar{t})'
rxlabels['tpt'] = 'p_{T}(t)'
rxlabels['ty'] = 'y(t)'
rxlabels['thadpt'] = 'p_{T}(t_{h})'
rxlabels['thady'] = 'y(t_{h})'
rxlabels['tleppt'] = 'p_{T}(t_{l})'
rxlabels['tlepy'] = 'y(t_{l})'

texxlabels = {}
texxlabels['tpt'] = r"\pt(\tq) [\mathrm{GeV}]"
texxlabels['ty'] = r"y(\tq)"
texxlabels['thadpt'] = r"\pt(\tq_h) [\mathrm{GeV}]"
texxlabels['thady'] = r"y(\tq_h)"
texxlabels['tleppt'] = r"\pt(\tq_l) [\mathrm{GeV}]"
texxlabels['tlepy'] = r"y(\tq_l)"
texxlabels['ttpt'] = r"\pt(\ttb) [\mathrm{GeV}]"
texxlabels['tty'] = r"y(\ttb)"
texxlabels['ttm'] = r"m(\ttb) [\mathrm{GeV}]"
texxlabels['njet'] = r"\mathrm{n-jet}"


units = {}
units['ttm'] = r'GeV'
units['ttpt'] = r'GeV'
units['tty'] = r''
units['thadpt'] = r'GeV'
units['thadeta'] = r''
units['tleppt'] = r'GeV'
units['tlepeta'] = r''

def getLabel(name):
	for key, label in labels.iteritems():
		if key in name:
			return label
	return('')

def getUnit(name):
	for key, label in units.iteritems():
		if key in name:
			return label
	return('')

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetHistLineWidth(3)
ROOT.gStyle.SetPadRightMargin(0.05);
cana = 0
def plotunc(typ, name, htruth, hcen, hdown, hup, lgh = ''):
	global cana
	cana = TCanvas('cana')
	htruth.Draw()
	MIN = 1000000.
	MAX = 0.
	for b in range(1, htruth.GetNbinsX()+1):
		bmin = min(htruth.GetBinContent(b), hcen.GetBinContent(b), hdown.GetBinContent(b), hup.GetBinContent(b))
		bmax = max(htruth.GetBinContent(b), hcen.GetBinContent(b), hdown.GetBinContent(b), hup.GetBinContent(b))
		MIN = min(bmin, MIN)
		MAX = max(bmax, MAX)

	htruth.GetYaxis().SetRangeUser(MIN*.8, MAX*1.2)
	htruth.SetLineColor(ROOT.kGreen-2)
	htruth.SetLineWidth(6)
	hcen.SetMarkerStyle(20)
	hcen.SetMarkerSize(2)
	hcen.SetLineColor(ROOT.kBlack)
	hcen.Draw('same')
	hup.Draw('samehist')
	hdown.Draw('samehist')
	lg = cana.BuildLegend(0.7, 0.7, 0.9, 0.94)
	lg.SetHeader(lgh)
	lg.SetBorderSize(0)
	lg.SetFillStyle(0)
	cana.SaveAs('PLOTS/'+typ+'_unfolded_'+name+'.pdf')
	cana.SaveAs('PLOTS/'+typ+'_unfolded_'+name+'.png')

def writeuncertainty(hcen, hup, hdown, typ, dist):
	outfile = TFile('UNCERTAINTIES/'+typ + '_' + dist + '.root', 'recreate')

	hcentral = TH1D(hcen)
	hcentral.SetName('cen_xsec')
	huncstat = TH1D(hcen)
	huncstat.SetName('ERR_stat')
	huncstatrel = TH1D(hcen)
	huncstatrel.SetName('ERRrel_stat')
	hunc = TH1D(hcen)
	hunc.SetName('ERR_max')
	huncrel = TH1D(hcen)
	huncrel.SetName('ERRrel_max')
	huncup = TH1D(hcen)
	huncup.SetName('ERR_up')
	huncuprel = TH1D(hcen)
	huncuprel.SetName('ERRrel_up')
	huncdown = TH1D(hcen)
	huncdown.SetName('ERR_down')
	huncdownrel = TH1D(hcen)
	huncdownrel.SetName('ERRrel_down')
	for b in range(1, hcen.GetNbinsX()+1):
		huncstat.SetBinContent(b, hcen.GetBinError(b))
		huncstatrel.SetBinContent(b, hcen.GetBinError(b)/hcen.GetBinContent(b))
		hunc.SetBinContent(b, max(abs(hup.GetBinContent(b)-hcen.GetBinContent(b)), abs(hdown.GetBinContent(b)-hcen.GetBinContent(b))))
		huncrel.SetBinContent(b, max(abs(hup.GetBinContent(b)-hcen.GetBinContent(b)), abs(hdown.GetBinContent(b)-hcen.GetBinContent(b)))/hcen.GetBinContent(b))
		huncup.SetBinContent(b, hup.GetBinContent(b)-hcen.GetBinContent(b))
		huncuprel.SetBinContent(b, (hup.GetBinContent(b)-hcen.GetBinContent(b))/hcen.GetBinContent(b))
		huncdown.SetBinContent(b, hdown.GetBinContent(b)-hcen.GetBinContent(b))
		huncdownrel.SetBinContent(b, (hdown.GetBinContent(b)-hcen.GetBinContent(b))/hcen.GetBinContent(b))
		hunc.SetBinError(b, 0.00001)
		huncrel.SetBinError(b, 0.00001)
		huncup.SetBinError(b, 0.00001)
		huncuprel.SetBinError(b, 0.00001)
		huncdown.SetBinError(b, 0.00001)
		huncdownrel.SetBinError(b, 0.00001)
		huncstat.SetBinError(b, 0.00001)
		huncstatrel.SetBinError(b, 0.00001)

	outfile.Write()
	outfile.Close()

