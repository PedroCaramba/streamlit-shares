#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 16:35:48 2020

@author: jeanlouisdendal
"""

import streamlit as st
import pandas as pd
from PIL import Image

import yfinance as yf
import matplotlib.pyplot as plt
from datetime import timedelta

# Security : passlib,hashlib,bcrypt,scrypt
import hashlib

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()

# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def main():
    image=Image.open("Bourse.jpg")
    newsize = (300, 50) 
    image = image.resize(newsize) 
    st.image(image, use_column_width=True)
    
    st.title("share and currency quotations")
    menu = ["Home","Login","SignUp"]
    choice = st.selectbox("Menu",menu)
    
    if choice == "Home":
        #st.subheader("share and currency quotations")
        pass
        
    elif choice == "Login":
        st.sidebar.subheader("Login")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        
        if st.sidebar.checkbox("Login"):
            #create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username,check_hashes(password,hashed_pswd))
            
            if result:
                #st.success("Logged In as {}".format(username))
                #st.sidebar.subheader("Choose Task")
                #task = st.sidebar.radio(label="", options=["Quotations", "Profiles"])
                #st.sidebar.empty()
                task = "Quotations"
                #st.info("Go to Task Menu")
                #session_state = SessionState.get(a=0, b=0)
                   
                           
                if task == "Profiles":
                   # session_state.a = float(st.text_input(label="What is a?", value=session_state.a))
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                    st.dataframe(clean_db)
                    st.table(clean_db)                
                elif task == "Quotations":
                    #session_state.b = float(st.text_input(label="What is b?", value=session_state.b))
                    st.sidebar.subheader("Choose Stock")
                    stock = st.sidebar.selectbox("Stocks", ("Apple (AAPL)", 
                                            "Baxter (BAX)",
                                            "Facebook (FB)",
                                            "Microsoft (MSFT)",
                                            "Eur-USD (EURUSD=X)"))
    
                    thisdict = {
                                "Apple (AAPL)": 'AAPL',
                                "Baxter (BAX)": 'BAX',
                                "Facebook (FB)": 'FB',
                                "Microsoft (MSFT)": 'MSFT',
                                "Eur-USD (EURUSD=X)": 'EURUSD=X'
                                }
                
                    st.sidebar.subheader("Choose Period")
                    period = st.sidebar.selectbox("Periods", ("3 Months", 
                                                          "6 Months",
                                                          "1 Year",
                                                          "2 Years",
                                                          "5 Years"
                                                          ))
                                        												  
                    #update tickerSymbol with the choosen stock in the sidebar
                    tickerSymbol = 'BAX'
                    tickerSymbol = thisdict.get(stock)
                    
                    #get data on this tickerSymbol
                    tickerData = yf.Ticker(tickerSymbol)
                
                
                    #get the historical prices for this tickerSymbol (Only one time request @st.cache(persist=True))
                    #@st.cache(persist=True)
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
                    
            else:
                 st.warning("Incorrect Username/Password")
        
                
    elif choice == "SignUp":
            st.subheader("Create New Account")
            new_user = st.text_input("Username")
            st.warning("Username should at least have 3 characters")        
            new_password = st.text_input("Password",type='password')
            
            if st.button("Signup"):
                if(len(new_user)<3):
                    st.error("Username do not have 3 characters")
                elif new_password[-3:] != "42#":
                    st.error("Password is no valid")            
                else:
                    create_usertable()
                    add_userdata(new_user,make_hashes(new_password))
                    st.success("You have successfully created a valid Account")
                    st.info("Go to Login Menu to login")
                    st.balloons()
            
if __name__ == '__main__':
    main()
    
                
	