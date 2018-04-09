#!/usr/bin/python
import math
from SCALE import *

MappingScales = {}

MappingScales['DATA'] = 1

#(signal region MC)/(data sideband), using skim_Vj.root and skim_QCD.root, Integral() without 'width' option
#MappingScales['DATA_Tvj_3j'] =  float(14905.1530001/2408630.0) #(13927.4997442/2396202)
#MappingScales['DATA_Tqcd_3j'] = float(22621.9400356/2408630.0) #(23689.4405466/2396202)
##MappingScales['DATA_Tbck_3j'] = float(37527.0930357/2408630.0)
#MappingScales['DATA_Tbck_3j'] = 37527.0930357

#MappingScales['DATA_Tvj_4j'] =  float(2987.70656998/228010.0) #(2992.64584053/209916)
#MappingScales['DATA_Tqcd_4j'] = float(3141.70281535/228010.0) #(3691.65460399/209916)
##MappingScales['DATA_Tbck_4j'] = float(6129.40938533/228010.0)
#MappingScales['DATA_Tbck_4j'] = 6129.40938533

#MappingScales['DATA_Tvj_5j'] =  float(1665.10884402/70090.0) #(1300.55219812/65965)
#MappingScales['DATA_Tqcd_5j'] = float(603.734061775/70090.0) #(469.600310087/65965)
##MappingScales['DATA_Tbck_5j'] = float(2268.842905795/70090.0)
#MappingScales['DATA_Tbck_5j'] = 2268.842905795

#MappingScales['DATA_Tvj_6j'] =  float(884.635112789/20649.0) #(402.385968536/19558)
#MappingScales['DATA_Tqcd_6j'] = float(822.950611542/20649.0) #(541.349269386/19558)
##MappingScales['DATA_Tbck_6j'] = float(1707.5857243310002/20649.0)
#MappingScales['DATA_Tbck_6j'] = 1707.5857243310002



MappingScales["STt_top"] = STtopscale
MappingScales["STt_topbar"] = STtopbarscale
MappingScales["Wt"] = WTscale
MappingScales["Wtbar"] = WTbarscale
MappingScales["DYJets"] = DYscale
MappingScales["WJets"] = Wscale
MappingScales["W1Jets"] = W1scale
MappingScales["W2Jets"] = W2scale
MappingScales["W3Jets"] = W3scale
MappingScales["W4Jets"] = W4scale
MappingScales["WW"] = WWscale
MappingScales["WZ"] = WZscale

MappingScales["tt_PowhegP8"] = ttpowheg

MappingScales["tt_aMCatNLO"] = ttamcatnlo
MappingScales["tt_PowhegHpp"] = ttpowheghpp

MappingScales["tt_mtop1735_PowhegP8"] = ttpowheg_mtnewup
MappingScales["tt_mtop1735_PowhegP8"] = ttpowheg_mtnewup
MappingScales["tt_mtop1715new_PowhegP8"] = ttpowheg_mtnewdown
MappingScales["tt_mtop1715new_PowhegP8"] = ttpowheg_mtnewdown
MappingScales["tt_mtop1735old_PowhegP8"] = ttpowheg_mtoldup
MappingScales["tt_mtop1715old_PowhegP8"] = ttpowheg_mtolddown
MappingScales["tt_mtop1755_PowhegP8"] = ttpowheg_mtup3
MappingScales["tt_mtop1695_PowhegP8"] = ttpowheg_mtdown3

MappingScales["tt_isrup_PowhegP8"] = ttpowheg_isrup
MappingScales["tt_isrdown_PowhegP8"] = ttpowheg_isrdown
MappingScales["tt_fsrup_PowhegP8"] = ttpowheg_fsrup
MappingScales["tt_fsrdown_PowhegP8"] = ttpowheg_fsrdown
MappingScales["tt_tuneup_PowhegP8"] = ttpowheg_tuneup
MappingScales["tt_tunedown_PowhegP8"] = ttpowheg_tunedown
MappingScales["tt_hdup_PowhegP8"] = ttpowheg_hdup
MappingScales["tt_hddown_PowhegP8"] = ttpowheg_hddown
MappingScales["tt_erdon_PowhegP8"] = ttpowheg_erdon

MappingScales["STt_top_isrfsrup"] = STtopscale_psup
MappingScales["STt_top_isrfsrdown"] = STtopscale_psdown
MappingScales["STt_topbar_isrfsrup"] = STtopbarscale_psup
MappingScales["STt_topbar_isrfsrdown"] = STtopbarscale_psdown
MappingScales["Wt_fsrdown"] = WTscale_fsrdown
MappingScales["Wt_isrdown"] = WTscale_isrdown
MappingScales["Wtbar_fsrdown"] = WTbarscale_fsrdown
MappingScales["Wtbar_isrdown"] = WTbarscale_isrdown


#MappingScales["mtUp/tt_mtop1755_PowhegP8"] = ttpowheg_mtup
#MappingScales["mtDown/tt_mtop1695_PowhegP8"] = ttpowheg_mtdown
'''
#systematics
MappingScales["pdf/tt_PowhegP8"] = ttpowheg
#systematics up/daown

MappingScales["btagDown/tt_PowhegP8"] = ttpowheg
MappingScales["btagUp/tt_PowhegP8"] = ttpowheg
MappingScales["ltagDown/tt_PowhegP8"] = ttpowheg
MappingScales["ltagUp/tt_PowhegP8"] = ttpowheg

MappingScales["JESUp/tt_PowhegP8"] = ttpowheg
MappingScales["JESDown/tt_PowhegP8"] = ttpowheg
MappingScales["JERUp/tt_PowhegP8"] = ttpowheg
MappingScales["JERDown/tt_PowhegP8"] = ttpowheg

MappingScales["pileupUp/tt_PowhegP8"] = ttpowheg
MappingScales["pileupDown/tt_PowhegP8"] = ttpowheg

MappingScales["fsUp/tt_PowhegP8"] = ttpowheg
MappingScales["fsDown/tt_PowhegP8"] = ttpowheg
MappingScales["rsUp/tt_PowhegP8"] = ttpowheg
MappingScales["rsDown/tt_PowhegP8"] = ttpowheg
MappingScales["hdampUp/tt_PowhegP8"] = ttpowheg
MappingScales["hdampDown/tt_PowhegP8"] = ttpowheg
'''


