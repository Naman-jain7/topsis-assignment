import streamlit as st
import pandas as pd
import numpy as np
import re
import smtplib
from email.message import EmailMessage
import tempfile
import os


def topsis(df, weights, impacts):
    data = df.iloc[:, 1:].values.astype(float)

    norm = np.sqrt((data**2).sum(axis=0))
    normalized = data / norm

    weighted = normalized * weights

    ideal_best = []
    ideal_worst = []

    for i in range(weighted.shape[1]):
        if impacts[i] == "+":
            ideal_best.append(np.max(weighted[:, i]))
            ideal_worst.append(np.min(weighted[:, i]))
        else:
            ideal_best.append(np.min(weighted[:, i]))
            ideal_worst.append(np.max(weighted[:, i]))

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(method="max", ascending=False).astype(int)

    return df

def check_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def send_email(receiver_email, file_path):
    sender_email="nj323875@gmail.com"
    app_password = "hqxx ckup ncbn qrka"

    msg=EmailMessage()
    msg['Subject']='TOPSIS Result'
    msg['From']=sender_email
    msg['To']=receiver_email
    msg.set_content('please find the attached file')

    with open(file_path,'rb') as f:
        file_data=f.read()
        file_name=os.path.basename(file_path)

    msg.add_attachment(file_data, maintype='application',subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

st.title('TOPSIS')

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
weights_input = st.text_input("Weights (comma separated)", "1,1,1,1")
impacts_input = st.text_input("Impacts (comma separated)", "+,+,+,+")
email_input = st.text_input("Email ID")

if st.button('Submit'):
    if not uploaded_file:
        st.error('please upload a file')
        st.stop()

    if not check_email(email_input):
        st.error('invalid email')
        st.stop()

    try:
        df=pd.read_csv(uploaded_file)
    except:
        st.error('unable to read file')
        st.stop()

    if df.shape[1]<3:
        st.error('file must contain at least 3 columns')
        st.stop()

    numeric_df = df.iloc[:,1:]
    if not all(numeric_df.dtypes.apply(lambda x: np.issubdtype(x, np.number))):
        st.error("From 2nd to last columns must contain numeric values only")
        st.stop()

    weights = weights_input.split(',')
    impacts = impacts_input.split(',')

    if len(weights)!=len(impacts) or len(weights)!=(df.shape[1]-1):
        st.error('number of weights, impacts and criteria must match')
        st.stop()

    try:
        weights = [float(w) for w in weights]
    except:
        st.error("Weights must be numeric.")
        st.stop()

    if not all(i in ["+", "-"] for i in impacts):
        st.error("Impacts must be either + or -.")
        st.stop()

    result_df = topsis(df, weights, impacts)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        result_df.to_csv(tmp.name, index=False)
        temp_path=tmp.name
    
    try:
        send_email(email_input, temp_path)
        st.success('result file sent to email')
    except Exception as e:
        st.error('failed to send email. check email config')
    
    os.remove(temp_path)
