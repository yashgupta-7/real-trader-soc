# Stock
# YearRangeLow
# YearRangeHigh
# MarketCap
# PE Ratio
# DividendYield
# QuaterlyRevenue
# QuaterlyYearlyChangeInRevenue
# QuaterlyNetIncome
# QuaterlyGrowthInNetIncome
# QuaterlyDilutedEPS
# QuaterlyDilutedEPSGrowth
# QuaterlyNetProfitMargin
# QuaterlyNetProfitMarginGrowth
# QuaterlyOperating Income
# QuaterlyOperating Income Growth
# QuaterlyCash On Hand
# QuaterlyCash on Hand Growth
# QuaterlyCost of Revenue
# QuaterlyCost of Revenue Growth
# AnnualRevenue
# AnnualYearlyChangeInRevenue
# AnnualNetIncome
# AnnualGrowthInNetIncome
# AnnualDilutedEPS
# AnnualDilutedEPSGrowth
# AnnualNetProfitMargin
# AnnualNetProfitMarginGrowth
# AnnualOperating Income
# AnnualOperating Income Growth
# Net Change in Cash
# Growth in NetChange in Cash
# AnnualCash On Hand
# AnnualCash on Hand Growth
# AnnualCost of Revenue
# AnnualCost of Revenue Growth

# 3) Price to Earning's Ratio (Can be done!)
# 3) Improved Graham's Formula (Can be done!)
# 6) Free Cash Flow to Growth (Can be done!)
# 8) FCF to Profit
# 9) Cash from Operations Growth to Revenue
# 10) Earnings Yield
# 14) Revenue to Market Capitalization
#
#
# (Important Ones!)
# (Dynamic Stuff!)
# 29) 52 Week Range to current price
# 30) Momentum to current price (done!)
# 31) MACD to current price (Done!)
# 32) Relative Strength Index to current price  (Done!)
# 33) Average True Range to current price (Done!)
# 37) R-squared/mean value of stock (Done!)
# 17) Standard Deviation of Stocks over various intervals/Mean (Done!)
# 18) Beta (Done!)
# 19) Maximum DrawDown (Done!)
# 27) Arithmetic and Geometric Growth Rates(over various intervals) (Done!)


#Assume that dat, almost always has size of 100
def GetRSI(dat):
    r = dat[1:]
    l = dat[:-1]
    X = np.divide(r-l,l)
    p = np.sum(np.multiply(X>0,p))
    l = np.sum(np.multiply(X<0,p))
    return 100.0-(100.0/(1+(p/l)))

def AG(dat):
    B = dat[::25]
    m = np.mean(dat)
    L = []
    s = len(B)
    for i in range(0,s):
        for j in range(i+1,s):
            L.append((B[j]-B[i])/m)
            L.append((B[j]/B[i])*100)
def DD(data):
    r = dat[1:]
    l = dat[:-1]
    X = np.divide(r-l,l)
    return min(A)

def StdDMen(data):
    return (np.std(data)/mp.mean(dat))*100

def R2(data):
    from sklearn.linear_model import LinearRegression
    x = np.arange(len(data))
    model = LinearRegression()
    model.fit(x,data)
    return (model.score(x,data)/np.mean(data))*100

def ATR(data):
    cnt = 0
    avg = 0
    i = len(data)-1
    while i >= 25:
        avg+=max(max(data[i-24:i])-min(data[i-24:i]),abs(max(data[i-24:i])-data[i-25]),abs(min(data[i-24:i])-data[i-25]))
        cnt+=1
        i-=25
    return ((avg/cnt)/data[-1])*100

def MACD(data):
    x = len(data)//2
    long = 0
    short = 0
    alpha = 0.75
    for i in range(0,len(data)):
        if i==0:
            long = data[i]
        else:
            long = alpha*long + (1-alpha)*data[i]

    for i in range(x,len(data)):
        if i==x:
            short = data[i]
        else:
            short = alpha*short + (1-alpha)*data[i]

    return ((short-long)/data[-1])*100

def Moment(data):
    x = 0
    alpha = 0.75
    for i in range(0,len(data)):
        if i==0:
            x  = data[i]
        else:
            x = alpha*x + (1-alpha)*data[i]

    return x/data[-1]
