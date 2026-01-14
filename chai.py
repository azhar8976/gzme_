import streamlit as st

st.title("Azzu Chai Wala")

if st.button("Make Chai"):
    st.success("Your chai is being brewed")

add_masala = st.checkbox("Add Masala")
if add_masala:
    st.write("Masala added to your chai")  

tea_type = st.radio("Pick your chai base:", ["Milk", "Water", "Almond Mlilk"]) 
st.write(f"Selected base {tea_type}")
flavour = st.selectbox("Choose flavour:", ["Adrak", "Kesar", "Tulsi"])     
st.write(f"Selected Flavour {flavour}") 

sugar = st.slider("Sigar level(spoon)", 0, 5, 4)
st.write(f"Selected sugar level {sugar}")

cups = st.number_input(
    "How many cups",
    value=1,
    min_value=1,
    max_value=10,
    step=1
)
name = st.text_input("Enter your name")
if name:
    st.write(f"Welcome, {name} ! Your chai is on the way")

dob = st.date_input(f"Select your date of birth")
st.write(f"Your date of birth {dob}")    

calculetor = st.number_input("Total amount is", min_value=0)
st.write("You entered:", calculetor)
