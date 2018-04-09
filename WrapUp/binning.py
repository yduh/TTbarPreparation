#!/usr/bin/python


class bins2D:
	rebinX = 10 #2GeV/bin, this should be the unit
	rebinY = 60 #0.01/bin

	#xbins = [10*i for i in range(201)]
	#xbins = [20*i for i in range(101)]
	#xbins = [40*i for i in range(51)]

	xbins_3j = [0, 280] #[0, 300]
	xbins_4j = [0, 340] #[0, 360]
	for i in range(15, 101):
		xbins_3j.append(20*i)
	for i in range(18, 101):
		xbins_4j.append(20*i)

	#ybins = [-6.0, -1.8, -1.2, -0.6, 0, 0.6, 1.2, 1.8, 6.0]
	#absybins = [0, 0.6, 1.2, 1.8, 6.0]

	ybins = [-6.0, -1.2, -0.6, 0, 0.6, 1.2, 6.0]
	absybins = [0, 0.6, 1.2, 6.0]

	#ybins = [-6.0, -1.8, -0.8, 0, 0.8, 1.8, 6.0]
	#absybins = [0, 0.8, 1.8, 6.0]


	#check if putting all dely for up/down templates is smooth enough
	#ybins = [-6.0, 0, 6.0]
	#absybins = [0, 6.0]

class bins1D:
	rebinX = 10 #pt:2GeV/bin, tty:0.025
	#xbins = [20*i for i in range(41)]

