import streamlit as st
import matplotlib.pyplot as plt
import numpy as np 
import time as t
st.set_option('deprecation.showPyplotGlobalUse', False)
st.write("Created by Juan Rossi")
st.write("""
   # Portfolio Return and Volatility calculation
""")
s1_r, s1_std = st.beta_columns(2)
with s1_r:
    s1_r = float(st.text_input("Enter Expected return of asset 1", "0.1"))
with s1_std:
    s1_std = float(st.text_input("Enter Standard Deviation of asset 1", "0.15"))

s2_r, s2_std = st.beta_columns(2)
with s2_r:
    s2_r = float(st.text_input("Enter Expected return of asset 2", "0.2"))
with s2_std:
    s2_std = float(st.text_input("Enter Standard Deviation of asset 2", "0.22"))

correl = float(st.slider("Enter correlation between asset 1 and 2", -1.0, 1.0,step=0.01))
covar = s1_std*s2_std*correl


def port_std(s1_std, s2_std, w1, w2, correl):
    return np.sqrt((s1_std**2)*(w1**2)+(s2_std**2)*(w2**2)+2*w1*w2*s1_std*s2_std*correl)
def port_r(s1_r, s2_r, w1, w2):
    return s1_r*w1+s2_r*w2
n, short = st.beta_columns(2)
with n:
    n = int(st.text_input("Number of portfolios to plot", "20"))
with short:
    short = st.selectbox("Short-selling", ("Allowed", "Not Allowed"))
def plot(n, short):
    stds = []
    r = []
    if short == "Allowed":
        start, stop = -1, 2
    else:
        start, stop =  0, 1
    weights = np.linspace(start,stop,n)
    for i in weights:      
        stds.append(port_std(s1_std, s2_std, i, 1-i, correl))
        r.append(port_r(s1_r, s2_r, i, 1-i))
    plt.scatter(stds, r, c=weights)
    plt.colorbar()
    plt.scatter(s1_std, s1_r)
    plt.scatter(s2_std, s2_r)
    plt.xlabel("Standard deviation")
    plt.ylabel("Expected Return")
    plt.grid(True)
    plt.legend(["Portfolios", "Asset 1", "Asset 2"])
    st.pyplot()
    return stds, r
        
if st.button("Plot portfolios"):
    data = plot(n, short)
    min_var_weight = (s2_std**2-covar)/(s1_std**2+s2_std**2-2*covar)
    min_std = float(port_std(s1_std, s2_std, min_var_weight, 1-min_var_weight, correl))
    st.write("The colorbar corresponds to the weight of asset 1")
    st.write("Minimum std: {}, with weight 1: {}%".format(round(min_std,2), round(min_var_weight*100,2)))
