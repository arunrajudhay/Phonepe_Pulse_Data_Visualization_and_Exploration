import os
import json
import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu
import plotly.express as px
import requests

#Streamlit Page Setting
slt.set_page_config(layout="wide")
with slt.sidebar:
    web=option_menu(menu_title="Exploring data",
                    options=["Home","About","GEO-VISUALIZATION","Insights"],
                    icons=["house","info-circle","globe","bar-chart"],
                    )
if web=="Home":
    slt.title("Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly")
    slt.subheader(":violet[Domain:]  FinTech")
    slt.subheader(":violet[Overview:]") 
    slt.markdown("Git: Utilized Git for version control and team collaboration, facilitating the efficient cloning of the PhonePe dataset from GitHub..")
    slt.markdown('''Pandas: Use the powerful Pandas library to transform the dataset from JSON format into a structured dataframe.
                    Pandas helps data manipulation, cleaning, and preprocessing, ensuring that data was ready for analysis.''')
    slt.markdown('''MySQL: With help of SQL to establish a connection to a SQL database, enabling seamless integration of the transformed dataset
                    and the data was efficiently inserted into relevant tables for storage and retrieval.''')
    slt.markdown("Streamlit: Developed an interactive web application using Streamlit, a user-friendly framework for data visualization and analysis.")
    slt.markdown('''Plotly: Integrated Plotly, a versatile plotting library, to generate insightful visualizations from the dataset. Plotly's interactive plots,
                    including geospatial plots and other data visualizations, provided users with a comprehensive understanding of the dataset's contents''')
    slt.subheader(":violet[Skill-take:]")
    slt.markdown("Github Cloning, Python, Pandas, MySQL,mysql-connector-python, Streamlit, and Plotly.")
    slt.subheader(":violet[Developed-by:]  ARUNRAJ R U")
if web=="About":
    col1,col2=slt.columns(2)
    with col1:
        slt.subheader(":violet[What is phonepe]")
        slt.markdown('''The PhonePe app is accessible in 11 Indian languages. It enables users to perform various financial 
                     transactions such as sending and receiving money, recharging mobile and DTH, making utility payments, 
                     conducting in-store payments. PhonePe was incorporated in December 2015.''')
        slt.subheader(":violet[What is phonepe-pulse]")
        slt.markdown('''PhonePe has launched the country’s first geospatial website ‘Pulse’ that will offer comprehensive data 
                     on digital payment trends. The site will reveal digital transaction habits of over 30 million Indians down 
                     to the district level.''')
    with  col2:
         slt.subheader("This project is inspired from")
         slt.link_button("Link","https://www.phonepe.com/pulse/explore/transaction/2022/4/")

#Analysis and Geo-Visualization
if web=="GEO-VISUALIZATION":
        def map_geo():
                       map_url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                       response = requests.get(map_url)
                       map_data = response.json()
                       return map_data
        tab1,tab2,tab3=slt.tabs(["Yearly Analysis","Quaterly Analysis","State Analysis"])

        #Yearly-Analysis
        with tab1:
            A=slt.selectbox("select",["Transaction","User"])
            if A=="Transaction":
                agg_year=slt.select_slider("Years",["2018","2019","2020","2021","2022","2023","2024"])
                col1,col2=slt.columns(2)
                with col1:    
                    def agg_year1(year):
                            conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                            my_cursor = conn.cursor()
                            my_cursor.execute(f'''select State,sum(Transaction_amount) from agg_trans
                                                where year = "{year}" group by State
                                                order by sum(Transaction_amount) desc ''')
                            out=my_cursor.fetchall()
                            df_agg=pd.DataFrame(out,columns=["State","Total_Transaction_amount"])
                            return df_agg
                    df_agg=agg_year1(agg_year)
                    slt.write(f'Total Transaction amount by State in {agg_year}')
                    slt.write(df_agg)
                    fix=px.choropleth(df_agg,geojson=map_geo(),featureidkey='properties.ST_NM',
                                    locations='State',color='Total_Transaction_amount',color_continuous_scale='Viridis',
                                    range_color=(df_agg["Total_Transaction_amount"].min(),
                                                 df_agg["Total_Transaction_amount"].max(),),
                                                 hover_name='State',height=600,width=800,
                                    title=f"Total Transaction Amount by State in {agg_year}",)
                    fix.update_geos(fitbounds='locations', visible=False)
                    slt.plotly_chart(fix)
                with col2:
                    fix=px.bar(df_agg,x="State",y="Total_Transaction_amount",title=f"Total Transaction Amount by State in {agg_year}",
                                color_discrete_sequence=px.colors.sequential.Plasma,height=577)
                    slt.plotly_chart(fix)
            if A=="User":
                agg_year_M=slt.select_slider("Years",["2018","2019","2020","2021","2022","2023","2024"])
                col1,col2=slt.columns(2)
                with col1:
                    def map_U_year(year):
                        conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                        my_cursor = conn.cursor()
                        my_cursor.execute(f'''select State,sum(user_count) from agg_user
                                                    where year = "{year}" group by State
                                                    order by sum(user_count )desc ''')
                        out=my_cursor.fetchall()
                        df_mapU=pd.DataFrame(out,columns=["State","Total_User_amount"])
                        return df_mapU
                    df_mapU=map_U_year(agg_year_M)
                    slt.write(f'Total User amount by State in {agg_year_M}')
                    slt.write(df_mapU)
                    fix=px.choropleth(df_mapU,geojson=map_geo(),featureidkey='properties.ST_NM',
                                locations='State',color='Total_User_amount',color_continuous_scale='Rainbow',
                                hover_name='State',height=600,width=777,
                                range_color=(df_mapU['Total_User_amount'].min(),
                                                                df_mapU['Total_User_amount'].max()),
                                title=f"Total User amount by State in {agg_year_M}",)
                    fix.update_geos(fitbounds='locations', visible=False)
                    slt.plotly_chart(fix) 
                with col2:
                    fix=px.bar(df_mapU,x="State",y="Total_User_amount",title=f"Total User amount by State in {agg_year_M}",
                                color_discrete_sequence=px.colors.sequential.Viridis,height=550)
                    slt.plotly_chart(fix)

        #Quaterly-Analysis               
        with tab2:
          S=slt.radio("select",["Aggregated","Map","Top"])
          if S=="Aggregated":
            option_1=slt.selectbox("option",["Insurance","Transaction","User"])
            if option_1=="Insurance":
                    Y_I=slt.select_slider("Year",["2021","2022","2023","2024"])
                    Q_Y=slt.selectbox("Quater",["Q1","Q2","Q3","Q4"])
                    quater_map = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                    quater_value = quater_map[Q_Y]
                    col1,col2=slt.columns(2)
                    with col1:
                        def agg_insurance_yearQ1(year,quater):
                                conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                                my_cursor = conn.cursor()
                                my_cursor.execute(f'''select State,sum(Transaction_amount) from agg_inc 
                                                        where Year="{year}"and Quater={quater} group by State
                                                    order by sum(Transaction_amount) desc ''')
                                out=my_cursor.fetchall()
                                dfQ_ins=pd.DataFrame(out,columns=["State","Total_Transaction_amount"])
                                return dfQ_ins
                        dfQ_ins=agg_insurance_yearQ1(Y_I,quater_value)
                        slt.write(f'{Q_Y} Transaction_amount by State in {Y_I}')
                        slt.write(dfQ_ins)
                        fix=px.choropleth(dfQ_ins,geojson=map_geo(),featureidkey='properties.ST_NM',
                                    locations='State',color='Total_Transaction_amount',color_continuous_scale='Rainbow',
                                    hover_name='State',height=600,width= 1000,
                                    range_color=(dfQ_ins['Total_Transaction_amount'].min(),
                                                dfQ_ins['Total_Transaction_amount'].max()),
                                    title=f"{Q_Y} Total Total_Transaction_amount by State in {Y_I}",)
                        fix.update_geos(fitbounds='locations', visible=False)
                        slt.plotly_chart(fix)
                    with col2:
                        fix = px.bar(dfQ_ins, x="State", y="Total_Transaction_amount", title=f"{Q_Y} Transaction_amount-{Y_I}",color="State")
                        slt.plotly_chart(fix)
            
            if option_1=="Transaction":
                    Y_T=slt.select_slider("Year",["2018","2019","2020","2021","2022","2023","2024"])
                    Q_T=slt.selectbox("Quater",["Q1","Q2","Q3","Q4"])
                    quater_trans = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                    quater_value = quater_trans[Q_T]
                    col1,col2,col3=slt.columns(3) 
                    with col1:
                        def agg_transaction_year(year,quater):
                            conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                            my_cursor = conn.cursor()
                            my_cursor.execute(f'''select State,sum(Transaction_amount)as total_amount from agg_trans
                                                    where Year="{year}" and Quater={quater} group by State 
                                                    order by sum(Transaction_amount) desc ''')
                            out=my_cursor.fetchall()
                            dfQ_trans=pd.DataFrame(out,columns=["State","Total_Transaction_amount"])
                            return dfQ_trans
                        dfQ_trans=agg_transaction_year(Y_T,quater_value)
                        slt.write(f"{Q_T} Total Total_Transaction_amount by State in {Y_T}")
                        slt.write(dfQ_trans)
                        fix=px.choropleth(dfQ_trans,geojson=map_geo(),featureidkey='properties.ST_NM',
                                    locations='State',color='Total_Transaction_amount',color_continuous_scale='Rainbow',
                                    hover_name='State',height=500,width=900,
                                    range_color=(dfQ_trans['Total_Transaction_amount'].min(),
                                                dfQ_trans['Total_Transaction_amount'].max()),
                                    title=f"{Q_T} Total Total_Transaction_amount by State in {Y_T}",)
                        fix.update_geos(fitbounds='locations', visible=False)
                        slt.plotly_chart(fix)
                        with col2:
                            def agg_transaction_year(year,quater):
                                conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                                my_cursor = conn.cursor()
                                my_cursor.execute(f'''select Transaction_type,sum(Transaction_amount)as total_amount from agg_trans
                                                        where Year={year} and Quater={quater} group by Transaction_type 
                                                        order by sum(Transaction_amount) desc ''')
                                out=my_cursor.fetchall()
                                dfQ_trans=pd.DataFrame(out,columns=["Transaction_type","total_amount"])
                                return dfQ_trans
                            dfQ_trans=agg_transaction_year(Y_T,quater_value)
                            slt.write(dfQ_trans)
                        with col3:
                            fix=px.pie(dfQ_trans, values="total_amount",names="Transaction_type",title=f"{Q_T} Transaction_type-{Y_T}",height=400)
                            slt.plotly_chart(fix)
                  
            if option_1=="User":
                T_Y=slt.select_slider("Year",["2018","2019","2020","2021","2022","2023","2024"])
                Y_Q=slt.selectbox("Quater",["Q1","Q2","Q3","Q4"])
                quater_trans = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                quater_value = quater_trans[Y_Q]
                col1,col2=slt.columns(2)
                with col1:
                    def agg_user_year(year,quater):
                        conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                        my_cursor = conn.cursor()
                        my_cursor.execute(f'''select State,user_Brand,sum(user_count)as total_count from agg_user
                                                where Year={year} and Quater={quater} group by State,user_Brand
                                                order by total_count desc ''')
                        out=my_cursor.fetchall()
                        dfQ_user=pd.DataFrame(out,columns=["State","user_Brand","Total_count"])
                        return dfQ_user
                    dfQ_user=agg_user_year(T_Y,quater_value)
                    slt.write(f'{Y_Q} Total_count-{T_Y}')
                    slt.write(dfQ_user) 
                with col2:
                    fix = px.bar(dfQ_user, x="user_Brand", y="Total_count", title=f'{Y_Q} Total_count-{T_Y}',color="user_Brand")
                    slt.plotly_chart(fix)
          elif S=="Map":
            option_2=slt.selectbox("option",["Insurance","Transaction","User"])
            if option_2=="Insurance":
                Y_MI=slt.select_slider("Year",["2021","2022","2023","2024"])
                Y_QI=slt.selectbox("Quater",["Q1","Q2","Q3","Q4"])
                quater_trans = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                quater_value = quater_trans[Y_QI]
                col1,col2=slt.columns(2)
                with col1:
                    def map_insurance_year(year,quater):
                        conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                        my_cursor = conn.cursor()
                        my_cursor.execute(f'''select District,sum(Transaction_amount)as total_amount from map_inc
                                                where Year={year} and Quater={quater} group by District 
                                                order by sum(Transaction_amount) desc limit 36''')
                        out=my_cursor.fetchall()
                        dfQ_map_inc=pd.DataFrame(out,columns=["District","total_amount"])
                        return dfQ_map_inc
                    dfQ_map_inc=map_insurance_year(Y_MI,quater_value)
                    slt.write(dfQ_map_inc)
                with col2:
                    fix=px.bar(dfQ_map_inc,x="District",y="total_amount",title=f"Transaction_type-{Y_MI}",height=500,width=500)
                    slt.plotly_chart(fix)
            elif option_2=="Transaction":
                Y_MT=slt.select_slider("Year",["2018","2019","2020","2021","2022","2023","2024"])
                Y_QT=slt.selectbox("Quater",["Q1","Q2","Q3","Q4"])
                quater_trans = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                quater_value = quater_trans[Y_QT]
                def map_transaction_year(year,quater):
                    conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                    my_cursor = conn.cursor()
                    my_cursor.execute(f'''select District,sum(Transaction_amount)as total_amount from map_trans
                                        where Year={year} and Quater={quater} group by District
                                        order by sum(Transaction_amount) desc limit 40 ''')
                    out=my_cursor.fetchall()
                    dfT_map_trans=pd.DataFrame(out,columns=["District","total_amount"])
                    return dfT_map_trans
                dfT_map_trans=map_transaction_year(Y_MT,quater_value)
                slt.write(dfT_map_trans)
                fix=px.pie(dfT_map_trans, values="total_amount",names="District",title=f"Transaction_amount-{Y_MT}")
                slt.plotly_chart(fix)
            if option_2=="User":
                    Y_UT=slt.select_slider("Year",["2018","2019","2021","2022","2023","2024"])
                    Y_BT=slt.selectbox("Quater",["Q1","Q2","Q3","Q4"])
                    quater_trans = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                    quater_value = quater_trans[Y_BT]
                    def map_user(year,quater):
                        conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                        my_cursor = conn.cursor()
                        my_cursor.execute(f'''select District,sum(Registered_Users) as Total_user from map_user
                                                    where Year={year} and Quater={quater} group by District
                                                    order by Total_user desc limit 50''')
                        out=my_cursor.fetchall()
                        df_map_user1=pd.DataFrame(out,columns=["District","Total_user"])
                        return df_map_user1
                    df_map_user1=map_user(Y_UT,quater_value)
                    slt.write(df_map_user1)
                    fix=px.pie(df_map_user1, values="Total_user",names="District",title=f"Registered_Users-{Y_UT}")
                    slt.plotly_chart(fix)
                    
          elif S=="Top":
                option_3=slt.selectbox("option",["Insurance","Transaction","User"])
                if option_3=="Insurance":
                    Y_TI=slt.select_slider("Year",["2021","2022","2023","2024"])
                    Y_TQ=slt.selectbox("Quater",["Q1","Q2","Q3","Q4"])
                    quater_trans = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                    quater_value = quater_trans[Y_TQ]  
                    def top_insurance_year(year,quater):
                        conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                        my_cursor = conn.cursor()
                        my_cursor.execute(f'''select State,Pincode,sum(Transaction_amount)as total_amount from top_inc
                                                where Year={year} and Quater={quater}  group by Pincode,State
                                                order by sum(Transaction_amount) desc limit 200''')
                        out=my_cursor.fetchall()
                        dft_top_ins=pd.DataFrame(out,columns=["State","Pincode","total_amount"])
                        return dft_top_ins
                    dft_top_ins=top_insurance_year(Y_TI,quater_value)
                    slt.write(dft_top_ins)
                    
                elif option_3=="Transaction":
                    Y_TT=slt.select_slider("Year",["2018","2019","2020","2021","2022","2023","2024"])
                    Y_A=slt.selectbox("Quater",["Q1","Q2","Q3","Q4"])
                    quater_trans = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                    quater_value = quater_trans[Y_A]
                    def top_transaction_year(year,quater):
                        conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                        my_cursor = conn.cursor()
                        my_cursor.execute(f'''select State,Pincode,sum(Transaction_amount)as total_amount from top_trans
                                                where Year={year} and Quater={quater} group by Pincode,State
                                                order by sum(Transaction_amount) desc limit 50
                                            ''')
                        out=my_cursor.fetchall()
                        dfA_top_trans=pd.DataFrame(out,columns=["State","Pincode","total_amount"])
                        return dfA_top_trans
                    dfA_top_trans=top_transaction_year(Y_TT,quater_value)
                    slt.write(dfA_top_trans)
                if option_3=="User":
                    Y=slt.select_slider("Year",["2018","2019","2020","2021","2022","2023","2024"])
                    Y_B=slt.selectbox("Quater",["Q1","Q2","Q3","Q4"])
                    quater_trans = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
                    quater_value = quater_trans[Y_B] 
                    def top_user(year,quater):
                        conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                        my_cursor = conn.cursor()
                        my_cursor.execute(f'''select State,Pincode,sum(Registered_Users) as Total_user from top_user
                                                    where Year={year} and Quater={quater} group by Pincode,State
                                                    order by Total_user desc ''')
                        out=my_cursor.fetchall()
                        df_top_user1=pd.DataFrame(out,columns=["State","Pincode","Total_user"])
                        return df_top_user1
                    df_top_user1=top_user(Y,quater_value)
                    slt.write(df_top_user1,width=1000)

        #State-Analysis            
        with tab3:
             def states():
                conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                my_cursor = conn.cursor()
                my_cursor.execute("select State from agg_trans")
                out=my_cursor.fetchall()
                df=pd.DataFrame(out,columns=["States"])
                S=df["States"].unique()
                return S
             S=states()
             S_A=slt.selectbox("List of States",S)
             Y_S=slt.select_slider("YearS",["2018","2019","2020","2021","2022","2023","2024"])
             Y_SQ=slt.selectbox("QuaterS",["Q1","Q2","Q3","Q4"])
             quater_trans = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
             quater_value = quater_trans[Y_SQ]

             def state_transaction(states_L,year,quater):
                conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                my_cursor = conn.cursor()
                query=('''select State, sum(Transaction_amount) as total_transaction_amount from agg_trans
                                  where State= %s and Year= %s and Quater=%s  group by State
                                  order by total_transaction_amount ''')
                output=my_cursor.execute(query,(states_L,year,quater))
                out=my_cursor.fetchall()
                df_S=pd.DataFrame(out,columns=["State","total_transaction_amount"])
                return df_S
             df_S=state_transaction(S_A,Y_S,quater_value)
             slt.write(f'State-wise total transaction amount {S_A}-{Y_S}-{Y_SQ}')
             slt.write(df_S)
             col1,col2=slt.columns(2)
             with col1:
                def Type_transaction(states_L,year,quater):
                    conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                    my_cursor = conn.cursor()
                    query=('''select State,Transaction_type,sum(Transaction_amount) as total_transaction_amount from agg_trans
                                    where State= %s and Year= %s and Quater= %s group by Transaction_type,State
                                    order by total_transaction_amount ''')
                    output=my_cursor.execute(query,(states_L,year,quater))
                    out=my_cursor.fetchall()
                    df_T=pd.DataFrame(out,columns=["State","Transaction_type","total_transaction_amount"])
                    return df_T
                df_T=Type_transaction(S_A,Y_S,quater_value)
                slt.write(f'State-wise total transaction amount and type "{S_A}"')
                slt.write(df_T)
             with col2:
              fix=px.pie(df_T,values="total_transaction_amount",names="Transaction_type",title=f'State-wise total transaction amount and type {S_A}-{Y_S}-{Y_SQ}')
              slt.plotly_chart(fix)
             def User_transaction(states_L,year,quater):
                conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                my_cursor = conn.cursor()
                query=('''select State,sum(Registered_Users) as total_Registered_Users from map_user
                                  where State= %s and Year= %s and Quater= %s group by State
                                  order by total_Registered_Users ''')
                output=my_cursor.execute(query,(states_L,year,quater))
                out=my_cursor.fetchall()
                df_U=pd.DataFrame(out,columns=["State","total_Registered_Users"])
                return df_U
             df_U=User_transaction(S_A,Y_S,quater_value)
             slt.write(f'State-wise total_Registered_Users {S_A}-{Y_S}-{Y_SQ}')
             slt.write(df_U)          
#Analysis for 10-Questions
if web=="Insights":
    slt.subheader("select questions to get insight")
    Questions=slt.selectbox("select option",("1.Top 20 aggregate insurance-transaction amount in state wise?",
                                             "2.Top most aggregate transaction-count in state wise?",
                                             "3.Top most map transaction count in district wise?",
                                             "4.Top most register user in district wise?",
                                             "5.Top most register user in pincode wise?",
                                             "6.Top most brand user in transaction?",
                                             "7.lowest top-transaction amount in state wise?",
                                             "8.avg transaction amount in Tamilnadu?",
                                            "9.which year has highest transaction in Karnataka?",
                                             "10.app opens in map_user?" ))
    if Questions=="1.Top 20 aggregate insurance-transaction amount in state wise?":
       if slt.button("SUBMIT"):
            conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
            my_cursor = conn.cursor()
            my_cursor.execute('''select State,sum(Transaction_amount)as total_amount from agg_inc
                              group by State 
                            order by sum(Transaction_amount) desc ''')
            out=my_cursor.fetchall()
            que_1=pd.DataFrame(out,columns=["State","total_amount"])
            slt.success("ANSWER")
            slt.write(que_1)

            fix=px.bar(que_1, x="State",y="total_amount",title="Transaction_amount",color="State",width=1000,height=600)
            slt.plotly_chart(fix)

    if Questions=="2.Top most aggregate transaction-count in state wise?":
       if slt.button("SUBMIT"):
            conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
            my_cursor = conn.cursor()
            my_cursor.execute('''select Transaction_type,sum(Transaction_count) as count from agg_trans
                              group by Transaction_type
                            order by sum(Transaction_count) desc ''')
            out=my_cursor.fetchall()
            que_2=pd.DataFrame(out,columns=["Transaction_type","count"])
            slt.success("ANSWER")
            slt.write(que_2)
            
            fix=px.bar(que_2, x="Transaction_type",y="count",title="Transaction_type",color="Transaction_type")
            slt.plotly_chart(fix)
            
    if Questions=="3.Top most map transaction count in district wise?":
       if slt.button("SUBMIT"):
            conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
            my_cursor = conn.cursor()
            my_cursor.execute('''select District,sum(Transaction_count)as total_count from map_trans
                              group by District
                            order by sum(Transaction_count) desc limit 10''')
            out=my_cursor.fetchall()
            que_3=pd.DataFrame(out,columns=["District","Total_count"])
            slt.success("ANSWER")
            slt.write(que_3)

            fix=px.bar(que_3, x="District",y="Total_count",title="Transaction_count",color="District")
            slt.plotly_chart(fix)

    if Questions=="4.Top most register user in district wise?":
        if slt.button("SUBMIT"):
                conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                my_cursor = conn.cursor()
                my_cursor.execute('''select District,sum(Registered_Users) as total_user from map_user
                                  group by District
                                order by sum(Registered_Users) desc limit 20''')
                out=my_cursor.fetchall()
                que_4=pd.DataFrame(out,columns=["District","total_user"])
                slt.success("ANSWER")
                slt.write(que_4)

                fix=px.bar(que_4, x="District",y="total_user",title="Registered_Users",color="District")
                slt.plotly_chart(fix)
        
    if Questions=="5.Top most register user in pincode wise?":
        if slt.button("SUBMIT"):
                conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                my_cursor = conn.cursor()
                my_cursor.execute('''select State,Pincode,sum(Registered_Users) as total_user from top_user
                                  group by pincode,State
                                order by sum(Registered_Users) desc limit 20''')
                out=my_cursor.fetchall()
                que_5=pd.DataFrame(out,columns=["State","Pincode","total_user"])
                slt.success("ANSWER")
                slt.write(que_5)

                fix=px.bar(que_5, x="State",y="total_user",title="Registered_Users",color="Pincode")
                slt.plotly_chart(fix)

    if Questions=="6.Top most brand user in transaction?":
        if slt.button("SUBMIT"):
                conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                my_cursor = conn.cursor()
                my_cursor.execute('''select user_Brand,sum(user_count) as "count" from agg_user
                                  Group by user_Brand
                                order by sum(user_count) desc limit 20''')
                out=my_cursor.fetchall()
                que_6=pd.DataFrame(out,columns=["user_Brand","count"])
                slt.success("ANSWER")
                slt.write(que_6)

                fix=px.bar(que_6, x="user_Brand",y="count",title="user_Brand",color="user_Brand")
                slt.plotly_chart(fix)
                
    if Questions=="7.lowest top-transaction amount in state wise?":
        if slt.button("SUBMIT"):
                conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                my_cursor = conn.cursor()
                my_cursor.execute('''select State,sum(Transaction_amount) as lowest_amount from agg_trans
                                  group by State
                                  order by sum(Transaction_amount) limit 500''')
                out=my_cursor.fetchall()
                que_7=pd.DataFrame(out,columns=["State","lowest_amount"])
                slt.success("ANSWER")
                slt.write(que_7)

                fix=px.bar(que_7, x="State",y="lowest_amount",title="Transaction_amount",color="State")
                slt.plotly_chart(fix)

    if Questions=="8.avg transaction amount in Tamilnadu?":
        if slt.button("SUBMIT"):
                conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                my_cursor = conn.cursor()
                my_cursor.execute('''select State,avg(Transaction_amount) as avg_amount 
                                  from agg_trans where State="Tamil Nadu"
                                  Group by State
                                order by avg(Transaction_amount) limit 20''')
                out=my_cursor.fetchall()
                que_8=pd.DataFrame(out,columns=["State","avg_amount"])
                slt.success("ANSWER")
                slt.write(que_8)
    if Questions=="9.which year has highest transaction in Karnataka?":
        if slt.button("SUBMIT"):
                conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                my_cursor = conn.cursor()
                my_cursor.execute('''select State,Year,max(Transaction_amount) as max_amount
                                  from agg_trans where State="Karnataka"
                                  group by year
                                order by max(Transaction_amount) desc limit 20''')
                out=my_cursor.fetchall()
                que_9=pd.DataFrame(out,columns=["State","Year","max_amount"])
                slt.success("ANSWER")
                slt.write(que_9)

                fix=px.bar(que_9, x="Year",y="max_amount",title="max_amount",color="Year")
                slt.plotly_chart(fix)

    if Questions=="10.app opens in map_user?":
        if slt.button("SUBMIT"):
                conn=mysql.connector.connect(host="localhost", user="root", password="Arunudhay2024",database="phonepe")
                my_cursor = conn.cursor()
                my_cursor.execute('''select State,sum(App_Opens) as total from map_user
                                  group by State
                                order by sum(App_Opens) desc ''')
                out=my_cursor.fetchall()
                que_10=pd.DataFrame(out,columns=["State","App_Opens"])
                slt.success("ANSWER")
                slt.write(que_10)

                fix=px.bar(que_10, x="State",y="App_Opens",title="App_Opens",color="State")
                slt.plotly_chart(fix)
    
    
    

