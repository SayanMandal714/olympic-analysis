import analysis
import streamlit as st
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns

d =pd.read_csv("olp.csv")
noc=pd.read_csv("noc_regions.csv")
df=analysis.process_data(d,noc)

country=analysis.getreg(df)
bcon=analysis.best_wise_region(df)
year=analysis.getyear(df) 
sport=analysis.getSport(df) 

option={
    'About': 'ab',
    'Medal Telly':'mt',
    'Player Analysis':'pa',
    'Country Performance':'cp'
}
st.sidebar.title(f"Olympics Analysis[{year[1]}-{year[-1]}]")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

sel=st.sidebar.radio("**Get Started**",options=option.keys())
ch=option[sel]



# about
if(ch=='ab'):
    st.title("About")
    d=analysis.stat(df)
    c=st.columns(1,border=True)[0]
    with c:
        it = iter(d.items())
        for i in range(2) :
            c1,c2,c3=st.columns(3,vertical_alignment='top',border=True)
            with c1:
                t=next(it)
                c1.markdown(f"#### {t[0]}")
                c1.markdown(f"##### {t[1]}")
            with c2:
                t=next(it)
                c2.markdown(f"#### {t[0]}")
                c2.markdown(f"##### {t[1]}")
            with c3:
                t=next(it)
                c3.markdown(f"#### {t[0]}")
                c3.markdown(f"##### {t[1]}")
    p1=st.columns(1,border=True)[0]
    p2=st.columns(1,border=True)[0]
    
                
    with p1:
        p1.markdown("### Team Vs Year")
        fig=analysis.team_year(df)
        p1.pyplot(fig)
    with p2:
        p2.markdown("### HeatMap(Sport-year)")
        fig2=analysis.heatmap_sport_year(df)
        p2.pyplot(fig2)

# medal
if(ch=='mt'):
    st.title("Medal Telly")
    con=st.sidebar.selectbox("Country",country,index=0)
    yr=st.sidebar.selectbox('Year',year,index=0)
    t=analysis.country_rank(df,con,yr) 
    st.dataframe(t, height=600)
    
# play   
if(ch=='pa'):
        op={
            'Best Player':'bp',
            'Athlete\'s Reports': 'ar'
        }
        sel2=st.sidebar.radio("**Select**",options=op.keys()) 
        c=  op[sel2] 
        
        if c=='bp':
            st.title('Best Playes')
            con=st.sidebar.selectbox("Country",country,index=0)
            yr=st.sidebar.selectbox('Year',year,index=0)
            sp=st.sidebar.selectbox('Sport',sport,index=0)
            l,m,r=st.columns([3,2,1])
            gen='both'
            with r:
                 g=r.selectbox('Sex',['Both','Male','Female'],index=0)
                 if g=='Male':gen='M'
                 elif g=='Female': gen='F'
                 else: gen='both'
            t=analysis.best_player(df,gen,sp,yr,con)
            st.dataframe(t, height=600)
        
        if c=='ar':
             st.title('Athlete\'s Reports')
             p1=st.columns(1,border=True)[0]    
             p2=st.columns(1,border=True)[0]   
             p3=st.columns(1,border=True)[0]   
             
             with p1:
                 p1.markdown("#### Age Distribution")
                 p1.plotly_chart(analysis.age_dist(df)) 
                
             with p2:
                 p2.markdown("### Athlete participatio")
                 p2.pyplot(analysis.playerbar(df))
            
             with p3:
                 p3.markdown("# Boxplot(Weight and Height)")
                 l,m,r=p3.columns([3,1,1])
                 g='Weight'
                 y='overall'
                 with m:
                      g=m.selectbox('Weight or Height',['Weight','Height'],index=0)
                      
                 with r:
                     y=r.selectbox('Year',year,index=0)
                      
                 p3.plotly_chart(analysis.personal(df,g,y))    
                     
                 
# country
if (ch=='cp'):
    st.title("Country Performance")
    p1=st.columns(1,border=True)[0]
    p2=st.columns(1,border=True)[0]
    con=st.sidebar.selectbox("Country",bcon,index=0)
    
    with p1:
        p1.markdown('### Performance Over Time')
        p1.pyplot(analysis.Count_perform(df,con))
    
    with p2:
        p2.markdown('### Region - Sport Performance Over Time')
        p2.pyplot(analysis.Sport_perform(df,con))
    
                     

            
        

            
 
        
        



