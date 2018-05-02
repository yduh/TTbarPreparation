#!/usr/bin/python

class Info(object):
	def __init__(self,saveName,rebinFactors):
		self.saveName = saveName
		self.rebinFactors = rebinFactors
		self.hist = None

	def getHistDim(self):
		return len(self.rebinFactors)


class Varargs:
	DefaultVarDict = {	'_Mtt':		Info('mtt', [10]), #root file for mtt 2GeV/bin
						'_delY':		Info('dely',[60]), #root file for dely 0.01/bin
						'_Mtt_delY':	Info('mtt_dely',[10,60])
						}

	AddVarDict = {	'_MET':				Info('met', [5]),
					'_lep_eta':			Info('lepeta', [40]),
					'_tlep_pt':			Info('tlept', [20]),
					'_thad_pt':			Info('thadpt', [20]),
					'_tlep_y':			Info('tlepy', [10]),
					'_thad_y':			Info('thady', [10]),
					'_tt_pt':			Info('ttpt', [10]),
					'_tt_y':			Info('tty', [5]),
					'_deltar_lepj':		Info('lepjDeltar', [10]),
					'_deltar_lepj1':		Info('lepj1Deltar', [10]),
					'_deltar_lepj2':		Info('lepj2Deltar', [10]),
					'_deltar_lepj3':		Info('lepj3Deltar', [10]),
					'_deltaphi_metj':	Info('metjDeltaphi', [10]),
					'_deltaphi_metj1':	Info('metj1Deltaphi', [10]),
					'_deltaphi_metj2':	Info('metj2Deltaphi', [10]),
					'_deltaphi_metj3':	Info('metj3Deltaphi', [10]),
					'_ptj1':			Info('ptj1', [5]),
					'_ptj2':			Info('ptj2', [5]),
					'_ptj3':			Info('ptj3', [5]),
					'_deltar_lepj_deltaphi_metj':	Info('lepjDeltarmetjDeltaphi', [10,10]),
					'_MTwl':			Info('mtwl', [10]),
					'_thadM_right':		Info('thadMright', [5]),
					'_thadM_wrong':		Info('thadMwrong', [5]),
					'_nschi_right':		Info('nschiright', [3]),
					'_nschi_wrong':		Info('nschiwrong', [3]),
 					#'btag_high':	Info('btaghigh', [5]),
					#'btag_low':		Info('btaglow', [5])
					#'all_massnutest':Info('')
					}

class vararg1D:
	control_3j = '/3j_tt_y' #/3j_tlep_pt, /3j_thad_pt, /3j_tt_y, /3j_tlep_y, /3j_thad_y, /3j_MET, /3j_lep_eta, /3j_tt_pt, /3j_tt_y

	control = '/all_massnutest' #/all_tlep_pt, /all_thad_pt, /all_tt_y, /all_tlep_y, /all_thad_y, /all_MET, /all_lep_eta, /all_tt_pt, /all_tt_y, /all_massnutest

	folder_savename = 'massnutest'
	control_savename = 'RECO/all_massnutest' #tlept, thadpt, tty #please don't put something more than 2 layers
	#for 3j: 3j_RECO/3j_xxx ; for 4j up: RECO/all_xxx

	#control_binL = 0
	#control_binH = 800 #800, 5
