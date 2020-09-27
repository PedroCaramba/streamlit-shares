#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:37:25 2020

@author: jeanlouisdendal
"""

import yfinance as yf
import streamlit as st
#import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta


def main():         
    #create the subheader 
    st.sidebar.title("Stock - Closing Price & Volume 📈 ")

    st.sidebar.subheader("Choose Stock")
    stock = st.sidebar.selectbox("Stocks", ("Apple (AAPL)", 
                                            "Baxter (BAX)"))

    st.sidebar.subheader("Choose Period")
    period = st.sidebar.selectbox("Periods", ("3 Months", 
                                          "6 Months",
                                          "1 Year",
                                          "2 Years",
                                          "5 Years"
                                          ))
    												  
    #update tickerSymbol with the choosen stock in the sidebar
    if stock == 'Apple (AAPL)':    
        tickerSymbol = 'AAPL'
    
    if stock == 'Baxter (BAX)':    
        tickerSymbol = 'BAX'
    
    
    #get data on this tickerSymbol
    tickerData = yf.Ticker(tickerSymbol)


    #get the historical prices for this tickerSymbol (Only one time request)
    @st.cache(persist=True)
    def load_data(tickerData):  
        tickerDf =  tickerData.history(period="5y", interval='1d')
        return tickerDf
    
    #load data based on a 5 years period as stated in the function
    tickerDf = load_data(tickerData)
    
    #extract the last date of the dataframe index (tickerDf)
    lastDate = tickerDf.index.max()
        
    #create dataframe slice based on the choosen period in the sidebar
    if period == '3 Months':
        firstDate = lastDate - timedelta(weeks=13) 
        tickerDfTemp = tickerDf.loc[firstDate.strftime('%Y-%m-%d'):lastDate.strftime('%Y-%m-%d')]
    if period == '6 Months':
        firstDate = lastDate - timedelta(weeks=26) 
        tickerDfTemp = tickerDf.loc[firstDate.strftime('%Y-%m-%d'):lastDate.strftime('%Y-%m-%d')]  
    if period == '1 Year':
        firstDate = lastDate - timedelta(weeks=52) 
        tickerDfTemp = tickerDf.loc[firstDate.strftime('%Y-%m-%d'):lastDate.strftime('%Y-%m-%d')]  
    if period == '2 Years':
        firstDate = lastDate - timedelta(weeks=104) 
        tickerDfTemp = tickerDf.loc[firstDate.strftime('%Y-%m-%d'):lastDate.strftime('%Y-%m-%d')]  
    if period == '5 Years':
        firstDate = lastDate - timedelta(weeks=260) 
        tickerDfTemp = tickerDf.loc[firstDate.strftime('%Y-%m-%d'):lastDate.strftime('%Y-%m-%d')]  
    
    #display information
    st.title(f"{stock} - {period}.")

    st.write(""" ***Closing Price*** 📈 """)   
    #a la demande de Frédéric
    fig, ax = plt.subplots()
    ax.plot(tickerDfTemp.Close)
    ax.tick_params(axis='x', rotation=30)
    plt.grid(axis='x', color='0.95')
    plt.grid(axis='y', color='0.95')
    st.pyplot(fig)
    #st.line_chart(tickerDfTemp.Close)

    st.write(""" ***Volume*** 📈 """)
    st.line_chart(tickerDfTemp.Volume)
        
    if st.sidebar.checkbox("Show raw data", False):
        st.subheader("Stock Data Set ")
        st.write(tickerDfTemp)


if __name__=='__main__':
    main()