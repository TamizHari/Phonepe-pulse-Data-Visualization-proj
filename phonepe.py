import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image


#dataframe_creation
mydb = mysql.connector.connect(host="localhost",user="root",password="")

print(mydb)
mycursor = mydb.cursor(buffered=True)
mycursor.execute('show databases')
for i in mycursor:
    print(i)

#aggregated_insurance_dataframe
mycursor.execute("SELECT * FROM phonepe.aggregated_insurance")
mydb.commit()
table1=mycursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggregated_Transaction_dataframe
mycursor.execute("SELECT * FROM phonepe.aggregated_transaction")
mydb.commit()
table2=mycursor.fetchall()

Aggre_transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggregated_user_dataframe
mycursor.execute("SELECT * FROM phonepe.aggregated_user")
mydb.commit()
table3=mycursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))

#map_insurance_dataframe
mycursor.execute("SELECT * FROM phonepe.map_insurance")
mydb.commit()
table4=mycursor.fetchall()

Map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

#map_Transaction_dataframe
mycursor.execute("SELECT * FROM phonepe.map_transaction")
mydb.commit()
table5=mycursor.fetchall()

Map_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

#map_user_dataframe
mycursor.execute("SELECT * FROM phonepe.map_user")
mydb.commit()
table6=mycursor.fetchall()

Map_user=pd.DataFrame(table6,columns=("States","Years","Quarter","Districts","RegisteredUser","AppOpens"))

#top_insurance_dataframe
mycursor.execute("SELECT * FROM phonepe.top_insurance")
mydb.commit()
table7=mycursor.fetchall()

top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_transaction_dataframe
mycursor.execute("SELECT * FROM phonepe.top_transaction")
mydb.commit()
table8=mycursor.fetchall()

top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_user_dataframe
mycursor.execute("SELECT * FROM phonepe.top_user")
mydb.commit()
table9=mycursor.fetchall()

top_user=pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes","RegisteredUsers"))

def Transaction_amount_count_Y(df,year):

    tacy= df[df["Years"]==year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_amount=px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tacyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Blackbody_r,height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)

    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"] :
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States",featureidkey= "properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name= "States",title= f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States",featureidkey= "properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name= "States",title= f"{year} TRANSACTION COUNT", fitbounds="locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df,quarter):
    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 =st.columns(2)
    with col1:

        fig_amount=px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count=px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"] :
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States",featureidkey= "properties.ST_NM",
                                    color="Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                    hover_name= "States",title= f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations",
                                    height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    
    with col2:

        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States",featureidkey= "properties.ST_NM",
                                    color="Transaction_count",color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                    hover_name= "States",title= f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds="locations",
                                    height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Aggre_Tran_Transaction_type(df,state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True, inplace=True)
    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_pie_1=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_amount",
                        width=600,title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)
        st.plotly_chart(fig_pie_1)
    
    with col2:

        fig_pie_2=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_count",
                        width=600,title=f"{state.upper()} TRANSACTION COUNT", hole=0.5)
        st.plotly_chart(fig_pie_2)

# Aggregated_user_analysis_1
def Aggre_user_plot_1(df, year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True,inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")[["Transaction_count"]].sum())
    aguyg.reset_index(inplace=True)
    fig_bar_1=px.bar(aguyg,x="Brands", y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence=px.colors.sequential.haline_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggregated_user analysis_2
def Aggre_user_plot_2(df,quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyqg,x="Brands", y="Transaction_count", title=f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence=px.colors.sequential.Magenta_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

#Aggregated_user_analysis_3
def Aggre_user_plot_3(df,state):
    auyqs=df[df["States"]== state]
    auyqs.reset_index(drop=True, inplace=True)
    
    fig_line_1=px.line(auyqs, x="Brands",y="Transaction_count",hover_data="Percentage",
                      title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width=1000, markers=True)
    st.plotly_chart(fig_line_1)

#map_insurance_district
def map_insur_District(df,state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1=px.bar(tacyg,  x="Transaction_amount", y="Districts", orientation= "h", height= 600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(tacyg,  x="Transaction_count", y="Districts", orientation= "h", height= 600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Purp_r)
        st.plotly_chart(fig_bar_2)

#Map_user_plot_1
def map_user_plot_1(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True,inplace=True)

    muyg=muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1=px.line(muyg, x="States",y=["RegisteredUser","AppOpens"],
                        title= f"{year} REGISTERED USER APPOPENS", width=1000, height=800, markers=True)
    st.plotly_chart(fig_line_1)

    return muy

#Map_user_plot_2
def map_user_plot_2(df,quarter):
    muq=df[df["Quarter"]==quarter]
    muq.reset_index(drop=True,inplace=True)

    muqg=muq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muqg.reset_index(inplace=True)

    fig_line_1=px.line(muqg, x="States",y=["RegisteredUser","AppOpens"],
                        title= f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USER APPOPENS", width=1000, height=800, markers=True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muq

#map_user_plot_3
def map_user_plot_3(df,states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2=st.columns(2)
    with col1:

        fig_map_user_bar_1=px.bar(muyqs, x="RegisteredUser",y="Districts", orientation= "h",
                                title= "REGISTERED USER", height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:

        fig_map_user_bar_2=px.bar(muyqs, x= "AppOpens",y= "Districts", orientation= "h",
                                title= f"{states.upper()} APPOPENS", height=800, color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

#top_insurance_plot_1
def Top_insurance_plot_1(df,state):
    tiy=df[df["States"]==state]
    tiy.reset_index(drop=True,inplace=True)

    tiyg=tiy.groupby("Pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    tiyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_top_insur_bar_1=px.bar(tiy, x="Quarter",y="Transaction_amount", hover_data= "Pincodes",
                                    title= "TRANSACTION AMOUNT", width=600, height=650, color_discrete_sequence=px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:

        fig_top_insur_bar_2=px.bar(tiy, x="Quarter",y="Transaction_count", hover_data= "Pincodes",
                                    title= "TRANSACTION COUNT", width=600, height=650, color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)
#top_user_plot_1
def top_user_plot_1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True,inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1=px.bar(tuyg, x= "States", y= "RegisteredUsers", color= "Quarter", width=1000, height=800,
                        color_discrete_sequence=px.colors.sequential.Burgyl, hover_name="States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

#top_user_plot_2
def top_user_plot_2(df,state):
    tuys=df[df["States"]==state]
    tuys.reset_index(drop=True,inplace=True)

    fig_top_plot_2=px.bar(tuys,x="Quarter",y="RegisteredUsers",title= "REGISTERED USERS, PINCODES, QUARTER",
                        width=1000, height= 800, color= "RegisteredUsers", hover_data="Pincodes",
                        color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)

# SQL_transaction_amount
def top_chart_transaction_amount(table_name):
    mydb = mysql.connector.connect(host="localhost",user="root",password="")

    print(mydb)
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute('show databases')
    for i in mycursor:
        print(i)

    #====================PLOT_1=========================>>>>>>>>>>>>>>>

    query1= f'''Select states, SUM(transaction_amount) AS transaction_amount
                from phonepe.{table_name}
                group by states
                order by transaction_amount DESC
                LIMIT 10;'''

    mycursor.execute(query1)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns= ("states","transaction_amount"))
    
    col1,col2=st.columns(2)
    with col1:
    
        fig_amount_1=px.bar(df_1, x="states", y="transaction_amount", title=" TOP 10 TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount_1)

    #=========================PLOT_2======================>>>>>>>>>>>>

    query2= f'''Select states, SUM(transaction_amount) AS transaction_amount
                from phonepe.{table_name}
                group by states
                order by transaction_amount
                LIMIT 10;'''

    mycursor.execute(query2)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns= ("states","transaction_amount"))

    with col2:


        fig_amount_2=px.bar(df_2, x="states", y="transaction_amount", title="LAST 10 TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)
        
    #=========================PLOT_3==========================>>>>>>>>>>>>>

    query3= f'''Select states, AVG(transaction_amount) AS transaction_amount
                from phonepe.{table_name}
                group by states
                order by transaction_amount'''

    mycursor.execute(query3)
    table_3=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns= ("states","transaction_amount"))

    fig_amount_3=px.bar(df_3, x="transaction_amount", y="states", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

# transaction_count_SQL
def top_chart_transaction_count(table_name):
    mydb = mysql.connector.connect(host="localhost",user="root",password="")

    print(mydb)
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute('show databases')
    for i in mycursor:
        print(i)

    #===================PLOT_1===================>>>>>>>>>>>>>>>>>

    query1= f'''Select states, SUM(Transaction_count) AS Transaction_count
                from phonepe.{table_name}
                group by states
                order by Transaction_count DESC
                LIMIT 10;'''

    mycursor.execute(query1)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns= ("states","Transaction_count"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount_1=px.bar(df_1, x="states", y="Transaction_count", title="TOP 10 TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount_1)

    #=========================PLOT_2==========================>>>>>>>>>>>>>>>>>>>

    query2= f'''Select states, SUM(Transaction_count) AS Transaction_count
                from phonepe.{table_name}
                group by states
                order by Transaction_count
                LIMIT 10;'''

    mycursor.execute(query2)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns= ("states","Transaction_count"))

    with col2:

        fig_amount_2=px.bar(df_2, x="states", y="Transaction_count", title="LAST 10 TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)
            
    #---------------------------PLOT_3----------------------------->>>>>>>>>>>>>>>>>

    query3= f'''Select states, AVG(Transaction_count) AS Transaction_count
                from phonepe.{table_name}
                group by states
                order by Transaction_count'''

    mycursor.execute(query3)
    table_3=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns= ("states","Transaction_count"))

    fig_amount_3=px.bar(df_3, x="Transaction_count", y="states", title="AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

# SQL_registered_user
def top_chart_registered_user(table_name, state):
    mydb = mysql.connector.connect(host="localhost",user="root",password="")

    print(mydb)
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute('show databases')
    for i in mycursor:
        print(i)

    #===========================PLOT_1=============================>>>>>>>>>>>>>>>

    query1= f'''Select Districts, SUM(registereduser) AS registereduser
                from phonepe.{table_name}
                where states= '{state}'
                group by Districts
                order by registereduser DESC
                LIMIT 10;'''

    mycursor.execute(query1)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns= ("Districts","registereduser"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount_1=px.bar(df_1, x="Districts", y="registereduser", title="TOP 10 REGISTERED USER", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount_1)

    #===============================PLOT_2======================>>>>>>>>>>>>

    query2= f'''Select Districts, SUM(registereduser) AS registereduser
                from phonepe.{table_name}
                where states= '{state}'
                group by Districts
                order by registereduser
                LIMIT 10;'''

    mycursor.execute(query2)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns= ("Districts","registereduser"))

    with col2:

        fig_amount_2=px.bar(df_2, x="Districts", y="registereduser", title="LAST 10 REGISTERED USER", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)
        
    #=================================PLOT_3=============================>>>>>>>>>>

    query3= f'''Select Districts, AVG(registereduser) AS registereduser
                from phonepe.{table_name}
                where states= '{state}'
                group by Districts
                order by registereduser;'''

    mycursor.execute(query3)
    table_3=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns= ("Districts","registereduser"))

    fig_amount_3=px.bar(df_3, x="registereduser", y="Districts", title="AVERAGE OF REGISTERED USER", hover_name= "Districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

# SQL_APPOPENS
def top_chart_appopens(table_name, state):
    mydb = mysql.connector.connect(host="localhost",user="root",password="")

    print(mydb)
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute('show databases')
    for i in mycursor:
        print(i)

    #PLOT_1

    query1= f'''Select Districts, SUM(AppOpens) AS AppOpens
                from phonepe.{table_name}
                where states= '{state}'
                group by Districts
                order by AppOpens DESC
                LIMIT 10;'''

    mycursor.execute(query1)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns= ("Districts","AppOpens"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount_1=px.bar(df_1, x="Districts", y="AppOpens", title="TOP 10 APPOPENS", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount_1)

    #PLOT_2

    query2= f'''Select Districts, SUM(AppOpens) AS AppOpens
                from phonepe.{table_name}
                where states= '{state}'
                group by Districts
                order by AppOpens
                LIMIT 10;'''

    mycursor.execute(query2)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns= ("Districts","AppOpens"))

    with col2:

        fig_amount_2=px.bar(df_2, x="Districts", y="AppOpens", title="LAST 10 APPOPENS", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)
        
    #PLOT_3

    query3= f'''Select Districts, AVG(AppOpens) AS AppOpens
                from phonepe.{table_name}
                where states= '{state}'
                group by Districts
                order by AppOpens;'''

    mycursor.execute(query3)
    table_3=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns= ("Districts","AppOpens"))

    fig_amount_3=px.bar(df_3, x="AppOpens", y="Districts", title="AVERAGE OF APPOPENS", hover_name= "Districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

# SQL_chart_registered_users
def top_chart_registered_users(table_name):
    mydb = mysql.connector.connect(host="localhost",user="root",password="")

    print(mydb)
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute('show databases')
    for i in mycursor:
        print(i)

    #PLOT_1

    query1= f'''Select states, SUM(registeredusers) AS registeredusers
                from phonepe.{table_name}
                group by states
                order by registeredusers DESC
                LIMIT 10;'''

    mycursor.execute(query1)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns= ("states","registeredusers"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount_1=px.bar(df_1, x="states", y="registeredusers", title="TOP 10 REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount_1)

    #PLOT_2

    query2= f'''Select states, SUM(registeredusers) AS registeredusers
                from phonepe.{table_name}                
                group by states
                order by registeredusers
                LIMIT 10;'''

    mycursor.execute(query2)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns= ("states","registeredusers"))

    with col2:

        fig_amount_2=px.bar(df_2, x="states", y="registeredusers", title="LAST 10 REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)
        
    #PLOT_3

    query3= f'''Select states, AVG(registeredusers) AS registeredusers
                from phonepe.{table_name}                
                group by states
                order by registeredusers;'''

    mycursor.execute(query3)
    table_3=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns= ("states","registeredusers"))

    fig_amount_3=px.bar(df_3, x="registeredusers", y="states", title="AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

#streamlit part

st.set_page_config(layout="wide")
st.title("PhonePe Data Visualization and Exploration")

with st.sidebar:
    
    select= option_menu("Main Menu",["HOME","Data Exploration","Top Charts"])

if select=="HOME":
    
    # About PAGE

    col1, col2, = st.columns(2)
    col1.image(Image.open("C:/Users/Green Events/Desktop/Phonepe/phonepe img.jpg"), width=600)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.markdown("[DOWNLOAD APP](https://www.phonepe.com/app-download/)")
    with col2:
        st.title(':violet[PHONEPE PULSE DATA VISUALISATION]')
        st.subheader(':violet[Phonepe Pulse]:')
        st.write('PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app.')
        st.subheader(':violet[Phonepe Pulse Data Visualisation]:')
        st.write('Data visualization refers to the graphical representation of data using charts, graphs, and other visual elements to facilitate understanding and analysis in a visually appealing manner.'
                'The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.')
        st.markdown("## :violet[Created By] : Tamizanban H")
          
       
elif select=="Data Exploration":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis","Map Analysis", "Top Analysis"])

    with tab1 :
        method=st.radio("Select The Method",["Insurance Analysis","Transaction Analysis","User Analysis"])

        if method=="Insurance Analysis":

            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y=Transaction_amount_count_Y(Aggre_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y,quarters)

        elif method=="Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States",Aggre_tran_tac_Y["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_Ty",Aggre_tran_tac_Y_Q["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q,states)

        elif method=="User Analysis":
            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot_1(Aggre_user,years)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States",Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)


    with tab2:
        method_2=st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

        if method_2=="Map Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_MI",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
            map_insur_tac_Y=Transaction_amount_count_Y(Map_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_MI",map_insur_tac_Y["States"].unique())

            map_insur_District(map_insur_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_MI",map_insur_tac_Y["Quarter"].min(),map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min())
            map_insur_tac_Y_Q= Transaction_amount_count_Y_Q(map_insur_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_MI",map_insur_tac_Y_Q["States"].unique())

            map_insur_District(map_insur_tac_Y_Q,states)


        elif method_2=="Map Transaction":
            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_MT",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
            map_tran_tac_Y=Transaction_amount_count_Y(Map_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_MT",map_tran_tac_Y["States"].unique())

            map_insur_District(map_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_MT",map_tran_tac_Y["Quarter"].min(),map_tran_tac_Y["Quarter"].max(),map_tran_tac_Y["Quarter"].min())
            map_tran_tac_Y_Q= Transaction_amount_count_Y_Q(map_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_T",map_tran_tac_Y_Q["States"].unique())

            map_insur_District(map_tran_tac_Y_Q,states)

        elif method_2=="Map User":
            
            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_MU",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            map_user_Y=map_user_plot_1(Map_user,years)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_MU",map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_MU",map_user_Y_Q["States"].unique())

            map_user_plot_3(map_user_Y_Q, states)

    with tab3:
        method_3=st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

        if method_3=="Top Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_TI",top_insurance["Years"].min(),top_insurance["Years"].max(),top_insurance["Years"].min())
            top_insur_tac_Y=Transaction_amount_count_Y(top_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_TI",top_insur_tac_Y["States"].unique())

            Top_insurance_plot_1(top_insur_tac_Y, states)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_TI",top_insur_tac_Y["Quarter"].min(),top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())
            top_insur_tac_Y_Q= Transaction_amount_count_Y_Q(top_insur_tac_Y,quarters)



        elif method_3=="Top Transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_Tt",top_transaction["Years"].min(),top_transaction["Years"].max(),top_transaction["Years"].min())
            top_tran_tac_Y=Transaction_amount_count_Y(top_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_Tt",top_tran_tac_Y["States"].unique())

            Top_insurance_plot_1(top_tran_tac_Y, states)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_Tt",top_tran_tac_Y["Quarter"].min(),top_tran_tac_Y["Quarter"].max(),top_tran_tac_Y["Quarter"].min())
            top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(top_tran_tac_Y,quarters)
        
        elif method_3=="Top User":
            
            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_TU",top_user["Years"].min(),top_user["Years"].max(),top_user["Years"].min())
            top_user_Y=top_user_plot_1(top_user,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_TU",top_user_Y["States"].unique())

            top_user_plot_2(top_user_Y, states)

elif select=="Top Charts":
    
    question= st.selectbox("Select The Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                 "2. Transaction Amount and Count of Map Insurance",
                                                 "3. Transaction Amount and Count of Top Insurance",
                                                 "4. Transaction Amount and Count of Aggregated Transaction",
                                                 "5. Transaction Amount and Count of Map Transaction",
                                                 "6. Transaction Amount and Count of Top Transaction",
                                                 "7. Transaction Count of Aggregated User",
                                                 "8. Registered users of Map user",
                                                 "9. App opens of Map User",
                                                 "10. Registered user of Top User"])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question == "6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "8. Registered users of Map user":
        
        states=st.selectbox("Select The State", Map_user["States"].unique())
        st.subheader("REGISTERED USER")
        top_chart_registered_user("map_user", states)

    elif question == "9. App opens of Map User":
        
        states=st.selectbox("Select The State", Map_user["States"].unique())
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)

    elif question == "10. Registered user of Top User":
        
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")