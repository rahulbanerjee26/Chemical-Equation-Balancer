from helpers import balance
import streamlit as st 


equation = st.text_input(label="Enter Chemical Equation",value="Al2(CO3)3 + H3PO4 -> AlPO4 + CO2 + H2O")


st.subheader( balance(equation))


        
