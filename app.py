import streamlit as st
import numpy as np
import pickle
import pandas as pd


def blanks():
    col11, col12, col13 = st.columns(3)
    with col11:
        st.write('          ')
    with col12:
        st.write('          ')
    with col13:
        st.write('          ')



st.title('IPL Win Predictor')

teams = ['Delhi Daredevils', 'Chennai Super Kings',
       'Royal Challengers Bangalore', 'Mumbai Indians', 'Kings XI Punjab',
       'Sunrisers Hyderabad', 'Kolkata Knight Riders', 'Rajasthan Royals',
       'Deccan Chargers', 'Delhi Capitals']

cities = ['Hyderabad', 'Delhi', 'Sharjah', 'Kolkata', 'Durban', 'Mumbai',
       'Port Elizabeth', 'Bengaluru', 'Jaipur', 'Chennai', 'Pune',
       'Johannesburg', 'Chandigarh', 'Centurion', 'Mohali', 'Nagpur',
       'Bangalore', 'Ahmedabad', 'Abu Dhabi', 'Cuttack', 'Dharamsala',
       'Ranchi', 'Cape Town', 'Raipur', 'East London', 'Bloemfontein',
       'Indore', 'Kimberley', 'Visakhapatnam']


pipe = pickle.load(open('pipe.pkl', 'rb'))

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select Batting / Chasing Team', sorted(teams))
with col2:
    teams = [team for team in teams if team != batting_team]
    bowling_team = st.selectbox('Select Bowling / Defending Team', sorted(teams))

selected_city = st.selectbox('Select Host City', cities)

target = st.number_input('Target')

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score')
with col4:
    overs = st.number_input('Overs Completed')
with col5:
    wickets = st.number_input('Wickets Out')

blanks()
blanks()


if st.button('Predict Probability'):
    runs_left = int(target - score)
    balls_left = int(120 - (overs*6))
    wickets = int(10 - wickets)
    crr = score / overs
    rrr = (runs_left*6) / balls_left

    data = pd.DataFrame([[batting_team, bowling_team, selected_city, runs_left, balls_left, wickets, target, crr, rrr]],
                    columns=['batting_team', 'bowling_team', 'city', 'runs_left', 'balls_left',	'wickets',	'total_runs_x',	'crr', 'rrr'])
    
    result = pipe.predict_proba(data)

    losing = result[0][0] * 100
    loss = str(losing).split('.')[0]
    loss += '.' + str(losing).split('.')[1][0:2]

    winning = result[0][1] * 100
    win = str(winning).split('.')[0]
    win += '.' + str(winning).split('.')[1][0:2]

    blanks()

    st.subheader(batting_team + ' : '+ str(win) + '%')
    st.subheader(bowling_team + ' : ' + str(loss) + '%')