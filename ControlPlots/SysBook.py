#!/usr/bin/python
from math import sqrt

errList = [
		['JESDownFlavorQCD','JESUpFlavorQCD'],
		['JESDownRelativeBal','JESUpRelativeBal'],
		['pileupDown','pileupUp'],
		['lepDown','lepUp'],
		['JERDown','JERUp'],
		['bdecayDown','bdecayUp'],
		['btagDown','btagUp'],
		['ltagDown','ltagUp'],
		]

#in the oreder of ttsig, st, V+jets and QCD
ele = {}
ele['3j'] = {
		'lumi':		[0.025, 0.025, 0.025],
		'JESnorm':	[0.007, 0.010, 0.015],
		'PDF':		[0.050, 0.030, 0.000],
		'alphas':	[0.010, 0.004, 0.000],
		'TbckNorm':	[0.000, 0.150, sqrt(0.8**2 + 1.8**2 + 0.8**2 + 1.3**2 + 0.2**2 + 3.6**2 + 3.3**2 + 13.2**2 + 1.9**2 + 68.6**2)/100]
		}
ele['4j'] = {
		'lumi':		[0.025, 0.025, 0.025],
		'JESnorm':	[0.013, 0.020, 0.031],
		'PDF':		[0.050, 0.010, 0.000],
		'alphas':	[0.010, 0.002, 0.000],
		'TbckNorm':	[0.000, 0.150, sqrt(2.9**2 + 1.8**2 + 2.7**2 + 4.5**2 + 2.7**2 + 2.7**2 + 3.6**2 + 0.6**2 + 2.3**2 + 62.0**2)/100]
		}
ele['5j'] = {
		'lumi':		[0.025, 0.025, 0.025],
		'JESnorm':	[0.025, 0.030, 0.076],
		'PDF':		[0.050, 0.010, 0.000],
		'alphas':	[0.011, 0.003, 0.000],
		'TbckNorm':	[0.000, 0.150, sqrt(2.2**2 + 1.8**2 + 2.8**2 + 6.2**2 + 1.9**2 + 3.1**2 + 3.8**2 + 7.9**2 + 2.4**2 + 42.4**2)/100]
		}
ele['6j'] = {
		'lumi':		[0.025, 0.025, 0.025],
		'JESnorm':	[0.037, 0.042, 0.078],
		'PDF':		[0.050, 0.010, 0.000],
		'alphas':	[0.011, 0.003, 0.000],
		'TbckNorm':	[0.000, 0.150, sqrt(3.7**2 + 1.8**2 + 3.9**2 + 4.6**2 + 3.0**2 + 2.5**2 + 2.8**2 + 10.5**2 + 2.7**2 + 60.6**2)/100]
		}

ele['3jSB'] = {
		'lumi':		[0.025, 0.025, 0.025],
		'JESnorm':	[0.007, 0.010, 0.015],
		'PDF':		[0.050, 0.030, 0.000],
		'alphas':	[0.010, 0.004, 0.000],
		'TbckNorm':	[0.000, 0.150, sqrt(0.8**2 + 1.8**2 + 0.8**2 + 1.3**2 + 0.2**2 + 3.6**2 + 3.3**2 + 13.2**2 + 1.9**2 + 68.6**2)/100] #7.3
		}
ele['4jSB'] = {
		'lumi':		[0.025, 0.025, 0.025],
		'JESnorm':	[0.013, 0.020, 0.031],
		'PDF':		[0.050, 0.010, 0.000],
		'alphas':	[0.010, 0.002, 0.000],
		'TbckNorm':	[0.000, 0.150, sqrt(2.9**2 + 1.8**2 + 2.7**2 + 4.5**2 + 2.7**2 + 2.7**2 + 3.6**2 + 0.6**2 + 2.3**2 + 62.0**2)/100] #11.1
		}
ele['5jSB'] = {
		'lumi':		[0.025, 0.025, 0.025],
		'JESnorm':	[0.025, 0.030, 0.076],
		'PDF':		[0.050, 0.010, 0.000],
		'alphas':	[0.011, 0.003, 0.000],
		'TbckNorm':	[0.000, 0.150, sqrt(2.2**2 + 1.8**2 + 2.8**2 + 6.2**2 + 1.9**2 + 3.1**2 + 3.8**2 + 7.9**2 + 2.4**2 + 42.4**2)/100] #9.6
		}
ele['6jSB'] = {
		'lumi':		[0.025, 0.025, 0.025],
		'JESnorm':	[0.037, 0.042, 0.078],
		'PDF':		[0.050, 0.010, 0.000],
		'alphas':	[0.011, 0.003, 0.000],
		'TbckNorm':	[0.000, 0.150, sqrt(3.7**2 + 1.8**2 + 3.9**2 + 4.6**2 + 3.0**2 + 2.5**2 + 2.8**2 + 10.5**2 + 2.7**2 + 60.6**2)/100] #15.4
		}

relsys = {}
for jetCat,systDict in ele.iteritems():
	relsys[jetCat] = [0.,0.,0.]
	for systName,systList in systDict.iteritems():
		for isyst,syst in enumerate(systList):
			relsys[jetCat][isyst] += syst**2
	for isyst,syst in enumerate(relsys[jetCat]):
		relsys[jetCat][isyst] = sqrt(syst)

evt = {}
evt['3j'] = [301192.2, 25855.5, 37882.3]
evt['4j'] = [224877.6, 6950.1, 6127.1]
evt['5j'] = [138688.3, 4057.6, 2584.4]
evt['6j'] = [82718.2, 2242.8, 1552.2]
evt['3jSB'] = [0, 0, 1]#[133174.8, 23678.9, 2131783.7]
evt['4jSB'] = [0, 0, 1]#[39483.5, 3603.5, 196742.6]
evt['5jSB'] = [0, 0, 1]#[17841.3, 1195.1, 51595.2]
evt['6jSB'] = [0, 0, 1]#[7387.2, 364.4, 15157.7]
evt['3jup'] = [sum(comp) for comp in zip(evt['3j'], evt['4j'], evt['5j'], evt['6j'])]
evt['4jup'] = [sum(comp) for comp in zip(evt['4j'], evt['5j'], evt['6j'])]

totsys = {}
for s in ['3j','4j','5j','6j','3jSB','4jSB','5jSB','6jSB']:
	totsys[s] = sqrt(sum([c1**2 *c2**2 for c1, c2 in zip([c for c in relsys[s]], [c/sum(evt[s]) for c in evt[s]])]))


totsys['4jup'] = 0.092
totsys['3jup'] = [totsys['3j'], totsys['4j'], totsys['5j'], totsys['6j'], totsys['6j'], totsys['6j'], totsys['6j'], totsys['6j']]

rnnlo_up = 851.53/831.76
rnnlo_dw = 802.56/831.76
rsfsup = {}
rsfsdw = {}

rsfsup['3j'] = rnnlo_dw*(1568749.61149/1385342.90254)
rsfsdw['3j'] = rnnlo_up*(1568749.61149/1754113.60533)
rsfsup['4j'] = rnnlo_dw*(1172704.53812/1039750.83389)
rsfsdw['4j'] = rnnlo_up*(1172704.53812/1311521.50047)
rsfsup['5j'] = rnnlo_dw*(722336.926549/630133.873745)
rsfsdw['5j'] = rnnlo_up*(722336.926549/822225.166865)
rsfsup['6j'] = rnnlo_dw*(430894.618573/366930.645656)
rsfsdw['6j'] = rnnlo_up*(430894.618573/507446.844826)

rsfsup['4jup'] = rnnlo_dw*(2325936.08324/2036815.35329)
rsfsdw['4jup'] = rnnlo_up*(2325936.08324/2641193.51216)
rsfsup['3jup'] = rnnlo_dw*(3894007.95821/3421628.863)
rsfsdw['3jup'] = rnnlo_up*(3894007.95821/4394410.54211)

