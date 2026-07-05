import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns


def process_data(df,noc):
   df.drop_duplicates(inplace=True)
   m=pd.get_dummies(df['Medal'],dtype=int)
   df=pd.concat([df,m],axis=1)
   df=pd.merge(df,noc,on='NOC',how='left')
   df=df.fillna({'Height':df['Height'].mean(),'Weight':df['Weight'].mean(),'Age':df['Age'].mean()}, inplace=True )
   return df




# about
def stat(olp):
    con=olp['region'].nunique()
    player=olp['Name'].nunique()
    event=olp['Event'].nunique()
    noc=olp['NOC'].nunique()
    sport=olp['Sport'].nunique()
    edition=olp['Year'].nunique()
    return {'Countries':con,"Players" :player, 'Event':event,'NOC' :noc, 'Sports':sport,'Edition': edition}



# about
def team_year(olp):
    fig=plt.figure(figsize=(12,7))
    a=olp.groupby('Year')['Team'].nunique().reset_index()   
    sns.set_theme(style="darkgrid")
    sns.lineplot(data=a,x='Year',y='Team')
    return fig
# about
def heatmap_sport_year(olp):
    fig=plt.figure(figsize=(25,20))
    pt=pd.pivot_table(olp, index='Sport', columns='Year', values='Event',aggfunc='nunique').fillna(0).astype('int')
    sns.heatmap(pt,annot=True)
    return fig
    
    
# medal
def country_rank(d,reg='overall',year='overall'):
   df=d.copy()
   df=df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],keep='first')
   if  year!='overall':
        df=df[df['Year']==year]
       
   t=df.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values(by=['Gold','Silver','Bronze'],ascending=False).reset_index()
   
   if reg!='overall':
      t=t[t['region']==reg]
   
   t['Total']=t['Gold']+t['Silver']+t['Bronze']
   t.index=t.index+1
   return t

# play
def playerbar(olp):
    b=olp.groupby(['Year','Sex'])['Name'].nunique().reset_index()   
    fig =plt.figure(figsize=(15,5))
    ax = sns.barplot(b,x='Year',y='Name',hue='Sex')
    ax.set_ylabel("Number of Players")
    ax.tick_params(axis="x", rotation=60)
    return fig
    
    
    

    
    #play
def best_player(d,sex='both',sport='overall',year='overall',region='overall'):
    df=d.copy()
    df=df.dropna(subset=['Medal'])
    if sex!='both':
        df=df[df['Sex']==sex]
        
    df3=df.copy()
    df=df.groupby(['Name','Team'])[['Gold','Silver','Bronze']].sum().sort_values(by=['Gold','Silver','Bronze'],ascending=False).reset_index()
    df3=df3.groupby(['Name','Year'])[['Gold','Silver','Bronze']].sum().reset_index()
    if sport!='overall' and year=='overall':
        df=df[df['Sport']==sport]
    if sport=='overall' and year!='overall':
        df=df3[df3['Year']==year].sort_values(by=['Gold','Silver','Bronze'],ascending=False)
    if sport!='overall' and year!='overall':
        df=df3[(df3['Sport']==sport) & (df3['Year']==year)].sort_values(by=['Gold','Silver','Bronze'],ascending=False)
    df.rename(columns={'Team':'Region'},inplace=True)
    if region!='overall':
        df=df[df['Region']==region]
        df.drop(columns=['Region'],inplace=True)
    df.index=df.index+1
    return df
    
    
    
    # play
def age_dist(olp):
    df=olp.copy()
    df=df[['Medal','Age','Name']]
    df.drop_duplicates(subset=['Name'])
    x1= df['Age']

    x2=df[df['Medal']=='Gold']['Age']
    x3=df[df['Medal']=='Silver']['Age']
    x4=df[df['Medal']=='Bronze']['Age']

    return ff.create_distplot([x1,x2,x3,x4],['Overall','Gold','Silver','Bronze'],show_hist=False,show_rug=False)
  



# play
def personal(olp,col='Weight',year='overall'):
    df=olp.copy()
    
    df=df[['Sport',col,'Sex','Name','Year']]
    df.drop_duplicates(subset=['Name'])
    if year!='overall':
        df=df[df['Year']==year]
        
    fig = go.Figure()
    fig.add_trace(go.Box(
        x=df["Sex"],
        y=df[col],
        name="Overall",
        visible=True
    ))
    for cat in df["Sport"].unique():
        
        fig.add_trace(
            go.Box(
                x=df[df["Sport"] == cat]["Sex"],
                y=df[df["Sport"] == cat][col],
                name=cat,
                visible=True if cat == "Male" else "legendonly"
            )
        )

    return fig

  
      
 # contry     
def Count_perform(d, country):
      df=d.copy()
      df=df.dropna(subset=['Medal'])
      df=df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],keep='first')[['Year','Medal','region']]
      df=df.groupby(['Year','region']).count().reset_index()
      df=df[df['region']==country]
      fig=plt.figure(figsize=(12,7))
      sns.set_theme(style="darkgrid")
      sns.lineplot(data=df,x='Year',y='Medal')
      return fig
      
      
      
   # country   
def Sport_perform(d, country):
      df=d.copy()
      df=df.dropna(subset=['Medal'])
      df=df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],keep='first')[['Year','Medal','region','Sport']]
      df=df.groupby(['Year','region','Sport']).count().reset_index()
      df=df[df['region']==country]
      fig=plt.figure(figsize=(25,20))
      sns.set_theme(style="darkgrid")
      pt=pd.pivot_table(df, index='Sport', columns='Year', values='Medal',aggfunc='count').fillna(0).astype('int')
      sns.heatmap(data=pt)  
      return fig    
      
      
      



def getreg(df):
    df=df.copy()
    l=df['region'].drop_duplicates().sort_values().to_list()
    l=list(l)
    l.insert(0,'overall')

    return l
def getyear(df):
    df=df.copy()
    l=df['Year'].drop_duplicates().sort_values().to_list()
    l=list(l)
    l.insert(0,'overall')
    return l
def getSport(df):
    df=df.copy()
    l=df['Sport'].drop_duplicates().sort_values().to_list()
    l=list(l)
    l.insert(0,'overall')
    return l

def best_wise_region(df):
    df=country_rank(df)
    return df['region'].to_list()
    
    