# install Hydroeval and import libs
# !pip install hydroeval
import pandas as pd
import hydroeval as he
import matplotlib.dates
from datetime import datetime
from dataretrieval import nwis
from IPython.display import display
from datetime import date
pd.options.mode.chained_assignment = None

def stat_eval_at_point(file1_path,file2_path):
    df1_r = pd.read_csv(file1_path)
    df2_r = pd.read_csv(file2_path)
    df1_r_name = df1_r.columns[1]
    df2_r_name = df2_r.columns[1]
#     data_1=df1_r.iloc[:, 1] 
#     data_2=df2_r.iloc[:, 1] 
    df=pd.merge(df1_r, df2_r,on=df1_r.iloc[:, 0])
    df.dropna(axis=0, inplace=True)
    data_1=df[df1_r_name]
    data_2=df[df2_r_name]
    nse_cpc=he.evaluator(he.nse,data_1,data_2)
    kge_cpc, r_cpc, alpha_cpc, beta_cpc = he.evaluator(he.kge, data_1,data_2)
    print("data 1 vs data 2","NSE=",nse_cpc,"KGE=",kge_cpc, "r=",r_cpc)
    return
    

# Set the parameters needed for the web service call

def Get_USGS_and_compute_statistics(siteID,startDate,endDate,NWM_data_path,USGS_saving_path):
    # Get the data
    discharge = nwis.get_iv(sites=siteID, parameterCd="00060", start=startDate, end=endDate)
    site = pd.DataFrame(discharge[0])
    site.reset_index(inplace=True)                                        
    site['datetime'] = pd.to_datetime(site['datetime'], utc=True,format='%Y-%m-%d %H:%M:%S')   
    site_copy = site.copy()
    site_copy['datetime'] = pd.to_datetime(site_copy['datetime'],utc=True, format='%Y-%m-%d %H:%M:%S')                                        
    site_copy.index = site_copy['datetime']                                         
    site_avg = site_copy['00060'].resample('d').mean()
    site_avg_num=site_avg.apply(pd.to_numeric)
    usgs_df = site_avg_num.to_frame(name='USGS')
    print(usgs_df)
    
    #USGS_csv='USGS_'+siteID+"_"+startDate+"_"+endDate+".csv"
    #print(USGS_csv)
#     usgs_df.to_csv(NWM_data_path+"usgs.csv")
    df1_r = pd.read_csv(NWM_data_path+"usgs.csv")
    df2_r = pd.read_csv(NWM_data_path)
    df1_r_name = df1_r.columns[1]
    df2_r_name = df2_r.columns[1]
#     data_1=df1_r.iloc[:, 1] 
#     data_2=df2_r.iloc[:, 1] 
    df=pd.merge(df1_r, df2_r,on=df2_r.iloc[:, 0])
    df.dropna(axis=0, inplace=True)
    print(df)
    data_1=df[df1_r_name]
    data_2=df[df2_r_name]
    nse_cpc=he.evaluator(he.nse,data_1,data_2)
    kge_cpc, r_cpc, alpha_cpc, beta_cpc = he.evaluator(he.kge, data_1,data_2)
    print("data 1 vs data 2","NSE=",nse_cpc,"KGE=",kge_cpc, "r=",r_cpc)
    return