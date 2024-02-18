import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from joblib import load


towns = ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH', 'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI', 'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST', 'KALLANG/WHAMPOA', 'LIM CHU KANG', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL', 'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES', 'TOA PAYOH', 'WOODLANDS', 'YISHUN']
flat_types = ['1 ROOM', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', 'MULTI GENERATION', 'MULTI-GENERATION']
street_names = ['ADMIRALTY DR', 'ADMIRALTY LINK', 'AH HOOD RD', 'ALEXANDRA RD', 'ALJUNIED AVE 2', 'ALJUNIED CRES', 'ALJUNIED RD', 'ANCHORVALE CRES', 'ANCHORVALE DR', 'ANCHORVALE LANE', 'ANCHORVALE LINK', 'ANCHORVALE RD', 'ANCHORVALE ST', 'ANG MO KIO AVE 1', 'ANG MO KIO AVE 10', 'ANG MO KIO AVE 2', 'ANG MO KIO AVE 3', 'ANG MO KIO AVE 4', 'ANG MO KIO AVE 5', 'ANG MO KIO AVE 6', 'ANG MO KIO AVE 8', 'ANG MO KIO AVE 9', 'ANG MO KIO ST 11', 'ANG MO KIO ST 21', 'ANG MO KIO ST 31', 'ANG MO KIO ST 32', 'ANG MO KIO ST 44', 'ANG MO KIO ST 51', 'ANG MO KIO ST 52', 'ANG MO KIO ST 61', 'BAIN ST', 'BALAM RD', 'BANGKIT RD', 'BEACH RD', 'BEDOK CTRL', 'BEDOK NTH AVE 1', 'BEDOK NTH AVE 2', 'BEDOK NTH AVE 3', 'BEDOK NTH AVE 4', 'BEDOK NTH RD', 'BEDOK NTH ST 1', 'BEDOK NTH ST 2', 'BEDOK NTH ST 3', 'BEDOK NTH ST 4', 'BEDOK RESERVOIR CRES', 'BEDOK RESERVOIR RD', 'BEDOK RESERVOIR VIEW', 'BEDOK STH AVE 1', 'BEDOK STH AVE 2', 'BEDOK STH AVE 3', 'BEDOK STH RD', 'BENDEMEER RD', 'BEO CRES', 'BISHAN ST 11', 'BISHAN ST 12', 'BISHAN ST 13', 'BISHAN ST 22', 'BISHAN ST 23', 'BISHAN ST 24', 'BOON KENG RD', 'BOON LAY AVE', 'BOON LAY DR', 'BOON LAY PL', 'BOON TIONG RD', 'BRIGHT HILL DR', 'BT BATOK CTRL', 'BT BATOK EAST AVE 3', 'BT BATOK EAST AVE 4', 'BT BATOK EAST AVE 5', 'BT BATOK EAST AVE 6', 'BT BATOK ST 11', 'BT BATOK ST 21', 'BT BATOK ST 22', 'BT BATOK ST 24', 'BT BATOK ST 25', 'BT BATOK ST 31', 'BT BATOK ST 32', 'BT BATOK ST 33', 'BT BATOK ST 34', 'BT BATOK ST 51', 'BT BATOK ST 52', 'BT BATOK WEST AVE 2', 'BT BATOK WEST AVE 4', 'BT BATOK WEST AVE 5', 'BT BATOK WEST AVE 6', 'BT BATOK WEST AVE 7', 'BT BATOK WEST AVE 8', 'BT BATOK WEST AVE 9', 'BT MERAH CTRL', 'BT MERAH LANE 1', 'BT MERAH VIEW', 'BT PANJANG RING RD', 'BT PURMEI RD', 'BUANGKOK CRES', 'BUANGKOK GREEN', 'BUANGKOK LINK', 'BUANGKOK STH FARMWAY 1', 'BUFFALO RD', "C'WEALTH AVE", "C'WEALTH AVE WEST", "C'WEALTH CL", "C'WEALTH CRES", "C'WEALTH DR", 'CAMBRIDGE RD', 'CANBERRA CRES', 'CANBERRA LINK', 'CANBERRA RD', 'CANBERRA ST', 'CANBERRA WALK', 'CANTONMENT CL', 'CANTONMENT RD', 'CASHEW RD', 'CASSIA CRES', 'CHAI CHEE AVE', 'CHAI CHEE DR', 'CHAI CHEE RD', 'CHAI CHEE ST', 'CHANDER RD', 'CHANGI VILLAGE RD', 'CHIN SWEE RD', 'CHOA CHU KANG AVE 1', 'CHOA CHU KANG AVE 2', 'CHOA CHU KANG AVE 3', 'CHOA CHU KANG AVE 4', 'CHOA CHU KANG AVE 5', 'CHOA CHU KANG AVE 7', 'CHOA CHU KANG CRES', 'CHOA CHU KANG CTRL', 'CHOA CHU KANG DR', 'CHOA CHU KANG LOOP', 'CHOA CHU KANG NTH 5', 'CHOA CHU KANG NTH 6', 'CHOA CHU KANG NTH 7', 'CHOA CHU KANG ST 51', 'CHOA CHU KANG ST 52', 'CHOA CHU KANG ST 53', 'CHOA CHU KANG ST 54', 'CHOA CHU KANG ST 62', 'CHOA CHU KANG ST 64', 'CIRCUIT RD', 'CLARENCE LANE', 'CLEMENTI AVE 1', 'CLEMENTI AVE 2', 'CLEMENTI AVE 3', 'CLEMENTI AVE 4', 'CLEMENTI AVE 5', 'CLEMENTI AVE 6', 'CLEMENTI ST 11', 'CLEMENTI ST 12', 'CLEMENTI ST 13', 'CLEMENTI ST 14', 'CLEMENTI WEST ST 1', 'CLEMENTI WEST ST 2', 'COMPASSVALE BOW', 'COMPASSVALE CRES', 'COMPASSVALE DR', 'COMPASSVALE LANE', 'COMPASSVALE LINK', 'COMPASSVALE RD', 'COMPASSVALE ST', 'COMPASSVALE WALK', 'CORPORATION DR', 'CRAWFORD LANE', 'DAKOTA CRES', 'DAWSON RD', 'DELTA AVE', 'DEPOT RD', 'DORSET RD', 'DOVER CL EAST', 'DOVER CRES', 'DOVER RD', 'EAST COAST RD', 'EDGEDALE PLAINS', 'EDGEFIELD PLAINS', 'ELIAS RD', 'EMPRESS RD', 'EUNOS CRES', 'EUNOS RD 5', 'EVERTON PK', 'FAJAR RD', 'FARRER PK RD', 'FARRER RD', 'FERNVALE LANE', 'FERNVALE LINK', 'FERNVALE RD', 'FERNVALE ST', 'FRENCH RD', 'GANGSA RD', 'GEYLANG BAHRU', 'GEYLANG EAST AVE 1', 'GEYLANG EAST AVE 2', 'GEYLANG EAST CTRL', 'GEYLANG SERAI', 'GHIM MOH LINK', 'GHIM MOH RD', 'GLOUCESTER RD', 'HAIG RD', 'HAVELOCK RD', 'HENDERSON CRES', 'HENDERSON RD', 'HILLVIEW AVE', 'HO CHING RD', 'HOLLAND AVE', 'HOLLAND CL', 'HOLLAND DR', 'HOUGANG AVE 1', 'HOUGANG AVE 10', 'HOUGANG AVE 2', 'HOUGANG AVE 3', 'HOUGANG AVE 4', 'HOUGANG AVE 5', 'HOUGANG AVE 6', 'HOUGANG AVE 7', 'HOUGANG AVE 8', 'HOUGANG AVE 9', 'HOUGANG CTRL', 'HOUGANG ST 11', 'HOUGANG ST 21', 'HOUGANG ST 22', 'HOUGANG ST 31', 'HOUGANG ST 32', 'HOUGANG ST 51', 'HOUGANG ST 52', 'HOUGANG ST 61', 'HOUGANG ST 91', 'HOUGANG ST 92', 'HOY FATT RD', 'HU CHING RD', 'INDUS RD', 'JELAPANG RD', 'JELEBU RD', 'JELLICOE RD', 'JLN BAHAGIA', 'JLN BATU', 'JLN BERSEH', 'JLN BT HO SWEE', 'JLN BT MERAH', 'JLN DAMAI', 'JLN DUA', 'JLN DUSUN', 'JLN KAYU', 'JLN KLINIK', 'JLN KUKOH', "JLN MA'MOR", 'JLN MEMBINA', 'JLN MEMBINA BARAT', 'JLN PASAR BARU', 'JLN RAJAH', 'JLN RUMAH TINGGI', 'JLN TECK WHYE', 'JLN TENAGA', 'JLN TENTERAM', 'JLN TIGA', 'JOO CHIAT RD', 'JOO SENG RD', 'JURONG EAST AVE 1', 'JURONG EAST ST 13', 'JURONG EAST ST 21', 'JURONG EAST ST 24', 'JURONG EAST ST 31', 'JURONG EAST ST 32', 'JURONG WEST AVE 1', 'JURONG WEST AVE 3', 'JURONG WEST AVE 5', 'JURONG WEST CTRL 1', 'JURONG WEST CTRL 3', 'JURONG WEST ST 24', 'JURONG WEST ST 25', 'JURONG WEST ST 41', 'JURONG WEST ST 42', 'JURONG WEST ST 51', 'JURONG WEST ST 52', 'JURONG WEST ST 61', 'JURONG WEST ST 62', 'JURONG WEST ST 64', 'JURONG WEST ST 65', 'JURONG WEST ST 71', 'JURONG WEST ST 72', 'JURONG WEST ST 73', 'JURONG WEST ST 74', 'JURONG WEST ST 75', 'JURONG WEST ST 81', 'JURONG WEST ST 91', 'JURONG WEST ST 92', 'JURONG WEST ST 93', 'KALLANG BAHRU', 'KANG CHING RD', 'KEAT HONG CL', 'KEAT HONG LINK', 'KELANTAN RD', 'KENT RD', 'KG ARANG RD', 'KG BAHRU HILL', 'KG KAYU RD', 'KIM CHENG ST', 'KIM KEAT AVE', 'KIM KEAT LINK', 'KIM PONG RD', 'KIM TIAN PL', 'KIM TIAN RD', "KING GEORGE'S AVE", 'KLANG LANE', 'KRETA AYER RD', 'LENGKOK BAHRU', 'LENGKONG TIGA', 'LIM CHU KANG RD', 'LIM LIAK ST', 'LOMPANG RD', 'LOR 1 TOA PAYOH', 'LOR 1A TOA PAYOH', 'LOR 2 TOA PAYOH', 'LOR 3 GEYLANG', 'LOR 3 TOA PAYOH', 'LOR 4 TOA PAYOH', 'LOR 5 TOA PAYOH', 'LOR 6 TOA PAYOH', 'LOR 7 TOA PAYOH', 'LOR 8 TOA PAYOH', 'LOR AH SOO', 'LOR LEW LIAN', 'LOR LIMAU', 'LOWER DELTA RD', 'MACPHERSON LANE', 'MARGARET DR', 'MARINE CRES', 'MARINE DR', 'MARINE PARADE CTRL', 'MARINE TER', 'MARSILING CRES', 'MARSILING DR', 'MARSILING LANE', 'MARSILING RD', 'MARSILING RISE', 'MCNAIR RD', 'MEI LING ST', 'MOH GUAN TER', 'MONTREAL DR', 'MONTREAL LINK', 'MOULMEIN RD', 'NEW MKT RD', 'NEW UPP CHANGI RD', 'NILE RD', 'NTH BRIDGE RD', 'OLD AIRPORT RD', 'OUTRAM HILL', 'OUTRAM PK', 'OWEN RD', 'PANDAN GDNS', 'PASIR RIS DR 1', 'PASIR RIS DR 10', 'PASIR RIS DR 3', 'PASIR RIS DR 4', 'PASIR RIS DR 6', 'PASIR RIS ST 11', 'PASIR RIS ST 12', 'PASIR RIS ST 13', 'PASIR RIS ST 21', 'PASIR RIS ST 41', 'PASIR RIS ST 51', 'PASIR RIS ST 52', 'PASIR RIS ST 53', 'PASIR RIS ST 71', 'PASIR RIS ST 72', 'PAYA LEBAR WAY', 'PENDING RD', 'PETIR RD', 'PINE CL', 'PIPIT RD', 'POTONG PASIR AVE 1', 'POTONG PASIR AVE 2', 'POTONG PASIR AVE 3', 'PUNGGOL CTRL', 'PUNGGOL DR', 'PUNGGOL EAST', 'PUNGGOL FIELD', 'PUNGGOL FIELD WALK', 'PUNGGOL PL', 'PUNGGOL RD', 'PUNGGOL WALK', 'PUNGGOL WAY', 'QUEEN ST', "QUEEN'S CL", "QUEEN'S RD", 'QUEENSWAY', 'RACE COURSE RD', 'REDHILL CL', 'REDHILL LANE', 'REDHILL RD', 'RIVERVALE CRES', 'RIVERVALE DR', 'RIVERVALE ST', 'RIVERVALE WALK', 'ROCHOR RD', 'ROWELL RD', 'SAGO LANE', 'SAUJANA RD', 'SEGAR RD', 'SELEGIE RD', 'SELETAR WEST FARMWAY 6', 'SEMBAWANG CL', 'SEMBAWANG CRES', 'SEMBAWANG DR', 'SEMBAWANG RD', 'SEMBAWANG VISTA', 'SEMBAWANG WAY', 'SENG POH RD', 'SENGKANG CTRL', 'SENGKANG EAST AVE', 'SENGKANG EAST RD', 'SENGKANG EAST WAY', 'SENGKANG WEST AVE', 'SENGKANG WEST WAY', 'SENJA LINK', 'SENJA RD', 'SERANGOON AVE 1', 'SERANGOON AVE 2', 'SERANGOON AVE 3', 'SERANGOON AVE 4', 'SERANGOON CTRL', 'SERANGOON CTRL DR', 'SERANGOON NTH AVE 1', 'SERANGOON NTH AVE 2', 'SERANGOON NTH AVE 3', 'SERANGOON NTH AVE 4', 'SHORT ST', 'SHUNFU RD', 'SILAT AVE', 'SIMEI LANE', 'SIMEI RD', 'SIMEI ST 1', 'SIMEI ST 2', 'SIMEI ST 4', 'SIMEI ST 5', 'SIMS AVE', 'SIMS DR', 'SIMS PL', 'SIN MING AVE', 'SIN MING RD', 'SMITH ST', 'SPOTTISWOODE PK RD', "ST. GEORGE'S LANE", "ST. GEORGE'S RD", 'STIRLING RD', 'STRATHMORE AVE', 'SUMANG LANE', 'SUMANG LINK', 'SUMANG WALK', 'TAH CHING RD', 'TAMAN HO SWEE', 'TAMPINES AVE 1', 'TAMPINES AVE 4', 'TAMPINES AVE 5', 'TAMPINES AVE 7', 'TAMPINES AVE 8', 'TAMPINES AVE 9', 'TAMPINES CTRL 1', 'TAMPINES CTRL 7', 'TAMPINES CTRL 8', 'TAMPINES ST 11', 'TAMPINES ST 12', 'TAMPINES ST 21', 'TAMPINES ST 22', 'TAMPINES ST 23', 'TAMPINES ST 24', 'TAMPINES ST 32', 'TAMPINES ST 33', 'TAMPINES ST 34', 'TAMPINES ST 41', 'TAMPINES ST 42', 'TAMPINES ST 43', 'TAMPINES ST 44', 'TAMPINES ST 45', 'TAMPINES ST 61', 'TAMPINES ST 71', 'TAMPINES ST 72', 'TAMPINES ST 81', 'TAMPINES ST 82', 'TAMPINES ST 83', 'TAMPINES ST 84', 'TAMPINES ST 86', 'TAMPINES ST 91', 'TANGLIN HALT RD', 'TAO CHING RD', 'TEBAN GDNS RD', 'TECK WHYE AVE', 'TECK WHYE CRES', 'TECK WHYE LANE', 'TELOK BLANGAH CRES', 'TELOK BLANGAH DR', 'TELOK BLANGAH HTS', 'TELOK BLANGAH RISE', 'TELOK BLANGAH ST 31', 'TELOK BLANGAH WAY', 'TESSENSOHN RD', 'TG PAGAR PLAZA', 'TIONG BAHRU RD', 'TOA PAYOH CTRL', 'TOA PAYOH EAST', 'TOA PAYOH NTH', 'TOH GUAN RD', 'TOH YI DR', 'TOWNER RD', 'UBI AVE 1', 'UPP ALJUNIED LANE', 'UPP BOON KENG RD', 'UPP CROSS ST', 'UPP SERANGOON CRES', 'UPP SERANGOON RD', 'UPP SERANGOON VIEW', 'VEERASAMY RD', 'WATERLOO ST', 'WELLINGTON CIRCLE', 'WEST COAST DR', 'WEST COAST RD', 'WHAMPOA DR', 'WHAMPOA RD', 'WHAMPOA STH', 'WHAMPOA WEST', 'WOODLANDS AVE 1', 'WOODLANDS AVE 3', 'WOODLANDS AVE 4', 'WOODLANDS AVE 5', 'WOODLANDS AVE 6', 'WOODLANDS AVE 9', 'WOODLANDS CIRCLE', 'WOODLANDS CRES', 'WOODLANDS CTR RD', 'WOODLANDS DR 14', 'WOODLANDS DR 16', 'WOODLANDS DR 40', 'WOODLANDS DR 42', 'WOODLANDS DR 44', 'WOODLANDS DR 50', 'WOODLANDS DR 52', 'WOODLANDS DR 53', 'WOODLANDS DR 60', 'WOODLANDS DR 62', 'WOODLANDS DR 70', 'WOODLANDS DR 71', 'WOODLANDS DR 72', 'WOODLANDS DR 73', 'WOODLANDS DR 75', 'WOODLANDS RING RD', 'WOODLANDS RISE', 'WOODLANDS ST 11', 'WOODLANDS ST 13', 'WOODLANDS ST 31', 'WOODLANDS ST 32', 'WOODLANDS ST 41', 'WOODLANDS ST 81', 'WOODLANDS ST 82', 'WOODLANDS ST 83', 'YISHUN AVE 1', 'YISHUN AVE 11', 'YISHUN AVE 2', 'YISHUN AVE 3', 'YISHUN AVE 4', 'YISHUN AVE 5', 'YISHUN AVE 6', 'YISHUN AVE 7', 'YISHUN AVE 9', 'YISHUN CTRL', 'YISHUN CTRL 1', 'YISHUN RING RD', 'YISHUN ST 11', 'YISHUN ST 20', 'YISHUN ST 21', 'YISHUN ST 22', 'YISHUN ST 31', 'YISHUN ST 41', 'YISHUN ST 43', 'YISHUN ST 51', 'YISHUN ST 61', 'YISHUN ST 71', 'YISHUN ST 72', 'YISHUN ST 81', 'YUAN CHING RD', 'YUNG AN RD', 'YUNG HO RD', 'YUNG KUANG RD', 'YUNG LOH RD', 'YUNG PING RD', 'YUNG SHENG RD', 'ZION RD']
flat_models = ['2-ROOM', '2-room', '3Gen', 'APARTMENT', 'Adjoined flat', 'Apartment', 'DBSS', 'IMPROVED', 'IMPROVED-MAISONETTE', 'Improved', 'Improved-Maisonette', 'MAISONETTE', 'MODEL A', 'MODEL A-MAISONETTE', 'MULTI GENERATION', 'Maisonette', 'Model A', 'Model A-Maisonette', 'Model A2', 'Multi Generation', 'NEW GENERATION', 'New Generation', 'PREMIUM APARTMENT', 'Premium Apartment', 'Premium Apartment Loft', 'Premium Maisonette', 'SIMPLIFIED', 'STANDARD', 'Simplified', 'Standard', 'TERRACE', 'Terrace', 'Type S1', 'Type S2']


st.set_page_config(layout='wide')

st.write("<h2 style='text-align:center; margin-top:-60px; font-weight:bolder;'>Singapore Resale Flat Prices Prediction Application</h2>",unsafe_allow_html=True)

with st.form('form1'):
    col1,col2 = st.columns(2)
    with col1:
        town = st.selectbox("**Select Town**",towns,index=None,placeholder="Please Select")
        flat_type = st.selectbox("**Select Flat Type**",flat_types,index=None,placeholder="Please Select")
        street = st.selectbox("**Select Street Name**",street_names,index=None,placeholder="Please Select")
        flat_model = st.selectbox("**Select Flat Model**",flat_models,index=None,placeholder="Please Select")
        block = st.number_input("**Enter Block number (min:0, max:2500)**")
        
    with col2:
        floor_area_sqm = st.number_input("**Enter Area sqm (min:0, max:500)**")
        lease_commence_year = st.number_input("**Enter Lease commence Year  (min:1990, max:2024)**")
        remaining_lease = st.number_input("**Enter Remaining Lease Year  (min:0, max:100)**")
        storey_range = st.text_input("**Enter Storey Range  (eg : 05-10 )**")
        resale_month = st.text_input("**Enter Resale Year & Month  (eg : 2000-10 )**")
    submit = st.form_submit_button("**Predict Resale Price**")
    st.markdown("""
            <style>
            
            .stButton>button{
                background-color: #01A982;
                font-weight:bolder;
                
                color:#ffffff;
                width:5em;
                color:#ffffff;
                width: 255px;
                transition-duration: 0.4s;
                margin: 10px 300px;
                border-radius: 25px;
                border-radius: 5px 25px;
                padding: 1px;
                box-shadow: 2px 2px 5px gray;
                transition: color 0.3s ease-in-out;
                animation: spin 2s linear infinite;
                
            }
            .st-ax{
                background-color: lightblue;
            }

            .stTextInput input{
                background-color: lightblue;
            }
            .stNumberInput input{
                background-color: lightblue;
            }

            .stDateInput Input{
                background-color: lightblue;
            }

            </style>
            """,unsafe_allow_html=True)

if submit:   
    if (town != None) and (flat_type !=None) and (street != None) and (flat_model != None) :
        low = 0
        up = 0
        if len(storey_range.split('-')) == 2 :
            low = (storey_range.split("-"))[0]
            up = (storey_range.split("-"))[1]
        year = 0
        month = 0
        if len(resale_month.split('-')) == 2:
            year = (resale_month.split("-"))[0]
            month = (resale_month.split("-"))[1]

        data = {
            "town": int(towns.index(town)),
            "flat_type": int(flat_types.index(flat_type)),
            "block": int(block),
            "street_name": int(street_names.index(street)),
            "floor_area_sqm": float(floor_area_sqm),
            "flat_model": int(flat_models.index(flat_model)),
            "lease_commence_date": int(lease_commence_year),
            "remaining_lease": float(remaining_lease),
            "storey_low": int(low),
            "storey_up": int(up),
            "resale_year": int(year),
            "resale_month": int(month),
        }
        
    df = pd.DataFrame([data])
    model = load("resalemodel.joblib")
    prediction = model.predict(df)
    st.write("Resale Price :",float(prediction))