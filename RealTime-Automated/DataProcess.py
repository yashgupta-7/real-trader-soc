import support as sp
import numpy as np

#Assuming the CompanyInf Vector will be like:
# 0) Last Year's RangeL,
# 1) Last YearRangeHigh ,
# 2) Market Capitalization
# 3) P/E Ratio,,
# 4) Dividend Yield,
# 5) QuaterlyYearlyChangeInRevenue,
# 6) QuaterlyNetIncome,
# 7) QuaterlyGrowthInNetIncome,
# 8) QuaterlyDilutedEPS,
# 9) QuaterlyDilutedEPSGrowth,
# 10) QuaterlyNetProfitMargin,
# 11) QuaterlyNetProfitMarginGrowth,
# 12) QuaterlyOperating Income,
# 13) QuaterlyOperating Income Growth,
# 14) QuaterlyCash On Hand,
# 15) QuaterlyCash on Hand Growth,
# 16) QuaterlyCost of Revenue,
# 17) QuaterlyCost of Revenue Growth,
# 18) AnnualRevenue,
# 19) AnnualYearlyChangeInRevenue,
# 20) AnnualNetIncome,
# 21) AnnualGrowthInNetIncome,
# 22) AnnualDilutedEPS,
# 23) AnnualDilutedEPSGrowth,
# 24) AnnualNetProfitMargin,
# 25) AnnualNetProfitMarginGrowth,
# 26) AnnualOperating Income,
# 27) AnnualOperating Income Growth,
# 28) Net Change in Cash,
# 29) Growth in NetChange in Cash ,
# 30) AnnualCash On Hand,
# 31) AnnualCash on Hand Growth,
# 32) AnnualCost of Revenue,
# 33) AnnualCost of Revenue Growth,
# 34) Beta


def GetX(StockPrice1000):
	# X= []
	# X.append(CompanyInf[3])
	# X.append(CompanyInf[4])
	# X.append(CompanyInf[34])
	# X.append(sp.GetGrahams(CompanyInf[0],CompanyInf[1],CompanyInf[22],CompanyInf[21]))
	# X.append(sp.GetGrahams(CompanyInf[0],CompanyInf[1],CompanyInf[8],CompanyInf[7]))
	# X.append(CompanyInf[14]/CompanyInf[6])
	# X.append(CompanyInf[30]/CompanyInf[20])
	# X.append(CompanyInf[12]/CompanyInf[6])
	# X.append(CompanyInf[32]/CompanyInf[20])
	# X.append(CompanyInf[2]/CompanyInf[18])
	# X.append(CompanyInf[7])
	# X.append(CompanyInf[9])
	# X.append(CompanyInf[10])
	# X.append(CompanyInf[11])
	# X.append(CompanyInf[13])
	# X.append(CompanyInf[15])
	# X.append(CompanyInf[17])
	# X.append(CompanyInf[19])
	# X.append(CompanyInf[21])
	# X.append(CompanyInf[23])
	# X.append(CompanyInf[24])
	# X.append(CompanyInf[25])
	# X.append(CompanyInf[27])
	# X.append(CompanyInf[29])
	# X.append(CompanyInf[31])
	# X.append(CompanyInf[33])
	Y = []
	StockPrice100 = StockPrice1000[900:]
	Y.append(sp.Moment(StockPrice1000))
	Y.append(sp.Moment(StockPrice1000[500:]))
	Y.append(sp.Moment(StockPrice1000[750:]))
	Y.append(sp.Moment(StockPrice100))
	Y.append(sp.Moment(StockPrice100[50:]))
	Y.append(sp.Moment(StockPrice100[90:]))
	Y.append(sp.MACD(StockPrice1000))
	Y.append(sp.MACD(StockPrice100))
	Y.append(sp.GetRSI(StockPrice1000[500:]))
	Y.append(sp.GetRSI(StockPrice1000[750:]))
	Y.append(sp.GetRSI(StockPrice1000[900:]))
	Y.append(sp.ATR(StockPrice1000[900:]))
	Y.append(sp.ATR(StockPrice1000[500:]))
	Y.append(sp.ATR(StockPrice1000[750:]))
	Y.append(sp.R2(StockPrice1000))
	Y.append(sp.R2(StockPrice1000[500:]))
	Y.append(sp.R2(StockPrice1000[750:]))
	Y.append(sp.R2(StockPrice100))
	Y.append(sp.R2(StockPrice100[50:]))
	Y.append(sp.R2(StockPrice100[90:]))
	Y+=sp.AG(StockPrice100)
	Y+=sp.AG(StockPrice1000[::10])
	Y.append(sp.DD(StockPrice100))
	Y.append(sp.DD(StockPrice100[50:]))
	Y.append(sp.DD(StockPrice100[90:]))
	Y.append(sp.DD(StockPrice1000[500:]))
	Y.append(sp.DD(StockPrice1000[750:]))
	Y.append(sp.StdDMen(StockPrice100[90:]))
	Y.append(sp.StdDMen(StockPrice1000))
	Y.append(sp.StdDMen(StockPrice100[50:]))
	Y.append(sp.StdDMen(StockPrice100))
	Y.append(sp.StdDMen(StockPrice1000[750:]))
	Y.append(sp.StdDMen(StockPrice1000[500:]))
	return np.array(Y)

def GetY(InitialPrice,StockPriceUpcoming750):
	X = []
	m = np.argmax(StockPriceUpcoming750[:10])
	l = max(0,m-10)
	r = min(StockPriceUpcoming750.shape[0],m+10)
	X.append(100.0*((sp.MomentJ(StockPriceUpcoming750[l:r])/InitialPrice)-1.00))    #0
	m = np.argmax(StockPriceUpcoming750[:60])
	l = max(0,m-10)
	r = min(StockPriceUpcoming750.shape[0],m+10)
	X.append(100.0*((sp.MomentJ(StockPriceUpcoming750[l:r])/InitialPrice)-1.00))   #1
	m = np.argmax(StockPriceUpcoming750[:180])
	l = max(0,m-10)
	r = min(StockPriceUpcoming750.shape[0],m+10)
	X.append(100.0*((sp.MomentJ(StockPriceUpcoming750[l:r])/InitialPrice)-1.00))      #2
	m = np.argmax(StockPriceUpcoming750[:360])
	l = max(0,m-10)
	r = min(StockPriceUpcoming750.shape[0],m+10)
	X.append(100.0*((sp.MomentJ(StockPriceUpcoming750[l:r])/InitialPrice)-1.00))      #3
	m = np.argmax(StockPriceUpcoming750[:540])
	l = max(0,m-10)
	r = min(StockPriceUpcoming750.shape[0],m+10)
	X.append(100.0*((sp.MomentJ(StockPriceUpcoming750[l:r])/InitialPrice)-1.00))      #4
	m = np.argmax(StockPriceUpcoming750[:750])
	l = max(0,m-10)
	r = min(StockPriceUpcoming750.shape[0],m+10)
	X.append(100.0*((sp.MomentJ(StockPriceUpcoming750[l:r])/InitialPrice)-1.00))        #5
	m = np.argmin(StockPriceUpcoming750[:10])
	l = max(0,m-10)
	r = min(StockPriceUpcoming750.shape[0],m+10)
	X.append(100.0*((sp.MomentJ(StockPriceUpcoming750[l:r])/InitialPrice)-1.00))             #6
	m = np.argmin(StockPriceUpcoming750[:60])
	l = max(0,m-10)
	r = min(StockPriceUpcoming750.shape[0],m+10)
	X.append(100.0*((sp.MomentJ(StockPriceUpcoming750[l:r])/InitialPrice)-1.00))                #7
	m = np.argmin(StockPriceUpcoming750[:180])
	l = max(0,m-10)
	r = min(StockPriceUpcoming750.shape[0],m+10)
	X.append(100.0*((sp.MomentJ(StockPriceUpcoming750[l:r])/InitialPrice)-1.00))               #8
	m = np.argmin(StockPriceUpcoming750[:360])
	l = max(0,m-10)
	r = min(StockPriceUpcoming750.shape[0],m+10)
	X.append(100.0*((sp.MomentJ(StockPriceUpcoming750[l:r])/InitialPrice)-1.00))              #9
	m = np.argmin(StockPriceUpcoming750[:540])
	l = max(0,m-10)
	r = min(StockPriceUpcoming750.shape[0],m+10)
	X.append(100.0*((sp.MomentJ(StockPriceUpcoming750[l:r])/InitialPrice)-1.00))                      #10
	m = np.argmin(StockPriceUpcoming750[:750])
	l = max(0,m-10)
	r = min(StockPriceUpcoming750.shape[0],m+10)
	X.append(100.0*((sp.MomentJ(StockPriceUpcoming750[l:r])/InitialPrice)-1.00))                 #11
	return np.array(X)
