# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

df = pd.read_csv('../data/processed/LOLOracleData.csv')

df.drop(['server','summoner_name','Time'],axis=1,inplace=True)

df.head()

df.columns

Blue=df.columns[1:6]
Red=df.columns[6:11]

df.loc[:,Blue]

champ=df.copy()
champ.drop(['winner'],axis=1,inplace=True)

CSdf = pd.read_csv('../data/processed/ChampionWr.csv')

CSdf.head()

# +
cs=pd.DataFrame()
Roles = ['Top','Jng','Mid','Adc','Sup']
champ=CSdf.loc[0,'Champions']
role=CSdf.loc[0,'Role1']
Roles.remove(role)
blue=df.loc[(df['B'+role]==champ)];
red=df.loc[(df['R'+role]==champ)];
for i in Roles:
    cs=cs.append(blue['B'+i].value_counts());
    cs=cs.append(red['R'+i].value_counts());
    
    
Roles.append(role)
g=cs.sum(axis=0)
tm=g.idxmax()
#if tm=='Jhin' || tm=="Kai'Sa":
#        g=g.drop(g.idxmax())
#b=CSdf[CSdf['Champions']==tm]
#rolemt=CSdf.loc[CSdf[CSdf['Champions']==tm].index[0],'Role1'];
rolemt=CSdf.loc[CSdf['Champions']==tm,'Role1'].iloc[0];
ptr=red.loc[(red['R'+rolemt]==tm)];
ptb=blue.loc[(blue['B'+rolemt]==tm)];
b=len(ptb);
bw=len(ptb[ptb['winner']=='Blue']);
r=len(ptr);
rw=len(ptr[ptr['winner']=='Red']);
twr=(rw+bw)/(r+b)
# -

cs

ka=pd.DataFrame()
#ka['Camille']=g

ka['Played together']=g

ka

type(rolemt)

twr

g=cs.sum(axis=0)

g

sum(g)

CSdf[CSdf['Champions']==champ]

cd = pd.DataFrame(CSdf['Champions'])
cd['TotalPlayed']=CSdf['TotalPlayed']
cd['Totalwinrate']=CSdf['Totalwinrate']

import time
start=time.process_time();
for ii in range(len(CSdf)):    
    cs=pd.DataFrame()
    Roles = ['Top','Jng','Mid','Adc','Sup']
    champ=CSdf.loc[ii,'Champions']
    role=CSdf.loc[ii,'Role1']
    Roles.remove(role)
    blue=df.loc[(df['B'+role]==champ)];
    red=df.loc[(df['R'+role]==champ)];
    for i in Roles:
        cs=cs.append(blue['B'+i].value_counts());
        cs=cs.append(red['R'+i].value_counts());


    Roles.append(role)
    
    f=cs.sum(axis=0)
    cd.loc[ii,'Most played teammate(Love is in the air)'] = f.idxmax()
    cd.loc[ii,'Times played together'] = f.max()
    #new since 05.02.2020
    tm=f.idxmax()
    #if tm=='Jhin' or tm=="Kai'Sa":
        #f=f.drop(f.idxmax())
        
    #cd.loc[ii,'Most played teammate(without Jhin)'] = f.idxmax()
    #cd.loc[ii,'Times played together(without Jhin)'] = f.max()
    
    #rolemt=CSdf.loc[CSdf[CSdf['Champions']==tm].index[0],'Role1'];
    rolemt=CSdf.loc[CSdf['Champions']==tm,'Role1'].iloc[0];
    ptr=red.loc[(red['R'+rolemt]==tm)];
    ptb=blue.loc[(blue['B'+rolemt]==tm)];
    b=len(ptb);
    bw=len(ptb[ptb['winner']=='Blue']);
    r=len(ptr);
    rw=len(ptr[ptr['winner']=='Red']);
    twr=(rw+bw)/(r+b)
    
    cd.loc[ii,'Totalwinrate with Most played Teammate']= twr
end=time.process_time();
print(end-start)


# +
n=20 #how often two champions have two play together to be considered in statistics
import time
start=time.process_time();
for ii in range(len(CSdf)):    
    ka=pd.DataFrame()
    cs=pd.DataFrame()
    Roles = ['Top','Jng','Mid','Adc','Sup']
    champ=CSdf.loc[ii,'Champions']
    role=CSdf.loc[ii,'Role1']
    Roles.remove(role)
    blue=df.loc[(df['B'+role]==champ)];
    red=df.loc[(df['R'+role]==champ)];
    for i in Roles:
        cs=cs.append(blue['B'+i].value_counts());
        cs=cs.append(red['R'+i].value_counts());


    Roles.append(role)
    
    f=cs.sum(axis=0)
    #ka['Teammates'] = f.index
    cd.loc[ii,'Most played teammate(Love is in the air)'] = f.idxmax()
    cd.loc[ii,'Times played together'] = f.max()
    ka['Times played together'] = f
    #new since 07.02.2020
    #tm=f.idxmax()
    #if tm=='Jhin' or tm=="Kai'Sa":
        #f=f.drop(f.idxmax())
        
    #cd.loc[ii,'Most played teammate(without Jhin)'] = f.idxmax()
    #cd.loc[ii,'Times played together(without Jhin)'] = f.max()
    
    #rolemt=CSdf.loc[CSdf[CSdf['Champions']==tm].index[0],'Role1'];
    for tm in f.index:
        rolemt=CSdf.loc[CSdf['Champions']==tm,'Role1'].iloc[0];
        ptr=red.loc[(red['R'+rolemt]==tm)];
        ptb=blue.loc[(blue['B'+rolemt]==tm)];
        b=len(ptb);
        bw=len(ptb[ptb['winner']=='Blue']);
        r=len(ptr);
        rw=len(ptr[ptr['winner']=='Red']);
        if b+r != 0:
            twr=(rw+bw)/(r+b)
        else: twr=np.NaN

        ka.loc[tm,'Winrate']= twr
    exec('Duos{} = ka.copy()'.format(champ[0:2]))
    cd.loc[ii,'Totalwinrate with Most played Teammate']= ka.loc[f.idxmax(),'Winrate']
    hist=ka[ka['Times played together']>=n]['Winrate']
    cd.loc[ii,'Winrate with all Teammates over {} Games'.format(n)]=np.mean(hist)
    cd.loc[ii,'Standard derivation wT over {} Games'.format(n)]=np.std(hist)
end=time.process_time();

print(end-start)
# -


# cd

cd.sort_values('Standard derivation wT over {} Games'.format(n))

cd.sort_values('Totalwinrate with Most played Teammate', ascending=False)

a=DuosCa[DuosCa['Times played together']>=20]['Winrate']
#a=b['Winrate']
plt.hist(a)
np.std(a)

a=DuosCa['Winrate']
a=a[~a.isnull()]
a.plot.hist()
np.std(a)



plt.plot(cd['Totalwinrate with Most played Teammate'],'*')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(cd)

cd.sort_values('Totalwinrate with Most played Teammate', ascending=False)

bc=cd[cd['Totalwinrate with Most played Teammate']>=0.55]
bc.sort_values('Times played together', ascending=False)

cd[cd['Most played teammate(without Jhin)']!="Kai'Sa"]

CSdf[CSdf['Champions']=="Kai'Sa"]

cd.sort_values('TotalPlayed', ascending=False)

cd[cd['TotalPlayed']>=5000]

CSdf[CSdf['TotalPlayed']>=5000]

k=[['Adc','Sup'],['Mid','Jng'],['Jng','Sup'],['Top','Mid'],['Top','Jng']]

# +
nak = pd.DataFrame(CSdf['Champions'])
nak['Role']=CSdf['Role1']
nak['TotalPlayed']=CSdf['TotalPlayed']
nak['Totalwinrate']=CSdf['Totalwinrate']
import time
start=time.process_time();
for ii in range(len(CSdf)): 
    champ=CSdf.loc[ii,'Champions']
    role=CSdf.loc[ii,'Role1']
    blue=df.loc[(df['B'+role]==champ)];
    red=df.loc[(df['R'+role]==champ)];
    Roles = ['Top','Jng','Mid','Adc','Sup']
    Roles.remove(role)
    for i in Roles:
        cs=pd.DataFrame()
        cs=cs.append(blue['B'+i].value_counts());
        cs=cs.append(red['R'+i].value_counts());
        f=cs.sum(axis=0)
        nak.loc[ii,'Most played teammate in '+i] = f.idxmax()
        nak.loc[ii,'Times played together in ' +i] = f.max()
        
        tm = f.idxmax()
        
        ptr=red.loc[(red['R'+i]==tm)];
        ptb=blue.loc[(blue['B'+i]==tm)];
        b=len(ptb);
        bw=len(ptb[ptb['winner']=='Blue']);
        r=len(ptr);
        rw=len(ptr[ptr['winner']=='Red']);
        twr=(rw+bw)/(r+b)

        nak.loc[ii,'Totalwinrate with Most played Teammate in '+ i]= twr
    
    Roles.append(role)
    
end=time.process_time();

print(end-start)
# -

nak[nak['Role']=='Adc']

# # synergies for the specific roles

asp = pd.DataFrame(CSdf['Champions'])
asp.columns = ['Champions']
champions=CSdf['Champions']
zeros = np.zeros(153).reshape(153,1)
for i in range(len(champions)):
    asp[champions[i]] = zeros

champions

adc = pd.DataFrame(CSdf[CSdf['Role1']=='Adc']['Champions'])
adc.columns = ['Champions with first Role Adc']
championssup=CSdf[CSdf['Role1']=='Sup']['Champions']
#zeros = np.zeros(len(adc)).reshape(len(adc),1)
#for i in range(len(championssup)):
#    adc[championssup[i]] = zeros

# +
import time
start=time.process_time();
for ii in adc.index: 
    champ=CSdf.loc[ii,'Champions']
    #champ=ii
    #role=CSdf.loc[ii,'Role1']
    role='Adc'
    
    blue=df.loc[(df['B'+role]==champ)];
    red=df.loc[(df['R'+role]==champ)];
    
    i='Sup'
    for iii in championssup:
        #tm=CSdf.loc[iii,'Champions']
        tm=iii

        ptr=red.loc[(red['R'+i]==tm)];
        ptb=blue.loc[(blue['B'+i]==tm)];
        b=len(ptb);
        bw=len(ptb[ptb['winner']=='Blue']);
        r=len(ptr);
        rw=len(ptr[ptr['winner']=='Red']);
        if r+b==0:
            twr=0
        else:
            twr=2*(rw+bw)-(r+b) #+-1 for win/loss
            #twr=(rw+bw)/(r+b) #winrates

        adc.loc[ii,iii]= twr
    
    
    
end=time.process_time();

print(end-start)
# -

syn=[['Adc','Sup'],['Mid','Jng'],['Jng','Sup'],['Top','Mid'],['Top','Jng']]

# +
import time
start=time.process_time();
for i,k in syn:
    adc = pd.DataFrame(CSdf[CSdf['Role1']==i]['Champions'])
    adc.columns = ['Champions with first Role'+i]
    championssup=CSdf[CSdf['Role1']==k]['Champions']


    for ii in adc.index: 
        champ=CSdf.loc[ii,'Champions']
        #champ=ii
        #role=CSdf.loc[ii,'Role1']
        role=i

        blue=df.loc[(df['B'+role]==champ)];
        red=df.loc[(df['R'+role]==champ)];

        
        for iii in championssup:
            #tm=CSdf.loc[iii,'Champions']
            tm=iii

            ptr=red.loc[(red['R'+k]==tm)];
            ptb=blue.loc[(blue['B'+k]==tm)];
            b=len(ptb);
            bw=len(ptb[ptb['winner']=='Blue']);
            r=len(ptr);
            rw=len(ptr[ptr['winner']=='Red']);
            if r+b==0:
                twr=0
            else:
                #twr=2*(rw+bw)-(r+b) #+-1 for win/loss
                #twr=(rw+bw)/(r+b) #winrates
                twr= (((rw+bw)/(r+b))-0.5)*2 #winrates scaled from +1 to -1
            adc.loc[ii,iii]= twr


    adc.to_csv('../data/processed/'+i+'and'+k+'(WinratesScaledTo+-1).csv',index=True)
end=time.process_time();

print(end-start)
# -

adc

# +
#asp = pd.DataFrame(CSdf['Champions'])
#asp['Role']=CSdf['Role1']
#asp['TotalPlayed']=CSdf['TotalPlayed']
#asp['Totalwinrate']=CSdf['Totalwinrate']
#asp.columns = ['Champions']


import time
start=time.process_time();
for ii in range(len(CSdf)): 
    champ=CSdf.loc[ii,'Champions']
    #role=CSdf.loc[ii,'Role1']
    role='Adc'
    
    blue=df.loc[(df['B'+role]==champ)];
    red=df.loc[(df['R'+role]==champ)];
    
    i='Sup'
    for iii in range(len(CSdf)):
        tm=CSdf.loc[iii,'Champions']

        ptr=red.loc[(red['R'+i]==tm)];
        ptb=blue.loc[(blue['B'+i]==tm)];
        b=len(ptb);
        bw=len(ptb[ptb['winner']=='Blue']);
        r=len(ptr);
        rw=len(ptr[ptr['winner']=='Red']);
        if r+b==0:
            twr=0
        else:
            twr=(rw+bw)/(r+b)

        asp.loc[ii,tm]= twr
    
    
    
end=time.process_time();

print(end-start)
# -

role='Adc'
champ='Miss Fortune'
blue=df.loc[(df['B'+role]==champ)];
red=df.loc[(df['R'+role]==champ)]; 
i='Sup'
tm='Volibear'
ptr=red.loc[(red['R'+i]==tm)];
ptb=blue.loc[(blue['B'+i]==tm)];
b=len(ptb);
bw=len(ptb[ptb['winner']=='Blue']);
r=len(ptr);
rw=len(ptr[ptr['winner']=='Red']);
twr=(rw+bw)/(r+b)

ra=df[df['BAdc']=='Ezreal']
ra[ra['BSup']=='Volibear']

asp[CSdf['Role1']=='Adc']

asp.to_csv('../data/processed/AdcAndSup.csv',index=True)

lol=pd.DataFrame()
for i in Roles:
    a=CSdf[CSdf['Role1']==i]
    jo=a['TotalPlayed']
    lol.loc[i,'MostPlayed']=CSdf.loc[jo.idxmax(),'Champions']
    jo=jo.drop(jo.idxmax())
    lol.loc[i,'SecondMostPlayed']=CSdf.loc[jo.idxmax(),'Champions']
    jo=jo.drop(jo.idxmax())
    lol.loc[i,'ThirdMostPlayed']=CSdf.loc[jo.idxmax(),'Champions']
    jo=jo.drop(jo.idxmax())
    lol.loc[i,'FourthMostPlayed']=CSdf.loc[jo.idxmax(),'Champions']
    jo=jo.drop(jo.idxmax())
    lol.loc[i,'FifthMostPlayed']=CSdf.loc[jo.idxmax(),'Champions']
    jo=jo.drop(jo.idxmax())
    lol.loc[i,'SixthMostPlayed']=CSdf.loc[jo.idxmax(),'Champions']


jo=a['TotalPlayed']
jo.idxmax()

lol



eis=df.copy()
#for i in Roles:
i='Top'
eis=eis[((eis['B'+i]==lol.loc[i,'MostPlayed'])&(eis['R'+i]==lol.loc[i,'SecondMostPlayed'])) | ((eis['R'+i]==lol.loc[i,'MostPlayed'])&(eis['B'+i]==lol.loc[i,'SecondMostPlayed']))]

eis

i='Jng'
eis=eis[((eis['B'+i]==lol.loc[i,'MostPlayed'])&(eis['R'+i]==lol.loc[i,'SecondMostPlayed'])) | ((eis['R'+i]==lol.loc[i,'MostPlayed'])&(eis['B'+i]==lol.loc[i,'SecondMostPlayed']))]

eis


# # Part Two

def getNmostPlayedByRole(n,data,columnNames=[],championNames=True):
    res = pd.DataFrame()
    for i in Roles:
        a = data[data['Role1']==i]
        jo = a['TotalPlayed']

        for j in range(1,n+1):
            if (championNames):
                colName = str(j)+'.mostPlayed'
                res.loc[i,colName] = data.loc[jo.idxmax(),'Champions']
            
            for k in columnNames:
                colRate = str(j)+'.'+k
                res.loc[i,colRate] = data.loc[jo.idxmax(),k]
            
            jo=jo.drop(jo.idxmax())
    return res


getNmostPlayedByRole(10,CSdf)


def cond(t,role,data,n):
    colName = str(n)+'.mostPlayed'
    return (t['B'+role]==data.loc[role,colName])|(t['R'+role]==data.loc[role,colName])


def atLeastOne(role,n):
    res = df.copy()
    nMostPlayedDf = getNmostPlayedByRole(n,CSdf)
    
    condition = cond(res,role,nMostPlayedDf,1)
    for i in range(2,n+1):
        condition = (condition | cond(res,role,nMostPlayedDf,i))
    
    res = res[condition]
    return res


len(df)


#percantage of all games
def percantageOfAllGames(data):
    rel = len(data) / len(df)
    return round(100*rel,1)


# In 90% of the games(in this patch) there was at least one of the 6 most played Adc-champions played.
# In 62.2% of the games either the most or the second most Adc-champion was played.

def cumulate(k):
    
    kumuliert = []
    x_coord = []
    
    roleCounter = 0
    for i in Roles:
        for n in range(1,1+k):
            kumuliert.append( percantageOfAllGames(atLeastOne(i,n)) )
            x_coord.append(roleCounter)
        roleCounter += 1
    
    x = np.arange(len(Roles))  # the label locations

    fig, ax = plt.subplots()
    ax.bar(x_coord,kumuliert,color='#00123456')   #         #1372ac = rgba(19, 114, 172, 1)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percent')
    ax.set_title('cumulated Percantage of games where at least 1,2,...,'+ str(k) +' of the most played champions in a role were played')
    ax.set_xticks(x)
    ax.set_xticklabels(Roles)
    
    ax.set_ylim([0,100])


    plt.show()


def cumulate_easyRead(k):
    
    kumuliert = []
    x_coord = []
    
    roleCounter = 0
    for i in Roles:
        for n in range(1,1+k):
            kumuliert.append( percantageOfAllGames(atLeastOne(i,n)) )
            x_coord.append(roleCounter)
            roleCounter += 1
        roleCounter += 1
    
    #x = np.arange(len(Roles))  # the label locations
    x = []
    for i in range(0,5):

        x.append(2+i*6)
    x

    fig, ax = plt.subplots()
    ax.bar(x_coord,kumuliert,color='#00123456')   #         #1372ac = rgba(19, 114, 172, 1)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percent')
    ax.set_title('cumulated Percantage of games where at least 1,2,...,'+ str(k) +' of the most played champions in a role were played')
    ax.set_xticks(x)
    ax.set_xticklabels(Roles)
    
    ax.set_ylim([0,100])


    plt.show()

x = []
for i in range(0,5):

    x.append(2+i*6)
x

cumulate_easyRead(5)


def printN(k):
    for i in Roles:
        print(i+':')
        for n in range(1,1+k):
            print( percantageOfAllGames(atLeastOne(i,n)), '%')


#printN(5)
for i in range(0,6):
    cumulate(6-i)

cumulate(11)


def getChampionStats(pArray):
    res = CSdf.copy()
    
    condition = (cd['Champions'] == pArray[0])
    for i in pArray:
        condition = (condition | (cd['Champions'] == i))
    
    res = res[condition]
    return res


c5 = getChampionStats(['Jayce','Taliyah','Galio','Miss Fortune','Alistar'])
c4 = getChampionStats(['Irelia','Nidalee','Yone','Ezreal','Sett'])
c4

getNmostPlayedByRole(11,CSdf)

getNmostPlayedByRole(6,CSdf,['Totalwinrate'],False)

getNmostPlayedByRole(6,CSdf,['Totalwinrate'])

getChampionStats(['Galio'])

first = df[df['RMid']=='Galio']
first = first[['RMid','BMid']]

# +
#for i in first['BMid']:

 #   first['freq'] = first.groupby(i)['Galio'].transform('count')
first['BMid'].value_counts()
# -

getChampionStats(['Galio','Akali','Sylas','Viktor','Orianna'])

temp = first
for i in ['Akali','Sylas','Ekko','Yone']:
    temp = temp[temp['BMid']!=i]
withoutMoreOftenPlayedChamps = temp

withoutMoreOftenPlayedChamps['BMid'].value_counts()


def getNmostPlayed_Opponent(n,data,pRole,columnNames=[],championNames=True):
    res = pd.DataFrame()
    for i in [pRole]:
        a = data[data['Role1']==i]
        jo = a['TotalPlayed']

        for j in range(1,n+1):
            if (championNames):
                colName = str(j)+'.mostPlayed'
                res.loc[i,colName] = data.loc[jo.idxmax(),'Champions']
            
            for k in columnNames:
                colRate = str(j)+'.'+k
                res.loc[i,colRate] = data.loc[jo.idxmax(),k]
            
            jo=jo.drop(jo.idxmax())
    return res


df['freq'] = df.groupby('a')['a'].transform('count')

getNmostPlayed_Opponent(6,first,['RMid'])
