from pandas_datareader import data as pdr

import yfinance as yf
import numpy as np
import pandas as pd
yf.pdr_override() # <== that's all it takes :-)
import matplotlib.pyplot as plt

def GenerateOutput_1(df_1):

    df_1["Output"] = np.nan


    n = 5
    for i in range(n,df.shape[0]-n):
        df_1['Output'].iloc[i] = 0
        OutputCriteria = (max(df_1["High"].iloc[i+1],df_1["High"].iloc[i+2],df_1["High"].iloc[i+3],df_1["High"].iloc[i+4],df_1["High"].iloc[i+5]) - df_1["High"].iloc[i]) / df_1["High"].iloc[i]

        if(OutputCriteria > .1):
            df_1['Output'].iloc[i] = 1
    return df_1

def CalculateRSI(df_1):
    df_1['change'] = df['Close'].diff(1) # Calculate change
    df_1['change']=df['change'].apply(lambda x:round(x,2))

    df['gain'] = np.select([df['change']>0, df['change'].isna()], 
                       [df['change'], np.nan], 
                       default=0) 
    
    df_1['gain']=df['gain'].apply(lambda x:round(x,2))

    df['loss'] = np.select([df['change']<0, df['change'].isna()], 
                       [-df['change'], np.nan], 
                       default=0)
    df_1['loss']=df['loss'].apply(lambda x:round(x,2))



    # create avg_gain /  avg_loss columns with all nan
    df_1['avg_gain'] = np.nan 
    df_1['avg_loss'] = np.nan

    n = 14 # what is the window

    # keep first occurrence of rolling mean
    df_1['avg_gain'][n] = df_1['gain'].rolling(window=n).mean().dropna().iloc[0] 
    df_1['avg_loss'][n] = df_1['loss'].rolling(window=n).mean().dropna().iloc[0]

    # This is not a pandas way, looping through the pandas series, but it does what you need
    for i in range(n+1, df.shape[0]):
        df_1['avg_gain'].iloc[i] = (df_1['avg_gain'].iloc[i-1] * (n - 1) + df_1['gain'].iloc[i]) / n
        df_1['avg_loss'].iloc[i] = (df_1['avg_loss'].iloc[i-1] * (n - 1) + df_1['loss'].iloc[i]) / n

    # calculate rs and rsi
    df_1['rs'] = df_1['avg_gain'] / df_1['avg_loss']
    df_1['rsi'] = 100 - (100 / (1 + df_1['rs'] ))

    df_1['rs']=df['rs'].apply(lambda x:round(x,2))
    df_1['rsi']=df['rsi'].apply(lambda x:round(x,2))

    return df_1

def GetSubDF(df_1):
    subClass = ["Date","Open","Close","High","Low","Volume","macd","macd_h","macd_s","rs","rsi"]

    df_1 = df_1[subClass]
    return df_1


def CalculateSMA(df_1,TimeFrame=50):

    df_1["SMA_"+str(TimeFrame)] = df_1['Close'].rolling(TimeFrame).mean()
    df_1["SMA_"+str(TimeFrame)] = df["SMA_"+str(TimeFrame)].apply(lambda x:round(x,2))
    return df_1

def RoundDFValues(df_1):
    df['Open']=df['Open'].apply(lambda x:round(x,2))
    df['High']=df['High'].apply(lambda x:round(x,2))

    df['Low']=df['Low'].apply(lambda x:round(x,2))
    df['Close']=df['Close'].apply(lambda x:round(x,2))


    df['Adj Close']=df['Adj Close'].apply(lambda x:round(x,2))
    df['Volume']=df['Volume'].apply(lambda x:round(x,2))


    df['macd']=df['macd'].apply(lambda x:round(x,2))
    df['macd_h']=df['macd_h'].apply(lambda x:round(x,2))

    df['macd_s']=df['macd_s'].apply(lambda x:round(x,2))


    return df_1

def PlotGraph_MACD(df_1,symbol):
    
    df_1.reset_index(inplace=True)

    # Get current axis 
    ax = plt.gca() 
    #subClass = ["Date","Open","Close","High","Low","Volume","macd","macd_h","macd_s","rs","rsi"]
    # line plot for math marks 
    df_1.plot(kind='line', 
            x='Date', 
            y='macd', 
            color='green', ax=ax) 
    
    # line plot for physics marks 
    df_1.plot(kind='line', x='Date', 
            y='macd_s', 
            color='blue', ax=ax) 
    
    # set the title 
    plt.title(symbol+'-MACD') 

    saveName = symbol+"_MACD.png"
    plt.savefig(saveName)
    # show the plot 
    plt.show()


def PlotGraph_RSI(df_1,symbol):
    
    df_1.reset_index(inplace=True)

    # Get current axis 
    ax = plt.gca() 
    #subClass = ["Date","Open","Close","High","Low","Volume","macd","macd_h","macd_s","rs","rsi"]
    # line plot for math marks 
    df_1.plot(kind='line', 
            x='Date', 
            y='rsi', 
            color='green', ax=ax) 
    
    # set the title 
    plt.title(symbol+'-RSI') 

    saveName = symbol+"_RSI.png"
    plt.savefig(saveName)

    # show the plot 
    plt.show()
    



def GetNseList():
    nsefile = "*.csv"
    df = pd.read_csv (nsefile)
    nsesymbollist = list(df['Symbol'])
    print(nsesymbollist)
    return nsesymbollist



if __name__=="__main__":
    #nseList = GetNseList()
    nseList = ['360ONE', '3MINDIA', 'ABB', 'ACC', 'AGI', 'AIAENG', 'APLAPOLLO', 'AUBANK', 'AARTIDRUGS', 'AARTIIND', 'AARTIPHARM', 'AAVAS', 'ABBOTINDIA', 'ACCELYA', 'ACE', 'ADANIENSOL', 'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ADANIPOWER', 'ATGL', 'AWL', 'ABCAPITAL', 'ABFRL', 'ADVENZYMES', 'AEGISCHEM', 'AETHER', 'AFFLE', 'AHLUCONT', 'AJANTPHARM', 'APLLTD', 'ALKEM', 'ALKYLAMINE', 'ACLGATI', 'ALLCARGO', 'ALOKINDS', 'ARE&M', 'AMBER', 'AMBUJACEM', 'AMIORG', 'ANANDRATHI', 'ANANTRAJ', 'ANGELONE', 'ANURAS', 'APARINDS', 'APCOTEXIND', 'APOLLOHOSP', 'APOLLOPIPE', 'APOLLOTYRE', 'APTUS', 'ACI', 'ARVINDFASN', 'ARVIND', 'ASAHIINDIA', 'ASHOKLEY', 'ASHOKA', 'ASIANPAINT', 'ASTEC', 'ASTERDM', 'ASTRAMICRO', 'ASTRAZEN', 'ASTRAL', 'ATUL', 'AUROPHARMA', 'AUTOAXLES', 'AVALON', 'AVANTIFEED', 'DMART', 'AXISBANK', 'BEML', 'BLS', 'BSE', 'BAJAJ-AUTO', 'BAJAJCON', 'BAJFINANCE', 'BAJAJFINSV', 'BAJAJHIND', 'BAJAJHLDNG', 'BALAMINES', 'BALKRISIND', 'BALMLAWRIE', 'BALRAMCHIN', 'BANDHANBNK', 'BANKBARODA', 'BANKINDIA', 'MAHABANK', 'BARBEQUE', 'BATAINDIA', 'BAYERCROP', 'BERGEPAINT', 'BEPL', 'BDL', 'BEL', 'BHARATFORG', 'BHEL', 'BPCL', 'BHARTIARTL', 'BIKAJI', 'BIOCON', 'BIRLACORPN', 'BSOFT', 'BLUEDART', 'BLUESTARCO', 'BBTC', 'BOMDYEING', 'BORORENEW', 'BOSCHLTD', 'BRIGADE', 'BCG', 'BRITANNIA', 'MAPMYINDIA', 'CARERATING', 'CCL', 'CESC', 'CGPOWER', 'CIEINDIA', 'CMSINFO', 'CRISIL', 'CSBBANK', 'CAMLINFINE', 'CAMPUS', 'CANFINHOME', 'CANBK', 'CAPLIPOINT', 'CGCL', 'CARBORUNIV', 'CARTRADE', 'CARYSIL', 'CASTROLIND', 'CEATLTD', 'CENTRALBK', 'CDSL', 'CENTURYPLY', 'CENTURYTEX', 'CERA', 'CHALET', 'CHAMBLFERT', 'CHEMPLASTS', 'CHENNPETRO', 'CHOICEIN', 'CHOLAHLDNG', 'CHOLAFIN', 'CIGNITITEC', 'CIPLA', 'CUB', 'CLEAN', 'COALINDIA', 'COCHINSHIP', 'COFORGE', 'COLPAL', 'CAMS', 'CONCORDBIO', 'CONFIPET', 'CONCOR', 'COROMANDEL', 'COSMOFIRST', 'CRAFTSMAN', 'CREDITACC', 'CROMPTON', 'CUMMINSIND', 'CYIENT', 'DBREALTY', 'DBCORP', 'DCBBANK', 'DCMSHRIRAM', 'DCXINDIA', 'DLF', 'DABUR', 'DALBHARAT', 'DALMIASUG', 'DATAPATTNS', 'DATAMATICS', 'DEEPAKFERT', 'DEEPAKNTR', 'DELHIVERY', 'DELTACORP', 'DEN', 'DEVYANI', 'DHANI', 'DBL', 'DISHTV', 'DCAL', 'DIVGIITTS', 'DIVISLAB', 'DIXON', 'DODLA', 'DOLLAR', 'LALPATHLAB', 'DRREDDY', 'DREAMFOLKS', 'DWARKESH', 'EIDPARRY', 'EIHOTEL', 'EPL', 'ESABINDIA', 'EASEMYTRIP', 'EDELWEISS', 'EICHERMOT', 'ELECON', 'EMIL', 'ELECTCAST', 'ELGIEQUIP', 'EMAMILTD', 'ENDURANCE', 'ENGINERSIN', 'EPIGRAL', 'EQUITASBNK', 'ERIS', 'ESCORTS', 'ETHOSLTD', 'EVEREADY', 'EXIDEIND', 'FDC', 'NYKAA', 'FEDERALBNK', 'FACT', 'FIEMIND', 'FINEORG', 'FCL', 'FINOPB', 'FINCABLES', 'FINPIPE', 'FSL', 'FIVESTAR', 'FORTIS', 'FUSION', 'GRINFRA', 'GAIL', 'GET&D', 'GHCL', 'GMMPFAUDLR', 'GMRINFRA', 'GABRIEL', 'GALAXYSURF', 'GANESHHOUC', 'GRSE', 'GARFIBRES', 'GATEWAY', 'GICRE', 'GILLETTE', 'GLAND', 'GLAXO', 'GLS', 'GLENMARK', 'MEDANTA', 'GLOBUSSPR', 'GOCOLORS', 'GPIL', 'GODFRYPHLP', 'GODREJAGRO', 'GODREJCP', 'GODREJIND', 'GODREJPROP', 'GOKEX', 'GRANULES', 'GRAPHITE', 'GRASIM', 'GRAVITA', 'GESHIP', 'GREAVESCOT', 'GREENLAM', 'GREENPANEL', 'GREENPLY', 'GRINDWELL', 'GUFICBIO', 'GUJALKALI', 'GAEL', 'FLUOROCHEM', 'GUJGASLTD', 'GMDCLTD', 'GNFC', 'GPPL', 'GSFC', 'GSPL', 'HEG', 'HGINFRA', 'HBLPOWER', 'HCLTECH', 'HDFCAMC', 'HDFCBANK', 'HDFCLIFE', 'HFCL', 'HIL', 'HLEGLAS', 'HAPPSTMNDS', 'HARSHA', 'HATHWAY', 'HAVELLS', 'HCG', 'HEIDELBERG', 'HEMIPROP', 'HERITGFOOD', 'HEROMOTOCO', 'HIKAL', 'HSCL', 'HINDALCO', 'HGS', 'HAL', 'HCC', 'HINDCOPPER', 'HNDFDS', 'HINDOILEXP', 'HINDPETRO', 'HINDUNILVR', 'HINDZINC', 'HINDWAREAP', 'POWERINDIA', 'HOMEFIRST', 'HONAUT', 'HUDCO', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI', 'ISEC', 'IDBI', 'IDFCFIRSTB', 'IDFC', 'IFBIND', 'IFCI', 'IIFL', 'IKIO', 'IOLCP', 'IRB', 'IRCON', 'ITC', 'ITDCEM', 'ITI', 'INDIACEM', 'INDIAGLYCO', 'IBULHSGFIN', 'IBREALEST', 'INDIAMART', 'INDIANB', 'IEX', 'INDHOTEL', 'IMFA', 'IOC', 'IOB', 'IRCTC', 'IRFC', 'INDIGOPNTS', 'ICIL', 'INDOCO', 'IGL', 'INDUSTOWER', 'INDUSINDBK', 'INFIBEAM', 'NAUKRI', 'INFY', 'INGERRAND', 'INOXWIND', 'INTELLECT', 'INDIGO', 'IONEXCHANG', 'IPCALAB', 'ISGEC', 'JBCHEPHARM', 'JKCEMENT', 'JKIL', 'JBMA', 'JKLAKSHMI', 'JKPAPER', 'JKTYRE', 'JMFINANCIL', 'JSWENERGY', 'JSWSTEEL', 'JTEKTINDIA', 'JTLIND', 'JAICORPLTD', 'JISLJALEQS', 'JPASSOCIAT', 'JPPOWER', 'J&KBANK', 'JAMNAAUTO', 'JINDALPOLY', 'JINDALSAW', 'JSL', 'JINDALSTEL', 'JINDWORLD', 'JCHAC', 'JUBLFOOD', 'JUBLINGREA', 'JUBLPHARMA', 'JWL', 'JUSTDIAL', 'JYOTHYLAB', 'KPRMILL', 'KEI', 'KNRCON', 'KPITTECH', 'KRBL', 'KSB', 'KAJARIACER', 'KPIL', 'KALYANKJIL', 'KANSAINER', 'KTKBANK', 'KARURVYSYA', 'KSCL', 'KAYNES', 'KEC', 'KKCL', 'KFINTECH', 'KIRIINDUS', 'KIRLOSBROS', 'KIRLOSENG', 'KIRLPNU', 'KOLTEPATIL', 'KOTAKBANK', 'KIMS', 'KRSNAA', 'L&TFH', 'LTTS', 'LGBBROSLTD', 'LICHSGFIN', 'LTFOODS', 'LTIM', 'LAOPALA', 'LAXMIMACH', 'LANDMARK', 'LT', 'LATENTVIEW', 'LAURUSLABS', 'LXCHEM', 'LEMONTREE', 'LICI', 'LINDEINDIA', 'LLOYDSENGG', 'LUPIN', 'LUXIND', 'MASFIN', 'MMTC', 'MOIL', 'MRF', 'MSTCLTD', 'MTARTECH', 'LODHA', 'MGL', 'MAHSEAMLES', 'M&MFIN', 'M&M', 'MHRIL', 'MAHLIFE', 'MAHLOG', 'MAITHANALL', 'MANINFRA', 'MANAPPURAM', 'MRPL', 'MANKIND', 'MARICO', 'MARKSANS', 'MARUTI', 'MASTEK', 'MFSL', 'MAXHEALTH', 'MAYURUNIQ', 'MAZDOCK', 'MEDPLUS', 'MOL', 'METROBRAND', 'METROPOLIS', 'MINDACORP', 'MIDHANI', 'MOLDTKPAC', 'MSUMI', 'MOTILALOFS', 'MPHASIS', 'BECTORFOOD', 'MCX', 'MUTHOOTFIN', 'NATCOPHARM', 'NBCC', 'NCC', 'NEOGEN', 'NESCO', 'NHPC', 'NLCINDIA', 'NMDC', 'NSLNISP', 'NOCIL', 'NRBBEARING', 'NTPC', 'NH', 'NATIONALUM', 'NFL', 'NAVA', 'NAVINFLUOR', 'NAVNETEDUL', 'NAZARA', 'NESTLEIND', 'NETWORK18', 'NEULANDLAB', 'NEWGEN', 'NAM-INDIA', 'NUVOCO', 'OBEROIRLTY', 'ONGC', 'OIL', 'OLECTRA', 'PAYTM', 'OPTIEMUS', 'OFSS', 'ORIENTCEM', 'ORIENTELEC', 'POLICYBZR', 'PCBL', 'PDSL', 'PGEL', 'PIIND', 'PNBHOUSING', 'PNCINFRA', 'PSPPROJECT', 'PTC', 'PTCIL', 'PVRINOX', 'PAGEIND', 'PAISALO', 'PARADEEP', 'PARAS', 'PATANJALI', 'PERSISTENT', 'PETRONET', 'PFIZER', 'PHOENIXLTD', 'PIDILITIND', 'PEL', 'PPLPHARMA', 'POLYMED', 'POLYCAB', 'POLYPLEX', 'POONAWALLA', 'PFC', 'POWERGRID', 'POWERMECH', 'PRAJIND', 'PRESTIGE', 'PRICOLLTD', 'PRINCEPIPE', 'PRSMJOHNSN', 'PRIVISCL', 'PGHL', 'PGHH', 'PRUDENT', 'PNB', 'QUESS', 'RBLBANK', 'RECLTD', 'RHIM', 'RITES', 'RADICO', 'RVNL', 'RAILTEL', 'RAIN', 'RAINBOW', 'RAJESHEXPO', 'RAJRATAN', 'RALLIS', 'RKFORGE', 'RAMKY', 'RCF', 'RATEGAIN', 'RATNAMANI', 'RTNINDIA', 'RTNPOWER', 'RAYMOND', 'REDINGTON', 'RELAXO', 'RELIANCE', 'RELINFRA', 'RPOWER', 'RELIGARE', 'RESPONIND', 'RBA', 'ROLEXRINGS', 'ROSSARI', 'ROUTE', 'RUPA', 'SBFC', 'SBICARD', 'SBILIFE', 'SIS', 'SJVN', 'SKFINDIA', 'SRF', 'SAFARI', 'SAKSOFT', 'MOTHERSON', 'SANOFI', 'SANSERA', 'SAPPHIRE', 'SARDAEN', 'SAREGAMA', 'SCHAEFFLER', 'SCHNEIDER', 'SEQUENT', 'SHANTIGEAR', 'SHARDACROP', 'SHAREINDIA', 'SFL', 'SHILPAMED', 'SCI', 'SBCL', 'SHOPERSTOP', 'SHREECEM', 'RENUKA', 'SHRIRAMFIN', 'SHYAMMETL', 'SIEMENS', 'SIYSIL', 'SOBHA', 'SOLARINDS', 'SOMANYCERA', 'SONACOMS', 'SONATSOFTW', 'SOUTHBANK', 'SPANDANA', 'STARCEMENT', 'STARHEALTH', 'SBIN', 'SAIL', 'SSWL', 'SWSOLAR', 'STLTECH', 'STAR', 'STYLAMIND', 'STYRENIX', 'SUBEXLTD', 'SUDARSCHEM', 'SULA', 'SUMICHEM', 'SPARC', 'SUNPHARMA', 'SUNTV', 'SUNDARMFIN', 'SUNDRMFAST', 'SUNFLAG', 'SUNTECK', 'SUPRAJIT', 'SUPREMEIND', 'SPLPETRO', 'SUPRIYA', 'SURYAROSNI', 'SUVENPHAR', 'SUZLON', 'SWANENERGY', 'SYMPHONY', 'SYNGENE', 'SYRMA', 'TCIEXP', 'TCNSBRANDS', 'TDPOWERSYS', 'TTKPRESTIG', 'TV18BRDCST', 'TVSMOTOR', 'TVSSCS', 'TMB', 'TANLA', 'TARSONS', 'TATACHEM', 'TATACOMM', 'TCS', 'TATACONSUM', 'TATAELXSI', 'TATAINVEST', 'TATAMETALI', 'TATAMTRDVR', 'TATAMOTORS', 'TATAPOWER', 'TATASTEEL', 'TTML', 'TATVA', 'TEAMLEASE', 'TECHM', 'TECHNOE', 'TIIL', 'TEGA', 'TEJASNET', 'NIACL', 'RAMCOCEM', 'THERMAX', 'TIRUMALCHM', 'THOMASCOOK', 'THYROCARE', 'TIDEWATER', 'TI', 'TIMETECHNO', 'TIMKEN', 'TINPLATE', 'TIPSINDLTD', 'TITAGARH', 'TITAN', 'TORNTPHARM', 'TORNTPOWER', 'TCI', 'TRENT', 'TRIDENT', 'TRIVENI', 'TRITURBINE', 'TIINDIA', 'UCOBANK', 'UFLEX', 'UNOMINDA', 'UPL', 'UTIAMC', 'UJJIVAN', 'UJJIVANSFB', 'ULTRACEMCO', 'UNICHEMLAB', 'UNIONBANK', 'UNIPARTS', 'UBL', 'MCDOWELL-N', 'USHAMART', 'VGUARD', 'VMART', 'VIPIND', 'VSTTILLERS', 'VRLLOG', 'WABAG', 'VAIBHAVGBL', 'VTL', 'VARROC', 'VBL', 'MANYAVAR', 'VEDL', 'VENKEYS', 'VESUVIUS', 'VIJAYA', 'VINATIORGA', 'IDEA', 'VOLTAMP', 'VOLTAS', 'WELCORP', 'WELENT', 'WELSPUNLIV', 'WSTCSTPAPR', 'WESTLIFE', 'WHIRLPOOL', 'WIPRO', 'WOCKPHARMA', 'WONDERLA', 'YESBANK', 'ZFCVINDIA', 'ZEEL', 'ZENTEC', 'ZENSARTECH', 'ZOMATO', 'ZYDUSLIFE', 'ZYDUSWELL', 'ECLERX', 'EMUDHRA']
    for each in nseList:
        symbol = each +".NS" #"ITC.NS"#"TATAMOTORS.NS"
        df = pdr.get_data_yahoo(symbol, start="2013-01-01", end="2023-12-12")

    
        # Get the 26-day EMA of the closing price
        k = df['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
        # Get the 12-day EMA of the closing price
        d = df['Close'].ewm(span=26, adjust=False, min_periods=26).mean()
        # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
        macd = k - d
        # Get the 9-Day EMA of the MACD for the Trigger line
        macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
        # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
        macd_h = macd - macd_s
        # Add all of our new values for the MACD to the dataframe
        df['macd'] = df.index.map(macd)
        df['macd_h'] = df.index.map(macd_h)
        df['macd_s'] = df.index.map(macd_s)

        #Date,Open,High,Low,Close,Adj Close,Volume,macd,macd_h,macd_s
        df = RoundDFValues(df)

        df = CalculateRSI(df)
        
        #df = GetSubDF(df)

        df = CalculateSMA(df,50)

        df = CalculateSMA(df,200)

        df = GenerateOutput_1(df)

        PlotGraph_MACD(df,symbol)
        PlotGraph_RSI(df,symbol)
        #csvname = symbol+".csv"
        #df.to_csv(csvname)
        

