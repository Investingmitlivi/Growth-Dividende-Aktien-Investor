import requests, json, time
#import streamlit_authenticator as stauth
#import pickle
import matplotlib.pyplot as plt
import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px
#import sqlite3 
#import bcrypt
import plotly.graph_objs as go
import plotly.graph_objects as go
import altair as alt
#import random
#import string
#import uuid  # Import the uuid library
#import hashlib
import time
import firebase_admin
import math
import textwrap

#import math
#import re
#import finnhub



from sqlite3 import OperationalError
from requests.exceptions import HTTPError
from datetime import datetime, timedelta, date
from PIL import Image,ImageDraw
from streamlit_lottie import st_lottie
from numpy_financial import npv
from pathlib import Path
from googletrans import Translator, LANGUAGES
from translate import Translator
#from transformers import pipeline
from forex_python.converter import CurrencyRates
from forex_python.converter import RatesNotAvailableError
from googlefinance import getQuotes
from pandas_market_calendars import get_calendar
from yahoo_fin import stock_info as si
from bs4 import BeautifulSoup
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from pandas_datareader import data
from finvizfinance.quote import finvizfinance
from pyfinviz.quote import Quote
from stocknews import StockNews





st.set_page_config(page_title="StockAnalysisTool", page_icon = "📚", layout="wide")

hide_streamlit_style = """
                <div style="max-width: 100%;">
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                </div>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


#
cred = credentials.Certificate('investingmitlivi-firebase key.json')
try:
     firebase_admin.initialize_app(cred)

except ValueError:
      
     st.write("")


fig = go.Figure()

#st.set_page_config(layout='wide')
#st.plotly_chart(fig, config={'displayModeBar': False})
#
config = {'displayModeBar': False}



#st.plotly_chart(fig, config={'displayModeBar': False})


#with st.container():
 #    st.subheader("Hi, I am Livinus :wave:")
  #   st.title("A youtuber who teaches how to build long-term wealth through Stocks.")
   #  st.write("[Youtube Channel >](https://www.youtube.com/@Investing_mit_Livi)")
     

# ---- Load Assets ----

with st.container():
     
     #left_column, center_column, right_column = st.columns([1, 2, 1])

     #with left_column:
     #st.header("what i do")
     st.write("##")
     st.write(
        """
        Stock Nerd | Fundamental Analysis | Learning, Understanding & Proper Application | Buy & Hold
        Stock Analysis.

        - I share my experiences on how to evaluate a stock or a company.
        - First, i take a look at the financial statements to determine if the company is financially sound, and ultimately, i identify potential price targets for the company.
        """
     
        )
     st.write("[Youtube Channel >](https://www.youtube.com/@Investing_mit_Livi)")
     st.write("---")

#finnhub_client = finnhub.Client(api_key="ckse5rhr01qjpllh316gckse5rhr01qjpllh3170")


     def get_exchange_rate(base_currency, target_currency):
                    try:
                         url = f"https://api.frankfurter.app/latest?amount=1&from={base_currency}&to={target_currency}"
                         response = requests.get(url)
                         data = response.json()
                         exchange_rate = data['rates'][target_currency]
                         return exchange_rate
                    
                    except Exception as e:
                         url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
                         response = requests.get(url)
                         data = response.json()
                         exchange_rate = data['rates'][target_currency]
                         return exchange_rate

                    # Get the exchange rate for USD to EUR
     usd_to_eur_rate = get_exchange_rate("USD", "EUR")

               # Display the rate in Streamlit
     #st.write(f"1 USD is equivalent to {usd_to_eur_rate} EUR")


#------------------------------------------------------------------------

ticker_symbol_name = {
     'GOOGL':'Alphabet Inc.  ',
     'A':'Agilent Technologies Inc. ',
     'AA':'Alcoa Corporation ',
     'AACG':'ATA Creativity Global ',
     'AACI':'Armada Acquisition Corp. I ',
     'AACIW':'Armada Acquisition Corp. I ',
     'AACT':'Ares Acquisition Corporation II ',
     'AADI':'Aadi Bioscience Inc. ',
     'AAIC':'Arlington Asset Investment Corp ',
     'AAL':'American Airlines Group Inc. ',
     'AAMC':'Altisource Asset Management Corp Com',
     'AAME':'Atlantic American Corporation ',
     'AAN':'Aarons Holdings Company Inc. ',
     'AAOI':'Applied Optoelectronics Inc. ',
     'AAON':'AAON Inc. ',
     'AAP':'Advance Auto Parts Inc.',
     'AAPL':'Apple Inc. ',
     'AAT':'American Assets Trust Inc. ',
     'AAU':'Almaden Minerals Ltd. ',
     'AB':'AllianceBernstein Holding L.P.  Units',
     'ABBV':'AbbVie Inc. ',
     'ABC':'AmerisourceBergen Corporation ',
     'ABCB':'Ameris Bancorp ',
     'ABCL':'AbCellera Biologics Inc. ',
     'ABCM':'Abcam plc ',
     'ABEO':'Abeona Therapeutics Inc. ',
     'ABEV':'Ambev S.A.  (Each representing 1 Common Share)',
     'ABG':'Asbury Automotive Group Inc ',
     'ABIO':'ARCA biopharma Inc. ',
     'ABL':'Abacus Life Inc.  ',
     'ABLLW':'Abacus Life Inc. ',
     'ABM':'ABM Industries Incorporated ',
     'ABNB':'Airbnb Inc.  ',
     'ABOS':'Acumen Pharmaceuticals Inc. ',
     'ABR':'Arbor Realty Trust ',
     'ABSI':'Absci Corporation ',
     'ABST':'Absolute Software Corporation ',
     'ABT':'Abbott Laboratories ',
     'ABUS':'Arbutus Biopharma Corporation ',
     'ABVC':'ABVC BioPharma Inc. ',
     'AC':'Associated Capital Group Inc. ',
     'ACA':'Arcosa Inc. ',
     'ACAB':'Atlantic Coastal Acquisition Corp. II  ',
     'ACABW':'Atlantic Coastal Acquisition Corp. II ',
     'ACAC':'Acri Capital Acquisition Corporation  ',
     'ACACU':'Acri Capital Acquisition Corporation Unit',
     'ACACW':'Acri Capital Acquisition Corporation ',
     'ACAD':'ACADIA Pharmaceuticals Inc. ',
     'ACAH':'Atlantic Coastal Acquisition Corp.  ',
     'ACAHW':'Atlantic Coastal Acquisition Corp. ',
     'ACAQ':'Athena Consumer Acquisition Corp.  ',
     'ACAX':'Alset Capital Acquisition Corp.  ',
     'ACAXR':'Alset Capital Acquisition Corp. Right',
     'ACAXU':'Alset Capital Acquisition Corp. Unit',
     'ACAXW':'Alset Capital Acquisition Corp. ',
     'ACB':'Aurora Cannabis Inc. ',
     'ACBA':'Ace Global Business Acquisition Limited ',
     'ACBAU':'Ace Global Business Acquisition Limited Unit',
     'ACCD':'Accolade Inc. ',
     'ACCO':'Acco Brands Corporation ',
     'ACDC':'ProFrac Holding Corp.  ',
     'ACDCW':'ProFrac Holding Corp. ',
     'ACEL':'Accel Entertainment Inc.',
     'ACER':'Acer Therapeutics Inc.  (DE)',
     'ACET':'Adicet Bio Inc. ',
     'ACGL':'Arch Capital Group Ltd. ',
     'ACGN':'Aceragen Inc. ',
     'ACHC':'Acadia Healthcare Company Inc. ',
     'ACHL':'Achilles Therapeutics plc ',
     'ACHR':'Archer Aviation Inc.  ',
     'ACHV':'Achieve Life Sciences Inc. ',
     'ACI':'Albertsons Companies Inc.  ',
     'ACIU':'AC Immune SA ',
     'ACIW':'ACI Worldwide Inc. ',
     'ACLS':'Axcelis Technologies Inc. ',
     'ACLX':'Arcellx Inc. ',
     'ACM':'AECOM ',
     'ACMR':'ACM Research Inc.  ',
     'ACN':'Accenture plc  (Ireland)',
     'ACNB':'ACNB Corporation ',
     'ACNT':'Ascent Industries Co. ',
     'ACON':'Aclarion Inc. ',
     'ACONW':'Aclarion Inc. ',
     'ACOR':'Acorda Therapeutics Inc. ',
     'ACP':'abrdn Income Credit Strategies Fund ',
     'ACR':'ACRES Commercial Realty Corp. ',
     'ACRE':'Ares Commercial Real Estate Corporation ',
     'ACRO':'Acropolis Infrastructure Acquisition Corp.  ',
     'ACRS':'Aclaris Therapeutics Inc. ',
     'ACRV':'Acrivon Therapeutics Inc. ',
     'ACRX':'AcelRx Pharmaceuticals Inc. ',
     'ACST':'Acasti Pharma Inc.  ',
     'ACT':'Enact Holdings Inc. ',
     'ACTG':'Acacia Research Corporation (Acacia Tech) ',
     'ACU':'Acme United Corporation. ',
     'ACVA':'ACV Auctions Inc.  ',
     'ACXP':'Acurx Pharmaceuticals Inc. ',
     'ADAG':'Adagene Inc. ',
     'ADAP':'Adaptimmune Therapeutics plc ',
     'ADBE':'Adobe Inc. ',
     'ADC':'Agree Realty Corporation ',
     'ADCT':'ADC Therapeutics SA ',
     'ADD':'Color Star Technology Co. Ltd. ',
     'ADS:DE':'ADIDAS AG. ',
     'ADEA':'Adeia Inc. ',
     'ADER':'26 Capital Acquisition Corp.  ',
     'ADERU':'26 Capital Acquisition Corp. Unit',
     'ADERW':'26 Capital Acquisition Corp. ',
     'ADES':'Advanced Emissions Solutions Inc. ',
     'ADEX':'Adit EdTech Acquisition Corp. ',
     'ADI':'Analog Devices Inc. ',
     'ADIL':'Adial Pharmaceuticals Inc ',
     'ADILW':'Adial Pharmaceuticals Inc ',
     'ADM':'Archer-Daniels-Midland Company ',
     'ADMA':'ADMA Biologics Inc ',
     'ADMP':'Adamis Pharmaceuticals Corporation ',
     'ADN':'Advent Technologies Holdings Inc.  ',
     'ADNT':'Adient plc ',
     'ADNWW':'Advent Technologies Holdings Inc. ',
     'ADOC':'Edoc Acquisition Corp.',
     'ADOCR':'Edoc Acquisition Corp. Right',
     'ADOCW':'Edoc Acquisition Corp. ',
     'ADP':'Automatic Data Processing Inc. ',
     'ADPT':'Adaptive Biotechnologies Corporation ',
     'ADRT':'Ault Disruptive Technologies Corporation ',
     'ADSE':'ADS-TEC ENERGY PLC ',
     'ADSEW':'ADS-TEC ENERGY PLC ',
     'ADSK':'Autodesk Inc. ',
     'ADT':'ADT Inc. ',
     'ADTH':'AdTheorent Holding Company Inc. ',
     'ADTHW':'AdTheorent Holding Company Inc. s',
     'ADTN':'ADTRAN Holdings Inc. ',
     'ADTX':'Aditxt Inc. ',
     'ADUS':'Addus HomeCare Corporation ',
     'ADV':'Advantage Solutions Inc.  ',
     'ADVM':'Adverum Biotechnologies Inc. ',
     'ADVWW':'Advantage Solutions Inc. ',
     'ADX':'Adams Diversified Equity Fund Inc.',
     'ADXN':'Addex Therapeutics Ltd ',
     'AE':'Adams Resources & Energy Inc. ',
     'AEAE':'AltEnergy Acquisition Corp.  ',
     'AEAEW':'AltEnergy Acquisition Corp. ',
     'AEE':'Ameren Corporation ',
     'AEF':'abrdn Emerging Markets Equity Income Fund Inc. ',
     'AEG':'AEGON N.V. ',
     'AEHL':'Antelope Enterprise Holdings Limited ',
     'AEHR':'Aehr Test Systems ',
     'AEI':'Alset Inc.  (TX)',
     'AEIS':'Advanced Energy Industries Inc. ',
     'AEL':'American Equity Investment Life Holding Company ',
     'AEM':'Agnico Eagle Mines Limited ',
     'AEMD':'Aethlon Medical Inc. ',
     'AENT':'Alliance Entertainment Holding Corporation  ',
     'AENTW':'Alliance Entertainment Holding Corporation s',
     'AENZ':'Aenza S.A.A. ',
     'AEO':'American Eagle Outfitters Inc. ',
     'AEP':'American Electric Power Company Inc. ',
     'AER':'AerCap Holdings N.V. ',
     'AES':'The AES Corporation ',
     'AESC':'The AES Corporation Corporate Units',
     'AESI':'Atlas Energy Solutions Inc.  ',
     'AEVA':'Aeva Technologies Inc. ',
     'AEY':'ADDvantage Technologies Group Inc. ',
     'AEYE':'AudioEye Inc. ',
     'AEZS':'Aeterna Zentaris Inc. ',
     'AFAR':'Aura FAT Projects Acquisition Corp ',
     'AFBI':'Affinity Bancshares Inc.  (MD)',
     'AFCG':'AFC Gamma Inc. ',
     'AFG':'American Financial Group Inc. ',
     'AFIB':'Acutus Medical Inc. ',
     'AFL':'AFLAC Incorporated ',
     'AFMD':'Affimed N.V.',
     'AFRI':'Forafric Global PLC ',
     'AFRM':'Affirm Holdings Inc.  ',
     'AFT':'Apollo Senior Floating Rate Fund Inc. ',
     'AFTR':'AfterNext HealthTech Acquisition Corp. ',
     'AFYA':'Afya Limited  ',
     'AG':'First Majestic Silver Corp.  (Canada)',
     'AGAC':'African Gold Acquisition Corporation ',
     'AGAE':'Allied Gaming & Entertainment Inc. ',
     'AGBA':'AGBA Group Holding Limited ',
     'AGBAW':'AGBA Group Holding Limited ',
     'AGCO':'AGCO Corporation ',
     'AGD':'abrdn Global Dynamic Dividend Fund  of Beneficial Interest',
     'AGE':'AgeX Therapeutics Inc. ',
     'AGEN':'Agenus Inc. ',
     'AGFY':'Agrify Corporation ',
     'AGI':'Alamos Gold Inc.  ',
     'AGIL':'AgileThought Inc.  ',
     'AGILW':'AgileThought Inc. ',
     'AGIO':'Agios Pharmaceuticals Inc. ',
     'AGL':'agilon health inc. ',
     'AGLE':'Aeglea BioTherapeutics Inc. ',
     'AGM':'Federal Agricultural Mortgage Corporation ',
     'AGMH':'AGM Group Holdings Inc. ',
     'AGNC':'AGNC Investment Corp. ',
     'AGO':'Assured Guaranty Ltd. ',
     'AGR':'Avangrid Inc. ',
     'AGRI':'AgriFORCE  Growing Systems Ltd. ',
     'AGRIW':'AgriFORCE  Growing Systems Ltd. ',
     'AGRO':'Adecoagro S.A. ',
     'AGRX':'Agile Therapeutics Inc. ',
     'AGS':'PlayAGS Inc. ',
     'AGTI':'Agiliti Inc. ',
     'AGX':'Argan Inc. ',
     'AGYS':'Agilysys Inc.  (DE)',
     'AHCO':'AdaptHealth Corp. ',
     'AHG':'Akso Health Group ADS',
     'AHH':'Armada Hoffler Properties Inc. ',
     'AHI':'Advanced Health Intelligence Ltd. ADR',
     'AHT':'Ashford Hospitality Trust Inc ',
     'AI':'C3.ai Inc.  ',
     'AIB':'AIB Acquisition Corporation ',
     'AIBBU':'AIB Acquisition Corporation Unit',
     'AIC':'Arlington Asset Investment Corp ',
     'AIF':'Apollo Tactical Income Fund Inc. ',
     'AIG':'American International Group Inc. New ',
     'AIH':'Aesthetic Medical International Holdings Group Ltd. ',
     'AIHS':'Senmiao Technology Limited ',
     'AIM':'AIM ImmunoTech Inc. ',
     'AIMAU':'Aimfinity Investment Corp. I Unit',
     'AIMAW':'Aimfinity Investment Corp. I ',
     'AIMBU':'Aimfinity Investment Corp. I Subunit',
     'AIMD':'Ainos Inc. ',
     'AIMDW':'Ainos Inc. s',
     'AIN':'Albany International Corporation ',
     'AINC':'Ashford Inc. (Holding Company) ',
     'AIO':'Virtus Artificial Intelligence & Technology Opportunities Fund  of Beneficial Interest',
     'AIP':'Arteris Inc. ',
     'AIR':'AAR Corp. ',
     'AIRC':'Apartment Income REIT Corp. ',
     'AIRG':'Airgain Inc. ',
     'AIRI':'Air Industries Group ',
     'AIRS':'AirSculpt Technologies Inc. ',
     'AIRT':'Air T Inc. ',
     'AIRTP':'Air T Inc. Air T Funding Alpha Income Trust Preferred Securities',
     'AIT':'Applied Industrial Technologies Inc. ',
     'AIU':'Meta Data Limited ADS',
     'AIV':'Apartment Investment and Management Company ',
     'AIQUF':'AIR LIQUIDE(L) ',
     'AIXI':'XIAO-I Corporation ',
     'AIZ':'Assurant Inc. ',
     'AJG':'Arthur J. Gallagher & Co. ',
     'AJRD':'Aerojet Rocketdyne Holdings Inc. ',
     'AJX':'Great Ajax Corp. ',
     'AKA':'a.k.a. Brands Holding Corp. ',
     'AKAM':'Akamai Technologies Inc. ',
     'AKAN':'Akanda Corp. ',
     'AKBA':'Akebia Therapeutics Inc. ',
     'AKLI':'Akili Inc. ',
     'AKO/A':'Embotelladora Andina S.A.',
     'AKO/B':'Embotelladora Andina S.A.',
     'AKR':'Acadia Realty Trust ',
     'AKRO':'Akero Therapeutics Inc. ',
     'AKTS':'Akoustis Technologies Inc. ',
     'AKTX':'Akari Therapeutics plc ADS',
     'AKU':'Akumin Inc.  (DE)',
     'AKYA':'Akoya BioSciences Inc. ',
     'AL':'Air Lease Corporation  ',
     'ALAR':'Alarum Technologies Ltd. ',
     'ALB':'Albemarle Corporation ',
     'ALBT':'Avalon GloboCare Corp. ',
     'ALC':'Alcon Inc. ',
     'ALCC':'AltC Acquisition Corp.  ',
     'ALCO':'Alico Inc. ',
     'ALCY':'Alchemy Investments Acquisition Corp 1 ',
     'ALCYU':'Alchemy Investments Acquisition Corp 1 Units',
     'ALCYW':'Alchemy Investments Acquisition Corp 1 s',
     'ALDX':'Aldeyra Therapeutics Inc. ',
     'ALE':'Allete Inc.',
     'ALEC':'Alector Inc. ',
     'ALEX':'Alexander & Baldwin Inc.  REIT Holding Company',
     'ALG':'Alamo Group Inc. ',
     'ALGM':'Allegro MicroSystems Inc. ',
     'ALGN':'Align Technology Inc. ',
     'ALGS':'Aligos Therapeutics Inc. ',
     'ALGT':'Allegiant Travel Company ',
     'ALHC':'Alignment Healthcare Inc. ',
     'ALIM':'Alimera Sciences Inc. ',
     'ALIT':'Alight Inc.  ',
     'ALK':'Alaska Air Group Inc. ',
     'ALKS':'Alkermes plc ',
     'ALKT':'Alkami Technology Inc. ',
     'ALL':'Allstate Corporation ',
     'ALLE':'Allegion plc ',
     'ALLG':'Allego N.V. ',
     'ALLK':'Allakos Inc. ',
     'ALLO':'Allogene Therapeutics Inc. ',
     'ALLR':'Allarity Therapeutics Inc. ',
     'ALLT':'Allot Ltd. ',
     'ALLY':'Ally Financial Inc. ',
     'ALNY':'Alnylam Pharmaceuticals Inc. ',
     'ALORW':'ALSP Orchid Acquisition Corporation I ',
     'ALOT':'AstroNova Inc. ',
     'ALPA':'Alpha Healthcare Acquisition Corp. III  ',
     'ALPAU':'Alpha Healthcare Acquisition Corp. III Units',
     'ALPAW':'Alpha Healthcare Acquisition Corp. III ',
     'ALPN':'Alpine Immune Sciences Inc. ',
     'ALPP':'Alpine 4 Holdings Inc.  ',
     'ALPS':'Alpine Summit Energy Partners Inc.  Subordinate Voting Shares',
     'ALRM':'Alarm.com Holdings Inc. ',
     'ALRN':'Aileron Therapeutics Inc. ',
     'ALRS':'Alerus Financial Corporation ',
     'ALSA':'Alpha Star Acquisition Corporation ',
     'ALSAR':'Alpha Star Acquisition Corporation Rights',
     'ALSAW':'Alpha Star Acquisition Corporation s',
     'ALSN':'Allison Transmission Holdings Inc. ',
     'ALT':'Altimmune Inc. ',
     'ALTG':'Alta Equipment Group Inc.  ',
     'ALTI':'AlTi Global Inc.  ',
     'ALTO':'Alto Ingredients Inc. ',
     'ALTR':'Altair Engineering Inc.  ',
     'ALTU':'Altitude Acquisition Corp.  ',
     'ALTUU':'Altitude Acquisition Corp. Unit',
     'ALTUW':'Altitude Acquisition Corp. ',
     'ALV':'Autoliv Inc. ',
     'ALVO':'Alvotech ',
     'ALVOW':'Alvotech ',
     'ALVR':'AlloVir Inc. ',
     'ALX':'Alexanders Inc. ',
     'ALXO':'ALX Oncology Holdings Inc. ',
     'ALYA':'Alithya Group inc.  Subordinate Voting Shares',
     'ALZN':'Alzamend Neuro Inc. ',
     'AM':'Antero Midstream Corporation ',
     'AMAL':'Amalgamated Financial Corp.  (DE)',
     'AMAM':'Ambrx Biopharma Inc. ',
     'AMAO':'American Acquisition Opportunity Inc.  ',
     'AMAOW':'American Acquisition Opportunity Inc. ',
     'AMAT':'Applied Materials Inc. ',
     'AMBA':'Ambarella Inc. ',
     'AMBC':'Ambac Financial Group Inc. ',
     'AMBI':'Ambipar Emergency Response ',
     'AMBO':'Ambow Education Holding Ltd. American Depository Shares each representing two ',
     'AMBP':'Ardagh Metal Packaging S.A. ',
     'AMC':'AMC Entertainment Holdings Inc.  ',
     'AMCR':'Amcor plc ',
     'AMCX':'AMC Networks Inc.  ',
     'AMD':'Advanced Micro Devices Inc. ',
     'AME':'AMETEK Inc.',
     'AMED':'Amedisys Inc ',
     'AMEH':'Apollo Medical Holdings Inc. ',
     'AMG':'Affiliated Managers Group Inc. ',
     'AMGN':'Amgen Inc. ',
     'AMH':'American Homes 4 Rent  of Beneficial Interest',
     'AMK':'AssetMark Financial Holdings Inc. ',
     'AMKR':'Amkor Technology Inc. ',
     'AMLI':'American Lithium Corp. ',
     'AMLX':'Amylyx Pharmaceuticals Inc. ',
     'AMN':'AMN Healthcare Services Inc AMN Healthcare Services Inc',
     'AMNB':'American National Bankshares Inc. ',
     'AMOT':'Allied Motion Technologies Inc.',
     'AMP':'Ameriprise Financial Inc. ',
     'AMPE':'Ampio Pharmaceuticals Inc.',
     'AMPG':'Amplitech Group Inc. ',
     'AMPGW':'Amplitech Group Inc. s',
     'AMPH':'Amphastar Pharmaceuticals Inc. ',
     'AMPL':'Amplitude Inc.  ',
     'AMPS':'Altus Power Inc.  ',
     'AMPX':'Amprius Technologies Inc. ',
     'AMPY':'Amplify Energy Corp. ',
     'AMR':'Alpha Metallurgical Resources Inc. ',
     'AMRC':'Ameresco Inc.  ',
     'AMRK':'A-Mark Precious Metals Inc. ',
     'AMRN':'Amarin Corporation plc',
     'AMRS':'Amyris Inc. ',
     'AMRX':'Amneal Pharmaceuticals Inc.  ',
     'AMS':'American Shared Hospital Services ',
     'AMSC':'American Superconductor Corporation ',
     'AMSF':'AMERISAFE Inc. ',
     'AMST':'Amesite Inc. ',
     'AMSWA':'American Software Inc.  ',
     'AMT':'American Tower Corporation (REIT) ',
     'AMTB':'Amerant Bancorp Inc.  ',
     'AMTD':'AMTD IDEA Group  each representing two ',
     'AMTI':'Applied Molecular Transport Inc. ',
     'AMTX':'Aemetis Inc. (DE) ',
     'AMWD':'American Woodmark Corporation ',
     'AMWL':'American Well Corporation  ',
     'AMX':'America Movil S.A.B. de C.V.  (each representing the right to receive twenty (20) Series B Shares',
     'AMZN':'Amazon.com Inc. ',
     'AN':'AutoNation Inc. ',
     'ANAB':'AnaptysBio Inc. ',
     'ANDE':'Andersons Inc. ',
     'ANEB':'Anebulo Pharmaceuticals Inc. ',
     'ANET':'Arista Networks Inc. ',
     'ANF':'Abercrombie & Fitch Company ',
     'ANGH':'Anghami Inc. ',
     'ANGHW':'Anghami Inc. s',
     'ANGI':'Angi Inc.  ',
     'ANGO':'AngioDynamics Inc. ',
     'ANIK':'Anika Therapeutics Inc. ',
     'ANIP':'ANI Pharmaceuticals Inc.',
     'ANIX':'Anixa Biosciences Inc. ',
     'ANNX':'Annexon Inc. ',
     'ANSS':'ANSYS Inc. ',
     'ANTE':'AirNet Technology Inc. ',
     'ANTX':'AN2 Therapeutics Inc. ',
     'ANVS':'Annovis Bio Inc. ',
     'ANY':'Sphere 3D Corp. ',
     'ANZUW':'Anzu Special Acquisition Corp I ',
     'AOD':'abrdn Total Dynamic Dividend Fund  of Beneficial Interest',
     'AOGO':'Arogo Capital Acquisition Corp.  ',
     'AOGOU':'Arogo Capital Acquisition Corp. Unit',
     'AOGOW':'Arogo Capital Acquisition Corp. ',
     'AOMR':'Angel Oak Mortgage REIT Inc. ',
     'AON':'Aon plc  (Ireland)',
     'AORT':'Artivion Inc. ',
     'AOS':'A.O. Smith Corporation ',
     'AOSL':'Alpha and Omega Semiconductor Limited ',
     'AOUT':'American Outdoor Brands Inc. ',
     'AP':'Ampco-Pittsburgh Corporation ',
     'APA':'APA Corporation ',
     'APAC':'StoneBridge Acquisition Corporation ',
     'APACW':'StoneBridge Acquisition Corporation ',
     'APAM':'Artisan Partners Asset Management Inc.  ',
     'APCA':'AP Acquisition Corp ',
     'APCX':'AppTech Payments Corp. ',
     'APCXW':'AppTech Payments Corp. ',
     'APD':'Air Products and Chemicals Inc. ',
     'APDN':'Applied DNA Sciences Inc. ',
     'APEI':'American Public Education Inc. ',
     'APG':'APi Group Corporation ',
     'APGB':'Apollo Strategic Growth Capital II ',
     'APGN':'Apexigen Inc. ',
     'APGNW':'Apexigen Inc. ',
     'APH':'Amphenol Corporation ',
     'API':'Agora Inc. ',
     'APLD':'Applied Digital Corporation ',
     'APLE':'Apple Hospitality REIT Inc. ',
     'APLM':'Apollomics Inc. ',
     'APLMW':'Apollomics Inc. ',
     'APLS':'Apellis Pharmaceuticals Inc. ',
     'APLT':'Applied Therapeutics Inc. ',
     'APM':'Aptorum Group Limited ',
     'APMI':'AxonPrime Infrastructure Acquisition Corporation  ',
     'APMIU':'AxonPrime Infrastructure Acquisition Corporation Unit',
     'APMIW':'AxonPrime Infrastructure Acquisition Corporation s',
     'APO':'Apollo Global Management Inc.',
     'APOG':'Apogee Enterprises Inc. ',
     'APP':'Applovin Corporation  ',
     'APPF':'AppFolio Inc.  ',
     'APPH':'AppHarvest Inc. ',
     'APPHW':'AppHarvest Inc. s',
     'APPN':'Appian Corporation  ',
     'APPS':'Digital Turbine Inc. ',
     'APRE':'Aprea Therapeutics Inc. ',
     'APRN':'Blue Apron Holdings Inc.  ',
     'APT':'Alpha Pro Tech Ltd. ',
     'APTM':'Alpha Partners Technology Merger Corp. ',
     'APTMU':'Alpha Partners Technology Merger Corp. Unit',
     'APTMW':'Alpha Partners Technology Merger Corp. ',
     'APTO':'Aptose Biosciences Inc. ',
     'APTV':'Aptiv PLC ',
     'APVO':'Aptevo Therapeutics Inc. ',
     'APWC':'Asia Pacific Wire & Cable Corporation Ltd.  (Bermuda)',
     'APXI':'APx Acquisition Corp. I',
     'APXIW':'APx Acquisition Corp. I ',
     'APYX':'Apyx Medical Corporation ',
     'AQB':'AquaBounty Technologies Inc. ',
     'AQMS':'Aqua Metals Inc. ',
     'AQN':'Algonquin Power & Utilities Corp. ',
     'AQST':'Aquestive Therapeutics Inc. ',
     'AQU':'Aquaron Acquisition Corp. ',
     'AQUNR':'Aquaron Acquisition Corp. Rights',
     'AR':'Antero Resources Corporation ',
     'ARAV':'Aravive Inc. ',
     'ARAY':'Accuray Incorporated ',
     'ARBB':'ARB IOT Group Limited ',
     'ARBE':'Arbe Robotics Ltd. ',
     'ARBEW':'Arbe Robotics Ltd. ',
     'ARBG':'Aequi Acquisition Corp.  ',
     'ARBGW':'Aequi Acquisition Corp. s',
     'ARBK':'Argo Blockchain plc ',
     'ARC':'ARC Document Solutions Inc. ',
     'ARCB':'ArcBest Corporation ',
     'ARCC':'Ares Capital Corporation ',
     'ARCE':'Arco Platform Limited  ',
     'ARCH':'Arch Resources Inc.  ',
     'ARCO':'Arcos Dorados Holdings Inc.  Shares',
     'ARCT':'Arcturus Therapeutics Holdings Inc. ',
     'ARDC':'Ares Dynamic Credit Allocation Fund Inc. ',
     'ARDS':'Aridis Pharmaceuticals Inc. ',
     'ARDX':'Ardelyx Inc. ',
     'ARE':'Alexandria Real Estate Equities Inc. ',
     'AREB':'American Rebel Holdings Inc. ',
     'AREBW':'American Rebel Holdings Inc. s',
     'AREC':'American Resources Corporation  ',
     'AREN':'The Arena Group Holdings Inc. ',
     'ARES':'Ares Management Corporation  ',
     'ARGD':'Argo Group International Holdings Ltd.',
     'ARGO':'Argo Group International Holdings Ltd.',
     'ARGX':'argenx SE ',
     'ARHS':'Arhaus Inc.  ',
     'ARI':'Apollo Commercial Real Estate Finance Inc',
     'ARIS':'Aris Water Solutions Inc.  ',
     'ARIZ':'Arisz Acquisition Corp. ',
     'ARIZW':'Arisz Acquisition Corp. ',
     'ARKO':'ARKO Corp. ',
     'ARKOW':'ARKO Corp. ',
     'ARKR':'Ark Restaurants Corp. ',
     'ARL':'American Realty Investors Inc. ',
     'ARLO':'Arlo Technologies Inc. ',
     'ARLP':'Alliance Resource Partners L.P.',
     'ARM':'Arm Holdings plc ',
     'ARMK':'Aramark ',
     'ARMP':'Armata Pharmaceuticals Inc. ',
     'ARNC':'Arconic Corporation ',
     'AROC':'Archrock Inc. ',
     'AROW':'Arrow Financial Corporation ',
     'ARQQ':'Arqit Quantum Inc. ',
     'ARQQW':'Arqit Quantum Inc. s',
     'ARQT':'Arcutis Biotherapeutics Inc. ',
     'ARR':'ARMOUR Residential REIT Inc.',
     'ARRW':'Arrowroot Acquisition Corp.  ',
     'ARRWU':'Arrowroot Acquisition Corp. Unit',
     'ARRWW':'Arrowroot Acquisition Corp. ',
     'ARRY':'Array Technologies Inc. ',
     'ARTE':'Artemis Strategic Investment Corporation  ',
     'ARTEW':'Artemis Strategic Investment Corporation ',
     'ARTL':'Artelo Biosciences Inc. ',
     'ARTLW':'Artelo Biosciences Inc. ',
     'ARTNA':'Artesian Resources Corporation  ',
     'ARTW':'Arts-Way Manufacturing Co. Inc. ',
     'ARVL':'Arrival ',
     'ARVN':'Arvinas Inc. ',
     'ARW':'Arrow Electronics Inc. ',
     'ARWR':'Arrowhead Pharmaceuticals Inc. ',
     'ARYD':'ARYA Sciences Acquisition Corp IV  Odinary Shares',
     'ARYE':'ARYA Sciences Acquisition Corp V ',
     'ASA':'ASA  Gold and Precious Metals Limited',
     'ASAI':'Sendas Distribuidora S A ADS',
     'ASAN':'Asana Inc.  ',
     'ASB':'Associated Banc-Corp ',
     'ASC':'Ardmore Shipping Corporation ',
     'ASG':'Liberty All-Star Growth Fund Inc.',
     'ASGI':'abrdn Global Infrastructure Income Fund  of Beneficial Interest',
     'ASGN':'ASGN Incorporated ',
     'ASH':'Ashland Inc. ',
     'ASIX':'AdvanSix Inc. ',
     'ASLE':'AerSale Corporation ',
     'ASLN':'ASLAN Pharmaceuticals Limited ',
     'ASM':'Avino Silver & Gold Mines Ltd.  (Canada)',
     'ASMB':'Assembly Biosciences Inc. ',
     'ASML':'ASML Holding N.V. New York Registry Shares',
     'ASND':'Ascendis Pharma A/S ',
     'ASNS':'Actelis Networks Inc. ',
     'ASO':'Academy Sports and Outdoors Inc. ',
     'ASPAW':'ABRI SPAC I INC. ',
     'ASPI':'ASP Isotopes Inc. ',
     'ASPN':'Aspen Aerogels Inc. ',
     'ASPS':'Altisource Portfolio Solutions S.A. ',
     'ASR':'Grupo Aeroportuario del Sureste S.A. de C.V. ',
     'ASRT':'Assertio Holdings Inc. ',
     'ASRV':'AmeriServ Financial Inc. ',
     'ASST':'Asset Entities Inc. Class B ',
     'ASTC':'Astrotech Corporation (DE) ',
     'ASTE':'Astec Industries Inc. ',
     'ASTI':'Ascent Solar Technologies Inc. ',
     'ASTL':'Algoma Steel Group Inc. ',
     'ASTLW':'Algoma Steel Group Inc. ',
     'ASTR':'Astra Space Inc.  ',
     'ASTS':'AST SpaceMobile Inc.  ',
     'ASTSW':'AST SpaceMobile Inc. ',
     'ASUR':'Asure Software Inc ',
     'ASX':'ASE Technology Holding Co. Ltd.',
     'ASXC':'Asensus Surgical Inc. ',
     'ASYS':'Amtech Systems Inc. ',
     'ATAI':'ATAI Life Sciences N.V. ',
     'ATAK':'Aurora Technology Acquisition Corp. ',
     'ATAKU':'Aurora Technology Acquisition Corp. Unit',
     'ATAQ':'Altimar Acquisition Corp. III ',
     'ATAT':'Atour Lifestyle Holdings Limited ',
     'ATCOL':'Atlas Corp. ',
     'ATEC':'Alphatec Holdings Inc. ',
     'ATEK':'Athena Technology Acquisition Corp. II  ',
     'ATEN':'A10 Networks Inc. ',
     'ATER':'Aterian Inc. ',
     'ATEX':'Anterix Inc. ',
     'ATGE':'Adtalem Global Education Inc. ',
     'ATHA':'Athira Pharma Inc. ',
     'ATHE':'Alterity Therapeutics Limited ',
     'ATHM':'Autohome Inc.  each representing four .',
     'ATHX':'Athersys Inc. ',
     'ATI':'ATI Inc. ',
     'ATIF':'ATIF Holdings Limited ',
     'ATIP':'ATI Physical Therapy Inc.  ',
     'ATKR':'Atkore Inc. ',
     'ATLC':'Atlanticus Holdings Corporation ',
     'ATLO':'Ames National Corporation ',
     'ATLX':'Atlas Lithium Corporation ',
     'ATMC':'AlphaTime Acquisition Corp ',
     'ATMCR':'AlphaTime Acquisition Corp Right',
     'ATMCU':'AlphaTime Acquisition Corp Unit',
     'ATMCW':'AlphaTime Acquisition Corp ',
     'ATMU':'Atmus Filtration Technologies Inc. ',
     'ATMV':'AlphaVest Acquisition Corp ',
     'ATMVR':'AlphaVest Acquisition Corp Right',
     'ATMVU':'AlphaVest Acquisition Corp Unit',
     'ATNF':'180 Life Sciences Corp. ',
     'ATNFW':'180 Life Sciences Corp. ',
     'ATNI':'ATN International Inc. ',
     'ATNM':'Actinium Pharmaceuticals Inc. (Delaware) ',
     'ATO':'Atmos Energy Corporation ',
     'ATOM':'Atomera Incorporated ',
     'ATOS':'Atossa Therapeutics Inc. ',
     'ATR':'AptarGroup Inc. ',
     'ATRA':'Atara Biotherapeutics Inc. ',
     'ATRC':'AtriCure Inc. ',
     'ATRI':'Atrion Corporation ',
     'ATRO':'Astronics Corporation ',
     'ATS':'ATS Corporation ',
     'ATSG':'Air Transport Services Group Inc',
     'ATTO':'Atento S.A. ',
     'ATUS':'Altice USA Inc.  ',
     'ATVI':'Activision Blizzard Inc. ',
     'ATXG':'Addentax Group Corp. ',
     'ATXI':'Avenue Therapeutics Inc. ',
     'ATXS':'Astria Therapeutics Inc. ',
     'AU':'AngloGold Ashanti Limited ',
     'AUB':'Atlantic Union Bankshares Corporation ',
     'AUBN':'Auburn National Bancorporation Inc. ',
     'AUDC':'AudioCodes Ltd. ',
     'AUGX':'Augmedix Inc. ',
     'AUID':'authID Inc. ',
     'AULT':'Ault Alliance Inc. ',
     'AUMN':'Golden Minerals Company ',
     'AUPH':'Aurinia Pharmaceuticals Inc ',
     'AUR':'Aurora Innovation Inc.  ',
     'AURA':'Aura Biosciences Inc. ',
     'AURC':'Aurora Acquisition Corp. ',
     'AUROW':'Aurora Innovation Inc. ',
     'AUST':'Austin Gold Corp. ',
     'AUTL':'Autolus Therapeutics plc ',
     'AUUD':'Auddia Inc. ',
     'AUUDW':'Auddia Inc. s',
     'AUVI':'Applied UV Inc. ',
     'AUVIP':'Applied UV Inc. 10.5% Series A Cumulative Perpetual Preferred Stock $0.0001 par value per share',
     'AVA':'Avista Corporation ',
     'AVAH':'Aveanna Healthcare Holdings Inc. ',
     'AVAL':'Grupo Aval Acciones y Valores S.A. ADR (Each representing 20 preferred shares)',
     'AVAV':'AeroVironment Inc. ',
     'AVB':'AvalonBay Communities Inc. ',
     'AVD':'American Vanguard Corporation  ($0.10 Par Value)',
     'AVDL':'Avadel Pharmaceuticals plc ',
     'AVDX':'AvidXchange Holdings Inc. ',
     'AVGO':'Broadcom Inc. ',
     'AVGR':'Avinger Inc. ',
     'AVHI':'Achari Ventures Holdings Corp. I ',
     'AVHIW':'Achari Ventures Holdings Corp. I ',
     'AVID':'Avid Technology Inc. ',
     'AVIR':'Atea Pharmaceuticals Inc. ',
     'AVK':'Advent Convertible and Income Fund',
     'AVNS':'Avanos Medical Inc. ',
     'AVNT':'Avient Corporation ',
     'AVNW':'Aviat Networks Inc. ',
     'AVO':'Mission Produce Inc. ',
     'AVPT':'AvePoint Inc.  ',
     'AVPTW':'AvePoint Inc. ',
     'AVRO':'AVROBIO Inc. ',
     'AVT':'Avnet Inc. ',
     'AVTA':'Avantax Inc. ',
     'AVTE':'Aerovate Therapeutics Inc. ',
     'AVTR':'Avantor Inc. ',
     'AVTX':'Avalo Therapeutics Inc. ',
     'AVXL':'Anavex Life Sciences Corp. ',
     'AVY':'Avery Dennison Corporation ',
     'AWH':'Aspira Womens Health Inc. ',
     'AWI':'Armstrong World Industries Inc ',
     'AWIN':'AERWINS Technologies Inc. ',
     'AWINW':'AERWINS Technologies Inc. ',
     'AWK':'American Water Works Company Inc. ',
     'AWP':'abrdn Global Premier Properties Fund  of Beneficial Interest',
     'AWR':'American States Water Company ',
     'AWRE':'Aware Inc. ',
     'AWX':'Avalon Holdings Corporation ',
     'AX':'Axos Financial Inc. ',
     'AXDX':'Accelerate Diagnostics Inc. ',
     'AXGN':'Axogen Inc. ',
     'AXL':'American Axle & Manufacturing Holdings Inc. ',
     'AXLA':'Axcella Health Inc. ',
     'AXNX':'Axonics Inc. ',
     'AXON':'Axon Enterprise Inc. ',
     'AXP':'American Express Company ',
     'AXR':'AMREP Corporation ',
     'AXS':'Axis Capital Holdings Limited ',
     'AXS^E':'Axis Capital Holdings Limited Depositary Shares each representing 1/100th interest in a share of a 5.50% Series E Preferred Shares',
     'AXSM':'Axsome Therapeutics Inc. ',
     'AXTA':'Axalta Coating Systems Ltd. ',
     'AXTI':'AXT Inc ',
     'AY':'Atlantica Sustainable Infrastructure plc ',
     'AYI':'Acuity Brands Inc.',
     'AYRO':'AYRO Inc. ',
     'AYTU':'Aytu BioPharma Inc.  ',
     'AYX':'Alteryx Inc.  ',
     'AZ':'A2Z Smart Technologies Corp. ',
     'AZEK':'The AZEK Company Inc.  ',
     'AZN':'AstraZeneca PLC ',
     'AZO':'AutoZone Inc. ',
     'AZPN':'Aspen Technology Inc. ',
     'AZRE':'Azure Power Global Limited Equity Shares',
     'AZTA':'Azenta Inc.',
     'AZTR':'Azitra Inc ',
     'AZUL':'Azul S.A.  (each representing three preferred shares)',
     'AZYO':'Aziyo Biologics Inc.  ',
     'AZZ':'AZZ Inc.',
     'B':'Barnes Group Inc. ',
     'BA':'Boeing Company ',
     'BABA':'Alibaba Group Holding Limited ',
     'BAC':'Bank of America Corporation ',
     'BACA':'Berenson Acquisition Corp. I  ',
     'BACK':'IMAC Holdings Inc. ',
     'BAER':'Bridger Aerospace Group Holdings Inc. ',
     'BAERW':'Bridger Aerospace Group Holdings Inc. ',
     'BAFN':'BayFirst Financial Corp. ',
     'BAH':'Booz Allen Hamilton Holding Corporation ',
     'BAK':'Braskem SA ADR',
     'BALL':'Ball Corporation ',
     'BALY':'Ballys Corporation ',
     'BAM':'Brookfield Asset Management Inc.',
     'BANC':'Banc of California Inc. ',
     'BAND':'Bandwidth Inc.  ',
     'BANF':'BancFirst Corporation ',
     'BANFP':'BancFirst Corporation - BFC Capital Trust II Cumulative Trust Preferred Securities',
     'BANL':'CBL International Limited ',
     'BANR':'Banner Corporation ',
     'BANX':'ArrowMark Financial Corp. ',
     'BAOS':'Baosheng Media Group Holdings Limited ',
     'BAP':'Credicorp Ltd. ',
     'BARK':'BARK Inc.  ',
     'BASE':'Couchbase Inc. ',
     'BFFAF':'BASF SE. ',
     'BATL':'Battalion Oil Corporation ',
     'BATRA':'Liberty Media Corporation Series A Liberty Braves ',
     'BATRK':'Liberty Media Corporation Series C Liberty Braves ',
     'BAX':'Baxter International Inc. ',
     'BB':'BlackBerry Limited ',
     'BBAI':'BigBear.ai Inc. ',
     'BBAR':'Banco BBVA Argentina S.A. ADS',
     'BBCP':'Concrete Pumping Holdings Inc. ',
     'BBD':'Banco Bradesco Sa ',
     'BBDC':'Barings BDC Inc. ',
     'BBDO':'Banco Bradesco Sa  (each representing one Common Share)',
     'BBGI':'Beasley Broadcast Group Inc.  ',
     'BBIG':'Vinco Ventures Inc. ',
     'BBIO':'BridgeBio Pharma Inc. ',
     'BBLG':'Bone Biologics Corp ',
     'BBLGW':'Bone Biologics Corp s',
     'BBN':'BlackRock Taxable Municipal Bond Trust  of Beneficial Interest',
     'BBSI':'Barrett Business Services Inc. ',
     'BBU':'Brookfield Business Partners L.P. Limited Partnership Units',
     'BBUC':'Brookfield Business Corporation  Exchangeable Subordinate Voting Shares',
     'BBVA':'Banco Bilbao Vizcaya Argentaria S.A. ',
     'BBW':'Build-A-Bear Workshop Inc. ',
     'BBWI':'Bath & Body Works Inc.',
     'BBY':'Best Buy Co. Inc. ',
     'BC':'Brunswick Corporation ',
     'BCAB':'BioAtla Inc. ',
     'BCAL':'Southern California Bancorp ',
     'BCAN':'BYND Cannasoft Enterprises Inc. ',
     'BCAT':'BlackRock Capital Allocation Term Trust  of Beneficial Interest',
     'BCBP':'BCB Bancorp Inc. (NJ) ',
     'BCC':'Boise Cascade L.L.C. ',
     'BCDA':'BioCardia Inc. ',
     'BCDAW':'BioCardia Inc. ',
     'BCE':'BCE Inc. ',
     'BCEL':'Atreca Inc.  ',
     'BCH':'Banco De Chile Banco De Chile ADS',
     'BCLI':'Brainstorm Cell Therapeutics Inc. ',
     'BCML':'BayCom Corp ',
     'BCO':'Brinks Company ',
     'BCOV':'Brightcove Inc. ',
     'BCOW':'1895 Bancorp of Wisconsin Inc. (MD) ',
     'BCPC':'Balchem Corporation ',
     'BCRX':'BioCryst Pharmaceuticals Inc. ',
     'BCS':'Barclays PLC ',
     'BCSF':'Bain Capital Specialty Finance Inc. ',
     'BCTX':'BriaCell Therapeutics Corp. ',
     'BCTXW':'BriaCell Therapeutics Corp. ',
     'BCV':'Bancroft Fund Ltd.',
     'BCX':'BlackRock Resources  of Beneficial Interest',
     'BCYC':'Bicycle Therapeutics plc ',
     'BDC':'Belden Inc ',
     'BDJ':'Blackrock Enhanced Equity Dividend Trust',
     'BDL':'Flanigans Enterprises Inc. ',
     'BDN':'Brandywine Realty Trust ',
     'BDRX':'Biodexa Pharmaceuticals plc American Depositary Shs',
     'BDSX':'Biodesix Inc. ',
     'BDTX':'Black Diamond Therapeutics Inc. ',
     'BDX':'Becton Dickinson and Company ',
     'BE':'Bloom Energy Corporation  ',
     'BEAM':'Beam Therapeutics Inc. ',
     'BEAT':'Heartbeam Inc. ',
     'BEATW':'Heartbeam Inc. ',
     'BECN':'Beacon Roofing Supply Inc. ',
     'BEDU':'Bright Scholar Education Holdings Limited  each  representing four',
     'BEEM':'Beam Global ',
     'BEEMW':'Beam Global ',
     'BEKE':'KE Holdings Inc  (each representing three )',
     'BELFA':'Bel Fuse Inc.  ',
     'BELFB':'Bel Fuse Inc. Class B ',
     'BEN':'Franklin Resources Inc. ',
     'BENF':'Beneficient  ',
     'BENFW':'Beneficient ',
     'BEP':'Brookfield Renewable Partners L.P.',
     'BEPC':'Brookfield Renewable Corporation  Subordinate Voting Shares',
     'BERY':'Berry Global Group Inc. ',
     'BEST':'BEST Inc.  each representing twenty (20) ',
     'BF/A':'Brown Forman Corporation',
     'BF/B':'Brown Forman Corporation',
     'BFAC':'Battery Future Acquisition Corp. ',
     'BFAM':'Bright Horizons Family Solutions Inc. ',
     'BFC':'Bank First Corporation ',
     'BFH':'Bread Financial Holdings Inc. ',
     'BFI':'BurgerFi International Inc. ',
     'BFIIW':'BurgerFi International Inc. ',
     'BFIN':'BankFinancial Corporation ',
     'BFK':'BlackRock Municipal Income Trust',
     'BFLY':'Butterfly Network Inc.  ',
     'BFRG':'Bullfrog AI Holdings Inc. ',
     'BFRGW':'Bullfrog AI Holdings Inc. s',
     'BFRI':'Biofrontera Inc. ',
     'BFRIW':'Biofrontera Inc. s',
     'BFS':'Saul Centers Inc. ',
     'BFST':'Business First Bancshares Inc. ',
     'BFZ':'BlackRock California Municipal Income Trust',
     'BG':'Bunge Limited Bunge Limited',
     'BGB':'Blackstone Strategic Credit 2027 Term Fund  of Beneficial Interest',
     'BGC':'BGC Group Inc.  ',
     'BGFV':'Big 5 Sporting Goods Corporation ',
     'BGH':'Barings Global Short Duration High Yield Fund  of Beneficial Interests',
     'BGI':'Birks Group Inc. ',
     'BGNE':'BeiGene Ltd. ',
     'BGR':'BlackRock Energy and Resources Trust',
     'BGRY':'Berkshire Grey Inc.  ',
     'BGRYW':'Berkshire Grey Inc. ',
     'BGS':'B&G Foods Inc. B&G Foods Inc. ',
     'BGSF':'BGSF Inc. ',
     'BGT':'BlackRock Floating Rate Income Trust',
     'BGX':'Blackstone Long Short Credit Income Fund ',
     'BGXX':'Bright Green Corporation ',
     'BGY':'Blackrock Enhanced International Dividend Trust',
     'BH':'Biglari Holdings Inc. Class B ',
     'BHAC':'Crixus BH3 Acquisition Company  ',
     'BHACU':'Crixus BH3 Acquisition Company Units',
     'BHACW':'Crixus BH3 Acquisition Company s',
     'BHAT':'Blue Hat Interactive Entertainment Technology ',
     'BHB':'Bar Harbor Bankshares Inc. ',
     'BHC':'Bausch Health Companies Inc. ',
     'BHE':'Benchmark Electronics Inc. ',
     'BHF':'Brighthouse Financial Inc. ',
     'BHG':'Bright Health Group Inc. ',
     'BHIL':'Benson Hill Inc. ',
     'BHK':'Blackrock Core Bond Trust Blackrock Core Bond Trust',
     'BHLB':'Berkshire Hills Bancorp Inc. ',
     'BHM':'Bluerock Homes Trust Inc.  ',
     'BHP':'BHP Group Limited  (Each representing two )',
     'BHR':'Braemar Hotels & Resorts Inc. ',
     'BHRB':'Burke & Herbert Financial Services Corp. ',
     'BHV':'BlackRock Virginia Municipal Bond Trust',
     'BHVN':'Biohaven Ltd. ',
     'BIAF':'bioAffinity Technologies Inc. ',
     'BIAFW':'bioAffinity Technologies Inc. ',
     'BIDU':'Baidu Inc. ADS',
     'BIG':'Big Lots Inc. ',
     'BIGC':'BigCommerce Holdings Inc. Series 1 ',
     'BIGZ':'BlackRock Innovation and Growth Term Trust  of Beneficial Interest',
     'BIIB':'Biogen Inc. ',
     'BILI':'Bilibili Inc. ',
     'BILL':'BILL Holdings Inc. ',
     'BIMI':'BIMI International Medical Inc. ',
     'BIO':'Bio-Rad Laboratories Inc.  ',
     'BIOC':'Biocept Inc. ',
     'BIOL':'Biolase Inc. ',
     'BIOR':'Biora Therapeutics Inc. ',
     'BIOS':'BioPlus Acquisition Corp. ',
     'BIOX':'Bioceres Crop Solutions Corp. ',
     'BIP':'Brookfield Infrastructure Partners LP Limited Partnership Units',
     'BIPC':'Brookfield Infrastructure Corporation',
     'BIPH':'Brookfield Infrastructure Corporation 5.000% Subordinated Notes due 2081',
     'BIPI':'BIP Bermuda Holdings I Limited 5.125% Perpetual Subordinated Notes',
     'BIRD':'Allbirds Inc.  ',
     'BIT':'BlackRock Multi-Sector Income Trust  of Beneficial Interest',
     'BITE':'Bite Acquisition Corp. ',
     'BITF':'Bitfarms Ltd. ',
     'BIVI':'BioVie Inc.  ',
     'BJ':'BJs Wholesale Club Holdings Inc. ',
     'BJDX':'Bluejay Diagnostics Inc. ',
     'BJRI':'BJs Restaurants Inc. ',
     'BK':'The Bank of New York Mellon Corporation ',
     'BKCC':'BlackRock Capital Investment Corporation ',
     'BKD':'Brookdale Senior Living Inc. ',
     'BKDT':'Brookdale Senior Living Inc. 7.00% Tangible Equity Units',
     'BKE':'Buckle Inc. ',
     'BKH':'Black Hills Corporation ',
     'BKI':'Black Knight Inc. ',
     'BKKT':'Bakkt Holdings Inc.  ',
     'BKN':'BlackRock Investment Quality Municipal Trust Inc. (The)',
     'BKNG':'Booking Holdings Inc. ',
     'BKR':'Baker Hughes Company  ',
     'BKSC':'Bank of South Carolina Corp. ',
     'BKSY':'BlackSky Technology Inc.  ',
     'BKT':'BlackRock Income Trust Inc. (The)',
     'BKTI':'BK Technologies Corporation ',
     'BKU':'BankUnited Inc. ',
     'BKYI':'BIO-key International Inc. ',
     'BL':'BlackLine Inc. ',
     'BLACR':'Bellevue Life Sciences Acquisition Corp. Rights',
     'BLACU':'Bellevue Life Sciences Acquisition Corp. Unit',
     'BLACW':'Bellevue Life Sciences Acquisition Corp. ',
     'BLBD':'Blue Bird Corporation ',
     'BLBX':'Blackboxstocks Inc. ',
     'BLCO':'Bausch + Lomb Corporation ',
     'BLD':'TopBuild Corp. ',
     'BLDE':'Blade Air Mobility Inc.  ',
     'BLDEW':'Blade Air Mobility Inc. s',
     'BLDP':'Ballard Power Systems Inc. ',
     'BLDR':'Builders FirstSource Inc. ',
     'BLE':'BlackRock Municipal Income Trust II',
     'BLEUR':'bleuacacia ltd Rights',
     'BLFS':'BioLife Solutions Inc. ',
     'BLFY':'Blue Foundry Bancorp ',
     'BLIN':'Bridgeline Digital Inc. ',
     'BLK':'BlackRock Inc. ',
     'BLKB':'Blackbaud Inc. ',
     'BLMN':'Bloomin Brands Inc. ',
     'BLND':'Blend Labs Inc.  ',
     'BLNG':'Belong Acquisition Corp.  ',
     'BLNGU':'Belong Acquisition Corp. Units',
     'BLNGW':'Belong Acquisition Corp. ',
     'BLNK':'Blink Charging Co. ',
     'BLPH':'Bellerophon Therapeutics Inc. ',
     'BLRX':'BioLineRx Ltd. ',
     'BLTE':'Belite Bio Inc ',
     'BLUA':'BlueRiver Acquisition Corp. ',
     'BLUE':'bluebird bio Inc. ',
     'BLW':'Blackrock Limited Duration Income Trust',
     'BLX':'Banco Latinoamericano de Comercio Exterior S.A.',
     'BLZE':'Backblaze Inc.  ',
     'BMA':'Banco Macro S.A.  ADR (representing Ten Class B )',
     'BMAC':'Black Mountain Acquisition Corp.  ',
     'BMBL':'Bumble Inc.  ',
     'BME':'Blackrock Health Sciences Trust',
     'BMEA':'Biomea Fusion Inc. ',
     'BMEZ':'BlackRock Health Sciences Term Trust  of Beneficial Interest',
     'BMI':'Badger Meter Inc. ',
     'BMN':'BlackRock 2037 Municipal Target Term Trust  of Beneficial Interest',
     'BMO':'Bank Of Montreal ',
     'BMR':'Beamr Imaging Ltd. ',
     'BMRA':'Biomerica Inc. ',
     'BMRC':'Bank of Marin Bancorp ',
     'BMRN':'BioMarin Pharmaceutical Inc. ',
     'BMTX':'BM Technologies Inc. ',
     'BMY':'Bristol-Myers Squibb Company ',
     'BN':'Brookfield Corporation  Limited Voting Shares',
     'BNED':'Barnes & Noble Education Inc ',
     'BNGO':'Bionano Genomics Inc. ',
     'BNGOW':'Bionano Genomics Inc. ',
     'BNH':'Brookfield Finance Inc. 4.625% Subordinated Notes due October 16 2080',
     'BNIX':'Bannix Acquisition Corp. ',
     'BNIXR':'Bannix Acquisition Corp. Right',
     'BNIXW':'Bannix Acquisition Corp. ',
     'BNJ':'Brookfield Finance Inc. 4.50% Perpetual Subordinated Notes',
     'BNL':'Broadstone Net Lease Inc. ',
     'BNMV':'BitNile Metaverse Inc. ',
     'BNOX':'Bionomics Limited American Depository Shares',
     'BNR':'Burning Rock Biotech Limited ',
     'BNRE':'Brookfield Reinsurance Ltd.  Exchangeable Limited Voting Shares',
     'BNRG':'Brenmiller Energy Ltd ',
     'BNS':'Bank Nova Scotia Halifax Pfd 3 ',
     'BNTC':'Benitec Biopharma Inc. ',
     'BNTX':'BioNTech SE ',
     'BNY':'BlackRock New York Municipal Income Trust',
     'BOAC':'Bluescape Opportunities Acquisition Corp. ',
     'BOC':'Boston Omaha Corporation  ',
     'BOCN':'Blue Ocean Acquisition Corp ',
     'BOCNU':'Blue Ocean Acquisition Corp Unit',
     'BOCNW':'Blue Ocean Acquisition Corp s',
     'BODY':'The Beachbody Company Inc.  ',
     'BOE':'Blackrock Enhanced Global Dividend Trust  of Beneficial Interest',
     'BOF':'BranchOut Food Inc. ',
     'BOH':'Bank of Hawaii Corporation ',
     'BOKF':'BOK Financial Corporation ',
     'BOLT':'Bolt Biotherapeutics Inc. ',
     'BON':'Bon Natural Life Limited ',
     'BOOM':'DMC Global Inc. ',
     'BOOT':'Boot Barn Holdings Inc. ',
     'BORR':'Borr Drilling Limited ',
     'BOSC':'B.O.S. Better Online Solutions ',
     'BOTJ':'Bank of the James Financial Group Inc. ',
     'BOWL':'Bowlero Corp.  ',
     'BOX':'Box Inc.  ',
     'BOXL':'Boxlight Corporation  ',
     'BP':'BP p.l.c. ',
     'BPMC':'Blueprint Medicines Corporation ',
     'BPOP':'Popular Inc. ',
     'BPRN':'Princeton Bancorp Inc.  (PA)',
     'BPT':'BP Prudhoe Bay Royalty Trust ',
     'BPTH':'Bio-Path Holdings Inc. ',
     'BPTS':'Biophytis SA  (0.01 Euro)',
     'BQ':'Boqii Holding Limited  representing ',
     'BR':'Broadridge Financial Solutions Inc. ',
     'BRAG':'Bragg Gaming Group Inc. ',
     'BRBR':'BellRing Brands Inc. ',
     'BRBS':'Blue Ridge Bankshares Inc. ',
     'BRC':'Brady Corporation ',
     'BRCC':'BRC Inc.  ',
     'BRD':'Beard Energy Transition Acquisition Corp.  ',
     'BRDG':'Bridge Investment Group Holdings Inc.  ',
     'BRDS':'Bird Global Inc.  ',
     'BREA':'Brera Holdings PLC Class B ',
     'BREZ':'Breeze Holdings Acquisition Corp. ',
     'BREZR':'Breeze Holdings Acquisition Corp. Right',
     'BREZW':'Breeze Holdings Acquisition Corp. ',
     'BRFH':'Barfresh Food Group Inc. ',
     'BRFS':'BRF S.A.',
     'BRID':'Bridgford Foods Corporation ',
     'BRK.A':'Berkshire Hathaway Inc.  ',
     'BRK.B':'Berkshire Hathaway   ',
     'BRKH':'BurTech Acquisition Corp.  ',
     'BRKHU':'BurTech Acquisition Corp. Unit',
     'BRKHW':'BurTech Acquisition Corp. s',
     'BRKL':'Brookline Bancorp Inc. ',
     'BRKR':'Bruker Corporation ',
     'BRLI':'Brilliant Acquisition Corporation ',
     'BRLIR':'Brilliant Acquisition Corporation Rights',
     'BRLIU':'Brilliant Acquisition Corporation Unit',
     'BRLT':'Brilliant Earth Group Inc.  ',
     'BRN':'Barnwell Industries Inc. ',
     'BRO':'Brown & Brown Inc. ',
     'BROG':'Brooge Energy Limited ',
     'BROGW':'Brooge Holdings Limited  expiring 12/20/2024',
     'BROS':'Dutch Bros Inc.  ',
     'BRP':'BRP Group Inc. (Insurance Company)  ',
     'BRQS':'Borqs Technologies Inc. ',
     'BRSH':'Bruush Oral Care Inc. ',
     'BRSHW':'Bruush Oral Care Inc. ',
     'BRSP':'BrightSpire Capital Inc.  ',
     'BRT':'BRT Apartments Corp. (MD) ',
     'BRTX':'BioRestorative Therapies Inc.  (NV)',
     'BRW':'Saba Capital Income & Opportunities Fund SBI',
     'BRX':'Brixmor Property Group Inc. ',
     'BRY':'Berry Corporation (bry) ',
     'BRZE':'Braze Inc.  ',
     'BSAC':'Banco Santander - Chile ADS',
     'BSAQ':'Black Spade Acquisition Co ',
     'BSBK':'Bogota Financial Corp. ',
     'BSBR':'Banco Santander Brasil SA  each representing one unit',
     'BSET':'Bassett Furniture Industries Incorporated ',
     'BSFC':'Blue Star Foods Corp. ',
     'BSGM':'BioSig Technologies Inc. ',
     'BSIG':'BrightSphere Investment Group Inc. ',
     'BSL':'Blackstone Senior Floating Rate 2027 Term Fund  of Beneficial Interest',
     'BSM':'Black Stone Minerals L.P. Common units representing limited partner interests',
     'BSQR':'BSQUARE Corporation ',
     'BSRR':'Sierra Bancorp ',
     'BSVN':'Bank7 Corp. ',
     'BSX':'Boston Scientific Corporation ',
     'BSY':'Bentley Systems Incorporated Class B ',
     'BTAI':'BioXcel Therapeutics Inc. ',
     'BTB':'Bit Brother Limited ',
     'BTBD':'BT Brands Inc. ',
     'BTBDW':'BT Brands Inc. ',
     'BTBT':'Bit Digital Inc. ',
     'BTCM':'BIT Mining Limited ADS',
     'BTCS':'BTCS Inc. ',
     'BTCY':'Biotricity Inc. ',
     'BTDR':'Bitdeer Technologies Group ',
     'BTE':'Baytex Energy Corp ',
     'BTG':'B2Gold Corp  (Canada)',
     'BTI':'British American Tobacco  Industries p.l.c.  ADR',
     'BTM':'Bitcoin Depot Inc.  ',
     'BTMD':'Biote Corp.  ',
     'BTMDW':'Biote Corp. ',
     'BTMWW':'Bitcoin Depot Inc. ',
     'BTO':'John Hancock Financial Opportunities Fund ',
     'BTOG':'Bit Origin Limited ',
     'BTT':'BlackRock Municipal 2030 Target Term Trust',
     'BTTR':'Better Choice Company Inc. ',
     'BTTX':'Better Therapeutics Inc. ',
     'BTU':'Peabody Energy Corporation ',
     'BTWN':'Bridgetown Holdings Limited ',
     'BTWNW':'Bridgetown Holdings Limited s',
     'BTZ':'BlackRock Credit Allocation Income Trust',
     'BUD':'Anheuser-Busch Inbev SA Sponsored ADR (Belgium)',
     'BUI':'BlackRock Utility Infrastructure & Power Opportunities Trust',
     'BUJAU':'Bukit Jalil Global Acquisition 1 Ltd. Unit',
     'BUR':'Burford Capital Limited ',
     #'BBRYF':'Burberry Group plc', 
     'BURL':'Burlington Stores Inc. ',
     'BURU':'Nuburu Inc. ',
     'BUSE':'First Busey Corporation  ',
     'BV':'BrightView Holdings Inc. ',
     'BVH':'Bluegreen Vacations Holding Corporation  ',
     'BVN':'Buenaventura Mining Company Inc.',
     'BVS':'Bioventus Inc.  ',
     'BVXV':'BiondVax Pharmaceuticals Ltd. ',
     'BW':'Babcock & Wilcox Enterprises Inc. ',
     'BWA':'BorgWarner Inc. ',
     'BWAC':'Better World Acquisition Corp. ',
     'BWAQ':'Blue World Acquisition Corporation ',
     'BWAY':'BrainsWay Ltd. ',
     'BWB':'Bridgewater Bancshares Inc. ',
     'BWC':'Blue Whale Acquisition Corp I ',
     'BWEN':'Broadwind Inc. ',
     'BWFG':'Bankwell Financial Group Inc. ',
     'BWG':'BrandywineGLOBAL Global Income Opportunities Fund Inc.',
     'BWMN':'Bowman Consulting Group Ltd. ',
     'BWMX':'Betterware de Mexico S.A.P.I. de C.V. ',
     'BWV':'Blue Water Biotech Inc. ',
     'BWXT':'BWX Technologies Inc. ',
     'BX':'Blackstone Inc. ',
     'BXC':'Bluelinx Holdings Inc. ',
     'BXMT':'Blackstone Mortgage Trust Inc. ',
     'BXMX':'Nuveen S&P 500 Buy-Write Income Fund  of Beneficial Interest',
     'BXP':'Boston Properties Inc. ',
     'BXRX':'Baudax Bio Inc. ',
     'BXSL':'Blackstone Secured Lending Fund  of Beneficial Interest',
     'BY':'Byline Bancorp Inc. ',
     'BYD':'Boyd Gaming Corporation ',
     'BYFC':'Broadway Financial Corporation ',
     'BYM':'Blackrock Municipal Income Quality Trust  of Beneficial Interest',
     'BYN':'Banyan Acquisition Corporation  ',
     'BYND':'Beyond Meat Inc. ',
     'BYNO':'byNordic Acquisition Corporation  ',
     'BYNOU':'byNordic Acquisition Corporation Units',
     'BYNOW':'byNordic Acquisition Corporation ',
     'BYRN':'Byrna Technologies Inc. ',
     'BYSI':'BeyondSpring Inc. ',
     'BYTS':'BYTE Acquisition Corp. ',
     'BYTSU':'BYTE Acquisition Corp. Units',
     'BYTSW':'BYTE Acquisition Corp. s',
     'BZ':'KANZHUN LIMITED American Depository Shares',
     'BZFD':'BuzzFeed Inc.  ',
     'BZFDW':'BuzzFeed Inc. ',
     'BZH':'Beazer Homes USA Inc. ',
     'BZUN':'Baozun Inc. ',
     'C':'Citigroup Inc. ',
     'CAAP':'Corporacion America Airports SA ',
     'CAAS':'China Automotive Systems Inc. ',
     'CABA':'Cabaletta Bio Inc. ',
     'CABO':'Cable One Inc. ',
     'CAC':'Camden National Corporation ',
     'CACC':'Credit Acceptance Corporation ',
     'CACI':'CACI International Inc.  ',
     'CACO':'Caravelle International Group ',
     'CADE':'Cadence Bank ',
     'CADL':'Candel Therapeutics Inc. ',
     'CAE':'CAE Inc. ',
     'CAG':'ConAgra Brands Inc. ',
     'CAH':'Cardinal Health Inc. ',
     'CAKE':'Cheesecake Factory Incorporated ',
     'CAL':'Caleres Inc. ',
     'CALB':'California BanCorp ',
     'CALC':'CalciMedica Inc. ',
     'CALM':'Cal-Maine Foods Inc. ',
     'CALT':'Calliditas Therapeutics AB ',
     'CALX':'Calix Inc ',
     'CAMP':'CalAmp Corp. ',
     'CAMT':'Camtek Ltd. ',
     'CAN':'Canaan Inc. ',
     'CANB':'Can B Corp.',
     'CANF':'Can-Fite Biopharma Ltd Sponsored ADR (Israel)',
     'CANG':'Cango Inc.   each representing two (2) ',
     'CANO':'Cano Health Inc.  ',
     'CAPR':'Capricor Therapeutics Inc. ',
     'CAR':'Avis Budget Group Inc. ',
     'CARA':'Cara Therapeutics Inc. ',
     'CARE':'Carter Bankshares Inc. ',
     'CARG':'CarGurus Inc.  ',
     'CARM':'Carisma Therapeutics Inc. ',
     'CARR':'Carrier Global Corporation ',
     'CARS':'Cars.com Inc. ',
     'CARV':'Carver Bancorp Inc. ',
     'CASA':'Casa Systems Inc. ',
     'CASH':'Pathward Financial Inc. ',
     'CASI':'CASI Pharmaceuticals Inc. ',
     'CASS':'Cass Information Systems Inc ',
     'CASY':'Caseys General Stores Inc. ',
     'CAT':'Caterpillar Inc. ',
     'CATC':'Cambridge Bancorp ',
     'CATO':'Cato Corporation  ',
     'CATX':'Perspective Therapeutics Inc. ',
     'CATY':'Cathay General Bancorp ',
     'CAVA':'CAVA Group Inc. ',
     'CB':'Chubb Limited  ',
     'CBAN':'Colony Bankcorp Inc. ',
     'CBAT':'CBAK Energy Technology Inc. ',
     'CBAY':'CymaBay Therapeutics Inc. ',
     'CBD':'Companhia Brasileira de Distribuicao American Depsitary Shares; each representing one Common Share',
     'CBFV':'CB Financial Services Inc. ',
     'CBH':'Virtus Convertible & Income 2024 Target Term Fund  of Beneficial Interest',
     'CBIO':'Catalyst Biosciences Inc. ',
     'CBL':'CBL & Associates Properties Inc. ',
     'CBNK':'Capital Bancorp Inc. ',
     'CBOE':'Cboe Global Markets Inc. ',
     'CBRE':'CBRE Group Inc  ',
     'CBRG':'Chain Bridge I ',
     'CBRGU':'Chain Bridge I Units',
     'CBRL':'Cracker Barrel Old Country Store Inc ',
     'CBSH':'Commerce Bancshares Inc. ',
     'CBT':'Cabot Corporation ',
     'CBU':'Community Bank System Inc. ',
     'CBUS':'Cibus Inc.  ',
     'CBZ':'CBIZ Inc. ',
     'CC':'Chemours Company ',
     'CCAI':'Cascadia Acquisition Corp.  ',
     'CCAIU':'Cascadia Acquisition Corp. Unit',
     'CCAIW':'Cascadia Acquisition Corp. ',
     'CCAP':'Crescent Capital BDC Inc. ',
     'CCB':'Coastal Financial Corporation ',
     'CCBG':'Capital City Bank Group ',
     'CCCC':'C4 Therapeutics Inc. ',
     'CCCS':'CCC Intelligent Solutions Holdings Inc. ',
     'CCD':'Calamos Dynamic Convertible & Income Fund ',
     'CCEL':'Cryo-Cell International Inc. ',
     'CCEP':'Coca-Cola Europacific Partners plc ',
     'CCF':'Chase Corporation ',
     'CCI':'Crown Castle Inc. ',
     'CCJ':'Cameco Corporation ',
     'CCK':'Crown Holdings Inc.',
     'CCL':'Carnival Corporation ',
     'CCLD':'CareCloud Inc. ',
     'CCLP':'CSI Compressco LP Common Units',
     'CCM':'Concord Medical Services Holdings Limited ADS (Each represents three )',
     'CCNE':'CNB Financial Corporation ',
     'CCO':'Clear Channel Outdoor Holdings Inc. ',
     'CCOI':'Cogent Communications Holdings Inc.',
     'CCRD':'CoreCard Corporation ',
     'CCRN':'Cross Country Healthcare Inc.  $0.0001 Par Value',
     'CCS':'Century Communities Inc. ',
     'CCSI':'Consensus Cloud Solutions Inc. ',
     'CCTS':'Cactus Acquisition Corp. 1 Limited',
     'CCTSW':'Cactus Acquisition Corp. 1 Limited ',
     'CCU':'Compania Cervecerias Unidas S.A. ',
     'CCV':'Churchill Capital Corp V  ',
     'CCVI':'Churchill Capital Corp VI  ',
     'CCZ':'Comcast Holdings ZONES',
     'CD':'Chindata Group Holdings Limited ',
     'CDAQ':'Compass Digital Acquisition Corp. ',
     'CDAQU':'Compass Digital Acquisition Corp. Unit',
     'CDAY':'Ceridian HCM Holding Inc. ',
     'CDE':'Coeur Mining Inc. ',
     'CDIO':'Cardio Diagnostics Holdings Inc. ',
     'CDIOW':'Cardio Diagnostics Holdings Inc. ',
     'CDLX':'Cardlytics Inc. ',
     'CDMO':'Avid Bioservices Inc. ',
     'CDNA':'CareDx Inc. ',
     'CDNS':'Cadence Design Systems Inc. ',
     'CDRE':'Cadre Holdings Inc. ',
     'CDRO':'Codere Online Luxembourg S.A. ',
     'CDROW':'Codere Online Luxembourg S.A. s',
     'CDTX':'Cidara Therapeutics Inc. ',
     'CDW':'CDW Corporation ',
     'CDXC':'ChromaDex Corporation ',
     'CDXS':'Codexis Inc. ',
     'CDZI':'CADIZ Inc. ',
     'CDZIP':'Cadiz Inc. Depositary Shares',
     'CE':'Celanese Corporation Celanese Corporation ',
     'CEAD':'CEA Industries Inc. ',
     'CEADW':'CEA Industries Inc. ',
     'CECO':'CECO Environmental Corp. ',
     'CEE':'The Central and Eastern Europe Fund Inc. ',
     'CEG':'Constellation Energy Corporation ',
     'CEI':'Camber Energy Inc. ',
     'CEIX':'CONSOL Energy Inc. ',
     'CELC':'Celcuity Inc. ',
     'CELH':'Celsius Holdings Inc. ',
     'CELL':'PhenomeX Inc. ',
     'CELU':'Celularity Inc.  ',
     'CELUW':'Celularity Inc. ',
     'CELZ':'Creative Medical Technology Holdings Inc. ',
     'CEM':'ClearBridge MLP and Midstream Fund Inc. ',
     'CEN':'Center Coast Brookfield MLP & Energy Infrastructure Fund',
     'CENN':'Cenntro Electric Group Limited ',
     'CENT':'Central Garden & Pet Company ',
     'CENTA':'Central Garden & Pet Company   Nonvoting',
     'CENX':'Century Aluminum Company ',
     'CEPU':'Central Puerto S.A.  (each represents ten )',
     'CEQP':'Crestwood Equity Partners LP',
     'CERE':'Cerevel Therapeutics Holdings Inc. ',
     'CERS':'Cerus Corporation ',
     'CERT':'Certara Inc. ',
     'CET':'Central Securities Corporation ',
     'CETUU':'Cetus Capital Acquisition Corp. Unit',
     'CETUW':'Cetus Capital Acquisition Corp. ',
     'CETX':'Cemtrex Inc. ',
     'CETXP':'Cemtrex Inc. Series 1 Preferred Stock',
     'CETY':'Clean Energy Technologies Inc. ',
     'CEVA':'CEVA Inc. ',
     'CF':'CF Industries Holdings Inc. ',
     'CFB':'CrossFirst Bankshares Inc. ',
     'CFBK':'CF Bankshares Inc. ',
     'CFFE':'CF Acquisition Corp. VIII  ',
     'CFFEW':'CF Acquisition Corp. VIII ',
     'CFFI':'C&F Financial Corporation ',
     'CFFN':'Capitol Federal Financial Inc. ',
     'CFFS':'CF Acquisition Corp. VII  ',
     'CFFSW':'CF Acquisition Corp. VII ',
     'CFG':'Citizens Financial Group Inc. ',
     'CFIV':'CF Acquisition Corp. IV  ',
     'CFIVW':'CF Acquisition Corp. IV ',
     'CFLT':'Confluent Inc.  ',
     'CFMS':'Conformis Inc. ',
     'CFR':'Cullen/Frost Bankers Inc. ',
     'CFRX':'ContraFect Corporation ',
     'CFSB':'CFSB Bancorp Inc. ',
     'CG':'The Carlyle Group Inc. ',
     'CGA':'China Green Agriculture Inc. ',
     'CGABL':'The Carlyle Group Inc. 4.625% Subordinated Notes due 2061',
     'CGAU':'Centerra Gold Inc. ',
     'CGBD':'Carlyle Secured Lending Inc. ',
     'CGC':'Canopy Growth Corporation ',
     'CGEM':'Cullinan Oncology Inc. ',
     'CGEN':'Compugen Ltd. ',
     'CGNT':'Cognyte Software Ltd. ',
     'CGNX':'Cognex Corporation ',
     'CGO':'Calamos Global Total Return Fund ',
     'CGRN':'Capstone Green Energy Corporation ',
     'CGTX':'Cognition Therapeutics Inc. ',
     'CHAA':'Catcha Investment Corp. ',
     'CHCI':'Comstock Holding Companies Inc.  ',
     'CHCO':'City Holding Company ',
     'CHCT':'Community Healthcare Trust Incorporated ',
     'CHD':'Church & Dwight Company Inc. ',
     'CHDN':'Churchill Downs Incorporated ',
     'CHE':'Chemed Corp',
     'CHEA':'Chenghe Acquisition Co.',
     'CHEAU':'Chenghe Acquisition Co. Unit',
     'CHEAW':'Chenghe Acquisition Co. ',
     'CHEF':'The Chefs Warehouse Inc. ',
     'CHEK':'Check-Cap Ltd. ',
     'CHGG':'Chegg Inc. ',
     'CHH':'Choice Hotels International Inc. ',
     'CHI':'Calamos Convertible Opportunities and Income Fund ',
     'CHK':'Chesapeake Energy Corporation ',
     'CHKEL':'Chesapeake Energy Corporation Class C s',
     'CHKP':'Check Point Software Technologies Ltd. ',
     'CHMG':'Chemung Financial Corp ',
     'CHMI':'Cherry Hill Mortgage Investment Corporation ',
     'CHN':'China Fund Inc. ',
     'CHNR':'China Natural Resources Inc. ',
     'CHPT':'ChargePoint Holdings Inc. ',
     'CHRD':'Chord Energy Corporation ',
     'CHRS':'Coherus BioSciences Inc. ',
     'CHRW':'C.H. Robinson Worldwide Inc. ',
     'CHS':'Chicos FAS Inc. ',
     'CHSCL':'CHS Inc Class B Cumulative Redeemable Preferred Stock Series 4',
     'CHSCM':'CHS Inc Class B Reset Rate Cumulative Redeemable Preferred Stock Series 3',
     'CHSCN':'CHS Inc Preferred Class B Series 2 Reset Rate',
     'CHSCO':'CHS Inc. Class B Cumulative Redeemable Preferred Stock',
     'CHSCP':'CHS Inc. 8%  Cumulative Redeemable Preferred Stock',
     'CHSN':'Chanson International Holding ',
     'CHT':'Chunghwa Telecom Co. Ltd.',
     'CHTR':'Charter Communications Inc.',
     'CHUY':'Chuys Holdings Inc. ',
     'CHW':'Calamos Global Dynamic Income Fund ',
     'CHWY':'Chewy Inc.  ',
     'CHX':'ChampionX Corporation ',
     'CHY':'Calamos Convertible and High Income Fund ',
     'CI':'The Cigna Group ',
     'CIA':'Citizens Inc.   ($1.00 Par)',
     'CIB':'BanColombia S.A. ',
     'CIEN':'Ciena Corporation ',
     'CIF':'MFS Intermediate High Income Fund ',
     'CIFR':'Cipher Mining Inc. ',
     'CIFRW':'Cipher Mining Inc. ',
     'CIG':'Comp En De Mn Cemig ADS ',
     'CIGI':'Colliers International Group Inc. Subordinate Voting Shares',
     'CII':'Blackrock Capital and Income Fund Inc.',
     'CIK':'Credit Suisse Asset Management Income Fund Inc. ',
     'CIM':'Chimera Investment Corporation ',
     'CINF':'Cincinnati Financial Corporation ',
     'CING':'Cingulate Inc. ',
     'CINGW':'Cingulate Inc. s',
     'CINT':'CI&T Inc  ',
     'CIO':'City Office REIT Inc. ',
     'CION':'CION Investment Corporation ',
     'CIR':'CIRCOR International Inc. ',
     'CISO':'CISO Global Inc. ',
     'CISS':'C3is Inc. ',
     'CITE':'Cartica Acquisition Corp ',
     'CITEW':'Cartica Acquisition Corp ',
     'CIVB':'Civista Bancshares Inc. ',
     'CIVI':'Civitas Resources Inc. ',
     'CIX':'CompX International Inc. ',
     'CIZN':'Citizens Holding Company ',
     'CJET':'Chijet Motor Company Inc. ',
     'CJJD':'China Jo-Jo Drugstores Inc. (Cayman Islands) ',
     'CKPT':'Checkpoint Therapeutics Inc. ',
     'CKX':'CKX Lands Inc. ',
     'CL':'Colgate-Palmolive Company ',
     'CLAR':'Clarus Corporation ',
     'CLAY':'Chavant Capital Acquisition Corp. ',
     'CLB':'Core Laboratories Inc. ',
     'CLBK':'Columbia Financial Inc. ',
     'CLBR':'Colombier Acquisition Corp.  ',
     'CLBT':'Cellebrite DI Ltd. ',
     'CLBTW':'Cellebrite DI Ltd. s',
     'CLCO':'Cool Company Ltd. ',
     'CLDT':'Chatham Lodging Trust (REIT)  of Beneficial Interest',
     'CLDX':'Celldex Therapeutics Inc.',
     'CLEU':'China Liberal Education Holdings Limited ',
     'CLF':'Cleveland-Cliffs Inc. ',
     'CLFD':'Clearfield Inc. ',
     'CLGN':'CollPlant Biotechnologies Ltd ',
     'CLH':'Clean Harbors Inc. ',
     'CLIN':'Clean Earth Acquisitions Corp.  ',
     'CLINR':'Clean Earth Acquisitions Corp. Right',
     'CLINW':'Clean Earth Acquisitions Corp. ',
     'CLIR':'ClearSign Technologies Corporation  (DE)',
     'CLLS':'Cellectis S.A. ',
     'CLM':'Cornerstone Strategic Value Fund Inc. ',
     'CLMB':'Climb Global Solutions Inc. ',
     'CLMT':'Calumet Specialty Products Partners L.P. Common Units',
     'CLNE':'Clean Energy Fuels Corp. ',
     'CLNN':'Clene Inc. ',
     'CLNNW':'Clene Inc. ',
     'CLOE':'Clover Leaf Capital Corp.  ',
     'CLOER':'Clover Leaf Capital Corp. Rights',
     'CLOV':'Clover Health Investments Corp.  ',
     'CLPR':'Clipper Realty Inc. ',
     'CLPS':'CLPS Incorporation ',
     'CLPT':'ClearPoint Neuro Inc. ',
     'CLRB':'Cellectar Biosciences Inc.  ',
     'CLRC':'ClimateRock ',
     'CLRO':'ClearOne Inc. (DE) ',
     'CLS':'Celestica Inc. ',
     'CLSD':'Clearside Biomedical Inc. ',
     'CLSK':'CleanSpark Inc. ',
     'CLST':'Catalyst Bancorp Inc. ',
     'CLVR':'Clever Leaves Holdings Inc. ',
     'CLVRW':'Clever Leaves Holdings Inc. ',
     'CLVT':'Clarivate Plc ',
     'CLW':'Clearwater Paper Corporation ',
     'CLWT':'Euro Tech Holdings Company Limited ',
     'CLX':'Clorox Company ',
     'CM':'Canadian Imperial Bank of Commerce ',
     'CMA':'Comerica Incorporated ',
     'CMAX':'CareMax Inc.  ',
     'CMAXW':'CareMax Inc. ',
     'CMBM':'Cambium Networks Corporation ',
     'CMC':'Commercial Metals Company ',
     'CMCA':'Capitalworks Emerging Markets Acquisition Corp ',
     'CMCL':'Caledonia Mining Corporation Plc ',
     'CMCM':'Cheetah Mobile Inc.  each representing fifty (50) ',
     'CMCO':'Columbus McKinnon Corporation ',
     'CMCSA':'Comcast Corporation  ',
     'CMCT':'Creative Media & Community Trust Corporation ',
     'CME':'CME Group Inc.  ',
     'CMG':'Chipotle Mexican Grill Inc. ',
     'CMI':'Cummins Inc. ',
     'CMLS':'Cumulus Media Inc.  ',
     'CMMB':'Chemomab Therapeutics Ltd. ',
     'CMND':'Clearmind Medicine Inc. ',
     'CMP':'Compass Minerals Intl Inc ',
     'CMPO':'CompoSecure Inc.  ',
     'CMPOW':'CompoSecure Inc. ',
     'CMPR':'Cimpress plc  (Ireland)',
     'CMPS':'COMPASS Pathways Plc American Depository Shares',
     'CMPX':'Compass Therapeutics Inc. ',
     'CMRA':'Comera Life Sciences Holdings Inc. ',
     'CMRAW':'Comera Life Sciences Holdings Inc. ',
     'CMRE':'Costamare Inc.  $0.0001 par value',
     'CMRX':'Chimerix Inc. ',
     'CMS':'CMS Energy Corporation ',
     'CMT':'Core Molding Technologies Inc ',
     'CMTG':'Claros Mortgage Trust Inc. ',
     'CMTL':'Comtech Telecommunications Corp. ',
     'CMU':'MFS Municipal Income Trust ',
     'CNA':'CNA Financial Corporation ',
     'CNC':'Centene Corporation ',
     'CNDA':'Concord Acquisition Corp II  ',
     'CNDT':'Conduent Incorporated ',
     'CNET':'ZW Data Action Technologies Inc. ',
     'CNEY':'CN Energy Group Inc. ',
     'CNF':'CNFinance Holdings Limited  each representing  twenty (20) ',
     'CNFR':'Conifer Holdings Inc. ',
     'CNGL':'Canna-Global Acquisition Corp.  ',
     'CNGLW':'Canna-Global Acquisition Corp ',
     'CNHI':'CNH Industrial N.V. ',
     'CNI':'Canadian National Railway Company ',
     'CNK':'Cinemark Holdings Inc Cinemark Holdings Inc. ',
     'CNM':'Core & Main Inc.  ',
     'CNMD':'CONMED Corporation ',
     'CNNE':'Cannae Holdings Inc. ',
     'CNO':'CNO Financial Group Inc. ',
     'CNO^A':'CNO Financial Group Inc. ',
     'CNOB':'ConnectOne Bancorp Inc. ',
     'CNP':'CenterPoint Energy Inc (Holding Co) ',
     'CNQ':'Canadian Natural Resources Limited ',
     'CNS':'Cohen & Steers Inc ',
     'CNSL':'Consolidated Communications Holdings Inc. ',
     'CNSP':'CNS Pharmaceuticals Inc. ',
     'CNTA':'Centessa Pharmaceuticals plc ',
     'CNTB':'Connect Biopharma Holdings Limited ',
     'CNTG':'Centogene N.V. ',
     'CNTX':'Context Therapeutics Inc. ',
     'CNTY':'Century Casinos Inc. ',
     'CNVS':'Cineverse Corp.  ',
     'CNX':'CNX Resources Corporation ',
     'CNXA':'Connexa Sports Technologies Inc. ',
     'CNXC':'Concentrix Corporation ',
     'CNXN':'PC Connection Inc. ',
     'COCO':'The Vita Coco Company Inc. ',
     'COCP':'Cocrystal Pharma Inc. ',
     'CODA':'Coda Octopus Group Inc. ',
     'CODI':'D/B/A Compass Diversified Holdings Shares of Beneficial Interest',
     'CODX':'Co-Diagnostics Inc. ',
     'COE':'51Talk Online Education Group  each representing 60 ',
     'COEP':'Coeptis Therapeutics Holdings Inc. ',
     'COEPW':'Coeptis Therapeutics Holdings Inc. s',
     'COF':'Capital One Financial Corporation ',
     'COFS':'ChoiceOne Financial Services Inc. ',
     'COGT':'Cogent Biosciences Inc. ',
     'COHN':'Cohen & Company Inc.',
     'COHR':'Coherent Corp. ',
     'COHU':'Cohu Inc. ',
     'COIN':'Coinbase Global Inc.  ',
     'COKE':'Coca-Cola Consolidated Inc. ',
     'COLB':'Columbia Banking System Inc. ',
     'COLD':'Americold Realty Trust Inc. ',
     'COLL':'Collegium Pharmaceutical Inc. ',
     'COLM':'Columbia Sportswear Company ',
     'COMM':'CommScope Holding Company Inc. ',
     'COMP':'Compass Inc.  ',
     'COMS':'COMSovereign Holding Corp. ',
     'COMSP':'COMSovereign Holding Corp. ',
     'COMSW':'COMSovereign Holding Corp. s',
     'CONN':'Conns Inc. ',
     'CONX':'CONX Corp.  ',
     'CONXW':'CONX Corp. ',
     'COO':'The Cooper Companies Inc. ',
     'COOK':'Traeger Inc. ',
     'COOL':'Corner Growth Acquisition Corp. ',
     'COOLU':'Corner Growth Acquisition Corp. Unit',
     'COOLW':'Corner Growth Acquisition Corp. ',
     'COOP':'Mr. Cooper Group Inc. ',
     'COP':'ConocoPhillips ',
     'CORR':'CorEnergy Infrastructure Trust Inc. ',
     'CORT':'Corcept Therapeutics Incorporated ',
     'COSM':'Cosmos Health Inc. ',
     'COST':'Costco Wholesale Corporation ',
     'COTY':'Coty Inc.  ',
     'COUR':'Coursera Inc. ',
     'COYA':'Coya Therapeutics Inc. ',
     'CP':'Canadian Pacific Kansas City Limited ',
     'CPA':'Copa Holdings S.A. Copa Holdings S.A.  ',
     'CPAA':'Conyers Park III Acquisition Corp.  ',
     'CPAAU':'Conyers Park III Acquisition Corp. Unit',
     'CPAAW':'Conyers Park III Acquisition Corp. s',
     'CPAC':'Cementos Pacasmayo S.A.A.  (Each representing five )',
     'CPB':'Campbell Soup Company ',
     'CPE':'Callon Petroleum Company ',
     'CPF':'Central Pacific Financial Corp New',
     'CPG':'Crescent Point Energy Corporation  (Canada)',
     'CPHC':'Canterbury Park Holding Corporation New ',
     'CPHI':'China Pharma Holdings Inc. ',
     'CPIX':'Cumberland Pharmaceuticals Inc. ',
     'CPK':'Chesapeake Utilities Corporation ',
     'CPLP':'Capital Product Partners L.P. Common Units',
     'CPNG':'Coupang Inc.  ',
     'CPOP':'Pop Culture Group Co. Ltd ',
     'CPRI':'Capri Holdings Limited ',
     'CPRT':'Copart Inc. (DE) ',
     'CPRX':'Catalyst Pharmaceuticals Inc. ',
     'CPS':'Cooper-Standard Holdings Inc. ',
     'CPSH':'CPS Technologies Corp. ',
     'CPSI':'Computer Programs and Systems Inc. ',
     'CPSS':'Consumer Portfolio Services Inc. ',
     'CPT':'Camden Property Trust ',
     'CPTK':'Crown PropTech Acquisitions ',
     'CPTN':'Cepton Inc. ',
     'CPTNW':'Cepton Inc. ',
     'CPUH':'Compute Health Acquisition Corp.  ',
     'CPZ':'Calamos Long/Short Equity & Dynamic Income Trust ',
     'CQP':'Cheniere Energy Partners LP Cheniere Energy Partners LP Common Units',
     'CR':'Crane Company ',
     'CRAI':'CRA International Inc. ',
     'CRBG':'Corebridge Financial Inc. ',
     'CRBP':'Corbus Pharmaceuticals Holdings Inc. ',
     'CRBU':'Caribou Biosciences Inc. ',
     'CRC':'California Resources Corporation ',
     'CRCT':'Cricut Inc.  ',
     'CRD/A':'Crawford & Company',
     'CRD/B':'Crawford & Company',
     'CRDF':'Cardiff Oncology Inc. ',
     'CRDL':'Cardiol Therapeutics Inc.  ',
     'CRDO':'Credo Technology Group Holding Ltd ',
     'CREC':'Crescera Capital Acquisition Corp ',
     'CRECU':'Crescera Capital Acquisition Corp Unit',
     'CRECW':'Crescera Capital Acquisition Corp ',
     'CREG':'Smart Powerr Corp. ',
     'CRESW':'Cresud S.A.C.I.F. y A. ',
     'CRESY':'Cresud S.A.C.I.F. y A. ',
     'CREX':'Creative Realities Inc. ',
     'CRF':'Cornerstone Total Return Fund Inc. ',
     'CRGE':'Charge Enterprises Inc. ',
     'CRGO':'Freightos Limited ',
     'CRGOW':'Freightos Limited s',
     'CRGY':'Crescent Energy Company  ',
     'CRH':'CRH PLC ',
     'CRI':'Carters Inc. ',
     'CRIS':'Curis Inc. ',
     'CRK':'Comstock Resources Inc. ',
     'CRKN':'Crown Electrokinetics Corp. ',
     'CRL':'Charles River Laboratories International Inc. ',
     'CRM':'Salesforce Inc. ',
     'CRMD':'CorMedix Inc. ',
     'CRMT':'Americas Car-Mart Inc ',
     'CRNC':'Cerence Inc. ',
     'CRNT':'Ceragon Networks Ltd. ',
     'CRNX':'Crinetics Pharmaceuticals Inc. ',
     'CRON':'Cronos Group Inc. Common Share',
     'CROX':'Crocs Inc. ',
     'CRS':'Carpenter Technology Corporation ',
     'CRSP':'CRISPR Therapeutics AG ',
     'CRSR':'Corsair Gaming Inc. ',
     'CRT':'Cross Timbers Royalty Trust ',
     'CRTO':'Criteo S.A. ',
     'CRUS':'Cirrus Logic Inc. ',
     'CRVL':'CorVel Corp. ',
     'CRVS':'Corvus Pharmaceuticals Inc. ',
     'CRWD':'CrowdStrike Holdings Inc.  ',
     'CRWS':'Crown Crafts Inc ',
     'CSAN':'Cosan S.A. ADS',
     'CSBR':'Champions Oncology Inc. ',
     'CSCO':'Cisco Systems Inc.',
     'CSGP':'CoStar Group Inc. ',
     'CSGS':'CSG Systems International Inc. ',
     'CSIQ':'Canadian Solar Inc.  (ON)',
     'CSL':'Carlisle Companies Incorporated ',
     'CSLM':'Consilium Acquisition Corp I Ltd.',
     'CSLMR':'Consilium Acquisition Corp I Ltd. Right',
     'CSLMW':'Consilium Acquisition Corp I Ltd. ',
     'CSPI':'CSP Inc. ',
     'CSQ':'Calamos Strategic Total Return ',
     'CSR':'D/B/A Centerspace ',
     'CSSE':'Chicken Soup for the Soul Entertainment Inc.  ',
     'CSTA':'Constellation Acquisition Corp I ',
     'CSTE':'Caesarstone Ltd. ',
     'CSTL':'Castle Biosciences Inc. ',
     'CSTM':'Constellium SE  (France)',
     'CSTR':'CapStar Financial Holdings Inc. ',
     'CSV':'Carriage Services Inc. ',
     'CSWC':'Capital Southwest Corporation ',
     'CSWI':'CSW Industrials Inc. ',
     'CSX':'CSX Corporation ',
     'CTAS':'Cintas Corporation ',
     'CTBB':'Qwest Corporation',
     'CTBI':'Community Trust Bancorp Inc. ',
     'CTDD':'Qwest Corporation',
     'CTG':'Computer Task Group Inc. ',
     'CTGO':'Contango ORE Inc. ',
     'CTHR':'Charles & Colvard Ltd ',
     'CTIB':'Yunhong CTI Ltd. ',
     'CTKB':'Cytek Biosciences Inc. ',
     'CTLP':'Cantaloupe Inc. ',
     'CTLT':'Catalent Inc. ',
     'CTM':'Castellum Inc. ',
     'CTMX':'CytomX Therapeutics Inc. ',
     'CTO':'CTO Realty Growth Inc. ',
     'CTOS':'Custom Truck One Source Inc. ',
     'CTR':'ClearBridge MLP and Midstream Total Return Fund Inc. ',
     'CTRA':'Coterra Energy Inc. ',
     'CTRE':'CareTrust REIT Inc. ',
     'CTRM':'Castor Maritime Inc. ',
     'CTRN':'Citi Trends Inc. ',
     'CTS':'CTS Corporation ',
     'CTSH':'Cognizant Technology Solutions Corporation  ',
     'CTSO':'Cytosorbents Corporation ',
     'CTV':'Innovid Corp. ',
     'CTVA':'Corteva Inc. ',
     'CTXR':'Citius Pharmaceuticals Inc. ',
     'CUBA':'Herzfeld Caribbean Basin Fund Inc. ',
     'CUBB':'Customers Bancorp Inc.',
     'CUBE':'CubeSmart ',
     'CUBI':'Customers Bancorp Inc ',
     'CUE':'Cue Biopharma Inc. ',
     'CUEN':'Cuentas Inc. ',
     'CUK':'Carnival Plc ADS ADS',
     'CULL':'Cullman Bancorp Inc. ',
     'CULP':'Culp Inc. ',
     'CURI':'CuriosityStream Inc.  ',
     'CURO':'CURO Group Holdings Corp. ',
     'CURV':'Torrid Holdings Inc. ',
     'CUTR':'Cutera Inc. ',
     'CUZ':'Cousins Properties Incorporated ',
     'CVAC':'CureVac N.V. ',
     'CVBF':'CVB Financial Corporation ',
     'CVCO':'Cavco Industries Inc.  When Issued',
     'CVCY':'Central Valley Community Bancorp ',
     'CVE':'Cenovus Energy Inc ',
     'CVEO':'Civeo Corporation (Canada) ',
     'CVGI':'Commercial Vehicle Group Inc. ',
     'CVGW':'Calavo Growers Inc. ',
     'CVI':'CVR Energy Inc. ',
     'CVII':'Churchill Capital Corp VII  ',
     'CVKD':'Cadrenal Therapeutics Inc. ',
     'CVLG':'Covenant Logistics Group Inc.  ',
     'CVLT':'Commvault Systems Inc. ',
     'CVLY':'Codorus Valley Bancorp Inc ',
     'CVM':'Cel-Sci Corporation ',
     'CVNA':'Carvana Co.  ',
     'CVR':'Chicago Rivet & Machine Co. ',
     'CVRX':'CVRx Inc. ',
     'CVS':'CVS Health Corporation ',
     'CVU':'CPI Aerostructures Inc. ',
     'CVV':'CVD Equipment Corporation ',
     'CVX':'Chevron Corporation ',
     'CW':'Curtiss-Wright Corporation ',
     'CWAN':'Clearwater Analytics Holdings Inc.  ',
     'CWBC':'Community West Bancshares ',
     'CWBR':'CohBar Inc. ',
     'CWCO':'Consolidated Water Co. Ltd. ',
     'CWD':'CaliberCos Inc.  ',
     'CWEN':'Clearway Energy Inc. Class C ',
     'CWH':'Camping World Holdings Inc.  ',
     'CWK':'Cushman & Wakefield plc ',
     'CWST':'Casella Waste Systems Inc.  ',
     'CWT':'California Water Service Group ',
     'CX':'Cemex S.A.B. de C.V. Sponsored ADR',
     'CXAC':'C5 Acquisition Corporation  ',
     'CXAI':'CXApp Inc.  ',
     'CXAIW':'CXApp Inc. ',
     'CXDO':'Crexendo Inc. ',
     'CXE':'MFS High Income Municipal Trust ',
     'CXH':'MFS Investment Grade Municipal Trust ',
     'CXM':'Sprinklr Inc.  ',
     'CXT':'Crane NXT Co. ',
     'CXW':'CoreCivic Inc. ',
     'CYAN':'Cyanotech Corporation ',
     'CYBN':'Cybin Inc. ',
     'CYBR':'CyberArk Software Ltd. ',
     'CYCC':'Cyclacel Pharmaceuticals Inc. ',
     'CYCCP':'Cyclacel Pharmaceuticals Inc.',
     'CYCN':'Cyclerion Therapeutics Inc. ',
     'CYD':'China Yuchai International Limited ',
     'CYH':'Community Health Systems Inc. ',
     'CYN':'Cyngn Inc. ',
     'CYRX':'CryoPort Inc. ',
     'CYT':'Cyteir Therapeutics Inc. ',
     'CYTH':'Cyclo Therapeutics Inc. ',
     'CYTHW':'Cyclo Therapeutics Inc. ',
     'CYTK':'Cytokinetics Incorporated ',
     'CYTO':'Altamira Therapeutics Ltd. 0.2  (Bermuda)',
     'CZFS':'Citizens Financial Services Inc. ',
     'CZNC':'Citizens & Northern Corp ',
     'CZOO':'Cazoo Group Ltd ',
     'CZR':'Caesars Entertainment Inc. ',
     'CZWI':'Citizens Community Bancorp Inc. ',
     'D':'Dominion Energy Inc. ',
     'DAC':'Danaos Corporation ',
     'DADA':'Dada Nexus Limited ',
     'DAIO':'Data I/O Corporation ',
     'DAKT':'Daktronics Inc. ',
     'DAL':'Delta Air Lines Inc. ',
     'DALN':'DallasNews Corporation Series A ',
     'DALS':'DA32 Life Science Tech Acquisition Corp.  ',
     'DAN':'Dana Incorporated ',
     'DAO':'Youdao Inc.  each representing one',
     'DAR':'Darling Ingredients Inc. ',
     'DARE':'Dare Bioscience Inc. ',
     'DASH':'DoorDash Inc.  ',
     'DATS':'DatChat Inc. ',
     'DATSW':'DatChat Inc. Series A ',
     'DAVA':'Endava plc  (each representing one)',
     'DAVE':'Dave Inc.  ',
     'DAVEW':'Dave Inc. s',
     'DAWN':'Day One Biopharmaceuticals Inc. ',
     'DB':'Deutsche Bank AG ',
     'DBGI':'Digital Brands Group Inc. ',
     'DBGIW':'Digital Brands Group Inc. ',
     'DBI':'Designer Brands Inc.  ',
     'DBL':'DoubleLine Opportunistic Credit Fund  of Beneficial Interest',
     'DBRG':'DigitalBridge Group Inc.',
     'DBTX':'Decibel Therapeutics Inc. ',
     'DBVT':'DBV Technologies S.A. ',
     'DBX':'Dropbox Inc.  ',
     'DC':'Dakota Gold Corp. ',
     'DCBO':'Docebo Inc. ',
     'DCF':'BNY Mellon Alcentra Global Credit Income 2024 Target Term Fund Inc. ',
     'DCFC':'Tritium DCFC Limited ',
     'DCFCW':'Tritium DCFC Limited ',
     'DCGO':'DocGo Inc. ',
     'DCI':'Donaldson Company Inc. ',
     'DCO':'Ducommun Incorporated ',
     'DCOM':'Dime Community Bancshares Inc. ',
     'DCOMP':'Dime Community Bancshares Inc. Fixed-Rate Non-Cumulative Perpetual Preferred Stock Series A',
     'DCPH':'Deciphera Pharmaceuticals Inc. ',
     'DCTH':'Delcath Systems Inc. ',
     'DD':'DuPont de Nemours Inc. ',
     'DDD':'3D Systems Corporation ',
     'DDI':'DoubleDown Interactive Co. Ltd. American Depository Shares',
     'DDL':'Dingdong (Cayman) Limited  (each two representing three )',
     'DDOG':'Datadog Inc.  ',
     'DDS':'Dillards Inc. ',
     'DDT':'Dillards Capital Trust I',
     'DE':'Deere & Company ',
     'DEA':'Easterly Government Properties Inc. ',
     'DECA':'Denali Capital Acquisition Corp. ',
     'DECK':'Deckers Outdoor Corporation ',
     'DEI':'Douglas Emmett Inc. ',
     'DELL':'Dell Technologies Inc. Class C ',
     'DEN':'Denbury Inc. ',
     'DENN':'Dennys Corporation ',
     'DEO':'Diageo plc ',
     'DERM':'Journey Medical Corporation ',
     'DESP':'Despegar.com Corp. ',
     'DFFN':'Diffusion Pharmaceuticals Inc. ',
     'DFH':'Dream Finders Homes Inc.  ',
     'DFIN':'Donnelley Financial Solutions Inc. ',
     'DFLI':'Dragonfly Energy Holdings Corp.  (NV)',
     'DFLIW':'Dragonfly Energy Holdings Corp. ',
     'DFP':'Flaherty & Crumrine Dynamic Preferred and Income Fund Inc. ',
     'DFS':'Discover Financial Services ',
     'DG':'Dollar General Corporation ',
     'DGHI':'Digihost Technology Inc. Common Subordinate Voting Shares',
     'DGICA':'Donegal Group Inc.  ',
     'DGICB':'Donegal Group Inc. Class B ',
     'DGII':'Digi International Inc. ',
     'DGLY':'Digital Ally Inc. ',
     'DRWKF':'Drägerwerk AG & Co.KGaA',
     'DGX':'Quest Diagnostics Incorporated ',
     'DH':'Definitive Healthcare Corp.  ',
     'DHAC':'Digital Health Acquisition Corp. ',
     'DHACW':'Digital Health Acquisition Corp. ',
     'DHC':'Diversified Healthcare Trust  of Beneficial Interest',
     'DHCA':'DHC Acquisition Corp.',
     'DHCAW':'DHC Acquisition Corp. ',
     'DHF':'BNY Mellon High Yield Strategies Fund ',
     'DHI':'D.R. Horton Inc. ',
     'DHIL':'Diamond Hill Investment Group Inc.  ',
     #'DPSTF':'Deutsche Post AG ',
     'DHR':'Danaher Corporation ',
     'DHT':'DHT Holdings Inc.',
     'DHX':'DHI Group Inc. ',
     'DHY':'Credit Suisse High Yield Bond Fund ',
     'DIAX':'Nuveen Dow 30SM Dynamic Overwrite Fund  of Beneficial Interest',
     'DIBS':'1stdibs.com Inc. ',
     'DICE':'DICE Therapeutics Inc. ',
     'DIN':'Dine Brands Global Inc. ',
     'DINO':'HF Sinclair Corporation ',
     'DIOD':'Diodes Incorporated ',
     'DIS':'Walt Disney Company ',
     'DISA':'Disruptive Acquisition Corporation I ',
     'DISAW':'Disruptive Acquisition Corporation I ',
     'DISH':'DISH Network Corporation  ',
     'DIST':'Distoken Acquisition Corporation ',
     'DISTR':'Distoken Acquisition Corporation Right',
     'DISTW':'Distoken Acquisition Corporation ',
     'DIT':'AMCON Distributing Company ',
     'DJCO':'Daily Journal Corp. (S.C.) ',
     'DK':'Delek US Holdings Inc. ',
     'DKDCA':'Data Knights Acquisition Corp.  ',
     'DKDCW':'Data Knights Acquisition Corp. ',
     'DKILF':'Daikin Industries,Ltd ',
     'DKL':'Delek Logistics Partners L.P. Common Units representing Limited Partner Interests',
     'DKNG':'DraftKings Inc.  ',
     'DKS':'Dicks Sporting Goods Inc ',
     'DLA':'Delta Apparel Inc. ',
     'DLB':'Dolby Laboratories ',
     'DLHC':'DLH Holdings Corp.',
     'DLNG':'Dynagas LNG Partners LP Common Units',
     'DLO':'DLocal Limited  ',
     'DLPN':'Dolphin Entertainment Inc. ',
     'DLR':'Digital Realty Trust Inc. ',
     'DLTH':'Duluth Holdings Inc. Class B ',
     'DLTR':'Dollar Tree Inc. ',
     'DLX':'Deluxe Corporation ',
     'DLY':'DoubleLine Yield Opportunities Fund  of Beneficial Interest',
     'DM':'Desktop Metal Inc.  ',
     'DMA':'Destra Multi-Alternative Fund ',
     'DMAC':'DiaMedica Therapeutics Inc. ',
     'DMAQ':'Deep Medicine Acquisition Corp.  ',
     'DMAQR':'Deep Medicine Acquisition Corp. Rights',
     'DMB':'BNY Mellon Municipal Bond Infrastructure Fund Inc. ',
     'DMF':'BNY Mellon Municipal Income Inc. ',
     'DMLP':'Dorchester Minerals L.P. Common Units Representing Limited Partnership Interests',
     'DMO':'Western Asset Mortgage Opportunity Fund Inc. ',
     'DMRC':'Digimarc Corporation ',
     'DMS':'Digital Media Solutions Inc. ',
     'DMTK':'DermTech Inc. ',
     'DNA':'Ginkgo Bioworks Holdings Inc.  ',
     'DNB':'Dun & Bradstreet Holdings Inc. ',
     'DNLI':'Denali Therapeutics Inc. ',
     'DNMR':'Danimer Scientific Inc. ',
     'DNN':'Denison Mines Corp  (Canada)',
     'DNOW':'NOW Inc. ',
     'DNP':'DNP Select Income Fund Inc. ',
     'DNUT':'Krispy Kreme Inc. ',
     'DO':'Diamond Offshore Drilling Inc. ',
     'DOC':'Physicians Realty Trust  of Beneficial Interest',
     'DOCN':'DigitalOcean Holdings Inc. ',
     'DOCS':'Doximity Inc.  ',
     'DOCU':'DocuSign Inc. ',
     'DOGZ':'Dogness (International) Corporation  ',
     'DOLE':'Dole plc ',
     'DOMA':'Doma Holdings Inc. ',
     'DOMH':'Dominari Holdings Inc. ',
     'DOMO':'Domo Inc. Class B ',
     'DOOO':'BRP Inc. (Recreational Products) Common Subordinate Voting Shares',
     'DOOR':'Masonite International Corporation  (Canada)',
     'DORM':'Dorman Products Inc. ',
     'DOUG':'Douglas Elliman Inc. ',
     'DOV':'Dover Corporation ',
     'DOW':'Dow Inc. ',
     'DOX':'Amdocs Limited ',
     'DOYU':'DouYu International Holdings Limited ADS',
     'DPCS':'DP Cap Acquisition Corp I ',
     'DPG':'Duff & Phelps Utility and Infrastructure Fund Inc.',
     'DPRO':'Draganfly Inc. ',
     'DPSI':'DecisionPoint Systems Inc. ',
     'DPZ':'Dominos Pizza Inc ',
     'DQ':'DAQO New Energy Corp.  each representing five ',
     'DRCT':'Direct Digital Holdings Inc.  ',
     'DRD':'DRDGOLD Limited ',
     'DRH':'Diamondrock Hospitality Company ',
     'DRI':'Darden Restaurants Inc. ',
     'DRIO':'DarioHealth Corp. ',
     'DRMA':'Dermata Therapeutics Inc. ',
     'DRMAW':'Dermata Therapeutics Inc. ',
     'DRQ':'Dril-Quip Inc. ',
     'DRRX':'DURECT Corporation ',
     'DRS':'Leonardo DRS Inc. ',
     'DRTS':'Alpha Tau Medical Ltd. ',
     'DRTSW':'Alpha Tau Medical Ltd. ',
     'DRTT':'DIRTT Environmental Solutions Ltd. ',
     'DRUG':'Bright Minds Biosciences Inc. ',
     'DRVN':'Driven Brands Holdings Inc. ',
     'DSGN':'Design Therapeutics Inc. ',
     'DSGR':'Distribution Solutions Group Inc. ',
     'DSGX':'Descartes Systems Group Inc. ',
     'DSKE':'Daseke Inc. ',
     'DSL':'DoubleLine Income Solutions Fund  of Beneficial Interests',
     'DSM':'BNY Mellon Strategic Municipal Bond Fund Inc. ',
     'DSP':'Viant Technology Inc.  ',
     'DSS':'DSS Inc. ',
     'DSU':'Blackrock Debt Strategies Fund Inc. ',
     'DSWL':'Deswell Industries Inc. ',
     'DSX':'Diana Shipping inc. ',
     'DT':'Dynatrace Inc. ',
     'DTB':'DTE Energy Company ',
     'DTC':'Solo Brands Inc.  ',
     'DTE':'DTE Energy Company ',
     'DTF':'DTF Tax-Free Income 2028 Term Fund Inc. ',
     'DTG':'DTE Energy Company ',
     'DTI':'Drilling Tools International Corporation ',
     'DTIL':'Precision BioSciences Inc. ',
     'DTM':'DT Midstream Inc. ',
     'DTOC':'Digital Transformation Opportunities Corp.  ',
     'DTOCW':'Digital Transformation Opportunities Corp. ',
     'DTSS':'Datasea Inc. ',
     'DTST':'Data Storage Corporation ',
     'DTSTW':'Data Storage Corporation ',
     'DTW':'DTE Energy Company ',
     'DUET':'DUET Acquisition Corp.  ',
     'DUETW':'DUET Acquisition Corp. ',
     'DUK':'Duke Energy Corporation (Holding Company) ',
     'DUNE':'Dune Acquisition Corporation  ',
     'DUNEU':'Dune Acquisition Corporation Unit',
     'DUNEW':'Dune Acquisition Corporation ',
     'DUO':'Fangdd Network Group Ltd. ',
     'DUOL':'Duolingo Inc.  ',
     'DUOT':'Duos Technologies Group Inc. ',
     'DV':'DoubleVerify Holdings Inc. ',
     'DVA':'DaVita Inc. ',
     'DVAX':'Dynavax Technologies Corporation ',
     'DVN':'Devon Energy Corporation ',
     'DWAC':'Digital World Acquisition Corp.  ',
     'DWACU':'Digital World Acquisition Corp. Units',
     'DWACW':'Digital World Acquisition Corp. s',
     'DWSN':'Dawson Geophysical Company ',
     'DX':'Dynex Capital Inc. ',
     'DXC':'DXC Technology Company ',
     'DXCM':'DexCom Inc. ',
     'DXF':'Dunxin Financial Holdings Limited ',
     'DXLG':'Destination XL Group Inc. ',
     'DXPE':'DXP Enterprises Inc. ',
     'DXR':'Daxor Corporation ',
     'DXYN':'Dixie Group Inc. ',
     'DY':'Dycom Industries Inc. ',
     'DYAI':'Dyadic International Inc. ',
     'DYN':'Dyne Therapeutics Inc. ',
     'DYNT':'Dynatronics Corporation ',
     'DZSI':'DZS Inc. ',
     'E':'ENI S.p.A. ',
     'EA':'Electronic Arts Inc. ',
     'EAC':'Edify Acquisition Corp.  ',
     'EACPW':'Edify Acquisition Corp. ',
     'EAD':'Allspring Income Opportunities Fund ',
     'EAF':'GrafTech International Ltd. ',
     'EAR':'Eargo Inc. ',
     'EARN':'Ellington Residential Mortgage REIT  of Beneficial Interest',
     'EAST':'Eastside Distilling Inc. ',
     'EAT':'Brinker International Inc. ',
     'EB':'Eventbrite Inc.  ',
     'EBAY':'eBay Inc. ',
     'EBC':'Eastern Bankshares Inc. ',
     'EBET':'EBET INC. ',
     'EBF':'Ennis Inc. ',
     'EBIX':'Ebix Inc. ',
     'EBMT':'Eagle Bancorp Montana Inc. ',
     'EBON':'Ebang International Holdings Inc. ',
     'EBR':'Centrais Electricas Brasileiras S A  (Each representing one Common Share)',
     'EBS':'Emergent Biosolutions Inc. ',
     'EBTC':'Enterprise Bancorp Inc ',
     'EC':'Ecopetrol S.A. ',
     'ECAT':'BlackRock ESG Capital Allocation Term Trust  of Beneficial Interest',
     'ECBK':'ECB Bancorp Inc. ',
     'ECC':'Eagle Point Credit Company Inc. ',
     'ECCC':'Eagle Point Credit Company Inc. ',
     'ECCV':'Eagle Point Credit Company Inc. ',
     'ECCW':'Eagle Point Credit Company Inc.',
     'ECCX':'Eagle Point Credit Company Inc. ',
     'ECF':'Ellsworth Growth and Income Fund Ltd.',
     'ECL':'Ecolab Inc. ',
     'ECOR':'electroCore Inc. ',
     'ECPG':'Encore Capital Group Inc ',
     'ECVT':'Ecovyst Inc. ',
     'ECX':'ECARX Holdings Inc. ',
     'ECXWW':'ECARX Holdings Inc. s',
     'ED':'Consolidated Edison Inc. ',
     'EDAP':'EDAP TMS S.A. ',
     'EDBL':'Edible Garden AG Incorporated ',
     'EDBLW':'Edible Garden AG Incorporated ',
     'EDF':'Virtus Stone Harbor Emerging Markets Income Fund  of Beneficial Interest',
     'EDI':'Virtus Stone Harbor Emerging Markets Total Income Fund  of Beneficial Interest',
     'EDIT':'Editas Medicine Inc. ',
     'EDN':'Empresa Distribuidora Y Comercializadora Norte S.A. (Edenor) ',
     'EDR':'Endeavor Group Holdings Inc.  ',
     'EDRY':'EuroDry Ltd. ',
     'EDSA':'Edesa Biotech Inc. ',
     'EDTK':'Skillful Craftsman Education Technology Limited ',
     'EDTX':'EdtechX Holdings Acquisition Corp. II  ',
     'EDTXU':'EdtechX Holdings Acquisition Corp. II Unit',
     'EDTXW':'EdtechX Holdings Acquisition Corp. II ',
     'EDU':'New Oriental Education & Technology Group Inc.',
     'EDUC':'Educational Development Corporation ',
     'EE':'Excelerate Energy Inc.  ',
     'EEA':'The European Equity Fund Inc. ',
     'EEFT':'Euronet Worldwide Inc. ',
     'EEIQ':'EpicQuest Education Group International Limited ',
     'EEX':'Emerald Holding Inc. ',
     'EFC':'Ellington Financial Inc. ',
     'EFHT':'EF Hutton Acquisition Corporation I ',
     'EFHTR':'EF Hutton Acquisition Corporation I Rights',
     'EFOI':'Energy Focus Inc. ',
     'EFR':'Eaton Vance Senior Floating-Rate Fund  of Beneficial Interest',
     'EFSC':'Enterprise Financial Services Corporation ',
     'EFSCP':'Enterprise Financial Services Corp.',
     'EFSH':'1847 Holdings LLC ',
     'EFT':'Eaton Vance Floating Rate Income Trust  of Beneficial Interest',
     'EFTR':'eFFECTOR Therapeutics Inc. ',
     'EFTRW':'eFFECTOR Therapeutics Inc. ',
     'EFX':'Equifax Inc. ',
     'EFXT':'Enerflex Ltd ',
     'EGAN':'eGain Corporation ',
     'EGBN':'Eagle Bancorp Inc. ',
     'EGF':'Blackrock Enhanced Government Fund Inc. ',
     'EGGF':'EG Acquisition Corp.  ',
     'EGHT':'8x8 Inc ',
     'EGIO':'Edgio Inc. ',
     'EGLE':'Eagle Bulk Shipping Inc. ',
     'EGLX':'Enthusiast Gaming Holdings Inc. ',
     'EGO':'Eldorado Gold Corporation ',
     'EGP':'EastGroup Properties Inc. ',
     'EGRX':'Eagle Pharmaceuticals Inc. ',
     'EGY':'VAALCO Energy Inc.  ',
     'EH':'EHang Holdings Limited ADS',
     'EHAB':'Enhabit Inc. ',
     'EHC':'Encompass Health Corporation ',
     'EHI':'Western Asset Global High Income Fund Inc ',
     'EHTH':'eHealth Inc. ',
     'EIC':'Eagle Point Income Company Inc. ',
     'EICA':'Eagle Point Income Company Inc.',
     'EIG':'Employers Holdings Inc ',
     'EIGR':'Eiger BioPharmaceuticals Inc. ',
     'EIM':'Eaton Vance Municipal Bond Fund  of Beneficial Interest $.01 par value',
     'EIX':'Edison International ',
     'EJH':'E-Home Household Service Holdings Limited ',
     'EKSO':'Ekso Bionics Holdings Inc. ',
     'EL':'Estee Lauder Companies Inc. ',
     'ELA':'Envela Corporation ',
     'ELAN':'Elanco Animal Health Incorporated ',
     'ELBM':'Electra Battery Materials Corporation ',
     'ELC':'Entergy Louisiana Inc. ',
     'ELDN':'Eledon Pharmaceuticals Inc. ',
     'ELEV':'Elevation Oncology Inc. ',
     'ELF':'e.l.f. Beauty Inc. ',
     'ELLO':'Ellomay Capital Ltd  (Israel)',
     'ELMD':'Electromed Inc. ',
     'ELME':'Elme Communities ',
     'ELOX':'Eloxx Pharmaceuticals Inc. ',
     'ELP':'Companhia Paranaense de Energia (COPEL)  (each representing one Unit consisting one Common Share and four non-voting Class B Preferred Shares)',
     'ELS':'Equity Lifestyle Properties Inc. ',
     'ELSE':'Electro-Sensors Inc. ',
     'ELTK':'Eltek Ltd. ',
     'ELTX':'Elicio Therapeutics Inc. ',
     'ELV':'Elevance Health Inc. ',
     'ELVA':'Electrovaya Inc. ',
     'ELVN':'Enliven Therapeutics Inc. ',
     'ELYM':'Eliem Therapeutics Inc ',
     'ELYS':'Elys Game Technology Corp. ',
     'EM':'Smart Share Global Limited ',
     'EMAN':'eMagin Corporation ',
     'EMBC':'Embecta Corp. ',
     'EMBK':'Embark Technology Inc. ',
     'EMBKW':'Embark Technology Inc. s',
     'EMCG':'Embrace Change Acquisition Corp ',
     'EMCGR':'Embrace Change Acquisition Corp Rights',
     'EMCGU':'Embrace Change Acquisition Corp Unit',
     'EMCGW':'Embrace Change Acquisition Corp s',
     'EMD':'Western Asset Emerging Markets Debt Fund Inc ',
     'EME':'EMCOR Group Inc. ',
     'EMF':'Templeton Emerging Markets Fund ',
     'EMKR':'EMCORE Corporation ',
     'EML':'Eastern Company ',
     'EMLD':'FTAC Emerald Acquisition Corp.  ',
     'EMLDU':'FTAC Emerald Acquisition Corp. Unit',
     'EMLDW':'FTAC Emerald Acquisition Corp. ',
     'EMN':'Eastman Chemical Company ',
     'EMO':'ClearBridge Energy Midstream Opportunity Fund Inc. ',
     'EMR':'Emerson Electric Company ',
     'EMX':'EMX Royalty Corporation  (Canada)',
     'ENB':'Enbridge Inc ',
     'ENCP':'Energem Corp ',
     'ENCPU':'Energem Corp Unit',
     'ENER':'Accretion Acquisition Corp. ',
     'ENERR':'Accretion Acquisition Corp. Right',
     'ENERW':'Accretion Acquisition Corp. ',
     'ENFN':'Enfusion Inc.  ',
     'ENG':'ENGlobal Corporation ',
     'ENIC':'Enel Chile S.A.  (Each representing 50 shares of )',
     'ENLC':'EnLink Midstream LLC Common Units representing Limited Partner Interests',
     'ENLT':'Enlight Renewable Energy Ltd. ',
     'ENLV':'Enlivex Therapeutics Ltd. ',
     'ENOB':'Enochian Biosciences Inc. ',
     'ENOV':'Enovis Corporation ',
     'ENPH':'Enphase Energy Inc. ',
     'ENR':'Energizer Holdings Inc. ',
     'ENS':'EnerSys ',
     'ENSC':'Ensysce Biosciences Inc. ',
     'ENSG':'The Ensign Group Inc. ',
     'ENSV':'Enservco Corporation ',
     'ENTA':'Enanta Pharmaceuticals Inc. ',
     'ENTG':'Entegris Inc. ',
     'ENTX':'Entera Bio Ltd. ',
     'ENV':'Envestnet Inc ',
     'ENVA':'Enova International Inc. ',
     'ENVB':'Enveric Biosciences Inc. ',
     'ENVX':'Enovix Corporation ',
     'ENX':'Eaton Vance New York Municipal Bond Fund  of Beneficial Interest $.01 par value',
     'ENZ':'Enzo Biochem Inc.  ($0.01 Par Value)',
     'EOD':'Allspring Global Dividend Opportunity Fund  of Beneficial Interest',
     'EOG':'EOG Resources Inc. ',
     'EOI':'Eaton Vance Enhance Equity Income Fund Eaton Vance Enhanced Equity Income Fund Shares of Beneficial Interest',
     'EOLS':'Evolus Inc. ',
     'EOS':'Eaton Vance Enhance Equity Income Fund II ',
     'EOSE':'Eos Energy Enterprises Inc.  ',
     'EOSEW':'Eos Energy Enterprises Inc. ',
     'EOT':'Eaton Vance Municipal Income Trust EATON VANCE NATIONAL MUNICIPAL OPPORTUNITIES TRUST',
     'EP':'Empire Petroleum Corporation ',
     'EPAC':'Enerpac Tool Group Corp. ',
     'EPAM':'EPAM Systems Inc. ',
     'EPC':'Edgewell Personal Care Company ',
     'EPD':'Enterprise Products Partners L.P. ',
     'EPIX':'ESSA Pharma Inc. ',
     'EPM':'Evolution Petroleum Corporation Inc. ',
     'EPOW':'Sunrise New Energy Co. Ltd ',
     'EPR':'EPR Properties ',
     'EPRT':'Essential Properties Realty Trust Inc. ',
     'EPSN':'Epsilon Energy Ltd. Common Share',
     'EQ':'Equillium Inc. ',
     'EQBK':'Equity Bancshares Inc.  ',
     'EQC':'Equity Commonwealth  of Beneficial Interest',
     'EQH':'Equitable Holdings Inc. ',
     'EQIX':'Equinix Inc.  REIT',
     'EQNR':'Equinor ASA',
     'EQR':'Equity Residential  of Beneficial Interest',
     'EQRX':'EQRx Inc.  ',
     'EQRXW':'EQRx Inc. ',
     'EQS':'Equus Total Return Inc. ',
     'EQT':'EQT Corporation ',
     'EQX':'Equinox Gold Corp. ',
     'ERAS':'Erasca Inc. ',
     'ERC':'Allspring Multi-Sector Income Fund ',
     'ERF':'Enerplus Corporation ',
     'ERH':'Allspring Utilities and High Income Fund ',
     'ERIC':'Ericsson ',
     'ERIE':'Erie Indemnity Company  ',
     'ERII':'Energy Recovery Inc. ',
     'ERJ':'Embraer S.A. ',
     'ERNA':'Eterna Therapeutics Inc. ',
     'ERO':'Ero Copper Corp. ',
     'ES':'Eversource Energy (D/B/A) ',
     'ESAB':'ESAB Corporation ',
     'ESAC':'ESGEN Acquisition Corporation ',
     'ESACW':'ESGEN Acquisition Corporation s',
     'ESCA':'Escalade Incorporated ',
     'ESE':'ESCO Technologies Inc. ',
     'ESEA':'Euroseas Ltd.  (Marshall Islands)',
     'ESGR':'Enstar Group Limited ',
     'ESHAU':'ESH Acquisition Corp. Unit',
     'ESI':'Element Solutions Inc. ',
     'ESLT':'Elbit Systems Ltd. ',
     'ESMT':'EngageSmart Inc. ',
     'ESNT':'Essent Group Ltd. ',
     'ESOA':'Energy Services of America Corporation ',
     'ESP':'Espey Mfg. & Electronics Corp. ',
     'ESPR':'Esperion Therapeutics Inc. ',
     'ESQ':'Esquire Financial Holdings Inc. ',
     'ESRT':'Empire State Realty Trust Inc.  ',
     'ESS':'Essex Property Trust Inc. ',
     'ESSA':'ESSA Bancorp Inc. ',
     'ESTA':'Establishment Labs Holdings Inc. ',
     'ESTC':'Elastic N.V. ',
     'ESTE':'Earthstone Energy Inc.  ',
     'ET':'Energy Transfer LP Common Units',
     'ETAO':'Etao International Co. Ltd. ',
     'ETD':'Ethan Allen Interiors Inc. ',
     'ETN':'Eaton Corporation PLC ',
     'ETNB':'89bio Inc. ',
     'ETON':'Eton Pharmaceuticals Inc. ',
     'ETR':'Entergy Corporation ',
     'ETRN':'Equitrans Midstream Corporation ',
     'ETSY':'Etsy Inc. ',
     'ETWO':'E2open Parent Holdings Inc. ',
     'EU':'enCore Energy Corp. ',
     'EUDA':'EUDA Health Holdings Limited ',
     'EUDAW':'EUDA Health Holdings Limited ',
     'EURN':'Euronav NV ',
     'EVA':'Enviva Inc. ',
     'EVAX':'Evaxion Biotech A/S ',
     'EVBG':'Everbridge Inc. ',
     'EVBN':'Evans Bancorp Inc. ',
     'EVC':'Entravision Communications Corporation ',
     'EVCM':'EverCommerce Inc. ',
     'EVE':'EVe Mobility Acquisition Corp ',
     'EVER':'EverQuote Inc.  ',
     'EVEX':'Eve Holding Inc. ',
     'EVF':'Eaton Vance Senior Income Trust ',
     'EVGN':'Evogene Ltd ',
     'EVGO':'EVgo Inc.  ',
     'EVGOW':'EVgo Inc. s',
     'EVGR':'Evergreen Corporation',
     'EVGRU':'Evergreen Corporation Unit',
     'EVGRW':'Evergreen Corporation ',
     'EVH':'Evolent Health Inc  ',
     'EVI':'EVI Industries Inc.  ',
     'EVLO':'Evelo Biosciences Inc. ',
     'EVLV':'Evolv Technologies Holdings Inc.  ',
     'EVLVW':'Evolv Technologies Holdings Inc. ',
     'EVM':'Eaton Vance California Municipal Bond Fund  of Beneficial Interest $.01 par value',
     'EVN':'Eaton Vance Municipal Income Trust ',
     'EVO':'Evotec SE ',
     'EVOK':'Evoke Pharma Inc. ',
     'EVR':'Evercore Inc.  ',
     'EVRG':'Evergy Inc. ',
     'EVRI':'Everi Holdings Inc. ',
     'EVT':'Eaton Vance Tax Advantaged Dividend Income Fund  of Beneficial Interest',
     'EVTC':'Evertec Inc. ',
     'EVTL':'Vertical Aerospace Ltd. ',
     'EVTV':'Envirotech Vehicles Inc. ',
     'EVV':'Eaton Vance Limited Duration Income Fund  of Beneficial Interest',
     'EW':'Edwards Lifesciences Corporation ',
     'EWBC':'East West Bancorp Inc. ',
     'EWCZ':'European Wax Center Inc.  ',
     'EWTX':'Edgewise Therapeutics Inc. ',
     'EXAI':'Exscientia Plc ',
     'EXAS':'Exact Sciences Corporation ',
     'EXC':'Exelon Corporation ',
     'EXEL':'Exelixis Inc. ',
     'EXFY':'Expensify Inc.  ',
     'EXK':'Endeavour Silver Corporation  (Canada)',
     'EXLS':'ExlService Holdings Inc. ',
     'EXP':'Eagle Materials Inc ',
     'EXPD':'Expeditors International of Washington Inc. ',
     'EXPE':'Expedia Group Inc. ',
     'EXPI':'eXp World Holdings Inc. ',
     'EXPO':'Exponent Inc. ',
     'EXPR':'Express Inc. ',
     'EXR':'Extra Space Storage Inc ',
     'EXTR':'Extreme Networks Inc. ',
     'EYE':'National Vision Holdings Inc. ',
     'EYEN':'Eyenovia Inc. ',
     'EYPT':'EyePoint Pharmaceuticals Inc. ',
     'EZFL':'EzFill Holdings Inc. ',
     'EZGO':'EZGO Technologies Ltd. ',
     'EZPW':'EZCORP Inc.  Non Voting ',
     'F':'Ford Motor Company ',
     'FA':'First Advantage Corporation ',
     'FACT':'Freedom Acquisition I Corp. ',
     'FAF':'First American Corporation  ',
     'FAM':'First Trust/abrdn Global Opportunity Income Fund  of Beneficial Interest',
     'FAMI':'Farmmi Inc. ',
     'FANG':'Diamondback Energy Inc. ',
     'FANH':'Fanhua Inc. ',
     'FARM':'Farmer Brothers Company ',
     'FARO':'FARO Technologies Inc. ',
     'FAST':'Fastenal Company ',
     'FAT':'FAT Brands Inc.  ',
     'FATBB':'FAT Brands Inc. Class B ',
     'FATBW':'FAT Brands Inc. ',
     'FATE':'Fate Therapeutics Inc. ',
     'FATH':'Fathom Digital Manufacturing Corporation  ',
     'FATP':'Fat Projects Acquisition Corp',
     'FATPU':'Fat Projects Acquisition Corp Unit',
     'FAX':'abrdn Asia-Pacific Income Fund Inc. ',
     'FAZE':'FaZe Holdings Inc. ',
     'FAZEW':'FaZe Holdings Inc. ',
     'FBIN':'Fortune Brands Innovations Inc. ',
     'FBIO':'Fortress Biotech Inc. ',
     'FBIZ':'First Business Financial Services Inc. ',
     'FBK':'FB Financial Corporation ',
     'FBMS':'First Bancshares Inc.',
     'FBNC':'First Bancorp ',
     'FBP':'First BanCorp. New ',
     'FBRT':'Franklin BSP Realty Trust Inc. ',
     'FBRX':'Forte Biosciences Inc. ',
     'FC':'Franklin Covey Company ',
     'FCAP':'First Capital Inc. ',
     'FCBC':'First Community Bankshares Inc. (VA) ',
     'FCCO':'First Community Corporation ',
     'FCEL':'FuelCell Energy Inc. ',
     'FCF':'First Commonwealth Financial Corporation ',
     'FCFS':'FirstCash Holdings Inc. ',
     'FCN':'FTI Consulting Inc. ',
     'FCNCA':'First Citizens BancShares Inc.  ',
     'FCNCP':'First Citizens BancShares Inc. Depositary Shares',
     'FCO':'abrdn Global Income Fund Inc. ',
     'FCPT':'Four Corners Property Trust Inc. ',
     'FCRX':'Crescent Capital BDC Inc. ',
     'FCT':'First Trust Senior Floating Rate Income Fund II  of Beneficial Interest',
     'FCUV':'Focus Universal Inc. ',
     'FCX':'Freeport-McMoRan Inc. ',
     'FDBC':'Fidelity D & D Bancorp Inc. ',
     'FDEU':'First Trust Dynamic Europe Equity Income Fund  of Beneficial Interest',
     'FDMT':'4D Molecular Therapeutics Inc. ',
     'FDP':'Fresh Del Monte Produce Inc. ',
     'FDS':'FactSet Research Systems Inc. ',
     'FDUS':'Fidus Investment Corporation ',
     'FDX':'FedEx Corporation ',
     'FE':'FirstEnergy Corp. ',
     'FEAM':'5E Advanced Materials Inc. ',
     'FEDU':'Four Seasons Education (Cayman) Inc.  each ADS representing 10 ',
     'FEI':'First Trust MLP and Energy Income Fund  of Beneficial Interest',
     'FEIM':'Frequency Electronics Inc. ',
     'FELE':'Franklin Electric Co. Inc. ',
     'FEMY':'Femasys Inc. ',
     'FEN':'First Trust Energy Income and Growth Fund',
     'FENC':'Fennec Pharmaceuticals Inc. ',
     'FENG':'Phoenix New Media Limited  each representing 48 .',
     'FERG':'Ferguson plc ',
     'FET':'Forum Energy Technologies Inc. ',
     'FEXD':'Fintech Ecosystem Development Corp.  ',
     'FEXDR':'Fintech Ecosystem Development Corp. Right',
     'FEXDW':'Fintech Ecosystem Development Corp. ',
     'FF':'FutureFuel Corp.  ',
     'FFA':'First Trust Enhanced Equity Income Fund',
     'FFBC':'First Financial Bancorp. ',
     'FFC':'Flaherty & Crumrine Preferred and Income Securities Fund Incorporated',
     'FFIC':'Flushing Financial Corporation ',
     'FFIE':'Faraday Future Intelligent Electric Inc. ',
     'FFIEW':'Faraday Future Intelligent Electric Inc. ',
     'FFIN':'First Financial Bankshares Inc. ',
     'FFIV':'F5 Inc. ',
     'FFNW':'First Financial Northwest Inc. ',
     'FFWM':'First Foundation Inc. ',
     'FG':'F&G Annuities & Life Inc. ',
     'FGB':'First Trust Specialty Finance and Financial Opportunities Fund',
     'FGBI':'First Guaranty Bancshares Inc. ',
     'FGBIP':'First Guaranty Bancshares Inc.',
     'FGEN':'FibroGen Inc ',
     'FGF':'FG Financial Group Inc.  (NV)',
     'FGFPP':'FG Financial Group Inc. ',
     'FGH':'FG Group Holdings Inc. ',
     'FGI':'FGI Industries Ltd. ',
     'FGIWW':'FGI Industries Ltd. ',
     'FGMC':'FG Merger Corp. ',
     'FGMCU':'FG Merger Corp. Unit',
     'FGMCW':'FG Merger Corp. ',
     'FHB':'First Hawaiian Inc. ',
     'FHI':'Federated Hermes Inc. ',
     'FHLTU':'Future Health ESG Corp. Unit',
     'FHN':'First Horizon Corporation ',
     'FHTX':'Foghorn Therapeutics Inc. ',
     'FI':'Fiserv Inc. ',
     'FIAC':'Focus Impact Acquisition Corp.  ',
     'FIBK':'First Interstate BancSystem Inc.  (DE)',
     'FICO':'Fair Isaac Corproation ',
     'FICV':'Frontier Investment Corp ',
     'FICVW':'Frontier Investment Corp s',
     'FIF':'First Trust Energy Infrastructure Fund  of Beneficial Interest',
     'FIGS':'FIGS Inc.  ',
     'FIHL':'Fidelis Insurance Holdings Limited ',
     'FINS':'Angel Oak Financial Strategies Income Term Trust  of Beneficial Interest',
     'FINV':'FinVolution Group ',
     'FINW':'FinWise Bancorp ',
     'FIP':'FTAI Infrastructure Inc. ',
     'FIS':'Fidelity National Information Services Inc. ',
     'FISI':'Financial Institutions Inc. ',
     'FITB':'Fifth Third Bancorp ',
     'FITBI':'Fifth Third Bancorp Depositary Shares',
     'FIVE':'Five Below Inc. ',
     'FIVN':'Five9 Inc. ',
     'FIX':'Comfort Systems USA Inc. ',
     'FIXX':'Homology Medicines Inc. ',
     'FIZZ':'National Beverage Corp. ',
     'FKWL':'Franklin Wireless Corp. ',
     'FL':'Foot Locker Inc.',
     'FLAG':'First Light Acquisition Group Inc.  ',
     'FLC':'Flaherty & Crumrine Total Return Fund Inc ',
     'FLEX':'Flex Ltd. ',
     'FLFV':'Feutune Light Acquisition Corporation  ',
     'FLFVR':'Feutune Light Acquisition Corporation Right',
     'FLGC':'Flora Growth Corp. ',
     'FLGT':'Fulgent Genetics Inc. ',
     'FLIC':'First of Long Island Corporation ',
     'FLJ':'FLJ Group Limited ',
     'FLL':'Full House Resorts Inc. ',
     'FLME':'Flame Acquisition Corp.  ',
     'FLNC':'Fluence Energy Inc.  ',
     'FLNG':'FLEX LNG Ltd. ',
     'FLNT':'Fluent Inc. ',
     'FLO':'Flowers Foods Inc. ',
     'FLR':'Fluor Corporation ',
     'FLS':'Flowserve Corporation ',
     'FLT':'FleetCor Technologies Inc. ',
     'FLUX':'Flux Power Holdings Inc. ',
     'FLWS':'1-800-FLOWERS.COM Inc. ',
     'FLXS':'Flexsteel Industries Inc. ',
     'FLYW':'Flywire Corporation Voting ',
     'FMAO':'Farmers & Merchants Bancorp Inc. ',
     'FMBH':'First Mid Bancshares Inc. ',
     'FMC':'FMC Corporation ',
     'FMIV':'Forum Merger IV Corporation  ',
     'FMIVU':'Forum Merger IV Corporation Unit',
     'FMIVW':'Forum Merger IV Corporation ',
     'FMN':'Federated Hermes Premier Municipal Income Fund',
     'FMNB':'Farmers National Banc Corp. ',
     'FMS':'Fresenius Medical Care AG ',
     'FMX':'Fomento Economico Mexicano S.A.B. de C.V. ',
     'FMY':'First Trust Motgage Income Fund  of Beneficial Interest',
     'FN':'Fabrinet ',
     'FNA':'Paragon 28 Inc. ',
     'FNB':'F.N.B. Corporation ',
     'FNCB':'FNCB Bancorp Inc. ',
     'FNCH':'Finch Therapeutics Group Inc. ',
     'FND':'Floor & Decor Holdings Inc. ',
     'FNF':'Fidelity National Financial Inc. ',
     'FNGR':'FingerMotion Inc. ',
     'FNKO':'Funko Inc.  ',
     'FNLC':'First Bancorp Inc  (ME) ',
     'FNV':'Franco-Nevada Corporation',
     'FNVT':'Finnovate Acquisition Corp. ',
     'FNVTU':'Finnovate Acquisition Corp. Units',
     'FNVTW':'Finnovate Acquisition Corp. s',
     'FNWB':'First Northwest Bancorp ',
     'FNWD':'Finward Bancorp ',
     'FOA':'Finance of America Companies Inc.  ',
     'FOCS':'Focus Financial Partners Inc.  ',
     'FOF':'Cohen & Steers Closed-End Opportunity Fund Inc. ',
     'FOLD':'Amicus Therapeutics Inc. ',
     'FONR':'Fonar Corporation ',
     'FOR':'Forestar Group Inc ',
     'FORA':'Forian Inc. ',
     'FORD':'Forward Industries Inc. ',
     'FORG':'ForgeRock Inc.  ',
     'FORL':'Four Leaf Acquisition Corporation  ',
     'FORLU':'Four Leaf Acquisition Corporation Unit',
     'FORLW':'Four Leaf Acquisition Corporation s',
     'FORM':'FormFactor Inc. FormFactor Inc. ',
     'FORR':'Forrester Research Inc. ',
     'FORTY':'Formula Systems (1985) Ltd. ',
     'FOSL':'Fossil Group Inc. ',
     'FOUR':'Shift4 Payments Inc.  ',
     'FOX':'Fox Corporation Class B ',
     'FOXA':'Fox Corporation  ',
     'FOXF':'Fox Factory Holding Corp. ',
     'FOXO':'FOXO Technologies Inc.  ',
     'FPAY':'FlexShopper Inc. ',
     'FPF':'First Trust Intermediate Duration Preferred & Income Fund  of Beneficial Interest',
     'FPH':'Five Point Holdings LLC  ',
     'FPI':'Farmland Partners Inc. ',
     'FPL':'First Trust New Opportunities MLP & Energy Fund  of Beneficial Interest',
     'FR':'First Industrial Realty Trust Inc. ',
     'FRA':'Blackrock Floating Rate Income Strategies Fund Inc  ',
     'FRAF':'Franklin Financial Services Corporation ',
     'FRBA':'First Bank ',
     'FRBK':'Republic First Bancorp Inc. ',
     'FRBN':'Forbion European Acquisition Corp. ',
     'FRBNW':'Forbion European Acquisition Corp. s',
     'FRD':'Friedman Industries Inc. ',
     'FREE':'Whole Earth Brands Inc.  ',
     'FREEW':'Whole Earth Brands Inc. ',
     'FREQ':'Frequency Therapeutics Inc. ',
     'FRES':'Fresh2 Group Limited ',
     'FREY':'FREYR Battery ',
     'FRG':'Franchise Group Inc. ',
     'FRGE':'Forge Global Holdings Inc. ',
     'FRGI':'Fiesta Restaurant Group Inc. ',
     'FRGT':'Freight Technologies Inc. ',
     'FRHC':'Freedom Holding Corp. ',
     'FRLA':'Fortune Rise Acquisition Corporation  ',
     'FRLAW':'Fortune Rise Acquisition Corporation ',
     'FRLN':'Freeline Therapeutics Holdings plc ',
     'FRME':'First Merchants Corporation ',
     'FRMEP':'First Merchants Corporation Depository Shares',
     'FRO':'Frontline Plc ',
     'FROG':'JFrog Ltd. ',
     'FRPH':'FRP Holdings Inc. ',
     'FRPT':'Freshpet Inc. ',
     'FRSH':'Freshworks Inc.  ',
     'FRST':'Primis Financial Corp. ',
     'FRSX':'Foresight Autonomous Holdings Ltd. ',
     'FRT':'Federal Realty Investment Trust ',
     'FRTX':'Fresh Tracks Therapeutics Inc. ',
     'FRXB':'Forest Road Acquisition Corp. II  ',
     'FRZA':'Forza X1 Inc. ',
     'FSBC':'Five Star Bancorp ',
     'FSBW':'FS Bancorp Inc. ',
     'FSCO':'FS Credit Opportunities Corp. ',
     'FSD':'First Trust High Income Long Short Fund  of Beneficial Interest',
     'FSEA':'First Seacoast Bancorp Inc. ',
     'FSFG':'First Savings Financial Group Inc. ',
     'FSI':'Flexible Solutions International Inc.  (CDA)',
     'FSK':'FS KKR Capital Corp. ',
     'FSLR':'First Solar Inc. ',
     'FSLY':'Fastly Inc.  ',
     'FSM':'Fortuna Silver Mines Inc  (Canada)',
     'FSNB':'Fusion Acquisition Corp. II  ',
     'FSP':'Franklin Street Properties Corp. ',
     'FSR':'Fisker Inc.  ',
     'FSRX':'FinServ Acquisition Corp. II  ',
     'FSRXU':'FinServ Acquisition Corp. II Unit',
     'FSRXW':'FinServ Acquisition Corp. II ',
     'FSS':'Federal Signal Corporation ',
     'FSTR':'L.B. Foster Company ',
     'FSV':'FirstService Corporation ',
     'FT':'Franklin Universal Trust ',
     'FTAI':'FTAI Aviation Ltd. ',
     'FTCH':'Farfetch Limited ',
     'FTCI':'FTC Solar Inc. ',
     'FTDR':'Frontdoor Inc. ',
     'FTEK':'Fuel Tech Inc. ',
     'FTF':'Franklin Limited Duration Income Trust  of Beneficial Interest',
     'FTFT':'Future FinTech Group Inc. ',
     'FTHM':'Fathom Holdings Inc. ',
     'FTHY':'First Trust High Yield Opportunities 2027 Term Fund ',
     'FTI':'TechnipFMC plc ',
     'FTII':'FutureTech II Acquisition Corp.  ',
     'FTIIU':'FutureTech II Acquisition Corp. Unit',
     'FTIIW':'FutureTech II Acquisition Corp. ',
     'FTK':'Flotek Industries Inc. ',
     'FTNT':'Fortinet Inc. ',
     'FTRE':'Fortrea Holdings Inc. ',
     'FTS':'Fortis Inc. ',
     'FTV':'Fortive Corporation ',
     'FUBO':'fuboTV Inc. ',
     'FUL':'H. B. Fuller Company ',
     'FULC':'Fulcrum Therapeutics Inc. ',
     'FULT':'Fulton Financial Corporation ',
     'FUN':'Cedar Fair L.P. ',
     'FUNC':'First United Corporation ',
     'FUND':'Sprott Focus Trust Inc. ',
     'FURY':'Fury Gold Mines Limited ',
     'FUSB':'First US Bancshares Inc. ',
     'FUSN':'Fusion Pharmaceuticals Inc. ',
     'FUTU':'Futu Holdings Limited ',
     'FUV':'Arcimoto Inc. ',
     'FVCB':'FVCBankcorp Inc. ',
     'FVRR':'Fiverr International Ltd.  no par value',
     'FWAC':'Fifth Wall Acquisition Corp. III ',
     'FWBI':'First Wave BioPharma Inc. ',
     'FWONA':'Liberty Media Corporation Series A Liberty Formula One ',
     'FWONK':'Liberty Media Corporation Series C Liberty Formula One ',
     'FWRD':'Forward Air Corporation ',
     'FWRG':'First Watch Restaurant Group Inc. ',
     'FXLV':'F45 Training Holdings Inc. ',
     'FXNC':'First National Corporation ',
     'FYBR':'Frontier Communications Parent Inc. ',
     'FZT':'FAST Acquisition Corp. II  ',
     'G':'Genpact Limited ',
     'GAB':'Gabelli Equity Trust Inc. ',
     'GABC':'German American Bancorp Inc. ',
     'GAIA':'Gaia Inc.  ',
     'GAIN':'Gladstone Investment Corporation Business Development Company',
     'GALT':'Galectin Therapeutics Inc. ',
     'GAM':'General American Investors Inc. ',
     'GAM^B':'General American Investors Company Inc. Cumulative Preferred Stock',
     'GAMB':'Gambling.com Group Limited ',
     'GAMC':'Golden Arrow Merger Corp.  ',
     'GAMCW':'Golden Arrow Merger Corp. ',
     'GAME':'GameSquare Holdings Inc. ',
     'GAN':'GAN Limited ',
     'GANX':'Gain Therapeutics Inc. ',
     'GAQ':'Generation Asia I Acquisition Limited ',
     'GASS':'StealthGas Inc. ',
     'GATE':'Marblegate Acquisition Corp.  ',
     'GATEU':'Marblegate Acquisition Corp. Unit',
     'GATEW':'Marblegate Acquisition Corp. ',
     'GATO':'Gatos Silver Inc. ',
     'GATX':'GATX Corporation ',
     'GAU':'Galiano Gold Inc.',
     'GB':'Global Blue Group Holding AG ',
     'GBAB':'Guggenheim Taxable Municipal Bond & Investment Grade Debt Trust  of Beneficial Interest',
     'GBBK':'Global Blockchain Acquisition Corp. ',
     'GBCI':'Glacier Bancorp Inc. ',
     'GBDC':'Golub Capital BDC Inc. ',
     'GBIO':'Generation Bio Co. ',
     'GBLI':'Global Indemnity Group LLC   (DE)',
     'GBNH':'Greenbrook TMS Inc. ',
     'GBNY':'Generations Bancorp NY Inc. ',
     'GBR':'New Concept Energy Inc ',
     'GBTG':'Global Business Travel Group Inc.  ',
     'GBX':'Greenbrier Companies Inc. ',
     'GCBC':'Greene County Bancorp Inc. ',
     'GCI':'Gannett Co. Inc. ',
     'GCMG':'GCM Grosvenor Inc.  ',
     'GCMGW':'GCM Grosvenor Inc. ',
     'GCO':'Genesco Inc. ',
     'GCT':'GigaCloud Technology Inc ',
     'GCTK':'GlucoTrack Inc. ',
     'GCV':'Gabelli Convertible and Income Securities Fund Inc. ',
     'GD':'General Dynamics Corporation ',
     'GDC':'GD Culture Group Limited ',
     'GDDY':'GoDaddy Inc.  ',
     'GDEN':'Golden Entertainment Inc. ',
     'GDEV':'GDEV Inc. ',
     'GDEVW':'GDEV Inc. ',
     'GDHG':'Golden Heaven Group Holdings Ltd. ',
     'GDL':'GDL Fund The  of Beneficial Interest',
     'GDNR':'Gardiner Healthcare Acquisitions Corp. ',
     'GDNRW':'Gardiner Healthcare Acquisitions Corp. ',
     'GDO':'Western Asset Global Corporate Defined Opportunity Fund Inc. Western Asset Global Corporate Defined Opportunity Fund Inc.',
     'GDOT':'Green Dot Corporation   $0.001 par value',
     'GDRX':'GoodRx Holdings Inc.  ',
     'GDS':'GDS Holdings Limited ADS',
     'GDST':'Goldenstone Acquisition Limited ',
     'GDSTR':'Goldenstone Acquisition Limited Rights',
     'GDSTU':'Goldenstone Acquisition Limited Units',
     'GDSTW':'Goldenstone Acquisition Limited s',
     'GDTC':'CytoMed Therapeutics Limited ',
     'GDV':'Gabelli Dividend & Income Trust  of Beneficial Interest',
     'GDYN':'Grid Dynamics Holdings Inc.  ',
     'GE':'General Electric Company ',
     'GECC':'Great Elm Capital Corp. ',
     'GEF':'Greif Inc.  ',
     'GEG':'Great Elm Group Inc. ',
     'GEHC':'GE HealthCare Technologies Inc. ',
     'GEHI':'Gravitas Education Holdings Inc.  each representing twenty ',
     'GEL':'Genesis Energy L.P. Common Units',
     'GEN':'Gen Digital Inc. ',
     'GENC':'Gencor Industries Inc. ',
     'GENE':'Genetic Technologies Ltd ADS',
     'GENI':'Genius Sports Limited ',
     'GENK':'GEN Restaurant Group Inc.  ',
     'GENQ':'Genesis Unicorn Capital Corp.  ',
     'GENQU':'Genesis Unicorn Capital Corp. Unit',
     'GENQW':'Genesis Unicorn Capital Corp. s',
     'GEO':'Geo Group Inc REIT',
     'GEOS':'Geospace Technologies Corporation  (Texas)',
     'GERN':'Geron Corporation ',
     'GES':'Guess? Inc. ',
     'GETR':'Getaround Inc. ',
     'GETY':'Getty Images Holdings Inc.  ',
     'GEV':'GE Vernova Inc.  ',
     'GEVO':'Gevo Inc. ',
     'GF':'New Germany Fund Inc. ',
     'GFAI':'Guardforce AI Co. Limited ',
     'GFAIW':'Guardforce AI Co. Limited ',
     'GFF':'Griffon Corporation ',
     'GFGD':'The Growth for Good Acquisition Corporation ',
     'GFGDU':'The Growth for Good Acquisition Corporation Unit',
     'GFI':'Gold Fields Limited ',
     'GFL':'GFL Environmental Inc. Subordinate voting shares no par value',
     'GFOR':'Graf Acquisition Corp. IV ',
     'GFS':'GlobalFoundries Inc. ',
     'GFX':'Golden Falcon Acquisition Corp.  ',
     'GGAA':'Genesis Growth Tech Acquisition Corp. ',
     'GGAAU':'Genesis Growth Tech Acquisition Corp. Unit',
     'GGAAW':'Genesis Growth Tech Acquisition Corp. ',
     'GGAL':'Grupo Financiero Galicia S.A. ',
     'GGB':'Gerdau S.A. ',
     'GGE':'Green Giant Inc. ',
     'GGG':'Graco Inc. ',
     'GGN':'GAMCO Global Gold Natural Resources & Income Trust',
     'GGR':'Gogoro Inc. ',
     'GGROW':'Gogoro Inc. ',
     'GGT':'Gabelli Multi-Media Trust Inc. ',
     'GGZ':'Gabelli Global Small and Mid Cap Value Trust  of Beneficial Interest',
     'GH':'Guardant Health Inc. ',
     'GHC':'Graham Holdings Company ',
     'GHG':'GreenTree Hospitality Group Ltd.  each representing one',
     'GHI':'Greystone Housing Impact Investors LP Beneficial Unit Certificates representing assignments of limited partnership interests',
     'GHIX':'Gores Holdings IX Inc.  ',
     'GHL':'Greenhill & Co. Inc. ',
     'GHLD':'Guild Holdings Company  ',
     'GHM':'Graham Corporation ',
     'GHRS':'GH Research PLC ',
     'GHSI':'Guardion Health Sciences Inc. ',
     'GHY':'PGIM Global High Yield Fund Inc.',
     'GIA':'GigCapital 5 Inc. ',
     'GIB':'CGI Inc. ',
     'GIC':'Global Industrial Company ',
     'GIFI':'Gulf Island Fabrication Inc. ',
     'GIGM':'GigaMedia Limited ',
     'GIII':'G-III Apparel Group LTD. ',
     'GIL':'Gildan Activewear Inc.  Sub. Vot. ',
     'GILD':'Gilead Sciences Inc. ',
     'GILT':'Gilat Satellite Networks Ltd. ',
     'GIM':'Templeton Global Income Fund Inc. ',
     'GIPR':'Generation Income Properties Inc. ',
     'GIPRW':'Generation Income Properties Inc ',
     'GIS':'General Mills Inc. ',
     'GKOS':'Glaukos Corporation ',
     'GL':'Globe Life Inc. ',
     'GLAD':'Gladstone Capital Corporation ',
     'GLBE':'Global-E Online Ltd. ',
     'GLBS':'Globus Maritime Limited ',
     'GLBZ':'Glen Burnie Bancorp ',
     'GLDD':'Great Lakes Dredge & Dock Corporation ',
     'GLDG':'GoldMining Inc. ',
     'GLCNF':'GLENCORE PLC. ',
     'GLG':'TD Holdings Inc. ',
     'GLLI':'Globalink Investment Inc. ',
     'GLLIR':'Globalink Investment Inc. Rights',
     'GLLIW':'Globalink Investment Inc. s',
     'GLMD':'Galmed Pharmaceuticals Ltd. ',
     'GLNG':'Golar Lng Ltd',
     'GLO':'Clough Global Opportunities Fund ',
     'GLOB':'Globant S.A. ',
     'GLOP':'GasLog Partners LP Common Units representing limited partnership interests',
     'GLP':'Global Partners LP Global Partners LP Common Units representing Limited Partner Interests',
     'GLPG':'Galapagos NV ',
     'GLPI':'Gaming and Leisure Properties Inc. ',
     'GLQ':'Clough Global Equity Fund Clough Global Equity Fund  of Beneficial Interest',
     'GLRE':'Greenlight Capital Re Ltd. ',
     'GLSI':'Greenwich LifeSciences Inc. ',
     'GLST':'Global Star Acquisition Inc.  ',
     'GLSTU':'Global Star Acquisition Inc. Unit',
     'GLT':'Glatfelter Corporation ',
     'GLTA':'Galata Acquisition Corp. ',
     'GLTO':'Galecto Inc. ',
     'GLU':'Gabelli Global Utility  of Beneficial Ownership',
     'GLUE':'Monte Rosa Therapeutics Inc. ',
     'GLV':'Clough Global Dividend and Income Fund  of beneficial interest',
     'GLW':'Corning Incorporated ',
     'GLYC':'GlycoMimetics Inc. ',
     'GM':'General Motors Company ',
     'GMAB':'Genmab A/S ADS',
     'GMBL':'Esports Entertainment Group Inc. ',
     'GMBLW':'Esports Entertainment Group Inc. ',
     'GMBLZ':'Esports Entertainment Group Inc. ',
     'GMDA':'Gamida Cell Ltd. ',
     'GME':'GameStop Corporation ',
     'GMED':'Globus Medical Inc.  ',
     'GMFI':'Aetherium Acquisition Corp.  ',
     'GMFIW':'Aetherium Acquisition Corp. ',
     'GMGI':'Golden Matrix Group Inc. ',
     'GMRE':'Global Medical REIT Inc. ',
     'GMS':'GMS Inc. ',
     'GMVD':'G Medical Innovations Holdings Ltd. ',
     'GMVDW':'G Medical Innovations Holdings Ltd. s',
     'GNE':'Genie Energy Ltd. Class B  Stock',
     'GNFT':'GENFIT S.A. ',
     'GNK':'Genco Shipping & Trading Limited  New (Marshall Islands)',
     'GNL':'Global Net Lease Inc. ',
     'GNLN':'Greenlane Holdings Inc.  ',
     'GNLX':'Genelux Corporation ',
     'GNPX':'Genprex Inc. ',
     'GNRC':'Generac Holdlings Inc. ',
     'GNS':'Genius Group Limited ',
     'GNSS':'Genasys Inc. ',
     'GNT':'GAMCO Natural Resources Gold & Income Trust',
     'GNTA':'Genenta Science S.p.A. ',
     'GNTX':'Gentex Corporation ',
     'GNTY':'Guaranty Bancshares Inc. ',
     'GNW':'Genworth Financial Inc ',
     'GO':'Grocery Outlet Holding Corp. ',
     'GOCO':'GoHealth Inc.  ',
     'GODN':'Golden Star Acquisition Corporation ',
     'GODNR':'Golden Star Acquisition Corporation Rights',
     'GOEV':'Canoo Inc.  ',
     'GOEVW':'Canoo Inc. ',
     'GOF':'Guggenheim Strategic Opportunities Fund  of Beneficial Interest',
     'GOGL':'Golden Ocean Group Limited ',
     'GOGO':'Gogo Inc. ',
     'GOL':'Gol Linhas Aereas Inteligentes S.A. Sponsored ADR representing 2 Pfd Shares',
     'GOLD':'Barrick Gold Corporation  (BC)',
     'GOLF':'Acushnet Holdings Corp. ',
     'GOOD':'Gladstone Commercial Corporation Real Estate Investment Trust',
     'GOOG':'Alphabet Inc. Class C ',
     'GOOGL':'Alphabet Inc.  ',
     'GOOS':'Canada Goose Holdings Inc. Subordinate Voting Shares',
     'GORO':'Gold Resource Corporation ',
     'GOSS':'Gossamer Bio Inc. ',
     'GOTU':'Gaotu Techedu Inc. ',
     'GOVX':'GeoVax Labs Inc. ',
     'GOVXW':'GeoVax Labs Inc. s',
     'GP':'GreenPower Motor Company Inc. ',
     'GPAC':'Global Partner Acquisition Corp II',
     'GPACW':'Global Partner Acquisition Corp II ',
     'GPC':'Genuine Parts Company ',
     'GPCR':'Structure Therapeutics Inc. ',
     'GPI':'Group 1 Automotive Inc. ',
     'GPK':'Graphic Packaging Holding Company',
     'GPMT':'Granite Point Mortgage Trust Inc. ',
     'GPN':'Global Payments Inc. ',
     'GPOR':'Gulfport Energy Corporation ',
     'GPP':'Green Plains Partners LP Common Units',
     'GPRE':'Green Plains Inc. ',
     'GPRK':'Geopark Ltd ',
     'GPRO':'GoPro Inc.  ',
     'GPS':'Gap Inc. ',
     'GRAB':'Grab Holdings Limited ',
     'GRABW':'Grab Holdings Limited ',
     'GRBK':'Green Brick Partners Inc. ',
     'GRC':'Gorman-Rupp Company ',
     'GRCL':'Gracell Biotechnologies Inc. ',
     'GREE':'Greenidge Generation Holdings Inc.  ',
     'GRF':'Eagle Capital Growth Fund Inc. ',
     'GRFS':'Grifols S.A. ',
     'GRFX':'Graphex Group Limited  each  representing 20 ',
     'GRI':'GRI Bio Inc. ',
     'GRIL':'Muscle Maker Inc ',
     'GRIN':'Grindrod Shipping Holdings Ltd. ',
     'GRMN':'Garmin Ltd.  (Switzerland)',
     'GRNA':'GreenLight Biosciences Holdings PBC ',
     'GRNAW':'GreenLight Biosciences Holdings PBC ',
     'GRND':'Grindr Inc. ',
     'GRNQ':'Greenpro Capital Corp. ',
     'GRNT':'Granite Ridge Resources Inc. ',
     'GROM':'Grom Social Enterprises Inc. ',
     'GROMW':'Grom Social Enterprises Inc. s',
     'GROV':'Grove Collaborative Holdings Inc.  ',
     'GROW':'U.S. Global Investors Inc.  ',
     'GROY':'Gold Royalty Corp. ',
     'GRPH':'Graphite Bio Inc. ',
     'GRPN':'Groupon Inc. ',
     'GRRR':'Gorilla Technology Group Inc. ',
     'GRRRW':'Gorilla Technology Group Inc. ',
     'GRTS':'Gritstone bio Inc. ',
     'GRTX':'Galera Therapeutics Inc. ',
     'GRVY':'GRAVITY Co. Ltd. American Depository Shares',
     'GRWG':'GrowGeneration Corp. ',
     'GRX':'The Gabelli Healthcare & Wellness Trust  of Beneficial Interest',
     'GS':'Goldman Sachs Group Inc. ',
     'GSAT':'Globalstar Inc. ',
     'GSBC':'Great Southern Bancorp Inc. ',
     'GSBD':'Goldman Sachs BDC Inc. ',
     'GSD':'Global Systems Dynamics Inc.  ',
     'GSDWW':'Global Systems Dynamics Inc. ',
     'GSHD':'Goosehead Insurance Inc.  ',
     'GSIT':'GSI Technology ',
     'GSK':'GSK plc  (Each representing two )',
     'GSL':'Global Ship Lease Inc New  ',
     'GSM':'Ferroglobe PLC ',
     'GSMG':'Glory Star New Media Group Holdings Limited ',
     'GSMGW':'Glory Star New Media Group Holdings Limited  expiring 2/13/2025',
     'GSUN':'Golden Sun Education Group Limited ',
     'GT':'The Goodyear Tire & Rubber Company ',
     'GTAC':'Global Technology Acquisition Corp. I ',
     'GTACU':'Global Technology Acquisition Corp. I Unit',
     'GTACW':'Global Technology Acquisition Corp. I ',
     'GTBP':'GT Biopharma Inc. ',
     'GTE':'Gran Tierra Energy Inc. ',
     'GTEC':'Greenland Technologies Holding Corporation ',
     'GTES':'Gates Industrial Corporation plc ',
     'GTH':'Genetron Holdings Limited ADS',
     'GTHX':'G1 Therapeutics Inc. ',
     'GTIM':'Good Times Restaurants Inc. ',
     'GTLB':'GitLab Inc.  ',
     'GTLS':'Chart Industries Inc. ',
     'GTN':'Gray Television Inc. ',
     'GTX':'Garrett Motion Inc. ',
     'GTY':'Getty Realty Corporation ',
     'GUG':'Guggenheim Active Allocation Fund  of Beneficial Interest',
     'GURE':'Gulf Resources Inc. (NV) ',
     'GUT':'Gabelli Utility Trust ',
     'GVA':'Granite Construction Incorporated ',
     'GVP':'GSE Systems Inc. ',
     'GWAV':'Greenwave Technology Solutions Inc. ',
     'GWH':'ESS Tech Inc. ',
     'GWRE':'Guidewire Software Inc. ',
     'GWRS':'Global Water Resources Inc. ',
     'GWW':'W.W. Grainger Inc. ',
     'GXO':'GXO Logistics Inc. ',
     'GYRO':'Gyrodyne LLC ',
     'H':'Hyatt Hotels Corporation  ',
     'HA':'Hawaiian Holdings Inc. ',
     'HAE':'Haemonetics Corporation ',
     'HAFC':'Hanmi Financial Corporation ',
     'HAIN':'Hain Celestial Group Inc. ',
     'HAL':'Halliburton Company ',
     'HALL':'Hallmark Financial Services Inc. ',
     'HALO':'Halozyme Therapeutics Inc. ',
     'HARP':'Harpoon Therapeutics Inc. ',
     'HAS':'Hasbro Inc. ',
     'HASI':'Hannon Armstrong Sustainable Infrastructure Capital Inc. ',
     'HAYN':'Haynes International Inc. ',
     'HAYW':'Hayward Holdings Inc. ',
     'HBAN':'Huntington Bancshares Incorporated ',
     'HBB':'Hamilton Beach Brands Holding Company  ',
     'HBCP':'Home Bancorp Inc. ',
     'HBI':'Hanesbrands Inc. ',
     'HBIO':'Harvard Bioscience Inc. ',
     'HBM':'Hudbay Minerals Inc.  (Canada)',
     'HBNC':'Horizon Bancorp Inc. ',
     'HBT':'HBT Financial Inc. ',
     'HCA':'HCA Healthcare Inc. ',
     'HCAT':'Health Catalyst Inc ',
     'HCC':'Warrior Met Coal Inc. ',
     'HCCI':'Heritage-Crystal Clean Inc. ',
     'HCDI':'Harbor Custom Development Inc. ',
     'HCDIW':'Harbor Custom Development Inc. ',
     'HCDIZ':'Harbor Custom Development Inc. ',
     'HCI':'HCI Group Inc. ',
     'HCKT':'Hackett Group Inc (The). ',
     'HCM':'HUTCHMED (China) Limited ',
     'HCMA':'HCM Acquisition Corp ',
     'HCMAW':'HCM Acquisition Corp ',
     'HCP':'HashiCorp Inc.  ',
     'HCSG':'Healthcare Services Group Inc. ',
     'HCTI':'Healthcare Triangle Inc. ',
     'HCVI':'Hennessy Capital Investment Corp. VI  ',
     'HCVIU':'Hennessy Capital Investment Corp. VI Unit',
     'HCVIW':'Hennessy Capital Investment Corp. VI ',
     'HCWB':'HCW Biologics Inc. ',
     'HCXY':'Hercules Capital Inc.',
     'HD':'Home Depot Inc. ',
     'HDB':'HDFC Bank Limited ',
     'HDSN':'Hudson Technologies Inc. ',
     'HE':'Hawaiian Electric Industries Inc. ',
     'HEAR':'Turtle Beach Corporation ',
     'HEES':'H&E Equipment Services Inc. ',
     'HEI':'Heico Corporation ',
     'HELE':'Helen of Troy Limited ',
     'HEP':'Holly Energy Partners L.P. ',
     'HEPA':'Hepion Pharmaceuticals Inc. ',
     'HEPS':'D-Market Electronic Services & Trading ',
     'HEQ':'John Hancock Hedged Equity & Income Fund  of Beneficial Interest',
     'HES':'Hess Corporation ',
     'HESAF':'Hermès International Société en commandite par actions',
     'HESM':'Hess Midstream LP  Share',
     'HFBL':'Home Federal Bancorp Inc. of Louisiana ',
     'HFFG':'HF Foods Group Inc. ',
     'HFRO':'Highland Opportunities and Income Fund  of Beneficial Interest',
     'HFWA':'Heritage Financial Corporation ',
     'HGBL':'Heritage Global Inc. ',
     'HGEN':'Humanigen Inc. ',
     'HGLB':'Highland Global Allocation Fund ',
     'HGTY':'Hagerty Inc.  ',
     'HGV':'Hilton Grand Vacations Inc. ',
     'HHC':'Howard Hughes Corporation ',
     'HHGC':'HHG Capital Corporation ',
     'HHGCR':'HHG Capital Corporation Rights',
     'HHGCW':'HHG Capital Corporation ',
     'HHLA':'HH&L Acquisition Co. ',
     'HHRS':'Hammerhead Energy Inc.  ',
     'HHRSW':'Hammerhead Energy Inc. ',
     'HHS':'Harte-Hanks Inc. ',
     'HI':'Hillenbrand Inc ',
     'HIBB':'Hibbett Inc. ',
     'HIE':'Miller/Howard High Income Equity Fund  of Beneficial Interest',
     'HIFS':'Hingham Institution for Savings ',
     'HIG':'Hartford Financial Services Group Inc. ',
     'HIHO':'Highway Holdings Limited ',
     'HII':'Huntington Ingalls Industries Inc. ',
     'HILS':'Hillstream BioPharma Inc. ',
     'HIMS':'Hims & Hers Health Inc.  ',
     'HIMX':'Himax Technologies Inc. ',
     'HIO':'Western Asset High Income Opportunity Fund Inc. ',
     'HIPO':'Hippo Holdings Inc. ',
     'HITI':'High Tide Inc. ',
     'HIVE':'Hive Blockchain Technologies Ltd. ',
     'HIW':'Highwoods Properties Inc. ',
     'HIX':'Western Asset High Income Fund II Inc. ',
     'HKD':'AMTD Digital Inc.  (every five of which represent two )',
     'HKIT':'Hitek Global Inc. ',
     'HL':'Hecla Mining Company ',
     'HLAGF':'Hapag-Lloyd AG ',
     'HLF':'Herbalife Ltd. ',
     'HLGN':'Heliogen Inc. ',
     'HLI':'Houlihan Lokey Inc.  ',
     'HLIO':'Helios Technologies Inc. ',
     'HLIT':'Harmonic Inc. ',
     'HLLY':'Holley Inc. ',
     'HLMN':'Hillman Solutions Corp. ',
     'HLN':'Haleon plc  (Each representing two )',
     'HLNE':'Hamilton Lane Incorporated  ',
     'HLP':'Hongli Group Inc. ',
     'HLT':'Hilton Worldwide Holdings Inc. ',
     'HLTH':'Cue Health Inc. ',
     'HLVX':'HilleVax Inc. ',
     'HLX':'Helix Energy Solutions Group Inc. ',
     'HMA':'Heartland Media Acquisition Corp.  ',
     'HMAC':'Hainan Manaslu Acquisition Corp. ',
     'HMACR':'Hainan Manaslu Acquisition Corp. Right',
     'HMACW':'Hainan Manaslu Acquisition Corp. ',
     'HMC':'Honda Motor Company Ltd. ',
     'HMN':'Horace Mann Educators Corporation ',
     'HMNF':'HMN Financial Inc. ',
     'HMPT':'Home Point Capital Inc ',
     'HMST':'HomeStreet Inc. ',
     'HMY':'Harmony Gold Mining Company Limited',
     'HNI':'HNI Corporation ',
     'HNNA':'Hennessy Advisors Inc. ',
     'HNRA':'HNR Acquisition Corp ',
     'HNRG':'Hallador Energy Company ',
     'HNST':'The Honest Company Inc. ',
     'HNVR':'Hanover Bancorp Inc. ',
     'HNW':'Pioneer Diversified High Income Fund Inc.',
     'HOFT':'Hooker Furnishings Corporation ',
     'HOFV':'Hall of Fame Resort & Entertainment Company ',
     'HOFVW':'Hall of Fame Resort &amp; Entertainment Company ',
     'HOG':'Harley-Davidson Inc. ',
     'HOLI':'Hollysys Automation Technologies Ltd.  (British Virgin Islands)',
     'HOLO':'MicroCloud Hologram Inc. ',
     'HOLX':'Hologic Inc. ',
     'HOMB':'Home BancShares Inc. ',
     'HON':'Honeywell International Inc. ',
     'HONE':'HarborOne Bancorp Inc. ',
     'HOOD':'Robinhood Markets Inc.  ',
     'HOOK':'HOOKIPA Pharma Inc. ',
     'HOPE':'Hope Bancorp Inc. ',
     'HOTH':'Hoth Therapeutics Inc. ',
     'HOUR':'Hour Loop Inc. ',
     'HOUS':'Anywhere Real Estate Inc. ',
     'HOV':'Hovnanian Enterprises Inc.  ',
     'HOVNP':'Hovnanian Enterprises Inc Dep Shr Srs A Pfd',
     'HOWL':'Werewolf Therapeutics Inc. ',
     'HP':'Helmerich & Payne Inc. ',
     'HPCO':'Hempacco Co. Inc. ',
     'HPE':'Hewlett Packard Enterprise Company ',
     'HPF':'John Hancock Pfd Income Fund II Pfd Income Fund II',
     'HPI':'John Hancock Preferred Income Fund  of Beneficial Interest',
     'HPK':'HighPeak Energy Inc. ',
     'HPKEW':'HighPeak Energy Inc. ',
     'HPLT':'Home Plate Acquisition Corporation  ',
     'HPLTW':'Home Plate Acquisition Corporation ',
     'HPP':'Hudson Pacific Properties Inc. ',
     'HPQ':'HP Inc. ',
     'HPS':'John Hancock Preferred Income Fund III Preferred Income Fund III',
     'HQH':'Tekla Healthcare Investors ',
     'HQI':'HireQuest Inc.  (DE)',
     'HQL':'TeklaLife Sciences Investors ',
     'HQY':'HealthEquity Inc. ',
     'HR':'Healthcare Realty Trust Incorporated ',
     'HRB':'H&R Block Inc. ',
     'HRI':'Herc Holdings Inc. ',
     'HRL':'Hormel Foods Corporation ',
     'HRMY':'Harmony Biosciences Holdings Inc. ',
     'HROW':'Harrow Health Inc. ',
     'HRT':'HireRight Holdings Corporation ',
     'HRTG':'Heritage Insurance Holdings Inc. ',
     'HRTX':'Heron Therapeutics Inc. ',
     'HRZN':'Horizon Technology Finance Corporation ',
     'HSAI':'Hesai Group  each ADS represents one Class B ',
     'HSBC':'HSBC Holdings plc. ',
     'HSCS':'Heart Test Laboratories Inc. ',
     'HSCSW':'Heart Test Laboratories Inc. ',
     'HSDT':'Helius Medical Technologies Inc.   (DE)',
     'HSHP':'Himalaya Shipping Ltd. ',
     'HSIC':'Henry Schein Inc. ',
     'HSII':'Heidrick & Struggles International Inc. ',
     'HSON':'Hudson Global Inc. ',
     'HSPO':'Horizon Space Acquisition I Corp. ',
     'HSPOR':'Horizon Space Acquisition I Corp. Right',
     'HSPOU':'Horizon Space Acquisition I Corp. Unit',
     'HST':'Host Hotels & Resorts Inc. ',
     'HSTM':'HealthStream Inc. ',
     'HSTO':'Histogen Inc. ',
     'HSY':'The Hershey Company ',
     'HT':'Hersha Hospitality Trust   of Beneficial Interest',
     'HTBI':'HomeTrust Bancshares Inc. ',
     'HTBK':'Heritage Commerce Corp ',
     'HTCR':'Heartcore Enterprises Inc. ',
     'HTD':'John Hancock Tax Advantaged Dividend Income Fund  of Beneficial Interest',
     'HTGC':'Hercules Capital Inc. ',
     'HTH':'Hilltop Holdings Inc.',
     'HTHT':'H World Group Limited ',
     'HTLD':'Heartland Express Inc. ',
     'HTLF':'Heartland Financial USA Inc. ',
     'HTOO':'Fusion Fuel Green PLC ',
     'HTOOW':'Fusion Fuel Green PLC ',
     'HTY':'John Hancock Tax-Advantaged Global Shareholder Yield Fund  of Beneficial Interest',
     'HTZ':'Hertz Global Holdings Inc ',
     'HTZWW':'Hertz Global Holdings Inc ',
     'HUBB':'Hubbell Inc ',
     'HUBC':'Hub Cyber Security Ltd. ',
     'HUBCW':'Hub Cyber Security Ltd.  2/27/28',
     'HUBCZ':'Hub Cyber Security Ltd.  8/22/23',
     'HUBG':'Hub Group Inc.  ',
     'HUBS':'HubSpot Inc. ',
     'HUDA':'Hudson Acquisition I Corp. ',
     'HUDAR':'Hudson Acquisition I Corp. Right',
     'HUDAU':'Hudson Acquisition  I Corp. Unit',
     'HUDI':'Huadi International Group Co. Ltd. ',
     'HUGE':'FSD Pharma Inc. Class B Subordinate Voting Shares',
     'HUIZ':'Huize Holding Limited ',
     'HUM':'Humana Inc. ',
     'HUMA':'Humacyte Inc. ',
     'HUMAW':'Humacyte Inc. ',
     'HUN':'Huntsman Corporation ',
     'HURC':'Hurco Companies Inc. ',
     'HURN':'Huron Consulting Group Inc. ',
     'HUSA':'Houston American Energy Corporation ',
     'HUT':'Hut 8 Mining Corp. ',
     'HUYA':'HUYA Inc.  each  representing one',
     'HVT':'Haverty Furniture Companies Inc. ',
     'HVT/A':'Haverty Furniture Companies Inc.',
     'HWBK':'Hawthorn Bancshares Inc. ',
     'HWC':'Hancock Whitney Corporation ',
     'HWEL':'Healthwell Acquisition Corp. I  ',
     'HWELU':'Healthwell Acquisition Corp. I Unit',
     'HWELW':'Healthwell Acquisition Corp. I ',
     'HWKN':'Hawkins Inc. ',
     'HWKZ':'Hawks Acquisition Corp  ',
     'HWM':'Howmet Aerospace Inc. ',
     'HWM^':'Howmet Aerospace Inc. $3.75 Preferred Stock',
     'HXL':'Hexcel Corporation ',
     'HY':'Hyster-Yale Materials Handling Inc.  ',
     'HYB':'New America High Income Fund Inc. ',
     'HYFM':'Hydrofarm Holdings Group Inc. ',
     'HYI':'Western Asset High Yield Defined Opportunity Fund Inc. ',
     'HYLN':'Hyliion Holdings Corp.  ',
     'HYPR':'Hyperfine Inc.  ',
     'HYT':'Blackrock Corporate High Yield Fund Inc. ',
     'HYW':'Hywin Holdings Ltd. ',
     'HYZN':'Hyzon Motors Inc.  ',
     'HYZNW':'Hyzon Motors Inc. s',
     'HZNP':'Horizon Therapeutics Public Limited Company ',
     'HZO':'MarineMax Inc.  (FL) ',
     'IAC':'IAC Inc. ',
     'IAE':'Voya Asia Pacific High Dividend Equity Income Fund ING Asia Pacific High Dividend Equity Income Fund  of Beneficial Interest',
     'IAF':'abrdn Australia Equity Fund Inc. ',
     'IAG':'Iamgold Corporation ',
     'IART':'Integra LifeSciences Holdings Corporation ',
     'IAS':'Integral Ad Science Holding Corp. ',
     'IAUX':'i-80 Gold Corp. ',
     'IBCP':'Independent Bank Corporation ',
     'IBEX':'IBEX Limited ',
     'IBIO':'iBio Inc. ',
     'IBKR':'Interactive Brokers Group Inc.  ',
     'IBM':'International Business Machines Corporation ',
     'IBN':'ICICI Bank Limited ',
     'IBOC':'International Bancshares Corporation ',
     'IBP':'Installed Building Products Inc. ',
     'IBRX':'ImmunityBio Inc. ',
     'IBTX':'Independent Bank Group Inc ',
     'ICAD':'iCAD Inc. ',
     'ICCC':'ImmuCell Corporation ',
     'ICCH':'ICC Holdings Inc. ',
     'ICCM':'IceCure Medical Ltd. ',
     'ICD':'Independence Contract Drilling Inc. ',
     'ICE':'Intercontinental Exchange Inc. ',
     'ICFI':'ICF International Inc. ',
     'ICG':'Intchains Group Limited ',
     'ICHR':'Ichor Holdings ',
     'ICL':'ICL Group Ltd. ',
     'ICLK':'iClick Interactive Asia Group Limited ',
     'ICLR':'ICON plc ',
     'ICMB':'Investcorp Credit Management BDC Inc. ',
     'ICNC':'Iconic Sports Acquisition Corp. ',
     'ICPT':'Intercept Pharmaceuticals Inc. ',
     'ICU':'SeaStar Medical Holding Corporation ',
     'ICUCW':'SeaStar Medical Holding Corporation ',
     'ICUI':'ICU Medical Inc. ',
     'ICVX':'Icosavax Inc. ',
     'ID':'PARTS iD Inc.  ',
     'IDA':'IDACORP Inc. ',
     'IDAI':'T Stamp Inc.  ',
     'IDBA':'IDEX Biometrics ASA ',
     'IDCC':'InterDigital Inc. ',
     'IDE':'Voya Infrastructure Industrials and Materials Fund  of Beneficial Interest',
     'IDEX':'Ideanomics Inc. ',
     'IDN':'Intellicheck Inc. ',
     'IDR':'Idaho Strategic Resources Inc. ',
     'IDT':'IDT Corporation Class B ',
     'IDXX':'IDEXX Laboratories Inc. ',
     'IDYA':'IDEAYA Biosciences Inc. ',
     'IE':'Ivanhoe Electric Inc. ',
     'IEP':'Icahn Enterprises L.P. ',
     'IESC':'IES Holdings Inc. ',
     'IEX':'IDEX Corporation ',
     'IFBD':'Infobird Co. Ltd ',
     'IFF':'International Flavors & Fragrances Inc. ',
     'IFIN':'InFinT Acquisition Corporation ',
     'IFN':'India Fund Inc. ',
     'IFRX':'InflaRx N.V. ',
     'IFS':'Intercorp Financial Services Inc. ',
     'IGA':'Voya Global Advantage and Premium Opportunity Fund  of Beneficial Interest',
     'IGC':'IGC Pharma Inc. ',
     'IGD':'Voya Global Equity Dividend and Premium Opportunity Fund',
     'IGI':'Western Asset Investment Grade Defined Opportunity Trust Inc. ',
     'IGIC':'International General Insurance Holdings Ltd. ',
     'IGICW':'International General Insurance Holdings Ltd. s expiring 03/17/2025',
     'IGMS':'IGM Biosciences Inc. ',
     'IGR':'CBRE Global Real Estate Income Fund  of Beneficial Interest',
     'IGT':'International Game Technology ',
     'IGTA':'Inception Growth Acquisition Limited ',
     'IGTAR':'Inception Growth Acquisition Limited Rights',
     'IGTAW':'Inception Growth Acquisition Limited s',
     'IH':'iHuman Inc.  each representing five ',
     'IHD':'Voya Emerging Markets High Income Dividend Equity Fund ',
     'IHG':'Intercontinental Hotels Group  (Each representing one )',
     'IHIT':'Invesco High Income 2023 Target Term Fund  of Beneficial Interest',
     'IHRT':'iHeartMedia Inc.  ',
     'IHS':'IHS Holding Limited ',
     'IHT':'InnSuites Hospitality Trust Shares of Beneficial Interest',
     'IHTA':'Invesco High Income 2024 Target Term Fund  of Beneficial Interest No par value per share',
     'III':'Information Services Group Inc. ',
     'IIIN':'Insteel Industries Inc. ',
     'IIIV':'i3 Verticals Inc.  ',
     'IIM':'Invesco Value Municipal Income Trust ',
     'IINN':'Inspira Technologies Oxy B.H.N. Ltd. ',
     'IINNW':'Inspira Technologies Oxy B.H.N. Ltd. ',
     'IIPR':'Innovative Industrial Properties Inc. ',
     'IKNA':'Ikena Oncology Inc. ',
     'IKT':'Inhibikase Therapeutics Inc. ',
     'ILAG':'Intelligent Living Application Group Inc. ',
     'ILLM':'illumin Holdings Inc. ',
     'ILMN':'Illumina Inc. ',
     'ILPT':'Industrial Logistics Properties Trust  of Beneficial Interest',
     'IMAB':'I-MAB ',
     'IMAQ':'International Media Acquisition Corp.  ',
     'IMAQR':'International Media Acquisition Corp. Rights',
     'IMAQW':'International Media Acquisition Corp. s',
     'IMAX':'Imax Corporation ',
     'IMBI':'iMedia Brands Inc.  ',
     'IMCC':'IM Cannabis Corp. ',
     'IMCR':'Immunocore Holdings plc ',
     'IMGN':'ImmunoGen Inc. ',
     'IMKTA':'Ingles Markets Incorporated  ',
     'IMMP':'Immutep Limited ',
     'IMMR':'Immersion Corporation ',
     'IMMX':'Immix Biopharma Inc. ',
     'IMNM':'Immunome Inc. ',
     'IMNN':'Imunon Inc. ',
     'IMO':'Imperial Oil Limited ',
     'IMOS':'ChipMOS TECHNOLOGIES INC. ',
     'IMPL':'Impel Pharmaceuticals Inc. ',
     'IMPP':'Imperial Petroleum Inc. ',
     'IMRN':'Immuron Limited ',
     'IMRX':'Immuneering Corporation  ',
     'IMTE':'Integrated Media Technology Limited ',
     'IMTX':'Immatics N.V. ',
     'IMTXW':'Immatics N.V. s',
     'IMUX':'Immunic Inc. ',
     'IMVT':'Immunovant Inc. ',
     'IMXI':'International Money Express Inc. ',
     'INAB':'IN8bio Inc. ',
     'INAQ':'Insight Acquisition Corp.  ',
     'INAQW':'Insight Acquisition Corp. ',
     'INBK':'First Internet Bancorp ',
     'INBS':'Intelligent Bio Solutions Inc. ',
     'INBX':'Inhibrx Inc. ',
     'INCR':'Intercure Ltd. ',
     'INCY':'Incyte Corp. ',
     'INDB':'Independent Bank Corp. ',
     'INDI':'indie Semiconductor Inc.  ',
     'INDIW':'indie Semiconductor Inc. ',
     'INDO':'Indonesia Energy Corporation Limited ',
     'INDP':'Indaptus Therapeutics Inc. ',
     'INDV':'Indivior PLC ',
     'INFA':'Informatica Inc.  ',
     'INFI':'Infinity Pharmaceuticals Inc. ',
     'INFN':'Infinera Corporation ',
     'INFU':'InfuSystems Holdings Inc. ',
     'INFY':'Infosys Limited ',
     'ING':'ING Group N.V. ',
     'INGN':'Inogen Inc ',
     'INGR':'Ingredion Incorporated ',
     'INKT':'MiNK Therapeutics Inc. ',
     'INLX':'Intellinetics Inc. ',
     'INM':'InMed Pharmaceuticals Inc. ',
     'INMB':'INmune Bio Inc. ',
     'INMD':'InMode Ltd. ',
     'INN':'Summit Hotel Properties Inc. ',
     'INNV':'InnovAge Holding Corp. ',
     'INO':'Inovio Pharmaceuticals Inc. ',
     'INOD':'Innodata Inc. ',
     'INPX':'Inpixon ',
     'INSE':'Inspired Entertainment Inc. ',
     'INSG':'Inseego Corp. ',
     'INSI':'Insight Select Income Fund',
     'INSM':'Insmed Incorporated ',
     'INSP':'Inspire Medical Systems Inc. ',
     'INST':'Instructure Holdings Inc. ',
     'INSW':'International Seaways Inc. ',
     'INTA':'Intapp Inc. ',
     'INTC':'Intel Corporation ',
     'INTE':'Integral Acquisition Corporation 1  ',
     'INTEU':'Integral Acquisition Corporation 1 Unit',
     'INTEW':'Integral Acquisition Corporation 1 s',
     'INTG':'Intergroup Corporation ',
     'INTR':'Inter & Co. Inc.  ',
     'INTS':'Intensity Therapeutics Inc. ',
     'INTT':'inTest Corporation ',
     'INTU':'Intuit Inc. ',
     'INTZ':'Intrusion Inc. ',
     'INUV':'Inuvo Inc.',
     'INVA':'Innoviva Inc. ',
     'INVE':'Identiv Inc. ',
     'INVH':'Invitation Homes Inc. ',
     'INVO':'INVO BioScience Inc. ',
     'INVZ':'Innoviz Technologies Ltd. ',
     'INVZW':'Innoviz Technologies Ltd. ',
     'INZY':'Inozyme Pharma Inc. ',
     'IOAC':'Innovative International Acquisition Corp. ',
     'IOACW':'Innovative International Acquisition Corp. s',
     'IOBT':'IO Biotech Inc. ',
     'IONM':'Assure Holdings Corp. ',
     'IONQ':'IonQ Inc. ',
     'IONR':'ioneer Ltd ',
     'IONS':'Ionis Pharmaceuticals Inc. ',
     'IOR':'Income Opportunity Realty Investors Inc. ',
     'IOSP':'Innospec Inc. ',
     'IOT':'Samsara Inc.  ',
     'IOVA':'Iovance Biotherapeutics Inc. ',
     'IP':'International Paper Company ',
     'IPA':'ImmunoPrecise Antibodies Ltd. ',
     'IPAR':'Inter Parfums Inc. ',
     'IPDN':'Professional Diversity Network Inc. ',
     'IPG':'Interpublic Group of Companies Inc. ',
     'IPGP':'IPG Photonics Corporation ',
     'IPHA':'Innate Pharma S.A. ADS',
     'IPI':'Intrepid Potash Inc ',
     'IPSC':'Century Therapeutics Inc. ',
     'IPVF':'InterPrivate III Financial Partners Inc.  ',
     'IPW':'iPower Inc. ',
     'IPWR':'Ideal Power Inc. ',
     'IPX':'IperionX Limited ',
     'IPXXU':'Inflection Point Acquisition Corp. II Unit',
     'IQ':'iQIYI Inc. ',
     'IQI':'Invesco Quality Municipal Income Trust ',
     'IQV':'IQVIA Holdings Inc. ',
     'IR':'Ingersoll Rand Inc. ',
     'IRAA':'Iris Acquisition Corp  ',
     'IRAAW':'Iris Acquisition Corp ',
     'IRBT':'iRobot Corporation ',
     'IRDM':'Iridium Communications Inc ',
     'IREN':'Iris Energy Limited ',
     'IRIX':'IRIDEX Corporation ',
     'IRM':'Iron Mountain Incorporated (Delaware) REIT',
     'IRMD':'iRadimed Corporation ',
     'IRNT':'IronNet Inc. ',
     'IRON':'Disc Medicine Inc. ',
     'IROQ':'IF Bancorp Inc. ',
     'IRS':'IRSA Inversiones Y Representaciones S.A. ',
     'IRT':'Independence Realty Trust Inc. ',
     'IRTC':'iRhythm Technologies Inc. ',
     'IRWD':'Ironwood Pharmaceuticals Inc.  ',
     'ISD':'PGIM High Yield Bond Fund Inc.',
     'ISDR':'Issuer Direct Corporation ',
     'ISEE':'IVERIC bio Inc. ',
     'ISIG':'Insignia Systems Inc. ',
     'ISPC':'iSpecimen Inc. ',
     'ISPO':'Inspirato Incorporated  ',
     'ISPOW':'Inspirato Incorporated ',
     'ISPR':'Ispire Technology Inc. ',
     'ISRG':'Intuitive Surgical Inc. ',
     'ISRL':'Israel Acquisitions Corp ',
     'ISRLU':'Israel Acquisitions Corp Unit',
     'ISRLW':'Israel Acquisitions Corp ',
     'ISSC':'Innovative Solutions and Support Inc. ',
     'ISTR':'Investar Holding Corporation ',
     'ISUN':'iSun Inc. ',
     'IT':'Gartner Inc. ',
     'ITCI':'Intra-Cellular Therapies Inc. ',
     'ITCL':'Banco Itau Chile  (each representing one third of a share of )',
     'ITGR':'Integer Holdings Corporation ',
     'ITI':'Iteris Inc. ',
     'ITIC':'Investors Title Company ',
     'ITOS':'iTeos Therapeutics Inc. ',
     'ITP':'IT Tech Packaging Inc. ',
     'ITRG':'Integra Resources Corp. ',
     'ITRI':'Itron Inc. ',
     'ITRM':'Iterum Therapeutics plc ',
     'ITRN':'Ituran Location and Control Ltd. ',
     'ITT':'ITT Inc. ',
     'ITUB':'Itau Unibanco Banco Holding SA  (Each repstg 500 Preferred shares)',
     'ITW':'Illinois Tool Works Inc. ',
     'IVA':'Inventiva S.A. American Depository Shares',
     'IVAC':'Intevac Inc. ',
     'IVCA':'Investcorp India Acquisition Corp.',
     'IVCAW':'Investcorp India Acquisition Corp. ',
     'IVCB':'Investcorp Europe Acquisition Corp I ',
     'IVCP':'Swiftmerge Acquisition Corp.',
     'IVCPU':'Swiftmerge Acquisition Corp. Unit',
     'IVCPW':'Swiftmerge Acquisition Corp. s',
     'IVDA':'Iveda Solutions Inc. ',
     'IVDAW':'Iveda Solutions Inc. ',
     'IVR':'INVESCO MORTGAGE CAPITAL INC ',
     'IVT':'InvenTrust Properties Corp. ',
     'IVVD':'Invivyd Inc. ',
     'IVZ':'Invesco Ltd ',
     'IX':'Orix Corp Ads ',
     'IXAQ':'IX Acquisition Corp.',
     'IXAQU':'IX Acquisition Corp. Unit',
     'IXHL':'Incannex Healthcare Limited ',
     'IZEA':'IZEA Worldwide Inc. ',
     'IZM':'ICZOOM Group Inc. ',
     'J':'Jacobs Solutions Inc. ',
     'JACK':'Jack In The Box Inc. ',
     'JAGX':'Jaguar Health Inc. ',
     'JAKK':'JAKKS Pacific Inc. ',
     'JAMF':'Jamf Holding Corp. ',
     'JAN':'JanOne Inc.  (NV)',
     'JANX':'Janux Therapeutics Inc. ',
     'JAQCU':'Jupiter Acquisition Corporation Units',
     'JAZZ':'Jazz Pharmaceuticals plc  (Ireland)',
     'JBGS':'JBG SMITH Properties ',
     'JBHT':'J.B. Hunt Transport Services Inc. ',
     'JBI':'Janus International Group Inc. ',
     'JBL':'Jabil Inc. ',
     'JBLU':'JetBlue Airways Corporation ',
     'JBSS':'John B. Sanfilippo & Son Inc. ',
     'JBT':'John Bean Technologies Corporation ',
     'JCI':'Johnson Controls International plc ',
     'JCSE':'JE Cleantech Holdings Limited ',
     'JCTCF':'Jewett-Cameron Trading Company ',
     'JD':'JD.com Inc. ',
     'JEF':'Jefferies Financial Group Inc. ',
     'JELD':'JELD-WEN Holding Inc. ',
     'JEQ':'abrdn Japan Equity Fund Inc. ',
     'JEWL':'Adamas One Corp. ',
     'JFBR':'Jeffs Brands Ltd ',
     'JFBRW':'Jeffs Brands Ltd ',
     'JFIN':'Jiayin Group Inc. ',
     'JFR':'Nuveen Floating Rate Income Fund ',
     'JFU':'9F Inc. ',
     'JG':'Aurora Mobile Limited ',
     'JGH':'Nuveen Global High Income Fund  of Beneficial Interest',
     'JHAA':'Nuveen Corporate Income 2023 Target Term Fund',
     'JHG':'Janus Henderson Group plc ',
     'JHI':'John Hancock Investors Trust ',
     'JHS':'John Hancock Income Securities Trust ',
     'JHX':'James Hardie Industries plc  (Ireland)',
     'JILL':'J. Jill Inc. ',
     'JJSF':'J & J Snack Foods Corp. ',
     'JKHY':'Jack Henry & Associates Inc. ',
     'JKS':'JinkoSolar Holding Company Limited  (each representing 4 )',
     'JLL':'Jones Lang LaSalle Incorporated ',
     'JLS':'Nuveen Mortgage and Income Fund',
     'JMIA':'Jumia Technologies AG  each representing two ',
     'JMM':'Nuveen Multi-Market Income Fund (MA)',
     'JMSB':'John Marshall Bancorp Inc. ',
     'JNJ':'Johnson & Johnson ',
     'JNPR':'Juniper Networks Inc. ',
     'JOAN':'JOANN Inc. ',
     'JOB':'GEE Group Inc. ',
     'JOBY':'Joby Aviation Inc. ',
     'JOE':'St. Joe Company ',
     'JOF':'Japan Smaller Capitalization Fund Inc ',
     'JOUT':'Johnson Outdoors Inc.  ',
     'JPM':'JP Morgan Chase & Co. ',
     'JRSH':'Jerash Holdings (US) Inc. ',
     'JRVR':'James River Group Holdings Ltd. ',
     'JSD':'Nuveen Short Duration Credit Opportunities Fund  of Beneficial Interest',
     'JSPR':'Jasper Therapeutics Inc. ',
     'JSPRW':'Japer Therapeutics Inc. s',
     'JT':'Jianpu Technology Inc. ',
     'JUN':'Juniper II Corp.  ',
     'JUPW':'Jupiter Wellness Inc. ',
     'JUPWW':'Jupiter Wellness Inc. ',
     'JVA':'Coffee Holding Co. Inc. ',
     'JWEL':'Jowell Global Ltd. ',
     'JWN':'Nordstrom Inc. ',
     'JWSM':'Jaws Mustang Acquisition Corp. ',
     'JXJT':'JX Luxventure Limited ',
     'JXN':'Jackson Financial Inc.  ',
     'JYD':'Jayud Global Logistics Limited ',
     'JYNT':'The Joint Corp. ',
     'JZ':'Jianzhi Education Technology Group Company Limited ',
     'JZXN':'Jiuzi Holdings Inc. ',
     'K':'Kellogg Company ',
     'KA':'Kineta Inc. ',
     'KACLR':'Kairous Acquisition Corp. Limited Rights',
     'KACLW':'Kairous Acquisition Corp. Limited s',
     'KAI':'Kadant Inc ',
     'KALA':'Kala Pharmaceuticals Inc. ',
     'KALU':'Kaiser Aluminum Corporation ',
     'KALV':'KalVista Pharmaceuticals Inc. ',
     'KAMN':'Kaman Corporation ',
     'KAR':'OPENLANE Inc. ',
     'KARO':'Karooooo Ltd. ',
     'KAVL':'Kaival Brands Innovations Group Inc. ',
     'KB':'KB Financial Group Inc',
     'KBH':'KB Home ',
     'KBNT':'Kubient Inc. ',
     'KBNTW':'Kubient Inc. ',
     'KBR':'KBR Inc. ',
     'KC':'Kingsoft Cloud Holdings Limited ',
     'KCGI':'Kensington Capital Acquisition Corp. V ',
     'KD':'Kyndryl Holdings Inc. ',
     'KDNY':'Chinook Therapeutics Inc. ',
     'KDP':'Keurig Dr Pepper Inc. ',
     'KE':'Kimball Electronics Inc. ',
     'KELYA':'Kelly Services Inc.  ',
     'KELYB':'Kelly Services Inc. Class B ',
     'KEN':'Kenon Holdings Ltd. ',
     'KEP':'Korea Electric Power Corporation ',
     'KEQU':'Kewaunee Scientific Corporation ',
     'KERN':'Akerna Corp. ',
     'KERNW':'Akerna Corp ',
     'KEX':'Kirby Corporation ',
     'KEY':'KeyCorp ',
     'KEYS':'Keysight Technologies Inc. ',
     'KF':'Korea Fund Inc. New ',
     'KFFB':'Kentucky First Federal Bancorp ',
     'KFRC':'Kforce Inc. ',
     'KFS':'Kingsway Financial Services Inc.  (DE)',
     'KFY':'Korn Ferry ',
     'KGC':'Kinross Gold Corporation ',
     'KGS':'Kodiak Gas Services Inc. ',
     'KHC':'The Kraft Heinz Company ',
     'KIDS':'OrthoPediatrics Corp. ',
     'KIM':'Kimco Realty Corporation (HC) ',
     'KIND':'Nextdoor Holdings Inc.  ',
     'KINS':'Kingstone Companies Inc. ',
     'KIND':'Nextdoor Holdings Inc.  ',
     'KINS':'Kingstone Companies Inc. ',
     'KIND':'Nextdoor Holdings Inc.  ',
     'KINS':'Kingstone Companies Inc. ',
     'KIND':'Nextdoor Holdings Inc.  ',
     'KINS':'Kingstone Companies Inc. ',
     'KKR':'KKR & Co. Inc.',
     'KLAC':'KLA Corporation ',
     'KLIC':'Kulicke and Soffa Industries Inc. ',
     'KLR':'Kaleyra Inc. ',
     'KLTR':'Kaltura Inc. ',
     'KLXE':'KLX Energy Services Holdings Inc. ',
     'KMB':'Kimberly-Clark Corporation ',
     'KMDA':'Kamada Ltd. ',
     'KMF':'Kayne Anderson NextGen Energy & Infrastructure Inc.',
     'KMI':'Kinder Morgan Inc. ',
     'KMPR':'Kemper Corporation',
     'KMT':'Kennametal Inc. ',
     'KMX':'CarMax Inc',
     'KN':'Knowles Corporation ',
     'KNDI':'Kandi Technologies Group Inc ',
     'KNF':'Knife Riv Holding Co. ',
     'KNOP':'KNOT Offshore Partners LP Common Units representing Limited Partner Interests',
     'KNSA':'Kiniksa Pharmaceuticals Ltd.  ',
     'KNSL':'Kinsale Capital Group Inc. ',
     'KNSW':'KnightSwan Acquisition Corporation  ',
     'KNTE':'Kinnate Biopharma Inc. ',
     'KNTK':'Kinetik Holdings Inc.  ',
     'KNW':'Know Labs Inc. ',
     'KNX':'Knight-Swift Transportation Holdings Inc.',
     'KO':'Coca-Cola Company ',
     'KOD':'Kodiak Sciences Inc ',
     'KODK':'Eastman Kodak Company Common New',
     'KOF':'Coca Cola Femsa S.A.B. de C.V. ',
     'KOP':'Koppers Holdings Inc. Koppers Holdings Inc. ',
     'KOPN':'Kopin Corporation ',
     'KORE':'KORE Group Holdings Inc. ',
     'KOS':'Kosmos Energy Ltd.  (DE)',
     'KOSS':'Koss Corporation ',
     'KPLT':'Katapult Holdings Inc. ',
     'KPLTW':'Katapult Holdings Inc. ',
     'KPRX':'Kiora Pharmaceuticals Inc.  ',
     'KPTI':'Karyopharm Therapeutics Inc. ',
     'KR':'Kroger Company ',
     'KRBP':'Kiromic BioPharma Inc. ',
     'KRC':'Kilroy Realty Corporation ',
     'KREF':'KKR Real Estate Finance Trust Inc. ',
     'KRG':'Kite Realty Group Trust ',
     'KRKR':'36Kr Holdings Inc. ',
     'KRMD':'KORU Medical Systems Inc.  (DE)',
     'KRNL':'Kernel Group Holdings Inc. ',
     'KRNLU':'Kernel Group Holdings Inc. Units',
     'KRNLW':'Kernel Group Holdings Inc. s',
     'KRNT':'Kornit Digital Ltd. ',
     'KRNY':'Kearny Financial Corp ',
     'KRO':'Kronos Worldwide Inc ',
     'KRON':'Kronos Bio Inc. ',
     'KROS':'Keros Therapeutics Inc. ',
     'KRP':'Kimbell Royalty Partners ',
     'KRT':'Karat Packaging Inc. ',
     'KRTX':'Karuna Therapeutics Inc. ',
     'KRUS':'Kura Sushi USA Inc.  ',
     'KRYS':'Krystal Biotech Inc. ',
     'KSCP':'Knightscope Inc.  ',
     'KSM':'DWS Strategic Municipal Income Trust',
     'KSS':'Kohls Corporation ',
     'KT':'KT Corporation ',
     'KTB':'Kontoor Brands Inc. ',
     'KTCC':'Key Tronic Corporation ',
     'KTF':'DWS Municipal Income Trust',
     'KTOS':'Kratos Defense & Security Solutions Inc. ',
     'KTRA':'Kintara Therapeutics Inc. ',
     'KTTA':'Pasithea Therapeutics Corp. ',
     'KTTAW':'Pasithea Therapeutics Corp. ',
     'KUKE':'Kuke Music Holding Limited  each representing one ',
     'KULR':'KULR Technology Group Inc. ',
     'KURA':'Kura Oncology Inc. ',
     'KVHI':'KVH Industries Inc. ',
     'KVSA':'Khosla Ventures Acquisition Co.  ',
     'KVUE':'Kenvue Inc. ',
     'KW':'Kennedy-Wilson Holdings Inc. ',
     'KWE':'KWESST Micro Systems Inc. ',
     'KWESW':'KWESST Micro Systems Inc. ',
     'KWR':'Quaker Houghton ',
     'KXIN':'Kaixin Auto Holdings ',
     'KYCH':'Keyarch Acquisition Corporation ',
     'KYCHR':'Keyarch Acquisition Corporation Rights',
     'KYCHU':'Keyarch Acquisition Corporation Unit',
     'KYCHW':'Keyarch Acquisition Corporation ',
     'KYMR':'Kymera Therapeutics Inc. ',
     'KYN':'Kayne Anderson Energy Infrastructure Fund Inc.',
     'KZIA':'Kazia Therapeutics Limited ',
     'KZR':'Kezar Life Sciences Inc. ',
     'L':'Loews Corporation ',
     'LAB':'Standard BioTools Inc. ',
     'LABP':'Landos Biopharma Inc. ',
     'LAC':'Lithium Americas Corp. ',
     'LAD':'Lithia Motors Inc. ',
     'LADR':'Ladder Capital Corp  ',
     'LAES':'SEALSQ Corp ',
     'LAKE':'Lakeland Industries Inc. ',
     'LAMR':'Lamar Advertising Company  ',
     'LANC':'Lancaster Colony Corporation ',
     'LAND':'Gladstone Land Corporation ',
     'LANV':'Lanvin Group Holdings Limited ',
     'LARK':'Landmark Bancorp Inc. ',
     'LASE':'Laser Photonics Corporation ',
     'LASR':'nLIGHT Inc. ',
     'LATG':'LatAmGrowth SPAC ',
     'LATGU':'LatAmGrowth SPAC Unit',
     'LAUR':'Laureate Education Inc. ',
     'LAW':'CS Disco Inc. ',
     'LAZ':'Lazard LTD. Lazard LTD.  ',
     'LAZR':'Luminar Technologies Inc.   ',
     'LAZY':'Lazydays Holdings Inc. ',
     'LBAI':'Lakeland Bancorp Inc. ',
     'LBBB':'Lakeshore Acquisition II Corp. ',
     'LBBBR':'Lakeshore Acquisition II Corp. Rights',
     'LBBBW':'Lakeshore Acquisition II Corp. s',
     'LBC':'Luther Burbank Corporation ',
     'LBPH':'Longboard Pharmaceuticals Inc. ',
     'LBRDA':'Liberty Broadband Corporation  ',
     'LBRDK':'Liberty Broadband Corporation Class C ',
     'LBRDP':'Liberty Broadband Corporation Series A Cumulative Redeemable Preferred Stock',
     'LBRT':'Liberty Energy Inc.  ',
     'LBTYA':'Liberty Global plc ',
     'LBTYB':'Liberty Global plc Class B ',
     'LBTYK':'Liberty Global plc Class C ',
     'LC':'LendingClub Corporation ',
     'LCAA':'L Catterton Asia Acquisition Corp ',
     'LCAAU':'L Catterton Asia Acquisition Corp Units',
     'LCAAW':'L Catterton Asia Acquisition Corp ',
     'LCAHU':'Landcadia Holdings IV Inc. Units',
     'LCAHW':'Landcadia Holdings IV Inc. ',
     'LCFY':'Locafy Limited ',
     'LCFYW':'Locafy Limited ',
     'LCID':'Lucid Group Inc. ',
     'LCII':'LCI Industries',
     'LCNB':'LCNB Corporation ',
     'LCTX':'Lineage Cell Therapeutics Inc. ',
     'LCUT':'Lifetime Brands Inc. ',
     'LCW':'Learn CW Investment Corporation ',
     'LDI':'loanDepot Inc.  ',
     'LDOS':'Leidos Holdings Inc. ',
     'LDP':'Cohen & Steers Limited Duration Preferred and Income Fund Inc.',
     'LE':'Lands End Inc. ',
     'LEA':'Lear Corporation ',
     'LECO':'Lincoln Electric Holdings Inc. ',
     'LEDS':'SemiLEDS Corporation ',
     'LEE':'Lee Enterprises Incorporated ',
     'LEG':'Leggett & Platt Incorporated ',
     'LEGH':'Legacy Housing Corporation  (TX)',
     'LEGN':'Legend Biotech Corporation ',
     'LEJU':'Leju Holdings Limited  each representing one ',
     'LEN':'Lennar Corporation  ',
     'LEO':'BNY Mellon Strategic Municipals Inc. ',
     'LESL':'Leslies Inc. ',
     'LEU':'Centrus Energy Corp.  ',
     'LEV':'The Lion Electric Company ',
     'LEVI':'Levi Strauss & Co  ',
     'LEXX':'Lexaria Bioscience Corp. ',
     'LEXXW':'Lexaria Bioscience Corp. ',
     'LFAC':'LF Capital Acquisition Corp. II  ',
     'LFACW':'LF Capital Acquisition Corp. II s',
     'LFCR':'Lifecore Biomedical Inc. ',
     'LFLY':'Leafly Holdings Inc. ',
     'LFLYW':'Leafly Holdings Inc. ',
     'LFMD':'LifeMD Inc. ',
     'LFST':'LifeStance Health Group Inc. ',
     'LFT':'Lument Finance Trust Inc. ',
     'LFUS':'Littelfuse Inc. ',
     'LFVN':'Lifevantage Corporation  (Delaware)',
     'LGHL':'Lion Group Holding Ltd. ',
     'LGHLW':'Lion Group Holding Ltd. ',
     'LGI':'Lazard Global Total Return and Income Fund ',
     'LGIH':'LGI Homes Inc. ',
     'LGL':'LGL Group Inc. ',
     'LGMK':'LogicMark Inc.  (NV)',
     'LGND':'Ligand Pharmaceuticals Incorporated ',
     'LGO':'Largo Inc. ',
     'LGST':'Semper Paratus Acquisition Corporation ',
     'LGSTW':'Semper Paratus Acquisition Corporation ',
     'LGVC':'LAMF Global Ventures Corp. I ',
     'LGVCW':'LAMF Global Ventures Corp. I ',
     'LGVN':'Longeveron Inc.  ',
     'LH':'Laboratory Corporation of America Holdings ',
     'LHC':'Leo Holdings Corp. II ',
     'LHX':'L3Harris Technologies Inc. ',
     'LI':'Li Auto Inc. ',
     'LIAN':'LianBio ',
     'LIBY':'Liberty Resources Acquisition Corp.  ',
     'LIBYU':'Liberty Resources Acquisition Corp. Unit',
     'LICN':'Lichen China Limited ',
     'LICY':'Li-Cycle Holdings Corp. ',
     'LIDR':'AEye Inc.  ',
     'LIDRW':'AEye Inc. ',
     'LIFE':'aTyr Pharma Inc. ',
     'LIFW':'MSP Recovery Inc.  ',
     'LIFWW':'MSP Recovery Inc. ',
     'LIFWZ':'MSP Recovery Inc. ',
     'LII':'Lennox International Inc. ',
     'LILA':'Liberty Latin America Ltd.  ',
     'LILAK':'Liberty Latin America Ltd. Class C ',
     'LILM':'Lilium N.V. ',
     'LILMW':'Lilium N.V. s',
     'LIN':'Linde plc ',
     'LINC':'Lincoln Educational Services Corporation ',
     'LIND':'Lindblad Expeditions Holdings Inc. ',
     'LINK':'Interlink Electronics Inc. ',
     'LIPO':'Lipella Pharmaceuticals Inc. ',
     'LIQT':'LiqTech International Inc. ',
     'LITB':'LightInTheBox Holding Co. Ltd.  each representing 2 ',
     'LITE':'Lumentum Holdings Inc. ',
     'LITM':'Snow Lake Resources Ltd. ',
     'LIVB':'LIV Capital Acquisition Corp. II ',
     'LIVBW':'LIV Capital Acquisition Corp. II s',
     'LIVE':'Live Ventures Incorporated ',
     'LIVN':'LivaNova PLC ',
     'LIXT':'Lixte Biotechnology Holdings Inc. ',
     'LIXTW':'Lixte Biotechnology Holdings Inc. s',
     'LIZI':'LIZHI INC. ',
     'LKCO':'Luokung Technology Corp ',
     'LKFN':'Lakeland Financial Corporation ',
     'LKQ':'LKQ Corporation ',
     'LL':'LL Flooring Holdings Inc. ',
     'LLAP':'Terran Orbital Corporation ',
     'LLY':'Eli Lilly and Company ',
     'LMAT':'LeMaitre Vascular Inc. ',
     'LMB':'Limbach Holdings Inc. ',
     'LMDX':'LumiraDx Limited ',
     'LMDXW':'LumiraDx Limited ',
     'LMFA':'LM Funding America Inc. ',
     'LMND':'Lemonade Inc. ',
     'LMNL':'Liminal BioSciences Inc. ',
     'LMNR':'Limoneira Co ',
     'LMT':'Lockheed Martin Corporation ',
     'LNC':'Lincoln National Corporation ',
     'LND':'Brasilagro Brazilian Agric Real Estate Co Sponsored ADR (Brazil)',
     'LNG':'Cheniere Energy Inc. ',
     'LNKB':'LINKBANCORP Inc. ',
     'LNN':'Lindsay Corporation ',
     'LNSR':'LENSAR Inc. ',
     'LNT':'Alliant Energy Corporation ',
     'LNTH':'Lantheus Holdings Inc. ',
     'LNW':'Light & Wonder Inc. ',
     'LNZA':'LanzaTech Global Inc. ',
     'LNZAW':'LanzaTech Global Inc. ',
     'LOAN':'Manhattan Bridge Capital Inc',
     'LOB':'Live Oak Bancshares Inc. ',
     'LOCC':'Live Oak Crestview Climate Acquisition Corp.  ',
     'LOCL':'Local Bounti Corporation ',
     'LOCO':'El Pollo Loco Holdings Inc. ',
     'LODE':'Comstock Inc. ',
     'LOGI':'Logitech International S.A. ',
     'LOMA':'Loma Negra Compania Industrial Argentina Sociedad Anonima ADS',
     'LOOP':'Loop Industries Inc. ',
     'LOPE':'Grand Canyon Education Inc. ',
     'LOV':'Spark Networks SE ',
     'LOVE':'The Lovesac Company ',
     'LOW':'Lowes Companies Inc. ',
     'LPCN':'Lipocine Inc. ',
     'LPG':'Dorian LPG Ltd. ',
     'LPL':'LG Display Co Ltd AMERICAN DEPOSITORY SHARES',
     'LPLA':'LPL Financial Holdings Inc. ',
     'LPRO':'Open Lending Corporation ',
     'LPSN':'LivePerson Inc. ',
     'LPTH':'LightPath Technologies Inc.  ',
     'LPTV':'Loop Media Inc. ',
     'LPTX':'Leap Therapeutics Inc. ',
     'LPX':'Louisiana-Pacific Corporation ',
     'LQDA':'Liquidia Corporation ',
     'LQDT':'Liquidity Services Inc. ',
     'LRCX':'Lam Research Corporation ',
     'LRFC':'Logan Ridge Finance Corporation ',
     'LRMR':'Larimar Therapeutics Inc. ',
     'LRN':'Stride Inc. ',
     'LRLCF':'LOréal S.A. ',
     'LSAK':'Lesaka Technologies Inc. ',
     'LSBK':'Lake Shore Bancorp Inc. ',
     'LSCC':'Lattice Semiconductor Corporation ',
     'LSDI':'Lucy Scientific Discovery Inc. ',
     'LSEA':'Landsea Homes Corporation ',
     'LSEAW':'Landsea Homes Corporation ',
     'LSF':'Laird Superfood Inc. ',
     'LSI':'Life Storage Inc. ',
     'LSPD':'Lightspeed Commerce Inc. Subordinate Voting Shares',
     'LSTA':'Lisata Therapeutics Inc. ',
     'LSTR':'Landstar System Inc. ',
     'LSXMA':'Liberty Media Corporation Series A Liberty SiriusXM ',
     'LSXMB':'Liberty Media Corporation Series B Liberty SiriusXM ',
     'LSXMK':'Liberty Media Corporation Series C Liberty SiriusXM ',
     'LTBR':'Lightbridge Corporation ',
     'LTC':'LTC Properties Inc. ',
     'LTCH':'Latch Inc. ',
     'LTCHW':'Latch Inc.  expiring 6/4/2026',
     'LTH':'Life Time Group Holdings Inc. ',
     'LTHM':'Livent Corporation ',
     'LTRN':'Lantern Pharma Inc. ',
     'LTRPA':'Liberty TripAdvisor Holdings Inc. Series A ',
     'LTRPB':'Liberty TripAdvisor Holdings Inc. Series B ',
     'LTRX':'Lantronix Inc. ',
     'LTRY':'Lottery.com Inc. ',
     'LTRYW':'Lottery.com Inc. s',
     'LU':'Lufax Holding Ltd  two of which representing one ',
     'LUCD':'Lucid Diagnostics Inc. ',
     'LUCY':'Innovative Eyewear Inc. ',
     'LUCYW':'Innovative Eyewear Inc. Series A s',
     'LULU':'lululemon athletica inc. ',
     'LUMN':'Lumen Technologies Inc. ',
     'LUMO':'Lumos Pharma Inc. ',
     'LUNA':'Luna Innovations Incorporated ',
     'LUNG':'Pulmonx Corporation ',
     'LUNR':'Intuitive Machines Inc.  ',
     'LUNRW':'Intuitive Machines Inc. s',
     'LUV':'Southwest Airlines Company ',
     'LUXH':'LuxUrban Hotels Inc. ',
     'LVLU':'Lulus Fashion Lounge Holdings Inc. ',
     'LVMHF':'LVMH Moet Hennessey-Louis Vuitton ',
     'LVO':'LiveOne Inc. ',
     'LVOX':'LiveVox Holdings Inc.  ',
     'LVOXW':'LiveVox Holdings Inc. ',
     'LVRO':'Lavoro Limited ',
     'LVROW':'Lavoro Limited ',
     'LVS':'Las Vegas Sands Corp. ',
     'LVTX':'LAVA Therapeutics N.V. ',
     'LVWR':'LiveWire Group Inc. ',
     'LW':'Lamb Weston Holdings Inc. ',
     'LWAY':'Lifeway Foods Inc. ',
     'LWLG':'Lightwave Logic Inc. ',
     'LX':'LexinFintech Holdings Ltd. ',
     'LXEH':'Lixiang Education Holding Co. Ltd. ',
     'LXFR':'Luxfer Holdings PLC ',
     'LXP':'LXP Industrial Trust  (Maryland REIT)',
     'LXRX':'Lexicon Pharmaceuticals Inc. ',
     'LXU':'LSB Industries Inc. ',
     'LYB':'LyondellBasell Industries NV   (Netherlands)',
     'LYEL':'Lyell Immunopharma Inc. ',
     'LYFT':'Lyft Inc.  ',
     'LYG':'Lloyds Banking Group Plc ',
     'LYRA':'Lyra Therapeutics Inc. ',
     'LYT':'Lytus Technologies Holdings PTV. Ltd. ',
     'LYTS':'LSI Industries Inc. ',
     'LYV':'Live Nation Entertainment Inc. ',
     'LZ':'LegalZoom.com Inc. ',
     'LZB':'La-Z-Boy Incorporated ',
     'LZM':'Lifezone Metals Limited ',
     'M':'Macys Inc ',
     'MA':'Mastercard Incorporated ',
     'MAA':'Mid-America Apartment Communities Inc. ',
     'MAC':'Macerich Company ',
     'MACA':'Moringa Acquisition Corp ',
     'MACAW':'Moringa Acquisition Corp ',
     'MACK':'Merrimack Pharmaceuticals Inc. ',
     'MAG':'MAG Silver Corporation ',
     'MAIA':'MAIA Biotechnology Inc. ',
     'MAIN':'Main Street Capital Corporation ',
     'MAN':'ManpowerGroup ',
     'MANH':'Manhattan Associates Inc. ',
     'MANU':'Manchester United Ltd. ',
     'MAPS':'WM Technology Inc.  ',
     'MAPSW':'WM Technology Inc. s',
     'MAQC':'Maquia Capital Acquisition Corporation  ',
     'MAQCU':'Maquia Capital Acquisition Corporation Unit',
     'MAR':'Marriott International  ',
     'MARA':'Marathon Digital Holdings Inc. ',
     'MARK':'Remark Holdings Inc. ',
     'MARPS':'Marine Petroleum Trust Units of Beneficial Interest',
     'MARX':'Mars Acquisition Corp. ',
     'MARXR':'Mars Acquisition Corp. Rights',
     'MAS':'Masco Corporation ',
     'MASI':'Masimo Corporation ',
     'MASS':'908 Devices Inc. ',
     'MAT':'Mattel Inc. ',
     'MATH':'Metalpha Technology Holding Limited ',
     'MATV':'Mativ Holdings Inc. ',
     'MATW':'Matthews International Corporation  ',
     'MATX':'Matson Inc. ',
     'MAV':'Pioneer Municipal High Income Advantage Fund Inc.',
     'MAX':'MediaAlpha Inc.  ',
     'MAXN':'Maxeon Solar Technologies Ltd. ',
     'MAYS':'J. W. Mays Inc. ',
     'MBAC':'M3-Brigade Acquisition II Corp.  ',
     'MBC':'MasterBrand Inc. ',
     'MBCN':'Middlefield Banc Corp. ',
     'MBI':'MBIA Inc. ',
     'MBIN':'Merchants Bancorp ',
     'MBIO':'Mustang Bio Inc. ',
     'MBLY':'Mobileye Global Inc.  ',
     'MBOT':'Microbot Medical Inc. ',
     'MBRX':'Moleculin Biotech Inc. ',
     'MBSC':'M3-Brigade Acquisition III Corp.  ',
     'MBTC':'Nocturne Acquisition Corporation ',
     'MBTCR':'Nocturne Acquisition Corporation Right',
     'MBUU':'Malibu Boats Inc.  ',
     'MBWM':'Mercantile Bank Corporation ',
     'MC':'Moelis & Company  ',
     'MCAA':'Mountain & Co. I Acquisition Corp. ',
     'MCACR':'Monterey Capital Acquisition Corporation Rights',
     'MCACW':'Monterey Capital Acquisition Corporation s',
     'MCAF':'Mountain Crest Acquisition Corp. IV ',
     'MCAFR':'Mountain Crest Acquisition Corp. IV Rights',
     'MCAG':'Mountain Crest Acquisition Corp. V ',
     'MCB':'Metropolitan Bank Holding Corp. ',
     'MCBC':'Macatawa Bank Corporation ',
     'MCBS':'MetroCity Bankshares Inc. ',
     'MCD':'McDonalds Corporation ',
     'MCFT':'MasterCraft Boat Holdings Inc. ',
     'MCHP':'Microchip Technology Incorporated ',
     'MCHX':'Marchex Inc. Class B ',
     'MCI':'Barings Corporate Investors ',
     'MCK':'McKesson Corporation ',
     'MCLD':'mCloud Technologies Corp. ',
     'MCLDW':'mCloud Technologies Corp. s',
     'MCN':'Madison Covered Call & Equity Strategy Fund ',
     'MCO':'Moodys Corporation ',
     'MCOM':'micromobility.com Inc.  ',
     'MCOMW':'micromobility.com Inc. ',
     'MCR':'MFS Charter Income Trust ',
     'MCRB':'Seres Therapeutics Inc. ',
     'MCRI':'Monarch Casino & Resort Inc. ',
     'MCS':'Marcus Corporation ',
     'MCVT':'Mill City Ventures III Ltd. ',
     'MCW':'Mister Car Wash Inc. ',
     'MCY':'Mercury General Corporation ',
     'MD':'Pediatrix Medical Group Inc. ',
     'MDB':'MongoDB Inc.  ',
     'MDC':'M.D.C. Holdings Inc. ',
     'MDGL':'Madrigal Pharmaceuticals Inc. ',
     'MDGS':'Medigus Ltd. ',
     'MDGSW':'Medigus Ltd. Series C ',
     'MDIA':'Mediaco Holding Inc.  ',
     'MDJH':'MDJM LTD ',
     'MDLZ':'Mondelez International Inc.  ',
     'MDNA':'Medicenna Therapeutics Corp. ',
     'MDRR':'Medalist Diversified REIT Inc. ',
     'MDRRP':'Medalist Diversified REIT Inc. Series A Cumulative Redeemable Preferred Stock',
     'MDRX':'Veradigm Inc. ',
     'MDT':'Medtronic plc. ',
     'MDU':'MDU Resources Group Inc.  (Holding Company)',
     'MDV':'Modiv Inc. Class C ',
     'MDVL':'MedAvail Holdings Inc. ',
     'MDWD':'MediWound Ltd. ',
     'MDWT':'Midwest Holding Inc. ',
     'MDXG':'MiMedx Group Inc ',
     'MDXH':'MDxHealth SA ',
     'ME':'23andMe Holding Co.  ',
     'MEC':'Mayville Engineering Company Inc. ',
     'MED':'MEDIFAST INC ',
     'MEDP':'Medpace Holdings Inc. ',
     'MEDS':'TRxADE HEALTH Inc. ',
     'MEG':'Montrose Environmental Group Inc. ',
     'MEGI':'MainStay CBRE Global Infrastructure Megatrends Term Fund ',
     'MEGL':'Magic Empire Global Limited ',
     'MEI':'Methode Electronics Inc. ',
     'MEIP':'MEI Pharma Inc. ',
     'MELI':'MercadoLibre Inc. ',
     'MEOH':'Methanex Corporation ',
     'MERC':'Mercer International Inc. ',
     'MESA':'Mesa Air Group Inc. ',
     'MESO':'Mesoblast Limited ',
     'MET':'MetLife Inc. ',
     'META':'Meta Platforms Inc.  ',
     'METC':'Ramaco Resources Inc.  ',
     'METCB':'Ramaco Resources Inc. Class B ',
     'METX':'Meten Holding Group Ltd. ',
     'METXW':'Meten Holding Group Ltd. ',
     'MF':'Missfresh Limited ',
     'MFA':'MFA Financial Inc.',
     'MFC':'Manulife Financial Corporation ',
     'MFD':'Macquarie First Trust Global ',
     'MFG':'Mizuho Financial Group Inc. Sponosred ADR (Japan)',
     'MFH':'Mercurity Fintech Holding Inc. ',
     'MFIC':'MidCap Financial Investment Corporation ',
     'MFIN':'Medallion Financial Corp. ',
     'MFM':'MFS Municipal Income Trust ',
     'MFV':'MFS Special Value Trust ',
     'MG':'Mistras Group Inc ',
     'MGA':'Magna International Inc. ',
     'MGAM':'Mobile Global Esports Inc. ',
     'MGEE':'MGE Energy Inc',
     'MGF':'MFS Government Markets Income Trust ',
     'MGIC':'Magic Software Enterprises Ltd. ',
     'MGIH':'Millennium Group International Holdings Limited ',
     'MGLD':'The Marygold Companies Inc. ',
     'MGM':'MGM Resorts International ',
     'MGNI':'Magnite Inc. ',
     'MGNX':'MacroGenics Inc. ',
     'MGOL':'MGO Global Inc. ',
     'MGPI':'MGP Ingredients Inc.',
     'MGRC':'McGrath RentCorp ',
     'MGRM':'Monogram Orthopaedics Inc. ',
     'MGRX':'Mangoceuticals Inc. ',
     'MGTA':'Magenta Therapeutics Inc. ',
     'MGTX':'MeiraGTx Holdings plc ',
     'MGY':'Magnolia Oil & Gas Corporation  ',
     'MGYR':'Magyar Bancorp Inc. ',
     'MHD':'Blackrock MuniHoldings Fund Inc. ',
     'MHF':'Western Asset Municipal High Income Fund Inc. ',
     'MHH':'Mastech Digital Inc ',
     'MHI':'Pioneer Municipal High Income Fund Inc.',
     'MHK':'Mohawk Industries Inc. ',
     'MHLD':'Maiden Holdings Ltd.',
     'MHN':'Blackrock MuniHoldings New York Quality Fund Inc. ',
     'MHO':'M/I Homes Inc. ',
     'MHUA':'Meihua International Medical Technologies Co. Ltd. ',
     'MICS':'The Singing Machine Company Inc. ',
     'MIDD':'Middleby Corporation ',
     'MIGI':'Mawson Infrastructure Group Inc. ',
     'MIMO':'Airspan Networks Holdings Inc. ',
     'MIN':'MFS Intermediate Income Trust ',
     'MIND':'MIND Technology Inc.  (DE)',
     'MINM':'Minim Inc. ',
     'MIO':'Pioneer Municipal High Income Opportunities Fund Inc. ',
     'MIR':'Mirion Technologies Inc.  ',
     'MIRM':'Mirum Pharmaceuticals Inc. ',
     'MIRO':'Miromatrix Medical Inc. ',
     'MIST':'Milestone Pharmaceuticals Inc. ',
     'MITA':'Coliseum Acquisition Corp.',
     'MITAU':'Coliseum Acquisition Corp. Unit',
     'MITAW':'Coliseum Acquisition Corp. ',
     'MITK':'Mitek Systems Inc. ',
     'MITQ':'Moving iMage Technologies Inc. ',
     'MITT':'AG Mortgage Investment Trust Inc. ',
     'MIXT':'MiX Telematics Limited  each representing 25 ',
     'MIY':'Blackrock MuniYield Michigan Quality Fund Inc. ',
     'MKC':'McCormick & Company Incorporated ',
     'MKFG':'Markforged Holding Corporation ',
     #'MKGAF':'MERCK KgaA.', 
     'MKL':'Markel Group Inc. ',
     'MKSI':'MKS Instruments Inc. ',
     'MKTW':'MarketWise Inc.  ',
     'MKTX':'MarketAxess Holdings Inc. ',
     'MKUL':'Molekule Group Inc. ',
     'ML':'MoneyLion Inc.  ',
     'MLAB':'Mesa Laboratories Inc. ',
     'MLCO':'Melco Resorts & Entertainment Limited ',
     'MLEC':'Moolec Science SA ',
     'MLECW':'Moolec Science SA ',
     'MLGO':'MicroAlgo Inc. ',
     'MLI':'Mueller Industries Inc. ',
     'MLKN':'MillerKnoll Inc. ',
     'MLM':'Martin Marietta Materials Inc. ',
     'MLNK':'MeridianLink Inc. ',
     'MLP':'Maui Land & Pineapple Company Inc. ',
     'MLR':'Miller Industries Inc. ',
     'MLSS':'Milestone Scientific Inc. ',
     'MLTX':'MoonLake Immunotherapeutics ',
     'MLVF':'Malvern Bancorp Inc. ',
     'MLYS':'Mineralys Therapeutics Inc. ',
     'MMAT':'Meta Materials Inc. ',
     'MMC':'Marsh & McLennan Companies Inc. ',
     'MMD':'MainStay MacKay DefinedTerm Municipal Opportunities Fund',
     'MMI':'Marcus & Millichap Inc. ',
     'MMLP':'Martin Midstream Partners L.P. Limited Partnership',
     'MMM':'3M Company ',
     'MMMB':'MamaMancinis Holdings Inc. ',
     'MMP':'Magellan Midstream Partners L.P. Limited Partnership',
     'MMS':'Maximus Inc. ',
     'MMSI':'Merit Medical Systems Inc. ',
     'MMT':'MFS Multimarket Income Trust ',
     'MMU':'Western Asset Managed Municipals Fund Inc. ',
     'MMV':'MultiMetaVerse Holdings Limited',
     'MMVWW':'MultiMetaVerse Holdings Limited ',
     'MMYT':'MakeMyTrip Limited ',
     'MNDO':'MIND C.T.I. Ltd. ',
     'MNDY':'monday.com Ltd. ',
     'MNK':'Mallinckrodt plc ',
     'MNKD':'MannKind Corporation ',
     'MNMD':'Mind Medicine (MindMed) Inc. ',
     'MNOV':'Medicinova Inc ',
     'MNP':'Western Asset Municipal Partners Fund Inc. ',
     'MNPR':'Monopar Therapeutics Inc. ',
     'MNRO':'Monro Inc. ',
     'MNSB':'MainStreet Bancshares Inc. ',
     'MNSO':'MINISO Group Holding Limited  each representing four ',
     'MNST':'Monster Beverage Corporation',
     'MNTK':'Montauk Renewables Inc. ',
     'MNTN':'Everest Consolidator Acquisition Corporation  ',
     'MNTS':'Momentus Inc.  ',
     'MNTSW':'Momentus Inc. ',
     'MNTX':'Manitex International Inc. ',
     'MO':'Altria Group Inc.',
     'MOB':'Mobilicom Limited ',
     'MOBBW':'Mobilicom Limited s',
     'MOBQ':'Mobiquity Technologies Inc. ',
     'MOBQW':'Mobiquity Technologies Inc. ',
     'MOBV':'Mobiv Acquisition Corp  ',
     'MOBVU':'Mobiv Acquisition Corp Unit',
     'MOBVW':'Mobiv Acquisition Corp ',
     'MOD':'Modine Manufacturing Company ',
     'MODD':'Modular Medical Inc. ',
     'MODG':'Topgolf Callaway Brands Corp. ',
     'MODN':'Model N Inc. ',
     'MODV':'ModivCare Inc. ',
     'MOFG':'MidWestOne Financial Gp ',
     'MOGO':'Mogo Inc. ',
     'MOGU':'MOGU Inc.  (each  representing 25 )',
     'MOH':'Molina Healthcare Inc ',
     'MOLN':'Molecular Partners AG ',
     'MOMO':'Hello Group Inc. ',
     'MOND':'Mondee Holdings Inc.  ',
     'MOR':'MorphoSys AG ',
     'MORF':'Morphic Holding Inc. ',
     'MORN':'Morningstar Inc. ',
     'MOS':'Mosaic Company ',
     'MOTS':'Motus GI Holdings Inc. ',
     'MOV':'Movado Group Inc. ',
     'MOVE':'Movano Inc. ',
     'MOXC':'Moxian (BVI) Inc ',
     'MP':'MP Materials Corp. ',
     'MPA':'Blackrock MuniYield Pennsylvania Quality Fund ',
     'MPAA':'Motorcar Parts  of America Inc. ',
     'MPB':'Mid Penn Bancorp ',
     'MPC':'Marathon Petroleum Corporation ',
     'MPLN':'MultiPlan Corporation  ',
     'MPLX':'MPLX LP Common Units Representing Limited Partner Interests',
     'MPRA':'Mercato Partners Acquisition Corporation  ',
     'MPRAW':'Mercato Partners Acquisition Corporation ',
     'MPTI':'M-tron Industries Inc. ',
     'MPU':'Mega Matrix Corp. ',
     'MPV':'Barings Participation Investors ',
     'MPW':'Medical Properties Trust Inc. ',
     'MPWR':'Monolithic Power Systems Inc. ',
     'MPX':'Marine Products Corporation ',
     'MQ':'Marqeta Inc.  ',
     'MQT':'Blackrock MuniYield Quality Fund II Inc. ',
     'MQY':'Blackrock MuniYield Quality Fund Inc. ',
     'MRAI':'Marpai Inc.  ',
     'MRAM':'Everspin Technologies Inc. ',
     'MRBK':'Meridian Corporation ',
     'MRC':'MRC Global Inc. ',
     'MRCC':'Monroe Capital Corporation ',
     'MRCY':'Mercury Systems Inc ',
     'MRDB':'MariaDB plc ',
     'MREO':'Mereo BioPharma Group plc ',
     'MRIN':'Marin Software Incorporated ',
     'MRK':'Merck & Company Inc.',
     'MRKR':'Marker Therapeutics Inc. ',
     'MRM':'MEDIROM Healthcare Technologies Inc. ',
     'MRNA':'Moderna Inc. ',
     'MRNS':'Marinus Pharmaceuticals Inc. ',
     'MRO':'Marathon Oil Corporation ',
     'MRSN':'Mersana Therapeutics Inc. ',
     'MRTN':'Marten Transport Ltd. ',
     'MRTX':'Mirati Therapeutics Inc. ',
     'MRUS':'Merus N.V. ',
     'MRVI':'Maravai LifeSciences Holdings Inc.  ',
     'MRVL':'Marvell Technology Inc. ',
     'MS':'Morgan Stanley ',
     'MSA':'MSA Safety Incorporated ',
     'MSB':'Mesabi Trust ',
     'MSBI':'Midland States Bancorp Inc. ',
     'MSC':'Studio City International Holdings Limited  each representing four  ',
     'MSCI':'MSCI Inc. ',
     'MSEX':'Middlesex Water Company ',
     'MSFT':'Microsoft Corporation ',
     'MSGE':'Madison Square Garden Entertainment Corp.  ',
     'MSGM':'Motorsport Games Inc.  ',
     'MSGS':'Madison Square Garden Sports Corp.',
     'MSI':'Motorola Solutions Inc. ',
     'MSM':'MSC Industrial Direct Company Inc. ',
     'MSN':'Emerson Radio Corporation ',
     'MSSA':'Metal Sky Star Acquisition Corporation ',
     'MSSAU':'Metal Sky Star Acquisition Corporation Unit',
     'MSSAW':'Metal Sky Star Acquisition Corporation ',
     'MSTR':'MicroStrategy Incorporated  ',
     'MSVB':'Mid-Southern Bancorp Inc. ',
     'MT':'Arcelor Mittal NY Registry Shares NEW',
     'MTA':'Metalla Royalty & Streaming Ltd. ',
     'MTAC':'MedTech Acquisition Corporation  ',
     'MTACW':'MedTech Acquisition Corporation ',
     'MTAL':'Metals Acquisition Limited ',
     'MTB':'M&T Bank Corporation ',
     'MTBL':'Moatable Inc.  (each representing forty-five (45) )',
     'MTC':'MMTec Inc. ',
     'MTCH':'Match Group Inc. ',
     'MTD':'Mettler-Toledo International Inc. ',
     'MTDR':'Matador Resources Company ',
     'MTEK':'Maris-Tech Ltd. ',
     'MTEKW':'Maris-Tech Ltd. s',
     'MTEM':'Molecular Templates Inc. ',
     'MTEX':'Mannatech Incorporated ',
     'MTG':'MGIC Investment Corporation ',
     'MTH':'Meritage Homes Corporation ',
     'MTLS':'Materialise NV ',
     'MTN':'Vail Resorts Inc. ',
     'MTNB':'Matinas Biopharma Holdings Inc. ',
     'MTR':'Mesa Royalty Trust ',
     'MTRN':'Materion Corporation',
     'MTRX':'Matrix Service Company ',
     'MTSI':'MACOM Technology Solutions Holdings Inc. ',
     'MTTR':'Matterport Inc.  ',
     'MTW':'Manitowoc Company Inc. ',
     'MTX':'Minerals Technologies Inc. ',
     'MTZ':'MasTec Inc. ',
     'MU':'Micron Technology Inc. ',
     'MUA':'Blackrock MuniAssets Fund Inc ',
     'MUFG':'Mitsubishi UFJ Financial Group Inc. ',
     'MUI':'BlackRock Municipal Income Fund Inc. ',
     'MULN':'Mullen Automotive Inc. ',
     'MUR':'Murphy Oil Corporation ',
     'MURF':'Murphy Canyon Acquisition Corp.  ',
     'MUSA':'Murphy USA Inc. ',
     'MUX':'McEwen Mining Inc. ',
     'MVBF':'MVB Financial Corp. ',
     'MVF':'Blackrock MuniVest Fund Inc. ',
     'MVIS':'MicroVision Inc. ',
     'MVLA':'Movella Holdings Inc. ',
     'MVLAW':'Movella Holdings Inc. ',
     'MVO':'MV Oil Trust Units of Beneficial Interests',
     'MVST':'Microvast Holdings Inc. ',
     'MVSTW':'Microvast Holdings Inc. s',
     'MVT':'Blackrock MuniVest Fund II Inc.  ',
     'MWA':'MUELLER WATER PRODUCTS ',
     'MWG':'Multi Ways Holdings Limited ',
     'MX':'Magnachip Semiconductor Corporation ',
     'MXC':'Mexco Energy Corporation ',
     'MXCT':'MaxCyte Inc. ',
     'MXE':'Mexico Equity and Income Fund Inc. ',
     'MXF':'Mexico Fund Inc. ',
     'MXL':'MaxLinear Inc. ',
     'MYD':'Blackrock MuniYield Fund Inc.  ',
     'MYE':'Myers Industries Inc. ',
     'MYFW':'First Western Financial Inc. ',
     'MYGN':'Myriad Genetics Inc. ',
     'MYI':'Blackrock MuniYield Quality Fund III Inc ',
     'MYMD':'MyMD Pharmaceuticals Inc. ',
     'MYN':'Blackrock MuniYield New York Quality Fund Inc.',
     'MYNA':'Mynaric AG American Depository Shares',
     'MYNZ':'Mainz Biomed N.V. ',
     'MYO':'Myomo Inc. ',
     'MYPS':'PLAYSTUDIOS Inc.   ',
     'MYPSW':'PLAYSTUDIOS Inc. ',
     'MYRG':'MYR Group Inc. ',
     'MYSZ':'My Size Inc. ',
     'MYTE':'MYT Netherlands Parent B.V.  each representing one ',
     'NA':'Nano Labs Ltd ',
     'NAAS':'NaaS Technology Inc. ',
     'NABL':'N-able Inc. ',
     'NAC':'Nuveen California Quality Municipal Income Fund',
     'NAD':'Nuveen Quality Municipal Income Fund ',
     'NAII':'Natural Alternatives International Inc. ',
     'NAK':'Northern Dynasty Minerals Ltd. ',
     'NAMS':'NewAmsterdam Pharma Company N.V. ',
     'NAMSW':'NewAmsterdam Pharma Company N.V. ',
     'NAN':'Nuveen New York Quality Municipal Income Fund ',
     'NAOV':'NanoVibronix Inc. ',
     'NAPA':'The Duckhorn Portfolio Inc. ',
     'NARI':'Inari Medical Inc. ',
     'NAT':'Nordic American Tankers Limited ',
     'NATH':'Nathans Famous Inc. ',
     'NATI':'National Instruments Corporation ',
     'NATR':'Natures Sunshine Products Inc. ',
     'NAUT':'Nautilus Biotechnolgy Inc. ',
     'NAVB':'Navidea Biopharmaceuticals Inc. ',
     'NAVI':'Navient Corporation ',
     'NAZ':'Nuveen Arizona Quality Municipal Income Fund ',
     'NB':'NioCorp Developments Ltd. ',
     'NBB':'Nuveen Taxable Municipal Income Fund  of Beneficial Interest',
     'NBH':'Neuberger Berman Municipal Fund Inc. ',
     'NBHC':'National Bank Holdings Corporation ',
     'NBIX':'Neurocrine Biosciences Inc. ',
     'NBN':'Northeast Bank ',
     'NBO':'Neuberger Berman New York Municipal Fund Inc. ',
     'NBR':'Nabors Industries Ltd.',
     'NBRV':'Nabriva Therapeutics plc  Ireland',
     'NBSE':'NeuBase Therapeutics Inc.  ',
     'NBST':'Newbury Street Acquisition Corporation ',
     'NBSTU':'Newbury Street Acquisition Corporation Units',
     'NBSTW':'Newbury Street Acquisition Corporation s',
     'NBTB':'NBT Bancorp Inc. ',
     'NBTX':'Nanobiotix S.A. ',
     'NBW':'Neuberger Berman California Municipal Fund Inc ',
     'NBXG':'Neuberger Berman Next Generation Connectivity Fund Inc. ',
     'NBY':'NovaBay Pharmaceuticals Inc. ',
     'NC':'NACCO Industries Inc. ',
     'NCA':'Nuveen California Municipal Value Fund',
     'NCAC':'Newcourt Acquisition Corp',
     'NCACW':'Newcourt Acquisition Corp ',
     'NCLH':'Norwegian Cruise Line Holdings Ltd. ',
     'NCMI':'National CineMedia Inc. ',
     'NCNA':'NuCana plc ',
     'NCNO':'nCino Inc. ',
     'NCPL':'Netcapital Inc. ',
     'NCR':'NCR Corporation ',
     'NCRA':'Nocera Inc. ',
     'NCSM':'NCS Multistage Holdings Inc. ',
     'NCTY':'The9 Limited American Depository Shares',
     'NDAQ':'Nasdaq Inc. ',
     'NDLS':'Noodles & Company  ',
     'NDMO':'Nuveen Dynamic Municipal Opportunities Fund  of Beneficial Interest',
     'NDP':'Tortoise Energy Independence Fund Inc. ',
     'NDRA':'ENDRA Life Sciences Inc. ',
     #'NIABY':'NIBE Industrier AB ',
     'NDSN':'Nordson Corporation ',
     'NE':'Noble Corporation plc A ',
     'NEA':'Nuveen AMT-Free Quality Municipal Income Fund  of Beneficial Interest Par Value $.01',
     'NECB':'NorthEast Community Bancorp Inc. ',
     'NEE':'NextEra Energy Inc. ',
     'NEGG':'Newegg Commerce Inc. ',
     'NEM':'Newmont Corporation',
     'NEN':'New England Realty Associates Limited Partnership  Depositary Receipts Evidencing Units of Limited Partnership',
     'NEO':'NeoGenomics Inc. ',
     'NEOG':'Neogen Corporation ',
     'NEON':'Neonode Inc. ',
     'NEOV':'NeoVolta Inc. ',
     'NEOVW':'NeoVolta Inc. ',
     'NEP':'NextEra Energy Partners LP Common Units representing limited partner interests',
     'NEPH':'Nephros Inc. ',
     'NEPT':'Neptune Wellness Solutions Inc. ',
     'NERV':'Minerva Neurosciences Inc ',
     'NET':'Cloudflare Inc.  ',
     'NETC':'Nabors Energy Transition Corp.  ',
     'NETI':'Eneti Inc. ',
     'NEU':'NewMarket Corp ',
     'NEWP':'New Pacific Metals Corp. ',
     'NEWR':'New Relic Inc. ',
     'NEWT':'NewtekOne Inc. ',
     'NEX':'NexTier Oilfield Solutions Inc. ',
     'NEXA':'Nexa Resources S.A. ',
     'NEXI':'NexImmune Inc. ',
     'NEXT':'NextDecade Corporation ',
     'NFBK':'Northfield Bancorp Inc.  (Delaware)',
     'NFE':'New Fortress Energy Inc.  ',
     'NFG':'National Fuel Gas Company ',
     'NFGC':'New Found Gold Corp ',
     'NFJ':'Virtus Dividend Interest & Premium Strategy Fund  of Beneficial Interest',
     'NFLX':'Netflix Inc. ',
     'NFNT':'Infinite Acquisition Corp. ',
     'NFTG':'The NFT Gaming Company Inc. ',
     'NFYS':'Enphys Acquisition Corp. ',
     'NG':'Novagold Resources Inc.',
     'NGD':'New Gold Inc.',
     'NGG':'National Grid Transco PLC National Grid PLC (NEW) ',
     'NGL':'NGL ENERGY PARTNERS LP Common Units representing Limited Partner Interests',
     'NGM':'NGM Biopharmaceuticals Inc. ',
     'NGMS':'NeoGames S.A. ',
     'NGS':'Natural Gas Services Group Inc. ',
     'NGVC':'Natural Grocers by Vitamin Cottage Inc. ',
     'NGVT':'Ingevity Corporation ',
     'NHC':'National HealthCare Corporation ',
     'NHI':'National Health Investors Inc. ',
     'NHS':'Neuberger Berman High Yield Strategies Fund',
     'NHTC':'Natural Health Trends Corp. ',
     'NHWK':'NightHawk Biosciences Inc. ',
     'NI':'NiSource Inc ',
     'NIC':'Nicolet Bankshares Inc. ',
     'NICE':'NICE Ltd ',
     'NICK':'Nicholas Financial Inc. ',
     'NIE':'Virtus Equity & Convertible Income Fund  of Beneficial Interest',
     'NIM':'Nuveen Select Maturities Municipal Fund ',
     'NIMC':'NiSource Inc Series A Corporate Units',
     'NINE':'Nine Energy Service Inc. ',
     'NIO':'NIO Inc.',
     'NIOBW':'NioCorp Developments Ltd. ',
     'NIR':'Near Intelligence Inc. ',
     'NIRWW':'Near Intelligence Inc. ',
     'NISN':'NiSun International Enterprise Development Group Co. Ltd.  ',
     'NIU':'Niu Technologies ',
     'NJR':'NewJersey Resources Corporation ',
     'NKE':'Nike Inc. ',
     'NKLA':'Nikola Corporation ',
     'NKSH':'National Bankshares Inc. ',
     'NKTR':'Nektar Therapeutics  ',
     'NKTX':'Nkarta Inc. ',
     'NKX':'Nuveen California AMT-Free Quality Municipal Income Fund',
     'NL':'NL Industries Inc. ',
     'NLS':'Nautilus Inc. ',
     'NLSP':'NLS Pharmaceutics Ltd. ',
     'NLSPW':'NLS Pharmaceutics Ltd. ',
     'NLTX':'Neoleukin Therapeutics Inc. ',
     'NLY':'Annaly Capital Management Inc. ',
     'NM':'Navios Maritime Holdings Inc. ',
     'NMAI':'Nuveen Multi-Asset Income Fund  of Beneficial Interest',
     'NMCO':'Nuveen Municipal Credit Opportunities Fund ',
     'NMFC':'New Mountain Finance Corporation ',
     'NMG':'Nouveau Monde Graphite Inc. ',
     'NMI':'Nuveen Municipal Income Fund Inc. ',
     'NMIH':'NMI Holdings Inc.  ',
     'NML':'Neuberger Berman Energy Infrastructure and Income Fund Inc. ',
     'NMM':'Navios Maritime Partners LP Common Units Representing Limited Partner Interests',
     'NMR':'Nomura Holdings Inc ADR ',
     'NMRD':'Nemaura Medical Inc. ',
     'NMRK':'Newmark Group Inc.  ',
     'NMS':'Nuveen Minnesota Quality Municipal Income Fund',
     'NMT':'Nuveen Massachusetts Quality Municipal Income Fund ',
     'NMTC':'NeuroOne Medical Technologies Corporation ',
     'NMTR':'9 Meters Biopharma Inc. ',
     'NMZ':'Nuveen Municipal High Income Opportunity Fund  $0.01 par value per share',
     'NN':'NextNav Inc. ',
     'NNAVW':'NextNav Inc. ',
     'NNBR':'NN Inc. ',
     'NNDM':'Nano Dimension Ltd. ',
     'NNI':'Nelnet Inc. ',
     'NNN':'NNN REIT Inc. ',
     'NNOX':'NANO-X IMAGING LTD ',
     'NNVC':'NanoViricides Inc. ',
     'NNY':'Nuveen New York Municipal Value Fund ',
     'NOA':'North American Construction Group Ltd.  (no par)',
     'NOAH':'Noah Holdings Limited',
     'NOC':'Northrop Grumman Corporation ',
     'NODK':'NI Holdings Inc. ',
     'NOG':'Northern Oil and Gas Inc. ',
     'NOGN':'Nogin Inc. ',
     'NOGNW':'Nogin Inc. ',
     'NOK':'Nokia Corporation Sponsored ',
     'NOM':'Nuveen Missouri Quality Municipal Income Fund',
     'NOMD':'Nomad Foods Limited ',
     'NOTE':'FiscalNote Holdings Inc.  ',
     'NOTV':'Inotiv Inc. ',
     'NOV':'NOV Inc. ',
     'NOVA':'Sunnova Energy International Inc. ',
     'NOVN':'Novan Inc. ',
     'NOVT':'Novanta Inc. ',
     'NOVV':'Nova Vision Acquisition Corp. ',
     'NOVVR':'Nova Vision Acquisition Corp. Rights',
     'NOVVW':'Nova Vision Acquisition Corp. ',
     'NOW':'ServiceNow Inc. ',
     'NPAB':'New Providence Acquisition Corp. II  ',
     'NPCE':'Neuropace Inc. ',
     'NPCT':'Nuveen Core Plus Impact Fund  of Beneficial Interest',
     'NPFD':'Nuveen Variable Rate Preferred & Income Fund ',
     'NPK':'National Presto Industries Inc. ',
     'NPO':'EnPro Industries Inc',
     'NPV':'Nuveen Virginia Quality Municipal Income Fund ',
     'NPWR':'NET Power Inc.  ',
     'NQP':'Nuveen Pennsylvania Quality Municipal Income Fund ',
     'NR':'Newpark Resources Inc. ',
     'NRAC':'Northern Revival Acquisition Corporation',
     'NRACW':'Northern Revival Acquisition Corporation ',
     'NRBO':'NeuroBo Pharmaceuticals Inc. ',
     'NRC':'National Research Corporation  (Delaware)',
     'NRDS':'NerdWallet Inc.  ',
     'NRDY':'Nerdy Inc.  ',
     'NREF':'NexPoint Real Estate Finance Inc. ',
     'NRG':'NRG Energy Inc. ',
     'NRGV':'Energy Vault Holdings Inc. ',
     'NRGX':'PIMCO Energy and Tactical Credit Opportunities Fund  of Beneficial Interest',
     'NRIM':'Northrim BanCorp Inc ',
     'NRIX':'Nurix Therapeutics Inc. ',
     'NRK':'Nuveen New York AMT-Free Quality Municipal Income Fund',
     'NRO':'Neuberger Berman Real Estate Securities Income Fund Inc. Neuberger Berman Real Estate Securities Income Fund Inc.',
     'NRP':'Natural Resource Partners LP Limited Partnership',
     'NRSN':'NeuroSense Therapeutics Ltd. ',
     'NRSNW':'NeuroSense Therapeutics Ltd. ',
     'NRT':'North European Oil Royality Trust ',
     'NRUC':'National Rural Utilities Cooperative Finance Corporation )',
     'NRXP':'NRX Pharmaceuticals Inc. ',
     'NS':'Nustar Energy L.P.  Common Units',
     'NSA':'National Storage Affiliates Trust  of Beneficial Interest',
     'NSC':'Norfolk Southern Corporation ',
     'NSIT':'Insight Enterprises Inc. ',
     'NSL':'Nuveen Senior Income Fund ',
     'NSP':'Insperity Inc. ',
     'NSPR':'InspireMD Inc. ',
     'NSS':'NuStar Logistics L.P. ',
     'NSSC':'NAPCO Security Technologies Inc. ',
     'NSTB':'Northern Star Investment Corp. II  ',
     'NSTC':'Northern Star Investment Corp. III  ',
     'NSTG':'NanoString Technologies Inc. ',
     'NSTS':'NSTS Bancorp Inc. ',
     'NSYS':'Nortech Systems Incorporated ',
     'NTAP':'NetApp Inc. ',
     'NTB':'Bank of N.T. Butterfield & Son Limited Voting ',
     'NTCO':'Natura &Co Holding S.A. ',
     'NTCT':'NetScout Systems Inc. ',
     'NTDOF':'Nintendo Co. Ltd.', 
     'NTES':'NetEase Inc. ',
     'NTG':'Tortoise Midstream Energy Fund Inc. ',
     'NTGR':'NETGEAR Inc. ',
     'NTIC':'Northern Technologies International Corporation ',
     'NTIP':'Network-1 Technologies Inc. ',
     'NTLA':'Intellia Therapeutics Inc. ',
     'NTNX':'Nutanix Inc.  ',
     'NTR':'Nutrien Ltd. ',
     'NTRA':'Natera Inc. ',
     'NTRB':'Nutriband Inc. ',
     'NTRBW':'Nutriband Inc. ',
     'NTRS':'Northern Trust Corporation ',
     'NTST':'NetSTREIT Corp. ',
     'NTWK':'NetSol Technologies Inc. Common  Stock',
     'NTZ':'Natuzzi S.p.A.',
     'NU':'Nu Holdings Ltd. ',
     'NUBI':'Nubia Brand International Corp.  ',
     'NUBIW':'Nubia Brand International Corp. ',
     'NUE':'Nucor Corporation ',
     'NURO':'NeuroMetrix Inc. ',
     'NUS':'Nu Skin Enterprises Inc. ',
     'NUTX':'Nutex Health Inc. ',
     'NUV':'Nuveen Municipal Value Fund Inc. ',
     'NUVA':'NuVasive Inc. ',
     'NUVB':'Nuvation Bio Inc.  ',
     'NUVL':'Nuvalent Inc.  ',
     'NUW':'Nuveen AMT-Free Municipal Value Fund',
     'NUWE':'Nuwellis Inc. ',
     'NUZE':'NuZee Inc. ',
     'NVAC':'NorthView Acquisition Corporation ',
     'NVAX':'Novavax Inc. ',
     'NVCR':'NovoCure Limited ',
     'NVCT':'Nuvectis Pharma Inc. ',
     'NVDA':'NVIDIA Corporation ',
     'NVEC':'NVE Corporation ',
     'NVEE':'NV5 Global Inc. ',
     'NVEI':'Nuvei Corporation Subordinate Voting Shares',
     'NVFY':'Nova Lifestyle Inc. ',
     'NVG':'Nuveen AMT-Free Municipal Credit Income Fund',
     'NVGS':'Navigator Holdings Ltd.  (Marshall Islands)',
     'NVIV':'InVivo Therapeutics Holdings Corp ',
     'NVMI':'Nova Ltd. ',
     'NVNO':'enVVeno Medical Corporation ',
     'NVO':'Novo Nordisk A/S ',
     'NVOS':'Novo Integrated Sciences Inc. ',
     'NVR':'NVR Inc. ',
     'NVRI':'Enviri Corporation ',
     'NVRO':'Nevro Corp. ',
     'NVS':'Novartis AG ',
     'NVST':'Envista Holdings Corporation ',
     'NVT':'nVent Electric plc ',
     'NVTA':'Invitae Corporation ',
     'NVTS':'Navitas Semiconductor Corporation ',
     'NVVE':'Nuvve Holding Corp. ',
     'NVVEW':'Nuvve Holding Corp. ',
     'NVX':'NOVONIX Limited American Depository Shares',
     'NWBI':'Northwest Bancshares Inc. ',
     'NWE':'NorthWestern Corporation ',
     'NWFL':'Norwood Financial Corp. ',
     'NWG':'NatWest Group plc  (each representing two (2) )',
     'NWL':'Newell Brands Inc. ',
     'NWLI':'National Western Life Group Inc.  ',
     'NWN':'Northwest Natural Holding Company ',
     'NWPX':'Northwest Pipe Company ',
     'NWS':'News Corporation Class B ',
     'NWSA':'News Corporation  ',
     'NWTN':'NWTN Inc. Class B ',
     'NWTNW':'NWTN Inc. ',
     'NX':'Quanex Building Products Corporation ',
     'NXC':'Nuveen California Select Tax-Free Income Portfolio ',
     'NXDT':'NexPoint Diversified Real Estate Trust ',
     'NXE':'Nexgen Energy Ltd. ',
     'NXG':'NXG NextGen Infrastructure Income Fund  of Beneficial Interest',
     'NXGL':'NexGel Inc ',
     'NXGLW':'NexGel Inc ',
     'NXGN':'NextGen Healthcare Inc. ',
     'NXJ':'Nuveen New Jersey Qualified Municipal Fund',
     'NXL':'Nexalin Technology Inc. ',
     'NXLIW':'Nexalin Technology Inc. ',
     'NXN':'Nuveen New York Select Tax-Free Income Portfolio ',
     'NXP':'Nuveen Select Tax Free Income Portfolio ',
     'NXPI':'NXP Semiconductors N.V. ',
     'NXPL':'NextPlat Corp ',
     'NXPLW':'NextPlat Corp s',
     'NXRT':'NexPoint Residential Trust Inc. ',
     'NXST':'Nexstar Media Group Inc. ',
     'NXT':'Nextracker Inc.  ',
     'NXTC':'NextCure Inc. ',
     'NXTP':'NextPlay Technologies Inc. ',
     'NXU':'Nxu Inc.  ',
     'NYAX':'Nayax Ltd. ',
     'NYC':'American Strategic Investment Co.  ',
     'NYCB':'New York Community Bancorp Inc. ',
     'NYMT':'New York Mortgage Trust Inc. ',
     'NYT':'New York Times Company ',
     'NYXH':'Nyxoah SA ',
     'NZF':'Nuveen Municipal Credit Income Fund',
     'O':'Realty Income Corporation ',
     'OABI':'OmniAb Inc. ',
     'OABIW':'OmniAb Inc. ',
     'OAKU':'Oak Woods Acquisition Corporation ',
     'OB':'Outbrain Inc. ',
     'OBDC':'Blue Owl Capital Corporation ',
     'OBE':'Obsidian Energy Ltd. ',
     'OBIO':'Orchestra BioMed Holdings Inc. ',
     'OBK':'Origin Bancorp Inc. ',
     'OBLG':'Oblong Inc. ',
     'OBT':'Orange County Bancorp Inc. ',
     'OC':'Owens Corning Inc  New',
     'OCAX':'OCA Acquisition Corp.  ',
     'OCAXU':'OCA Acquisition Corp. Unit',
     'OCAXW':'OCA Acquisition Corp. ',
     'OCC':'Optical Cable Corporation ',
     'OCCI':'OFS Credit Company Inc. ',
     'OCEA':'Ocean Biomedical Inc. ',
     'OCEAW':'Ocean Biomediacal Inc. s',
     'OCFC':'OceanFirst Financial Corp. ',
     'OCFCP':'OceanFirst Financial Corp. Depositary Shares',
     'OCFT':'OneConnect Financial Technology Co. Ltd.  each representing thirty ',
     'OCG':'Oriental Culture Holding LTD ',
     'OCGN':'Ocugen Inc. ',
     'OCN':'Ocwen Financial Corporation NEW ',
     'OCS':'Oculis Holding AG ',
     'OCSAW':'Oculis Holding AG s',
     'OCSL':'Oaktree Specialty Lending Corporation ',
     'OCTO':'Eightco Holdings Inc. ',
     'OCUL':'Ocular Therapeutix Inc. ',
     'OCUP':'Ocuphire Pharma Inc. ',
     'OCX':'Oncocyte Corporation ',
     'ODC':'Oil-Dri Corporation Of America ',
     'ODFL':'Old Dominion Freight Line Inc. ',
     'ODP':'The ODP Corporation ',
     'ODV':'Osisko Development Corp. ',
     'ODVWW':'Osisko Development Corp. ',
     'OEC':'Orion S.A. ',
     'OESX':'Orion Energy Systems Inc. ',
     'OFC':'Corporate Office Properties Trust ',
     'OFED':'Oconee Federal Financial Corp. ',
     'OFG':'OFG Bancorp ',
     'OFIX':'Orthofix Medical Inc.  (DE)',
     'OFLX':'Omega Flex Inc. ',
     'OFS':'OFS Capital Corporation ',
     'OGE':'OGE Energy Corp ',
     'OGEN':'Oragenics Inc. ',
     'OGI':'Organigram Holdings Inc. ',
     'OGN':'Organon & Co. ',
     'OGS':'ONE Gas Inc. ',
     'OHAAW':'OPY Acquisition Corp. I ',
     'OHI':'Omega Healthcare Investors Inc. ',
     'OI':'O-I Glass Inc. ',
     'OIA':'Invesco Municipal Income Opportunities Trust ',
     'OIG':'Orbital Infrastructure Group Inc. ',
     'OII':'Oceaneering International Inc. ',
     'OIS':'Oil States International Inc. ',
     'OKE':'ONEOK Inc. ',
     'OKTA':'Okta Inc.  ',
     'OKYO':'OKYO Pharma Limited ',
     'OLB':'The OLB Group Inc. ',
     'OLED':'Universal Display Corporation ',
     'OLITU':'OmniLit Acquisition Corp. Units',
     'OLITW':'OmniLit Acquisition Corp. s.',
     'OLK':'Olink Holding AB (publ) ',
     'OLLI':'Ollies Bargain Outlet Holdings Inc. ',
     'OLMA':'Olema Pharmaceuticals Inc. ',
     'OLN':'Olin Corporation ',
     'OLO':'Olo Inc.  ',
     'OLP':'One Liberty Properties Inc. ',
     'OLPX':'Olaplex Holdings Inc. ',
     'OLYMY':'Olympus Corp. ',
     'OM':'Outset Medical Inc. ',
     'OMAB':'Grupo Aeroportuario del Centro Norte S.A.B. de C.V. ADS',
     'OMC':'Omnicom Group Inc. ',
     'OMCL':'Omnicell Inc.  ($0.001 par value)',
     'OMER':'Omeros Corporation ',
     'OMEX':'Odyssey Marine Exploration Inc. ',
     'OMF':'OneMain Holdings Inc. ',
     'OMGA':'Omega Therapeutics Inc. ',
     'OMH':'Ohmyhome Limited ',
     'OMI':'Owens & Minor Inc. ',
     'OMIC':'Singular Genomics Systems Inc. ',
     'OMQS':'OMNIQ Corp. ',
     'ON':'ON Semiconductor Corporation ',
     'ONB':'Old National Bancorp ',
     'ONCT':'Oncternal Therapeutics Inc. ',
     'ONCY':'Oncolytics Biotech Inc. ',
     'ONDS':'Ondas Holdings Inc. ',
     'ONEW':'OneWater Marine Inc.  ',
     'ONFO':'Onfolio Holdings Inc. ',
     'ONFOW':'Onfolio Holdings Inc. ',
     'ONL':'Orion Office REIT Inc. ',
     'ONON':'On Holding AG ',
     'ONTF':'ON24 Inc. ',
     'ONTO':'Onto Innovation Inc. ',
     'ONTX':'Onconova Therapeutics Inc. ',
     'ONVO':'Organovo Holdings Inc. ',
     'ONYX':'Onyx Acquisition Co. I ',
     'ONYXU':'Onyx Acquisition Co. I Unit',
     'ONYXW':'Onyx Acquisition Co. I ',
     'OOMA':'Ooma Inc. ',
     'OP':'OceanPal Inc. ',
     'OPA':'Magnum Opus Acquisition Limited ',
     'OPAD':'Offerpad Solutions Inc.  ',
     'OPAL':'OPAL Fuels Inc.  ',
     'OPBK':'OP Bancorp ',
     'OPCH':'Option Care Health Inc. ',
     'OPEN':'Opendoor Technologies Inc ',
     'OPFI':'OppFi Inc.  ',
     'OPGN':'OpGen Inc. ',
     'OPHC':'OptimumBank Holdings Inc. ',
     'OPI':'Office Properties Income Trust  of Beneficial Interest',
     'OPK':'OPKO Health Inc. ',
     'OPOF':'Old Point Financial Corporation ',
     'OPP':'RiverNorth/DoubleLine Strategic Opportunity Fund Inc. ',
     'OPRA':'Opera Limited ',
     'OPRT':'Oportun Financial Corporation ',
     'OPRX':'OptimizeRx Corporation ',
     'OPT':'Opthea Limited ',
     'OPTN':'OptiNose Inc. ',
     'OPTT':'Ocean Power Technologies Inc. ',
     'OPXS':'Optex Systems Holdings Inc. ',
     'OPY':'Oppenheimer Holdings Inc.   (DE)',
     'OR':'Osisko Gold Royalties Ltd ',
     'ORA':'Ormat Technologies Inc. ',
     'ORAN':'Orange',
     'ORC':'Orchid Island Capital Inc. ',
     'ORCL':'Oracle Corporation ',
     'ORGN':'Origin Materials Inc. ',
     'ORGNW':'Origin Materials Inc. s',
     'ORGO':'Organogenesis Holdings Inc.  ',
     'ORGS':'Orgenesis Inc. ',
     'ORI':'Old Republic International Corporation ',
     'ORIC':'Oric Pharmaceuticals Inc. ',
     'ORLA':'Orla Mining Ltd. ',
     'ORLY':'OReilly Automotive Inc. ',
     'ORMP':'Oramed Pharmaceuticals Inc. ',
     'ORN':'Orion Group Holdings Inc. Common',
     'ORRF':'Orrstown Financial Services Inc ',
     'ORTX':'Orchard Therapeutics plc ',
     'OSA':'ProSomnus Inc. ',
     'OSAAW':'ProSomnus Inc. ',
     'OSBC':'Old Second Bancorp Inc. ',
     'OSCR':'Oscar Health Inc.  ',
     'OSG':'Overseas Shipholding Group Inc.  ',
     'OSI':'Osiris Acquisition Corp.  ',
     'OSIS':'OSI Systems Inc.  (DE)',
     'OSK':'Oshkosh Corporation (Holding Company)',
     'OSPN':'OneSpan Inc. ',
     'OSS':'One Stop Systems Inc. ',
     'OST':'Ostin Technology Group Co. Ltd. ',
     'OSTK':'Overstock.com Inc. ',
     'OSUR':'OraSure Technologies Inc. ',
     'OSW':'OneSpaWorld Holdings Limited ',
     'OTEC':'OceanTech Acquisitions I Corp.  ',
     'OTECW':'OceanTech Acquisitions I Corp. ',
     'OTEX':'Open Text Corporation ',
     'OTIS':'Otis Worldwide Corporation ',
     'OTLK':'Outlook Therapeutics Inc. ',
     'OTLY':'Oatly Group AB ',
     'OTMO':'Otonomo Technologies Ltd. ',
     'OTMOW':'Otonomo Technologies Ltd. ',
     'OTRK':'Ontrak Inc. ',
     'OTTR':'Otter Tail Corporation ',
     'OUST':'Ouster Inc. ',
     'OUT':'OUTFRONT Media Inc. ',
     'OVBC':'Ohio Valley Banc Corp. ',
     'OVID':'Ovid Therapeutics Inc. ',
     'OVLY':'Oak Valley Bancorp (CA) ',
     'OVV':'Ovintiv Inc. (DE)',
     'OWL':'Blue Owl Capital Inc.  ',
     'OWLT':'Owlet Inc.  ',
     'OXAC':'Oxbridge Acquisition Corp. ',
     'OXACW':'Oxbridge Acquisition Corp. ',
     'OXBR':'Oxbridge Re Holdings Limited ',
     'OXBRW':'Oxbridge Re Holdings Limited  expiring 3/26/2024',
     'OXLC':'Oxford Lane Capital Corp. ',
     'OXM':'Oxford Industries Inc. ',
     'OXSQ':'Oxford Square Capital Corp. ',
     'OXUS':'Oxus Acquisition Corp. ',
     'OXUSW':'Oxus Acquisition Corp. ',
     'OXY':'Occidental Petroleum Corporation ',
     'OZ':'Belpointe PREP LLC  Units',
     'OZK':'Bank OZK ',
     'PAA':'Plains All American Pipeline L.P. Common Units representing Limited Partner Interests',
     'PAAS':'Pan American Silver Corp. ',
     'PAC':'Grupo Aeroportuario Del Pacifico S.A. B. de C.V. )',
     'PACB':'Pacific Biosciences of California Inc. ',
     'PACI':'PROOF Acquisition Corp I  ',
     'PACK':'Ranpak Holdings Corp  ',
     'PACW':'PacWest Bancorp ',
     'PAG':'Penske Automotive Group Inc. ',
     'PAGP':'Plains GP Holdings L.P.  Units representing Limited Partner Interests',
     'PAGS':'PagSeguro Digital Ltd.  ',
     'PAHC':'Phibro Animal Health Corporation  ',
     'PAI':'Western Asset Investment Grade Income Fund Inc.',
     'PALI':'Palisade Bio Inc. ',
     'PALT':'Paltalk Inc. ',
     'PAM':'Pampa Energia S.A. Pampa Energia S.A.',
     'PANL':'Pangaea Logistics Solutions Ltd. ',
     'PANW':'Palo Alto Networks Inc. ',
     'PAR':'PAR Technology Corporation ',
     'PARA':'Paramount Global Class B ',
     'PARAA':'Paramount Global  ',
     'PARR':'Par Pacific Holdings Inc.  ',
     'PASG':'Passage Bio Inc. ',
     'PATH':'UiPath Inc.  ',
     'PATI':'Patriot Transportation Holding Inc. ',
     'PATK':'Patrick Industries Inc. ',
     'PAVM':'PAVmed Inc. ',
     'PAVS':'Paranovus Entertainment Technology Ltd. ',
     'PAX':'Patria Investments Limited  ',
     'PAXS':'PIMCO Access Income Fund  of Beneficial Interest',
     'PAY':'Paymentus Holdings Inc.  ',
     'PAYC':'Paycom Software Inc. ',
     'PAYO':'Payoneer Global Inc. ',
     'PAYOW':'Payoneer Global Inc. ',
     'PAYS':'Paysign Inc. ',
     'PAYX':'Paychex Inc. ',
     'PB':'Prosperity Bancshares Inc. ',
     'PBA':'Pembina Pipeline Corp.  (Canada)',
     'PBAX':'Phoenix Biotech Acquisition Corp.  ',
     'PBAXU':'Phoenix Biotech Acquisition Corp. Unit',
     'PBAXW':'Phoenix Biotech Acquisition Corp. s',
     'PBBK':'PB Bankshares Inc. ',
     'PBF':'PBF Energy Inc.  ',
     'PBFS':'Pioneer Bancorp Inc. ',
     'PBH':'Prestige Consumer Healthcare Inc. ',
     'PBHC':'Pathfinder Bancorp Inc.  (MD)',
     'PBI':'Pitney Bowes Inc. ',
     'PBLA':'Panbela Therapeutics Inc. ',
     'PBPB':'Potbelly Corporation ',
     'PBR':'Petroleo Brasileiro S.A.- Petrobras ',
     'PBT':'Permian Basin Royalty Trust ',
     'PBTS':'Powerbridge Technologies Co. Ltd. ',
     'PBYI':'Puma Biotechnology Inc ',
     'PCAR':'PACCAR Inc. ',
     'PCB':'PCB Bancorp ',
     'PCCT':'Perception Capital Corp. II ',
     'PCCTW':'Perception Capital Corp. II s',
     'PCF':'High Income Securities Fund ',
     'PCG':'Pacific Gas & Electric Co. ',
     'PCH':'PotlatchDeltic Corporation ',
     'PCK':'Pimco California Municipal Income Fund II  of Beneficial Interest',
     'PCM':'PCM Fund Inc. ',
     'PCN':'Pimco Corporate & Income Strategy Fund ',
     'PCOR':'Procore Technologies Inc. ',
     'PCQ':'PIMCO California Municipal Income Fund ',
     'PCRX':'Pacira BioSciences Inc. ',
     'PCSA':'Processa Pharmaceuticals Inc. ',
     'PCT':'PureCycle Technologies Inc. ',
     'PCTI':'PCTEL Inc. ',
     'PCTTW':'PureCycle Technologies Inc. ',
     'PCTY':'Paylocity Holding Corporation ',
     'PCVX':'Vaxcyte Inc. ',
     'PCYG':'Park City Group Inc. ',
     'PCYO':'Pure Cycle Corporation ',
     'PD':'PagerDuty Inc. ',
     'PDCE':'PDC Energy Inc.  (Delaware)',
     'PDCO':'Patterson Companies Inc. ',
     'PDD':'PDD Holdings Inc. ',
     'PDEX':'Pro-Dex Inc. ',
     'PDFS':'PDF Solutions Inc. ',
     'PDI':'PIMCO Dynamic Income Fund ',
     'PDLB':'Ponce Financial Group Inc. ',
     'PDM':'Piedmont Office Realty Trust Inc.  ',
     'PDO':'PIMCO Dynamic Income Opportunities Fund  of Beneficial Interest',
     'PDS':'Precision Drilling Corporation ',
     'PDSB':'PDS Biotechnology Corporation ',
     'PDT':'John Hancock Premium Dividend Fund',
     'PEAK':'Healthpeak Properties Inc. ',
     'PEB':'Pebblebrook Hotel Trust  of Beneficial Interest',
     'PEBK':'Peoples Bancorp of North Carolina Inc. ',
     'PEBO':'Peoples Bancorp Inc. ',
     'PECO':'Phillips Edison & Company Inc. ',
     'PED':'Pedevco Corp. ',
     'PEG':'Public Service Enterprise Group Incorporated ',
     'PEGA':'Pegasystems Inc. ',
     'PEGR':'Project Energy Reimagined Acquisition Corp.',
     'PEGY':'Pineapple Energy Inc. ',
     'PEN':'Penumbra Inc. ',
     'PENN':'PENN Entertainment Inc. ',
     'PEO':'Adams Natural Resources Fund Inc. ',
     'PEP':'PepsiCo Inc. ',
     'PEPG':'PepGen Inc. ',
     'PEPL':'PepperLime Health Acquisition Corporation',
     'PERF':'Perfect Corp.',
     'PERI':'Perion Network Ltd. ',
     'PESI':'Perma-Fix Environmental Services Inc. ',
     'PET':'Wag! Group Co. ',
     'PETQ':'PetIQ Inc.  ',
     'PETS':'PetMed Express Inc. ',
     'PETV':'PetVivo Holdings Inc. ',
     'PETWW':'Wag! Group Co ',
     'PETZ':'TDH Holdings Inc. ',
     'PEV':'Phoenix Motor Inc. ',
     'PFBC':'Preferred Bank ',
     'PFC':'Premier Financial Corp. ',
     'PFD':'Flaherty & Crumrine Preferred and Income Fund Incorporated',
     'PFE':'Pfizer Inc. ',
     'PFG':'Principal Financial Group Inc ',
     'PFGC':'Performance Food Group Company ',
     'PFIE':'Profire Energy Inc. ',
     'PFIN':'P & F Industries Inc.  ',
     'PFIS':'Peoples Financial Services Corp. ',
     'PFL':'PIMCO Income Strategy Fund Shares of Beneficial Interest',
     'PFLT':'PennantPark Floating Rate Capital Ltd. ',
     'PFMT':'Performant Financial Corporation ',
     'PFN':'PIMCO Income Strategy Fund II',
     'PFO':'Flaherty & Crumrine Preferred and Income Opportunity Fund Incorporated',
     'PFS':'Provident Financial Services Inc ',
     'PFSI':'PennyMac Financial Services Inc. ',
     'PFSW':'PFSweb Inc. ',
     'PFTA':'Portage Fintech Acquisition Corporation',
     'PFX':'PhenixFIN Corporation ',
     'PG':'Procter & Gamble Company ',
     'PGC':'Peapack-Gladstone Financial Corporation ',
     'PGEN':'Precigen Inc. ',
     'PGNY':'Progyny Inc. ',
     'PGP':'Pimco Global Stocksplus & Income Fund Pimco Global StocksPlus & Income Fund  of Beneficial Interest',
     'PGR':'Progressive Corporation ',
     'PGRE':'Paramount Group Inc. ',
     'PGRU':'PropertyGuru Group Limited ',
     'PGSS':'Pegasus Digital Mobility Acquisition Corp. ',
     'PGTI':'PGT Innovations Inc.',
     'PGY':'Pagaya Technologies Ltd. ',
     'PGYWW':'Pagaya Technologies Ltd. s',
     'PGZ':'Principal Real Estate Income Fund  of Beneficial Interest',
     'PH':'Parker-Hannifin Corporation ',
     'PHAR':'Pharming Group N.V. ADS each representing 10 ',
     'PHAT':'Phathom Pharmaceuticals Inc. ',
     'PHD':'Pioneer Floating Rate Fund Inc.',
     'PHG':'Koninklijke Philips N.V. NY Registry Shares',
     'PHGE':'BiomX Inc. ',
     'PHI':'PLDT Inc. Sponsored ADR',
     'PHIN':'PHINIA Inc. ',
     'PHIO':'Phio Pharmaceuticals Corp. ',
     'PHK':'Pimco High Income Fund Pimco High Income Fund',
     'PHM':'PulteGroup Inc. ',
     'PHR':'Phreesia Inc. ',
     'PHT':'Pioneer High Income Fund Inc.',
     'PHUN':'Phunware Inc. ',
     'PHUNW':'Phunware Inc. s',
     'PHVS':'Pharvaris N.V. ',
     'PHX':'PHX Minerals Inc. ',
     'PHXM':'PHAXIAM Therapeutics S.A.. ',
     'PHYT':'Pyrophyte Acquisition Corp. ',
     'PI':'Impinj Inc. ',
     'PII':'Polaris Inc. ',
     'PIII':'P3 Health Partners Inc.  ',
     'PIK':'Kidpik Corp. ',
     'PIM':'Putnam Master Intermediate Income Trust ',
     'PINC':'Premier Inc.  ',
     'PINE':'Alpine Income Property Trust Inc. ',
     'PINS':'Pinterest Inc.  ',
     'PIPR':'Piper Sandler Companies ',
     'PIRS':'Pieris Pharmaceuticals Inc. ',
     'PIXY':'ShiftPixy Inc. ',
     'PJT':'PJT Partners Inc.  ',
     'PK':'Park Hotels & Resorts Inc. ',
     'PKBK':'Parke Bancorp Inc. ',
     'PKE':'Park Aerospace Corp. ',
     'PKG':'Packaging Corporation of America ',
     'PKOH':'Park-Ohio Holdings Corp. ',
     'PKST':'Peakstone Realty Trust ',
     'PKX':'POSCO Holdings Inc.  (Each representing 1/4th of a share of )',
     'PL':'Planet Labs PBC  ',
     'PLAB':'Photronics Inc. ',
     'PLAG':'Planet Green Holdings Corp. ',
     'PLAY':'Dave & Busters Entertainment Inc. ',
     'PLBC':'Plumas Bancorp',
     'PLBY':'PLBY Group Inc. ',
     'PLCE':'Childrens Place Inc. ',
     'PLD':'Prologis Inc. ',
     'PLG':'Platinum Group Metals Ltd.  (Canada)',
     'PLL':'Piedmont Lithium Inc. ',
     'PLM':'Polymet Mining Corporation  (Canada)',
     'PLMI':'Plum Acquisition Corp. I',
     'PLMIW':'Plum Acquisition Corp. I ',
     'PLMR':'Palomar Holdings Inc. ',
     'PLNT':'Planet Fitness Inc. ',
     'PLOW':'Douglas Dynamics Inc. ',
     'PLPC':'Preformed Line Products Company ',
     'PLRX':'Pliant Therapeutics Inc. ',
     'PLSE':'Pulse Biosciences Inc  (DE)',
     'PLTK':'Playtika Holding Corp. ',
     'PLTN':'Plutonian Acquisition Corp. ',
     'PLTNR':'Plutonian Acquisition Corp. Rights',
     'PLTNU':'Plutonian Acquisition Corp. Unit',
     'PLTNW':'Plutonian Acquisition Corp. ',
     'PLTR':'Palantir Technologies Inc.  ',
     'PLUG':'Plug Power Inc. ',
     'PLUR':'Pluri Inc. ',
     'PLUS':'ePlus inc. ',
     'PLX':'Protalix BioTherapeutics Inc. (DE) ',
     'PLXS':'Plexus Corp. ',
     'PLYA':'Playa Hotels & Resorts N.V. ',
     'PLYM':'Plymouth Industrial REIT Inc. ',
     'PM':'Philip Morris International Inc ',
     'PMCB':'PharmaCyte  Biotech Inc. ',
     'PMD':'Psychemedics Corporation',
     'PMF':'PIMCO Municipal Income Fund ',
     'PMGM':'Priveterra Acquisition Corp.  ',
     'PMGMU':'Priveterra Acquisition Corp. Units',
     'PMGMW':'Priveterra Acquisition Corp. ',
     'PML':'Pimco Municipal Income Fund II  of Beneficial Interest',
     'PMM':'Putnam Managed Municipal Income Trust ',
     'PMN':'ProMIS Neurosciences Inc. ',
     'PMO':'Putnam Municipal Opportunities Trust ',
     'PMT':'PennyMac Mortgage Investment Trust  of Beneficial Interest',
     'PMTS':'CPI Card Group Inc. ',
     'PMVP':'PMV Pharmaceuticals Inc. ',
     'PMX':'PIMCO Municipal Income Fund III  of Beneficial Interest',
     'PNAC':'Prime Number Acquisition I Corp.  ',
     'PNACR':'Prime Number Acquisition I Corp. Right',
     'PNBK':'Patriot National Bancorp Inc. ',
     'PNC':'PNC Financial Services Group Inc. ',
     'PNF':'PIMCO New York Municipal Income Fund ',
     'PNFP':'Pinnacle Financial Partners Inc. ',
     'PNI':'Pimco New York Municipal Income Fund II  of Beneficial Interest',
     'PNM':'PNM Resources Inc. (Holding Co.) ',
     'PNNT':'PennantPark Investment Corporation ',
     'PNR':'Pentair plc. ',
     'PNRG':'PrimeEnergy Resources Corporation ',
     'PNT':'POINT Biopharma Global Inc. ',
     'PNTG':'The Pennant Group Inc. ',
     'PNW':'Pinnacle West Capital Corporation ',
     'POAI':'Predictive Oncology Inc. ',
     'POCI':'Precision Optics Corporation Inc. ',
     'PODD':'Insulet Corporation ',
     'POET':'POET Technologies Inc. ',
     'POL':'Polished Inc. ',
     'POLA':'Polar Power Inc. ',
     'POOL':'Pool Corporation ',
     'POR':'Portland General Electric Co ',
     'PORT':'Southport Acquisition Corporation  ',
     'POST':'Post Holdings Inc. ',
     'POWI':'Power Integrations Inc. ',
     'POWL':'Powell Industries Inc. ',
     'POWW':'AMMO Inc. ',
     'PPBI':'Pacific Premier Bancorp Inc',
     'PPBT':'Purple Biotech Ltd. ',
     'PPC':'Pilgrims Pride Corporation ',
     'PPG':'PPG Industries Inc. ',
     'PPHP':'PHP Ventures Acquisition Corp.  ',
     'PPHPR':'PHP Ventures Acquisition Corp. Rights',
     'PPIH':'Perma-Pipe International Holdings Inc. ',
     'PPL':'PPL Corporation ',
     'PPSI':'Pioneer Power Solutions Inc. ',
     'PPT':'Putnam Premier Income Trust ',
     'PPTA':'Perpetua Resources Corp. ',
     'PPYA':'Papaya Growth Opportunity Corp. I  ',
     'PPYAU':'Papaya Growth Opportunity Corp. I Unit',
     'PPYAW':'Papaya Growth Opportunity Corp. I ',
     'PR':'Permian Resources Corporation  ',
     'PRA':'ProAssurance Corporation ',
     'PRAA':'PRA Group Inc. ',
     'PRAX':'Praxis Precision Medicines Inc. ',
     'PRCH':'Porch Group Inc. ',
     'PRCT':'PROCEPT BioRobotics Corporation ',
     'PRDO':'Perdoceo Education Corporation ',
     'PRDS':'Pardes Biosciences Inc. ',
     'PRE':'Prenetics Global Limited',
     'PRENW':'Prenetics Global Limited ',
     'PRFT':'Perficient Inc. ',
     'PRFX':'PainReform Ltd. ',
     'PRG':'PROG Holdings Inc. ',
     'PRGO':'Perrigo Company plc ',
     'PRGS':'Progress Software Corporation  (DE)',
     'PRI':'Primerica Inc. ',
     'PRIM':'Primoris Services Corporation ',
     'PRK':'Park National Corporation ',
     'PRLB':'Proto Labs Inc. ',
     'PRLD':'Prelude Therapeutics Incorporated ',
     'PRLH':'Pearl Holdings Acquisition Corp ',
     'PRLHU':'Pearl Holdings Acquisition Corp Unit',
     'PRLHW':'Pearl Holdings Acquisition Corp ',
     'PRM':'Perimeter Solutions SA ',
     'PRME':'Prime Medicine Inc. ',
     'PRMW':'Primo Water Corporation ',
     'PRO':'PROS Holdings Inc. ',
     'PROC':'Procaps Group S.A. ',
     'PROF':'Profound Medical Corp. ',
     'PROK':'ProKidney Corp. ',
     'PROV':'Provident Financial Holdings Inc. ',
     'PRPC':'CC Neuberger Principal Holdings III ',
     'PRPH':'ProPhase Labs Inc.  (DE)',
     'PRPL':'Purple Innovation Inc. ',
     'PRPO':'Precipio Inc.  ',
     'PRQR':'ProQR Therapeutics N.V. ',
     'PRSO':'Peraso Inc. ',
     'PRSR':'Prospector Capital Corp. ',
     'PRSRU':'Prospector Capital Corp. Unit',
     'PRSRW':'Prospector Capital Corp. s',
     'PRST':'Presto Automation Inc. ',
     'PRSTW':'Presto Automation Inc. ',
     'PRT':'PermRock Royalty Trust Trust Units',
     'PRTA':'Prothena Corporation plc ',
     'PRTC':'PureTech Health plc ',
     'PRTG':'Portage Biotech Inc. ',
     'PRTH':'Priority Technology Holdings Inc. ',
     'PRTK':'Paratek Pharmaceuticals Inc. ',
     'PRTS':'CarParts.com Inc. ',
     'PRU':'Prudential Financial Inc. ',
     'PRVA':'Privia Health Group Inc. ',
     'PSA':'Public Storage ',
     'PSEC':'Prospect Capital Corporation ',
     'PSF':'Cohen & Steers Select Preferred and Income Fund Inc. ',
     'PSFE':'Paysafe Limited ',
     'PSHG':'Performance Shipping Inc. ',
     'PSMT':'PriceSmart Inc. ',
     'PSN':'Parsons Corporation ',
     'PSNL':'Personalis Inc. ',
     'PSNY':'Polestar Automotive Holding UK PLC  ADS',
     'PSNYW':'Polestar Automotive Holding UK PLC Class C-1 ADS (ADW)',
     'PSO':'Pearson Plc ',
     'PSTG':'Pure Storage Inc.  ',
     'PSTL':'Postal Realty Trust Inc.  ',
     'PSTV':'PLUS THERAPEUTICS Inc. ',
     'PSTX':'Poseida Therapeutics Inc. ',
     'PSX':'Phillips 66 ',
     'PT':'Pintec Technology Holdings Limited ',
     'PTC':'PTC Inc. ',
     'PTCT':'PTC Therapeutics Inc. ',
     'PTEN':'Patterson-UTI Energy Inc. ',
     'PTGX':'Protagonist Therapeutics Inc. ',
     'PTHRU':'Pono Capital Three Inc. Unit',
     'PTHRW':'Pono Capital Three Inc. ',
     'PTIX':'Protagenic Therapeutics Inc. ',
     'PTIXW':'Protagenic Therapeutics Inc. ',
     'PTLO':'Portillos Inc.  ',
     'PTMN':'Portman Ridge Finance Corporation ',
     'PTN':'Palatin Technologies Inc. ',
     'PTON':'Peloton Interactive Inc.  ',
     'PTPI':'Petros Pharmaceuticals Inc. ',
     'PTRA':'Proterra Inc. ',
     'PTRS':'Partners Bancorp ',
     'PTSI':'P.A.M. Transportation Services Inc. ',
     'PTVE':'Pactiv Evergreen Inc. ',
     'PTWO':'Pono Capital Two Inc.  ',
     'PTWOU':'Pono Capital Two Inc. Unit',
     'PTWOW':'Pono Capital Two Inc. s',
     'PTY':'Pimco Corporate & Income Opportunity Fund',
     'PUBM':'PubMatic Inc.  ',
     'PUCK':'Goal Acquisitions Corp. ',
     'PUCKW':'Goal Acquisitions Corp. ',
     'PUK':'Prudential Public Limited Company ',
     'PULM':'Pulmatrix Inc. ',
     'PUMP':'ProPetro Holding Corp. ',
     'PUYI':'Puyi Inc. American Depository Shares',
     'PVBC':'Provident Bancorp Inc. (MD) ',
     'PVH':'PVH Corp. ',
     'PVL':'Permianville Royalty Trust Trust Units',
     'PW':'Power REIT (MD) ',
     'PWFL':'PowerFleet Inc. ',
     'PWM':'Prestige Wealth Inc. ',
     'PWOD':'Penns Woods Bancorp Inc. ',
     'PWP':'Perella Weinberg Partners  ',
     'PWR':'Quanta Services Inc. ',
     'PWSC':'PowerSchool Holdings Inc.  ',
     'PWUP':'PowerUp Acquisition Corp. ',
     'PWUPU':'PowerUp Acquisition Corp. Unit',
     'PWUPW':'PowerUp Acquisition Corp. ',
     'PX':'P10 Inc.  ',
     'PXLW':'Pixelworks Inc.  ',
     'PXMD':'PaxMedica Inc. ',
     'PXS':'Pyxis Tankers Inc. ',
     'PXSAW':'Pyxis Tankers Inc. ',
     'PYCR':'Paycor HCM Inc. ',
     'PYN':'PIMCO New York Municipal Income Fund III  of Beneficial Interest',
     'PYPD':'PolyPid Ltd. ',
     'PYPL':'PayPal Holdings Inc. ',
     'PYR':'PyroGenesis Canada Inc. ',
     'PYT':'PPlus Tr GSC-2 Tr Ctf Fltg Rate',
     'PYXS':'Pyxis Oncology Inc. ',
     'PZC':'PIMCO California Municipal Income Fund III  of Beneficial Interest',
     'PZG':'Paramount Gold Nevada Corp. ',
     'PZZA':'Papa Johns International Inc. ',
     'QBTS':'D-Wave Quantum Inc. ',
     'QCOM':'QUALCOMM Incorporated ',
     'QCRH':'QCR Holdings Inc. ',
     'QD':'Qudian Inc.  each representing one',
     'QDEL':'QuidelOrtho Corporation ',
     'QDRO':'Quadro Acquisition One Corp. ',
     'QDROW':'Quadro Acquisition One Corp.  ',
     'QFIN':'Qifu Technology Inc. ',
     'QFTA':'Quantum FinTech Acquisition Corporation ',
     'QGEN':'Qiagen N.V. ',
     'QH':'Quhuo Limited American Depository Shares',
     'QIPT':'Quipt Home Medical Corp. ',
     'QLGN':'Qualigen Therapeutics Inc. ',
     'QLI':'Qilian International Holding Group Ltd. ',
     'QLYS':'Qualys Inc. ',
     'QMCO':'Quantum Corporation ',
     'QNCX':'Quince Therapeutics Inc. ',
     'QNRX':'Quoin Pharmaceuticals Ltd. ',
     'QNST':'QuinStreet Inc. ',
     'QOMO':'Qomolangma Acquisition Corp. ',
     'QOMOR':'Qomolangma Acquisition Corp. Right',
     'QRHC':'Quest Resource Holding Corporation ',
     'QRTEA':'Qurate Retail Inc. Series A ',
     'QRTEB':'Qurate Retail Inc. Series B ',
     'QRVO':'Qorvo Inc. ',
     'QS':'QuantumScape Corporation  ',
     'QSG':'QuantaSing Group Limited ',
     'QSI':'Quantum-Si Incorporated  ',
     'QSIAW':'Quantum-Si Incorporated ',
     'QSR':'Restaurant Brands International Inc. ',
     'QTRX':'Quanterix Corporation ',
     'QTWO':'Q2 Holdings Inc. ',
     'QUAD':'Quad Graphics Inc  ',
     'QUBT':'Quantum Computing Inc. ',
     'QUIK':'QuickLogic Corporation ',
     'QUOT':'Quotient Technology Inc. ',
     'QURE':'uniQure N.V. ',
     'R':'Ryder System Inc. ',
     'RA':'Brookfield Real Assets Income Fund Inc. ',
     'RACE':'Ferrari N.V. ',
     'RAD':'Rite Aid Corporation ',
     'RADI':'Radius Global Infrastructure Inc.  ',
     'RAIL':'FreightCar America Inc. ',
     'RAIN':'Rain Oncology Inc. ',
     'RAMP':'LiveRamp Holdings Inc. ',
     'RAND':'Rand Capital Corporation ',
     'RANI':'Rani Therapeutics Holdings Inc.  ',
     'RAPT':'RAPT Therapeutics Inc. ',
     'RARE':'Ultragenyx Pharmaceutical Inc. ',
     'RAVE':'Rave Restaurant Group Inc. ',
     'RAYA':'Erayak Power Solution Group Inc. ',
     'RBA':'RB Global Inc. ',
     'RBB':'RBB Bancorp ',
     'RBBN':'Ribbon Communications Inc. ',
     'RBC':'RBC Bearings Incorporated ',
     'RBCAA':'Republic Bancorp Inc.  ',
     'RBGLY':'RECKitt BENCKISER GROUP PLC ',
     'RBKB':'Rhinebeck Bancorp Inc. ',
     'RBLX':'Roblox Corporation  ',
     'RBOT':'Vicarious Surgical Inc.  ',
     'RBT':'Rubicon Technologies Inc.  ',
     'RC':'Ready Capital Corproation ',
     'RCAC':'Revelstone Capital Acquisition Corp.  ',
     'RCAT':'Red Cat Holdings Inc. ',
     'RCEL':'Avita Medical Inc. ',
     'RCG':'RENN Fund Inc ',
     'RCI':'Rogers Communication Inc. ',
     'RCKT':'Rocket Pharmaceuticals Inc. ',
     'RCKTW':'Rocket Pharmaceuticals Inc. ',
     'RCKY':'Rocky Brands Inc. ',
     'RCL':'Royal Caribbean Cruises Ltd. ',
     'RCLF':'Rosecliff Acquisition Corp I  ',
     'RCLFW':'Rosecliff Acquisition Corp I s',
     'RCM':'R1 RCM Inc. ',
     'RCMT':'RCM Technologies Inc. ',
     'RCON':'Recon Technology Ltd. ',
     'RCRT':'Recruiter.com Group Inc. ',
     'RCS':'PIMCO Strategic Income Fund Inc.',
     'RCUS':'Arcus Biosciences Inc. ',
     'RDCM':'Radcom Ltd. ',
     'RDDT':'Reddit Inc. ',
     'RDFN':'Redfin Corporation ',
     'RDHL':'Redhill Biopharma Ltd. ',
     'RDI':'Reading International Inc  ',
     'RDIB':'Reading International Inc Class B ',
     'RDN':'Radian Group Inc. ',
     'RDNT':'RadNet Inc. ',
     'RDVT':'Red Violet Inc. ',
     'RDW':'Redwire Corporation ',
     'RDWR':'Radware Ltd. ',
     'RDY':'Dr. Reddys Laboratories Ltd ',
     'RE':'Everest Re Group Ltd. ',
     'REAL':'The RealReal Inc. ',
     'REAX':'The Real Brokerage Inc. ',
     'REBN':'Reborn Coffee Inc. ',
     'REE':'REE Automotive Ltd. ',
     'REFI':'Chicago Atlantic Real Estate Finance Inc. ',
     'REFR':'Research Frontiers Incorporated ',
     'REG':'Regency Centers Corporation ',
     'REGN':'Regeneron Pharmaceuticals Inc. ',
     'REI':'Ring Energy Inc. ',
     'REKR':'Rekor Systems Inc. ',
     'RELI':'Reliance Global Group Inc. ',
     'RELIW':'Reliance Global Group Inc. Series A s',
     'RELL':'Richardson Electronics Ltd. ',
     'RELX':'RELX PLC PLC  (Each representing One )',
     'RELY':'Remitly Global Inc. ',
     'RENE':'Cartesian Growth Corporation II ',
     'RENEU':'Cartesian Growth Corporation II Unit',
     'RENEW':'Cartesian Growth Corporation II ',
     'RENT':'Rent the Runway Inc.  ',
     'REPL':'Replimune Group Inc. ',
     'REPX':'Riley Exploration Permian Inc. ',
     'RERE':'ATRenew Inc.  (every three of which representing two )',
     'RES':'RPC Inc. ',
     'RETA':'Reata Pharmaceuticals Inc.  ',
     'RETO':'ReTo Eco-Solutions Inc. ',
     'REUN':'Reunion Neuroscience Inc. ',
     'REVB':'Revelation Biosciences Inc. ',
     'REVBW':'Revelation Biosciences Inc. ',
     'REVG':'REV Group Inc. ',
     'REX':'REX American Resources Corporation',
     'REXR':'Rexford Industrial Realty Inc. ',
     'REYN':'Reynolds Consumer Products Inc. ',
     'REZI':'Resideo Technologies Inc. ',
     'RF':'Regions Financial Corporation ',
     'RFAC':'RF Acquisition Corp.  ',
     'RFACR':'RF Acquisition Corp. Rights',
     'RFACU':'RF Acquisition Corp. Unit',
     'RFI':'Cohen & Steers Total Return Realty Fund Inc. ',
     'RFIL':'RF Industries Ltd. ',
     'RFL':'Rafael Holdings Inc. Class B ',
     'RFM':'RiverNorth Flexible Municipal Income Fund Inc. ',
     'RFMZ':'RiverNorth Flexible Municipal Income Fund II Inc. ',
     'RGA':'Reinsurance Group of America Incorporated ',
     'RGC':'Regencell Bioscience Holdings Limited ',
     'RGCO':'RGC Resources Inc. ',
     'RGEN':'Repligen Corporation ',
     'RGF':'The Real Good Food Company Inc.  ',
     'RGLD':'Royal Gold Inc. ',
     'RGLS':'Regulus Therapeutics Inc. ',
     'RGNX':'REGENXBIO Inc. ',
     'RGP':'Resources Connection Inc. ',
     'RGR':'Sturm Ruger & Company Inc. ',
     'RGS':'Regis Corporation ',
     'RGT':'Royce Global Value Trust Inc. ',
     'RGTI':'Rigetti Computing Inc. ',
     'RGTIW':'Rigetti Computing Inc. s',
     'RH':'RH ',
     'RHE':'Regional Health Properties Inc. ',
     'RHI':'Robert Half International Inc. ',
     'RHP':'Ryman Hospitality Properties Inc. (REIT)',
     'RIBT':'RiceBran Technologies ',
     'RICK':'RCI Hospitality Holdings Inc. ',
     'RIG':'Transocean Ltd (Switzerland) ',
     'RIGL':'Rigel Pharmaceuticals Inc. ',
     'RILY':'B. Riley Financial Inc. ',
     'RIO':'Rio Tinto Plc ',
     'RIOT':'Riot Platforms Inc. ',
     'RITM':'Rithm Capital Corp. ',
     'RIV':'RiverNorth Opportunities Fund Inc. ',
     'RIVN':'Rivian Automotive Inc.  ',
     'RJF':'Raymond James Financial Inc. ',
     'RKDA':'Arcadia Biosciences Inc. ',
     'RKLB':'Rocket Lab USA Inc. ',
     'RKT':'Rocket Companies Inc.  ',
     'RL':'Ralph Lauren Corporation ',
     'RLAY':'Relay Therapeutics Inc. ',
     'RLGT':'Radiant Logistics Inc. ',
     'RLI':'RLI Corp.  (DE)',
     'RLJ':'RLJ Lodging Trust  of Beneficial Interest $0.01 par value',
     'RLMD':'Relmada Therapeutics Inc. ',
     'RLTY':'Cohen & Steers Real Estate Opportunities and Income Fund  of Beneficial Interest',
     'RLX':'RLX Technology Inc.  each representing the right to receive one (1)',
     'RLYB':'Rallybio Corporation ',
     'RM':'Regional Management Corp. ',
     'RMAX':'RE/MAX Holdings Inc.  ',
     'RMBI':'Richmond Mutual Bancorporation Inc. ',
     'RMBL':'RumbleOn Inc. Class B ',
     'RMBS':'Rambus Inc. ',
     'RMCF':'Rocky Mountain Chocolate Factory Inc. ',
     'RMD':'ResMed Inc. ',
     'RMED':'Ra Medical Systems Inc. ',
     'RMGC':'RMG Acquisition Corp. III ',
     'RMGCW':'RMG Acquisition Corp. III ',
     'RMNI':'Rimini Street Inc. (DE) ',
     'RMR':'The RMR Group Inc.  ',
     'RMT':'Royce Micro-Cap Trust Inc. ',
     'RMTI':'Rockwell Medical Inc. ',
     'RNA':'Avidity Biosciences Inc. ',
     'RNAZ':'TransCode Therapeutics Inc. ',
     'RNG':'RingCentral Inc.  ',
     'RNGR':'Ranger Energy Services Inc.  ',
     'RNLX':'Renalytix plc ',
     'RNP':'Cohen & Steers REIT and Preferred and Income Fund Inc. ',
     'RNR':'RenaissanceRe Holdings Ltd. ',
     'RNST':'Renasant Corporation ',
     'RNW':'ReNew Energy Global plc ',
     'RNWWW':'ReNew Energy Global plc ',
     'RNXT':'RenovoRx Inc. ',
     'ROAD':'Construction Partners Inc.  ',
     'ROCK':'Gibraltar Industries Inc. ',
     'ROCL':'Roth CH Acquisition V Co. ',
     'ROCLW':'Roth CH Acquisition V Co. ',
     'ROG':'Rogers Corporation ',
     'ROIC':'Retail Opportunity Investments Corp.  (MD)',
     'ROIV':'Roivant Sciences Ltd. ',
     'ROIVW':'Roivant Sciences Ltd. ',
     'ROK':'Rockwell Automation Inc. ',
     'ROKU':'Roku Inc.  ',
     'ROL':'Rollins Inc. ',
     'ROOT':'Root Inc.  ',
     'ROP':'Roper Technologies Inc. ',
     'ROSE':'Rose Hill Acquisition Corporation ',
     'ROSEW':'Rose Hill Acquisition Corporation ',
     'ROSS':'Ross Acquisition Corp II ',
     'ROST':'Ross Stores Inc. ',
     'ROVR':'Rover Group Inc.  ',
     'RPAY':'Repay Holdings Corporation  ',
     'RPD':'Rapid7 Inc. ',
     'RPHM':'Reneo Pharmaceuticals Inc. ',
     'RPID':'Rapid Micro Biosystems Inc.  ',
     'RPM':'RPM International Inc. ',
     'RPRX':'Royalty Pharma plc ',
     'RPT':'RPT Realty ',
     'RPTX':'Repare Therapeutics Inc. ',
     'RQI':'Cohen & Steers Quality Income Realty Fund Inc ',
     'RRAC':'Rigel Resource Acquisition Corp. ',
     'RRBI':'Red River Bancshares Inc. ',
     'RRC':'Range Resources Corporation ',
     'RRGB':'Red Robin Gourmet Burgers Inc. ',
     'RRR':'Red Rock Resorts Inc.  ',
     'RRX':'Regal Rexnord Corporation ',
     'RS':'Reliance Steel & Aluminum Co.  (DE)',
     'RSF':'RiverNorth Capital and Income Fund ',
     'RSG':'Republic Services Inc. ',
     'RSI':'Rush Street Interactive Inc.  ',
     'RSKD':'Riskified Ltd. ',
     'RSLS':'ReShape Lifesciences Inc. ',
     'RSSS':'Research Solutions Inc ',
     'RSVR':'Reservoir Media Inc. ',
     'RSVRW':'Reservoir Media Inc. ',
     'RTC':'Baijiayun Group Ltd. ',
     'RTL':'The Necessity Retail REIT Inc.  ',
     'RTO':'Rentokil Initial plc  (each representing five (5) )',
     'RTX':'Raytheon Technologies Corporation ',
     'RUM':'Rumble Inc.  ',
     'RUMBW':'Rumble Inc. ',
     'RUN':'Sunrun Inc. ',
     'RUSHA':'Rush Enterprises Inc.  Cl A',
     'RUSHB':'Rush Enterprises Inc. Class B',
     'RVLP':'RVL Pharmaceuticals plc ',
     'RVLV':'Revolve Group Inc.  ',
     'RVMD':'Revolution Medicines Inc. ',
     'RVNC':'Revance Therapeutics Inc. ',
     'RVP':'Retractable Technologies Inc. ',
     'RVPH':'Reviva Pharmaceuticals Holdings Inc. ',
     'RVPHW':'Reviva Pharmaceuticals Holdings Inc. s',
     'RVSB':'Riverview Bancorp Inc ',
     'RVSN':'Rail Vision Ltd. ',
     'RVSNW':'Rail Vision Ltd. ',
     'RVT':'Royce Value Trust Inc. ',
     'RVTY':'Revvity Inc. ',
     'RVYL':'Ryvyl Inc. ',
     'RWAY':'Runway Growth Finance Corp. ',
     'RWLK':'ReWalk Robotics Ltd. ',
     'RWOD':'Redwoods Acquisition Corp. ',
     'RWT':'Redwood Trust Inc. ',
     'RXO':'RXO Inc. ',
     'RXRX':'Recursion Pharmaceuticals Inc.  ',
     'RXST':'RxSight Inc. ',
     'RXT':'Rackspace Technology Inc. ',
     'RY':'Royal Bank Of Canada ',
     'RYAAY':'Ryanair Holdings plc ',
     'RYAM':'Rayonier Advanced Materials Inc. ',
     'RYAN':'Ryan Specialty Holdings Inc.  ',
     'RYI':'Ryerson Holding Corporation ',
     'RYN':'Rayonier Inc. REIT ',
     'RYTM':'Rhythm Pharmaceuticals Inc. ',
     'RZLT':'Rezolute Inc.  (NV)',
     'S':'SentinelOne Inc.  ',
     'SA':'Seabridge Gold Inc.  (Canada)',
     'SABR':'Sabre Corporation ',
     'SABS':'SAB Biotherapeutics Inc. ',
     'SABSW':'SAB Biotherapeutics Inc. ',
     'SACH':'Sachem Capital Corp. ',
     'SAFE':'Safehold Inc. New ',
     'SAFT':'Safety Insurance Group Inc. ',
     'SAGA':'Sagaliam Acquisition Corp.  ',
     'SAGAR':'Sagaliam Acquisition Corp. Rights',
     'SAGAU':'Sagaliam Acquisition Corp. Units',
     'SAGE':'Sage Therapeutics Inc. ',
     'SAH':'Sonic Automotive Inc. ',
     'SAI':'SAI.TECH Global Corporation ',
     'SAIA':'Saia Inc. ',
     'SAIC':'SCIENCE APPLICATIONS INTERNATIONAL CORPORATION ',
     'SAITW':'SAI.TECH Global Corporation ',
     'SAL':'Salisbury Bancorp Inc. ',
     'SALM':'Salem Media Group Inc.  ',
     'SAM':'Boston Beer Company Inc. ',
     'SAMA':'Schultze Special Purpose Acquisition Corp. II  ',
     'SAMG':'Silvercrest Asset Management Group Inc.  ',
     'SAN':'Banco Santander S.A. Sponsored ADR (Spain)',
     'SANA':'Sana Biotechnology Inc. ',
     'SAND':'Sandstorm Gold Ltd.  (Canada)',
     'SANG':'Sangoma Technologies Corporation ',
     'SANM':'Sanmina Corporation ',
     'SANW':'S&W Seed Company  (NV)',
     'SAP':'SAP SE ',
     'SAR':'Saratoga Investment Corp New',
     'SARTF':'Sartorius AG',
     'SASI':'Sigma Additive Solutions Inc. ',
     'SASR':'Sandy Spring Bancorp Inc. ',
     'SATL':'Satellogic Inc. ',
     'SATLW':'Satellogic Inc. ',
     'SATS':'EchoStar  Corporation ',
     'SATX':'SatixFy Communications Ltd. ',
     'SAVA':'Cassava Sciences Inc. ',
     'SAVE':'Spirit Airlines Inc. ',
     'SB':'Safe Bulkers Inc  ($0.001 par value)',
     'SBAC':'SBA Communications Corporation  ',
     'SBCF':'Seacoast Banking Corporation of Florida ',
     'SBET':'SharpLink Gaming Ltd. ',
     'SBEV':'Splash Beverage Group Inc. (NV) ',
     'SBFG':'SB Financial Group Inc. ',
     'SBFM':'Sunshine Biopharma Inc. ',
     'SBFMW':'Sunshine Biopharma Inc. ',
     'SBGI':'Sinclair Inc.  ',
     'SBH':'Sally Beauty Holdings Inc. (Name to be changed from Sally Holdings Inc.) ',
     'SBI':'Western Asset Intermediate Muni Fund Inc ',
     'SBIG':'SpringBig Holdings Inc. ',
     'SBIGW':'SpringBig Holdings Inc. ',
     'SBLK':'Star Bulk Carriers Corp. ',
     'SBOW':'SilverBow Resorces Inc. ',
     'SBR':'Sabine Royalty Trust ',
     'SBRA':'Sabra Health Care REIT Inc. ',
     'SBS':'Companhia de saneamento Basico Do Estado De Sao Paulo - Sabesp  (Each repstg 250 )',
     'SBSI':'Southside Bancshares Inc. ',
     'SBSW':'D/B/A Sibanye-Stillwater Limited ADS',
     'SBT':'Sterling Bancorp Inc. ',
     'SBUX':'Starbucks Corporation ',
     'SBXC':'SilverBox Corp III  ',
     'SCAQ':'Stratim Cloud Acquisition Corp.  ',
     'SCAQW':'Stratim Cloud Acquisition Corp. ',
     'SCCO':'Southern Copper Corporation ',
     'SCD':'LMP Capital and Income Fund Inc. ',
     'SCHL':'Scholastic Corporation ',
     'SCHN':'Schnitzer Steel Industries Inc.  ',
     'SCHW':'Charles Schwab Corporation ',
     'SCI':'Service Corporation International ',
     'SCKT':'Socket Mobile Inc. ',
     'SCL':'Stepan Company ',
     'SCLX':'Scilex Holding Company ',
     'SCLXW':'Scilex Holding Company ',
     'SCM':'Stellus Capital Investment Corporation ',
     'SCOR':'comScore Inc. ',
     'SCPH':'scPharmaceuticals Inc. ',
     'SCPL':'SciPlay Corporation  ',
     'SCRM':'Screaming Eagle Acquisition Corp. ',
     'SCRMU':'Screaming Eagle Acquisition Corp. Unit',
     'SCRMW':'Screaming Eagle Acquisition Corp. ',
     'SCS':'Steelcase Inc. ',
     'SCSC':'ScanSource Inc. ',
     'SCTL':'Societal CDMO Inc. ',
     'SCU':'Sculptor Capital Management Inc.  ',
     'SCVL':'Shoe Carnival Inc. ',
     'SCWO':'374Water Inc. ',
     'SCWX':'SecureWorks Corp.  ',
     'SCX':'L.S. Starrett Company ',
     'SCYX':'SCYNEXIS Inc. ',
     'SD':'SandRidge Energy Inc. ',
     'SDA':'SunCar Technology Group Inc. ',
     'SDAC':'Sustainable Development Acquisition I Corp.  ',
     'SDACU':'Sustainable Development Acquisition I Corp. Unit',
     'SDACW':'Sustainable Development Acquisition I Corp. ',
     'SDAWW':'SunCar Technology Group Inc. ',
     'SDC':'SmileDirectClub Inc.  ',
     'SDGR':'Schrodinger Inc. ',
     'SDHY':'PGIM Short Duration High Yield Opportunities Fund ',
     'SDIG':'Stronghold Digital Mining Inc.  ',
     'SDPI':'Superior Drilling Products Inc. ',
     'SDRL':'Seadrill Limited ',
     'SE':'Sea Limited',
     'SEAC':'SeaChange International Inc. ',
     'SEAS':'SeaWorld Entertainment Inc. ',
     'SEAT':'Vivid Seats Inc.  ',
     'SEB':'Seaboard Corporation ',
     'SECO':'Secoo Holding Limited ADS',
     'SEDA':'SDCL EDGE Acquisition Corporation ',
     'SEDG':'SolarEdge Technologies Inc. ',
     'SEE':'Sealed Air Corporation ',
     'SEED':'Origin Agritech Limited ',
     'SEEL':'Seelos Therapeutics Inc. ',
     'SEER':'Seer Inc.  ',
     'SEIC':'SEI Investments Company ',
     'SELB':'Selecta Biosciences Inc. ',
     'SELF':'Global Self Storage Inc. ',
     'SEM':'Select Medical Holdings Corporation ',
     'SEMR':'SEMrush Holdings Inc.  ',
     'SENEA':'Seneca Foods Corp.  ',
     'SENEB':'Seneca Foods Corp. Class B ',
     'SENS':'Senseonics Holdings Inc. ',
     'SEPA':'SEP Acquisition Corp  ',
     'SEPAU':'SEP Acquisition Corp Unit',
     'SEPAW':'SEP Acquisition Corp s',
     'SERA':'Sera Prognostics Inc.  ',
     'SES':'SES AI Corporation  ',
     'SEV':'Sono Group N.V. ',
     'SEVN':'Seven Hills Realty Trust ',
     'SF':'Stifel Financial Corporation ',
     'SFB':'Stifel Financial Corporation 5.20% Senior Notes due 2047',
     'SFBC':'Sound Financial Bancorp Inc. ',
     'SFBS':'ServisFirst Bancshares Inc. ',
     'SFE':'Safeguard Scientifics Inc. ',
     'SFIX':'Stitch Fix Inc.  ',
     'SFL':'SFL Corporation Ltd',
     'SFM':'Sprouts Farmers Market Inc. ',
     'SFNC':'Simmons First National Corporation  ',
     'SFR':'Appreciate Holdings Inc.  ',
     'SFST':'Southern First Bancshares Inc. ',
     'SFT':'Shift Technologies Inc.  ',
     'SFWL':'Shengfeng Development Limited ',
     'SG':'Sweetgreen Inc.  ',
     'SGA':'Saga Communications Inc.   (FL)',
     'SGBX':'Safe & Green Holdings Corp. ',
     'SGC':'Superior Group of Companies Inc. ',
     'SGE':'Strong Global Entertainment Inc.  Common Voting Shares',
     'SGEN':'Seagen Inc. ',
     'SGH':'SMART Global Holdings Inc. ',
     'SGHC':'Super Group (SGHC) Limited ',
     'SGHT':'Sight Sciences Inc. ',
     'SGII':'Seaport Global Acquisition II Corp.  ',
     'SGIIW':'Seaport Global Acquisition II Corp. s',
     'SGLY':'Singularity Future Technology Ltd. ',
     'SGMA':'SigmaTron International Inc. ',
     'SGML':'Sigma Lithium Corporation ',
     'SGMO':'Sangamo Therapeutics Inc. ',
     'SGRP':'SPAR Group Inc. ',
     'SGRY':'Surgery Partners Inc. ',
     'SGTX':'Sigilon Therapeutics Inc. ',
     'SGU':'Star Group L.P. ',
     'SHAK':'Shake Shack Inc.  ',
     'SHAP':'Spree Acquisition Corp. 1 Limited ',
     'SHBI':'Shore Bancshares Inc ',
     'SHC':'Sotera Health Company ',
     'SHCO':'Soho House & Co Inc.  ',
     'SHCR':'Sharecare Inc.  ',
     'SHCRW':'Sharecare Inc. ',
     'SHEL':'Royal Dutch Shell PLC  (each representing two (2) )',
     'SHEN':'Shenandoah Telecommunications Co ',
     'SHFS':'SHF Holdings Inc.  ',
     'SHFSW':'SHF Holdings Inc. s',
     'SHG':'Shinhan Financial Group Co Ltd ',
     'SHIP':'Seanergy Maritime Holdings Corp. ',
     'SHLS':'Shoals Technologies Group Inc.  ',
     'SHLT':'SHL Telemedicine Ltd ',
     'SHO':'Sunstone Hotel Investors Inc. Sunstone Hotel Investors Inc. ',
     'SHOO':'Steven Madden Ltd. ',
     'SHOP':'Shopify Inc.',
     'SHPH':'Shuttle Pharmaceuticals Holdings Inc. ',
     'SHPW':'Shapeways Holdings Inc. ',
     'SHUA':'SHUAA Partners Acquisition Corp I',
     'SHUAW':'SHUAA Partners Acquisition Corp I ',
     'SHW':'Sherwin-Williams Company ',
     'SHYF':'The Shyft Group Inc. ',
     'SIBN':'SI-BONE Inc. ',
     'SID':'Companhia Siderurgica Nacional S.A. ',
     'SIDU':'Sidus Space Inc.  ',
     'SIEB':'Siebert Financial Corp. ',
     'SIEN':'Sientra Inc. ',
     'SIF':'SIFCO Industries Inc. ',
     'SIFY':'Sify Technologies Limited ',
     'SIG':'Signet Jewelers Limited ',
     'SIGA':'SIGA Technologies Inc. ',
     'SIGI':'Selective Insurance Group Inc. ',
     'SII':'Sprott Inc. ',
     'SILC':'Silicom Ltd ',
     'SILK':'Silk Road Medical Inc. ',
     'SILO':'Silo Pharma Inc. ',
     'SILV':'SilverCrest Metals Inc. ',
     'SIM':'Grupo Simec S.A.B. de C.V. ',
     'SIMO':'Silicon Motion Technology Corporation ',
     'SINT':'SiNtx Technologies Inc. ',
     'SIRI':'Sirius XM Holdings Inc. ',
     'SISI':'Shineco Inc. ',
     'SITC':'SITE Centers Corp. ',
     'SITC^A':'SITE Centers Corp. 6.375%  Preferred Shares',
     'SITE':'SiteOne Landscape Supply Inc. ',
     'SITM':'SiTime Corporation ',
     'SIX':'Six Flags Entertainment Corporation New ',
     'SJ':'Scienjoy Holding Corporation ',
     'SJM':'J.M. Smucker Company ',
     'SJT':'San Juan Basin Royalty Trust ',
     'SJW':'SJW Group  (DE)',
     'SKE':'Skeena Resources Limited ',
     'SKGR':'SK Growth Opportunities Corporation  ',
     'SKGRW':'SK Growth Opportunities Corporation ',
     'SKIL':'Skillsoft Corp.  ',
     'SKIN':'The Beauty Health Company  ',
     'SKLZ':'Skillz Inc.  ',
     'SKM':'SK Telecom Co. Ltd. ',
     'SKT':'Tanger Factory Outlet Centers Inc. ',
     'SKWD':'Skyward Specialty Insurance Group Inc. ',
     'SKX':'Skechers U.S.A. Inc. ',
     'SKY':'Skyline Champion Corporation ',
     'SKYH':'Sky Harbour Group Corporation  ',
     'SKYT':'SkyWater Technology Inc. ',
     'SKYW':'SkyWest Inc. ',
     'SKYX':'SKYX Platforms Corp. ',
     'SLAB':'Silicon Laboratories Inc. ',
     'SLAC':'Social Leverage Acquisition Corp I  ',
     'SLAM':'Slam Corp.',
     'SLAMU':'Slam Corp. Unit',
     'SLAMW':'Slam Corp. ',
     'SLB':'Schlumberger N.V. ',
     'SLCA':'U.S. Silica Holdings Inc. ',
     'SLDB':'Solid Biosciences Inc. ',
     'SLDP':'Solid Power Inc.  ',
     'SLDPW':'Solid Power Inc. ',
     'SLF':'Sun Life Financial Inc. ',
     'SLG':'SL Green Realty Corp ',
     'SLGC':'SomaLogic Inc.  ',
     'SLGCW':'SomaLogic Inc. ',
     'SLGG':'Super League Gaming Inc. ',
     'SLGL':'Sol-Gel Technologies Ltd. ',
     'SLGN':'Silgan Holdings Inc. ',
     'SLI':'Standard Lithium Ltd. ',
     'SLM':'SLM Corporation ',
     'SLMBP':'SLM Corporation Floating Rate Non-Cumulative Preferred Stock Series B',
     'SLN':'Silence Therapeutics Plc American Depository Share',
     'SLNA':'Selina Hospitality PLC ',
     'SLNAW':'Selina Hospitality PLC ',
     'SLND':'Southland Holdings Inc. ',
     'SLNG':'Stabilis Solutions Inc. ',
     'SLNH':'Soluna Holdings Inc. ',
     'SLNO':'Soleno Therapeutics Inc. ',
     'SLP':'Simulations Plus Inc. ',
     'SLQT':'SelectQuote Inc. ',
     'SLRC':'SLR Investment Corp. ',
     'SLRN':'ACELYRIN INC. ',
     'SLRX':'Salarius Pharmaceuticals Inc. ',
     'SLS':'SELLAS Life Sciences Group Inc. ',
     'SLVM':'Sylvamo Corporation ',
     'SLVR':'SilverSPAC Inc.',
     'SLVRU':'SilverSPAC Inc. Unit',
     'SLVRW':'SilverSPAC Inc. ',
     'SM':'SM Energy Company ',
     'SMAP':'SportsMap Tech Acquisition Corp. ',
     'SMAPU':'SportsMap Tech Acquisition Corp. Units',
     'SMAPW':'SportsMap Tech Acquisition Corp. s',
     'SMAR':'Smartsheet Inc.  ',
     'SMBC':'Southern Missouri Bancorp Inc. ',
     'SMBK':'SmartFinancial Inc. ',
     'SMCI':'Super Micro Computer Inc. ',
     'SMFG':'Sumitomo Mitsui Financial Group Inc Unsponsored  (Japan)',
     'SMFL':'Smart for Life Inc. ',
     'SMG':'Scotts Miracle-Gro Company ',
     'SMHI':'SEACOR Marine Holdings Inc. ',
     'SMID':'Smith-Midland Corporation ',
     'SMLP':'Summit Midstream Partners LP Common Units Representing Limited Partner Interests',
     'SMLR':'Semler Scientific Inc. ',
     'SMMF':'Summit Financial Group Inc. ',
     'SMMT':'Summit Therapeutics Inc. ',
     'SMP':'Standard Motor Products Inc. ',
     'SMPL':'The Simply Good Foods Company ',
     'SMR':'NuScale Power Corporation  ',
     'SMRT':'SmartRent Inc.  ',
     'SMSI':'Smith Micro Software Inc. ',
     'SMTC':'Semtech Corporation ',
     'SMTI':'Sanara MedTech Inc. ',
     'SMWB':'Similarweb Ltd. ',
     'SMX':'SMX (Security Matters) Public Limited Company ',
     'SMXWW':'SMX (Security Matters) Public Limited Company ',
     'SNA':'Snap-On Incorporated ',
     'SNAL':'Snail Inc.  ',
     'SNAP':'Snap Inc.  ',
     'SNAX':'Stryve Foods Inc.  ',
     'SNAXW':'Stryve Foods Inc. ',
     'SNBR':'Sleep Number Corporation ',
     'SNCE':'Science 37 Holdings Inc. ',
     'SNCR':'Synchronoss Technologies Inc. ',
     'SNCRL':'Synchronoss Technologies Inc. 8.375% Senior Notes due 2026',
     'SNCY':'Sun Country Airlines Holdings Inc. ',
     'SND':'Smart Sand Inc. ',
     'SNDA':'Sonida Senior Living Inc. ',
     'SNDL':'SNDL Inc. ',
     'SNDR':'Schneider National Inc. ',
     'SNDX':'Syndax Pharmaceuticals Inc. ',
     'SNES':'SenesTech Inc. ',
     'SNEX':'StoneX Group Inc. ',
     'SNFCA':'Security National Financial Corporation  ',
     'SNGX':'Soligenix Inc. ',
     'SNN':'Smith & Nephew SNATS Inc. ',
     'SNOA':'Sonoma Pharmaceuticals Inc. ',
     'SNOW':'Snowflake Inc.  ',
     'SNPO':'Snap One Holdings Corp. ',
     'SNPS':'Synopsys Inc. ',
     'SNPX':'Synaptogenix Inc. ',
     'SNSE':'Sensei Biotherapeutics Inc. ',
     'SNT':'Senstar Technologies Ltd. ',
     'SNTG':'Sentage Holdings Inc. ',
     'SNTI':'Senti Biosciences Inc. ',
     'SNV':'Synovus Financial Corp. ',
     'SNX':'TD SYNNEX Corporation ',
     'SNY':'Sanofi ADS',
     'SNYNF':'Sanofi',
     'SO':'Southern Company ',
     'SOBR':'SOBR Safe Inc. ',
     'SOFI':'SoFi Technologies Inc. ',
     'SOFO':'Sonic Foundry Inc. ',
     'SOHO':'Sotherly Hotels Inc. ',
     'SOHU':'Sohu.com Limited ',
     'SOI':'Solaris Oilfield Infrastructure Inc.  ',
     'SOL':'Emeren Group Ltd  each representing 10 shares',
     'SOLO':'Electrameccanica Vehicles Corp. Ltd. ',
     'SOLOW':'Electrameccanica Vehicles Corp. Ltd. s',
     'SOLV':'Solventum Corporation',
     'SON':'Sonoco Products Company ',
     'SOND':'Sonder Holdings Inc.  ',
     'SONDW':'Sonder Holdings Inc. s',
     'SONM':'Sonim Technologies Inc. ',
     'SONN':'Sonnet BioTherapeutics Holdings Inc. ',
     'SONO':'Sonos Inc. ',
     'SONX':'Sonendo Inc. ',
     'SONY':'Sony Group Corporation ',
     'SOPA':'Society Pass Incorporated ',
     'SOPH':'SOPHiA GENETICS SA ',
     'SOR':'Source Capital Inc. ',
     'SOS':'SOS Limited ',
     'SOTK':'Sono-Tek Corporation ',
     'SOUN':'SoundHound AI Inc  ',
     'SOUNW':'SoundHound AI Inc. ',
     'SOVO':'Sovos Brands Inc. ',
     'SP':'SP Plus Corporation ',
     'SPB':'Spectrum Brands Holdings Inc. ',
     'SPCB':'SuperCom Ltd.  (Israel)',
     'SPCE':'Virgin Galactic Holdings Inc. ',
     'SPE':'Special Opportunities Fund Inc ',
     'SPFI':'South Plains Financial Inc. ',
     'SPG':'Simon Property Group Inc. ',
     'SPGI':'S&P Global Inc. ',
     'SPH':'Suburban Propane Partners L.P. ',
     'SPHR':'Sphere Entertainment Co.  ',
     'SPI':'SPI Energy Co. Ltd. ',
     'SPIR':'Spire Global Inc.  ',
     'SPLK':'Splunk Inc. ',
     'SPLP':'Steel Partners Holdings LP LTD PARTNERSHIP UNIT',
     'SPNS':'Sapiens International Corporation N.V.  (Cayman Islands)',
     'SPNT':'SiriusPoint Ltd. ',
     'SPOK':'Spok Holdings Inc. ',
     'SPOT':'Spotify Technology S.A. ',
     'SPPI':'Spectrum Pharmaceuticals Inc.',
     'SPR':'Spirit Aerosystems Holdings Inc. ',
     'SPRB':'Spruce Biosciences Inc. ',
     'SPRC':'SciSparc Ltd. ',
     'SPRO':'Spero Therapeutics Inc. ',
     'SPRU':'Spruce Power Holding Corporation  ',
     'SPRY':'ARS Pharmaceuticals Inc. ',
     'SPSC':'SPS Commerce Inc. ',
     'SPT':'Sprout Social Inc  ',
     'SPTN':'SpartanNash Company ',
     'SPWH':'Sportsmans Warehouse Holdings Inc. ',
     'SPWR':'SunPower Corporation ',
     'SPXC':'SPX Technologies Inc. ',
     'SPXX':'Nuveen S&P 500 Dynamic Overwrite Fund',
     'SQ':'Block Inc.  ',
     'SQFT':'Presidio Property Trust Inc.  ',
     'SQL':'SeqLL Inc. ',
     'SQLLW':'SeqLL Inc. ',
     'SQM':'Sociedad Quimica y Minera S.A. ',
     'SQNS':'Sequans Communications S.A. ',
     'SQSP':'Squarespace Inc.  ',
     'SR':'Spire Inc. ',
     'SRAD':'Sportradar Group AG ',
     'SRC':'Spirit Realty Capital Inc. ',
     'SRCE':'1st Source Corporation ',
     'SRCL':'Stericycle Inc. ',
     'SRDX':'Surmodics Inc. ',
     'SRE':'DBA Sempra ',
     'SREA':'DBA Sempra 5.750% Junior Subordinated Notes due 2079',
     'SRG':'Seritage Growth Properties  ',
     'SRI':'Stoneridge Inc. ',
     'SRL':'Scully Royalty Ltd.',
     'SRPT':'Sarepta Therapeutics Inc.  (DE)',
     'SRRK':'Scholar Rock Holding Corporation ',
     'SRT':'StarTek Inc. ',
     'SRTS':'Sensus Healthcare Inc. ',
     'SRV':'NXG Cushing Midstream Energy Fund  of Beneficial Interest',
     'SRZN':'Surrozen Inc. ',
     'SRZNW':'Surrozen Inc. ',
     'SSB':'SouthState Corporation ',
     'SSBI':'Summit State Bank ',
     'SSBK':'Southern States Bancshares Inc. ',
     'SSD':'Simpson Manufacturing Company Inc. ',
     'SSIC':'Silver Spike Investment Corp. ',
     'SSKN':'Strata Skin Sciences Inc. ',
     'SSL':'Sasol Ltd. ',
     'SSNC':'SS&C Technologies Holdings Inc. ',
     'SSNT':'SilverSun Technologies Inc. ',
     'SSP':'E.W. Scripps Company  ',
     'SSRM':'SSR Mining Inc. ',
     'SSSS':'SuRo Capital Corp. ',
     'SSSSL':'SuRo Capital Corp. 6.00% Notes due 2026',
     'SST':'System1 Inc.  ',
     'SSTI':'SoundThinking Inc. ',
     'SSTK':'Shutterstock Inc. ',
     'SSU':'SIGNA Sports United N.V. ',
     'SSY':'SunLink Health Systems Inc. ',
     'SSYS':'Stratasys Ltd.  (Israel)',
     'ST':'Sensata Technologies Holding plc ',
     'STAA':'STAAR Surgical Company ',
     'STAF':'Staffing 360 Solutions Inc.  (DE)',
     'STAG':'Stag Industrial Inc. ',
     'STBA':'S&T Bancorp Inc. ',
     'STBX':'Starbox Group Holdings Ltd. ',
     'STC':'Stewart Information Services Corporation ',
     'STCN':'Steel Connect Inc. ',
     'STE':'STERIS plc (Ireland) ',
     'STEL':'Stellar Bancorp Inc. ',
     'STEM':'Stem Inc.  ',
     'STEP':'StepStone Group Inc.  ',
     'STER':'Sterling Check Corp. ',
     'STEW':'SRH Total Return Fund Inc. ',
     'STG':'Sunlands Technology Group  representing ',
     'STGW':'Stagwell Inc.  ',
     'STHO':'Star Holdings Shares of Beneficial Interest',
     'STIM':'Neuronetics Inc. ',
     'STIX':'Semantix Inc. ',
     'STIXW':'Semantix Inc. ',
     'STK':'Columbia Seligman Premium Technology Growth Fund Inc',
     'STKH':'Steakholder Foods Ltd. ',
     'STKL':'SunOpta Inc. ',
     'STKS':'The ONE Group Hospitality Inc. ',
     'STLA':'Stellantis N.V. ',
     'STLD':'Steel Dynamics Inc.',
     'STM':'STMicroelectronics N.V. ',
     'STN':'Stantec Inc ',
     'STNE':'StoneCo Ltd.  ',
     'STNG':'Scorpio Tankers Inc. ',
     'STOK':'Stoke Therapeutics Inc. ',
     'STR':'Sitio Royalties Corp.  ',
     'STRA':'Strategic Education Inc. ',
     'STRC':'Sarcos Technology and Robotics Corporation ',
     'STRCW':'Sarcos Technology and Robotics Corporation s',
     'STRL':'Sterling Infrastructure Inc. ',
     'STRM':'Streamline Health Solutions Inc. ',
     'STRO':'Sutro Biopharma Inc. ',
     'STRR':'Star Equity Holdings Inc. ',
     'STRRP':'Star Equity Holdings Inc. Series A Cumulative Perpetual Preferred Stock',
     'STRS':'Stratus Properties Inc. ',
     'STRT':'STRATTEC SECURITY CORPORATION ',
     'STRW':'Strawberry Fields REIT Inc. ',
     'STSS':'Sharps Technology Inc. ',
     'STSSW':'Sharps Technology Inc. ',
     'STT':'State Street Corporation ',
     'STTK':'Shattuck Labs Inc. ',
     'STVN':'Stevanato Group S.p.A. ',
     'STWD':'STARWOOD PROPERTY TRUST INC. Starwood Property Trust Inc.',
     'STX':'Seagate Technology Holdings PLC  (Ireland)',
     'STXS':'Stereotaxis Inc. ',
     'STZ':'Constellation Brands Inc. ',
     'SU':'Suncor Energy  Inc. ',
     'SUAC':'ShoulderUp Technology Acquisition Corp.  ',
     'SUI':'Sun Communities Inc. ',
     'SUM':'Summit Materials Inc.  ',
     'SUN':'Sunoco LP Common Units representing limited partner interests',
     'SUNL':'Sunlight Financial Holdings Inc.  ',
     'SUNW':'Sunworks Inc. ',
     'SUP':'Superior Industries International Inc.  (DE)',
     'SUPN':'Supernus Pharmaceuticals Inc. ',
     'SUPV':'Grupo Supervielle S.A.  each Representing five Class B shares',
     'SURF':'Surface Oncology Inc. ',
     'SURG':'SurgePays Inc. ',
     'SURGW':'SurgePays Inc. ',
     'SUZ':'Suzano S.A.  (each representing One )',
     'SVC':'Service Properties Trust ',
     'SVFD':'Save Foods Inc. ',
     'SVII':'Spring Valley Acquisition Corp. II ',
     'SVIIR':'Spring Valley Acquisition Corp. II Rights',
     'SVIIU':'Spring Valley Acquisition Corp. II Unit',
     'SVIIW':'Spring Valley Acquisition Corp. II ',
     'SVM':'Silvercorp Metals Inc. ',
     'SVRA':'Savara Inc. ',
     'SVRE':'SaverOne 2014 Ltd. ',
     'SVT':'Servotronics Inc. ',
     'SVV':'Savers Value Village Inc. ',
     'SVVC':'Firsthand Technology Value Fund Inc. ',
     'SWAG':'Stran & Company Inc. ',
     'SWAGW':'Stran & Company Inc. ',
     'SWAV':'ShockWave Medical Inc. ',
     'SWBI':'Smith & Wesson Brands Inc. ',
     'SWI':'SolarWinds Corporation ',
     'SWIM':'Latham Group Inc. ',
     'SWK':'Stanley Black & Decker Inc. ',
     'SWKH':'SWK Holdings Corporation ',
     'SWKS':'Skyworks Solutions Inc. ',
     'SWN':'Southwestern Energy Company ',
     'SWSS':'Springwater Special Situations Corp. ',
     'SWTX':'SpringWorks Therapeutics Inc. ',
     'SWVL':'Swvl Holdings Corp  ',
     'SWVLW':'Swvl Holdings Corp ',
     'SWX':'Southwest Gas Holdings Inc.  (DE)',
     'SWZ':'Swiss Helvetia Fund Inc. ',
     'SXC':'SunCoke Energy Inc. ',
     'SXI':'Standex International Corporation ',
     'SXT':'Sensient Technologies Corporation ',
     'SXTC':'China SXT Pharmaceuticals Inc. ',
     'SY':'So-Young International Inc. American Depository Shares',
     'SYBT':'Stock Yards Bancorp Inc. ',
     'SYBX':'Synlogic Inc. ',
     'SYF':'Synchrony Financial ',
     'SYK':'Stryker Corporation ',
     'SYM':'Symbotic Inc.  ',
     'SYNA':'Synaptics Incorporated  $0.001 Par Value',
     'SYNH':'Syneos Health Inc.  ',
     'SYPR':'Sypris Solutions Inc. ',
     'SYRS':'Syros Pharmaceuticals Inc. ',
     'SYT':'SYLA Technologies Co. Ltd. ',
     'SYTA':'Siyata Mobile Inc. ',
     'SYTAW':'Siyata Mobile Inc. ',
     'SYY':'Sysco Corporation ',
     'SZZL':'Sizzle Acquisition Corp. ',
     'SZZLW':'Sizzle Acquisition Corp. ',
     'T':'AT&T Inc.',
     'TAC':'TransAlta Corporation ',
     'TACT':'TransAct Technologies Incorporated ',
     'TAIT':'Taitron Components Incorporated  ',
     'TAK':'Takeda Pharmaceutical Company Limited  (each representing 1/2 of a share of )',
     'TAL':'TAL Education Group ',
     'TALK':'Talkspace Inc. ',
     'TALKW':'Talkspace Inc. ',
     'TALO':'Talos Energy Inc. ',
     'TALS':'Talaris Therapeutics Inc. ',
     'TANH':'Tantech Holdings Ltd. ',
     'TAOP':'Taoping Inc. ',
     'TAP':'Molson Coors Beverage Company Class B ',
     'TARA':'Protara Therapeutics Inc.  ',
     'TARO':'Taro Pharmaceutical Industries Ltd. ',
     'TARS':'Tarsus Pharmaceuticals Inc. ',
     'TASK':'TaskUs Inc.  ',
     'TAST':'Carrols Restaurant Group Inc. ',
     'TATT':'TAT Technologies Ltd. ',
     'TAYD':'Taylor Devices Inc. ',
     'TBB':'AT&T Inc. 5.350% Global Notes due 2066',
     'TBBK':'The Bancorp Inc ',
     'TBC':'AT&T Inc. 5.625% Global Notes due 2067',
     'TBCP':'Thunder Bridge Capital Partners III Inc.  ',
     'TBI':'TrueBlue Inc. ',
     'TBIO':'Telesis Bio Inc. ',
     'TBLA':'Taboola.com Ltd. ',
     'TBLAW':'Taboola.com Ltd. ',
     'TBLD':'Thornburg Income Builder Opportunities Trust ',
     'TBLT':'ToughBuilt Industries Inc. ',
     'TBLTW':'ToughBuilt Industries Inc. ',
     'TBMC':'Trailblazer Merger Corporation I  ',
     'TBMCR':'Trailblazer Merger Corporation I Rights',
     'TBNK':'Territorial Bancorp Inc. ',
     'TBPH':'Theravance Biopharma Inc. ',
     'TC':'TuanChe Limited ',
     'TCBC':'TC Bancshares Inc. ',
     'TCBI':'Texas Capital Bancshares Inc. ',
     'TCBK':'TriCo Bancshares ',
     'TCBP':'TC BioPharm (Holdings) plc ',
     'TCBPW':'TC BioPharm (Holdings) plc s',
     'TCBS':'Texas Community Bancshares Inc. ',
     'TCBX':'Third Coast Bancshares Inc. ',
     'TCI':'Transcontinental Realty Investors Inc. ',
     'TCJH':'Top KingWin Ltd ',
     'TCMD':'Tactile Systems Technology Inc. ',
     'TCN':'Tricon Residential Inc. ',
     'TCOA':'Zalatoris Acquisition Corp.  ',
     'TCOM':'Trip.com Group Limited ',
     'TCON':'TRACON Pharmaceuticals Inc. ',
     'TCPC':'BlackRock TCP Capital Corp. ',
     'TCRT':'Alaunos Therapeutics Inc. ',
     'TCRX':'TScan Therapeutics Inc. ',
     'TCS':'Container Store ',
     'TCX':'Tucows Inc.  ',
     'TD':'Toronto Dominion Bank ',
     'TDC':'Teradata Corporation ',
     'TDCX':'TDCX Inc.  each representing one',
     'TDF':'Templeton Dragon Fund Inc. ',
     'TDG':'Transdigm Group Incorporated ',
     'TDOC':'Teladoc Health Inc. ',
     'TDS':'Telephone and Data Systems Inc. ',
     'TDUP':'ThredUp Inc.  ',
     'TDW':'Tidewater Inc. ',
     'TDY':'Teledyne Technologies Incorporated ',
     'TEAF':'Ecofin Sustainable and Social Impact Term Fund',
     'TEAM':'Atlassian Corporation  ',
     'TECH':'Bio-Techne Corp ',
     'TECK':'Teck Resources Ltd ',
     'TECTP':'Tectonic Financial Inc. 9.00% Fixed-to-Floating Rate Series B Non-Cumulative Perpetual Preferred Stock',
     'TEDU':'Tarena International Inc. ',
     'TEF':'Telefonica SA ',
     'TEI':'Templeton Emerging Markets Income Fund Inc. ',
     'TEL':'TE Connectivity Ltd. New Switzerland Registered Shares',
     'TELA':'TELA Bio Inc. ',
     'TELL':'Tellurian Inc. ',
     'TELZ':'Tellurian Inc. 8.25% Senior Notes due 2028',
     'TENB':'Tenable Holdings Inc. ',
     'TENK':'TenX Keane Acquisition ',
     'TENKR':'TenX Keane Acquisition Right',
     'TENX':'Tenax Therapeutics Inc. ',
     'TEO':'Telecom Argentina SA',
     'TER':'Teradyne Inc. ',
     'TERN':'Terns Pharmaceuticals Inc. ',
     'TESS':'TESSCO Technologies Incorporated ',
     'TETE':'Technology & Telecommunication Acquisition Corporation ',
     'TETEW':'Technology & Telecommunication Acquisition Corporation ',
     'TEVA':'Teva Pharmaceutical Industries Limited ',
     'TEX':'Terex Corporation ',
     'TFC':'Truist Financial Corporation ',
     'TFFP':'TFF Pharmaceuticals Inc. ',
     'TFII':'TFI International Inc. ',
     'TFIN':'Triumph Financial Inc. ',
     'TFPM':'Triple Flag Precious Metals Corp. ',
     'TFSL':'TFS Financial Corporation ',
     'TFX':'Teleflex Incorporated ',
     'TG':'Tredegar Corporation ',
     'TGAA':'Target Global Acquisition I Corp.',
     'TGAN':'Transphorm Inc. ',
     'TGB':'Taseko Mines Ltd. ',
     'TGH':'Textainer Group Holdings Limited ',
     'TGI':'Triumph Group Inc. ',
     'TGL':'Treasure Global Inc. ',
     'TGLS':'Tecnoglass Inc. ',
     'TGNA':'TEGNA Inc',
     'TGS':'Transportadora de Gas del Sur SA TGS ',
     'TGT':'Target Corporation ',
     'TGTX':'TG Therapeutics Inc. ',
     'TGVC':'TG Venture Acquisition Corp.  ',
     'TGVCW':'TG Venture Acquisition Corp. s',
     'TH':'Target Hospitality Corp. ',
     'THC':'Tenet Healthcare Corporation ',
     'THCH':'TH International Limited ',
     'THCP':'Thunder Bridge Capital Partners IV Inc.  ',
     'THFF':'First Financial Corporation Indiana ',
     'THG':'Hanover Insurance Group Inc',
     'THM':'International Tower Hill Mines Ltd.  (Canada)',
     'THMO':'ThermoGenesis Holdings Inc. ',
     'THO':'Thor Industries Inc. ',
     'THQ':'Tekla Healthcare Opportunies Fund Shares of Beneficial Interest',
     'THR':'Thermon Group Holdings Inc. ',
     'THRD':'Third Harmonic Bio Inc. ',
     'THRM':'Gentherm Inc ',
     'THRN':'Thorne Healthtech Inc. ',
     'THRX':'Theseus Pharmaceuticals Inc. ',
     'THRY':'Thryv Holdings Inc. ',
     'THS':'Treehouse Foods Inc. ',
     'THTX':'Theratechnologies Inc. ',
     'THW':'Tekla World Healthcare Fund Shares of Beneficial Interest',
     'THWWW':'Target Hospitality Corp.  expiring 3/15/2024',
     'TIGO':'Millicom International Cellular S.A. ',
     'TIGR':'UP Fintech Holding Ltd  representing fifteen ',
     'TIL':'Instil Bio Inc. ',
     'TILE':'Interface Inc. ',
     'TIMB':'TIM S.A.  (Each representing 5 )',
     'TIO':'Tingo Group Inc. ',
     'TIPT':'Tiptree Inc. ',
     'TIRX':'TIAN RUIXIANG Holdings Ltd ',
     'TISI':'Team Inc. ',
     'TITN':'Titan Machinery Inc. ',
     'TIVC':'Tivic Health Systems Inc. ',
     'TIXT':'TELUS International (Cda) Inc. Subordinate Voting Shares',
     'TJX':'TJX Companies Inc. ',
     'TK':'Teekay Corporation ',
     'TKAMY':'Thyssenkrupp AG ADR',
     'TKAT':'Takung Art Co. Ltd. ',
     'TKC':'Turkcell Iletisim Hizmetleri AS ',
     'TKLF':'Yoshitsu Co. Ltd ',
     'TKNO':'Alpha Teknova Inc. ',
     'TKR':'Timken Company ',
     'TLF':'Tandy Leather Factory Inc. ',
     'TLGA':'TLG Acquisition One Corp.  ',
     'TLGY':'TLGY Acquisition Corporation',
     'TLIS':'Talis Biomedical Corporation ',
     'TLK':'PT Telekomunikasi Indonesia Tbk',
     'TLRY':'Tilray Brands Inc. ',
     'TLS':'Telos Corporation ',
     'TLSA':'Tiziana Life Sciences Ltd. ',
     'TLYS':'Tillys Inc. ',
     'TM':'Toyota Motor Corporation ',
     'TMBR':'Timber Pharmaceuticals Inc. ',
     'TMC':'TMC the metals company Inc. ',
     'TMCI':'Treace Medical Concepts Inc. ',
     'TMCWW':'TMC the metals company Inc. s',
     'TMDX':'TransMedics Group Inc. ',
     'TME':'Tencent Music Entertainment Group  each representing two ',
     'TMHC':'Taylor Morrison Home Corporation ',
     'TMKR':'Tastemaker Acquisition Corp.  ',
     'TMKRU':'Tastemaker Acquisition Corp. Unit',
     'TMKRW':'Tastemaker Acquisition Corp.  to purchase  ',
     'TMO':'Thermo Fisher Scientific Inc ',
     'TMP':'Tompkins Financial Corporation ',
     'TMPO':'Tempo Automation Holdings Inc. ',
     'TMQ':'Trilogy Metals Inc. ',
     'TMST':'TimkenSteel Corporation ',
     'TMTCR':'TMT Acquisition Corp Rights',
     'TMUS':'T-Mobile US Inc. ',
     'TNC':'Tennant Company ',
     'TNDM':'Tandem Diabetes Care Inc. ',
     'TNET':'TriNet Group Inc. ',
     'TNGX':'Tango Therapeutics Inc.',
     'TNK':'Teekay Tankers Ltd.',
     'TNL':'Travel Leisure Co. Common  Stock',
     'TNON':'Tenon Medical Inc. ',
     'TNONW':'Tenon Medical Inc. ',
     'TNP':'Tsakos Energy Navigation Ltd ',
     'TNXP':'Tonix Pharmaceuticals Holding Corp. ',
     'TNYA':'Tenaya Therapeutics Inc. ',
     'TOI':'The Oncology Institute Inc. ',
     'TOIIW':'The Oncology Institute Inc. ',
     'TOL':'Toll Brothers Inc. ',
     'TOMZ':'TOMI Environmental Solutions Inc. ',
     'TOON':'Kartoon Studios Inc. ',
     'TOP':'TOP Financial Group Limited ',
     'TOPS':'TOP Ships Inc. ',
     'TORO':'Toro Corp. ',
     'TOST':'Toast Inc.  ',
     'TOUR':'Tuniu Corporation ',
     'TOVX':'Theriva Biologics Inc. ',
     'TOWN':'TowneBank ',
     'TPB':'Turning Point Brands Inc. ',
     'TPC':'Tutor Perini Corporation ',
     'TPCS':'TechPrecision Corporation ',
     'TPET':'Trio Petroleum Corp. ',
     'TPG':'TPG Inc.  ',
     'TPH':'Tri Pointe Homes Inc. ',
     'TPHS':'Trinity Place Holdings Inc. ',
     'TPIC':'TPI Composites Inc. ',
     'TPL':'Texas Pacific Land Corporation ',
     'TPR':'Tapestry Inc. ',
     'TPST':'Tempest Therapeutics Inc. ',
     'TPTA':'Terra Property Trust Inc. 6.00% Notes due 2026',
     'TPVG':'TriplePoint Venture Growth BDC Corp. ',
     'TPX':'Tempur Sealy International Inc. ',
     'TPZ':'Tortoise Power and Energy Infrastructure Fund Inc ',
     'TR':'Tootsie Roll Industries Inc. ',
     'TRC':'Tejon Ranch Co ',
     'TRCA':'Twin Ridge Capital Acquisition Corp. ',
     'TRDA':'Entrada Therapeutics Inc. ',
     'TREE':'LendingTree Inc. ',
     'TREX':'Trex Company Inc. ',
     'TRGP':'Targa Resources Inc. ',
     'TRHC':'Tabula Rasa HealthCare Inc. ',
     'TRI':'Thomson Reuters Corp ',
     'TRIB':'Trinity Biotech plc ',
     'TRIN':'Trinity Capital Inc. ',
     'TRINL':'Trinity Capital Inc. 7.00% Notes Due 2025',
     'TRIP':'TripAdvisor Inc. ',
     'TRIS':'Tristar Acquisition I Corp. ',
     'TRKA':'Troika Media Group Inc. ',
     'TRKAW':'Troika Media Group Inc. ',
     'TRMB':'Trimble Inc. ',
     'TRMD':'TORM plc  ',
     'TRMK':'Trustmark Corporation ',
     'TRMR':'Tremor International Ltd. American Depository Shares',
     'TRN':'Trinity Industries Inc. ',
     'TRNO':'Terreno Realty Corporation ',
     'TRNR':'Interactive Strength Inc. ',
     'TRNS':'Transcat Inc. ',
     'TRON':'Corner Growth Acquisition Corp. 2',
     'TROO':'TROOPS Inc. ',
     'TROW':'T. Rowe Price Group Inc. ',
     'TROX':'Tronox Holdings plc  (UK)',
     'TRP':'TC Energy Corporation ',
     'TRS':'TriMas Corporation ',
     'TRST':'TrustCo Bank Corp NY ',
     'TRT':'Trio-Tech International ',
     'TRTL':'TortoiseEcofin Acquisition Corp. III ',
     'TRTN':'Triton International Limited ',
     'TRU':'TransUnion ',
     'TRUE':'TrueCar Inc. ',
     'TRUP':'Trupanion Inc. ',
     'TRV':'The Travelers Companies Inc. ',
     'TRVG':'trivago N.V. ',
     'TRVI':'Trevi Therapeutics Inc. ',
     'TRVN':'Trevena Inc. ',
     'TRX':'TRX Gold Corporation ',
     'TS':'Tenaris S.A. ',
     'TSAT':'Telesat Corporation   and Class B Variable Voting Shares',
     'TSBK':'Timberland Bancorp Inc. ',
     'TSCO':'Tractor Supply Company ',
     'TSE':'Trinseo PLC ',
     'TSEM':'Tower Semiconductor Ltd. ',
     'TSHA':'Taysha Gene Therapies Inc. ',
     'TSI':'TCW Strategic Income Fund Inc. ',
     'TSLA':'Tesla Inc. ',
     'TSLX':'Sixth Street Specialty Lending Inc. ',
     'TSM':'Taiwan Semiconductor Manufacturing Company Ltd.',
     'TSN':'Tyson Foods Inc. ',
     'TSP':'TuSimple Holdings Inc.  ',
     'TSQ':'Townsquare Media Inc.  ',
     'TSRI':'TSR Inc. ',
     'TSVT':'2seventy bio Inc. ',
     'TT':'Trane Technologies plc',
     'TTC':'Toro Company ',
     'TTCF':'Tattooed Chef Inc  ',
     'TTD':'The Trade Desk Inc.  ',
     'TTE':'TotalEnergies SE',
     'TTEC':'TTEC Holdings Inc. ',
     'TTEK':'Tetra Tech Inc. ',
     'TTGT':'TechTarget Inc. ',
     'TTI':'Tetra Technologies Inc. ',
     'TTMI':'TTM Technologies Inc. ',
     'TTNP':'Titan Pharmaceuticals Inc. ',
     'TTOO':'T2 Biosystems Inc. ',
     'TTP':'Tortoise Pipeline & Energy Fund Inc. ',
     'TTSH':'Tile Shop Holdings Inc. ',
     'TTWO':'Take-Two Interactive Software Inc. ',
     'TU':'Telus Corporation ',
     'TUP':'Tupperware Brands Corporation ',
     'TURN':'180 Degree Capital Corp. ',
     'TUSK':'Mammoth Energy Services Inc. ',
     'TUYA':'Tuya Inc.  each representing one',
     'TV':'Grupo Televisa S.A. ',
     'TVC':'Tennessee Valley Authority ',
     'TVE':'Tennessee Valley Authority',
     'TVTX':'Travere Therapeutics Inc. ',
     'TW':'Tradeweb Markets Inc.  ',
     'TWCB':'Bilander Acquisition Corp.  ',
     'TWCBU':'Bilander Acquisition Corp. Unit',
     'TWCBW':'Bilander Acquisition Corp. ',
     'TWI':'Titan International Inc. (DE) ',
     'TWIN':'Twin Disc Incorporated ',
     'TWKS':'Thoughtworks Holding Inc. ',
     'TWLO':'Twilio Inc.  ',
     'TWLV':'Twelve Seas Investment Company II  ',
     'TWLVU':'Twelve Seas Investment Company II Unit',
     'TWLVW':'Twelve Seas Investment Company II ',
     'TWN':'Taiwan Fund Inc. ',
     'TWNK':'Hostess Brands Inc.  ',
     'TWO':'Two Harbors Investment Corp',
     'TWOU':'2U Inc. ',
     'TWST':'Twist Bioscience Corporation ',
     'TX':'Ternium S.A. Ternium S.A. ',
     'TXG':'10x Genomics Inc.  ',
     'TXMD':'TherapeuticsMD Inc. ',
     'TXN':'Texas Instruments Incorporated ',
     'TXO':'TXO Partners L.P.',
     'TXRH':'Texas Roadhouse Inc. ',
     'TXT':'Textron Inc. ',
     'TY':'Tri Continental Corporation ',
     'TY^':'Tri Continental Corporation Preferred Stock',
     'TYG':'Tortoise Energy Infrastructure Corporation ',
     'TYGO':'Tigo Energy Inc. ',
     'TYGOW':'Tigo Energy Inc. ',
     'TYL':'Tyler Technologies Inc. ',
     'TYRA':'Tyra Biosciences Inc. ',
     'TZOO':'Travelzoo ',
     'U':'Unity Software Inc. ',
     'UA':'Under Armour Inc. Class C ',
     'UAA':'Under Armour Inc.  ',
     'UAL':'United Airlines Holdings Inc. ',
     'UAMY':'United States Antimony Corporation ',
     'UAN':'CVR Partners LP Common Units representing Limited Partner Interests',
     'UAVS':'AgEagle Aerial Systems Inc. ',
     'UBA':'Urstadt Biddle Properties Inc. ',
     'UBCP':'United Bancorp Inc. ',
     'UBER':'Uber Technologies Inc. ',
     'UBFO':'United Security Bancshares ',
     'UBP':'Urstadt Biddle Properties Inc. ',
     'UBS':'UBS Group AG Registered ',
     'UBSI':'United Bankshares Inc. ',
     'UBX':'Unity Biotechnology Inc. ',
     'UCAR':'U Power Limited ',
     'UCBI':'United Community Banks Inc. ',
     'UCL':'uCloudlink Group Inc. ',
     'UCTT':'Ultra Clean Holdings Inc. ',
     'UDMY':'Udemy Inc. ',
     'UDR':'UDR Inc. ',
     'UE':'Urban Edge Properties  of Beneficial Interest',
     'UEC':'Uranium Energy Corp. ',
     'UEIC':'Universal Electronics Inc. ',
     'UFAB':'Unique Fabricating Inc. ',
     'UFCS':'United Fire Group Inc. ',
     'UFI':'Unifi Inc. New ',
     'UFPI':'UFP Industries Inc. ',
     'UFPT':'UFP Technologies Inc. ',
     'UG':'United-Guardian Inc. ',
     'UGI':'UGI Corporation ',
     'UGIC':'UGI Corporation Corporate Units',
     'UGP':'Ultrapar Participacoes S.A. (New)  (Each representing one Common Share)',
     'UGRO':'urban-gro Inc. ',
     'UHAL':'U-Haul Holding Company ',
     'UHG':'United Homes Group Inc  ',
     'UHGWW':'United Homes Group Inc. ',
     'UHS':'Universal Health Services Inc. ',
     'UHT':'Universal Health Realty Income Trust ',
     'UI':'Ubiquiti Inc. ',
     'UIHC':'United Insurance Holdings Corp. ',
     'UIS':'Unisys Corporation New ',
     'UK':'Ucommune International Ltd ',
     'UKOMW':'Ucommune International Ltd  expiring 11/17/2025',
     'UL':'Unilever PLC ',
     'ULBI':'Ultralife Corporation ',
     'ULCC':'Frontier Group Holdings Inc. ',
     'ULH':'Universal Logistics Holdings Inc. ',
     'ULTA':'Ulta Beauty Inc. ',
     'UMBF':'UMB Financial Corporation ',
     'UMC':'United Microelectronics Corporation (NEW) ',
     'UMH':'UMH Properties Inc. ',
     'UNB':'Union Bankshares Inc. ',
     'UNCY':'Unicycive Therapeutics Inc. ',
     'UNF':'Unifirst Corporation ',
     'UNFI':'United Natural Foods Inc. ',
     'UNH':'UnitedHealth Group Incorporated ',
     'UNIT':'Uniti Group Inc. ',
     'UNM':'Unum Group ',
     'UNMA':'Unum Group 6.250% Junior Subordinated Notes due 2058',
     'UNP':'Union Pacific Corporation ',
     'UNTY':'Unity Bancorp Inc. ',
     'UNVR':'Univar Solutions Inc. ',
     'UONE':'Urban One Inc.  ',
     'UONEK':'Urban One Inc. Class D ',
     'UP':'Wheels Up Experience Inc.  ',
     'UPBD':'Upbound Group Inc. ',
     'UPC':'Universe Pharmaceuticals Inc. ',
     'UPH':'UpHealth Inc. ',
     'UPLD':'Upland Software Inc. ',
     'UPS':'United Parcel Service Inc. ',
     'UPST':'Upstart Holdings Inc. ',
     'UPTD':'TradeUP Acquisition Corp. ',
     'UPTDU':'TradeUP Acquisition Corp. Unit',
     'UPTDW':'TradeUP Acquisition Corp. ',
     'UPWK':'Upwork Inc. ',
     'UPXI':'Upexi Inc. ',
     'URBN':'Urban Outfitters Inc. ',
     'URG':'Ur Energy Inc  (Canada)',
     'URGN':'UroGen Pharma Ltd. ',
     'URI':'United Rentals Inc. ',
     'UROY':'Uranium Royalty Corp. ',
     'USA':'Liberty All-Star Equity Fund ',
     'USAC':'USA Compression Partners LP Common Units Representing Limited Partner Interests',
     'USAP':'Universal Stainless & Alloy Products Inc. ',
     'USAS':'Americas Gold and Silver Corporation  no par value',
     'USAU':'U.S. Gold Corp. ',
     'USB':'U.S. Bancorp ',
     'USCB':'USCB Financial Holdings Inc.  ',
     'USCT':'TKB Critical Technologies 1 ',
     'USCTW':'TKB Critical Technologies 1 ',
     'USDP':'USD Partners LP Common Units representing limited partner interest',
     'USEA':'United Maritime Corporation ',
     'USEG':'U.S. Energy Corp.  (DE)',
     'USFD':'US Foods Holding Corp. ',
     'USGO':'U.S. GoldMining Inc. ',
     'USGOW':'U.S. GoldMining Inc. ',
     'USIO':'Usio Inc. ',
     'USLM':'United States Lime & Minerals Inc. ',
     'USM':'United States Cellular Corporation ',
     'USNA':'USANA Health Sciences Inc. ',
     'USPH':'U.S. Physical Therapy Inc. ',
     'UTAA':'UTA Acquisition Corporation ',
     'UTAAU':'UTA Acquisition Corporation Units',
     'UTAAW':'UTA Acquisition Corporation s',
     'UTF':'Cohen & Steers Infrastructure Fund Inc ',
     'UTG':'Reaves Utility Income Fund  of Beneficial Interest',
     'UTHR':'United Therapeutics Corporation ',
     'UTI':'Universal Technical Institute Inc ',
     'UTL':'UNITIL Corporation ',
     'UTMD':'Utah Medical Products Inc. ',
     'UTME':'UTime Limited ',
     'UTRS':'Minerva Surgical Inc. ',
     'UTSI':'UTStarcom Holdings Corp. ',
     'UTZ':'Utz Brands Inc  ',
     'UUU':'Universal Security Instruments Inc. ',
     'UUUU':'Energy Fuels Inc  (Canada)',
     'UVE':'UNIVERSAL INSURANCE HOLDINGS INC ',
     'UVSP':'Univest Financial Corporation ',
     'UVV':'Universal Corporation ',
     'UWMC':'UWM Holdings Corporation  ',
     'UXIN':'Uxin Limited ADS',
     'V':'Visa Inc.',
     'VABK':'Virginia National Bankshares Corporation ',
     'VAC':'Marriott Vacations Worldwide Corporation ',
     'VACC':'Vaccitech plc ',
     'VAL':'Valaris Limited ',
     'VALE':'VALE S.A.   Each Representing one common share',
     'VALN':'Valneva SE ',
     'VALU':'Value Line Inc. ',
     'VANI':'Vivani Medical Inc. ',
     'VAPO':'Vapotherm Inc. ',
     'VAQC':'Vector Acquisition Corporation II ',
     'VATE':'INNOVATE Corp. ',
     'VAXX':'Vaxxinity Inc.  ',
     'VBF':'Invesco Bond Fund ',
     'VBFC':'Village Bank and Trust Financial Corp. ',
     'VBIV':'VBI Vaccines Inc. New  (Canada)',
     'VBLT':'Vascular Biogenics Ltd. ',
     'VBNK':'VersaBank ',
     'VBOC':'Viscogliosi Brothers Acquisition Corp ',
     'VBOCU':'Viscogliosi Brothers Acquisition Corp Unit',
     'VBOCW':'Viscogliosi Brothers Acquisition Corp ',
     'VBTX':'Veritex Holdings Inc. ',
     'VC':'Visteon Corporation ',
     'VCEL':'Vericel Corporation ',
     'VCIF':'Vertical Capital Income Fund  of Beneficial Interest',
     'VCIG':'VCI Global Limited ',
     'VCNX':'Vaccinex Inc. ',
     'VCSA':'Vacasa Inc.  ',
     'VCTR':'Victory Capital Holdings Inc.  ',
     'VCV':'Invesco California Value Municipal Income Trust ',
     'VCXA':'10X Capital Venture Acquisition Corp. II',
     'VCYT':'Veracyte Inc. ',
     'VECO':'Veeco Instruments Inc. ',
     'VECT':'VectivBio Holding AG ',
     'VEDU':'Visionary Education Technology Holdings Group Inc. ',
     'VEEE':'Twin Vee PowerCats Co. ',
     'VEEV':'Veeva Systems Inc.  ',
     'VEL':'Velocity Financial Inc. ',
     'VEON':'VEON Ltd. ADS',
     'VERA':'Vera Therapeutics Inc.  ',
     'VERB':'Verb Technology Company Inc. ',
     'VERBW':'Verb Technology Company Inc. ',
     'VERI':'Veritone Inc. ',
     'VERO':'Venus Concept Inc. ',
     'VERU':'Veru Inc. ',
     'VERV':'Verve Therapeutics Inc. ',
     'VERX':'Vertex Inc.  ',
     'VERY':'Vericity Inc. ',
     'VET':'Vermilion Energy Inc. Common (Canada)',
     'VEV':'Vicinity Motor Corp. ',
     'VFC':'V.F. Corporation ',
     'VFF':'Village Farms International Inc. ',
     'VFL':'Delaware Investments National Municipal Income Fund ',
     'VGAS':'Verde Clean Fuels Inc.  ',
     'VGASW':'Verde Clean Fuels Inc. ',
     'VGI':'Virtus Global Multi-Sector Income Fund  of Beneficial Interest',
     'VGM':'Invesco Trust for Investment Grade Municipals  (DE)',
     'VGR':'Vector Group Ltd. ',
     'VGZ':'Vista Gold Corp ',
     'VHAQ':'Viveon Health Acquisition Corp. ',
     'VHC':'VirnetX Holding Corp ',
     'VHI':'Valhi Inc. ',
     'VHNA':'Vahanna Tech Edge Acquisition I Corp. ',
     'VHNAU':'Vahanna Tech Edge Acquisition I Corp. Units',
     'VIA':'Via Renewables Inc.  ',
     'VIAO':'VIA optronics AG  each representing one-fifth of an ',
     'VIAV':'Viavi Solutions Inc. ',
     'VICI':'VICI Properties Inc. ',
     'VICR':'Vicor Corporation ',
     'VIEW':'View Inc.  ',
     'VIEWW':'View Inc. ',
     'VIGL':'Vigil Neuroscience Inc. ',
     'VII':'7GC & Co. Holdings Inc.  ',
     'VIIAU':'7GC & Co. Holdings Inc. Unit',
     'VINC':'Vincerx Pharma Inc. ',
     'VINE':'Fresh Vine Wine Inc. ',
     'VINO':'Gaucho Group Holdings Inc. ',
     'VINP':'Vinci Partners Investments Ltd.  ',
     'VIOT':'Viomi Technology Co. Ltd ',
     'VIPS':'Vipshop Holdings Limited  each representing two ',
     'VIR':'Vir Biotechnology Inc. ',
     'VIRC':'Virco Manufacturing Corporation ',
     'VIRI':'Virios Therapeutics Inc. ',
     'VIRT':'Virtu Financial Inc.  ',
     'VIRX':'Viracta Therapeutics Inc. ',
     'VISL':'Vislink Technologies Inc. ',
     'VIST':'Vista Energy S.A.B. de C.V.',
     'VITL':'Vital Farms Inc. ',
     'VIV':'Telefonica Brasil S.A.  (Each representing One Common Share)',
     'VIVK':'Vivakor Inc. ',
     'VJET':'voxeljet AG ',
     'VKI':'Invesco Advantage Municipal Income Trust II  of Beneficial Interest (DE)',
     'VKQ':'Invesco Municipal Trust ',
     'VKTX':'Viking Therapeutics Inc. ',
     'VLCN':'Volcon Inc. ',
     'VLD':'Velo3D Inc. ',
     'VLGEA':'Village Super Market Inc.  ',
     'VLN':'Valens Semiconductor Ltd. ',
     'VLO':'Valero Energy Corporation ',
     'VLRS':'Controladora Vuela Compania de Aviacion S.A.B. de C.V.  each representing ten (10) Ordinary Participation Certificates',
     'VLT':'Invesco High Income Trust II',
     'VLY':'Valley National Bancorp ',
     'VMAR':'Vision Marine Technologies Inc. ',
     'VMC':'Vulcan Materials Company (Holding Company) ',
     'VMCA':'Valuence Merger Corp. I ',
     'VMCAW':'Valuence Merger Corp. I ',
     'VMD':'Viemed Healthcare Inc. ',
     'VMEO':'Vimeo Inc. ',
     'VMI':'Valmont Industries Inc. ',
     'VMO':'Invesco Municipal Opportunity Trust ',
     'VMW':'Vmware Inc.  ',
     'VNCE':'Vince Holding Corp. ',
     'VNDA':'Vanda Pharmaceuticals Inc. ',
     'VNET':'VNET Group Inc. ',
     'VNO':'Vornado Realty Trust ',    
     'VNOM':'Viper Energy Partners LP Common Unit',
     'VNRX':'VolitionRX Limited ',
     'VNT':'Vontier Corporation ',
     'VOC':'VOC Energy Trust Units of Beneficial Interest',
     'VOD':'Vodafone Group Plc ',
     'VOR':'Vor Biopharma Inc. ',
     'VOXR':'Vox Royalty Corp. ',
     'VOXX':'VOXX International Corporation  ',
     'VOYA':'Voya Financial Inc. ',
     'VPG':'Vishay Precision Group Inc. ',
     'VPV':'Invesco Pennsylvania Value Municipal Income Trust  (DE)',
     'VQS':'VIQ Solutions Inc. ',
     'VRA':'Vera Bradley Inc. ',
     'VRAR':'The Glimpse Group Inc. ',
     'VRAX':'Virax Biolabs Group Limited ',
     'VRAY':'ViewRay Inc. ',
     'VRCA':'Verrica Pharmaceuticals Inc. ',
     'VRDN':'Viridian Therapeutics Inc. ',
     'VRE':'Veris Residential Inc. ',
     'VREX':'Varex Imaging Corporation ',
     'VRM':'Vroom Inc. ',
     'VRME':'VerifyMe Inc. ',
     'VRMEW':'VerifyMe Inc. ',
     'VRNA':'Verona Pharma plc ',
     'VRNS':'Varonis Systems Inc. ',
     'VRNT':'Verint Systems Inc. ',
     'VRPX':'Virpax Pharmaceuticals Inc. ',
     'VRRM':'Verra Mobility Corporation  ',
     'VRSK':'Verisk Analytics Inc. ',
     'VRSN':'VeriSign Inc. ',
     'VRT':'Vertiv Holdings LLC  ',
     'VRTS':'Virtus Investment Partners Inc. ',
     'VRTV':'Veritiv Corporation ',
     'VRTX':'Vertex Pharmaceuticals Incorporated ',
     'VS':'Versus Systems Inc. ',
     'VSAC':'Vision Sensing Acquisition Corp.  ',
     'VSACW':'Vision Sensing Acquisition Corp. s',
     'VSAT':'ViaSat Inc. ',
     'VSCO':'Victorias Secret & Co. ',
     'VSEC':'VSE Corporation ',
     'VSH':'Vishay Intertechnology Inc. ',
     'VSSYW':'Versus Systems Inc.  s',
     'VST':'Vistra Corp. ',
     'VSTA':'Vasta Platform Limited ',
     'VSTM':'Verastem Inc. ',
     'VSTO':'Vista Outdoor Inc. ',
     'VTEX':'VTEX  ',
     'VTGN':'VistaGen Therapeutics Inc. ',
     'VTLE':'Vital Energy Inc.  par value $0.01 per share',
     'VTMX':'Corporacion Inmobiliaria Vesta S.A.B de C.V.  each representing ten (10) ',
     'VTN':'Invesco Trust for Investment Grade New York Municipals ',
     'VTNR':'Vertex Energy Inc ',
     'VTOL':'Bristow Group Inc. ',
     'VTR':'Ventas Inc. ',
     'VTRS':'Viatris Inc. ',
     'VTRU':'Vitru Limited ',
     'VTS':'Vitesse Energy Inc. ',
     'VTSI':'VirTra Inc. ',
     'VTVT':'vTv Therapeutics Inc.  ',
     'VTYX':'Ventyx Biosciences Inc. ',
     'VUZI':'Vuzix Corporation ',
     'VVI':'Viad Corp ',
     'VVOS':'Vivos Therapeutics Inc. ',
     'VVPR':'VivoPower International PLC ',
     'VVR':'Invesco Senior Income Trust  (DE)',
     'VVV':'Valvoline Inc. ',
     'VVX':'V2X Inc. ',
     'VWE':'Vintage Wine Estates Inc. ',
     'VWEWW':'Vintage Wine Estates Inc. s',
     'VXRT':'Vaxart Inc ',
     'VYGR':'Voyager Therapeutics Inc. ',
     'VYNE':'VYNE Therapeutics Inc. ',
     'VZ':'Verizon Communications Inc. ',
     'VZIO':'VIZIO Holding Corp.  ',
     'VZLA':'Vizsla Silver Corp. ',
     'W':'Wayfair Inc.  ',
     'WAB':'Westinghouse Air Brake Technologies Corporation ',
     'WABC':'Westamerica Bancorporation ',
     'WAFD':'Washington Federal Inc. ',
     'WAFDP':'Washington Federal Inc. Depositary Shares',
     'WAFU':'Wah Fu Education Group Limited ',
     'WAL':'Western Alliance Bancorporation  (DE)',
     'WALD':'Waldencast plc',
     'WALDW':'Waldencast plc ',
     'WASH':'Washington Trust Bancorp Inc. ',
     'WAT':'Waters Corporation ',
     'WATT':'Energous Corporation ',
     'WAVC':'Waverley Capital Acquisition Corp. 1 ',
     'WAVD':'WaveDancer Inc. ',
     'WAVE':'Eco Wave Power Global AB (publ) ',
     'WAVS':'Western Acquisition Ventures Corp. ',
     'WAVSU':'Western Acquisition Ventures Corp. Unit',
     'WAVSW':'Western Acquisition Ventures Corp. ',
     'WB':'Weibo Corporation ',
     'WBA':'Walgreens Boots Alliance Inc. ',
     'WBD':'Warner Bros. Discovery Inc. Series A ',
     'WBS':'Webster Financial Corporation ',
     'WBX':'Wallbox N.V. ',
     'WCC':'WESCO International Inc. ',
     'WCN':'Waste Connections Inc. ',
     'WD':'Walker & Dunlop Inc ',
     'WDAY':'Workday Inc.  ',
     'WDC':'Western Digital Corporation ',
     'WDFC':'WD-40 Company ',
     'WDH':'Waterdrop Inc.  (each representing the right to receive 10 )',
     'WDI':'Western Asset Diversified Income Fund  of Beneficial Interest',
     'WDS':'Woodside Energy Group Limited  each representing one ',
     'WE':'WeWork Inc.  ',
     'WEA':'Western Asset Bond Fund Share of Beneficial Interest',
     'WEAV':'Weave Communications Inc. ',
     'WEC':'WEC Energy Group Inc. ',
     'WEL':'Integrated Wellness Acquisition Corp ',
     'WELL':'Welltower Inc. ',
     'WEN':'Wendys Company ',
     'WERN':'Werner Enterprises Inc. ',
     'WES':'Western Midstream Partners LP Common Units Representing Limited Partner Interests',
     'WEST':'Westrock Coffee Company ',
     'WESTW':'Westrock Coffee Company s',
     'WETG':'WeTrade Group Inc. ',
     'WEX':'WEX Inc. ',
     'WEYS':'Weyco Group Inc. ',
     'WF':'Woori Financial Group Inc.  (each representing three (3) shares of )',
     'WFC':'Wells Fargo & Company ',
     'WFCF':'Where Food Comes From Inc. ',
     'WFG':'West Fraser Timber Co. Ltd ',
     'WFRD':'Weatherford International plc ',
     'WGO':'Winnebago Industries Inc. ',
     'WGS':'GeneDx Holdings Corp.  ',
     'WGSWW':'GeneDx Holdings Corp. ',
     'WH':'Wyndham Hotels & Resorts Inc. ',
     'WHD':'Cactus Inc.  ',
     'WHF':'WhiteHorse Finance Inc. ',
     'WHG':'Westwood Holdings Group Inc ',
     'WHLM':'Wilhelmina International Inc. ',
     'WHLR':'Wheeler Real Estate Investment Trust Inc. ',
     'WHR':'Whirlpool Corporation ',
     'WIA':'Western Asset Inflation-Linked Income Fund',
     'WILC':'G. Willi-Food International  Ltd. ',
     'WIMI':'WiMi Hologram Cloud Inc. ',
     'WINA':'Winmark Corporation ',
     'WING':'Wingstop Inc. ',
     'WINT':'Windtree Therapeutics Inc. ',
     'WINV':'WinVest Acquisition Corp. ',
     'WIRE':'Encore Wire Corporation ',
     'WISA':'WiSA Technologies Inc. ',
     'WISH':'ContextLogic Inc.  ',
     'WIT':'Wipro Limited ',
     'WIW':'Western Asset Inflation-Linked Opportunities & Income Fund',
     'WIX':'Wix.com Ltd. ',
     'WK':'Workiva Inc.  ',
     'WKC':'World Kinect Corporation ',
     'WKEY':'WISeKey International Holding Ltd ',
     'WKHS':'Workhorse Group Inc. ',
     'WKME':'WalkMe Ltd. ',
     'WKSP':'Worksport Ltd. ',
     'WKSPW':'Worksport Ltd. ',
     'WLDN':'Willdan Group Inc. ',
     'WLDS':'Wearable Devices Ltd. ',
     'WLDSW':'Wearable Devices Ltd. ',
     'WLFC':'Willis Lease Finance Corporation ',
     'WLGS':'Wang & Lee Group Inc. ',
     'WLK':'Westlake Corporation ',
     'WLKP':'Westlake Chemical Partners LP Common Units representing limited partner interests',
     'WLMS':'Williams Industrial Services Group Inc. ',
     'WLY':'John Wiley & Sons Inc. ',
     'WLYB':'John Wiley & Sons Inc. ',
     'WM':'Waste Management Inc. ',
     'WMB':'Williams Companies Inc. ',
     'WMC':'Western Asset Mortgage Capital Corporation ',
     'WMG':'Warner Music Group Corp.  ',
     'WMK':'Weis Markets Inc. ',
     'WMPN':'William Penn Bancorporation ',
     'WMS':'Advanced Drainage Systems Inc. ',
     'WMT':'Walmart Inc. ',
     'WNC':'Wabash National Corporation ',
     'WNEB':'Western New England Bancorp Inc. ',
     'WNNR':'Andretti Acquisition Corp. ',
     'WNS':'WNS (Holdings) Limited Sponsored ADR (Jersey)',
     'WNW':'Meiwu Technology Company Limited ',
     'WOLF':'Wolfspeed Inc. ',
     'WOOF':'Petco Health and Wellness Company Inc.  ',
     'WOR':'Worthington Industries Inc. ',
     'WORX':'SCWorx Corp. ',
     'WOW':'WideOpenWest Inc. ',
     'WPC':'W. P. Carey Inc. REIT',
     'WPM':'Wheaton Precious Metals Corp  (Canada)',
     'WPP':'WPP plc ',
     'WPRT':'Westport Fuel Systems Inc ',
     'WRAC':'Williams Rowland Acquisition Corp. ',
     'WRAP':'Wrap Technologies Inc. ',
     'WRB':'W.R. Berkley Corporation ',
     'WRBY':'Warby Parker Inc.  ',
     'WRK':'Westrock Company ',
     'WRLD':'World Acceptance Corporation ',
     'WRN':'Western Copper and Gold Corporation ',
     'WSBC':'WesBanco Inc. ',
     'WSBCP':'WesBanco Inc. Depositary Shares Each Representing a 1/40th Interest in a Share of 6.75% Fixed-Rate Reset Non-Cumulative Perpetual Preferred Stock Series A',
     'WSBF':'Waterstone Financial Inc.  (MD)',
     'WSC':'WillScot Mobile Mini Holdings Corp.  ',
     'WSFS':'WSFS Financial Corporation ',
     'WSM':'Williams-Sonoma Inc.  (DE)',
     'WSO':'Watsco Inc. ',
     'WSO/B':'Watsco Inc.',
     'WSR':'Whitestone REIT ',
     'WST':'West Pharmaceutical Services Inc. ',
     'WT':'WisdomTree Inc. ',
     'WTBA':'West Bancorporation ',
     'WTER':'The Alkaline Water Company Inc. ',
     'WTFC':'Wintrust Financial Corporation ',
     'WTI':'W&T Offshore Inc. ',
     'WTM':'White Mountains Insurance Group Ltd. ',
     'WTMAR':'Welsbach Technology Metals Acquisition Corp. one right to receive 1/10th of a share of ',
     'WTRG':'Essential Utilities Inc. ',
     'WTS':'Watts Water Technologies Inc.  ',
     'WTT':'Wireless Telecom Group  Inc. ',
     'WTTR':'Select Water Solutions Inc.  ',
     'WTW':'Willis Towers Watson Public Limited Company ',
     'WU':'Western Union Company ',
     'WULF':'TeraWulf Inc. ',
     'WVE':'Wave Life Sciences Ltd. ',
     'WVVI':'Willamette Valley Vineyards Inc. ',
     'WW':'WW International Inc. ',
     'WWAC':'Worldwide Webb Acquisition Corp.',
     'WWACU':'Worldwide Webb Acquisition Corp. Unit',
     'WWACW':'Worldwide Webb Acquisition Corp. ',
     'WWD':'Woodward Inc. ',
     'WWE':'World Wrestling Entertainment Inc.  ',
     'WWR':'Westwater Resources Inc. ',
     'WWW':'Wolverine World Wide Inc. ',
     'WY':'Weyerhaeuser Company ',
     'WYNN':'Wynn Resorts Limited ',
     'WYY':'WidePoint Corporation ',
     'X':'United States Steel Corporation ',
     'XAIR':'Beyond Air Inc. ',
     'XBIO':'Xenetic Biosciences Inc. ',
     'XBIOW':'Xenetic Biosciences Inc. s',
     'XBIT':'XBiotech Inc. ',
     'XCUR':'Exicure Inc. ',
     'XEL':'Xcel Energy Inc. ',
     'XELA':'Exela Technologies Inc. ',
     'XELB':'Xcel Brands Inc. ',
     'XENE':'Xenon Pharmaceuticals Inc. ',
     'XERS':'Xeris Biopharma Holdings Inc. ',
     'XFIN':'ExcelFin Acquisition Corp  ',
     'XFINU':'ExcelFin Acquisition Corp Unit',
     'XFINW':'ExcelFin Acquisition Corp ',
     'XFLT':'XAI Octagon Floating Rate & Alternative Income Term Trust  of Beneficial Interest',
     'XFOR':'X4 Pharmaceuticals Inc. ',
     'XGN':'Exagen Inc. ',
     'XHR':'Xenia Hotels & Resorts Inc. ',
     'XIN':'Xinyuan Real Estate Co Ltd ',
     'XLO':'Xilio Therapeutics Inc. ',
     'XMTR':'Xometry Inc.  ',
     'XNCR':'Xencor Inc. ',
     'XNET':'Xunlei Limited ',
     'XOM':'Exxon Mobil Corporation ',
     'XOMA':'XOMA Corporation ',
     'XOS':'Xos Inc. ',
     'XOSWW':'Xos Inc. s',
     'XP':'XP Inc.  ',
     'XPAX':'XPAC Acquisition Corp. ',
     'XPAXW':'XPAC Acquisition Corp. ',
     'XPDB':'Power & Digital Infrastructure Acquisition II Corp.  ',
     'XPDBW':'Power & Digital Infrastructure Acquisition II Corp. ',
     'XPEL':'XPEL Inc. ',
     'XPER':'Xperi Inc. ',
     'XPEV':'XPeng Inc.  each representing two ',
     'XPL':'Solitario Zinc Corp. ',
     'XPO':'XPO Inc. ',
     'XPOF':'Xponential Fitness Inc.  ',
     'XPON':'Expion360 Inc. ',
     'XPRO':'Expro Group Holdings N.V. ',
     'XRAY':'DENTSPLY SIRONA Inc. ',
     'XRTX':'XORTX Therapeutics Inc. ',
     'XRX':'Xerox Holdings Corporation ',
     'XTLB':'XTL Biopharmaceuticals Ltd. ',
     'XTNT':'Xtant Medical Holdings Inc. ',
     'XWEL':'XWELL Inc. ',
     'XXII':'22nd Century Group Inc. ',
     'XYF':'X Financial  each representing six ',
     'XYL':'Xylem Inc.  New',
     'YALA':'Yalla Group Limited  each representing one',
     'YCBD':'cbdMD Inc. ',
     'YELL':'Yellow Corporation ',
     'YELP':'Yelp Inc. ',
     'YETI':'YETI Holdings Inc. ',
     'YEXT':'Yext Inc. ',
     'YGF':'YanGuFang International Group Co. Ltd. ',
     'YGMZ':'MingZhu Logistics Holdings Limited ',
     'YI':'111 Inc. ',
     'YJ':'Yunji Inc. American Depository Shares',
     'YMAB':'Y-mAbs Therapeutics Inc. ',
     'YMM':'Full Truck Alliance Co. Ltd.  (each representing 20 )',
     'YORW':'York Water Company ',
     'YOSH':'Yoshiharu Global Co.  ',
     'YOTA':'Yotta Acquisition Corporation ',
     'YOTAW':'Yotta Acquisition Corporation ',
     'YOU':'Clear Secure Inc.  ',
     'YPF':'YPF Sociedad Anonima ',
     'YQ':'17 Education & Technology Group Inc. ',
     'YRD':'Yiren Digital Ltd.  each representing two ',
     'YS':'YS Biopharma Co. Ltd. ',
     'YSBPW':'YS Biopharma Co. Ltd. s',
     'YSG':'Yatsen Holding Limited  each representing four ',
     'YTEN':'Yield10 Bioscience Inc. ',
     'YTRA':'Yatra Online Inc. ',
     'YUM':'Yum! Brands Inc.',
     'YUMC':'Yum China Holdings Inc. ',
     'YVR':'Liquid Media Group Ltd. ',
     'YY':'JOYY Inc. ',
     'Z':'Zillow Group Inc. Class C Capital Stock',
     'ZAPP':'Zapp Electric Vehicles Group Limited ',
     'ZAPPW':'Zapp Electric Vehicles Group Limited ',
     'ZBH':'Zimmer Biomet Holdings Inc. ',
     'ZBRA':'Zebra Technologies Corporation  ',
     'ZCMD':'Zhongchao Inc. ',
     'ZD':'Ziff Davis Inc. ',
     'ZDGE':'Zedge Inc. Class B ',
     'ZENV':'Zenvia Inc.  ',
     'ZEPP':'Zepp Health Corporation ',
     'ZETA':'Zeta Global Holdings Corp.  ',
     'ZEUS':'Olympic Steel Inc. ',
     'ZEV':'Lightning eMotors Inc ',
     'ZFOX':'ZeroFox Holdings Inc. ',
     'ZFOXW':'ZeroFox Holdings Inc. s',
     'ZG':'Zillow Group Inc.  ',
     'ZGN':'Ermenegildo Zegna N.V. ',
     'ZH':'Zhihu Inc.  (every two of each representing one)',
     'ZI':'ZoomInfo Technologies Inc ',
     'ZIM':'ZIM Integrated Shipping Services Ltd. ',
     'ZIMV':'ZimVie Inc. ',
     'ZING':'FTAC Zeus Acquisition Corp.  ',
     'ZINGU':'FTAC Zeus Acquisition Corp. Unit',
     'ZINGW':'FTAC Zeus Acquisition Corp. ',
     'ZION':'Zions Bancorporation N.A. ',
     'ZIP':'ZipRecruiter Inc.  ',
     'ZIVO':'Zivo Bioscience Inc. ',
     'ZIVOW':'Zivo Bioscience Inc. s',
     'ZJYL':'JIN MEDICAL INTERNATIONAL LTD. ',
     'ZKIN':'ZK International Group Co. Ltd ',
     'ZLAB':'Zai Lab Limited ',
     'ZM':'Zoom Video Communications Inc.  ',
     'ZNTL':'Zentalis Pharmaceuticals Inc. ',
     'ZOM':'Zomedica Corp. ',
     'ZS':'Zscaler Inc. ',
     'ZTEK':'Zentek Ltd. ',
     'ZTO':'ZTO Express (Cayman) Inc.  each representing one.',
     'ZTR':'Virtus Total Return Fund Inc.',
     'ZTS':'Zoetis Inc.  ',
     'ZUMZ':'Zumiez Inc. ',
     'ZUO':'Zuora Inc.  ',
     'ZURA':'Zura Bio Limited ',
     'ZURAW':'Zura Bio Limited s',
     'ZVIA':'Zevia PBC  ',
     'ZVRA':'Zevra Therapeutics Inc. ',
     'ZVSA':'ZyVersa Therapeutics Inc. ',
     'ZWS':'Zurn Elkay Water Solutions Corporation ',
     'ZYME':'Zymeworks Inc. ',
     'ZYNE':'Zynerba Pharmaceuticals Inc. ',
     'ZYXI':'Zynex Inc. '
}

#........................................................................


#web design---------------------


# -----------------USER AUTHENTICATOR--------------

# names =["Livinus Emmanuel","Chinedu Okonkwo"]
# usernames =["lEmmanuel","cokonkwo"]

# file_path = Path(__file__).parent / "hashed_pw.pkl"

# with file_path.open("rb") as file:
#     hashed_passwords = pickle.load(file)
  

# authenticator = stauth.Authenticate (names, usernames, hashed_passwords,"Charts","abcdef",cookie_expiry_days= 30)  # abcdef=random key to save the cookies on the browser

# name, authentication_status, username = authenticator.login("Login", "sidebar")


# if authentication_status == False:
#        st.error("Username/Password is incorrect")

# if authentication_status == None:
#        st.warning("Please enter your Username and Password")

# if  authentication_status:   
#      authenticator.logout("Logout","sidebar")
#      st.sidebar.title(f"Welcome{name}")  



# def load_lottieurl(url):
#      r = requests.get(url)
#      if r.status_code != 200:
#           return None
#      return r.json()     

    
# lottie_coding = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_49rdyysj.json")
# img_contact_from = Image.open("/Users/okonkwolivinus/streamlit/Thumbnail.png")
# visa_contact_from = Image.open("/Users/okonkwolivinus/streamlit/Thumbnail CanvasVisa.png")
    

#           st.write("----")
#           st.header("Youtube Videos")
#           st.write("##")
#           image_column, text_column = st.columns((1, 2))
#           with image_column:
#            st.image(img_contact_from)
#           with text_column:
#            st.subheader("Paycom Software Aktienanalyse") 
#            st.write(
#                """
#                Paycom software Aktienanalyse | Diese Aktie hat S&P 500 und ihre Konkurrenten deutlich geschlagen

#                """
#           )
#           st.markdown("[Watch Video...](https://youtu.be/N2b-Jhf7-wY)")

# with st.container():
#           image_column, text_column = st.columns((1, 2))
#           with image_column:
#            st.image(visa_contact_from)
#           with text_column:
#            st.subheader("Visa Aktienanalyse") 
#            st.write(
#                """
#                VISA Aktienanalyse - Ist die Aktie krisensicher? Und historisch gerade unterbewertet?

#                """
#           )
#           st.markdown("[Watch Video...](https://youtu.be/DCpfVYP2HjY)")


# Get the ticker input from the user
#....................................................
# def main():
    
   

#      if 'username' not in st.session_state:
#            st.session_state.username =''

#      if 'useremail' not in st.session_state:
#            st.session_state.useremail =''   

#      def f():

#           try:
#                 user =auth.get_user_by_email(email)
#                 #st.sidebar.write(user.uid)

#                 st.write('Login successful')

#                 st.session_state.username=user.uid
#                 st.session_state.useremail=user.email

#                 st.session_state.signedout=True
#                 st.session_state.signout=True


#           except:

#                st.warning('Login Failed')

               

#      def t():
#            st.session_state.signout=False
#            st.session_state.signedout=False
#            st.session_state.username ='' 



#      if 'signedout' not in st.session_state:
#           st.session_state.signedout =False 

#      if 'signout' not in st.session_state:
#           st.session_state.signout =False 

#      if not st.session_state['signedout']:  
#           choice = st.selectbox('Login/Sign up',['Login','Sign Up'])  


#           if choice =="Login":

#                #st.sidebar.subheader("Login Section")  

#                email=st.text_input("Email Address")
#                password=st.text_input("Password",type='password')

#                #username=st.sidebar.text_input("User Name")

#                st.button('Login',on_click=f)

#           else:

#                email=st.text_input("Email Address")

#                password=st.text_input("Password",type='password')

#                username=st.text_input("Enter User Name")
               



#                if st.button('Create my account'):

#                     user=auth.create_user(email=email,password=password,uid=username)

#                     st.success('Account created successfully!')    
#                     st.markdown('Please Login using your email and password')
#                     st.balloons()


#      if st.session_state.signedout:
#            #st.sidebar.text('Name' +st.session_state.username)
#            #st.sidebar.text('Emailid:' +st.session_state.useremail)
#            st.button('Sign out',on_click=t)

   
# #if __name__ == '__main__':
#  #     main()

#..............................................................

st.markdown("""
    <style>
    .stSelectbox > div:first-child {
        width: 100px;  /* Set the width you want for the selectbox */
    }
    </style>
""", unsafe_allow_html=True)

ticker_symbol_name = {f'{name} : {symbol}': symbol for symbol, name in ticker_symbol_name.items()}     
selected_ticker = st.selectbox('Select a ticker', list(ticker_symbol_name.keys()), key='symbol')    



#ticker = ticker_symbol_name.get(selected_ticker) 
#name, symbol = selected_ticker.split(' : ')


if selected_ticker:
    ticker = ticker_symbol_name.get(selected_ticker) 
    name, symbol = selected_ticker.split(' : ')
    #st.write(f'Selected Ticker Name: {name}')



custom_css = """
          <style>
               .my-header {
                    font-family: serif;
                    font-size: 24px;
                    letter-spacing: 2px;
                    text-align: center;
                    width: 100%;  /* Nutzt die Seitenbreite */
               }
          </style>
          """






#............................... quickfs api .................


#api_key = "5f478e5d5c33dea7e1a950e500e94a4bbfbd4368"
#api_key = "1d26eb898e859a7f519e974f6fa969bb073ba09f"
api_key = "7bd83d28344a3e5d2c2103dd4ca746f133259764"
header = {'x-qfs-api-key': api_key}

url = f'https://public-api.quickfs.net/v1/data/all-data/{ticker}?api_key={api_key}'
usage_url = f'https://public-api.quickfs.net/v1/usage'
#marketwatch ="https://www.marketwatch.com/investing/stock/{ticker}/financials/balance-sheet"
#headers = "/html/body/div[3]/div[6]/div/div[3]/div/div/table/tbody/tr[12]/td[6]/div/span"
          
response = requests.get(url, headers=header)
usage_response = requests.get(usage_url, headers=header)

if response.status_code == 200:
   data = response.json()
   usage = usage_response.json()
    # Continue processing the data as required
else:
    st.write()

#data = response.json()
#usage = response.json()
#st.write(data)
#st.write(usage)
#response.json()
#--------------------------------------------------------------
#annual_data = data['data']['financials']['annual']
Financial_data = data['data']['financials']
annual_data = Financial_data['annual']
quarterly_data = Financial_data['quarterly']
eps_diluted_ttm = Financial_data['ttm']['eps_diluted']
fcf_per_share = Financial_data['ttm']['fcf_per_share']
Dividend_ttm = Financial_data['ttm']['cff_dividend_paid'] 
Dividend_current_dividend= Financial_data['ttm']['dividends'] 
fcf_ttm = Financial_data['ttm']['fcf']/1000000000           
netincome_ttm = Financial_data['ttm']['net_income']/1000000000
revenue_ttm = Financial_data['ttm']['revenue']/1000000000
shares_diluted_ttm = (Financial_data['ttm']['shares_diluted'])/1000000000
shares_basic_ttm = (Financial_data['ttm']['shares_basic'])/1000000000
shares_eop_ttm=(Financial_data['ttm']['shares_eop'])/1000000000
shares_eop_change_ttm=(Financial_data['ttm']['shares_eop_change'])/1000000000
shares_eop_annual=annual_data['shares_eop'][-1:]
shares_eop_quarter=quarterly_data['shares_eop'][-1:]
period_end_price_ttm = (Financial_data['ttm']['period_end_price'])
Revenue_ttm = (Financial_data['ttm']['revenue'])
Debt_equity_last_quater = annual_data['debt_to_equity'][-1:]
Debt_equity_ttm =(Financial_data['ttm']['debt_to_equity'])
date_quarter = quarterly_data['period_end_date'][-10:] 
date_annual = annual_data['period_end_date'][-10:] 
Stock_description=data["data"]["metadata"]["description"]
#gross_margin_ttm=Financial_data['ttm']['gross_margin']
stock_sector=data["data"]["metadata"]["sector"]
Industry=data["data"]["metadata"]["industry"]
cik=data["data"]["metadata"]["CIK"]
FCF_Cagr_10 = annual_data['fcf_cagr_10'][-1:]
EPS_Cagr_10 = annual_data['eps_diluted_cagr_10'][-1:]
Revenue_Cagr_10 = annual_data['revenue_cagr_10'][-1:]
date_list_quarter = [period_end_date for period_end_date in date_quarter]
date_list_annual = [period_end_date for period_end_date in date_annual]
#---------------------------pyfinanz-----------------------------------
          
quote = Quote(ticker)
#--------------------------10K-----------------------------------
#st.title('Chart:',{name})
#st.title(name)
# st.markdown(
#     '<div style="text-align:center;"><b>{}</b></div>'.format(name),
#     unsafe_allow_html=True
# )

# st.text("")  # This adds a line break
# st.markdown(f"Sector: {stock_sector}")
# #st.sidebar.text(f"Sector: {stock_sector}")
# st.text("")  # This adds a line break
# st.markdown(f"Industry: {Industry}")
link = f"https://www.sec.gov/edgar/browse/?CIK={cik}&owner=exclude"

styled_link = f'<div style="display: flex; justify-content: center;"><a href="{link}" style="color: green; font-family: serif;" target="_blank">Annual/Quarterly Reports &rarr;</a></div>'




col1, col2,col3 = st.columns(3)

# Display name centered in the first column
st.markdown(
    '<div style="text-align:center;"><b>{}</b></div>'.format(name),
    unsafe_allow_html=True
)

# Add a line break
st.text("")

# Display sector and industry information in the second column
with col1:
     st.markdown(f"Sector: {stock_sector}", unsafe_allow_html=True)
with col2:
     st.markdown(f"Industry: {Industry}", unsafe_allow_html=True)
with col3:
     st.markdown(styled_link, unsafe_allow_html=True)

#.............................................................................................

if ticker == 'ADS:DE':
    ticker = 'ADS.DE'

if ticker == 'BRK.A':
     ticker ='BRK-A'

if ticker == 'BRK.B':
     ticker ='BRK-B'

else:
    # Handle other cases if needed
    ticker = ticker

stock_info = yf.Ticker(ticker)





def get_current_price():

     try:
          current_price = stock_info.history(period="1d", interval="1m")["Close"].iloc[-1]
          #current_price = stock_info.history(period="1d")["Close"].iloc[-1]

     except Exception as e: #except all errors
     
          current_price = quote.fundamental_df.at[0, "Price"]
          #current_price = 23
     else:   
           current_price = 23  

     return current_price 

current_price = get_current_price()    

def format_date(date):
    return date.strftime('%Y/%m/%d')

def get_all_time_high_and_low_price(ticker):
    data = stock_info.history(period="max", actions=False)  # Exclude dividend data

    # Find all-time high points
    all_time_highs = data[data['Close'] == data['Close'].max()]
    fifty_two_week_low = data['Close'].iloc[-260:].min()

    if not all_time_highs.empty:
        # Get the date and price of the first all-time high point
        first_all_time_high = all_time_highs.iloc[0]
        all_time_high_date = first_all_time_high.name
        all_time_high_price = first_all_time_high['Close']

        return all_time_high_date, all_time_high_price, fifty_two_week_low
    else:
        return None, None, None
try:
     all_time_high_date, all_time_high_price, fifty_two_week_low = get_all_time_high_and_low_price(ticker)
except Exception as e:
      st.write(" ")
try:      
     if all_time_high_date and all_time_high_price:
          formatted_date = format_date(all_time_high_date)
         # print(f"All-Time High for {ticker}:")
          #print(f"Date: {formatted_date}")
          #print(f"Price: {all_time_high_price:.2f}$")
    # else:
          #print(f"No all-time high data found for {ticker}")

     if fifty_two_week_low:
          st.write("")
          #print(f"Price: {fifty_two_week_low:.2f}$")
     else:
          st.write(" ")

     # Fetch historical data and exclude dividend data
     historical_data = stock_info.history(period='1y', actions=False)

     min_price = historical_data['Close'].min()
     min_price_date = historical_data[historical_data['Close'] == min_price].index[0]

except Exception as e:
      st.write(" ")

#print(f"52-Week Low for {ticker}:")
#print(f"Datedgfdhggjhkgj: {min_price_date.strftime('%Y-%m-%d')}")
#print(f"Price: ${min_price:.2f}")


#..............
#start_date = datetime.now() - timedelta(days=1095)
start_date = datetime.now() - timedelta(days=39 * 365)
#end_date = st.sidebar.date_input('End Date')
end_date=datetime.now() 

data = yf.download(ticker,start=start_date, end=end_date)
#data = yf.Ticker(ticker)
try:
     close_price = round(data['Close'][-2],2)#-2 meaning a day before
     #st.write(close_price)
     current_price = stock_info.history(period="1d",interval="1m")["Close"].iloc[-1] 

     percentage_difference = round(((current_price - close_price) / close_price) * 100,2)
     amount = current_price 
     converted_amount = "{:.2f}".format(amount * usd_to_eur_rate)
except Exception as e:
      st.write(" ")
# Determine text color based on percentage_difference
#text_color = "green" if percentage_difference >= 0 else "red"

# Display the percentage difference with the specified text color
#st.write(f"Percentage Difference: <span style='color:{text_color};'>{percentage_difference:.2f}%</span>", unsafe_allow_html=True)

# try:
#      base_currency = 'USD'
#      target_currency ='EUR'
#      amount = current_price 
#      convert = requests.get(f"https://api.frankfurter.app/latest?amount={amount}&from={base_currency}&to={target_currency}")
#      data10 = convert.json()
#      # Extract the converted amount from the response
#      converted_amount = data10['rates'][target_currency]
#      #st.write(f"{current_price} USD is approximately {converted_amount:.2f} EUR")

# except Exception as e:
#      st.warning("Error occurred. Using alternative conversion method.")
        
#      c = CurrencyRates()
     #converted_amount = amount * usd_to_eur_rate
     #print(f"{current_price} USD is approximately {converted_amount:.2f} EUR")

#..........................................................................................................   
#formatted_value = f"{current_price:.2f} "

green_style = "color: green;"


formatted_value = f"{current_price:.2f} $"
formatted_price_with_color = f"<span style='{green_style}'>{formatted_value}</span>"

formatted_value2 = f"{converted_amount} €"
formatted_price_with_color2 = f"<span style='{green_style}'>{formatted_value2}</span>"

     # Display the metric with the formatted price and green font color using st.markdown
    #st.markdown("Current Price: " + formatted_price_with_color, unsafe_allow_html=True)


     
    # Calculate the text color based on the percentage difference
#arrow_text = "🟩 " if percentage_difference >= 0 else "🔻"
try:
     arrow_text = " 🔼 " if percentage_difference > 0 else " 🔻 "
     text_color = "green" if percentage_difference > 0 else "red"


     text_color = "green" if percentage_difference >= 0 else "red"
     #formatted_value2 = f" {converted_amount} €"
          #formatted_price_euro = "&euro; {:.2f}".format(formatted_value2)  # Format with Euro sign

     st.markdown(
    f"<div style='text-align: center; width: 100%;'>Current Price: {formatted_price_with_color}          Aktueller Preis: {formatted_price_with_color2} "
     f"{arrow_text}<span style='color:{text_color};'>{percentage_difference:.2f}%</span></div>",
     unsafe_allow_html=True
) 
except Exception as e:
     st.markdown(
    f"<div style='text-align: center; width: 100%;'>Current Price: {formatted_price_with_color}          Aktueller Preis: {formatted_price_with_color2} "
     f"{arrow_text}<span style='color:{text_color};'>{percentage_difference:.2f}%</span></div>",
     #unsafe_allow_html=True
    unsafe_allow_html=True
)
    
#...............................................................................................................

# col2, col3, col4, col5, col6, col7= st.columns(6)

# with col2:
#     button2 = col2.button("1W")
# with col3:
#     button3 = col3.button("1M")
# with col4:
#     button4 = col4.button("YTD")
# with col5:
#     button5 = col5.button("1Y")
# with col6:
#     button6 = col6.button("5Y")
# with col7:
#     button7 = col7.button("MAX")


# if button2:
#     start_date = datetime.now() - timedelta(days=5)
    
# elif button3:
#     start_date = datetime.now() - timedelta(days=31)
# elif button4:
#     start_date = datetime(datetime.now().year, 1, 1)
# elif button5:
#     start_date = datetime.now() - timedelta(days=365)
# elif button6:
  
#     start_date = datetime.now() - timedelta(days=5 * 365)
# elif button7:
        
#     start_date = datetime(1984, 1, 1)
# #---------------..........................................
# #---------------...........................................



#start_date = datetime(1986, 1, 1)

#start_date_input = st.sidebar.date_input('Start Date', start_date)
start_date_input=start_date

if start_date_input is None:
    # Set the default start date to "2002-03-04"
    start_date_input = start_date


data = yf.download(ticker,start=start_date_input, end=end_date)



data['Adj Close'] = data['Adj Close'].round(2)


fig = px.line(data, x=data.index, y='Adj Close', labels={'x ': 'Date', 'Adj Close': 'Price ($)'})

fig.update_layout(
    #title=f'{ticker} Price',
    xaxis_title='Date',
    yaxis_title='Price ',
)

st.plotly_chart(fig,use_container_width=True,config={'displayModeBar': False})


#st.plotly_chart(fig, config={'displayModeBar': False})



data2 = data
data2['% change'] = data['Adj Close'] / data['Adj Close'].shift(1)-1
data2.dropna(inplace = True)
#--------------------------------------

# Format the percentages in thousands
#data2['% change'] = data2['% change'] * 1000




#-------------------------------------------------------------------------------------------------------------------
# st.subheader("Candlestick Chart")
# candlestick_chart = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
# candlestick_chart.update_layout(title=f"{symbol} Candlestick Chart", xaxis_rangeslider_visible=False)
# st.plotly_chart(candlestick_chart, use_container_width=True)
#............................................................................


price_movement = data['Adj Close']
initial_price = price_movement.iloc[0]
final_price = price_movement.iloc[-1]
percentage_return = ((final_price - initial_price) / initial_price) * 100

#annual_return = data2['% change'].mean()*252*100
formatted_percentage_return = "{:,.2f}%".format(percentage_return)

aufrundung = round(percentage_return, 2)

color = "#2E8B57" if aufrundung >= 0 else "red"
# try:

#      if button2:
#           st.write(f'5 Days Return: <span style="color:{color}">{formatted_percentage_return}</span>', unsafe_allow_html=True)

#      elif button3:
#           st.write(f'1 Month Return: <span style="color:{color}">{formatted_percentage_return}</span>', unsafe_allow_html=True)

#      elif button4:
#           st.write(f'YTD Return: <span style="color:{color}">{formatted_percentage_return}</span>', unsafe_allow_html=True)

#      elif button5:
#           st.write(f'1 YR Return: <span style="color:{color}">{formatted_percentage_return}</span>', unsafe_allow_html=True)

#      elif button6:
#           st.write(f'5 YR Return: <span style="color:{color}">{formatted_percentage_return}</span>', unsafe_allow_html=True)  

#      elif button7:
#           st.write(f'MAX Return: <span style="color:{color}">{formatted_percentage_return}</span>', unsafe_allow_html=True) 

# except NameError as ne:
#           st.write("")


          

#..............................................................
  #st.write(data2)
#...................................................................
# Create a session state variable to track authentication
# if 'authenticated' not in st.session_state:
#     st.session_state.authenticated = False

# correct_password = "123"
# correct_Username = "chinedu"

# # Prompt the user for a password
# #username = st.sidebar.text_input("Enter the username:")

# #password = st.sidebar.text_input("Enter the password:", type="password")

# # Define the ticker variable
# #ticker = ""
# ticker ='MSFT'

# if not st.session_state.authenticated:
#     # Only show the username and password input fields if not authenticated
#     password = st.sidebar.text_input("Enter the password:", type="password")
#     username = st.sidebar.text_input("Enter the username:")
# else:
#     # Hide the input fields if authenticated
#     password = username = " "

# # Define the ticker symbols and names outside of the password check
# ticker_symbol_name = {f'{name} : {symbol}': symbol for symbol, name in ticker_symbol_name.items()}

# if password == correct_password and username == correct_Username:
#     st.session_state.authenticated = True
#     st.sidebar.write("Authentication successful.")
#     selected_ticker = st.sidebar.selectbox('Select a ticker', list(ticker_symbol_name.keys()), key='symbol')

#     ticker = ticker_symbol_name.get(selected_ticker) 

#     name, symbol = selected_ticker.split(' : ')
#     st.write("{name}") 

#     start_date = datetime.now() - timedelta(days=1095)  # 3 years (approximately 1095 days)

#     start_date_input = st.sidebar.date_input('Start Date', start_date)

#     if start_date_input is None:
#         # Set the default start date to "3 years ago"
#         start_date_input = start_date

#     end_date = st.sidebar.date_input('End Date')

#     data = yf.download(ticker, start=start_date_input, end=end_date)
#     fig = px.line(data, x=data.index, y=round(data['Adj Close'], 2))
#     st.plotly_chart(fig) 

#     data2 = data
#     data2['% change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
#     data2.dropna(inplace=True)
    
#     # Calculate annual return
#     annual_return = data2['% change'].mean() * 252 * 100
#     aufrundung = round(annual_return, 2)
    
#     #st.write(f"Annual Return: {aufrundung}%")
# else:
#     st.sidebar.error("Authentication failed. Please enter the correct username and password.")



#..............................................Stock beta......................................................

# Define the stock symbol and the market index symbol (e.g., S&P 500)
market_index_symbol = '^GSPC'

 # Define the time period for historical data (start_date and end_date)
start_date = datetime.now() - timedelta(days=1826)#5years 
end_date = datetime.now()     

try:
     # Retrieve historical stock and market index data using yfinance
     stock_data = yf.download(ticker, start=start_date, end=end_date)
     market_data = yf.download(market_index_symbol, start=start_date, end=end_date)

     # Calculate daily returns for stock and market
     stock_returns = stock_data['Adj Close'].pct_change().dropna()
     market_returns = market_data['Adj Close'].pct_change().dropna()

     # Calculate covariance and variance of returns
     covariance = np.cov(stock_returns, market_returns)[0][1]
     market_variance = np.var(market_returns)

     # Calculate beta
     beta ="{:,.2f}".format((covariance / market_variance))
     #st.write("beta",beta)

except Exception as e:
    # Handle ValueError (e.g., division by zero) or KeyError (data not found) by setting beta to 1
     beta = "{:,.2f}".format(1.0)
     #print(f"Beta of {ticker} could not be calculated. Using default value: {beta:.2f}")




#......................................Disclaimer.......................................


 #------------------------currency conversin-----------------------------------------------
# try:
#      base_currency = 'USD'
#      target_currency ='EUR'
#      amount = current_price 
#      convert = requests.get(f"https://api.frankfurter.app/latest?amount={amount}&from={base_currency}&to={target_currency}")
#      data10 = convert.json()
#      # Extract the converted amount from the response
#      converted_amount = data10['rates'][target_currency]
#      #st.write(f"{current_price} USD is approximately {converted_amount:.2f} EUR")

# except Exception as e:
#      st.warning("Error occurred. Using alternative conversion method.")
        
#      c = CurrencyRates()
#      converted_amount = c.convert("USD", "EUR", current_price)
#      print(f"{current_price} USD is approximately {converted_amount:.2f} EUR")



# #print(f"{amount} USD is approximately {amount_euro:.2f} EUR")

#      # Display the result
#      #print(f"{amount} {base_currency} is equal to {converted_amount} {target_currency}")
# # .   ....................................................................................   
# formatted_value = f"{current_price:.2f} "
# formatted_value2 = f" {converted_amount:.2f} "
# #after_hours_price_ = f" {after_hours_price:.2f} "

# # Calculate the percentage difference
# #percentage_difference = ((after_hours_price - current_price) / current_price) * 100

# # Determine the arrow color and direction
# #arrow_color = 'green' if percentage_difference >= 0 else 'red'
# #arrow_direction = '▲' if percentage_difference >= 0 else '▼'

# #st.write('Price:',formatted_value,'oder', formatted_value2)

# # Display the values with arrows
# #st.write(f'<span style="color:#2E8B57">&dollar; {formatted_value}</span>',unsafe_allow_html=True)

# #st.write(f'<span style="color: #2E8B57">&euro; {formatted_value2}</span>', unsafe_allow_html=True)
# #st.write("Current Price:",f'<span style="color:#2E8B57">&dollar; {formatted_value}  </span> <span style="color:#2E8B57">&euro; {formatted_value2}</span>', unsafe_allow_html=True)

# col2,col3, col4 = st.columns(3)
# with col2:
#     #price_usd = "${:.2f}".format(formatted_value)
#     #price_euro = "&euro; {:.2f}".format(formatted_value2)
#     st.metric("Current Price:", formatted_value, "USD")
#     st.metric("", formatted_value2, "EUR")

# with col3:
#     st.metric("ATH High", f"${all_time_high_price:.2f}")
# with col4:
#     st.metric("52-Week Low", f"${fifty_two_week_low:.2f}")
# Define the correct username and password
# Define the correct username and password

# Define the correct username and password
# Define the correct username and password

#Initialize authentication status

# def make_hashes(password):
# 	return hashlib.sha256(str.encode(password)).hexdigest()

# def check_hashes(password,hashed_text):
# 	if make_hashes(password) == hashed_text:
# 		return hashed_text
# 	return False
# # DB Management

# conn = sqlite3.connect('data.db')
# c = conn.cursor()
# # DB  Functions

# def create_usertable():
# 	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


# def add_userdata(username,password):
# 	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
# 	conn.commit()

# def login_user(username,password):
# 	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
# 	data = c.fetchall()
# 	return data


# def view_all_users():
# 	c.execute('SELECT * FROM userstable')
# 	data = c.fetchall()
# 	return data




#Metric, Financials,Pillar_Analysis,Stock_Analyser,Multiple_Valuation,EPS_Valuation,Dividend_Discount_Model,Key_ratios,Charts,Retirement_Calculator,news = st.tabs(["Key Statistics", "Financials","12 Pillar Process","Discounted Cash Flow Analysis","Multiple of Earnings Valuation","EPS Valuation","Dividend Discount Model","Key Ratios","Charts","Calculator","Top 10 News"])

Metric, Financials,Pillar_Analysis,Stock_Analyser,Multiple_Valuation,Dividend_Discount_Model,Charts,Key_ratios,Retirement_Calculator,news = st.tabs(["Key Statistics", "Financials","12 Pillar Process","Discounted Cash Flow Analysis","Multiple of Earnings Valuation","Dividend Discount Model","Charts","Key Ratios","Calculator","Top 10 News"])

     #st.header('Price / Total return')


    
     #st.write(data['info'])
     #color = st.markdown('<svg height="100" width="100"><circle cx="50" cy="50" r="15" fill="red" /></svg>', unsafe_allow_html=True)
  # Round to 2 decimal places
#st.write(annual_return)


 #------------------------------------------------------------
 #..........................................................

with st.container():
     with Metric:  
 

          stock_info = yf.Ticker(ticker)



          try:
               # Get market capitalization
               Marketcap = stock_info.info['marketCap']
               Marketcap_in_million=Marketcap
               Marketcap =Marketcap /1000000000
               #Marketcap_in_Billion = "{:.2f}B".format(Marketcap)            
               Marketcap_in_Billion = "{:.2f}T".format(Marketcap / 1000) if abs(Marketcap) >= 1000 else "{:,.1f}B".format(Marketcap / 1)
 
               #print("10-year Treasury yield:", treasury_yield)

          except Exception as e:
               st.write("     ")
               #print(f"yfinance: HTTP Error: {e}")
               #print("     ")

          #except (KeyError, TypeError):
           #    st.write("     ")
               #print("Yfinace: Error: No data found for Marketcap.")
               #print("     ")

          try:
              
               fundamental_df = quote.fundamental_df
               market_cap_original = quote.fundamental_df.at[0, "Market Cap"] 
               #print("market_cap",market_cap_original)

               try:
                    Marketcap = float(market_cap_original.replace('B', ''))  
                    #Marketcap = float(market_cap.replace('B', '').replace('M', '')) 
                    # Remove 'B' and convert to float

                    #Marketcap =Marketcap /1000000000
                    Marketcap_in_Billion = "{:.2f}T".format(Marketcap / 1000) if abs(Marketcap) >= 1000 else "{:,.2f}B".format(Marketcap / 1)
                    
               except Exception as e:
                     Marketcap_in_Billion=market_cap_original   
                    
          except Exception as e:
               # Handle the specific exceptions here
               Forward_PE="NA"   
               RSI="N/A"
               #print("     ")
               #print(f"Pyfinance: An error occurred: {e}")
               #print("     ")

          if 'market_cap' not in locals():  
                            #print("Error: No data found Marketcap.")
               Marketcap = current_price * shares_eop_ttm

               Marketcap_in_Billion = "{:.2f}T".format(Marketcap / 1000) if abs(Marketcap) >= 1000 else "{:,.2f}B".format(Marketcap / 1)

               #Marketcap_in_Billion = "{:.2f}B".format(current_price * shares_eop_ttm) 
               
               

          EPS_last = annual_data['eps_basic'][-1:]
          EPS_last_average  = ((sum(EPS_last) / len(EPS_last))) 
          EPS_last_average_one=EPS_last_average

          EPS_growth_3years = annual_data['eps_diluted_growth'][-3:]
          EPS_growth_3years = sum(EPS_growth_3years)/len(EPS_growth_3years)
          EPS_growth_3years =EPS_growth_3years*100

          EPS_growth_five = annual_data['eps_diluted_growth'][-5:]
          EPS_growth_5yrs = sum(EPS_growth_five)/len(EPS_growth_five)
          EPS_growth_5yrs =EPS_growth_5yrs*100

          EPS_growth = annual_data['eps_diluted_growth'][-10:]
          EPS_growth_10yrs = sum(EPS_growth)/len(EPS_growth)
          EPS_growth_10yrs =EPS_growth_10yrs*100


          #Neticome_five = annual_data['revenue'][-5:]
          #average_Revenue_five =round(((sum(Revenue_five) / len(Revenue_five)))/1000000000, 2)

          

          FCF_annual_one =annual_data['fcf'][-1:]
          average_fcf_Annual_one = (sum(FCF_annual_one) / len(FCF_annual_one)) / 1000000000
          rounded = "{:.2f}B".format(average_fcf_Annual_one)
          
          FCF_annual_five =annual_data['fcf'][-5:]
          average_FCF_annual_five = float((sum(FCF_annual_five) / len(FCF_annual_five)))

          FCF_annual_ten =annual_data['fcf'][-10:]
          average_FCF_annual_ten = float((sum(FCF_annual_ten) / len(FCF_annual_ten)))
          #average_FCF_annual_five_we = float((sum(FCF_annual_five) / len(FCF_annual_five)))

          #average_FCF_annual_five_rounded = "{:.2f}B".format(average_FCF_annual_five)

        

          ROIC_annual_one = "{:.2f}%".format(annual_data['roic'][-1]*100)

          ROIC_annual_funf =annual_data['roic'][-5:]
          #ROIC_annual_funf =annual_data['roic'][-5:]
          Average_ROIC_funf = "{:.2f}%".format((sum(ROIC_annual_funf) / len(ROIC_annual_funf))*100)

     
          ROIC_annual_3years = annual_data['roic'][-3:]
          ROIC_annual_3years=sum(ROIC_annual_3years)/len(ROIC_annual_3years)
          ROIC_annual_3years = "{:.2f}%".format(ROIC_annual_3years*100)
          

          net_income_annual_funf = annual_data['net_income'][-5:] 
          Average_netIncome_annual = (sum(net_income_annual_funf) / len(net_income_annual_funf)) / 1000000000
          Average_netIncome_annual_we = (sum(net_income_annual_funf) / len(net_income_annual_funf))

          #fcf_ttm =fcf_ttm*1000000000
          Average_netIncome_annual_we ="{:.2f}B".format(Average_netIncome_annual_we/ 1000000000) if abs(Average_netIncome_annual_we) >= 1000000000 else "{:,.1f}M".format(Average_netIncome_annual_we / 1000000)
          #Avg_netincome = "{:.2f}B".format(Average_netIncome_annual)

          net_income_annual_one = annual_data['net_income'][-1:]
          Average_net_income_annual_one = "{:.2f}B".format((sum(net_income_annual_one) / len(net_income_annual_one)) / 1000000000) 
          
          round_net_income_annual_one =(sum(net_income_annual_one) / len(net_income_annual_one)) / 1000000000

         # Revenue_last = annual_data['revenue'][-1:]
          #average_Revenue_last_ohne_billion = (sum(Revenue_last) / len(Revenue_last))/1000000000
          #average_Revenue_last = "{:.2f}B".format(round(((sum(Revenue_last) / len(Revenue_last)))/1000000000, 2))

          revenue_annual_ttm = annual_data['revenue'][-1:] 
          average_revenue_annual_ttm = ((sum(revenue_annual_ttm) / len(revenue_annual_ttm)) / 1000000000)

          eps_basic_annual = annual_data['eps_basic'][-10:]
          Revenue_growth = annual_data['revenue_growth'][-10:]
          revenue_2013 = annual_data['revenue'][-10:] 


          Dividend_per_share = annual_data['dividends'][-10:]
          Dividend_per_share = Financial_data['ttm']['dividends']
         

           #...........................................CAGR..........................................................................
          FCF_Cagr_10 = sum(FCF_Cagr_10)/len(FCF_Cagr_10)
          FCF_Cagr_10 =round((FCF_Cagr_10*100),2)

     #........................................................................................................................
          EPS_Cagr_10 = sum(EPS_Cagr_10)/len(EPS_Cagr_10)
          EPS_Cagr_10 =round((EPS_Cagr_10*100),2)
     #...........................................................................
          Revenue_Cagr_10 = sum(Revenue_Cagr_10)/len(Revenue_Cagr_10)
          Revenue_Cagr_10= round((Revenue_Cagr_10*100),2)

     #....................................................
          Dividend_per_share_cagr_10 = annual_data['dividends_per_share_cagr_10'][-1:]  
          Dividend_per_share_cagr_10 = sum(Dividend_per_share_cagr_10)/len(Dividend_per_share_cagr_10)
          Dividend_per_share_cagr_10= round((Dividend_per_share_cagr_10*100),2)
     #................................................

     #-------------------------------------------------------------------------------------------- 
          Dividend_per_share_cagr_10_quarter = quarterly_data['dividends_per_share_cagr_10'][-1:]  
          Dividend_per_share_cagr_10_quarter = sum(Dividend_per_share_cagr_10_quarter)/len(Dividend_per_share_cagr_10_quarter)
          Dividend_per_share_cagr_10_quarter= round((Dividend_per_share_cagr_10_quarter*100),2)

          
          try:
               value_at_index_6 = FCF_annual_ten[-6]
               value_at_index_last  = FCF_annual_ten[-1]

          except Exception as e:
               value_at_index_6 = 0
               value_at_index_last = 0
          try:
               
               if value_at_index_6 == 0:
                    FCF_5_CAGR = 0

               else:
                         try:
                              FCF_5_CAGR = (pow((value_at_index_last / value_at_index_6), 0.2) - 1) * 100
                              #CAGR = round(CAGR, 2)

                              if isinstance(FCF_5_CAGR, complex):
                                        FCF_5_CAGR = 0  # Set CAGR to 0 if it's a complex number
                              else:
                                   FCF_5_CAGR = "{:.2f}".format(FCF_5_CAGR)

                         except Exception as e:
                              FCF_5_CAGR = 0

          except Exception as e:  

               FCF_5_CAGR =0;    
               
        
     #......................................................................................................................     
          
          try:
               value_at_index_6 = eps_basic_annual[-6]
               value_at_index_last = eps_basic_annual[-1]

          except Exception as e:
               value_at_index_6 = 0
               value_at_index_last = 0
          try:
               
               if value_at_index_6 == 0:
                    EPS_5_CAGR = 0

               else:
                         try:
                              EPS_5_CAGR = (pow((value_at_index_last / value_at_index_6), 0.2) - 1) * 100
                              #CAGR = round(CAGR, 2)

                              if isinstance(EPS_5_CAGR, complex):
                                        EPS_5_CAGR = 0  # Set CAGR to 0 if it's a complex number
                              else:
                                   EPS_5_CAGR = "{:.2f}".format(EPS_5_CAGR)

                         except Exception as e:
                              EPS_5_CAGR = 0

          except Exception as e:  

               EPS_5_CAGR =0;    
               
#------------------------------------------------------------------------------------------------------------------------------------------------------------
          

               
          try:
               value_at_index_6 = revenue_2013[-6]
               value_at_index_last = revenue_2013[-1]

          except Exception as e:
               value_at_index_6 = 0
               value_at_index_last = 0
          try:
               
               if value_at_index_6 == 0:
                    Revenue_5_CAGR = 0

               else:
                         try:
                              Revenue_5_CAGR = (pow((value_at_index_last / value_at_index_6), 0.2) - 1) * 100
                              #CAGR = round(CAGR, 2)

                              if isinstance(Revenue_5_CAGR, complex):
                                        Revenue_5_CAGR = 0  # Set CAGR to 0 if it's a complex number
                              else:
                                   Revenue_5_CAGR = "{:.2f}".format(Revenue_5_CAGR)

                         except Exception as e:
                              Revenue_5_CAGR = 0

          except Exception as e:  

               Revenue_5_CAGR =0;    
               
#------------------------------------------------------------------------------------------------------------------------------------------------------------
          
          #10years

          Revenue_growth_3years = annual_data['revenue_growth'][-3:]
          Revenue_growth_3years=sum(Revenue_growth_3years)/len(Revenue_growth_3years)
          Revenue_growth_3years = (Revenue_growth_3years*100)


          Revenue_growth_1year = annual_data['revenue_growth'][-1:]
          Revenue_growth_1year=sum(Revenue_growth_1year)/len(Revenue_growth_1year)
          Revenue_growth_1year = (Revenue_growth_1year*100)

         

          FCF_Margin = annual_data['fcf_margin'][-10:] #10years
          FCF_Margin_10 =sum(FCF_Margin)/len(FCF_Margin)
          #FCF_Margin_10 = (FCF_Margin_10*100)

          FCF_Margin_5 = annual_data['fcf_margin'][-5:] 
          FCF_Margin_5=sum(FCF_Margin_5)/len(FCF_Margin_5)
          #FCF_Margin_5 = (FCF_Margin_5*100)

          FCF_Margin_1 = annual_data['fcf_margin'][-1:]
          FCF_Margin_1=sum(FCF_Margin_1)/len(FCF_Margin_1)
          FCF_Margin_1 = (FCF_Margin_1*100)

          One_YR_ROCE = annual_data['roce'][-1:]  
          One_YR_ROCE=sum(One_YR_ROCE)/len(One_YR_ROCE)
          One_YR_ROCE = (One_YR_ROCE*100)

          five_yrs_ROCE = annual_data['roce'][-5:]
          five_yrs_ROCE=sum(five_yrs_ROCE)/len(five_yrs_ROCE)
          five_yrs_ROCE = (five_yrs_ROCE*100)
     

          #Revenue_growth_3years = annual_data['revenue_growth'][-3:]
          #Revenue_growth_3years=sum(Revenue_growth_3years)/len(Revenue_growth_3years)
          #Revenue_growth_3years = (Revenue_growth_3years*100)

          Revenue_growth_5years = annual_data['revenue_growth'][-5:]
          Revenue_growth_5years=sum(Revenue_growth_5years)/len(Revenue_growth_5years)
          Revenue_growth_5years = (Revenue_growth_5years*100)

          try:
               fcf_yield_ttm = "{:.2f}%".format((fcf_per_share/amount)*100)
          except Exception as e:
                fcf_yield_ttm = "NA"

          PE_historical = annual_data['price_to_earnings'][-10:] 

          # if len(PE_historical) == 10:
          
          #      average_PE_historical = "{:.2f}".format((sum(PE_historical) / len(PE_historical)))
          # else:
                
          #       average_PE_historical="-"

          ROA_annual_ttm = annual_data['roa'][-1:] 
          average_ROA_annual_ttm = "{:.2f}%".format((sum(ROA_annual_ttm) / len(ROA_annual_ttm))*100)

          Total_Equity_annual_one = annual_data['total_equity'][-1:]
          Average_total_equity_annual = (sum(Total_Equity_annual_one) / len(Total_Equity_annual_one)) / 1000000000
         
          Net_income_margin_10_ = annual_data['net_income_margin'][-10:]
          Net_income_margin_10 = sum(Net_income_margin_10_)/len(Net_income_margin_10_)

          Net_income_margin_5 = annual_data['net_income_margin'][-5:]
          Net_income_margin_5 = sum(Net_income_margin_5)/len(Net_income_margin_5)

          Net_income_margin_1 = annual_data['net_income_margin'][-1:]
          Net_income_margin_1 = sum(Net_income_margin_1)/len(Net_income_margin_1)
          
          if Revenue_ttm!=0 and average_revenue_annual_ttm !=0 :
               Price_to_sales_last = "{:.2f}".format(Marketcap/(Revenue_ttm/1000000000))
               #five_yrs_Nettomarge = "{:.2f}%".format((Net_income_margin_5)*100)
               Net_margin_ttm ="{:.2f}%".format((Net_income_margin_1)*100)
          else:
               Price_to_sales_last = "NA"
               #five_yrs_Nettomarge ="NA"
               Net_margin_ttm="NA"
          
          
          

         
          
          
          

          #pe_ttm = round(amount/eps_diluted_ttm,2) #amount = current_price eps_basic_ttm
          #pe_ttm = round(Marketcap/netincome_ttm,2)

          # Check if Marketcap and netincome_ttm data is available
          if not pd.isna(Marketcap) and not pd.isna(netincome_ttm) and netincome_ttm != 0 and fcf_ttm !=0:
         
               #pe_ttm = "{:.2f} ".format(Marketcap / netincome_ttm)
               try:
                    pe_ttm =quote.fundamental_df.at[0, "P/E"]

               except Exception as e:
                    pe_ttm = "{:.2f} ".format(Marketcap / netincome_ttm)
                    
               pfcf_ttm="{:.2f} ".format(Marketcap / fcf_ttm)  
               

          elif not pd.isna(amount) and not pd.isna(eps_diluted_ttm) and eps_diluted_ttm != 0:
          # Calculate P/E ratio using amount and eps_diluted_ttm
               pe_ttm = "{:.2f} ".format(amount / eps_diluted_ttm)

          # Check if pe_ttm is still None (no data or division by zero)
          if netincome_ttm is None:
          # Handle the case where there is no valid data
               pe_ttm = "{:.2f} ".format(amount / eps_diluted_ttm)
          
          if fcf_ttm is None or fcf_ttm < 0.0:
               pfcf_ttm="-"
               #pe_ttm = "-"  # You can use any value or message you prefer
          if netincome_ttm < 0:
               #pfcf_ttm="-"
               pe_ttm = "-"  # You can use any value or message you prefer     
          else:
               pfcf_ttm="-" 
                
          try:
               if fcf_ttm == 0.00:
                    pfcf_ttm= "-"
               else:
                    pfcf_ttm="{:.2f} ".format(Marketcap / fcf_ttm) 
             

          except Exception as a:
                
               pfcf_ttm="-"
                
          Historical_marketkap=annual_data['market_cap'][-5:]
          Historical_marketkap = round(sum(Historical_marketkap) / len(Historical_marketkap)/ 1000000000, 2)  

          Net_Operating_CashFlow_annual_5 = annual_data['cf_cfo'][-5:] 
          Net_Operating_CashFlow_annual = annual_data['cf_cfo'][-10:] 

          fcf_growth_five =annual_data['fcf_growth'][-5:]
          fcf_growth_ten =annual_data['fcf_growth'][-10:]

          pe_five =annual_data['price_to_earnings'][-5:]
          pe_ten =annual_data['price_to_earnings'][-10:]

          ROE_five = annual_data['roe'][-5:]

          if len(Net_Operating_CashFlow_annual) >= 10:
               P_OCF_10="{:.2f}".format(Marketcap/((sum(Net_Operating_CashFlow_annual)/len(Net_Operating_CashFlow_annual))/1000000000))
               Average_fcf_growth_ten =  "{:.2f}".format(((sum(fcf_growth_ten) / len(fcf_growth_ten)))*100)
               average_PE_historical = "{:.2f}".format((sum(PE_historical) / len(PE_historical)))
               pfcf_ten="{:.2f}".format(Marketcap/(average_FCF_annual_ten/1000000000))
               #Revenue_growth_10years=sum(Revenue_growth)/len(Revenue_growth)
               #Revenue_growth_10years = "{:.2f}%".format(Revenue_growth_10years*100)
               Net_income_margin_10 = "{:.2f}".format((Net_income_margin_10)*100)
               FCF_Margin_10 = "{:.2f}".format((FCF_Margin_10)*100)
               EPS_growth_10yrs="{:.2f}".format(EPS_growth_10yrs)
               Average_pe_ten = "{:.2f}".format(sum(pe_ten) / len(pe_ten))

          else:
               P_OCF_10= "-"
               Average_fcf_growth_ten = "0.00"
               #Revenue_growth_10years= "0.00"
               EPS_growth_10yrs="0.00"
               Average_pe_ten = "0.00"
               average_PE_historical = "-"
               pfcf_ten = "-"
               Net_income_margin_10 ="-"
               FCF_Margin_10 ="-"
               
            
           
        

          fcf_growth_3years =annual_data['fcf_growth'][-3:]
          Average_fcf_growth_3years =  "{:.2f}%".format(((sum(fcf_growth_3years) / len(fcf_growth_3years)))*100)

          pe_one =annual_data['price_to_earnings'][-1:]
          Average_pe_one =  "{:.2f}".format(((sum(pe_one) / len(pe_one))))


          try:
               average_end_price_five = annual_data['period_end_price'][-5:]
               average_end_price_five = sum(average_end_price_five) / len(average_end_price_five)

          except Exception as e: 
                
               average_end_price_five = 0.0

          Divdends_paid_5years =annual_data['dividends'][-5:]
          #st.write(Divdends_paid_5years)

          try:
               if len(Divdends_paid_5years) >= 5:
                    Divdend_per_share_yield_average =sum(Divdends_paid_5years) / len(Divdends_paid_5years)
                    Dividend_yield_average ="{:.2f}%".format(abs((Divdend_per_share_yield_average)/average_end_price_five)*100)

               else:
                    
                    Dividend_yield_average =0.00

                    
          except Exception as e: 
                
               Dividend_yield_average=0.0


               

        

          try:
               

               if len(FCF_annual_five) >= 5:
                    Average_ROIC_funf = "{:.2f}%".format(((sum(ROIC_annual_funf) / len(ROIC_annual_funf))*100))
                    average_FCF_annual_five_we ="{:.2f}B".format(average_FCF_annual_five/ 1000000000) if abs(average_FCF_annual_five) >= 1000000000 else "{:,.1f}M".format(average_FCF_annual_five / 1000000)
                    five_ROE="{:.2f}".format(((sum(ROE_five) / len(ROE_five))*100))
                    pe_five_ = "{:.2f}".format(float(Marketcap)/Average_netIncome_annual)
                    pfcf_funf="{:.2f}".format(Marketcap/(average_FCF_annual_five/1000000000))
                    #average_PE_historical = "{:.2f}".format((sum(PE_historical) / len(PE_historical)))
                    P_OCF_5= "{:.2f}".format(Marketcap/((sum(Net_Operating_CashFlow_annual_5)/len(Net_Operating_CashFlow_annual_5))/1000000000))
                    KCV =  pfcf_funf
                    #five_Yrs_ROE = round((Average_netIncome_annual/Average_total_equity_annual)*100,2)
                    five_Yrs_ROE="{:.2f}".format(((sum(ROE_five) / len(ROE_five))*100))
                    Average_fcf_growth_five =  "{:.2f}%".format(((sum(fcf_growth_five) / len(fcf_growth_five)))*100)
                    #five_yrs_Nettomarge =  "{:.2f}".format((Average_netIncome_annual/average_revenue_annual)*100)  
                    Average_pe_five =  "{:.2f}".format(((sum(pe_five) /len(pe_five)))) 
                    five_yrs_Nettomarge = "{:.2f}".format((Net_income_margin_5)*100)
                    FCF_Margin_5 = "{:.2f}".format((FCF_Margin_5)*100)
                    
              
               
                    

                    if Average_netIncome_annual==0.0 or Average_netIncome_annual==-0.0:
                             KGV = round(amount/eps_5years_average_diluted_annual, 2)
                    else:
                         KGV = round(Marketcap/Average_netIncome_annual, 2)
                
               
               else:
                    Average_ROIC_funf ="NA"
                    average_FCF_annual_five_we="{:.2f}".format(0.0)
                    #pe_five_ =0
                    rounded_operating_margin_five ="{:.2f}%".format(0.0)
                    five_yrs_Nettomarge ="0.00"
                    five_ROE="0.00"
                    pfcf_funf="-"
                    pe_five_="-"
                    average_PE_historical="-"
                    P_OCF_5 = "-"
                    KGV=0.0
                    KCV=0.0
                    five_Yrs_ROE=0.0
                    Average_fcf_growth_five = "0.00"
                    Average_pe_five = "0.00"
                    FCF_Margin_5 ="-"



                  
          

          except Exception as e:
               eps_diluted_annual=annual_data['eps_diluted'][-5:]
               eps_5years_average_diluted_annual=sum(eps_diluted_annual)/len(eps_diluted_annual)

              
               pe_five_ = round((amount)/(eps_5years_average_diluted_annual),2)
              

               if average_FCF_annual_five>5:
                    pfcf_funf="{:.2f}".format(Marketcap_in_million/(average_FCF_annual_five/1000000000))
               else: 
                     
                     pfcf_funf ="-"

               #st.write(Average_netIncome_annual)
               #Marketcap_in_million = round(Marketcap_in_million,2)
               #st.write(Marketcap_in_million)
               #st.write(eps_5years_average_diluted_annual)

          
          #Historical_marketkap ="{:.2f}".format(Historical_marketkap/ 1000000000) if abs(Historical_marketkap) >= 1000000000 else "{:,.1f}".format(Historical_marketkap / 1000000)

          #st.write(Historical_marketkap)
          
          #print(f"{amount} USD is approximately {amount_euro:.2f} EUR")
         
               #five_Yrs_ROE ="0.00"
              
          try:
               
               forwardPE=quote.fundamental_df.at[0, "Forward P/E"]
               RSI=quote.fundamental_df.at[0, "RSI (14)"]
               PEG=quote.fundamental_df.at[0, "PEG"]
               Beta=quote.fundamental_df.at[0, "Beta"]
               #Earnings = quote.fundamental_df.at[0, "Earnings"]
               Moving_200=quote.fundamental_df.at[0, "SMA200"]
               Moving_50=quote.fundamental_df.at[0, "SMA50"]
               Target_Price = quote.fundamental_df.at[0,"Target Price"] 
               #Target_Price='{:.2f}'.format(Target_Price)   
               Dividend_TTM = quote.fundamental_df.at[0,"Dividend TTM"]
               Dividend_Est = quote.fundamental_df.at[0,"Dividend Est."]
               Dividend_Ex_Date= quote.fundamental_df.at[0,"Dividend Ex-Date"]
               Earnings_this_yr=quote.fundamental_df.at[0,"EPS this Y"]
               Earnings_next_yr_in_prozent=quote.fundamental_df.at[0,"EPS next Y - EPS growth next year"]
               Earnings_next_yr_in_value=quote.fundamental_df.at[0,"EPS next Y - EPS estimate for next year"]
               Earnings_next_5_yrs=quote.fundamental_df.at[0,"EPS next 5Y"]
                   
          except Exception as e: 

               forwardPE ="-"
               Earnings ="-"
               RSI="-"
               PEG="-"
               Beta=beta
               Dividend_TTM = Dividend_per_share
               Moving_200="-"
               Moving_50="-"
               Target_Price ="-"
               Dividend_Est ="-"
               Dividend_Ex_Date = "-"
               Earnings_this_yr="-"
               Earnings_next_yr_in_prozent="-"
               Earnings_next_yr_in_value ="-"
               Earnings_next_5_yrs="-"
          


          
          #Dividend_yield ="{:.2f}%".format(abs((average_Dividend_paid_ttm/basic_shares_last_annual)/current_price)*100)
          Divdend_per_share =Financial_data['ttm']['dividends']
          Dividend_per_share_yield ="{:.2f}%".format(abs((Divdend_per_share)/current_price)*100)


          Divdend_per_share =Financial_data['ttm']['dividends']
          Dividend_per_share_yield ="{:.2f}%".format(abs((Divdend_per_share)/current_price)*100)

         

        

          #Net_margin ="{:.2f}%".format((round_net_income_annual_one/average_revenue_annual_ttm)*100)
     
          try:
               ROE_ttm_ohne = (round_net_income_annual_one/Average_total_equity_annual)*100
          #ROE_ttm_ohne = 100
               ROE_ttm="{:.2f}%".format(ROE_ttm_ohne)
          except Exception as e: 
               ROE_ttm = "-"
          

          cash_equiv_quarter =quarterly_data['cash_and_equiv'][-1:]
          cash_equiv_quarter = round((sum(cash_equiv_quarter) / len(cash_equiv_quarter)) / 1000000000, 3)
          #Short_term_debt_annual = annual_data['st_debt'][-1:]
          #Short_term_debt_annual = round((sum(Short_term_debt_annual) / len(Short_term_debt_annual)) / 1000000000, 2)
          #Short_term_debt_annual=float(Short_term_debt_annual[9])

          #LongTerm_debt_annual =annual_data['lt_debt'][-1:]
          #LongTerm_debt_annual = round((sum(LongTerm_debt_annual) / len(LongTerm_debt_annual)) / 1000000000, 2)
          #LongTerm_debt_annual =float(LongTerm_debt_annual[9])

          

          #Total_debt = round((Short_term_debt_annual + LongTerm_debt_annual),2)
          #Total_debt = round((sum(Total_debt) / len(Total_debt)) / 1000000000, 2)

               

                                        #------------------------------------------------------------------
          try:
               Accounts_payable_quarter = quarterly_data['accounts_payable'][-10:]
               Current_accrued_liab_quarter = quarterly_data['current_accrued_liabilities'][-10:]
               Tax_payable_quarter = quarterly_data['tax_payable'][-10:]
               Other_current_liabilities_quarter = quarterly_data['other_current_liabilities'][-10:]
               Current_deferred_revenue_quarter = quarterly_data['current_deferred_revenue'][-10:]
               Total_current_liabilities_quarter = quarterly_data['total_current_liabilities'][-10:] 

               Short_term_debt_quarter = quarterly_data['st_debt'][-10:]
               current_portion_of_lease_obligation = quarterly_data['current_capital_leases'][-10:]
               capital_leases = quarterly_data['noncurrent_capital_leases'][-10:]
               LongTerm_debt_quarter = quarterly_data['lt_debt'][-10:]
                                             #Total_debt_quarter = quarterly_data[''][-10:]
               Other_longterm_liabilities_quarter = quarterly_data['other_lt_liabilities'][-10:]
               Total_liabilities_quarter = quarterly_data['total_liabilities'][-10:]
                                             #Total_Sharehold_equity_quarter = quarterly_data[''][-10:]
               Total_Equity_quarter = quarterly_data['total_equity'][-10:]

               st_investments_annual =quarterly_data['st_investments'][-1:]
               st_investments_annual = round((sum(st_investments_annual) / len(st_investments_annual)) / 1000000000, 3)

               gross_margin =quarterly_data['gross_margin'][-1:]
               average_gross_margin = round((sum(gross_margin) / len(gross_margin))*100, 2)
               #gross_margin_ttm =gross_margin_ttm
               rounded_gross_margin = "{:.2f}%".format(average_gross_margin)

               five_yrs_average_gross_margin =annual_data['gross_margin'][-5:]
               five_yrs_average_gross_margin = round((sum(five_yrs_average_gross_margin) / len(five_yrs_average_gross_margin))*100, 2)
               #gross_margin_ttm =gross_margin_ttm
               five_yrs_average_gross_margin = "{:.2f}%".format(five_yrs_average_gross_margin)

               operating_margin =annual_data['operating_margin'][-1:]
               average_operating_margin = round((sum(operating_margin) / len(operating_margin))*100, 2)
               rounded_operating_margin = "{:.2f}%".format(average_operating_margin)

               operating_margin_five =annual_data['operating_margin'][-5:]
               average_operating_margin_five = round((sum(operating_margin_five) / len(operating_margin_five))*100, 2)
               rounded_operating_margin_five = "{:.2f}%".format(average_operating_margin_five)

               #Total_Equity_ttm =Financial_data['ttm']['total_equity']/1000000000
               #P_B_ttm =Marketcap/Total_Equity_ttm

               
          #cash_equiv_annual =float(cash_equiv_annual[9])

               Total_cash_last_years = round((st_investments_annual+cash_equiv_quarter),3)
                                             #Liabili_shareholders_Equity_quarter = quarterly_data[''][-10:]
                                             #Nopat_quarter= quarterly_data['nopat'][-10:]


               index = range(len(date_quarter))
               df = pd.DataFrame({
                    'period_end_date': date_quarter,
                    'accounts_payable': Accounts_payable_quarter,
                    'current_accrued_liabilities': Current_accrued_liab_quarter,
                    'tax_payable': Tax_payable_quarter,
                    'other_current_liabilities': Other_current_liabilities_quarter,
                    'current_deferred_revenue': Current_deferred_revenue_quarter,

                    'total_current_liabilities': Total_current_liabilities_quarter,
                    'noncurrent_capital_leases': capital_leases,
                    'lt_debt': LongTerm_debt_quarter}, index=index)
                                             
               df['Total Difference'] = df['total_current_liabilities'] - \
                                        (df['accounts_payable'] + df['current_accrued_liabilities'] + df['tax_payable'] +
                                        df['other_current_liabilities'] + df['current_deferred_revenue'])
                                             
               df['Total add'] =df['noncurrent_capital_leases']+df['lt_debt']

               df['Total Debt'] =df['Total Difference']+df['Total add'] 
                                             
               total = df.T
               total.columns = total.iloc[0]  # Use the first row as column names
               total = total[1:]
               total = total.applymap(lambda x: "{:,.0f}".format(x / 1000000))
                                             
               #print("total",total)

               

               total_debt_column = df['Total Debt']
               last_value_total_debt = total_debt_column.iloc[-1]

               Total_Debt_from_all_calc = last_value_total_debt/ 1000000000
          


          except Exception as e:    #if "Consumer Finance" in Industry or "Banks" in Industry or "Insurance" in Industry or "Health Care Providers & Services" in Industry:
               Short_term_debt_quarter = quarterly_data['st_debt'][-10:]
               LongTerm_debt_quarter = quarterly_data['lt_debt'][-10:]

               index = range(len(date_quarter))
               df = pd.DataFrame({
                    'period_end_date': date_quarter,
                    'lt_debt': LongTerm_debt_quarter,
                    'st_debt':Short_term_debt_quarter }, index=index)

               df['Total Debt'] =df['lt_debt']+df['st_debt'] 
                                             
               total = df.T
               total.columns = total.iloc[0]  # Use the first row as column names
               total = total[1:]
               total = total.applymap(lambda x: "{:,.0f}".format(x / 1000000))
                                             
               #print("total",total)

               

               total_debt_column = df['Total Debt']
               last_value_total_debt = total_debt_column.iloc[-1]

               Total_Debt_from_all_calc = last_value_total_debt/ 1000000000
               Total_cash_last_years = round((cash_equiv_quarter),3)
               rounded_gross_margin="-"
               five_yrs_average_gross_margin="-"
               rounded_operating_margin="-"
               rounded_operating_margin_five="-"
               #P_B_ttm ="NA"






          #print("Total_Debt_from_all_calc", Total_Debt_from_all_calc)
          
     # Total_DEbt_in_billion = "{:.2f}B".format(df.loc[9, 'Total Debt'] / 1000000000) if df.loc[9, 'Total Debt'] >= 1000000000 else "{:,.0f}M".format(df.loc[9, 'Total Debt'] / 1000000)
          Total_DEbt_in_billion = "{:.2f}B".format(last_value_total_debt/ 1000000000) if abs(last_value_total_debt)>= 1000000000 else "{:,.0f}M".format(last_value_total_debt / 1000000)
          #print("Last value from Total Debt column:", Total_DEbt_in_billion)
          #Total_Debt_from_all_calc=32.22
          Enterprise_value = "{:.2f}".format((Marketcap)+Total_Debt_from_all_calc-Total_cash_last_years)
          try:
               Enterprise_value = "{:.2f}".format((Marketcap)+Total_Debt_from_all_calc-Total_cash_last_years)
               #Enterprise_value =1
               #Enterprise_value_in_Billion = "{:.2f}".format((Marketcap)+Total_Debt_from_all_calc-Total_cash_last_years)
               enter=((Marketcap)+Total_Debt_from_all_calc-Total_cash_last_years)
               Enterprise_value_in_Billion = "{:.2f}T".format(enter/1000) if abs(enter) >= 1000 else "{:,.2f}B".format(enter / 1)

          except Exception as e:
     # Handle KeyError or TypeError here
               Enterprise_value = "N/A"
               Enterprise_value_in_Billion = "N/A"



          #Enterprise_value_in_Billion=1

          netincome_ttm=netincome_ttm*1000000000
          netincome_ttm ="{:.2f}B".format(netincome_ttm/ 1000000000) if abs(netincome_ttm) >= 1000000000 else "{:,.1f}M".format(netincome_ttm / 1000000)

          revenue_ttm = revenue_ttm*1000000000

          if revenue_ttm!=0.00 or Dividend_ttm>0 :
               Dividend_ttm ="{:.2f}B".format(abs(Dividend_ttm/ 1000000000)) if abs(Dividend_ttm) >= 1000000000 else "{:,.1f}M".format(abs(Dividend_ttm / 1000000))
               revenue_ttm ="{:.2f}B".format(revenue_ttm/ 1000000000) if abs(revenue_ttm)>= 1000000000 else "{:,.1f}M".format(revenue_ttm / 1000000)

          else:
               revenue_ttm="-"
               Dividend_ttm="-"

          fcf_ttm =fcf_ttm*1000000000
          fcf_ttm ="{:.2f}B".format(fcf_ttm/ 1000000000) if abs(fcf_ttm) >= 1000000000 else "{:,.1f}M".format(fcf_ttm / 1000000)

          
          #Net_Operating_CashFlow_ttm = Financial_data['ttm']['cf_cfo'] 
          current_Operating_cash_Flow =Financial_data['ttm']['cf_cfo']
          current_Operating_cash_Flow_Value ="{:.2f}B".format(current_Operating_cash_Flow/ 1000000000) if abs(current_Operating_cash_Flow) >= 1000000000 else "{:,.1f}M".format(current_Operating_cash_Flow / 1000000)

          if Financial_data['ttm']['cf_cfo'] !=0:
               P_OCF_ttm = "{:.2f}".format(Marketcap/(current_Operating_cash_Flow/1000000000))

          else:
               P_OCF_ttm = "-"
          #print(P_OCF_ttm)
          try:
                # Calculate the percentage increase
               percentage_difference_52_week_low = "{:.2f}%".format(((current_price - fifty_two_week_low) / fifty_two_week_low) * 100)

               percentage_diff_ATH = "{:.2f}%".format(((current_price - all_time_high_price) / all_time_high_price) * 100)
            
             
               
          except Exception as e:
               percentage_difference_52_week_low =""
               percentage_difference_ATH=""
              
          
         
                


          
          data1 = {
          'Market Cap (intraday)': [Marketcap_in_Billion],
          'Enterprise Value': [Enterprise_value_in_Billion], 
          #'Debt/EBITDA':[Net_debt_to_Ebitda],
          'Revenue (TTM)': [revenue_ttm],      
          '5 YR Net Income': [Average_netIncome_annual_we], 
          'Net Income (TTM)': [netincome_ttm], 
          'PEG': [PEG],
          'Forward P/E': [forwardPE], 
          'P/E (TTM)': [pe_ttm],
          '5 YR P/E': [pe_five_],
          '10 YR P/E': [average_PE_historical],
          'Operating Cash Flow (TTM)': [current_Operating_cash_Flow_Value], 
          'Price/OCF (TTM)':[P_OCF_ttm],  
          '5 YR Price/OCF ':[P_OCF_5],  
          '10 YR Price/OCF':[P_OCF_10],  
          '5 YR Gross Profit Margin': [five_yrs_average_gross_margin],
          'Gross Profit Margin (TTM)': [rounded_gross_margin],
          
         
                 
          }
         

          data2 = {
          '5 YR Dividend Yield': [Dividend_yield_average], 
          'Dividend Yield': [Dividend_per_share_yield],
          'Dividend Paid (TTM)': [Dividend_ttm], 
          'Dividend/Share (TTM)':f"$ {Dividend_TTM}",
          'Dividend Estimate':f"$ {Dividend_Est}",
          'Dividend Ex-Date':[Dividend_Ex_Date],
          '5 YR Avg FCF': [average_FCF_annual_five_we], 
          'Free Cash Flow (TTM)': [fcf_ttm],
          'Price/FCF (TTM)': [pfcf_ttm], 
          '5 YR Avg Price/FCF':[pfcf_funf],
          '10 YR Avg Price/FCF':[pfcf_ten],
          '5 YR Operating Margin': [rounded_operating_margin_five],
          'Operating Margin': [rounded_operating_margin],
          '5 YR Net Profit Margin':f"{five_yrs_Nettomarge}%",
          'Net Profit Margin': [Net_margin_ttm],
          '5 YR FCF Margin':f"{FCF_Margin_5}%",
          'FCF Margin': ' {:.2f}%'.format(FCF_Margin_1)
          
          
          
      
        
          }
          #date_obj = datetime.strptime(formatted_date,min_price_date, "%Y/%m/%d")
          date_obj = datetime.strptime(formatted_date, "%Y/%m/%d")

          # Convert 'min_price_date' string to datetime object
          #min_price_date_obj = datetime.strptime(min_price_date, '%Y/%m/%d')

          # Convert 'min_price_date_obj' datetime object back to string in the format 'YYYY/MM/DD'
         # min_price_date_str = datetime.strftime(min_price_date_obj, '%Y/%m/%d')

          all_time_high_date = formatted_date
#          min_price_date = min_price_date

          data3 = {
          'FCF Yield':[fcf_yield_ttm],
          'P/S': [Price_to_sales_last],
          'ROA': [average_ROA_annual_ttm],
          '5 YR ROE': ["{:.5}%".format(five_ROE)],
          'ROE': [ROE_ttm],
          '5 YR ROIC': [Average_ROIC_funf],
          'ROIC': [ROIC_annual_one],
          '5 YR ROCE': [ "{:.2f}%".format(five_yrs_ROCE)],
          'ROCE ':[ "{:.2f}%".format(One_YR_ROCE)],
          #f'ATH ({all_time_high_date}'")": ["$ {:.2f}".format(all_time_high_price)],
          f'ATH ({all_time_high_date}'")": f"$ {all_time_high_price:.2f} ({percentage_diff_ATH})",
         

          #f'52WK LOW ( {min_price_date.strftime("%Y/%m/%d")})': ["$ {:.2f}".format(fifty_two_week_low)]
          #f'52WK LOW ({min_price_date.strftime("%Y/%m/%d")}): $ {fifty_two_week_low:.2f} ({percentage_difference_52_week_low})'
          f'52WK LOW ({min_price_date.strftime("%Y/%m/%d")})': f"$ {fifty_two_week_low:.2f} ({percentage_difference_52_week_low})"
 
          }   


         # eps_basic_ttm =Financial_data['ttm']['eps_basic']
          #st.write("eps_basic_ttm",eps_basic_ttm)
          data4 = {
          
          #'Forward P/E': [forwardPE], 
          'EPS (TTM)':["$ {:.2f}".format(eps_diluted_ttm)],
          'EPS Estimate this YR': f"{Earnings_this_yr}",
         # 'EPS Estimate next YR':[Earnings_next_yr_in_prozent],
          'EPS Estimate next YR': f"$ {Earnings_next_yr_in_value} ({Earnings_next_yr_in_prozent})",
          #'EPS Estimate next YR':f"$ {Earnings_next_yr_in_value}",
          'EPS Estimate 5 YR':[Earnings_next_5_yrs],
          'EPS past 5 YR':f"{EPS_5_CAGR}% ",
          'Beta': [Beta],
          'RSI (14)': [RSI],
          '50 SMA' : [Moving_50],
          '200 SMA':[Moving_200],
          #'Earnings':[Earnings],
          'Analyst Target Price':  [f"$ {Target_Price}"],
          'Current price': ["$ {:.2f}".format(amount)] 
          #'Price Change':[Price_Change]      
#"{:.2f}".format(((sum(pe_one) / len(pe_one))))
          }
               # Convert data into DataFrames
          df1 = pd.DataFrame(data1).transpose()                                      
          df2 = pd.DataFrame(data2).transpose()
          df3 = pd.DataFrame(data3).transpose()
          df4 = pd.DataFrame(data4).transpose()

          # # Reset column index to start from 1
          # df1.columns = range(1, len(df1.columns) + 1)
          # df2.columns = range(2, len(df2.columns) + 2)
          # df3.columns = range(3, len(df3.columns) + 3)
          # df4.columns = range(4, len(df4.columns) + 4)
          

        
          # #style = "color: #2E8B57"
          # style = "color: #2E8B57; text-align: center"

          # styled_df1 = df1.style.applymap(lambda x: style).set_caption("")
          # styled_df2 = df2.style.applymap(lambda x: style).set_caption("")
          # styled_df3 = df3.style.applymap(lambda x: style).set_caption("")
          # styled_df4 = df4.style.applymap(lambda x: style).set_caption("")
          

          # Rename columns to replace indices with "ratios"
          df1 = df1.rename(columns={i: " " for i in df1.columns})
          df2 = df2.rename(columns={i: " " for i in df2.columns})
          df3 = df3.rename(columns={i: " " for i in df3.columns})
          df4 = df4.rename(columns={i: " " for i in df4.columns})

          # Apply styling to DataFrames
          style = "color: #2E8B57; text-align: center"
          styled_df1 = df1.style.applymap(lambda x: style).set_caption("")
          styled_df2 = df2.style.applymap(lambda x: style).set_caption("")
          styled_df3 = df3.style.applymap(lambda x: style).set_caption("")
          styled_df4 = df4.style.applymap(lambda x: style).set_caption("")

          

          # Create a responsive layout with three columns
          #col1, col2, col3 = st.columns(3)
          col1, col2, col3, col4 = st.columns(4)

          # Display the dataframes in each column
          with col1:
               st.table(styled_df1)
          with col2:
               st.table(styled_df2)
          with col3:
               st.table(styled_df3)
          with col4:
               st.table(styled_df4)
                         




     #----------------------------------------------------------------------------
          # Display the first 20 characters of the description
          short_description = Stock_description[:20]
          #with st.expander("Description: Read More"):
               # English expander
          #with st.expander("Description (English): Read More"):
          #st.write("About",name)
          st.markdown(f"About <u style='color:green;'>{name}</u>", unsafe_allow_html=True)


          st.write(Stock_description)

          # German expander
     # with st.expander("Beschreibung (Deutsch): Mehr lesen"):
          #     try:
          #         translator = Translator()
          #        target_language = 'de'  # German
          #       translated_text = translator.translate(Stock_description, src='en', dest=target_language)
          #      translated_text_only = translated_text.text
               #     st.write(translated_text_only)

               #except TypeError:
               #    st.write("Nicht vorhanden auf Deutsch")
                    
               # Print the translation
               #print(f"Original Text: {Stock_description}")
               #print(f"Translated Text ({translated_text.text}")
     #----------------------------------------------------------------------------
          



          disclaimer = """
          The information provided on this website is intended for informational purposes only and does not constitute financial advice, investment recommendations, or a solicitation to buy or sell any securities. The content and data presented on this website are not tailored to your specific investment goals, financial situation, or risk tolerance. You should always consult with a qualified financial advisor before making investment decisions.
          """
          # The stock and financial data provided on this website may be delayed, inaccurate, or subject to errors. We make no representations or warranties about the accuracy, completeness, or reliability of the information presented. Any reliance you place on such information is strictly at your own risk.
          # Past performance is not indicative of future results. Investments in stocks, securities, and financial instruments involve risks, including the loss of your invested capital. Market conditions can change rapidly, and investment values can fluctuate.
          # This website may contain links to third-party websites or content. We do not endorse or control the content of these external sites and are not responsible for their accuracy, legality, or availability.
          # We are not licensed financial advisors, and the content provided on this website should not be construed as professional financial advice. You are solely responsible for evaluating the suitability of any investment decisions based on your individual circumstances and objectives.
          # By using this website, you agree to hold us harmless from any and all claims, losses, liabilities, or damages resulting from your reliance on the information presented herein. We reserve the right to modify or discontinue the content and services offered on this website at any time.
          # Please consult with a qualified financial professional and conduct your own research before making any investment decisions. We encourage you to review the terms of use and privacy policy of this website for more information about your use of this site.
          # For specific legal, tax, and financial advice, you should contact your own attorney, accountant, or other professional advisors..
          

          st.markdown("<style>body { font-family: serif; }</style>", unsafe_allow_html=True)
          st.markdown("<u><h3 style='color:#FF4B4B;'>Disclaimer</h3></u>", unsafe_allow_html=True)
          #short_description = disclaimer[:20]
          #with st.expander("Read More"):
          st.write(disclaimer)
          

          #st.header("Found an error or have an idea? Write us an email!")
          #st.markdown("<h1 style='font-family: serif; font-size: 24px; text-align: center;'>Found an error or have an idea? Write us an email!</h1>", unsafe_allow_html=True, use_container_width=True)

        

          # Text mit benutzerdefiniertem CSS und Container-Breite
          st.markdown(custom_css, unsafe_allow_html=True)
          st.markdown('<div class="my-header">Found an error or have an idea? Write us an Email!</div>', unsafe_allow_html=True)
             
     # ---- Documentation : https://formsubmit.co/
          contact_form = """
               <form action="https://formsubmit.co/nedumokonkwo@gmail.com" method="POST">
                    <input type = "hidden" name="_captcha" value="false">
                    <input type="text" name="name" placeholder="Your name" required>
                    <input type="email" name="email" placeholder="Your email" required>
                    <input type="country" name="country" placeholder="Your country" required>
                    <textarea name ="message" placeholder="Your message here" required></textarea>
                    <button type="submit">Send</button>
               </form>
               """

               
          st.markdown(contact_form, unsafe_allow_html = True)



      

          def local_css(file_name):
                    with open(file_name)as f:
                         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)      
          local_css("style.css")

          current_year = datetime.now().year
 
          st.markdown(f'&copy; {2023} - {current_year} Stock valuation', unsafe_allow_html=True)
     #.............................................................
# Assuming revenue_list and gross_profit_list are extracted from the API response
with st.container():
     with Financials:
          Income_Statement, Balance_Sheet, Cash_Flow = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])

          with Cash_Flow:
               Annual,Quarterly = st.tabs(["Annual","Quarterly"])
               
               with Annual:
                    Changes_in_working_capital_annual = annual_data['cfo_change_in_working_capital'][-10:] 
                    Capex_annual = annual_data['capex'][-10:] 
                    Net_Assets_from_Acquisitions_annual = annual_data['cfi_acquisitions'][-10:] 
                    Purchase_of_Investment_annual = annual_data['cfi_investment_purchases'][-10:]
                    Sale_maturity_of_Investments_annual = annual_data['cfi_investment_sales'][-10:]
                    Net_investing_CashFlow_annual = annual_data['cf_cfi'][-10:] 
                    Cash_Dividends_paid_Total_annual = annual_data['cff_dividend_paid'][-10:] 
                    Insurance_Reduction_of_DebtNet_annual = annual_data['cff_debt_net'][-10:]
                    #Cash_Dividends_paid_Total_annual = annual_data['cff_dividend_paid'][-10:]
                    Repurchase_of_common_Preferred_stock_annual = annual_data['cff_common_stock_repurchased'][-10:]
                    Net_Financing_cashFlow_annual = annual_data['cf_cff'][-10:]
                    Net_change_in_cash_annual = annual_data['cf_net_change_in_cash'][-10:]
                    Free_cash_flow_annual = annual_data['fcf'][-10:]

                    index = range(len(date_list_annual))


                    
                    FFO = pd.DataFrame({'Period End Date': date_list_annual,
                                                       'Operating Cash Flow': Net_Operating_CashFlow_annual,
                                                       'Changes In Working Capital': Changes_in_working_capital_annual
                                                       }, index=index)
                              # Convert JSON data to a DataFrame
                    df = pd.DataFrame(FFO)

                              # Add a new column "total_cashflow" which is the sum of the two columns
                    df["Funds from Operations"] = df["Operating Cash Flow"] + df["Changes In Working Capital"]
                         
                    total = df.T

                                   # Replace the numbering with the actual date
                    total.columns = total.iloc[0]  # Use the first row as column names
                    total = total[1:]  

                    total_annual = total.applymap(lambda x: "{:.2f}B".format(x / 1e9) if abs(x)>= 1e9 else "{:,.0f}M".format(x / 1e6))


                    #Changes_in_working_capital_annual_table= ["{:.2f}B".format(cfo_change_in_working_capital / 1000000000) if cfo_change_in_working_capital >= 1000000000 else "{:,.0f}M".format(cfo_change_in_working_capital / 1000000)for cfo_change_in_working_capital in Changes_in_working_capital_annual]
                    #Changes_in_working_capital_annual_df = pd.DataFrame(Changes_in_working_capital_annual_table, index=date_list_annual,  columns=["Changes in Working Capital"])
                    #Changes_in_working_capital_annual_df = Changes_in_working_capital_annual_df.transpose()

                    #Net_Operating_CashFlow_annual_table= ["{:.2f}B".format(cf_cfo / 1000000000) if cf_cfo >= 1000000000 else "{:,.0f}M".format(cf_cfo / 1000000)for cf_cfo in Net_Operating_CashFlow_annual]
                    #Net_Operating_CashFlow_annual_df = pd.DataFrame(Net_Operating_CashFlow_annual_table, index=date_list_annual,  columns=["Operating Cash Flow"])
                    #Net_Operating_CashFlow_annual_df = Net_Operating_CashFlow_annual_df.transpose()

                    Capex_annual_table= ["{:.2f}B".format(capex / 1000000000) if abs(capex) >= 1000000000 else "{:,.0f}M".format(capex / 1000000)for capex in Capex_annual]
                    Capex_annual_df = pd.DataFrame(Capex_annual_table, index=date_list_annual,  columns=["Capital Expenditure"])
                    Capex_annual_df = Capex_annual_df.transpose()
                    


                    Net_Assets_from_Acquisitions_annual_table= ["{:.2f}B".format(cfi_acquisitions / 1000000000) if abs(cfi_acquisitions) >= 1000000000 else "{:,.0f}M".format(cfi_acquisitions / 1000000)for cfi_acquisitions in Net_Assets_from_Acquisitions_annual]
                    Net_Assets_from_Acquisitions_annual_df = pd.DataFrame(Net_Assets_from_Acquisitions_annual_table, index=date_list_annual,  columns=["Acquisitions, net"])
                    Net_Assets_from_Acquisitions_annual_df = Net_Assets_from_Acquisitions_annual_df.transpose()

                    Purchase_of_Investment_annual_table= ["{:.2f}B".format(cfi_investment_purchases / 1000000000) if abs(cfi_investment_purchases) >= 1000000000 else "{:,.0f}M".format(cfi_investment_purchases / 1000000)for cfi_investment_purchases in Purchase_of_Investment_annual]
                    Purchase_of_Investment_annual_df = pd.DataFrame(Purchase_of_Investment_annual_table, index=date_list_annual,  columns=["Purchase of Investments"])
                    Purchase_of_Investment_annual_df = Purchase_of_Investment_annual_df.transpose()

                    Sale_maturity_of_Investments_annual_table=["{:.2f}B".format(cfi_investment_sales / 1000000000) if abs(cfi_investment_sales) >= 1000000000 else "{:,.0f}M".format(cfi_investment_sales / 1000000)for cfi_investment_sales in Sale_maturity_of_Investments_annual]
                    Sale_maturity_of_Investments_annual_df = pd.DataFrame(Sale_maturity_of_Investments_annual_table, index=date_list_annual,  columns=["Sale/Maturity of Investments"])
                    Sale_maturity_of_Investments_annual_df = Purchase_of_Investment_annual_df.transpose()

                    Net_investing_CashFlow_annual_table= ["{:.2f}B".format(cf_cfi / 1000000000) if abs(cf_cfi) >= 1000000000 else "{:,.0f}M".format(cf_cfi / 1000000)for cf_cfi in Net_investing_CashFlow_annual]
                    Net_investing_CashFlow_annual_df = pd.DataFrame(Net_investing_CashFlow_annual_table, index=date_list_annual,  columns=["Net Investing Cash Flow"])
                    Net_investing_CashFlow_annual_df = Net_investing_CashFlow_annual_df.transpose()

                    Cash_Dividends_paid_Total_annual_table= ["{:.2f}B".format(abs(cff_dividend_paid) / 1000000000) if abs(cff_dividend_paid) >= 1000000000 else "{:,.0f}M".format(abs(cff_dividend_paid) / 1000000)for cff_dividend_paid in Cash_Dividends_paid_Total_annual]
                    Cash_Dividends_paid_Total_annual_df = pd.DataFrame(Cash_Dividends_paid_Total_annual_table, index=date_list_annual,  columns=["Cash Dividends Paid"])
                    Cash_Dividends_paid_Total_annual_df = Cash_Dividends_paid_Total_annual_df.transpose()

                    Insurance_Reduction_of_DebtNet_annual_table= ["{:.2f}B".format(cff_debt_net / 1000000000) if abs(cff_debt_net) >= 1000000000 else "{:,.0f}M".format(cff_debt_net / 1000000)for cff_debt_net in Insurance_Reduction_of_DebtNet_annual]
                    Insurance_Reduction_of_DebtNet_annual_df = pd.DataFrame(Insurance_Reduction_of_DebtNet_annual_table, index=date_list_annual,  columns=["Issuance/Reduction of Debt,Net"])
                    Insurance_Reduction_of_DebtNet_annual_df = Insurance_Reduction_of_DebtNet_annual_df.transpose()

                    Repurchase_of_common_Preferred_stock_annual_table= ["{:.2f}B".format(cff_common_stock_repurchased / 1000000000) if abs(cff_common_stock_repurchased) >= 1000000000 else "{:,.0f}M".format(cff_common_stock_repurchased / 1000000)for cff_common_stock_repurchased in Repurchase_of_common_Preferred_stock_annual]
                    Repurchase_of_common_Preferred_stock_annual_df = pd.DataFrame(Repurchase_of_common_Preferred_stock_annual_table, index=date_list_annual,  columns=["Repurchase Comm. & Pref. Stks"])
                    Repurchase_of_common_Preferred_stock_annual_df = Repurchase_of_common_Preferred_stock_annual_df.transpose()

                    Net_Financing_cashFlow_annual_table= ["{:.2f}B".format(cf_cff / 1000000000) if abs(cf_cff) >= 1000000000 else "{:,.0f}M".format(cf_cff / 1000000)for cf_cff in Net_Financing_cashFlow_annual]
                    Net_Financing_cashFlow_annual_df = pd.DataFrame(Net_Financing_cashFlow_annual_table, index=date_list_annual,  columns=["Net Financing Cash Flow"])
                    Net_Financing_cashFlow_annual_df = Net_Financing_cashFlow_annual_df.transpose()

                    Net_change_in_cash_annual_table= ["{:.2f}B".format(cf_net_change_in_cash / 1000000000) if abs(cf_net_change_in_cash) >= 1000000000 else "{:,.0f}M".format(cf_net_change_in_cash / 1000000)for cf_net_change_in_cash in Net_change_in_cash_annual]
                    Net_change_in_cash_annual_df = pd.DataFrame(Net_change_in_cash_annual_table, index=date_list_annual,  columns=["Net Change in Cash"])
                    Net_change_in_cash_annual_df = Net_change_in_cash_annual_df.transpose()

                    Free_cash_flow_annual_table= ["{:.2f}B".format(fcf / 1000000000) if abs(fcf) >= 1000000000 else "{:,.0f}M".format(fcf / 1000000)for fcf in Free_cash_flow_annual]
                    Free_cash_flow_annual_df = pd.DataFrame(Free_cash_flow_annual_table, index=date_list_annual,  columns=["Free Cash Flow"])
                    Free_cash_flow_annual_df = Free_cash_flow_annual_df.transpose()



                    merged_df = pd.concat([total_annual,Capex_annual_df,Net_Assets_from_Acquisitions_annual_df,Purchase_of_Investment_annual_df,Net_investing_CashFlow_annual_df,Cash_Dividends_paid_Total_annual_df,Insurance_Reduction_of_DebtNet_annual_df,Repurchase_of_common_Preferred_stock_annual_df,Net_Financing_cashFlow_annual_df,Net_change_in_cash_annual_df,Free_cash_flow_annual_df]) 
                              
                    

                    st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))

                    
                    #st.dataframe(merged_df.style.set_table_attributes('class="scroll-table"'),use_container_width=True)
                    #st.markdown('<div style="margin-bottom: 100px;"></div>', unsafe_allow_html=True)


                    

                    with Quarterly:
                         
                         Net_Operating_CashFlow_quarter = quarterly_data['cf_cfo'][-10:] 
                         changes_in_working_capital_quarter = quarterly_data['cfo_change_in_working_capital'][-10:] 
                         Capex_quarter = quarterly_data['capex'][-10:] 
                         Net_Assets_from_Acquisitions_quarter = quarterly_data['cfi_acquisitions'][-10:] 
                         Purchase_of_Investment_quarter = quarterly_data['cfi_investment_purchases'][-10:]
                         Sale_maturity_of_Investments_quarter = quarterly_data['cfi_investment_sales'][-10:]
                         Net_investing_CashFlow_quarter = quarterly_data['cf_cfi'][-10:] 
                         Cash_Dividends_paid_Total_quarter = quarterly_data['cff_dividend_paid'][-10:] 
                         Insurance_Reduction_of_DebtNet_quarter = quarterly_data['cff_debt_net'][-10:]
                         Cash_Dividends_paid_Total_annual = annual_data['cff_dividend_paid'][-10:]
                         Repurchase_of_common_Preferred_stock_quarter = quarterly_data['cff_common_stock_repurchased'][-10:]
                         Net_Financing_cashFlow_quarter = quarterly_data['cf_cff'][-10:]
                         Net_change_in_cash_quarter = quarterly_data['cf_net_change_in_cash'][-10:]
                         Free_cash_flow_quarter = quarterly_data['fcf'][-10:]


                    
                         index = range(len(date_quarter))
                         FFO = pd.DataFrame({'Period End Date': date_quarter,
                                                       'Operating Cash Flow': Net_Operating_CashFlow_quarter,
                                                       'Changes In Working Capital': changes_in_working_capital_quarter
                                                       }, index=index)
                              # Convert JSON data to a DataFrame
                         df = pd.DataFrame(FFO)

                              # Add a new column "total_cashflow" which is the sum of the two columns
                         df["Funds from Operations"] = df["Operating Cash Flow"] + df["Changes In Working Capital"]
                         
                         total = df.T

                                   # Replace the numbering with the actual date
                         total.columns = total.iloc[0]  # Use the first row as column names
                         total = total[1:]  # Remove the first row

                                        # Convert the numbers to billions and display with 2 decimal places
                                        #total = (total / 1e9).round(2)
                                        
                                        #total = "{:.2f}B".format((total/1000000000))
                         #total_qaurter = total.applymap(lambda x: "{:.2f}B".format(x / 1e9))
                         total_quarter = total.applymap(lambda x: "{:.2f}B".format(x / 1e9) if abs(x) >= 1e9 else "{:,.0f}M".format(x / 1e6))




                         #changes_in_working_capital_quarter_table= ["{:.2f}B".format(cfo_change_in_working_capital / 1000000000) if cfo_change_in_working_capital >= 1000000000 else "{:,.0f}M".format(cfo_change_in_working_capital / 1000000)for cfo_change_in_working_capital in changes_in_working_capital_quarter]
                         #changes_in_working_capital_quarter_df = pd.DataFrame(changes_in_working_capital_quarter_table, index=date_list_quarter,  columns=["Changes in Working Capital"])
                         #changes_in_working_capital_quarter_df = changes_in_working_capital_quarter_df.transpose()

                         #Net_Operating_CashFlow_quarter_table= ["{:.2f}B".format(cf_cfo / 1000000000) if cf_cfo >= 1000000000 else "{:,.0f}M".format(cf_cfo / 1000000)for cf_cfo in Net_Operating_CashFlow_quarter]
                         #Net_Operating_CashFlow_quarter_df = pd.DataFrame(Net_Operating_CashFlow_quarter_table, index=date_list_quarter,  columns=["Operating Cash Flow"])
                         #Net_Operating_CashFlow_quarter_df = Net_Operating_CashFlow_quarter_df.transpose()

                         Capex_quarter_table= ["{:.2f}B".format(capex / 1000000000) if abs(capex) >= 1000000000 else "{:,.0f}M".format(capex / 1000000)for capex in Capex_quarter]
                         Capex_quarter_df = pd.DataFrame(Capex_quarter_table, index=date_list_quarter,  columns=["Capital Expenditure"])
                         Capex_quarter_df = Capex_quarter_df.transpose()

                         Net_Assets_from_Acquisitions_quarter_table= ["{:.2f}B".format(cfi_acquisitions / 1000000000) if abs(cfi_acquisitions) >= 1000000000 else "{:,.0f}M".format(cfi_acquisitions / 1000000)for cfi_acquisitions in Net_Assets_from_Acquisitions_quarter]
                         Net_Assets_from_Acquisitions_quarter_df = pd.DataFrame(Net_Assets_from_Acquisitions_quarter_table, index=date_list_quarter,  columns=["Acquisitions, net"])
                         Net_Assets_from_Acquisitions_quarter_df = Net_Assets_from_Acquisitions_quarter_df.transpose()

                         Purchase_of_Investment_quarter_table= ["{:.2f}B".format(cfi_investment_purchases / 1000000000) if abs(cfi_investment_purchases) >= 1000000000 else "{:,.0f}M".format(cfi_investment_purchases / 1000000)for cfi_investment_purchases in Purchase_of_Investment_quarter]
                         Purchase_of_Investment_quarter_df = pd.DataFrame(Purchase_of_Investment_quarter_table, index=date_list_quarter,  columns=["Purchase of Investments"])
                         Purchase_of_Investment_quarter_df = Purchase_of_Investment_quarter_df.transpose()

                         Sale_maturity_of_Investments_quarter_table= ["{:.2f}B".format(cfi_investment_sales / 1000000000) if abs(cfi_investment_sales) >= 1000000000 else "{:,.0f}M".format(cfi_investment_sales / 1000000)for cfi_investment_sales in Sale_maturity_of_Investments_quarter]
                         Sale_maturity_of_Investments_quarter_df = pd.DataFrame(Sale_maturity_of_Investments_quarter_table, index=date_list_quarter,  columns=["Sale/Maturity of Investments"])
                         Sale_maturity_of_Investments_quarter_df = Purchase_of_Investment_quarter_df.transpose()

                         Net_investing_CashFlow_quarter_table= ["{:.2f}B".format(cf_cfi / 1000000000) if abs(cf_cfi) >= 1000000000 else "{:,.0f}M".format(cf_cfi / 1000000)for cf_cfi in Net_investing_CashFlow_quarter]
                         Net_investing_CashFlow_quarter_df = pd.DataFrame(Net_investing_CashFlow_quarter_table, index=date_list_quarter,  columns=["Net Investing Cash Flow"])
                         Net_investing_CashFlow_quarter_df = Net_investing_CashFlow_quarter_df.transpose()

                         Cash_Dividends_paid_Total_quarter_table= ["{:.2f}B".format(abs(cff_dividend_paid) / 1000000000) if abs(cff_dividend_paid) >= 1000000000 else "{:,.0f}M".format(abs(cff_dividend_paid) / 1000000)for cff_dividend_paid in Cash_Dividends_paid_Total_quarter]
                         Cash_Dividends_paid_Total_quarter_df = pd.DataFrame(Cash_Dividends_paid_Total_quarter_table, index=date_list_quarter,  columns=["Cash Dividends Paid"])
                         Cash_Dividends_paid_Total_quarter_df = Cash_Dividends_paid_Total_quarter_df.transpose()

                         Insurance_Reduction_of_DebtNet_quarter_table= ["{:.2f}B".format(cff_debt_net / 1000000000) if abs(cff_debt_net) >= 1000000000 else "{:,.0f}M".format(cff_debt_net / 1000000)for cff_debt_net in Insurance_Reduction_of_DebtNet_quarter]
                         Insurance_Reduction_of_DebtNet_quarter_df = pd.DataFrame(Insurance_Reduction_of_DebtNet_quarter_table, index=date_list_quarter,  columns=["Issuance/Reduction of Debt,Net"])
                         Insurance_Reduction_of_DebtNet_quarter_df = Insurance_Reduction_of_DebtNet_quarter_df.transpose()

                         Repurchase_of_common_Preferred_stock_quarter_table= ["{:.2f}B".format(cff_common_stock_repurchased / 1000000000) if abs(cff_common_stock_repurchased) >= 1000000000 else "{:,.0f}M".format(cff_common_stock_repurchased / 1000000)for cff_common_stock_repurchased in Repurchase_of_common_Preferred_stock_quarter]
                         Repurchase_of_common_Preferred_stock_quarter_df = pd.DataFrame(Repurchase_of_common_Preferred_stock_quarter_table, index=date_list_quarter,  columns=["Repurchase Comm. & Pref. Stks"])
                         Repurchase_of_common_Preferred_stock_quarter_df = Repurchase_of_common_Preferred_stock_quarter_df.transpose()

                         Net_Financing_cashFlow_quarter_table= ["{:.2f}B".format(cf_cff / 1000000000) if abs(cf_cff) >= 1000000000 else "{:,.0f}M".format(cf_cff / 1000000)for cf_cff in Net_Financing_cashFlow_quarter]
                         Net_Financing_cashFlow_quarter_df = pd.DataFrame(Net_Financing_cashFlow_quarter_table, index=date_list_quarter,  columns=["Net Financing Cash Flow"])
                         Net_Financing_cashFlow_quarter_df = Net_Financing_cashFlow_quarter_df.transpose()

                         Net_change_in_cash_quarter_table= ["{:.2f}B".format(cf_net_change_in_cash / 1000000000) if abs(cf_net_change_in_cash) >= 1000000000 else "{:,.0f}M".format(cf_net_change_in_cash / 1000000)for cf_net_change_in_cash in Net_change_in_cash_quarter]
                         Net_change_in_cash_quarter_df = pd.DataFrame(Net_change_in_cash_quarter_table, index=date_list_quarter,  columns=["Net Change in Cash"])
                         Net_change_in_cash_quarter_df = Net_change_in_cash_quarter_df.transpose()

                         Free_cash_flow_quarter_table= ["{:.2f}B".format(fcf / 1000000000) if abs(fcf) >= 1000000000 else "{:,.0f}M".format(fcf / 1000000)for fcf in Free_cash_flow_quarter]
                         Free_cash_flow_quarter_df = pd.DataFrame(Free_cash_flow_quarter_table, index=date_list_quarter,  columns=["Free Cash Flow"])
                         Free_cash_flow_quarter_df = Free_cash_flow_quarter_df.transpose()



                         merged_df = pd.concat([total_quarter,Capex_quarter_df,Net_Assets_from_Acquisitions_quarter_df,Purchase_of_Investment_quarter_df,Net_investing_CashFlow_quarter_df,Cash_Dividends_paid_Total_quarter_df,Insurance_Reduction_of_DebtNet_quarter_df,Repurchase_of_common_Preferred_stock_quarter_df,Net_Financing_cashFlow_quarter_df,Net_change_in_cash_quarter_df,Free_cash_flow_quarter_df])           
                         
                         st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))


                         #st.dataframe(merged_df.style.set_table_attributes('class="scroll-table"'),use_container_width=True)
                                                           
                         #st.markdown('<div style="margin-bottom: 100px;"></div>', unsafe_allow_html=True)
                      


                         with Balance_Sheet:
                              Annual,Quarterly = st.tabs(["Annual","Quarterly"])

                              period_end_dates = annual_data['period_end_date'][-10:]
                              date_quarterly_Balance_Sheet = quarterly_data['period_end_date'][-10:] 
                              
                              with Annual:

                                   #if "Consumer Finance" in Industry or "Banks" in Industry or ticker == "MAIN":
                                   try:
                                        cash_und_cash_investments = annual_data['cash_and_equiv'][-10:]
                                        st_investments_annual = annual_data['total_investments'][-10:]
                                        #Total_current_assets_annual = annual_data['total_current_assets'][-10:]
                                        #Income_Tax_payable_annual = annual_data['tax_payable'][-10:]
                                        #Total_current_liabilities_annual = annual_data['total_current_liabilities'][-10:]
                                        #Total_current_assets_annual = annual_data['total_current_assets'][-10:]
                                        Intangible_assets_annual = annual_data['intangible_assets'][-10:]
                                        Net_goodwill_annual = annual_data['goodwill'][-10:]
                                        #Other_assets_annual = annual_data['other_assets'][-10:]
                                        Total_assets_annual = annual_data['total_assets'][-10:]
                                        Short_term_debt_annual = annual_data['st_debt'][-10:]
                                        #Income_Tax_payable_annual = annual_data['tax_payable'][-10:]
                                        #Total_current_liabilities_annual = annual_data['total_current_liabilities'][-10:]
                                        LongTerm_debt_annual = annual_data['lt_debt'][-10:]
                                        #Other_LongTerm_liabilites_annual = annual_data['other_lt_liabilities'][-10:]
                                        #Total_debt_annual = annual_data[''][-10:]
                                        Other_longterm_liabilities_annual = annual_data['other_lt_liabilities'][-10:]
                                        Total_liabilities_annual = annual_data['total_liabilities'][-10:]
                                        #Total_Sharehold_equity_annual = annual_data[''][-10:]
                                        Total_Equity_annual = annual_data['total_equity'][-10:]
                                        #Income_Tax_payable_annual = annual_data['tax_payable'][-10:]
                                        #Total_current_liabilities_annual = annual_data['total_current_liabilities'][-10:]
                                        #Liabili_shareholders_Equity_annual = annual_data[''][-10:]
                                        #Nopat_Annual = annual_data['nopat'][-10:]
                                        Deposits_annual = annual_data['deposits_liability'][-10:]
                                        Gross_loans_annual = annual_data['loans_gross'][-10:]
                                        Loans_loss_annual = annual_data['allowance_for_loan_losses'][-10:]
                                        Net_Loan_annual = annual_data['loans_net'][-10:]


                                        

                                        #---------------------------------Quarterly---------------------------------
                                        
                                   

                                        cash_and_equiv_quarterly_Balance_Sheet = quarterly_data['cash_and_equiv'][-10:]
                                        st_investments_quarterly_Balance_Sheet = quarterly_data['total_investments'][-10:]
                                        #Inventories_quarter = quarterly_data['inventories'][-10:]
                                        #Total_current_assets_quarter = quarterly_data['total_current_assets'][-10:]
                                        Intangible_assets_quarter= quarterly_data['intangible_assets'][-10:]
                                        Net_goodwill_quarter= quarterly_data['goodwill'][-10:]
                                        #Other_assets_quarter = quarterly_data['other_assets'][-10:]
                                        Total_assets_quarter = quarterly_data['total_assets'][-10:]
                                        #Accounts_payable_quarter = quarterly_data['accounts_payable'][-10:]
                                        #Current_accrued_liab_quarter = quarterly_data['current_accrued_liabilities'][-10:]
                                        #Tax_payable_quarter = quarterly_data['tax_payable'][-10:]
                                        #Other_current_liabilities_quarter = quarterly_data['other_current_liabilities'][-10:]
                                        #Current_deferred_revenue_quarter = quarterly_data['current_deferred_revenue'][-10:]
                                        #Total_current_liabilities_quarter = quarterly_data['total_current_liabilities'][-10:] 
                                        Short_term_debt_quarter = quarterly_data['st_debt'][-10:]
                                        #current_portion_of_lease_obligation = quarterly_data['current_capital_leases'][-10:]
                                        #capital_leases = quarterly_data['noncurrent_capital_leases'][-10:]
                                        LongTerm_debt_quarter = quarterly_data['lt_debt'][-10:]
                                        #Total_debt_quarter = quarterly_data[''][-10:]
                                        Other_longterm_liabilities_quarter = quarterly_data['other_lt_liabilities'][-10:]
                                        Total_liabilities_quarter = quarterly_data['total_liabilities'][-10:]
                                        #Total_Sharehold_equity_quarter = quarterly_data[''][-10:]
                                        Total_Equity_quarter = quarterly_data['total_equity'][-10:]
                                        Deposits_quarter = quarterly_data['deposits_liability'][-10:]
                                        Gross_loans_quarter = quarterly_data['loans_gross'][-10:]
                                        Loans_loss_quarter = quarterly_data['allowance_for_loan_losses'][-10:]
                                        Net_Loan_quarter = quarterly_data['loans_net'][-10:]


                                        cash_und_cash_investments_annual= ["{:.2f}B".format(cash_and_equiv / 1000000000) if abs(cash_and_equiv) >= 1000000000 else "{:,.0f}M".format(cash_and_equiv / 1000000)for cash_and_equiv in cash_und_cash_investments]
                                        cash_und_cash_investments_annual_df = pd.DataFrame(cash_und_cash_investments_annual, index=date_list_annual,  columns=["Total Cash"])
                                        cash_und_cash_investments_annual_df = cash_und_cash_investments_annual_df.transpose()

                                        Intangible_assets_annual_table= ["{:.2f}B".format(intangible_assets / 1000000000) if abs(intangible_assets) >= 1000000000 else "{:,.0f}M".format(intangible_assets / 1000000)for intangible_assets in Intangible_assets_annual]
                                        Intangible_assets_annual_df = pd.DataFrame(Intangible_assets_annual_table, index=date_list_annual,  columns=["Intangible Assets"])
                                        Intangible_assets_annual_df = Intangible_assets_annual_df.transpose()

                                        Net_goodwill_table= ["{:.2f}B".format(goodwill / 1000000000) if abs(goodwill) >= 1000000000 else "{:,.0f}M".format(goodwill / 1000000)for goodwill in Net_goodwill_annual]
                                        Net_goodwill_annual_df = pd.DataFrame(Net_goodwill_table, index=date_list_annual,  columns=["Goodwill"])
                                        Net_goodwill_annual_df = Net_goodwill_annual_df.transpose()

                                        Total_assets_annual_table= ["{:.2f}B".format(total_assets / 1000000000) if abs(total_assets) >= 1000000000 else "{:,.0f}M".format(total_assets / 1000000)for total_assets in Total_assets_annual]
                                        Total_assets_annual_df = pd.DataFrame(Total_assets_annual_table, index=date_list_annual,  columns=["Total Assets"])
                                        Total_assets_annual_df = Total_assets_annual_df.transpose()

                                        Short_term_debt_annual_table= ["{:.2f}B".format(st_debt / 1000000000) if abs(st_debt) >= 1000000000 else "{:,.0f}M".format(st_debt / 1000000)for st_debt in Short_term_debt_annual]
                                        Short_term_debt_annual_df = pd.DataFrame(Short_term_debt_annual_table, index=date_list_annual,  columns=["Short Term Debt"])
                                        Short_term_debt_annual_df = Short_term_debt_annual_df.transpose()

                                        LongTerm_debt_annual_table= ["{:.2f}B".format(lt_debt / 1000000000) if abs(lt_debt) >= 1000000000 else "{:,.0f}M".format(lt_debt / 1000000)for lt_debt in LongTerm_debt_annual]
                                        LongTerm_debt_annual_df = pd.DataFrame(LongTerm_debt_annual_table, index=date_list_annual,  columns=["Long-Term Debt"])
                                        LongTerm_debt_annual_df = LongTerm_debt_annual_df.transpose()

                                        Other_longterm_liabilities_annual_table= ["{:.2f}B".format(other_lt_liabilities / 1000000000) if abs(other_lt_liabilities) >= 1000000000 else "{:,.0f}M".format(other_lt_liabilities / 1000000)for other_lt_liabilities in Other_longterm_liabilities_annual]
                                        Other_longterm_liabilities_annual_df = pd.DataFrame(Other_longterm_liabilities_annual_table, index=date_list_annual,  columns=["Other Non-current Liabilities"])
                                        Other_longterm_liabilities_annual_df = Other_longterm_liabilities_annual_df.transpose()

                                        Total_liabilities_annual_table= ["{:.2f}B".format(total_liabilities / 1000000000) if abs(total_liabilities) >= 1000000000 else "{:,.0f}M".format(total_liabilities / 1000000)for total_liabilities in Total_liabilities_annual]
                                        Total_liabilities_annual_df = pd.DataFrame(Total_liabilities_annual_table, index=date_list_annual,  columns=["Total Liabilities"])
                                        Total_liabilities_annual_df = Total_liabilities_annual_df.transpose()

                                        Total_Equity_annual_table= ["{:.2f}B".format(total_equity / 1000000000) if abs(total_equity) >= 1000000000 else "{:,.0f}M".format(total_equity / 1000000)for total_equity in Total_Equity_annual]
                                        Total_Equity_annual_df = pd.DataFrame(Total_Equity_annual_table, index=date_list_annual,  columns=["Total Equity"])
                                        Total_Equity_annual_df = Total_Equity_annual_df.transpose()

                                        
                                        deposits_liability_annual_table= ["{:.2f}B".format(deposits_liability / 1000000000) if abs(deposits_liability) >= 1000000000 else "{:,.0f}M".format(deposits_liability / 1000000)for deposits_liability in Deposits_annual]
                                        deposits_liability_annual_df = pd.DataFrame(deposits_liability_annual_table, index=date_list_annual,  columns=["Deposits"])
                                        deposits_liability_df = deposits_liability_annual_df.transpose()

                                        Gross_loans_annual_table= ["{:.2f}B".format(loans_gross / 1000000000) if abs(loans_gross) >= 1000000000 else "{:,.0f}M".format(loans_gross / 1000000)for loans_gross in Gross_loans_annual]
                                        Gross_loans_annual_df = pd.DataFrame(Gross_loans_annual_table, index=date_list_annual,  columns=["Gross Loans"])
                                        Gross_loans_annual_df = Gross_loans_annual_df.transpose()

                                        Loans_loss_annual_table= ["{:.2f}B".format(allowance_for_loan_losses / 1000000000) if abs(allowance_for_loan_losses) >= 1000000000 else "{:,.0f}M".format(allowance_for_loan_losses / 1000000)for allowance_for_loan_losses in Loans_loss_annual]
                                        Loans_loss_annual_df = pd.DataFrame(Loans_loss_annual_table, index=date_list_annual,  columns=["Loan Losses"])
                                        Loans_loss_annual_df = Loans_loss_annual_df.transpose()

                                        Net_Loan_annual_table= ["{:.2f}B".format(loans_net / 1000000000) if abs(loans_net) >= 1000000000 else "{:,.0f}M".format(loans_net / 1000000)for loans_net in Net_Loan_annual]
                                        Net_Loan_annual_df = pd.DataFrame(Net_Loan_annual_table, index=date_list_annual,  columns=["Net Loans"])
                                        Net_Loan_annual_df = Net_Loan_annual_df.transpose()

                                   


                                        #........................................................................................quarterly....................


                                        #Total_current_assets_table_quarter= ["{:.2f}B".format(total_current_assets / 1000000000) if total_current_assets >= 1000000000 else "{:,.0f}M".format(total_current_assets / 1000000)for total_current_assets in Total_current_assets_quarter]
                                        #Total_current_assets_quarter_df = pd.DataFrame(Total_current_assets_table_quarter, index=date_list_quarter,  columns=["Total Current Assets"])
                                        #Total_current_assets_quarter_df = Total_current_assets_quarter_df.transpose()

                                        cash_und_cash_investments_quarter_table= ["{:.2f}B".format(cash_and_equiv / 1000000000) if abs(cash_and_equiv) >= 1000000000 else "{:,.0f}M".format(cash_and_equiv / 1000000)for cash_and_equiv in cash_and_equiv_quarterly_Balance_Sheet]
                                        cash_und_cash_investments_quarter_df = pd.DataFrame(cash_und_cash_investments_quarter_table, index=date_list_quarter,  columns=["Total Cash"])
                                        cash_und_cash_investments_quarter_df = cash_und_cash_investments_quarter_df.transpose()

                                        Intangible_assets_quarter_table= ["{:.2f}B".format(intangible_assets / 1000000000) if abs(intangible_assets) >= 1000000000 else "{:,.0f}M".format(intangible_assets / 1000000)for intangible_assets in Intangible_assets_quarter]
                                        Intangible_assets_quarter_df = pd.DataFrame(Intangible_assets_quarter_table, index=date_list_quarter,  columns=["Intangible Assets"])
                                        Intangible_assets_quarter_df = Intangible_assets_quarter_df.transpose()

                                        Net_goodwill_quarter_table= ["{:.2f}B".format(goodwill / 1000000000) if abs(goodwill) >= 1000000000 else "{:,.0f}M".format(goodwill / 1000000)for goodwill in Net_goodwill_quarter]
                                        Net_goodwill_quarter_df = pd.DataFrame(Net_goodwill_quarter_table, index=date_list_quarter,  columns=["Goodwill"])
                                        Net_goodwill_quarter_df = Net_goodwill_quarter_df.transpose()

                                        Total_assets_quarter_table= ["{:.2f}B".format(total_assets / 1000000000) if abs(total_assets) >= 1000000000 else "{:,.0f}M".format(total_assets / 1000000)for total_assets in Total_assets_quarter]
                                        Total_assets_quarter_df = pd.DataFrame(Total_assets_quarter_table, index=date_list_quarter,  columns=["Total Assets"])
                                        Total_assets_quarter_df = Total_assets_quarter_df.transpose()


                                        #Income_Tax_payable_quarter_table= ["{:.2f}B".format(tax_payable / 1000000000) if tax_payable >= 1000000000 else "{:,.0f}M".format(tax_payable / 1000000)for tax_payable in Income_Tax_payable_quarter]
                                        #Income_Tax_payable_quarter_df = pd.DataFrame(Income_Tax_payable_quarter_table, index=date_list_quarter,  columns=["Income Tax payable"])
                                        #Income_Tax_payable_quarter_df = Income_Tax_payable_quarter_df.transpose()

                                        #Total_current_liabilities_quarter_table= ["{:.2f}B".format(total_current_liabilities / 1000000000) if total_current_liabilities >= 1000000000 else "{:,.0f}M".format(total_current_liabilities / 1000000)for total_current_liabilities in Total_current_liabilities_quarter]
                                        #Total_current_liabilities_quarter_df = pd.DataFrame(Total_current_liabilities_quarter_table, index=date_list_quarter,  columns=["Total current liabilities"])
                                        #Total_current_liabilities_quarter_df = Total_current_liabilities_quarter_df.transpose()

                                        Short_term_debt_quarter_table= ["{:.2f}B".format(st_debt / 1000000000) if abs(st_debt) >= 1000000000 else "{:,.0f}M".format(st_debt / 1000000)for st_debt in Short_term_debt_quarter]
                                        Short_term_debt_quarter_df = pd.DataFrame(Short_term_debt_quarter_table, index=date_list_quarter,  columns=["Short Term Debt"])
                                        Short_term_debt_quarter_df = Short_term_debt_quarter_df.transpose()

                                        LongTerm_debt_quarter_table= ["{:.2f}B".format(lt_debt / 1000000000) if abs(lt_debt) >= 1000000000 else "{:,.0f}M".format(lt_debt / 1000000)for lt_debt in LongTerm_debt_quarter]
                                        LongTerm_debt_quarter_df = pd.DataFrame(LongTerm_debt_quarter_table, index=date_list_quarter,  columns=["Long-Term Debt"])
                                        LongTerm_debt_quarter_df = LongTerm_debt_quarter_df.transpose()

                                        Other_longterm_liabilities_quarter_table= ["{:.2f}B".format(other_lt_liabilities / 1000000000) if abs(other_lt_liabilities) >= 1000000000 else "{:,.0f}M".format(other_lt_liabilities / 1000000)for other_lt_liabilities in Other_longterm_liabilities_quarter]
                                        Other_longterm_liabilities_quarter_df = pd.DataFrame(Other_longterm_liabilities_quarter_table, index=date_list_quarter,  columns=["Other Non-current Liabilities"])
                                        Other_longterm_liabilities_quarter_df = Other_longterm_liabilities_quarter_df.transpose()

                                        Total_liabilities_quarter_table= ["{:.2f}B".format(total_liabilities / 1000000000) if abs(total_liabilities) >= 1000000000 else "{:,.0f}M".format(total_liabilities / 1000000)for total_liabilities in Total_liabilities_quarter]
                                        Total_liabilities_quarter_df = pd.DataFrame(Total_liabilities_quarter_table, index=date_list_quarter,  columns=["Total Liabilities"])
                                        Total_liabilities_quarter_df = Total_liabilities_quarter_df.transpose()

                                        Total_Equity_quarter_table= ["{:.2f}B".format(total_equity / 1000000000) if abs(total_equity) >= 1000000000 else "{:,.0f}M".format(total_equity / 1000000)for total_equity in Total_Equity_quarter]
                                        Total_Equity_quarter_df = pd.DataFrame(Total_Equity_quarter_table, index=date_list_quarter,  columns=["Total Equity"])
                                        Total_Equity_quarter_df = Total_Equity_quarter_df.transpose()

                                        deposits_liability_quarter_table= ["{:.2f}B".format(deposits_liability / 1000000000) if abs(deposits_liability) >= 1000000000 else "{:,.0f}M".format(deposits_liability / 1000000)for deposits_liability in Deposits_quarter]
                                        deposits_liability_quarter_df = pd.DataFrame(deposits_liability_quarter_table, index=date_list_quarter,  columns=["Deposits"])
                                        deposits_liability_quarter_df = deposits_liability_quarter_df.transpose()


                                        Gross_loans_quarter_table= ["{:.2f}B".format(loans_gross / 1000000000) if abs(loans_gross) >= 1000000000 else "{:,.0f}M".format(loans_gross / 1000000)for loans_gross in Gross_loans_quarter]
                                        Gross_loans_quarter_df = pd.DataFrame(Gross_loans_quarter_table, index=date_list_quarter,  columns=["Gross Loans"])
                                        Gross_loans_quarter_df = Gross_loans_quarter_df.transpose()

                                        Loans_loss_quarter_table= ["{:.2f}B".format(allowance_for_loan_losses / 1000000000) if abs(allowance_for_loan_losses) >= 1000000000 else "{:,.0f}M".format(allowance_for_loan_losses / 1000000)for allowance_for_loan_losses in Loans_loss_quarter]
                                        Loans_loss_quarter_df = pd.DataFrame(Loans_loss_quarter_table, index=date_list_quarter,  columns=["Loan Losses"])
                                        Loans_loss_quarter_df = Loans_loss_quarter_df.transpose()

                                        Net_Loan_quarter_table= ["{:.2f}B".format(loans_net / 1000000000) if abs(loans_net) >= 1000000000 else "{:,.0f}M".format(loans_net / 1000000)for loans_net in Net_Loan_quarter]
                                        Net_Loan_quarter_df = pd.DataFrame(Net_Loan_quarter_table, index=date_list_quarter,  columns=["Net Loans"])
                                        Net_Loan_quarter_df = Net_Loan_quarter_df.transpose()



                         
                                        merged_df_quarter = pd.concat([cash_und_cash_investments_quarter_df,Gross_loans_quarter_df,Loans_loss_quarter_df,Net_Loan_quarter_df,Intangible_assets_quarter_df,Net_goodwill_quarter_df,Total_assets_quarter_df,deposits_liability_quarter_df,Short_term_debt_quarter_df,LongTerm_debt_quarter_df,Other_longterm_liabilities_quarter_df,Total_liabilities_quarter_df,Total_Equity_quarter_df])           

                                       
                                        merged_df = pd.concat([cash_und_cash_investments_annual_df,Gross_loans_annual_df,Loans_loss_annual_df,Net_Loan_annual_df,Intangible_assets_annual_df,Net_goodwill_annual_df,Total_assets_annual_df,deposits_liability_df,Short_term_debt_annual_df,LongTerm_debt_annual_df,Other_longterm_liabilities_annual_df,Total_liabilities_annual_df,Total_Equity_annual_df])           
                                       
                                        st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))

                                        #st.dataframe(merged_df.style.set_table_attributes('class="scroll-table"'),use_container_width=True)
                         
                                        #st.markdown('<div style="margin-bottom: 100px;"></div>', unsafe_allow_html=True)

                                   #elif "Insurance" in Industry or "Health Care Providers & Services" in Industry or ticker=="BRK-A" or ticker=="BRK-B":
                                        pass
                                   except KeyError:
                                        cash_und_cash_investments = annual_data['cash_and_equiv'][-10:]
                                        #Total_current_assets_annual = annual_data['total_current_assets'][-10:]
                                        #Income_Tax_payable_annual = annual_data['tax_payable'][-10:]
                                        #Total_current_liabilities_annual = annual_data['total_current_liabilities'][-10:]
                                        #Total_current_assets_annual = annual_data['total_current_assets'][-10:]
                                        Intangible_assets_annual = annual_data['intangible_assets'][-10:]
                                        Net_goodwill_annual = annual_data['goodwill'][-10:]
                                        #Other_assets_annual = annual_data['other_assets'][-10:]
                                        Total_assets_annual = annual_data['total_assets'][-10:]
                                        Short_term_debt_annual = annual_data['st_debt'][-10:]
                                        #Income_Tax_payable_annual = annual_data['tax_payable'][-10:]
                                        #Total_current_liabilities_annual = annual_data['total_current_liabilities'][-10:]
                                        LongTerm_debt_annual = annual_data['lt_debt'][-10:]
                                        #Other_LongTerm_liabilites_annual = annual_data['other_lt_liabilities'][-10:]
                                        #Total_debt_annual = annual_data[''][-10:]
                                        Other_longterm_liabilities_annual = annual_data['other_lt_liabilities'][-10:]
                                        Total_liabilities_annual = annual_data['total_liabilities'][-10:]
                                        #Total_Sharehold_equity_annual = annual_data[''][-10:]
                                        Total_Equity_annual = annual_data['total_equity'][-10:]
                                        #Income_Tax_payable_annual = annual_data['tax_payable'][-10:]
                                        #Total_current_liabilities_annual = annual_data['total_current_liabilities'][-10:]
                                        #Liabili_shareholders_Equity_annual = annual_data[''][-10:]
                                        #Nopat_Annual = annual_data['nopat'][-10:]



     #...............................................................Quarterly........................................................
                                        cash_and_equiv_quarterly_Balance_Sheet = quarterly_data['cash_and_equiv'][-10:]
                                        #st_investments_quarterly_Balance_Sheet = quarterly_data['total_investments'][-10:]
                                        #Inventories_quarter = quarterly_data['inventories'][-10:]
                                        #Total_current_assets_quarter = quarterly_data['total_current_assets'][-10:]
                                        Intangible_assets_quarter= quarterly_data['intangible_assets'][-10:]
                                        Net_goodwill_quarter= quarterly_data['goodwill'][-10:]
                                        #Other_assets_quarter = quarterly_data['other_assets'][-10:]
                                        Total_assets_quarter = quarterly_data['total_assets'][-10:]
                                        #Accounts_payable_quarter = quarterly_data['accounts_payable'][-10:]
                                        #Current_accrued_liab_quarter = quarterly_data['current_accrued_liabilities'][-10:]
                                        #Tax_payable_quarter = quarterly_data['tax_payable'][-10:]
                                        #Other_current_liabilities_quarter = quarterly_data['other_current_liabilities'][-10:]
                                        #Current_deferred_revenue_quarter = quarterly_data['current_deferred_revenue'][-10:]
                                        #Total_current_liabilities_quarter = quarterly_data['total_current_liabilities'][-10:] 
                                        Short_term_debt_quarter = quarterly_data['st_debt'][-10:]
                                        #current_portion_of_lease_obligation = quarterly_data['current_capital_leases'][-10:]
                                        #capital_leases = quarterly_data['noncurrent_capital_leases'][-10:]
                                        LongTerm_debt_quarter = quarterly_data['lt_debt'][-10:]
                                        #Total_debt_quarter = quarterly_data[''][-10:]
                                        Other_longterm_liabilities_quarter = quarterly_data['other_lt_liabilities'][-10:]
                                        Total_liabilities_quarter = quarterly_data['total_liabilities'][-10:]
                                        #Total_Sharehold_equity_quarter = quarterly_data[''][-10:]
                                        Total_Equity_quarter = quarterly_data['total_equity'][-10:]

                                        cash_und_cash_investments_annual= ["{:.2f}B".format(cash_and_equiv / 1000000000) if abs(cash_and_equiv) >= 1000000000 else "{:,.0f}M".format(cash_and_equiv / 1000000)for cash_and_equiv in cash_und_cash_investments]
                                        cash_und_cash_investments_annual_df = pd.DataFrame(cash_und_cash_investments_annual, index=date_list_annual,  columns=["Total Cash"])
                                        cash_und_cash_investments_annual_df = cash_und_cash_investments_annual_df.transpose()

                                        Intangible_assets_annual_table= ["{:.2f}B".format(intangible_assets / 1000000000) if abs(intangible_assets) >= 1000000000 else "{:,.0f}M".format(intangible_assets / 1000000)for intangible_assets in Intangible_assets_annual]
                                        Intangible_assets_annual_df = pd.DataFrame(Intangible_assets_annual_table, index=date_list_annual,  columns=["Intangible Assets"])
                                        Intangible_assets_annual_df = Intangible_assets_annual_df.transpose()

                                        Net_goodwill_table= ["{:.2f}B".format(goodwill / 1000000000) if abs(goodwill) >= 1000000000 else "{:,.0f}M".format(goodwill / 1000000)for goodwill in Net_goodwill_annual]
                                        Net_goodwill_annual_df = pd.DataFrame(Net_goodwill_table, index=date_list_annual,  columns=["Goodwill"])
                                        Net_goodwill_annual_df = Net_goodwill_annual_df.transpose()

                                        Total_assets_annual_table= ["{:.2f}B".format(total_assets / 1000000000) if abs(total_assets) >= 1000000000 else "{:,.0f}M".format(total_assets / 1000000)for total_assets in Total_assets_annual]
                                        Total_assets_annual_df = pd.DataFrame(Total_assets_annual_table, index=date_list_annual,  columns=["Total Assets"])
                                        Total_assets_annual_df = Total_assets_annual_df.transpose()

                                        Short_term_debt_annual_table= ["{:.2f}B".format(st_debt / 1000000000) if abs(st_debt) >= 1000000000 else "{:,.0f}M".format(st_debt / 1000000)for st_debt in Short_term_debt_annual]
                                        Short_term_debt_annual_df = pd.DataFrame(Short_term_debt_annual_table, index=date_list_annual,  columns=["Short Term Debt"])
                                        Short_term_debt_annual_df = Short_term_debt_annual_df.transpose()

                                        LongTerm_debt_annual_table= ["{:.2f}B".format(lt_debt / 1000000000) if abs(lt_debt) >= 1000000000 else "{:,.0f}M".format(lt_debt / 1000000)for lt_debt in LongTerm_debt_annual]
                                        LongTerm_debt_annual_df = pd.DataFrame(LongTerm_debt_annual_table, index=date_list_annual,  columns=["Long-Term Debt"])
                                        LongTerm_debt_annual_df = LongTerm_debt_annual_df.transpose()

                                        Other_longterm_liabilities_annual_table= ["{:.2f}B".format(other_lt_liabilities / 1000000000) if abs(other_lt_liabilities) >= 1000000000 else "{:,.0f}M".format(other_lt_liabilities / 1000000)for other_lt_liabilities in Other_longterm_liabilities_annual]
                                        Other_longterm_liabilities_annual_df = pd.DataFrame(Other_longterm_liabilities_annual_table, index=date_list_annual,  columns=["Other Non-current Liabilities"])
                                        Other_longterm_liabilities_annual_df = Other_longterm_liabilities_annual_df.transpose()

                                        Total_liabilities_annual_table= ["{:.2f}B".format(total_liabilities / 1000000000) if abs(total_liabilities) >= 1000000000 else "{:,.0f}M".format(total_liabilities / 1000000)for total_liabilities in Total_liabilities_annual]
                                        Total_liabilities_annual_df = pd.DataFrame(Total_liabilities_annual_table, index=date_list_annual,  columns=["Total Liabilities"])
                                        Total_liabilities_annual_df = Total_liabilities_annual_df.transpose()

                                        Total_Equity_annual_table= ["{:.2f}B".format(total_equity / 1000000000) if abs(total_equity) >= 1000000000 else "{:,.0f}M".format(total_equity / 1000000)for total_equity in Total_Equity_annual]
                                        Total_Equity_annual_df = pd.DataFrame(Total_Equity_annual_table, index=date_list_annual,  columns=["Total Equity"])
                                        Total_Equity_annual_df = Total_Equity_annual_df.transpose()

     #--------------------------------------------------------------------------Quarter-----------------------------

                                        cash_und_cash_investments_quarter_table= ["{:.2f}B".format(cash_and_equiv / 1000000000) if abs(cash_and_equiv) >= 1000000000 else "{:,.0f}M".format(cash_and_equiv / 1000000)for cash_and_equiv in cash_and_equiv_quarterly_Balance_Sheet]
                                        cash_und_cash_investments_quarter_df = pd.DataFrame(cash_und_cash_investments_quarter_table, index=date_list_quarter,  columns=["Total Cash"])
                                        cash_und_cash_investments_quarter_df = cash_und_cash_investments_quarter_df.transpose()

                                        Intangible_assets_quarter_table= ["{:.2f}B".format(intangible_assets / 1000000000) if abs(intangible_assets) >= 1000000000 else "{:,.0f}M".format(intangible_assets / 1000000)for intangible_assets in Intangible_assets_quarter]
                                        Intangible_assets_quarter_df = pd.DataFrame(Intangible_assets_quarter_table, index=date_list_quarter,  columns=["Intangible Assets"])
                                        Intangible_assets_quarter_df = Intangible_assets_quarter_df.transpose()

                                        Net_goodwill_quarter_table= ["{:.2f}B".format(goodwill / 1000000000) if abs(goodwill) >= 1000000000 else "{:,.0f}M".format(goodwill / 1000000)for goodwill in Net_goodwill_quarter]
                                        Net_goodwill_quarter_df = pd.DataFrame(Net_goodwill_quarter_table, index=date_list_quarter,  columns=["Goodwill"])
                                        Net_goodwill_quarter_df = Net_goodwill_quarter_df.transpose()

                                        Total_assets_quarter_table= ["{:.2f}B".format(total_assets / 1000000000) if abs(total_assets) >= 1000000000 else "{:,.0f}M".format(total_assets / 1000000)for total_assets in Total_assets_quarter]
                                        Total_assets_quarter_df = pd.DataFrame(Total_assets_quarter_table, index=date_list_quarter,  columns=["Total Assets"])
                                        Total_assets_quarter_df = Total_assets_quarter_df.transpose()


                                        #Income_Tax_payable_quarter_table= ["{:.2f}B".format(tax_payable / 1000000000) if tax_payable >= 1000000000 else "{:,.0f}M".format(tax_payable / 1000000)for tax_payable in Income_Tax_payable_quarter]
                                        #Income_Tax_payable_quarter_df = pd.DataFrame(Income_Tax_payable_quarter_table, index=date_list_quarter,  columns=["Income Tax payable"])
                                        #Income_Tax_payable_quarter_df = Income_Tax_payable_quarter_df.transpose()

                                        #Total_current_liabilities_quarter_table= ["{:.2f}B".format(total_current_liabilities / 1000000000) if total_current_liabilities >= 1000000000 else "{:,.0f}M".format(total_current_liabilities / 1000000)for total_current_liabilities in Total_current_liabilities_quarter]
                                        #Total_current_liabilities_quarter_df = pd.DataFrame(Total_current_liabilities_quarter_table, index=date_list_quarter,  columns=["Total current liabilities"])
                                        #Total_current_liabilities_quarter_df = Total_current_liabilities_quarter_df.transpose()

                                        Short_term_debt_quarter_table= ["{:.2f}B".format(st_debt / 1000000000) if abs(st_debt) >= 1000000000 else "{:,.0f}M".format(st_debt / 1000000)for st_debt in Short_term_debt_quarter]
                                        Short_term_debt_quarter_df = pd.DataFrame(Short_term_debt_quarter_table, index=date_list_quarter,  columns=["Short Term Debt"])
                                        Short_term_debt_quarter_df = Short_term_debt_quarter_df.transpose()

                                        LongTerm_debt_quarter_table= ["{:.2f}B".format(lt_debt / 1000000000) if abs(lt_debt) >= 1000000000 else "{:,.0f}M".format(lt_debt / 1000000)for lt_debt in LongTerm_debt_quarter]
                                        LongTerm_debt_quarter_df = pd.DataFrame(LongTerm_debt_quarter_table, index=date_list_quarter,  columns=["Long-Term Debt"])
                                        LongTerm_debt_quarter_df = LongTerm_debt_quarter_df.transpose()

                                        Other_longterm_liabilities_quarter_table= ["{:.2f}B".format(other_lt_liabilities / 1000000000) if abs(other_lt_liabilities) >= 1000000000 else "{:,.0f}M".format(other_lt_liabilities / 1000000)for other_lt_liabilities in Other_longterm_liabilities_quarter]
                                        Other_longterm_liabilities_quarter_df = pd.DataFrame(Other_longterm_liabilities_quarter_table, index=date_list_quarter,  columns=["Other Non-current Liabilities"])
                                        Other_longterm_liabilities_quarter_df = Other_longterm_liabilities_quarter_df.transpose()

                                        Total_liabilities_quarter_table= ["{:.2f}B".format(total_liabilities / 1000000000) if abs(total_liabilities) >= 1000000000 else "{:,.0f}M".format(total_liabilities / 1000000)for total_liabilities in Total_liabilities_quarter]
                                        Total_liabilities_quarter_df = pd.DataFrame(Total_liabilities_quarter_table, index=date_list_quarter,  columns=["Total Liabilities"])
                                        Total_liabilities_quarter_df = Total_liabilities_quarter_df.transpose()

                                        Total_Equity_quarter_table= ["{:.2f}B".format(total_equity / 1000000000) if abs(total_equity) >= 1000000000 else "{:,.0f}M".format(total_equity / 1000000)for total_equity in Total_Equity_quarter]
                                        Total_Equity_quarter_df = pd.DataFrame(Total_Equity_quarter_table, index=date_list_quarter,  columns=["Total Equity"])
                                        Total_Equity_quarter_df = Total_Equity_quarter_df.transpose()



                         
                                        merged_df_quarter = pd.concat([cash_und_cash_investments_quarter_df,Intangible_assets_quarter_df,Net_goodwill_quarter_df,Total_assets_quarter_df,Short_term_debt_quarter_df,LongTerm_debt_quarter_df,Other_longterm_liabilities_quarter_df,Total_liabilities_quarter_df,Total_Equity_quarter_df])           


                                   

                                        merged_df = pd.concat([cash_und_cash_investments_annual_df,Intangible_assets_annual_df,Net_goodwill_annual_df,Total_assets_annual_df,Short_term_debt_annual_df,LongTerm_debt_annual_df,Other_longterm_liabilities_annual_df,Total_liabilities_annual_df,Total_Equity_annual_df])           
                                                                           
                                                                           
                                        
                                        st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))

                                        #st.dataframe(merged_df.style.set_table_attributes('class="scroll-table"'),use_container_width=True)
                                       
                                        #st.markdown('<div style="margin-bottom: 100px;"></div>', unsafe_allow_html=True)
                                        pass    
                                   #else:      
                                   try:    
                                        cash_und_cash_investments_annual = annual_data['cash_and_equiv'][-10:]
                                   #st_investments_annual = annual_data['st_investments'][-10:]
                                        st_investments_annual = annual_data['st_investments'][-10:]
                                        Inventories_annual = annual_data['inventories'][-10:]
                                        Total_current_assets_annual = annual_data['total_current_assets'][-10:]
                                        Income_Tax_payable_annual = annual_data['tax_payable'][-10:]
                                        Total_current_liabilities_annual = annual_data['total_current_liabilities'][-10:]
                                        #Nopat_Annual = annual_data['nopat'][-10:]
                                        #Inventories_annual = annual_data['inventories'][-10:]
                                        #Total_current_assets_annual = annual_data['total_current_assets'][-10:]
                                        Intangible_assets_annual = annual_data['intangible_assets'][-10:]
                                        Net_goodwill_annual = annual_data['goodwill'][-10:]
                                        #Other_assets_annual = annual_data['other_assets'][-10:]
                                        Total_assets_annual = annual_data['total_assets'][-10:]
                                        Short_term_debt_annual = annual_data['st_debt'][-10:]
                                        #Income_Tax_payable_annual = annual_data['tax_payable'][-10:]
                                        #Total_current_liabilities_annual = annual_data['total_current_liabilities'][-10:]
                                        LongTerm_debt_annual = annual_data['lt_debt'][-10:]
                                        #Other_LongTerm_liabilites_annual = annual_data['other_lt_liabilities'][-10:]
                                        #Total_debt_annual = annual_data[''][-10:]
                                        Other_longterm_liabilities_annual = annual_data['other_lt_liabilities'][-10:]
                                        Total_liabilities_annual = annual_data['total_liabilities'][-10:]
                                        #Total_Sharehold_equity_annual = annual_data[''][-10:]
                                        Total_Equity_annual = annual_data['total_equity'][-10:]
                                        #Liabili_shareholders_Equity_annual = annual_data[''][-10:]
                                        #Nopat_Annual = annual_data['nopat'][-10:]

                                   # Create a DataFrame
                                        index = range(len(period_end_dates))
                                        df = pd.DataFrame({'Period End Date': period_end_dates,
                                                       'Cash and Equivalents': cash_und_cash_investments_annual,
                                                       'Short term Investments': st_investments_annual
                                                       }, index=index)

                                        # Add the columns together
                                        #df['Total Cash'] = df['cash_and_equiv'] + df['st_investments']
                                        if 'Short term Investments' in df.columns:
                                                  df['Total Cash'] = df['Cash and Equivalents'] + df['Short term Investments']
                                        else:
                                                  df['Total Cash'] = df['Cash and Equivalents']
                                             # Transpose the DataFrame
                                             #total = df.T
                                        # Transpose the DataFrame
                                        total = df.T

                                   # Replace the numbering with the actual date
                                        total.columns = total.iloc[0]  # Use the first row as column names
                                        total = total[1:]  # Remove the first row

                                        # Convert the numbers to billions and display with 2 decimal places
                                        #total = (total / 1e9).round(2)
                                        
                                        #total = "{:.2f}B".format((total/1000000000))
                                        #total_annual = total.applymap(lambda x: "{:.2f}B".format(x / 1e9))
                                        total_annual = total.applymap(lambda x: "{:.2f}B".format(x / 1e9) if abs(x) >= 1e9 else "{:,.0f}M".format(x / 1e6))

                                        
                                        #------------------------------------------------------------------
                                        Inventories_annual_table= ["{:.2f}B".format(inventories / 1000000000) if abs(inventories) >= 1000000000 else "{:,.0f}M".format(inventories / 1000000)for inventories in Inventories_annual]
                                        Inventories_annual_df = pd.DataFrame(Inventories_annual_table, index=date_list_annual,  columns=["Inventory"])
                                        Inventories_annual_df = Inventories_annual_df.transpose()

                                        Total_current_assets_table= ["{:.2f}B".format(total_current_assets / 1000000000) if abs(total_current_assets) >= 1000000000 else "{:,.0f}M".format(total_current_assets / 1000000)for total_current_assets in Total_current_assets_annual]
                                        Total_current_assets_df = pd.DataFrame(Total_current_assets_table, index=date_list_annual,  columns=["Total Current Assets"])
                                        Total_current_assets_df = Total_current_assets_df.transpose()

                                        Intangible_assets_annual_table= ["{:.2f}B".format(intangible_assets / 1000000000) if abs(intangible_assets) >= 1000000000 else "{:,.0f}M".format(intangible_assets / 1000000)for intangible_assets in Intangible_assets_annual]
                                        Intangible_assets_annual_df = pd.DataFrame(Intangible_assets_annual_table, index=date_list_annual,  columns=["Intangible Assets"])
                                        Intangible_assets_annual_df = Intangible_assets_annual_df.transpose()

                                        Net_goodwill_table= ["{:.2f}B".format(goodwill / 1000000000) if abs(goodwill) >= 1000000000 else "{:,.0f}M".format(goodwill / 1000000)for goodwill in Net_goodwill_annual]
                                        Net_goodwill_annual_df = pd.DataFrame(Net_goodwill_table, index=date_list_annual,  columns=["Goodwill"])
                                        Net_goodwill_annual_df = Net_goodwill_annual_df.transpose()

                                        Total_assets_annual_table= ["{:.2f}B".format(total_assets / 1000000000) if abs(total_assets) >= 1000000000 else "{:,.0f}M".format(total_assets / 1000000)for total_assets in Total_assets_annual]
                                        Total_assets_annual_df = pd.DataFrame(Total_assets_annual_table, index=date_list_annual,  columns=["Total Assets"])
                                        Total_assets_annual_df = Total_assets_annual_df.transpose()

                                        Short_term_debt_annual_table= ["{:.2f}B".format(st_debt / 1000000000) if abs(st_debt) >= 1000000000 else "{:,.0f}M".format(st_debt / 1000000)for st_debt in Short_term_debt_annual]
                                        Short_term_debt_annual_df = pd.DataFrame(Short_term_debt_annual_table, index=date_list_annual,  columns=["Short Term Debt"])
                                        Short_term_debt_annual_df = Short_term_debt_annual_df.transpose()

                                        Income_Tax_payable_annual_table= ["{:.2f}B".format(tax_payable / 1000000000) if abs(tax_payable) >= 1000000000 else "{:,.0f}M".format(tax_payable / 1000000)for tax_payable in Income_Tax_payable_annual]
                                        Income_Tax_payable_annual_df = pd.DataFrame(Income_Tax_payable_annual_table, index=date_list_annual,  columns=["Income Tax payable"])
                                        Income_Tax_payable_annual_df = Income_Tax_payable_annual_df.transpose()

                                        Total_current_liabilities_annual_table= ["{:.2f}B".format(total_current_liabilities / 1000000000) if abs(total_current_liabilities) >= 1000000000 else "{:,.0f}M".format(total_current_liabilities / 1000000)for total_current_liabilities in Total_current_liabilities_annual]
                                        Total_current_liabilities_annual_df = pd.DataFrame(Total_current_liabilities_annual_table, index=date_list_annual,  columns=["Total current liabilities"])
                                        Total_current_liabilities_annual_df = Total_current_liabilities_annual_df.transpose()

                                        LongTerm_debt_annual_table= ["{:.2f}B".format(lt_debt / 1000000000) if abs(lt_debt) >= 1000000000 else "{:,.0f}M".format(lt_debt / 1000000)for lt_debt in LongTerm_debt_annual]
                                        LongTerm_debt_annual_df = pd.DataFrame(LongTerm_debt_annual_table, index=date_list_annual,  columns=["Long-Term Debt"])
                                        LongTerm_debt_annual_df = LongTerm_debt_annual_df.transpose()

                                        Other_longterm_liabilities_annual_table= ["{:.2f}B".format(other_lt_liabilities / 1000000000) if abs(other_lt_liabilities) >= 1000000000 else "{:,.0f}M".format(other_lt_liabilities / 1000000)for other_lt_liabilities in Other_longterm_liabilities_annual]
                                        Other_longterm_liabilities_annual_df = pd.DataFrame(Other_longterm_liabilities_annual_table, index=date_list_annual,  columns=["Other Non-current Liabilities"])
                                        Other_longterm_liabilities_annual_df = Other_longterm_liabilities_annual_df.transpose()

                                        Total_liabilities_annual_table= ["{:.2f}B".format(total_liabilities / 1000000000) if abs(total_liabilities) >= 1000000000 else "{:,.0f}M".format(total_liabilities / 1000000)for total_liabilities in Total_liabilities_annual]
                                        Total_liabilities_annual_df = pd.DataFrame(Total_liabilities_annual_table, index=date_list_annual,  columns=["Total Liabilities"])
                                        Total_liabilities_annual_df = Total_liabilities_annual_df.transpose()

                                        Total_Equity_annual_table= ["{:.2f}B".format(total_equity / 1000000000) if abs(total_equity) >= 1000000000 else "{:,.0f}M".format(total_equity / 1000000)for total_equity in Total_Equity_annual]
                                        Total_Equity_annual_df = pd.DataFrame(Total_Equity_annual_table, index=date_list_annual,  columns=["Total Equity"])
                                        Total_Equity_annual_df = Total_Equity_annual_df.transpose()



                                        #Nopat_Annual_table= ["{:.2f}B".format(nopat / 1000000000)for nopat in Nopat_Annual]
                                        #Nopat_Annual_df = pd.DataFrame(Nopat_Annual_table, index=date_list_annual,  columns=["Nopat"])
                                        #Nopat_Annual_df = Nopat_Annual_df.transpose()

                                        



                                        #.............................................quarterly..................................................................................
                                        date_quarterly_Balance_Sheet = quarterly_data['period_end_date'][-10:] 


                                        cash_and_equiv_quarterly_Balance_Sheet = quarterly_data['cash_and_equiv'][-10:]
                                        st_investments_quarterly_Balance_Sheet = quarterly_data['st_investments'][-10:]
                                        Inventories_quarter = quarterly_data['inventories'][-10:]
                                   
                                        Total_current_assets_quarter = quarterly_data['total_current_assets'][-10:]
                                        Intangible_assets_quarter= quarterly_data['intangible_assets'][-10:]
                                        Net_goodwill_quarter= quarterly_data['goodwill'][-10:]
                                        #Other_assets_quarter = quarterly_data['other_assets'][-10:]
                                        Total_assets_quarter = quarterly_data['total_assets'][-10:]
                                        st_investments_quarterly_Balance_Sheet = quarterly_data['st_investments'][-10:]
                                        Accounts_payable_quarter = quarterly_data['accounts_payable'][-10:]
                                        Current_accrued_liab_quarter = quarterly_data['current_accrued_liabilities'][-10:]
                                        Tax_payable_quarter = quarterly_data['tax_payable'][-10:]
                                        Other_current_liabilities_quarter = quarterly_data['other_current_liabilities'][-10:]
                                        Current_deferred_revenue_quarter = quarterly_data['current_deferred_revenue'][-10:]
                                        Total_current_liabilities_quarter = quarterly_data['total_current_liabilities'][-10:] 
                                        Short_term_debt_quarter = quarterly_data['st_debt'][-10:]
                                        current_portion_of_lease_obligation = quarterly_data['current_capital_leases'][-10:]
                                        capital_leases = quarterly_data['noncurrent_capital_leases'][-10:]
                                        LongTerm_debt_quarter = quarterly_data['lt_debt'][-10:]
                                        #Total_debt_quarter = quarterly_data[''][-10:]
                                        Other_longterm_liabilities_quarter = quarterly_data['other_lt_liabilities'][-10:]
                                        Total_liabilities_quarter = quarterly_data['total_liabilities'][-10:]
                                        #Total_Sharehold_equity_quarter = quarterly_data[''][-10:]
                                        Total_Equity_quarter = quarterly_data['total_equity'][-10:]
                                             #Liabili_shareholders_Equity_quarter = quarterly_data[''][-10:]
                                             #Nopat_quarter= quarterly_data['nopat'][-10:]
                                   #-----------------------------------------------------------
                                        index = range(len(date_list_quarter))
                                        df = pd.DataFrame({'Period End Date': date_list_quarter,
                                                       'Cash and Equivalents': cash_and_equiv_quarterly_Balance_Sheet,
                                                       'Short term Investments': st_investments_quarterly_Balance_Sheet
                                                       }, index=index)


                                        # Add the columns together
                                        #df['Total Cash'] = df['cash_and_equiv'] + df['st_investments']
                                   # Check if 'st_investments_quarterly_Balance_Sheet' column exists in the DataFrame
                                        if 'Short term Investments' in df.columns:
                                             df['Total Cash'] = df['Cash and Equivalents'] + df['Short term Investments']
                                        else:
                                             df['Total Cash'] = df['Cash and Equivalents']
                                        # Transpose the DataFrame
                                        total = df.T
                                        

                                   # Replace the numbering with the actual date
                                        total.columns = total.iloc[0]  # Use the first row as column names
                                        total = total[1:]  # Remove the first row

                                        # Convert the numbers to billions and display with 2 decimal places
                                        #total = (total / 1e9).round(2)
                                        #total = total.applymap(lambda x: "{:.2f}B".format(x / 1e9))
                                        total = total.applymap(lambda x: "{:.2f}B".format(x / 1e9) if abs(x) >= 1e9 else "{:,.0f}M".format(x / 1e6))


                                        Inventories_quarter_table= ["{:.2f}B".format(inventories / 1000000000) if abs(inventories) >= 1000000000 else "{:,.0f}M".format(inventories / 1000000)for inventories in Inventories_quarter]
                                        #["{:.2f}B".format(inventories / 1000000000)for inventories in Inventories_quarter]
                                        Inventories_quarter_df = pd.DataFrame(Inventories_quarter_table, index=date_list_quarter,  columns=["Inventory"])
                                        Inventories_quarter_df = Inventories_quarter_df.transpose()

                                        Total_current_assets_table_quarter= ["{:.2f}B".format(total_current_assets / 1000000000) if abs(total_current_assets) >= 1000000000 else "{:,.0f}M".format(total_current_assets / 1000000)for total_current_assets in Total_current_assets_quarter]
                                        Total_current_assets_quarter_df = pd.DataFrame(Total_current_assets_table_quarter, index=date_list_quarter,  columns=["Total Current Assets"])
                                        Total_current_assets_quarter_df = Total_current_assets_quarter_df.transpose()

                                        Intangible_assets_quarter_table= ["{:.2f}B".format(intangible_assets / 1000000000) if abs(intangible_assets) >= 1000000000 else "{:,.0f}M".format(intangible_assets / 1000000)for intangible_assets in Intangible_assets_quarter]
                                        Intangible_assets_quarter_df = pd.DataFrame(Intangible_assets_quarter_table, index=date_list_quarter,  columns=["Intangible Assets"])
                                        Intangible_assets_quarter_df = Intangible_assets_quarter_df.transpose()

                                        Net_goodwill_quarter_table= ["{:.2f}B".format(goodwill / 1000000000) if abs(goodwill) >= 1000000000 else "{:,.0f}M".format(goodwill / 1000000)for goodwill in Net_goodwill_quarter]
                                        Net_goodwill_quarter_df = pd.DataFrame(Net_goodwill_quarter_table, index=date_list_quarter,  columns=["Goodwill"])
                                        Net_goodwill_quarter_df = Net_goodwill_quarter_df.transpose()

                                        Total_assets_quarter_table= ["{:.2f}B".format(total_assets / 1000000000) if abs(total_assets) >= 1000000000 else "{:,.0f}M".format(total_assets / 1000000)for total_assets in Total_assets_quarter]
                                        Total_assets_quarter_df = pd.DataFrame(Total_assets_quarter_table, index=date_list_quarter,  columns=["Total Assets"])
                                        Total_assets_quarter_df = Total_assets_quarter_df.transpose()


                                        #Income_Tax_payable_quarter_table= ["{:.2f}B".format(tax_payable / 1000000000) if tax_payable >= 1000000000 else "{:,.0f}M".format(tax_payable / 1000000)for tax_payable in Income_Tax_payable_quarter]
                                        #Income_Tax_payable_quarter_df = pd.DataFrame(Income_Tax_payable_quarter_table, index=date_list_quarter,  columns=["Income Tax payable"])
                                        #Income_Tax_payable_quarter_df = Income_Tax_payable_quarter_df.transpose()

                                        Total_current_liabilities_quarter_table= ["{:.2f}B".format(total_current_liabilities / 1000000000) if abs(total_current_liabilities) >= 1000000000 else "{:,.0f}M".format(total_current_liabilities / 1000000)for total_current_liabilities in Total_current_liabilities_quarter]
                                        Total_current_liabilities_quarter_df = pd.DataFrame(Total_current_liabilities_quarter_table, index=date_list_quarter,  columns=["Total current liabilities"])
                                        Total_current_liabilities_quarter_df = Total_current_liabilities_quarter_df.transpose()

                                        Short_term_debt_quarter_table= ["{:.2f}B".format(st_debt / 1000000000) if abs(st_debt) >= 1000000000 else "{:,.0f}M".format(st_debt / 1000000)for st_debt in Short_term_debt_quarter]
                                        Short_term_debt_quarter_df = pd.DataFrame(Short_term_debt_quarter_table, index=date_list_quarter,  columns=["Short Term Debt"])
                                        Short_term_debt_quarter_df = Short_term_debt_quarter_df.transpose()

                                        LongTerm_debt_quarter_table= ["{:.2f}B".format(lt_debt / 1000000000) if abs(lt_debt) >= 1000000000 else "{:,.0f}M".format(lt_debt / 1000000)for lt_debt in LongTerm_debt_quarter]
                                        LongTerm_debt_quarter_df = pd.DataFrame(LongTerm_debt_quarter_table, index=date_list_quarter,  columns=["Long-Term Debt"])
                                        LongTerm_debt_quarter_df = LongTerm_debt_quarter_df.transpose()

                                        Other_longterm_liabilities_quarter_table= ["{:.2f}B".format(other_lt_liabilities / 1000000000) if abs(other_lt_liabilities) >= 1000000000 else "{:,.0f}M".format(other_lt_liabilities / 1000000)for other_lt_liabilities in Other_longterm_liabilities_quarter]
                                        Other_longterm_liabilities_quarter_df = pd.DataFrame(Other_longterm_liabilities_quarter_table, index=date_list_quarter,  columns=["Other Non-current Liabilities"])
                                        Other_longterm_liabilities_quarter_df = Other_longterm_liabilities_quarter_df.transpose()

                                        Total_liabilities_quarter_table= ["{:.2f}B".format(total_liabilities / 1000000000) if abs(total_liabilities) >= 1000000000 else "{:,.0f}M".format(total_liabilities / 1000000)for total_liabilities in Total_liabilities_quarter]
                                        Total_liabilities_quarter_df = pd.DataFrame(Total_liabilities_quarter_table, index=date_list_quarter,  columns=["Total Liabilities"])
                                        Total_liabilities_quarter_df = Total_liabilities_quarter_df.transpose()

                                        Total_Equity_quarter_table= ["{:.2f}B".format(total_equity / 1000000000) if abs(total_equity) >= 1000000000 else "{:,.0f}M".format(total_equity / 1000000)for total_equity in Total_Equity_quarter]
                                        Total_Equity_quarter_df = pd.DataFrame(Total_Equity_quarter_table, index=date_list_quarter,  columns=["Total Equity"])
                                        Total_Equity_quarter_df = Total_Equity_quarter_df.transpose()


                                        merged_df =pd.concat([total_annual,Inventories_annual_df,Total_current_assets_df,Intangible_assets_annual_df,Net_goodwill_annual_df,Total_assets_annual_df,Short_term_debt_annual_df,Total_current_liabilities_annual_df,LongTerm_debt_annual_df,Other_longterm_liabilities_annual_df,Total_liabilities_annual_df,Total_Equity_annual_df])           
                                        merged_df_quarter = pd.concat([total,Inventories_quarter_df,Total_current_assets_quarter_df,Intangible_assets_quarter_df,Net_goodwill_quarter_df,Total_assets_quarter_df,Short_term_debt_quarter_df,Total_current_liabilities_quarter_df,LongTerm_debt_quarter_df,Other_longterm_liabilities_quarter_df,Total_liabilities_quarter_df,Total_Equity_quarter_df])           
                                        
                                        
                                        st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))

                                        #st.dataframe(merged_df.style.set_table_attributes('class="scroll-table"'),use_container_width=True)
                                      
                                       # st.markdown('<div style="margin-bottom: 100px;"></div>', unsafe_allow_html=True)
                                        pass



                                   except KeyError:
                                   
                                        st.write()

                                        pass





                                   with Quarterly:

                                        st.table(merged_df_quarter.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))

                                        #st.dataframe(merged_df_quarter.style.set_table_attributes('class="scroll-table"'),use_container_width=True)
                                       
                                       # st.markdown('<div style="margin-bottom: 100px;"></div>', unsafe_allow_html=True)
                                        
                                   

     #................................................................................................................................................

                                        

     #...........................................................................
                                        with Income_Statement:
                                        #with Balance_Sheet: 
                                             Annual,Quarterly = st.tabs(["Annual","Quarterly"])

                                             with Quarterly:
                                                  #if "Consumer Finance" in Industry or "Banks" in Industry or ticker == "MAIN":
                                                  try:               
                                                       revenue_2013_quarterly = quarterly_data['revenue'][-10:] 
                                                       Pretax_income_quarterly = quarterly_data['pretax_income'][-10:]
                                                       eps_basic_quarterly= quarterly_data['eps_basic'][-10:]
                                                       shares_basic_quarterly = quarterly_data['shares_basic'][-10:]
                                                       eps_diluted_quarterly = quarterly_data['eps_diluted'][-10:]
                                                       shares_diluted_quarterly = quarterly_data['shares_diluted'][-10:]
                                                       Income_tax_quarterly = quarterly_data['income_tax'][-10:]
                                                       net_income_quarterly = quarterly_data['net_income'][-10:]
                                                       Total_interest_income_list_quarterly = quarterly_data['total_interest_income'][-10:]
                                                       Total_interest_expense_list_quarterly = quarterly_data['total_interest_expense'][-10:]
                                                       Net_interest_Income_quarterly = quarterly_data['net_interest_income'][-10:]
                                                       Prov_Credit_losses_quarterly = quarterly_data['credit_losses_provision'][-10:]
                                                       Netinterest_Prov_Credit_losses_quarterly = quarterly_data['net_interest_income_after_credit_losses_provision'][-10:]
                                                       Total_Non_interest_expenses_quarterly = quarterly_data['total_noninterest_expense'][-10:]
                                                       Total_Non_interest_revenue_quarterly = quarterly_data['total_noninterest_revenue'][-10:]
                                                  #....................................................................................................
                                                       revenue_quarterly_list_billion = ["{:.2f}B".format(revenue / 1000000000) if abs(revenue)>= 1000000000 else "{:,.0f}M".format(revenue / 1000000) for revenue in revenue_2013_quarterly]
                                                       revenue_quarterly_df = pd.DataFrame(revenue_quarterly_list_billion, index=date_list_quarter,  columns=["Revenue"])
                                                       revenue_quarterly_df = revenue_quarterly_df.transpose()
                                                  #..........................................................................................................................................
                                                       Pretax_income_quarterly_table = ["{:.2f}B".format(pretax_income / 1000000000) if abs(pretax_income) >= 1000000000 else "{:,.0f}M".format(pretax_income / 1000000) for pretax_income in Pretax_income_quarterly]
                                                       Pretax_income_quarterly_df = pd.DataFrame(Pretax_income_quarterly_table, index=date_list_quarter,  columns=["Pre_Tax Income"])
                                                       Pretax_income_quarterly_df = Pretax_income_quarterly_df.transpose()
                                                  #----------------------------------------------------------------    
                                                       
                                                       net_income_quarterly_table = ["{:.2f}B".format(net_income / 1000000000) if abs(net_income) >= 1000000000 else "{:,.0f}M".format(net_income / 1000000) for net_income in net_income_quarterly]
                                                       net_income_quarterly_df = pd.DataFrame(net_income_quarterly_table, index=date_list_quarter,  columns=["Net Income"])
                                                       net_income_quarterly_df = net_income_quarterly_df.transpose()
                                                  #----------------------------------------------------------------   
                                                       eps_basic_quarterly_table = ["{:.2f}".format(eps_basic) for eps_basic in eps_basic_quarterly]
                                                                 #eps_basic_table = [int(eps_basic) for eps_basic in eps_basic_annual]
                                                       eps_basic_quarterly_df = pd.DataFrame(eps_basic_quarterly_table, index=date_list_quarter,  columns=["EPS(basic)"])
                                                       eps_basic_quarterly_df = eps_basic_quarterly_df.transpose()
                                                  #----------------------------------------------------------------    
                                                       shares_basic_quarterly_table = ["{:.2f}B".format(shares_basic / 1000000000) if shares_basic >= 1000000000 else "{:,.0f}M".format(shares_basic / 1000000) for shares_basic in shares_basic_quarterly]
                                                       shares_basic_quarterly_df = pd.DataFrame(shares_basic_quarterly_table, index=date_list_quarter,  columns=["Basic Shares Outstanding"])
                                                       shares_basic_quarterly_df = shares_basic_quarterly_df.transpose()
                                                  #----------------------------------------------------------------    
                                                       eps_diluted_quarterly_table = ["{:.2f}".format(eps_diluted / 1) for eps_diluted in eps_diluted_quarterly]
                                                       eps_diluted_quarterly_df = pd.DataFrame(eps_diluted_quarterly_table, index=date_list_quarter,  columns=["EPS(diluted)"])
                                                       eps_diluted_quarterly_df = eps_diluted_quarterly_df.transpose()
                                                  #----------------------------------------------------------------    
                                                       shares_diluted_quarterly_table = ["{:.2f}B".format(shares_diluted / 1000000000) if shares_diluted >= 1000000000 else "{:,.0f}M".format(shares_diluted / 1000000) for shares_diluted in shares_diluted_quarterly]
                                                       shares_diluted_quarterly_df = pd.DataFrame(shares_diluted_quarterly_table, index=date_list_quarter,  columns=["Diluted Shares Outstanding"])
                                                       shares_diluted_quarterly_df = shares_diluted_quarterly_df.transpose()
                                                  #----------------------------------------------------------------      
                                                  
                                                       # Convert interest income values to billion USD and round to 3 decimal places
                                                       Total_interestincome_list_quarterly_billion = ["{:.2f}B".format(total_interest_income / 1000000000) if abs(total_interest_income) >= 1000000000 else "{:,.0f}M".format(total_interest_income / 1000000) for total_interest_income in Total_interest_income_list_quarterly]
                                                       total_interestincome_quarterly_df = pd.DataFrame(Total_interestincome_list_quarterly_billion,  index=date_list_quarter, columns=["Total Interest Income"])
                                                       total_interestincome_quarterly_df = total_interestincome_quarterly_df.transpose()
                                                       #-------------------------------------------------------------
                                                                                                    # Convert interest income values to billion USD and round to 3 decimal places
                                                       Total_interest_expense_list_quarterly_billion = ["{:.2f}B".format(total_interest_expense / 1000000000) if abs(total_interest_expense) >= 1000000000 else "{:,.0f}M".format(total_interest_expense / 1000000) for total_interest_expense in Total_interest_expense_list_quarterly]
                                                       total_interest_expense_quarterly_df = pd.DataFrame(Total_interest_expense_list_quarterly_billion,  index=date_list_quarter, columns=["Total Interest Expense"])
                                                       total_interest_expense_quarterly_df = total_interest_expense_quarterly_df.transpose()
                                                       #-------------------------------------------------------------
                                   
                                                       Net_interest_Income_list_quarterly_billion = ["{:.2f}B".format(net_interest_income / 1000000000) if abs(net_interest_income) >= 1000000000 else "{:,.0f}M".format(net_interest_income / 1000000) for net_interest_income in Total_interest_income_list_quarterly]
                                                       Net_interest_Income_quarterly_df = pd.DataFrame(Net_interest_Income_list_quarterly_billion,  index=date_list_quarter, columns=["Net Interest Income"])
                                                       Net_interest_Income_quarterly_df = Net_interest_Income_quarterly_df.transpose()
                                                       #-------------------------------------------------------------
                                                                 
                                                       Prov_Credit_losses_list_quarterly_billion = ["{:.2f}B".format(credit_losses_provision / 1000000000) if abs(credit_losses_provision) >= 1000000000 else "{:,.0f}M".format(credit_losses_provision / 1000000) for credit_losses_provision in Prov_Credit_losses_quarterly]
                                                       Prov_Credit_losses_quarterly_df = pd.DataFrame(Prov_Credit_losses_list_quarterly_billion,  index=date_list_quarter, columns=["Provision for Credit Losses"])
                                                       Prov_Credit_losses_quarterly_df = Prov_Credit_losses_quarterly_df.transpose()
                                                       #-------------------------------------------------------------
                                                       Netinterest_Prov_Credit_losses_list_quarterly_billion = ["{:.2f}B".format(net_interest_income_after_credit_losses_provision / 1000000000) if abs(net_interest_income_after_credit_losses_provision) >= 1000000000 else "{:,.0f}M".format(net_interest_income_after_credit_losses_provision / 1000000) for net_interest_income_after_credit_losses_provision in Netinterest_Prov_Credit_losses_quarterly]
                                                       Netinterest_Prov_Credit_losses_quarterly_df = pd.DataFrame(Netinterest_Prov_Credit_losses_list_quarterly_billion,  index=date_list_quarter, columns=["Net Interest Income After Provision"])
                                                       Netinterest_Prov_Credit_losses_quarterly_df = Netinterest_Prov_Credit_losses_quarterly_df.transpose()
                                                       #-------------------------------------------------------------
                                                       
                                                                 
                                                       Total_Non_interest_expenses_list_quarterly_billion = ["{:.2f}B".format(total_noninterest_expense / 1000000000) if abs(total_noninterest_expense) >= 1000000000 else "{:,.0f}M".format(total_noninterest_expense / 1000000) for total_noninterest_expense in Total_Non_interest_expenses_quarterly]
                                                       Total_Non_interest_expenses_quarterly_df = pd.DataFrame(Total_interestincome_list_quarterly_billion,  index=date_list_quarter, columns=["Non Interest Expense"])
                                                       Total_Non_interest_expenses_quarterly_df = Total_Non_interest_expenses_quarterly_df.transpose()
                                                       #-------------------------------------------------------------
                                   
                                                       Total_Non_interest_revenue_list_quarterly_billion = ["{:.2f}B".format(total_noninterest_revenue / 1000000000) if abs(total_noninterest_revenue) >= 1000000000 else "{:,.0f}M".format(total_noninterest_revenue / 1000000) for total_noninterest_revenue in Total_Non_interest_revenue_quarterly]
                                                       Total_Non_interest_revenue_quarterly_df = pd.DataFrame(Total_Non_interest_revenue_list_quarterly_billion,  index=date_list_quarter, columns=["Non Interest Revenue"])
                                                       Total_Non_interest_revenue_quarterly_df =Total_Non_interest_revenue_quarterly_df.transpose()
                                                       #-------------------------------------------------------------

                                                       merged_df_banks = pd.concat([total_interest_expense_quarterly_df,total_interestincome_quarterly_df,Net_interest_Income_quarterly_df,Prov_Credit_losses_quarterly_df,Total_Non_interest_expenses_quarterly_df,Total_Non_interest_revenue_quarterly_df,net_income_quarterly_df,Pretax_income_quarterly_df,eps_basic_quarterly_df,shares_basic_quarterly_df,eps_diluted_quarterly_df,shares_diluted_quarterly_df])    

                                                       st.table(merged_df_banks.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))

                                                                 
                                                                 #st.dataframe(merged_df_banks.style.set_table_attributes('class="scroll-table"'),use_container_width=True)
                                                            
                                                                # st.markdown('<div style="margin-bottom: 100px;"></div>', unsafe_allow_html=True)   
                                                       pass
                                                  
                                                 # elif "Insurance" in Industry or "Health Care Providers & Services" in Industry :
                                                  except KeyError:
                                                                 try:
                                                                      Net_premiums_earned = quarterly_data['premiums_earned'][-10:] 
                                                                      Net_investment_income = quarterly_data['net_investment_income'][-10:] 
                                                                      Fees_and_other_income = quarterly_data['fees_and_other_income'][-10:] 
                                                                      Interest_Expense_insurance = quarterly_data['interest_expense_insurance'][-10:] 
                                                                      revenue_2013 = quarterly_data['revenue'][-10:] 
                                                                      Pretax_income_annual = quarterly_data['pretax_income'][-10:]
                                                                      net_income_annual = quarterly_data['net_income'][-10:] 
                                                                      eps_basic_annual = quarterly_data['eps_basic'][-10:]
                                                                      shares_basic_annual = quarterly_data['shares_basic'][-10:]
                                                                      eps_diluted_annual = quarterly_data['eps_diluted'][-10:]
                                                                      shares_diluted_annual = quarterly_data['shares_diluted'][-10:]
                                                                      Income_tax_annual = quarterly_data['income_tax'][-10:]

                                                                      Net_premiums_earned_list_billion = ["{:.2f}B".format(premiums_earned / 1000000000) if abs(premiums_earned) >= 1000000000 else "{:,.0f}M".format(premiums_earned / 1000000) for premiums_earned in Net_premiums_earned]
                                                                      net_premiums_earned_df = pd.DataFrame(Net_premiums_earned_list_billion, index=date_list_quarter,  columns=["Net Premiums Earned"])
                                                                      net_premiums_earned_df = net_premiums_earned_df.transpose()
                                                                      #....................................................................................................
                                                                      #Net_investment_income = quarterly_data['net_investment_income'][-10:] 
                                                                 
                                                                      Net_investment_income_list_billion = ["{:.2f}B".format(net_investment_income / 1000000000) if abs(net_investment_income) >= 1000000000 else "{:,.0f}M".format(net_investment_income / 1000000) for net_investment_income in Net_investment_income]
                                                                      net_investment_income_df = pd.DataFrame(Net_investment_income_list_billion, index=date_list_quarter,  columns=["Net Investment Income"])
                                                                      net_investment_income_df = net_investment_income_df.transpose()
                                                                      #....................................................................................................
                                                                           #Fees_and_other_income = quarterly_data['fees_and_other_income'][-10:] 
                                                                      
                                                                      Fees_and_other_income_list_billion = ["{:.2f}B".format(fees_and_other_income / 1000000000) if abs(fees_and_other_income) >= 1000000000 else "{:,.0f}M".format(fees_and_other_income / 1000000) for fees_and_other_income in Fees_and_other_income]
                                                                      Fees_and_other_income_df = pd.DataFrame(Fees_and_other_income_list_billion, index=date_list_quarter,  columns=["Fees And Other Income"])
                                                                      Fees_and_other_income_df = Fees_and_other_income_df.transpose()
                                                                      #....................................................................................................
                                                                      #Interest_Expense_insurance = quarterly_data['interest_Expense_insurance'][-10:] 
                                                                      Interest_Expense_insurance_list_billion = ["{:.2f}B".format(interest_expense_insurance / 1000000000) if abs(interest_expense_insurance) >= 1000000000 else "{:,.0f}M".format(interest_expense_insurance / 1000000) for interest_expense_insurance in Interest_Expense_insurance]
                                                                      Interest_Expense_insurance_df = pd.DataFrame(Interest_Expense_insurance_list_billion, index=date_list_quarter,  columns=["Interest Expense"])
                                                                      Interest_Expense_insurance_df = Interest_Expense_insurance_df.transpose()
                                                                      
                                                                      #....................................................................................................
                                                                      revenue_list_billion = ["{:.2f}B".format(revenue / 1000000000) if abs(revenue) >= 1000000000 else "{:,.0f}M".format(revenue / 1000000) for revenue in revenue_2013]
                                                                      revenue_df = pd.DataFrame(revenue_list_billion, index=date_list_quarter,  columns=["Total Revenue"])
                                                                      revenue_df = revenue_df.transpose()
                                                                      
                                                                      #..........................................................................................................................................
                                                                      Pretax_income_table = ["{:.2f}B".format(pretax_income / 1000000000) if abs(pretax_income) >= 1000000000 else "{:,.0f}M".format(pretax_income / 1000000) for pretax_income in Pretax_income_annual]
                                                                      Pretax_income_df = pd.DataFrame(Pretax_income_table, index=date_list_quarter,  columns=["Pre-Tax Income"])
                                                                      Pretax_income_df = Pretax_income_df.transpose()
                                                       #----------------------------------------------------------------    
                                                            
                                                                      net_income_table = ["{:.2f}B".format(net_income / 1000000000) if abs(net_income) >= 1000000000 else "{:,.0f}M".format(net_income / 1000000) for net_income in net_income_annual]
                                                                      net_income_df = pd.DataFrame(net_income_table, index=date_list_quarter,  columns=["Net Income"])
                                                                      net_income_df = net_income_df.transpose()
                                                       #----------------------------------------------------------------   
                                                                      eps_basic_table = ["{:.2f}".format(eps_basic) for eps_basic in eps_basic_annual]
                                                                      #eps_basic_table = [int(eps_basic) for eps_basic in eps_basic_annual]
                                                                      eps_basic_df = pd.DataFrame(eps_basic_table, index=date_list_quarter,  columns=["EPS(basic)"])
                                                                      eps_basic_df = eps_basic_df.transpose()
                                                       #----------------------------------------------------------------    
                                                                      shares_basic_table = ["{:.2f}B".format(shares_basic / 1000000000) if shares_basic >= 1000000000 else "{:,.0f}M".format(shares_basic / 1000000) for shares_basic in shares_basic_annual]
                                                                      shares_basic_df = pd.DataFrame(shares_basic_table, index=date_list_quarter,  columns=["Basic Shares Outstanding"])
                                                                      shares_basic_df = shares_basic_df.transpose()
                                                       #----------------------------------------------------------------    
                                                                      eps_diluted_table = ["{:.2f}".format(eps_diluted / 1) for eps_diluted in eps_diluted_annual]
                                                                      eps_diluted_df = pd.DataFrame(eps_diluted_table, index=date_list_quarter,  columns=["EPS(diluted)"])
                                                                      eps_diluted_df = eps_diluted_df.transpose()
                                                       #----------------------------------------------------------------    
                                                                      shares_diluted_table = ["{:.2f}B".format(shares_diluted / 1000000000) if shares_diluted >= 1000000000 else "{:,.0f}M".format(shares_diluted / 1000000) for shares_diluted in shares_diluted_annual]
                                                                      shares_diluted_df = pd.DataFrame(shares_diluted_table, index=date_list_quarter,  columns=["Diluted Shares Outstanding"])
                                                                      shares_diluted_df = shares_diluted_df.transpose()
                                                  
                                                                      merged_df_insurance = pd.concat([net_premiums_earned_df,net_investment_income_df,Fees_and_other_income_df,revenue_df,Interest_Expense_insurance_df,Pretax_income_df,net_income_df,eps_basic_df,shares_basic_df,eps_diluted_df,shares_diluted_df]) 
                                             
                                                                      st.table(merged_df_insurance.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))

                                                                      #st.dataframe(merged_df_insurance.style.set_table_attributes('class="scroll-table"'),use_container_width=True)

                                                                      #st.markdown('<div style="margin-bottom: 100px;"></div>', unsafe_allow_html=True) 
                                                                      
                                                                 except KeyError:


          #                                                             revenue_2013 = quarterly_data['revenue'][-10:] 
          #                                                             Pretax_income_annual = quarterly_data['pretax_income'][-10:]
          #                                                             eps_basic_annual = quarterly_data['eps_basic'][-10:]
          #                                                             shares_basic_annual = quarterly_data['shares_basic'][-10:]
          #                                                             eps_diluted_annual = quarterly_data['eps_diluted'][-10:]
          #                                                             shares_diluted_annual = quarterly_data['shares_diluted'][-10:]
          #                                                             Income_tax_annual = quarterly_data['income_tax'][-10:]
          #                                                             net_income_annual = quarterly_data['net_income'][-10:]
          #                                                             cogs_list = quarterly_data['cogs'][-10:]
          #                                                             gross_profit_2013 = quarterly_data['gross_profit'][-10:]
          #                                                             SGA_Expense_annual = quarterly_data['total_opex'][-10:]
          #                                                             Research_Dev_annual = quarterly_data['rnd'][-10:]
          #                                                             interest_expense_list = quarterly_data['interest_expense'][-10:]
          #                                                             #Total_interest_income_list = annual_data['total_interest_income'][-10:]
          #                                                             interest_income_list = quarterly_data['interest_income'][-10:]
          #                                                             Ebita_annual = quarterly_data['ebitda'][-10:]
          #                                                             operating_income_list = quarterly_data['operating_income'][-10:]  
          # #....................................................................................................
          #                                                             revenue_list_billion = ["{:.2f}B".format(revenue / 1000000000) if abs(revenue) >= 1000000000 else "{:,.0f}M".format(revenue / 1000000) for revenue in revenue_2013]
          #                                                             revenue_df = pd.DataFrame(revenue_list_billion, index=date_list_quarter,  columns=["Revenue"])
          #                                                             revenue_df = revenue_df.transpose()

          #                                              #-----------------------------------------------------------
          #                                              # Convert cogs values to billion USD and round to 3 decimal places
          #                                                             #cogs_list_billion = ["{:.2f}B".format(cogs / 1000000000) for cogs in cogs_list]
          #                                                             cogs_list_billion = ["{:.2f}B".format(cogs / 1000000000) if abs(cogs) >= 1000000000 else "{:,.0f}M".format(cogs / 1000000) for cogs in cogs_list]
          #                                                             cogs_df = pd.DataFrame(cogs_list_billion,  index=date_list_quarter, columns=["Cost of Goods Sold"])
          #                                                             cogs_df = cogs_df.transpose()
          #                                              #----------------------------------------------------------
          #                                              # Convert gross profit values to billion USD and round to 3 decimal places
          #                                                             gross_profit_list_billion = ["{:.2f}B".format(gross_profit / 1000000000) if abs(gross_profit) >= 1000000000 else "{:,.0f}M".format(gross_profit / 1000000) for gross_profit in gross_profit_2013]
          #                                                             gross_profit_df = pd.DataFrame(gross_profit_list_billion, index=date_list_quarter,  columns=["Gross Profit"])
          #                                                             gross_profit_df = gross_profit_df.transpose()
          #                                              #----------------------------------------------------------------

          #                                                             SGA_Expense_table = ["{:.2f}B".format(total_opex / 1000000000) if abs(total_opex) >= 1000000000 else "{:,.0f}M".format(total_opex / 1000000) for total_opex in SGA_Expense_annual]
          #                                                             SGA_Expense_df = pd.DataFrame(SGA_Expense_table, index=date_list_quarter,  columns=["Operating Expense"])
          #                                                             SGA_Expense_df = SGA_Expense_df.transpose()
          #                                              #----------------------------------------------------------------
          #                                                             Research_Dev_table = ["{:.2f}B".format(rnd / 1000000000) if abs(rnd) >= 1000000000 else "{:,.0f}M".format(rnd / 1000000) for rnd in Research_Dev_annual]
          #                                                             Research_Dev_df = pd.DataFrame(Research_Dev_table, index=date_list_quarter,  columns=["Research & Development"])
          #                                                             Research_Dev_df = Research_Dev_df.transpose()
          #                                              #----------------------------------------------------------------    
          #                                                             interestexpense_list_billion = ["{:.2f}B".format(interest_expense / -1000000000) if abs(interest_expense) >= 1000000000 else "{:,.0f}M".format(interest_expense / -1000000) for interest_expense in interest_expense_list]
          #                                                             interestexxpense_df = pd.DataFrame(interestexpense_list_billion, index=date_list_quarter, columns=["Interest Expense"])                                   
          #                                                             interestexxpense_df = interestexxpense_df.transpose()                                                                  
          #                                              # -------------------------------------------------------------------
          #                                                             Pretax_income_table = ["{:.2f}B".format(pretax_income / 1000000000) if abs(pretax_income) >= 1000000000 else "{:,.0f}M".format(pretax_income / 1000000) for pretax_income in Pretax_income_annual]
          #                                                             Pretax_income_df = pd.DataFrame(Pretax_income_table, index=date_list_quarter,  columns=["Pre-Tax Income"])
          #                                                             Pretax_income_df = Pretax_income_df.transpose()
          #                                              #----------------------------------------------------------------    
          #                                                             Income_tax_table = ["{:.2f}B".format(income_tax / -1000000000) if abs(income_tax) >= 1000000000 else "{:,.0f}M".format(income_tax / -1000000) for income_tax in Income_tax_annual]
          #                                                             Income_tax_df = pd.DataFrame(Income_tax_table, index=date_list_quarter,  columns=["Income Tax"])
          #                                                             Income_tax_df = Income_tax_df.transpose()
          #                                              #----------------------------------------------------------------       
          #                                                             net_income_table = ["{:.2f}B".format(net_income / 1000000000) if abs(net_income) >= 1000000000 else "{:,.0f}M".format(net_income / 1000000) for net_income in net_income_annual]
          #                                                             net_income_df = pd.DataFrame(net_income_table, index=date_list_quarter,  columns=["Net Income"])
          #                                                             net_income_df = net_income_df.transpose()
          #                                              #----------------------------------------------------------------   
          #                                                             eps_basic_table = ["{:.2f}".format(eps_basic) for eps_basic in eps_basic_annual]
          #                                                             #eps_basic_table = [int(eps_basic) for eps_basic in eps_basic_annual]
          #                                                             eps_basic_df = pd.DataFrame(eps_basic_table, index=date_list_quarter,  columns=["EPS(basic)"])
          #                                                             eps_basic_df = eps_basic_df.transpose()
          #                                              #----------------------------------------------------------------    
          #                                                             shares_basic_table = ["{:.2f}B".format(shares_basic / 1000000000) if shares_basic >= 1000000000 else "{:,.0f}M".format(shares_basic / 1000000) for shares_basic in shares_basic_annual]
          #                                                             shares_basic_df = pd.DataFrame(shares_basic_table, index=date_list_quarter,  columns=["Basic Shares Outstanding"])
          #                                                             shares_basic_df = shares_basic_df.transpose()
          #                                              #----------------------------------------------------------------    
          #                                                             eps_diluted_table = ["{:.2f}".format(eps_diluted / 1) for eps_diluted in eps_diluted_annual]
          #                                                             eps_diluted_df = pd.DataFrame(eps_diluted_table, index=date_list_quarter,  columns=["EPS(diluted)"])
          #                                                             eps_diluted_df = eps_diluted_df.transpose()
          #                                              #----------------------------------------------------------------    
          #                                                             shares_diluted_table = ["{:.2f}B".format(shares_diluted / 1000000000) if shares_diluted >= 1000000000 else "{:,.0f}M".format(shares_diluted / 1000000) for shares_diluted in shares_diluted_annual]
          #                                                             shares_diluted_df = pd.DataFrame(shares_diluted_table, index=date_list_quarter,  columns=["Diluted Shares Outstanding"])
          #                                                             shares_diluted_df = shares_diluted_df.transpose()
          #                                              #----------------------------------------------------------------      
          #                                                             Ebitda_table = ["{:.2f}B".format(ebitda / 1000000000) if abs(ebitda) >= 1000000000 else "{:,.0f}M".format(ebitda / 1000000) for ebitda in Ebita_annual]
          #                                                             Ebitda_df = pd.DataFrame(Ebitda_table, index=date_list_quarter,  columns=["EBITDA"])
          #                                                             Ebitda_df = Ebitda_df.transpose()
          #                                              #----------------------------------------------------------------                                    
          #                                                             operatingincome_list_billion = ["{:.2f}B".format(operating_income / 1000000000) if abs(operating_income) >= 1000000000 else "{:,.0f}M".format(operating_income / 1000000) for operating_income in operating_income_list]
          #                                                             operatingincome_df = pd.DataFrame(operatingincome_list_billion,  index=date_list_quarter, columns=["Operating Income"])
          #                                                             operatingincome_df = operatingincome_df.transpose()
          #                                              #-------------------------------------------------------------

          #                                              # Convert interest income values to billion USD and round to 3 decimal places
          #                                                             interestincome_list_billion = ["{:.2f}B".format(interest_income / 1000000000) if abs(interest_income) >= 1000000000 else "{:,.0f}M".format(interest_income / 1000000) for interest_income in interest_income_list]
          #                                                             interestincome_df = pd.DataFrame(interestincome_list_billion,  index=date_list_quarter, columns=["Non-Operating Interest Income"])
          #                                                             interestincome_df = interestincome_df.transpose()
          #                                                   #------------------------------------------------------------

                                                                      
          #                                                             merged_df_insurance = pd.concat([revenue_df,cogs_df, gross_profit_df,SGA_Expense_df, Research_Dev_df,interestincome_df,interestexxpense_df,Pretax_income_df,Income_tax_df,net_income_df,eps_basic_df,shares_basic_df,eps_diluted_df,shares_diluted_df,Ebitda_df])  
                                                                      
          #                                                             st.table(merged_df_insurance.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))
     
                                                                      pass
                                                  #else:
                                                  try:          #st.write("no")       
                                                       revenue_2013 = quarterly_data['revenue'][-10:] 
                                                       Pretax_income_annual = quarterly_data['pretax_income'][-10:]
                                                       eps_basic_annual = quarterly_data['eps_basic'][-10:]
                                                       shares_basic_annual = quarterly_data['shares_basic'][-10:]
                                                       eps_diluted_annual = quarterly_data['eps_diluted'][-10:]
                                                       shares_diluted_annual = quarterly_data['shares_diluted'][-10:]
                                                       Income_tax_annual = quarterly_data['income_tax'][-10:]
                                                       net_income_annual = quarterly_data['net_income'][-10:]
                                                       cogs_list = quarterly_data['cogs'][-10:]
                                                       gross_profit_2013 = quarterly_data['gross_profit'][-10:]
                                                       SGA_Expense_annual = quarterly_data['total_opex'][-10:]
                                                       Research_Dev_annual = quarterly_data['rnd'][-10:]
                                                       interest_expense_list = quarterly_data['interest_expense'][-10:]
                                                                 #Total_interest_income_list = annual_data['total_interest_income'][-10:]
                                                       interest_income_list = quarterly_data['interest_income'][-10:]
                                                       Ebita_annual = quarterly_data['ebitda'][-10:]
                                                       operating_income_list = quarterly_data['operating_income'][-10:]                                   
                                                  #....................................................................................................
                                                       revenue_list_billion = ["{:.2f}B".format(revenue / 1000000000) if abs(revenue) >= 1000000000 else "{:,.0f}M".format(revenue / 1000000) for revenue in revenue_2013]
                                                       revenue_df = pd.DataFrame(revenue_list_billion, index=date_list_quarter,  columns=["Revenue"])
                                                       revenue_df = revenue_df.transpose()

                                                  #-----------------------------------------------------------
                                                  # Convert cogs values to billion USD and round to 3 decimal places
                                                                 #cogs_list_billion = ["{:.2f}B".format(cogs / 1000000000) for cogs in cogs_list]
                                                       cogs_list_billion = ["{:.2f}B".format(cogs / 1000000000) if abs(cogs) >= 1000000000 else "{:,.0f}M".format(cogs / 1000000) for cogs in cogs_list]
                                                       cogs_df = pd.DataFrame(cogs_list_billion,  index=date_list_quarter, columns=["Cost of Goods Sold"])
                                                       cogs_df = cogs_df.transpose()
                                                  #----------------------------------------------------------
                                                  # Convert gross profit values to billion USD and round to 3 decimal places
                                                       gross_profit_list_billion = ["{:.2f}B".format(gross_profit / 1000000000) if abs(gross_profit) >= 1000000000 else "{:,.0f}M".format(gross_profit / 1000000) for gross_profit in gross_profit_2013]
                                                       gross_profit_df = pd.DataFrame(gross_profit_list_billion, index=date_list_quarter,  columns=["Gross Profit"])
                                                       gross_profit_df = gross_profit_df.transpose()
                                                  #----------------------------------------------------------------

                                                       SGA_Expense_table = ["{:.2f}B".format(total_opex / 1000000000) if abs(total_opex) >= 1000000000 else "{:,.0f}M".format(total_opex / 1000000) for total_opex in SGA_Expense_annual]
                                                       SGA_Expense_df = pd.DataFrame(SGA_Expense_table, index=date_list_quarter,  columns=["Operating Expense"])
                                                       SGA_Expense_df = SGA_Expense_df.transpose()
                                                  #----------------------------------------------------------------
                                                       Research_Dev_table = ["{:.2f}B".format(rnd / 1000000000) if abs(rnd) >= 1000000000 else "{:,.0f}M".format(rnd / 1000000) for rnd in Research_Dev_annual]
                                                       Research_Dev_df = pd.DataFrame(Research_Dev_table, index=date_list_quarter,  columns=["Research & Development"])
                                                       Research_Dev_df = Research_Dev_df.transpose()
                                                  #----------------------------------------------------------------    
                                                       interestexpense_list_billion = ["{:.2f}B".format(interest_expense / -1000000000) if abs(interest_expense) >= 1000000000 else "{:,.0f}M".format(interest_expense / -1000000) for interest_expense in interest_expense_list]
                                                       interestexxpense_df = pd.DataFrame(interestexpense_list_billion, index=date_list_quarter, columns=["Interest Expense"])                                   
                                                       interestexxpense_df = interestexxpense_df.transpose()                                                                  
                                                  # -------------------------------------------------------------------
                                                       Pretax_income_table = ["{:.2f}B".format(pretax_income / 1000000000) if abs(pretax_income) >= 1000000000 else "{:,.0f}M".format(pretax_income / 1000000) for pretax_income in Pretax_income_annual]
                                                       Pretax_income_df = pd.DataFrame(Pretax_income_table, index=date_list_quarter,  columns=["Pre-Tax Income"])
                                                       Pretax_income_df = Pretax_income_df.transpose()
                                                  #----------------------------------------------------------------    
                                                       Income_tax_table = ["{:.2f}B".format(income_tax / -1000000000) if abs(income_tax) >= 1000000000 else "{:,.0f}M".format(income_tax / -1000000) for income_tax in Income_tax_annual]
                                                       Income_tax_df = pd.DataFrame(Income_tax_table, index=date_list_quarter,  columns=["Income Tax"])
                                                       Income_tax_df = Income_tax_df.transpose()
                                                  #----------------------------------------------------------------       
                                                       net_income_table = ["{:.2f}B".format(net_income / 1000000000) if abs(net_income) >= 1000000000 else "{:,.0f}M".format(net_income / 1000000) for net_income in net_income_annual]
                                                       net_income_df = pd.DataFrame(net_income_table, index=date_list_quarter,  columns=["Net Income"])
                                                       net_income_df = net_income_df.transpose()
                                                  #----------------------------------------------------------------   
                                                       eps_basic_table = ["{:.2f}".format(eps_basic) for eps_basic in eps_basic_annual]
                                                                 #eps_basic_table = [int(eps_basic) for eps_basic in eps_basic_annual]
                                                       eps_basic_df = pd.DataFrame(eps_basic_table, index=date_list_quarter,  columns=["EPS(basic)"])
                                                       eps_basic_df = eps_basic_df.transpose()
                                                  #----------------------------------------------------------------    
                                                       shares_basic_table = ["{:.2f}B".format(shares_basic / 1000000000) if shares_basic >= 1000000000 else "{:,.0f}M".format(shares_basic / 1000000) for shares_basic in shares_basic_annual]
                                                       shares_basic_df = pd.DataFrame(shares_basic_table, index=date_list_quarter,  columns=["Basic Shares Outstanding"])
                                                       shares_basic_df = shares_basic_df.transpose()
                                                  #----------------------------------------------------------------    
                                                       eps_diluted_table = ["{:.2f}".format(eps_diluted / 1) for eps_diluted in eps_diluted_annual]
                                                       eps_diluted_df = pd.DataFrame(eps_diluted_table, index=date_list_quarter,  columns=["EPS(diluted)"])
                                                       eps_diluted_df = eps_diluted_df.transpose()
                                                  #----------------------------------------------------------------    
                                                       shares_diluted_table = ["{:.2f}B".format(shares_diluted / 1000000000) if shares_diluted >= 1000000000 else "{:,.0f}M".format(shares_diluted / 1000000) for shares_diluted in shares_diluted_annual]
                                                       shares_diluted_df = pd.DataFrame(shares_diluted_table, index=date_list_quarter,  columns=["Diluted Shares Outstanding"])
                                                       shares_diluted_df = shares_diluted_df.transpose()
                                                  #----------------------------------------------------------------      
                                                       Ebitda_table = ["{:.2f}B".format(ebitda / 1000000000) if abs(ebitda) >= 1000000000 else "{:,.0f}M".format(ebitda / 1000000) for ebitda in Ebita_annual]
                                                       Ebitda_df = pd.DataFrame(Ebitda_table, index=date_list_quarter,  columns=["EBITDA"])
                                                       Ebitda_df = Ebitda_df.transpose()
                                                  #----------------------------------------------------------------                                    
                                                       operatingincome_list_billion = ["{:.2f}B".format(operating_income / 1000000000) if abs(operating_income) >= 1000000000 else "{:,.0f}M".format(operating_income / 1000000) for operating_income in operating_income_list]
                                                       operatingincome_df = pd.DataFrame(operatingincome_list_billion,  index=date_list_quarter, columns=["Operating Income"])
                                                       operatingincome_df = operatingincome_df.transpose()
                                                  #-------------------------------------------------------------

                                                  # Convert interest income values to billion USD and round to 3 decimal places
                                                       interestincome_list_billion = ["{:.2f}B".format(interest_income / 1000000000) if abs(interest_income) >= 1000000000 else "{:,.0f}M".format(interest_income / 1000000) for interest_income in interest_income_list]
                                                       interestincome_df = pd.DataFrame(interestincome_list_billion,  index=date_list_quarter, columns=["Non-Operating Interest Income"])
                                                       interestincome_df = interestincome_df.transpose()
                                                       #------------------------------------------------------------

                                                       merged_df = pd.concat([revenue_df,cogs_df, gross_profit_df,SGA_Expense_df, Research_Dev_df,interestincome_df,interestexxpense_df,Pretax_income_df,Income_tax_df,net_income_df,eps_basic_df,shares_basic_df,eps_diluted_df,shares_diluted_df,Ebitda_df])  
                                                       st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))

                                                                 
                                                                 #st.dataframe(merged_df.style.set_table_attributes('class="scroll-table"'),use_container_width=True)
                                                                
                                                                # st.markdown('<div style="margin-bottom: 100px;"></div>', unsafe_allow_html=True)      
                                                  
                                                       pass
                                                  except KeyError:   

                                                       st.write()
                                                       pass  
                                             

                                                  with Annual: 

                                                  #if "Consumer Finance" in Industry or "Banks" in Industry or ticker == "MAIN":
                                                       try:               
                                                            revenue_2013_quarterly = annual_data['revenue'][-10:] 
                                                            Pretax_income_quarterly = annual_data['pretax_income'][-10:]
                                                            eps_basic_quarterly= annual_data['eps_basic'][-10:]
                                                            shares_basic_quarterly = annual_data['shares_basic'][-10:]
                                                            eps_diluted_quarterly = annual_data['eps_diluted'][-10:]
                                                            shares_diluted_quarterly = annual_data['shares_diluted'][-10:]
                                                            Income_tax_quarterly = annual_data['income_tax'][-10:]
                                                            net_income_quarterly = annual_data['net_income'][-10:]
                                                            Total_interest_income_list_quarterly = annual_data['total_interest_income'][-10:]
                                                            Total_interest_expense_list_quarterly = annual_data['total_interest_expense'][-10:]
                                                            Net_interest_Income_quarterly = annual_data['net_interest_income'][-10:]
                                                            Prov_Credit_losses_quarterly = annual_data['credit_losses_provision'][-10:]
                                                            Netinterest_Prov_Credit_losses_quarterly = annual_data['net_interest_income_after_credit_losses_provision'][-10:]
                                                            Total_Non_interest_expenses_quarterly = annual_data['total_noninterest_expense'][-10:]
                                                            Total_Non_interest_revenue_quarterly = annual_data['total_noninterest_revenue'][-10:]
                                                       #....................................................................................................
                                                            revenue_quarterly_list_billion = ["{:.2f}B".format(revenue / 1000000000) if abs(revenue)>= 1000000000 else "{:,.0f}M".format(revenue / 1000000) for revenue in revenue_2013_quarterly]
                                                            revenue_quarterly_df = pd.DataFrame(revenue_quarterly_list_billion, index=date_list_annual,  columns=["Revenue"])
                                                            revenue_quarterly_df = revenue_quarterly_df.transpose()
                                                       #..........................................................................................................................................
                                                            Pretax_income_quarterly_table = ["{:.2f}B".format(pretax_income / 1000000000) if abs(pretax_income) >= 1000000000 else "{:,.0f}M".format(pretax_income / 1000000) for pretax_income in Pretax_income_quarterly]
                                                            Pretax_income_quarterly_df = pd.DataFrame(Pretax_income_quarterly_table, index=date_list_annual,  columns=["Pre_Tax Income"])
                                                            Pretax_income_quarterly_df = Pretax_income_quarterly_df.transpose()
                                                       #----------------------------------------------------------------    
                                                            
                                                            net_income_quarterly_table = ["{:.2f}B".format(net_income / 1000000000) if abs(net_income) >= 1000000000 else "{:,.0f}M".format(net_income / 1000000) for net_income in net_income_quarterly]
                                                            net_income_quarterly_df = pd.DataFrame(net_income_quarterly_table, index=date_list_annual,  columns=["Net Income"])
                                                            net_income_quarterly_df = net_income_quarterly_df.transpose()
                                                       #----------------------------------------------------------------   
                                                            eps_basic_quarterly_table = ["{:.2f}".format(eps_basic) for eps_basic in eps_basic_quarterly]
                                                                      #eps_basic_table = [int(eps_basic) for eps_basic in eps_basic_annual]
                                                            eps_basic_quarterly_df = pd.DataFrame(eps_basic_quarterly_table, index=date_list_annual,  columns=["EPS(basic)"])
                                                            eps_basic_quarterly_df = eps_basic_quarterly_df.transpose()
                                                       #----------------------------------------------------------------    
                                                            shares_basic_quarterly_table = ["{:.2f}B".format(shares_basic / 1000000000) if shares_basic >= 1000000000 else "{:,.0f}M".format(shares_basic / 1000000) for shares_basic in shares_basic_quarterly]
                                                            shares_basic_quarterly_df = pd.DataFrame(shares_basic_quarterly_table, index=date_list_annual,  columns=["Basic Shares Outstanding"])
                                                            shares_basic_quarterly_df = shares_basic_quarterly_df.transpose()
                                                       #----------------------------------------------------------------    
                                                            eps_diluted_quarterly_table = ["{:.2f}".format(eps_diluted / 1) for eps_diluted in eps_diluted_quarterly]
                                                            eps_diluted_quarterly_df = pd.DataFrame(eps_diluted_quarterly_table, index=date_list_annual,  columns=["EPS(diluted)"])
                                                            eps_diluted_quarterly_df = eps_diluted_quarterly_df.transpose()
                                                       #----------------------------------------------------------------    
                                                            shares_diluted_quarterly_table = ["{:.2f}B".format(shares_diluted / 1000000000) if shares_diluted >= 1000000000 else "{:,.0f}M".format(shares_diluted / 1000000) for shares_diluted in shares_diluted_quarterly]
                                                            shares_diluted_quarterly_df = pd.DataFrame(shares_diluted_quarterly_table, index=date_list_annual,  columns=["Diluted Shares Outstanding"])
                                                            shares_diluted_quarterly_df = shares_diluted_quarterly_df.transpose()
                                                       #----------------------------------------------------------------      
                                                       
                                                            # Convert interest income values to billion USD and round to 3 decimal places
                                                            Total_interestincome_list_quarterly_billion = ["{:.2f}B".format(total_interest_income / 1000000000) if abs(total_interest_income) >= 1000000000 else "{:,.0f}M".format(total_interest_income / 1000000) for total_interest_income in Total_interest_income_list_quarterly]
                                                            total_interestincome_quarterly_df = pd.DataFrame(Total_interestincome_list_quarterly_billion,  index=date_list_annual, columns=["Total Interest Income"])
                                                            total_interestincome_quarterly_df = total_interestincome_quarterly_df.transpose()
                                                            #-------------------------------------------------------------
                                                                                                         # Convert interest income values to billion USD and round to 3 decimal places
                                                            Total_interest_expense_list_quarterly_billion = ["{:.2f}B".format(total_interest_expense / 1000000000) if abs(total_interest_expense) >= 1000000000 else "{:,.0f}M".format(total_interest_expense / 1000000) for total_interest_expense in Total_interest_expense_list_quarterly]
                                                            total_interest_expense_quarterly_df = pd.DataFrame(Total_interest_expense_list_quarterly_billion,  index=date_list_annual, columns=["Total Interest Expense"])
                                                            total_interest_expense_quarterly_df = total_interest_expense_quarterly_df.transpose()
                                                            #-------------------------------------------------------------
                                        
                                                            Net_interest_Income_list_quarterly_billion = ["{:.2f}B".format(net_interest_income / 1000000000) if abs(net_interest_income) >= 1000000000 else "{:,.0f}M".format(net_interest_income / 1000000) for net_interest_income in Total_interest_income_list_quarterly]
                                                            Net_interest_Income_quarterly_df = pd.DataFrame(Net_interest_Income_list_quarterly_billion,  index=date_list_annual, columns=["Net Interest Income"])
                                                            Net_interest_Income_quarterly_df = Net_interest_Income_quarterly_df.transpose()
                                                            #-------------------------------------------------------------
                                                                      
                                                            Prov_Credit_losses_list_quarterly_billion = ["{:.2f}B".format(credit_losses_provision / 1000000000) if abs(credit_losses_provision) >= 1000000000 else "{:,.0f}M".format(credit_losses_provision / 1000000) for credit_losses_provision in Prov_Credit_losses_quarterly]
                                                            Prov_Credit_losses_quarterly_df = pd.DataFrame(Prov_Credit_losses_list_quarterly_billion,  index=date_list_annual, columns=["Provision for Credit Losses"])
                                                            Prov_Credit_losses_quarterly_df = Prov_Credit_losses_quarterly_df.transpose()
                                                            #-------------------------------------------------------------
                                                            Netinterest_Prov_Credit_losses_list_quarterly_billion = ["{:.2f}B".format(net_interest_income_after_credit_losses_provision / 1000000000) if abs(net_interest_income_after_credit_losses_provision) >= 1000000000 else "{:,.0f}M".format(net_interest_income_after_credit_losses_provision / 1000000) for net_interest_income_after_credit_losses_provision in Netinterest_Prov_Credit_losses_quarterly]
                                                            Netinterest_Prov_Credit_losses_quarterly_df = pd.DataFrame(Netinterest_Prov_Credit_losses_list_quarterly_billion,  index=date_list_annual, columns=["Net Interest Income After Provision"])
                                                            Netinterest_Prov_Credit_losses_quarterly_df = Netinterest_Prov_Credit_losses_quarterly_df.transpose()
                                                            #-------------------------------------------------------------
                                                            
                                                                      
                                                            Total_Non_interest_expenses_list_quarterly_billion = ["{:.2f}B".format(total_noninterest_expense / 1000000000) if abs(total_noninterest_expense) >= 1000000000 else "{:,.0f}M".format(total_noninterest_expense / 1000000) for total_noninterest_expense in Total_Non_interest_expenses_quarterly]
                                                            Total_Non_interest_expenses_quarterly_df = pd.DataFrame(Total_interestincome_list_quarterly_billion,  index=date_list_annual, columns=["Non Interest Expense"])
                                                            Total_Non_interest_expenses_quarterly_df = Total_Non_interest_expenses_quarterly_df.transpose()
                                                            #-------------------------------------------------------------
                                        
                                                            Total_Non_interest_revenue_list_quarterly_billion = ["{:.2f}B".format(total_noninterest_revenue / 1000000000) if abs(total_noninterest_revenue) >= 1000000000 else "{:,.0f}M".format(total_noninterest_revenue / 1000000) for total_noninterest_revenue in Total_Non_interest_revenue_quarterly]
                                                            Total_Non_interest_revenue_quarterly_df = pd.DataFrame(Total_Non_interest_revenue_list_quarterly_billion,  index=date_list_annual, columns=["Non Interest Revenue"])
                                                            Total_Non_interest_revenue_quarterly_df =Total_Non_interest_revenue_quarterly_df.transpose()
                                                            #-------------------------------------------------------------

                                                            merged_df_banks = pd.concat([total_interest_expense_quarterly_df,total_interestincome_quarterly_df,Net_interest_Income_quarterly_df,Prov_Credit_losses_quarterly_df,Total_Non_interest_expenses_quarterly_df,Total_Non_interest_revenue_quarterly_df,net_income_quarterly_df,Pretax_income_quarterly_df,eps_basic_quarterly_df,shares_basic_quarterly_df,eps_diluted_quarterly_df,shares_diluted_quarterly_df])    

                                                            st.table(merged_df_banks.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))

                                                                      
                                                                      #st.dataframe(merged_df_banks.style.set_table_attributes('class="scroll-table"'),use_container_width=True)
                                                                 
                                                                 # st.markdown('<div style="margin-bottom: 100px;"></div>', unsafe_allow_html=True)   
                                                            pass
                                                       
                                                  # elif "Insurance" in Industry or "Health Care Providers & Services" in Industry :
                                                       except KeyError:
                                                                      try:
                                                                           Net_premiums_earned = annual_data['premiums_earned'][-10:] 
                                                                           Net_investment_income = annual_data['net_investment_income'][-10:] 
                                                                           Fees_and_other_income = annual_data['fees_and_other_income'][-10:] 
                                                                           Interest_Expense_insurance = annual_data['interest_expense_insurance'][-10:] 
                                                                           revenue_2013 = annual_data['revenue'][-10:] 
                                                                           Pretax_income_annual = annual_data['pretax_income'][-10:]
                                                                           net_income_annual = annual_data['net_income'][-10:] 
                                                                           eps_basic_annual = annual_data['eps_basic'][-10:]
                                                                           shares_basic_annual = annual_data['shares_basic'][-10:]
                                                                           eps_diluted_annual = annual_data['eps_diluted'][-10:]
                                                                           shares_diluted_annual = annual_data['shares_diluted'][-10:]
                                                                           Income_tax_annual = annual_data['income_tax'][-10:]

                                                                           Net_premiums_earned_list_billion = ["{:.2f}B".format(premiums_earned / 1000000000) if abs(premiums_earned) >= 1000000000 else "{:,.0f}M".format(premiums_earned / 1000000) for premiums_earned in Net_premiums_earned]
                                                                           net_premiums_earned_df = pd.DataFrame(Net_premiums_earned_list_billion, index=date_list_annual,  columns=["Net Premiums Earned"])
                                                                           net_premiums_earned_df = net_premiums_earned_df.transpose()
                                                                           #....................................................................................................
                                                                           #Net_investment_income = quarterly_data['net_investment_income'][-10:] 
                                                                      
                                                                           Net_investment_income_list_billion = ["{:.2f}B".format(net_investment_income / 1000000000) if abs(net_investment_income) >= 1000000000 else "{:,.0f}M".format(net_investment_income / 1000000) for net_investment_income in Net_investment_income]
                                                                           net_investment_income_df = pd.DataFrame(Net_investment_income_list_billion, index=date_list_annual,  columns=["Net Investment Income"])
                                                                           net_investment_income_df = net_investment_income_df.transpose()
                                                                           #....................................................................................................
                                                                                #Fees_and_other_income = quarterly_data['fees_and_other_income'][-10:] 
                                                                           
                                                                           Fees_and_other_income_list_billion = ["{:.2f}B".format(fees_and_other_income / 1000000000) if abs(fees_and_other_income) >= 1000000000 else "{:,.0f}M".format(fees_and_other_income / 1000000) for fees_and_other_income in Fees_and_other_income]
                                                                           Fees_and_other_income_df = pd.DataFrame(Fees_and_other_income_list_billion, index=date_list_annual,  columns=["Fees And Other Income"])
                                                                           Fees_and_other_income_df = Fees_and_other_income_df.transpose()
                                                                           #....................................................................................................
                                                                           #Interest_Expense_insurance = quarterly_data['interest_Expense_insurance'][-10:] 
                                                                           Interest_Expense_insurance_list_billion = ["{:.2f}B".format(interest_expense_insurance / 1000000000) if abs(interest_expense_insurance) >= 1000000000 else "{:,.0f}M".format(interest_expense_insurance / 1000000) for interest_expense_insurance in Interest_Expense_insurance]
                                                                           Interest_Expense_insurance_df = pd.DataFrame(Interest_Expense_insurance_list_billion, index=date_list_annual,  columns=["Interest Expense"])
                                                                           Interest_Expense_insurance_df = Interest_Expense_insurance_df.transpose()
                                                                           
                                                                           #....................................................................................................
                                                                           revenue_list_billion = ["{:.2f}B".format(revenue / 1000000000) if abs(revenue) >= 1000000000 else "{:,.0f}M".format(revenue / 1000000) for revenue in revenue_2013]
                                                                           revenue_df = pd.DataFrame(revenue_list_billion, index=date_list_annual,  columns=["Total Revenue"])
                                                                           revenue_df = revenue_df.transpose()
                                                                           
                                                                           #..........................................................................................................................................
                                                                           Pretax_income_table = ["{:.2f}B".format(pretax_income / 1000000000) if abs(pretax_income) >= 1000000000 else "{:,.0f}M".format(pretax_income / 1000000) for pretax_income in Pretax_income_annual]
                                                                           Pretax_income_df = pd.DataFrame(Pretax_income_table, index=date_list_annual,  columns=["Pre-Tax Income"])
                                                                           Pretax_income_df = Pretax_income_df.transpose()
                                                            #----------------------------------------------------------------    
                                                                 
                                                                           net_income_table = ["{:.2f}B".format(net_income / 1000000000) if abs(net_income) >= 1000000000 else "{:,.0f}M".format(net_income / 1000000) for net_income in net_income_annual]
                                                                           net_income_df = pd.DataFrame(net_income_table, index=date_list_annual,  columns=["Net Income"])
                                                                           net_income_df = net_income_df.transpose()
                                                            #----------------------------------------------------------------   
                                                                           eps_basic_table = ["{:.2f}".format(eps_basic) for eps_basic in eps_basic_annual]
                                                                           #eps_basic_table = [int(eps_basic) for eps_basic in eps_basic_annual]
                                                                           eps_basic_df = pd.DataFrame(eps_basic_table, index=date_list_annual,  columns=["EPS(basic)"])
                                                                           eps_basic_df = eps_basic_df.transpose()
                                                            #----------------------------------------------------------------    
                                                                           shares_basic_table = ["{:.2f}B".format(shares_basic / 1000000000) if shares_basic >= 1000000000 else "{:,.0f}M".format(shares_basic / 1000000) for shares_basic in shares_basic_annual]
                                                                           shares_basic_df = pd.DataFrame(shares_basic_table, index=date_list_annual,  columns=["Basic Shares Outstanding"])
                                                                           shares_basic_df = shares_basic_df.transpose()
                                                            #----------------------------------------------------------------    
                                                                           eps_diluted_table = ["{:.2f}".format(eps_diluted / 1) for eps_diluted in eps_diluted_annual]
                                                                           eps_diluted_df = pd.DataFrame(eps_diluted_table, index=date_list_annual,  columns=["EPS(diluted)"])
                                                                           eps_diluted_df = eps_diluted_df.transpose()
                                                            #----------------------------------------------------------------    
                                                                           shares_diluted_table = ["{:.2f}B".format(shares_diluted / 1000000000) if shares_diluted >= 1000000000 else "{:,.0f}M".format(shares_diluted / 1000000) for shares_diluted in shares_diluted_annual]
                                                                           shares_diluted_df = pd.DataFrame(shares_diluted_table, index=date_list_annual,  columns=["Diluted Shares Outstanding"])
                                                                           shares_diluted_df = shares_diluted_df.transpose()
                                                       
                                                                           merged_df_insurance = pd.concat([net_premiums_earned_df,net_investment_income_df,Fees_and_other_income_df,revenue_df,Interest_Expense_insurance_df,Pretax_income_df,net_income_df,eps_basic_df,shares_basic_df,eps_diluted_df,shares_diluted_df]) 
                                                  
                                                                           st.table(merged_df_insurance.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))

                                                                           #st.dataframe(merged_df_insurance.style.set_table_attributes('class="scroll-table"'),use_container_width=True)

                                                                           #st.markdown('<div style="margin-bottom: 100px;"></div>', unsafe_allow_html=True) 
                                                                           
                                                                      except KeyError:


               #                                                             revenue_2013 = quarterly_data['revenue'][-10:] 
               #                                                             Pretax_income_annual = quarterly_data['pretax_income'][-10:]
               #                                                             eps_basic_annual = quarterly_data['eps_basic'][-10:]
               #                                                             shares_basic_annual = quarterly_data['shares_basic'][-10:]
               #                                                             eps_diluted_annual = quarterly_data['eps_diluted'][-10:]
               #                                                             shares_diluted_annual = quarterly_data['shares_diluted'][-10:]
               #                                                             Income_tax_annual = quarterly_data['income_tax'][-10:]
               #                                                             net_income_annual = quarterly_data['net_income'][-10:]
               #                                                             cogs_list = quarterly_data['cogs'][-10:]
               #                                                             gross_profit_2013 = quarterly_data['gross_profit'][-10:]
               #                                                             SGA_Expense_annual = quarterly_data['total_opex'][-10:]
               #                                                             Research_Dev_annual = quarterly_data['rnd'][-10:]
               #                                                             interest_expense_list = quarterly_data['interest_expense'][-10:]
               #                                                             #Total_interest_income_list = annual_data['total_interest_income'][-10:]
               #                                                             interest_income_list = quarterly_data['interest_income'][-10:]
               #                                                             Ebita_annual = quarterly_data['ebitda'][-10:]
               #                                                             operating_income_list = quarterly_data['operating_income'][-10:]  
               # #....................................................................................................
               #                                                             revenue_list_billion = ["{:.2f}B".format(revenue / 1000000000) if abs(revenue) >= 1000000000 else "{:,.0f}M".format(revenue / 1000000) for revenue in revenue_2013]
               #                                                             revenue_df = pd.DataFrame(revenue_list_billion, index=date_list_quarter,  columns=["Revenue"])
               #                                                             revenue_df = revenue_df.transpose()

               #                                              #-----------------------------------------------------------
               #                                              # Convert cogs values to billion USD and round to 3 decimal places
               #                                                             #cogs_list_billion = ["{:.2f}B".format(cogs / 1000000000) for cogs in cogs_list]
               #                                                             cogs_list_billion = ["{:.2f}B".format(cogs / 1000000000) if abs(cogs) >= 1000000000 else "{:,.0f}M".format(cogs / 1000000) for cogs in cogs_list]
               #                                                             cogs_df = pd.DataFrame(cogs_list_billion,  index=date_list_quarter, columns=["Cost of Goods Sold"])
               #                                                             cogs_df = cogs_df.transpose()
               #                                              #----------------------------------------------------------
               #                                              # Convert gross profit values to billion USD and round to 3 decimal places
               #                                                             gross_profit_list_billion = ["{:.2f}B".format(gross_profit / 1000000000) if abs(gross_profit) >= 1000000000 else "{:,.0f}M".format(gross_profit / 1000000) for gross_profit in gross_profit_2013]
               #                                                             gross_profit_df = pd.DataFrame(gross_profit_list_billion, index=date_list_quarter,  columns=["Gross Profit"])
               #                                                             gross_profit_df = gross_profit_df.transpose()
               #                                              #----------------------------------------------------------------

               #                                                             SGA_Expense_table = ["{:.2f}B".format(total_opex / 1000000000) if abs(total_opex) >= 1000000000 else "{:,.0f}M".format(total_opex / 1000000) for total_opex in SGA_Expense_annual]
               #                                                             SGA_Expense_df = pd.DataFrame(SGA_Expense_table, index=date_list_quarter,  columns=["Operating Expense"])
               #                                                             SGA_Expense_df = SGA_Expense_df.transpose()
               #                                              #----------------------------------------------------------------
               #                                                             Research_Dev_table = ["{:.2f}B".format(rnd / 1000000000) if abs(rnd) >= 1000000000 else "{:,.0f}M".format(rnd / 1000000) for rnd in Research_Dev_annual]
               #                                                             Research_Dev_df = pd.DataFrame(Research_Dev_table, index=date_list_quarter,  columns=["Research & Development"])
               #                                                             Research_Dev_df = Research_Dev_df.transpose()
               #                                              #----------------------------------------------------------------    
               #                                                             interestexpense_list_billion = ["{:.2f}B".format(interest_expense / -1000000000) if abs(interest_expense) >= 1000000000 else "{:,.0f}M".format(interest_expense / -1000000) for interest_expense in interest_expense_list]
               #                                                             interestexxpense_df = pd.DataFrame(interestexpense_list_billion, index=date_list_quarter, columns=["Interest Expense"])                                   
               #                                                             interestexxpense_df = interestexxpense_df.transpose()                                                                  
               #                                              # -------------------------------------------------------------------
               #                                                             Pretax_income_table = ["{:.2f}B".format(pretax_income / 1000000000) if abs(pretax_income) >= 1000000000 else "{:,.0f}M".format(pretax_income / 1000000) for pretax_income in Pretax_income_annual]
               #                                                             Pretax_income_df = pd.DataFrame(Pretax_income_table, index=date_list_quarter,  columns=["Pre-Tax Income"])
               #                                                             Pretax_income_df = Pretax_income_df.transpose()
               #                                              #----------------------------------------------------------------    
               #                                                             Income_tax_table = ["{:.2f}B".format(income_tax / -1000000000) if abs(income_tax) >= 1000000000 else "{:,.0f}M".format(income_tax / -1000000) for income_tax in Income_tax_annual]
               #                                                             Income_tax_df = pd.DataFrame(Income_tax_table, index=date_list_quarter,  columns=["Income Tax"])
               #                                                             Income_tax_df = Income_tax_df.transpose()
               #                                              #----------------------------------------------------------------       
               #                                                             net_income_table = ["{:.2f}B".format(net_income / 1000000000) if abs(net_income) >= 1000000000 else "{:,.0f}M".format(net_income / 1000000) for net_income in net_income_annual]
               #                                                             net_income_df = pd.DataFrame(net_income_table, index=date_list_quarter,  columns=["Net Income"])
               #                                                             net_income_df = net_income_df.transpose()
               #                                              #----------------------------------------------------------------   
               #                                                             eps_basic_table = ["{:.2f}".format(eps_basic) for eps_basic in eps_basic_annual]
               #                                                             #eps_basic_table = [int(eps_basic) for eps_basic in eps_basic_annual]
               #                                                             eps_basic_df = pd.DataFrame(eps_basic_table, index=date_list_quarter,  columns=["EPS(basic)"])
               #                                                             eps_basic_df = eps_basic_df.transpose()
               #                                              #----------------------------------------------------------------    
               #                                                             shares_basic_table = ["{:.2f}B".format(shares_basic / 1000000000) if shares_basic >= 1000000000 else "{:,.0f}M".format(shares_basic / 1000000) for shares_basic in shares_basic_annual]
               #                                                             shares_basic_df = pd.DataFrame(shares_basic_table, index=date_list_quarter,  columns=["Basic Shares Outstanding"])
               #                                                             shares_basic_df = shares_basic_df.transpose()
               #                                              #----------------------------------------------------------------    
               #                                                             eps_diluted_table = ["{:.2f}".format(eps_diluted / 1) for eps_diluted in eps_diluted_annual]
               #                                                             eps_diluted_df = pd.DataFrame(eps_diluted_table, index=date_list_quarter,  columns=["EPS(diluted)"])
               #                                                             eps_diluted_df = eps_diluted_df.transpose()
               #                                              #----------------------------------------------------------------    
               #                                                             shares_diluted_table = ["{:.2f}B".format(shares_diluted / 1000000000) if shares_diluted >= 1000000000 else "{:,.0f}M".format(shares_diluted / 1000000) for shares_diluted in shares_diluted_annual]
               #                                                             shares_diluted_df = pd.DataFrame(shares_diluted_table, index=date_list_quarter,  columns=["Diluted Shares Outstanding"])
               #                                                             shares_diluted_df = shares_diluted_df.transpose()
               #                                              #----------------------------------------------------------------      
               #                                                             Ebitda_table = ["{:.2f}B".format(ebitda / 1000000000) if abs(ebitda) >= 1000000000 else "{:,.0f}M".format(ebitda / 1000000) for ebitda in Ebita_annual]
               #                                                             Ebitda_df = pd.DataFrame(Ebitda_table, index=date_list_quarter,  columns=["EBITDA"])
               #                                                             Ebitda_df = Ebitda_df.transpose()
               #                                              #----------------------------------------------------------------                                    
               #                                                             operatingincome_list_billion = ["{:.2f}B".format(operating_income / 1000000000) if abs(operating_income) >= 1000000000 else "{:,.0f}M".format(operating_income / 1000000) for operating_income in operating_income_list]
               #                                                             operatingincome_df = pd.DataFrame(operatingincome_list_billion,  index=date_list_quarter, columns=["Operating Income"])
               #                                                             operatingincome_df = operatingincome_df.transpose()
               #                                              #-------------------------------------------------------------

               #                                              # Convert interest income values to billion USD and round to 3 decimal places
               #                                                             interestincome_list_billion = ["{:.2f}B".format(interest_income / 1000000000) if abs(interest_income) >= 1000000000 else "{:,.0f}M".format(interest_income / 1000000) for interest_income in interest_income_list]
               #                                                             interestincome_df = pd.DataFrame(interestincome_list_billion,  index=date_list_quarter, columns=["Non-Operating Interest Income"])
               #                                                             interestincome_df = interestincome_df.transpose()
               #                                                   #------------------------------------------------------------

                                                                           
               #                                                             merged_df_insurance = pd.concat([revenue_df,cogs_df, gross_profit_df,SGA_Expense_df, Research_Dev_df,interestincome_df,interestexxpense_df,Pretax_income_df,Income_tax_df,net_income_df,eps_basic_df,shares_basic_df,eps_diluted_df,shares_diluted_df,Ebitda_df])  
                                                                           
               #                                                             st.table(merged_df_insurance.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))
          
                                                                           pass
                                                       #else:
                                                       try:          #st.write("no")       
                                                            revenue_2013 = annual_data['revenue'][-10:] 
                                                            Pretax_income_annual = annual_data['pretax_income'][-10:]
                                                            eps_basic_annual = annual_data['eps_basic'][-10:]
                                                            shares_basic_annual = annual_data['shares_basic'][-10:]
                                                            eps_diluted_annual = annual_data['eps_diluted'][-10:]
                                                            shares_diluted_annual = annual_data['shares_diluted'][-10:]
                                                            Income_tax_annual = annual_data['income_tax'][-10:]
                                                            net_income_annual = annual_data['net_income'][-10:]
                                                            cogs_list = annual_data['cogs'][-10:]
                                                            gross_profit_2013 = annual_data['gross_profit'][-10:]
                                                            SGA_Expense_annual = annual_data['total_opex'][-10:]
                                                            Research_Dev_annual = annual_data['rnd'][-10:]
                                                            interest_expense_list = annual_data['interest_expense'][-10:]
                                                                      #Total_interest_income_list = annual_data['total_interest_income'][-10:]
                                                            interest_income_list = annual_data['interest_income'][-10:]
                                                            Ebita_annual = annual_data['ebitda'][-10:]
                                                            operating_income_list = annual_data['operating_income'][-10:]                                   
                                                       #....................................................................................................
                                                            revenue_list_billion = ["{:.2f}B".format(revenue / 1000000000) if abs(revenue) >= 1000000000 else "{:,.0f}M".format(revenue / 1000000) for revenue in revenue_2013]
                                                            revenue_df = pd.DataFrame(revenue_list_billion, index=date_list_annual,  columns=["Revenue"])
                                                            revenue_df = revenue_df.transpose()

                                                       #-----------------------------------------------------------
                                                       # Convert cogs values to billion USD and round to 3 decimal places
                                                                      #cogs_list_billion = ["{:.2f}B".format(cogs / 1000000000) for cogs in cogs_list]
                                                            cogs_list_billion = ["{:.2f}B".format(cogs / 1000000000) if abs(cogs) >= 1000000000 else "{:,.0f}M".format(cogs / 1000000) for cogs in cogs_list]
                                                            cogs_df = pd.DataFrame(cogs_list_billion,  index=date_list_annual, columns=["Cost of Goods Sold"])
                                                            cogs_df = cogs_df.transpose()
                                                       #----------------------------------------------------------
                                                       # Convert gross profit values to billion USD and round to 3 decimal places
                                                            gross_profit_list_billion = ["{:.2f}B".format(gross_profit / 1000000000) if abs(gross_profit) >= 1000000000 else "{:,.0f}M".format(gross_profit / 1000000) for gross_profit in gross_profit_2013]
                                                            gross_profit_df = pd.DataFrame(gross_profit_list_billion, index=date_list_annual,  columns=["Gross Profit"])
                                                            gross_profit_df = gross_profit_df.transpose()
                                                       #----------------------------------------------------------------

                                                            SGA_Expense_table = ["{:.2f}B".format(total_opex / 1000000000) if abs(total_opex) >= 1000000000 else "{:,.0f}M".format(total_opex / 1000000) for total_opex in SGA_Expense_annual]
                                                            SGA_Expense_df = pd.DataFrame(SGA_Expense_table, index=date_list_annual,  columns=["Operating Expense"])
                                                            SGA_Expense_df = SGA_Expense_df.transpose()
                                                       #----------------------------------------------------------------
                                                            Research_Dev_table = ["{:.2f}B".format(rnd / 1000000000) if abs(rnd) >= 1000000000 else "{:,.0f}M".format(rnd / 1000000) for rnd in Research_Dev_annual]
                                                            Research_Dev_df = pd.DataFrame(Research_Dev_table, index=date_list_annual,  columns=["Research & Development"])
                                                            Research_Dev_df = Research_Dev_df.transpose()
                                                       #----------------------------------------------------------------    
                                                            interestexpense_list_billion = ["{:.2f}B".format(interest_expense / -1000000000) if abs(interest_expense) >= 1000000000 else "{:,.0f}M".format(interest_expense / -1000000) for interest_expense in interest_expense_list]
                                                            interestexxpense_df = pd.DataFrame(interestexpense_list_billion, index=date_list_annual, columns=["Interest Expense"])                                   
                                                            interestexxpense_df = interestexxpense_df.transpose()                                                                  
                                                       # -------------------------------------------------------------------
                                                            Pretax_income_table = ["{:.2f}B".format(pretax_income / 1000000000) if abs(pretax_income) >= 1000000000 else "{:,.0f}M".format(pretax_income / 1000000) for pretax_income in Pretax_income_annual]
                                                            Pretax_income_df = pd.DataFrame(Pretax_income_table, index=date_list_annual,  columns=["Pre-Tax Income"])
                                                            Pretax_income_df = Pretax_income_df.transpose()
                                                       #----------------------------------------------------------------    
                                                            Income_tax_table = ["{:.2f}B".format(income_tax / -1000000000) if abs(income_tax) >= 1000000000 else "{:,.0f}M".format(income_tax / -1000000) for income_tax in Income_tax_annual]
                                                            Income_tax_df = pd.DataFrame(Income_tax_table, index=date_list_annual,  columns=["Income Tax"])
                                                            Income_tax_df = Income_tax_df.transpose()
                                                       #----------------------------------------------------------------       
                                                            net_income_table = ["{:.2f}B".format(net_income / 1000000000) if abs(net_income) >= 1000000000 else "{:,.0f}M".format(net_income / 1000000) for net_income in net_income_annual]
                                                            net_income_df = pd.DataFrame(net_income_table, index=date_list_annual,  columns=["Net Income"])
                                                            net_income_df = net_income_df.transpose()
                                                       #----------------------------------------------------------------   
                                                            eps_basic_table = ["{:.2f}".format(eps_basic) for eps_basic in eps_basic_annual]
                                                                      #eps_basic_table = [int(eps_basic) for eps_basic in eps_basic_annual]
                                                            eps_basic_df = pd.DataFrame(eps_basic_table, index=date_list_annual,  columns=["EPS(basic)"])
                                                            eps_basic_df = eps_basic_df.transpose()
                                                       #----------------------------------------------------------------    
                                                            shares_basic_table = ["{:.2f}B".format(shares_basic / 1000000000) if shares_basic >= 1000000000 else "{:,.0f}M".format(shares_basic / 1000000) for shares_basic in shares_basic_annual]
                                                            shares_basic_df = pd.DataFrame(shares_basic_table, index=date_list_annual,  columns=["Basic Shares Outstanding"])
                                                            shares_basic_df = shares_basic_df.transpose()
                                                       #----------------------------------------------------------------    
                                                            eps_diluted_table = ["{:.2f}".format(eps_diluted / 1) for eps_diluted in eps_diluted_annual]
                                                            eps_diluted_df = pd.DataFrame(eps_diluted_table, index=date_list_annual,  columns=["EPS(diluted)"])
                                                            eps_diluted_df = eps_diluted_df.transpose()
                                                       #----------------------------------------------------------------    
                                                            shares_diluted_table = ["{:.2f}B".format(shares_diluted / 1000000000) if shares_diluted >= 1000000000 else "{:,.0f}M".format(shares_diluted / 1000000) for shares_diluted in shares_diluted_annual]
                                                            shares_diluted_df = pd.DataFrame(shares_diluted_table, index=date_list_annual,  columns=["Diluted Shares Outstanding"])
                                                            shares_diluted_df = shares_diluted_df.transpose()
                                                       #----------------------------------------------------------------      
                                                            Ebitda_table = ["{:.2f}B".format(ebitda / 1000000000) if abs(ebitda) >= 1000000000 else "{:,.0f}M".format(ebitda / 1000000) for ebitda in Ebita_annual]
                                                            Ebitda_df = pd.DataFrame(Ebitda_table, index=date_list_annual,  columns=["EBITDA"])
                                                            Ebitda_df = Ebitda_df.transpose()
                                                       #----------------------------------------------------------------                                    
                                                            operatingincome_list_billion = ["{:.2f}B".format(operating_income / 1000000000) if abs(operating_income) >= 1000000000 else "{:,.0f}M".format(operating_income / 1000000) for operating_income in operating_income_list]
                                                            operatingincome_df = pd.DataFrame(operatingincome_list_billion,  index=date_list_annual, columns=["Operating Income"])
                                                            operatingincome_df = operatingincome_df.transpose()
                                                       #-------------------------------------------------------------

                                                       # Convert interest income values to billion USD and round to 3 decimal places
                                                            interestincome_list_billion = ["{:.2f}B".format(interest_income / 1000000000) if abs(interest_income) >= 1000000000 else "{:,.0f}M".format(interest_income / 1000000) for interest_income in interest_income_list]
                                                            interestincome_df = pd.DataFrame(interestincome_list_billion,  index=date_list_annual, columns=["Non-Operating Interest Income"])
                                                            interestincome_df = interestincome_df.transpose()
                                                            #------------------------------------------------------------

                                                            merged_df = pd.concat([revenue_df,cogs_df, gross_profit_df,SGA_Expense_df, Research_Dev_df,interestincome_df,interestexxpense_df,Pretax_income_df,Income_tax_df,net_income_df,eps_basic_df,shares_basic_df,eps_diluted_df,shares_diluted_df,Ebitda_df])  
                                                            st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))

                                                                      
                                                                      #st.dataframe(merged_df.style.set_table_attributes('class="scroll-table"'),use_container_width=True)
                                                                 
                                                                 # st.markdown('<div style="margin-bottom: 100px;"></div>', unsafe_allow_html=True)      
                                                       
                                                            pass
                                                       except KeyError:   

                                                            st.write()
                                                            pass  

     #pillar_analysis_width = 1  # Adjust this value as needed

     # Apply custom CSS style to control the width of the content
     #pillar_analysis_style = f"width: {pillar_analysis_width * 100}%;"
with st.container():
     with Pillar_Analysis: 
          #st.markdown("### Pillar Analysis", unsafe_allow_html=True)

          revenue_annual_funf = annual_data['revenue'][-5:] 
          ROIC_annual = annual_data['roic'][-10:]

          #ROIC_annual_funf =annual_data['roic'][-5:]
          #Average_ROIC_funf = round(((sum(ROIC_annual_funf) / len(ROIC_annual_funf)))*100, 2)
          Free_cash_flow_annual_one = annual_data['fcf'][-1:] 
          Free_cash_flow_annual_funf = annual_data['fcf'][-5:] 
          Total_assets_annual_one = annual_data['total_assets'][1:]
          Total_Equity_annual_one = annual_data['total_equity'][-1:]
          net_income_annual_funf = annual_data['net_income'][-5:] 
          shares_basic_annual_funf = annual_data['shares_basic'][-5:]
          try:
               debt_equity_annual_one =quarterly_data['debt_to_equity'][-1:]
               debt_Assets_annual =annual_data['debt_to_assets'][-10:]
               debt_Assets_annual_one =annual_data['debt_to_assets'][-1:]
               
               Free_cash_flow_annual_one = annual_data['fcf'][-1:] 
          
               
               LongTerm_debt_annual_one =annual_data['lt_debt'][-1:]
               Short_term_debt_annual_one =annual_data['st_debt'][-1:]
               Total_assets_annual_one = annual_data['total_assets'][-1:]
               interest_expense_yr =annual_data['interest_expense'][-1:]

          except KeyError:
               debt_equity_annual_one = pd.Series()
               debt_Assets_annual = pd.Series()
               debt_Assets_annual_one = pd.Series()
               interest_expense_yr=pd.Series()
           

          
          Cash_Dividends_paid_Total_annual_one = annual_data['cff_dividend_paid'][-1:] 
          Average_Cash_Dividends_paid_Total_annual_one = round(((sum(Cash_Dividends_paid_Total_annual_one) / len(Cash_Dividends_paid_Total_annual_one)))/1000000000, 2)

          Cash_Dividends_paid_Total_annual_five = annual_data['cff_dividend_paid'][-5:] 
          Average_Cash_Dividends_paid_Total_annual_five = round(((sum(Cash_Dividends_paid_Total_annual_five) / len(Cash_Dividends_paid_Total_annual_five)))/1000000000, 2)

          ROE_annual_five = annual_data['roe'][-5:] 
          Average_ROE_annual_five = round(((sum(ROE_annual_five) / len(ROE_annual_five)))*100,2)

          eps_basic_annual_five = annual_data['eps_basic'][-5:] 
          Average_eps_basic_annual_five = round(((sum(eps_basic_annual_five) / len(eps_basic_annual_five))),2)

          Total_Equity_quarter = quarterly_data['total_equity'][-1:]
          Total_Equity_quarter_average = round(((sum(Total_Equity_quarter) / len(Total_Equity_quarter))),3)
          




          Average_Free_cash_flow_annual_one = ((sum(Free_cash_flow_annual_one) / len(Free_cash_flow_annual_one)))/1000000000
          Average_Free_cash_flow_annual_one_one =Average_Free_cash_flow_annual_one

   
          #average_revenue_annual = round((sum(revenue_annual_funf) / len(revenue_annual_funf)) / 1000000000, 2)
          average_fcf_Annual_funf = ((sum(Free_cash_flow_annual_funf) / len(Free_cash_flow_annual_funf)) / 1000000000)
          Average_netIncome_annual = round((sum(net_income_annual_funf) / len(net_income_annual_funf)) / 1000000000, 2)
        
          Average_total_equity_annual = round((sum(Total_Equity_annual_one) / len(Total_Equity_annual_one)) / 1000000000, 2)

          
          
          Average_total_assets_one = round(((sum(Total_assets_annual_one) / len(Total_assets_annual_one))), 2)
          

          try:
               #debt_equity_annual_one =quarterly_data['debt_to_equity'][-1:]
               debt_equity_annual =annual_data['debt_to_equity'][-1:]
              
               Average_debt_equity_one = round((((sum(debt_equity_annual) / len(debt_equity_annual)))),2)
               
               Average_debt_assets_one = round(((sum(debt_Assets_annual_one) / len(debt_Assets_annual_one))), 2)

          except ZeroDivisionError:
               Average_debt_equity_one=0.00
               Average_debt_assets_one =0.00

          shares_basic_quarter = quarterly_data['shares_basic'][-1:]
          #DEBT_Equity = round(, 2)
          
          #Marketcap = current_price * shares_basic_quarter[0]/1000000000


          #st.write("Average_netIncome_annual",Average_netIncome_annual)
          

          #try:
               #one_FCF_annual_payout = round(abs(Average_Cash_Dividends_paid_Total_annual_one/Average_Free_cash_flow_annual_one)*100,2)

          if fcf_ttm == 0: 

                    #Average_Free_cash_flow_annual_one = 1
                    #Average_Free_cash_flow_annual_one = round(((sum(Free_cash_flow_annual_one) / len(Free_cash_flow_annual_one))), 2)
                    #Average_Cash_Dividends_paid_Total_annual_one = round(((sum(Cash_Dividends_paid_Total_annual_one) / len(Cash_Dividends_paid_Total_annual_one))), 2)
                    #Average_Cash_Dividends_paid_Total_annual_one = Average_Cash_Dividends_paid_Total_annual_one * 1000000000

                    fcf_ttm = 0

          else:
                    Dividend_ttm = Financial_data['ttm']['cff_dividend_paid']/1000000000  
                    fcf_ttm = Financial_data['ttm']['fcf']/1000000000  
                    #Dividend_ttm=sum(Dividend_ttm)/len(Dividend_ttm)
                    #fcf_ttm=sum(fcf_ttm)/len(fcf_ttm)

                    try:
                         one_FCF_annual_payout = round((abs(Dividend_ttm)/fcf_ttm)*100,2)

                    except ZeroDivisionError:
                          
                         one_FCF_annual_payout=0.00

          #except ZeroDivisionError:
                    #print("Index error occurred.")  # Handle the specific exception here

               
               
     #--------------------------------------------------------------------------------------------------------------------------------
          try:
               revenue_annual_funf_Growth =(revenue_annual_funf[-1]-revenue_annual_funf[-5])/abs(revenue_annual_funf[-5])*100

               if revenue_annual_funf[0] ==0:
                    revenue_annual_funf_Growth=0

          except (IndexError, ZeroDivisionError):
               revenue_annual_funf_Growth = 0
                                             
     #-----------------------------------------------------------------------------------------------------------------------------

          try:
               FCF_funf_growth = ((Free_cash_flow_annual_funf[-1]-Free_cash_flow_annual_funf[-5])/abs(Free_cash_flow_annual_funf[-5]))*100

               if Free_cash_flow_annual_funf[0] ==0:
                    FCF_funf_growth=0
          except (IndexError, ZeroDivisionError): 
               FCF_funf_growth=0                                 
     #----------------------------------------------------------------------------------------------------------------

          try:
               #for value in shares_basic_annual_funf:
               #    print(value(int[4]))
               Shares_outstanding_funf_growth = ((shares_basic_annual_funf[-1]-shares_basic_annual_funf[-5])/abs(shares_basic_annual_funf[-5]))*100
              # st.write(shares_basic_annual_funf[-5])
               #st.write(shares_basic_annual_funf[-1])
               if shares_basic_annual_funf[0] ==0:
                    
                    Shares_outstanding_funf_growth=0

          except (IndexError, ZeroDivisionError): 
               Shares_outstanding_funf_growth=0              
                                             
     #------------------------------------------------------------------------------------------------------------------

          try:
               netincome_annual_funf_growth_ = ((net_income_annual_funf[-1] - net_income_annual_funf[-5])/abs(net_income_annual_funf[-5]))*100

               if net_income_annual_funf[0] ==0:
                    netincome_annual_funf_growth =0
          except Exception as e:  

               netincome_annual_funf_growth_ =0    
     #...............................................................................................................................


     
     #...........................................................................................................
          #Netincome_annual_funf_Growth =round(((net_income_annual_funf[4]-net_income_annual_funf[0])/net_income_annual_funf[0])*100,2) 

          #Total_debt_assets= Average_debt_assets_one * Average_Total_assets_annual_one  


          Total_liabilities_quarter = quarterly_data['total_liabilities'][-1:]
          Average_Total_liabilities_quarter = sum(Total_liabilities_quarter)/len(Total_liabilities_quarter)

          if   Total_Debt_from_all_calc != 0:
               try:
                    Schuldentillgung = round(1 / (average_fcf_Annual_funf / Total_Debt_from_all_calc), 2)
                    Schuldentillgung = abs(Schuldentillgung)
               except Exception as e:
                     Schuldentillgung =0

               #print("Schuldentillgung",Schuldentillgung)
               #print("average_fcf_Annual_funf",average_fcf_Annual_funf)
               #print("Total_Debt_from_all_calc",Total_Debt_from_all_calc)


          elif Total_Debt_from_all_calc != 0:
               if Average_Total_liabilities_quarter != 0: 
                    Total_debt_= Average_Total_liabilities_quarter/1000000000
                    Schuldentillgung=round(1/(average_fcf_Annual_funf/Total_debt_),2)
                    Schuldentillgung = abs(Schuldentillgung)

               
          else:
               try:
                    Total_liabilities_annual = annual_data['total_liabilities'][-1:]
                    Total_liabilities_annual = sum(Total_liabilities_annual)/len(Total_liabilities_annual)
                    Total_debt_= Total_liabilities_annual/1000000000
                    Schuldentillgung=round(1/(average_fcf_Annual_funf/Total_debt_),2)

                    Schuldentillgung = abs(Schuldentillgung)
               except Exception as e:
                    Schuldentillgung = 0
          #Schuldentillgung=round(1/(average_fcf_Annual_funf/Total_debt),1)
          
          
          if KGV > 23:
                    pe = "-🔴"  # Red X for KCV greater than 23
          elif KGV < 0:
                    pe = "-🔴"  # Red X for KCV smaller than 0
          else:
                    pe = "✅"  # Green checkmark for KGV greater than or equal to 23

          
          if float(KCV) > 23.00:
                    pcf = "-🔴"  # Red X for KCV greater than 23
          elif float(KCV) < 0.00:
                    pcf = "-🔴"  # Red X for KCV smaller than 0
          else:
                    pcf= "✅"  # Green checkmark for KGV greater than or equal to 23
                    

          if float(five_ROE) < 14.00:
                    roe = "-🔴"  # Red X for KGV less than 23
          
          else:
                    roe= "✅"  # Green checkmark for KGV greater than or equal to 23          

          if float(five_yrs_Nettomarge) > 5:
                    
               netmarge = "✅"  
          else:
               netmarge = "-🔴"    


          if one_FCF_annual_payout > 60:
                    payout = "-🔴"  # Red X for KGV less than 23

          elif one_FCF_annual_payout < 0:
                    payout = "-🔴"  # Red X for KCV smaller than 0           
          else:
                    payout= "✅"  # Green checkmark for KGV greater than or equal to 23

          if netincome_annual_funf_growth_ < -1:
                    netincome = "-🔴"  # Red X for KGV less than 23
          else:
                    netincome= "✅"  # Green checkmark for KGV greater than or equal to 23


          if revenue_annual_funf_Growth < -1:
                    rev = "-🔴"  # Red X for KGV less than 23
          else:
                    rev= "✅"  # Green checkmark for KGV greater than or equal to 23


          if FCF_funf_growth < -1:
                    fcf = "-🔴"  # Red X for KGV less than 23
          else:
                    fcf= "✅"  # Green checkmark for KGV greater than or equal to 23


          if Shares_outstanding_funf_growth > 0:
                    share = "-🔴"  # Red X for KGV less than 23
          else:
                    share= "✅"  # Green checkmark for KGV greater than or equal to 23

          if Average_ROIC_funf == 'NA' or float(Average_ROIC_funf[:-1]) < 9:
                    roic = "-🔴"  # Red X for 'NA' or less than 9
          else:
                    roic= "✅"  # Green checkmark for KGV greater than or equal to 23

          if Average_debt_equity_one > 2:
                    dt_equt = "-🔴"  # Red X for KGV less than 23

          elif Average_debt_equity_one < 0:
               
               dt_equt = "-🔴"  # Red X for KGV less than 23

          else:
                    dt_equt= "✅"  # Gree

          if Schuldentillgung > 5:
               schuld = "-🔴"  # Red X for KGV less than 23
          elif Schuldentillgung < 0:
               
               schuld = "-🔴"  # Red X for KGV less than 23
          else:
                schuld= "✅"  # Gree


     
          # Create a red circle
     # Create a red circle image
          #st.write(Sculdentillgung)
          #st.write(LongTerm_debt_annual)
          col1, col2, col3, col4 = st.columns(4)

          col1.metric("5 YR P/E < 23", KGV,pe)
          col2.metric("5 YR P/FCF < 23", KCV, pcf)
          col3.metric("5 YR FCF / DEBT < 5",Schuldentillgung,schuld)
          col4.metric("DEBT / EQUITY < 2",Average_debt_equity_one,dt_equt)
     #      metrics_data = [
     #     {"": "5 Yr KGV < 23:", "Value 1": KGV, "Value 2": pe}
     


          
          col5, col6, col7, col8 = st.columns(4)

          if Average_ROIC_funf == 'NA':
               Average_ROIC_funf = 0.0
               

          col5.metric("5 YR ROIC > 9%",f"{Average_ROIC_funf}",roic)
          col6.metric("5 YR ROE > 14%", f"{five_Yrs_ROE:.5}%",roe)
          col7.metric("5 YR NET MARGIN > 5%", f"{five_yrs_Nettomarge}%", netmarge)
          col8.metric("FCF PAYOUT RATIO < 60 %",f"{one_FCF_annual_payout:.2f}%",payout)

          col9, col10, col11, col12 = st.columns(4)

          col9.metric("Revenue Growth 5 YR",f"{revenue_annual_funf_Growth:.2f}%",rev)
          col10.metric("Net Income Growth 5 YR",f"{netincome_annual_funf_growth_:.2f}%", netincome)
          col11.metric("FCF Growth 5 YR",f"{FCF_funf_growth:.2f}%",fcf)
          col12.metric("Shares Outstanding 5 YR",f"{Shares_outstanding_funf_growth:.2f}%",share)

          #if Average_ROIC_funf == 'NA' or float(Average_ROIC_funf[:-1]) < 9:
           #    roic_text = f"{Average_ROIC_funf[:-1]}% 🟢"  # Green circle for success
          #else:
           #    roic_text = f"{float(Average_ROIC_funf[:-1]):.2f}% ❌"  # Red circle for failure

#          col5, _ = st.columns(2)

#          with col5:
 #              st.metric("5 YR ROIC", roic_text)
          # Display the metric using col5.metric
          #col5.metric("5 YR ROIC", roic_text)
                    # col3.metric("5 YR ROIC", roic_text)
          # col2.metric("5 YR ROIC", roic_text)
          # col4.metric("5 YR ROIC", roic_text)


          # col5,col3,col2,col4 = st.columns(4)
          # # Display the metric using col5.metric
          # col5.metric("5 YR ROIC", roic_text)
          # col3.metric("5 YR ROIC", roic_text)
          # col2.metric("5 YR ROIC", roic_text)
          # col4.metric("5 YR ROIC", roic_text)
               # Convert data into DataFrames
          df1 = pd.DataFrame(data1).transpose()
          df2 = pd.DataFrame(data2).transpose()
          df3 = pd.DataFrame(data3).transpose()
          df4 = pd.DataFrame(data4).transpose()

          # Reset column index to start from 1
         # df1.columns = range(1, len(df1.columns) + 1)
          #df2.columns = range(2, len(df2.columns) + 2)
          #df3.columns = range(3, len(df3.columns) + 3)
          #df4.columns = range(4, len(df4.columns) + 4)
          
          df1 = df1.rename(columns={i: " " for i in df1.columns})
          df2 = df2.rename(columns={i: " " for i in df2.columns})
          df3 = df3.rename(columns={i: " " for i in df3.columns})
          df4 = df4.rename(columns={i: " " for i in df4.columns})
        
          #style = "color: #2E8B57"
          style = "color: #2E8B57; text-align: center"

          styled_df1 = df1.style.applymap(lambda x: style).set_caption("")
          styled_df2 = df2.style.applymap(lambda x: style).set_caption("")
          styled_df3 = df3.style.applymap(lambda x: style).set_caption("")
          styled_df4 = df4.style.applymap(lambda x: style).set_caption("")


          

          # Create a responsive layout with three columns
          #col1, col2, col3 = st.columns(3)
          col1, col2, col3, col4 = st.columns(4)

          # Display the dataframes in each column
          with col1.container():
               st.table(styled_df1)
          with col2.container():
               st.table(styled_df2)
          with col3.container():
               st.table(styled_df3)
          with col4.container():
               st.table(styled_df4)
                         




with st.container():   
     with Stock_Analyser:
          # Get the value at index 1 from the Series
          #10_years_treasury_yield= GOOGLEFINANCE("TNX")/10
     #      treasury = '^TNX'
     #      treasury_yield_data = yf.download(treasury, period='1d')
     #      treasury_yield = treasury_yield_data['Close'].iloc[-1]

     #      #Average_10years_treasury_rate = 4.25
     #      try:
     #     # Calculate b based on treasury_yield
     #           if treasury_yield == 0:
     #                Average_10years_treasury_rate =  4.25
     #           else:
                    
     #                Average_10years_treasury_rate = round(treasury_yield,2)
     #      except (ZeroDivisionError, TypeError):
     #           # Handle the case when treasury_yield is zero or causes an error
          
          treasury = "^TNX"
          #treasury_yield_data = yf.download(treasury, period='1d')
          treasury_yield_data = yf.download(treasury)
          

     # Check if the treasury_yield_data DataFrame is empty
          if not treasury_yield_data.empty:
               treasury_yield = treasury_yield_data['Close'].iloc[-1]
               Average_10years_treasury_rate = round(treasury_yield,2)
               #print("10-year Treasury yield:", treasury_yield)
          else:
               #print("Error: No price data found for the 10-year Treasury yield symbol.")
               Average_10years_treasury_rate = 4.25
          # Check if the treasury_yield_data DataFrame is empty


               # Display the value of b
          try:          
               interest_expense_annual_one = annual_data['interest_expense'][-1:]
               Average_interest_expense_annual_one = round(((sum(interest_expense_annual_one) / len(interest_expense_annual_one)))/-1000000000, 2)
          except Exception as e:     
               Average_interest_expense_annual_one=0.0



          
     # Average_eps_quarter = round(((sum(int(eps_basic_quarter[9])) / len(int(eps_basic_quarter[9])))), 2)
          #eps_basic_quarter = [int(eps_basic) for eps_basic in eps_basic_quarter]


          Average_stock_market_beta = float(beta)
               
          Market_return = 8.51
          #total =annual_data['fcf'][-1:]
          #average_fcf_Annual_one = round((sum(FCF_annual_one) / len(FCF_annual_one)) / 1000000000, 2)

          #cash_und_cash_investments_annual = annual_data['cash_and_equiv'][-1:]
          #st_investments_annual = annual_data['st_investments'][-1:]
          #sum_cash_and_equiv = sum(cash_und_cash_investments_annual)
          #sum_st_investments = sum(st_investments_annual)

          #total_cash = round((sum_cash_and_equiv + sum_st_investments)/1000000000,2)

          Income_tax_annual_one = annual_data['income_tax'][-1:]
          Average_Income_tax_annual_one = round(((sum(Income_tax_annual_one) / len(Income_tax_annual_one)))/-1000000000, 2)

          Pretax_income_annual_one = annual_data['pretax_income'][-1:]
          Average_Pretax_annual_one = round(((sum(Pretax_income_annual_one) / len(Pretax_income_annual_one)))/1000000000, 2)

          shares_basic_annual_one = annual_data['shares_basic'][-1:]
          Average_shares_basic_annual_one= round(((sum(shares_basic_annual_one) / len(shares_basic_annual_one)))/1000000000, 2)

          if Total_Debt_from_all_calc != 0:
               Cost_of_debt = round((Average_interest_expense_annual_one/Total_Debt_from_all_calc)*100,2)
               Cost_of_debt_with_percentage = f"{Cost_of_debt:.2f}%"     
          elif Total_debt_ !=0:
          # Cost_of_debt = 0
               Cost_of_debt = round((Average_interest_expense_annual_one/Total_debt_)*100,2)
               Cost_of_debt_with_percentage = f"{Cost_of_debt:.2f}%"

          else:
                Cost_of_debt =1
          try:
               Effective_tax_rate = round((Average_Income_tax_annual_one/Average_Pretax_annual_one)*100,2)
               Effective_tax_rate_with_percentage = f"{ Effective_tax_rate:.2f}%"

          except Exception as e:
               Income_tax_annual_one = annual_data['income_tax'][-1:]
               Average_Income_tax_annual_one = round(((sum(Income_tax_annual_one) / len(Income_tax_annual_one)))/-1, 2)
               Pretax_income_annual_one = annual_data['pretax_income'][-1:]
               Average_Pretax_annual_one = round(((sum(Pretax_income_annual_one) / len(Pretax_income_annual_one)))/1, 2)
               Effective_tax_rate = round((Average_Income_tax_annual_one/Average_Pretax_annual_one)*100,2)
               Effective_tax_rate=Effective_tax_rate/1000
               Effective_tax_rate_with_percentage = f"{ Effective_tax_rate:.2f}%"

               #st.write(Effective_tax_rate)

          Cost_of_debt_after_Tax =round((((Cost_of_debt)/100)* (1-(Effective_tax_rate/100))*100),2)
          Cost_of_debt_after_Tax_with_percentage = f"{ Cost_of_debt_after_Tax:.2f}%"



          Cost_of_equity = ((Average_10years_treasury_rate)+((Average_stock_market_beta)*(Market_return-Average_10years_treasury_rate)))
          Cost_of_equity = round(Cost_of_equity,2)
          Cost_of_equity_with_percentage = f"{Cost_of_equity}%"

          Pepetual_growth_rate = 0.025
          Growth_rate = 8.30
          Growth_rate_with_percentage = f"{Growth_rate:.2f}%"
          Growth_input = Growth_rate/100.00
          #average_fcf_Annual_one
          
          Total_Capital = Total_Debt_from_all_calc+Marketcap
          Total_debt_prozent =Total_Debt_from_all_calc/Total_Capital
          Marketcap_in_prozent =Marketcap/Total_Capital

          WACC = round(((Total_debt_prozent*Cost_of_debt_after_Tax))+(Marketcap_in_prozent*Cost_of_equity),3)

          if WACC <= 0:

               WACC = 9


          WACC_prozent= WACC

     #------------------------------------------------------Roic oder ROE vs Retention ratio oder sustainanble growth rate (SGR)---------------------------------------
          #Five_yrs_dividend_FCF_payout_ratio = (Average_Cash_Dividends_paid_Total_annual_one)*-1/average_FCF_annual_five

          #ROIC_Rention_ratio = (1-Five_yrs_dividend_FCF_payout_ratio)*Average_ROIC_funf

          #ROIC_Rention_ratio = (1-Five_yrs_dividend_FCF_payout_ratio)*Average_ROIC_funf
          #Payout_ratio_annual = annual_data['payout_ratio'][-1:]
          #Payout_ratio_annual =sum(Payout_ratio_annual)/len(Payout_ratio_annual)
          #Payout_ratio_annual =Payout_ratio_annual

          #Retention_ratio = (1-Payout_ratio_annual)

          #if Payout_ratio_annual==0.0:
          #    ROE_ttm_ohne_ =ROE_ttm_ohne/100
          #   Sustainable_growth_rate = ROE_ttm_ohne
          #else:

               #Retention_ratio=0
          #    ROE_ttm_ohne_ =ROE_ttm_ohne/100
          #   Sustainable_growth_rate = (ROE_ttm_ohne_*(1-Retention_ratio))*100


          #Sustainable_growth_rate = (roe*(1-retention_ratio)
          

          

          #Payout_ratio_annual = annual_data['payout_ratio'][-1:]
          #print("Payout_ratio_annual",Payout_ratio_annual)
          #print("ROE_ttm",ROE_ttm_ohne)
          #print("Retention_ratio",Retention_ratio)
          #print("Sustainable_growth_rate",Sustainable_growth_rate)
          #SGR=

     #-----------------------------------------------------Growth rate Estimate-----------------------------------------------------------------------------

          
          #col4.info(f"ROE_Retention_ratio: {ROE_Retention_ratio:.2f}%")
          
          #col50000000.info(f"Sustainable Growth Rate: {Sustainable_growth_rate:.2f}%")
          
          
     #---------------------------------------------------------------------------------------------------------------------
          # Display the inputs on the same row
        

          
    
          #print("Value at index 4:", value_at_index_4)
          #print("Value at index 9:", value_at_index_9)
          
          #print("EPS_CAGR:",EPS_CAGR)


     #........................................................................................................................


                 
     #-------------------------------   

          col1, col2,col3,col4,col5 = st.columns(5)

          col1.info(f"FCF 10 CAGR: {FCF_Cagr_10}%")
          col2.info(f"FCF 5 CAGR: {FCF_5_CAGR}%")
          col3.info(f"EPS 10 CAGR: {EPS_Cagr_10}%")
          col4.info(f"EPS 5 CAGR: {EPS_5_CAGR}%")
          col5.info(f"EPS next 5 YR: {Earnings_next_5_yrs}")
          


          col1,col2,col3,col4 = st.columns(4)

          # Display the values in colored boxes
          #col1.info(f"Cost of Capital (WACC): {WACC_prozent:.2f}%")
          #col1.info(f"EPS Growth YOY: {EPS_growth_10yrs}%")
          #col2.info(f"5 YR EPS Growth YOY: {EPS_growth_5yrs:.2f}%") 
          #col3.info(f"3 YR EPS Growth YOY: {EPS_growth_3years:.2f}%") 
          #col4.info(f" EPS Growth next 5YR : {Earnings_next_5_yrs}")


          col1,col2,col3 = st.columns(3)

          # Display the values in colored boxes
          #col1.info(f"Cost of Capital (WACC): {WACC_prozent:.2f}%")
          col1.info(f"Revenue Growth: {Revenue_Cagr_10}%")
          col2.info(f"5 YR Revenue: {Revenue_5_CAGR}%") 
          col3.info(f"1 YR Revenue Growth YOY: {Revenue_growth_1year:.2f}%")


          col1, col2,col3 = st.columns(3)
     # Display the values
     # Display the values
     # Display the values in colored boxes
          
          col1.info(f"FCF Growth YOY: {Average_fcf_growth_ten}%")
          col2.info(f"5 YR FCF Growth YOY: {Average_fcf_growth_five}")
          col3.info(f"3 YR FCF Growth YOY: {Average_fcf_growth_3years}")


          col1,col2,col5,col4= st.columns(4)
          col1.info(f"5 YR ROIC: {Average_ROIC_funf}%")
          col2.info(f"3 YR ROIC: {ROIC_annual_3years}")
          #col3.info(f"3 YR ROIC: {ROIC_annual_3years}")
          WACC = col5.number_input("WACC (%):", value=WACC)
          FCF_discount_in_years = col4.number_input("Years:", value=int(10))
          #Average_10years_treasury_rate = col6.number_input("10 YR T.NOTE:(%):", value=Average_10years_treasury_rate)
          
          
          
          
          
          #st.write(FCF_Cagr_10.2f}%)
     #------------------------------------------------------------------------------------------------------------------------
          col9, col10= st.columns(2)
          Growth_rate1 = col9.number_input("Growth Rate (Base Case) in %:", value=0.00,key="growth_rate1")
          Growth_rate2 = col10.number_input("Growth Rate (Bullish Case) in %:", value=0.00, key="growth_rate2")

     
     #---------------------------------------------------------Margin of Safety -------------------------------------------------------------

          cola, colb, colc= st.columns(3)
          #input_box9 = col9.text_input("1.Growth Estimate %:", value=Growth_rate_with_percentage)
          Margin_of_safety1 = cola.number_input("1.Margin of Safety (%):", value=9.00)
     # Margin_of_safety2 = colb.number_input("2.Margin of Safety %:", value=8.50)
          Margin_of_safety3 = colc.number_input("2.Margin of Safety (%):", value=9.00)
     #-------------------------------------------------------------------------------------------------------------------------------------------
          #print("last FCF:",Average_Free_cash_flow_annual_one_one)
          if Average_Free_cash_flow_annual_one_one < 0:
               Average_Free_cash_flow_annual_one_one = average_fcf_Annual_funf
          
          discounted_values = [] 
     
          for i in range(FCF_discount_in_years):
               discounted_value = Average_Free_cash_flow_annual_one_one * (1 + (Growth_rate1/100))
               Average_Free_cash_flow_annual_one_one = discounted_value
               #discounted_values.append(discounted_value)  # Add the discounted value to the list
               discounted_values.append(round(discounted_value, 2)) 
          #discounted_values[4]*
          sum_discounted_values = sum(discounted_values) 

          #Terminal_Value = discounted_values[4]*(1+Pepetual_growth_rate)/(WACC/100-Pepetual_growth_rate)
          for i, value in enumerate(discounted_values):
               if i == len(discounted_values) - 1:
                    Terminal_Value = value * (1 + Pepetual_growth_rate) / ((WACC/100) - Pepetual_growth_rate)
                    Sum_terminal_fcf = Terminal_Value + discounted_values[i]

      
          discounted_values[-1] = round(Sum_terminal_fcf,2)
          
          npv_result = npv(WACC/100,discounted_values)   
          rounded_npv_result = round(npv_result, 2)  
          #st.write(Total_Debt_from_all_calc)
          Equity_value = rounded_npv_result+Total_cash_last_years-Total_Debt_from_all_calc
          Intrinsic_value =Equity_value/Average_shares_basic_annual_one
          #st.write(npv_result)

          Euro_equivalent = Intrinsic_value*usd_to_eur_rate
               #print(f"{Intrinsic_value} USD is approximately {Euro_equivalent:.2f} EUR")
          # Display the result
          #print(f"{amount} {base_currency} is equal to {converted_amount} {target_currency}")
     # .   ....................................................................................   
          

     #----------------------------------------------------------2:Growth rate Estimate------------------------------------------------------------------------
          if Average_Free_cash_flow_annual_one < 0:
               Average_Free_cash_flow_annual_one = average_fcf_Annual_funf
     
          discounted_values2 = [] 
          # Create an empty list to store discounted values
          for j in range(FCF_discount_in_years):
               discounted_value2 = Average_Free_cash_flow_annual_one * (1 + (Growth_rate2/100))
               Average_Free_cash_flow_annual_one = discounted_value2
               discounted_values2.append(round(discounted_value2,2))  # Add the discounted value to the list
               #print(discounted_value2)
          #Terminal_Value2 = discounted_values2[4]*(1+Pepetual_growth_rate)/(WACC/100-Pepetual_growth_rate)

          sum_discounted_values2 = sum(discounted_values2)

          for i, value2 in enumerate(discounted_values2):
               if i == len(discounted_values2) - 1:
                    Terminal_Value2 = value2 * (1 + Pepetual_growth_rate) / ((WACC/100) - Pepetual_growth_rate)
                    Sum_terminal_fcf2 = Terminal_Value2 + discounted_values2[i]

      
          discounted_values2[-1] = Sum_terminal_fcf2

          #Sum_terminal_fcf2 = Terminal_Value2 + discounted_values2[4]

          discounted_values2[-1] = round(Sum_terminal_fcf2,2)
          npv_result2 = npv(WACC/100,discounted_values2)   
          rounded_npv_result2 = round(npv_result2, 2)  

          Equity_value2 = rounded_npv_result2+Total_cash_last_years-Total_Debt_from_all_calc
          Intrinsic_value2 =Equity_value2/Average_shares_basic_annual_one
          #st.write(npv_result)

          Euro_equivalent2 = Intrinsic_value2*usd_to_eur_rate
               #print(f"{Intrinsic_value2} USD is approximately {Euro_equivalent2:.2f} EUR")
          # Display the result

          # Display the result
          #print(f"{amount} {base_currency} is equal to {converted_amount} {target_currency}")
     # .   ....................................................................................   
     
     #...................................................................................................................................

          #print(f"The current 10-year Treasury yield is: {Average_10years_treasury_rate:.2f}")
     
          #------------------------------------------Graham 1.Estimate--------------------------------------------------------------

          if EPS_last_average < 0:
               EPS_last_average = Average_eps_basic_annual_five

          graham_valuation = (EPS_last_average * (7+1.5*Growth_rate1)*4.4)/(Average_10years_treasury_rate)
          
          Euro_equivalent_graham_valuation = graham_valuation*usd_to_eur_rate
               #print(f"{graham_valuation} USD is approximately {Euro_equivalent_graham_valuation:.2f} EUR")
          # Display the result
     # .   ...........................................Graham 2.Estimate.........................................   

          if EPS_last_average_one < 0:
               EPS_last_average_one = Average_eps_basic_annual_five
          graham_valuation2 = (EPS_last_average_one * (7+1.5*Growth_rate2)*4.4)/(Average_10years_treasury_rate)
        
          Euro_equivalent_graham_valuation2 = graham_valuation2*usd_to_eur_rate
               #print(f"{graham_valuation2} USD is approximately {Euro_equivalent_graham_valuation2:.2f} EUR")
          # Display the result
    

     #........................................................................................
     
          if Euro_equivalent_graham_valuation < 0:

               Euro_equivalent_graham_valuation = Euro_equivalent

          elif Euro_equivalent < 0:
               
               Euro_equivalent=Euro_equivalent_graham_valuation

          if Euro_equivalent_graham_valuation2 < 0:

               Euro_equivalent_graham_valuation2 = Euro_equivalent2

          elif Euro_equivalent2 < 0:
               Euro_equivalent2=Euro_equivalent_graham_valuation2

          Multiples_valuation1 =Euro_equivalent + Euro_equivalent_graham_valuation
         
          average_sum1 = Multiples_valuation1 / 2
          average_sum_both1 =  round(average_sum1*(1-Margin_of_safety1/100),2)
          
          #st.write(average_sum_both1,converted_amount)


          Multiples_valuation2 =Euro_equivalent2+Euro_equivalent_graham_valuation2
          average_sum2 = Multiples_valuation2 / 2
          average_sum_both2=average_sum2 *(1-Margin_of_safety3/100)

          #Middle_multiple_value = average_sum2+average_sum1
          #average_Middle_multiple_value =Middle_multiple_value/2
          #average_Middle_multiple_value=average_Middle_multiple_value*(1-Margin_of_safety2/100)
          Middle_multiple_value = average_sum_both1+average_sum_both2
          average_Middle_multiple_value =round(Middle_multiple_value/2,2)

          #Middle_DCF =Euro_equivalent+Euro_equivalent2
          #Average_Middle_DCF =Middle_DCF/2
          #Average_Middle_DCF=Average_Middle_DCF*(1-Margin_of_safety2/100)

          low_DCF=(Euro_equivalent*(1-Margin_of_safety1/100))
          high_DCF=(Euro_equivalent2*(1-Margin_of_safety3/100))

          Average_Middle_DCF=(low_DCF+high_DCF)/2

          #------------------------2 step--------------------------------
          #hier i found the average of graham+dcf.. next step, i also found the average of (graham+dcf)+dcf
          # Euro_equivalent=Euro_equivalent*(1-Margin_of_safety1/100)
          # Euro_equivalent2=Euro_equivalent2*(1-Margin_of_safety3/100)

          # average_sum_both1 =(average_sum_both1+Euro_equivalent)/2
          # average_sum_both2 =(average_sum_both2+Euro_equivalent2)/2
          # average_Middle_multiple_value =(average_Middle_multiple_value+Average_Middle_DCF)/2
          #.........................................................................................

          #Average_both_multiples =average_sum1+average_sum2
          #Average_both_multiples_sum = Average_both_multiples/2

          if st.button("Calculate", key="Calculate_DCF"):
               col11, col12,col13, col14= st.columns(4)
               #input_box9 = col9.text_input("1.Growth Estimate %:", value=Growth_rate_with_percentage)
               #col11.write(f'<span style=Current Price: &euro;"color: green;">; {converted_amount:.2f}</span>',unsafe_allow_html=True)
               col11.write(f'Current Price: <span style="color: green;">{converted_amount} &euro;</span>', unsafe_allow_html=True)

               col12.write(f"Low Estimate:")
               col13.write(f"Middle Estimate: ")
               col14.write(f"High Estimate:")


               col15, col16, col17, col18 = st.columns(4)

               # # Display number outputs for each estimate
               # col15.write(f" Multiple Valuation Method:  ")
               # col16.write(f"{average_sum_both1:.2f} €")
               # col17.write(f"{average_Middle_multiple_value:.2f} €")
               # col18.write(f"{average_sum_both2:.2f} €")
               
                              # Display number outputs for each estimate
               col15.write(f" Benjamin Graham + DCF:  ")
               #col16.write(f"{average_sum_both1:.2f} €")
               
               if average_sum_both1 > float(converted_amount):
                    font_color = "green"
               else:
                    font_color = "red"
               col16.write(f"<span style='color:{font_color}'>{average_sum_both1:.2f} €</span>", unsafe_allow_html=True)

               if average_Middle_multiple_value > float(converted_amount):
                         font_color = "green"
               else:
                    font_color = "red"
               #col17.write(f"{average_Middle_multiple_value:.2f} €")
               col17.write(f"<span style='color:{font_color}'>{average_Middle_multiple_value:.2f} €</span>", unsafe_allow_html=True)
               #col18.write(f"{average_sum_both2:.2f} €")
               

               if average_sum_both2 > float(converted_amount):
                         font_color = "green"
               else:
                    font_color = "red"
               col18.write(f"<span style='color:{font_color}'>{average_sum_both2:.2f} €</span>", unsafe_allow_html=True)

                    # Display number outputs for each estimate
               col19, col20, col21, col22 = st.columns(4)

               col19.write(f"Discounted Cash Flow Analysis (DCF):")
               #col20.write(f"{low_DCF:.2f} €")
               if low_DCF > float(converted_amount):
                         font_color = "green"
               else:
                    font_color = "red"
               col20.write(f"<span style='color:{font_color}'>{low_DCF:.2f} €</span>", unsafe_allow_html=True)
               #col21.write(f"{Average_Middle_DCF:.2f} €")

               if Average_Middle_DCF > float(converted_amount):
                         font_color = "green"
               else:
                    font_color = "red"
               col21.write(f"<span style='color:{font_color}'>{Average_Middle_DCF:.2f} €</span>", unsafe_allow_html=True)
               #col22.write(f"{high_DCF:.2f} €")

               if high_DCF > float(converted_amount):
                         font_color = "green"
               else:
                    font_color = "red"
               col22.write(f"<span style='color:{font_color}'>{high_DCF:.2f} €</span>", unsafe_allow_html=True)


with st.container():
     with Multiple_Valuation:
          #load = st.button ('')

          #st.session_state = False

          #Profit_Margin_10 = annual_data['fcf_margin'][-10:]
          #Profit_Margin_10=sum(Profit_Margin_10)/len(Profit_Margin_10)
          #Profit_Margin_10 = (Profit_Margin_10*100)

         # Profit_Margin_5 = annual_data['fcf_margin'][-5:]   
          #Profit_Margin_5 =sum(Profit_Margin_5)/len(Profit_Margin_5)
          #Profit_Margin_5 = (Profit_Margin_5*100)

          Profit_Margin_1 = annual_data['fcf_margin'][-1:]     
          Profit_Margin_1=sum(Profit_Margin_1)/len(Profit_Margin_1)
          Profit_Margin_1 = (Profit_Margin_1*100)

          col1,col2 = st.columns(2)

          # Display the values in colored boxes
          #col1.info(f"Cost of Capital (WACC): {WACC_prozent:.2f}%")
          with col1:
               st.write(f"Historical:")

          with col2:
               st.write(f"My Assumptions:")

          #with col2:
               My_assumption = st.number_input("Years:", value=int(10), key="My_assumption")

          col1,col2,col3,col4,col5,col6 = st.columns(6)

          # Display the values in colored boxes
          #col1.info(f"Cost of Capital (WACC): {WACC_prozent:.2f}%")
          with col1:
               st.write(f"1YR:")
          with col2:
               st.write(f"5YR:") 
          with col3:
               st.write(f"10YR:")
          with col4:
               st.write(f"LOW")
          with col5:
               st.write(f"MID") 
          with col6:
               st.write(f"HIGH")


          colr1,colr2,colr3,colr9,colr10,colr11 = st.columns(6)

          # Display the values in colored boxes
          #col1.info(f"Cost of Capital (WACC): {WACC_prozent:.2f}%")
          colr1.info(f"Revenue Growth: {Revenue_growth_1year:.2f}%")
          colr2.info(f"Revenue Growth: {Revenue_5_CAGR}%") 
          colr3.info(f"Revenue Growth: {Revenue_Cagr_10}%")

          
          #Growth_rate1 = col9.number_input("Wachstumsrate (Base Case) in %:", value=0.00, key="growth_rate1")

          coln1,coln2,coln3,coln9,coln10,coln11 = st.columns(6)

          # Display the values in colored boxes
          #col1.info(f"Cost of Capital (WACC): {WACC_prozent:.2f}%")
          coln1.info(f"Net Profit Margin: {Net_margin_ttm}") 
          coln2.info(f"Net Profit Margin: {five_yrs_Nettomarge}%") 
          coln3.info(f"Net Profit Margin: {Net_income_margin_10}%")


          colf1,colf2,colf3,colf9,colf10,colf11 = st.columns(6)

          # Display the values in colored boxes
          #col1.info(f"Cost of Capital (WACC): {WACC_prozent:.2f}%")
          colf1.info(f"FCF Margin: {FCF_Margin_1:.2f}%")
          colf2.info(f"FCF Margin: {FCF_Margin_5}%") 
          colf3.info(f"FCF Margin: {FCF_Margin_10}%")





         

          colcf1,colcf2,colcf3,colcf9,colcf10,colcf11 = st.columns(6)

          colcf1.info(f"Price/OCF: {P_OCF_ttm}")
          colcf2.info(f"Price/OCF: {P_OCF_5}") 
          colcf3.info(f"Price/OCF: {P_OCF_10}")



          colfcf1,colfcf2,colfcf3,colfcf9,colfcf10,colfcf11 = st.columns(6)

          colfcf1.info(f"Price/FCF: {pfcf_ttm}")
          colfcf2.info(f"Price/FCF: {pfcf_funf}") 
          colfcf3.info(f"Price/FCF: {pfcf_ten}")
          


          col1,col2,colx,cola, colb, colc= st.columns(6)
          col1.info('Margin Of Safety')
          col2.info('-')
          colx.info('-')
          colx.write(f"Multiple of Earnings Valuation:")



          #load =st.button('LOAD')
          #if "load_state" not in st.session_state:
           #    st.session_state.load_state =False

          
          Growth_rate_revenue_LOW = colr9.number_input(" ", value=0.00,key="Growth_rate_revenue_LOW")
          Growth_rate_revenue_middle = colr10.number_input(" ", value=0.00,key="Growth_rate_revenue_middle")
          Growth_rate_revenue_high = colr11.number_input(" ", value=0.00,key="Growth_rate_revenue_high")

          Growth_rate_net_profit_LOW = coln9.number_input(" ", value=0.00,key="Growth_rate_net_profit_LOW")
          Growth_rate__net_profit_middle = coln10.number_input(" ", value=0.00,key="Growth_rate__net_profit_middle")
          Growth_rate__net_profit_high = coln11.number_input(" ", value=0.00,key="Growth_rate__net_profit_high")

          Growth_rate_fcf_margin_LOW = colf9.number_input(" ", value=0.00,key="Growth_rate_fcf_margin_LOW")
          Growth_rate_fcf_margin_middle = colf10.number_input(" ", value=0.00,key="Growth_rate_fcf_margin_middle")
          Growth_rate_fcf_margin_high = colf11.number_input(" ", value=0.00,key="Growth_rate_fcf_margin_high")

          Growth_rate_P_OCF_low = colcf9.number_input(" ", value=0.00,key="Growth_rate_P_OCF_low")
          Growth_rate_P_OCF_middle = colcf10.number_input(" ", value=0.00,key="Growth_rate_P_OCF_middle")
          Growth_rate_P_OCF_high = colcf11.number_input(" ", value=0.00,key="Growth_rate_P_OCF_high")

          Growth_rate_P_FCF_low = colfcf9.number_input(" ", value=0.00,key="Growth_rate_P_FCF_low")
          Growth_rate_P_FCF_middle = colfcf10.number_input(" ", value=0.00,key="Growth_rate_P_FCF_middle")
          Growth_rate_P_FCF_high = colfcf11.number_input(" ", value=0.00,key="Growth_rate_P_FCF_high")

          #input_box9 = col9.text_input("1.Growth Estimate %:", value=Growth_rate_with_percentage)
          Margin_of_safety_low = cola.number_input(" ", value=9.00,key="Margin_of_safety_low")
          Margin_of_safety_mid = colb.number_input(" ", value=9.00,key="Margin_of_safety_mid")
          Margin_of_safety_high = colc.number_input(" ", value=9.00,key="Margin_of_safety_high")


          
# -----------------------------LOW-------------
          average_FCF_Profit_margin_low=((Growth_rate_fcf_margin_LOW+Growth_rate_net_profit_LOW)/2)/100

          average_PFCF_POCF_low=(Growth_rate_P_OCF_low+Growth_rate_P_FCF_low)/2

          Revenue_assumption_low=average_revenue_annual_ttm*pow(1+(Growth_rate_revenue_LOW/100),My_assumption)
          #st.write("average_revenue_annual_ttm",average_revenue_annual_ttm)
          #st.write("Revenue_assumption_low",Revenue_assumption_low)

          Assumption_low=(Revenue_assumption_low*average_FCF_Profit_margin_low)*average_PFCF_POCF_low
          #st.write("Assumption_low_all margins",Assumption_low)
          Assumption_low_inklu_shares_outstanding_low =Assumption_low/Average_shares_basic_annual_one
          #st.write("Assumption_low_inklu_shares_outstanding",Assumption_low_inklu_shares_outstanding_low)

          Assumption_low_inklu_shares_outstanding_MarginofSafety_low=Assumption_low_inklu_shares_outstanding_low*(1-(Margin_of_safety_low/100))
          #st.write("Assumption_low_inklu_shares_outstanding_MarginofSafety_low",Assumption_low_inklu_shares_outstanding_MarginofSafety_low)


          Revenue_low_Euro = "{:.2f}".format(Assumption_low_inklu_shares_outstanding_MarginofSafety_low*usd_to_eur_rate)
          #st.write(Revenue_low_Euro)
          #st.write(converted_amount)

# -----------------------------MIDDLE-------------
          average_FCF_Profit_margin_mid=((Growth_rate_fcf_margin_middle+Growth_rate__net_profit_middle)/2)/100

          average_PFCF_POCF_mid=(Growth_rate_P_OCF_middle+Growth_rate_P_FCF_middle)/2

          Revenue_assumption_mid=average_revenue_annual_ttm*pow(1+(Growth_rate_revenue_middle/100),My_assumption)
          #st.write("average_revenue_annual_ttm",average_revenue_annual_ttm)
          #st.write("Revenue_assumption_low",Revenue_assumption_mid)

          Assumption_mid=(Revenue_assumption_mid*average_FCF_Profit_margin_mid)*average_PFCF_POCF_mid

          Assumption_mid_inklu_shares_outstanding_mid =Assumption_mid/Average_shares_basic_annual_one
          #st.write("Assumption_low_inklu_shares_outstanding",Assumption_mid_inklu_shares_outstanding_mid)

          Assumption_mid_inklu_shares_outstanding_MarginofSafety_mid=Assumption_mid_inklu_shares_outstanding_mid*(1-(Margin_of_safety_mid/100))
          #st.write("Assumption_low_inklu_shares_outstanding_MarginofSafety_mid",Assumption_mid_inklu_shares_outstanding_MarginofSafety_mid)
      

          Revenue_mid_Euro = "{:.2f}".format(Assumption_mid_inklu_shares_outstanding_MarginofSafety_mid*usd_to_eur_rate)
          

          
# -----------------------------HIGH-------------

          average_FCF_Profit_margin_high=((Growth_rate_fcf_margin_high+Growth_rate__net_profit_high)/2)/100

          average_PFCF_POCF_high=(Growth_rate_P_OCF_high+Growth_rate_P_FCF_high)/2

          Revenue_assumption_high=average_revenue_annual_ttm*pow(1+(Growth_rate_revenue_high/100),My_assumption)
          #st.write("average_revenue_annual_ttm",average_revenue_annual_ttm)
          #st.write("Revenue_assumption_low",Revenue_assumption_high)

          Assumption_high=(Revenue_assumption_high*average_FCF_Profit_margin_high)*average_PFCF_POCF_high

          Assumption_high_inklu_shares_outstanding_high =Assumption_high/Average_shares_basic_annual_one
          #st.write("Assumption_low_inklu_shares_outstanding",Assumption_high_inklu_shares_outstanding_high)

          Assumption_high_inklu_shares_outstanding_MarginofSafety_high=Assumption_high_inklu_shares_outstanding_high*(1-(Margin_of_safety_high/100))
          #st.write("Assumption_high_inklu_shares_outstanding_MarginofSafety_high",Assumption_high_inklu_shares_outstanding_MarginofSafety_high)
        
          Revenue_high_Euro = "{:.2f}".format(Assumption_high_inklu_shares_outstanding_MarginofSafety_high*usd_to_eur_rate)
          

          

          col1.write(f'Current Price: <span style="color: green;">{converted_amount} &euro;</span>', unsafe_allow_html=True) 
                  
          st.markdown('</div>', unsafe_allow_html=True)

          #st.session_state = True
          with col1:
               if st.button("Calculate", key="Calculate_revenue"):
               #if load or st.session_state.load_state:
                #    st.session_state.load_state = True

                                  #input_box9 = col9.text_input("1.Growth Estimate %:", value=Growth_rate_with_percentage)
                              #col11.write(f'<span style=Current Price: &euro;"color: green;">; {converted_amount:.2f}</span>',unsafe_allow_html=True)
               
                    #colx.write(f"Multiples of Earnings Value:")
                    #col20.write(f"{low_DCF:.2f} €")
                    if float(Revenue_low_Euro) < float(converted_amount):
                         font_color = "red"
                    else:
                         font_color = "green"
                    cola.write(f"<span style='color:{font_color}'>{Revenue_low_Euro} €</span>", unsafe_allow_html=True)
                    #col21.write(f"{Average_Middle_DCF:.2f} €")

                    if float(Revenue_mid_Euro) < float(converted_amount):
                         font_color = "red"
                    else:
                         font_color = "green"
                    colb.write(f"<span style='color:{font_color}'>{Revenue_mid_Euro} €</span>", unsafe_allow_html=True)
                    #col22.write(f"{high_DCF:.2f} €")

                    if float(Revenue_high_Euro) < float(converted_amount):
                         font_color = "red"
                    else:
                         font_color = "green"
                    colc.write(f"<span style='color:{font_color}'>{Revenue_high_Euro} €</span>", unsafe_allow_html=True)


 #with st.container():
#      with EPS_Valuation:

#           Price_to_earnings = annual_data['price_to_earnings'][-5:]

#           high_PE_value = float(max(Price_to_earnings))
#           LOW_PE_value = float(min(Price_to_earnings))

          


#           col1,col2 = st.columns(2)

#           #col1.info("WACC",WACC_prozent)
#           #col1.write(f'WACC: {WACC_prozent}')

#           #col1.info(f"WACC: {WACC:.2f}%")
#           #col2.info(f"10 YR T.NOTE: {Average_10years_treasury_rate:.2f}%")


#           col1,col2,col3,col4,col5= st.columns(5)
         
#           EPS_ttm = col1.number_input("EPS:", value=eps_diluted_ttm)

#           HIGH_5years_PE = col2.number_input("5 Year HIGH PE:", value=high_PE_value)
#           LOW_5years_PE = col3.number_input("5 Year LOW PE:", value=LOW_PE_value)

#           average_value = (HIGH_5years_PE + LOW_5years_PE) / 2

#           Average_both_high_und_low_PE = col4.number_input("Average PE:", value=average_value)

#           Growth_rate = col5.number_input("Growth Rate(%):", value=0.00)
#           Growth_rate=Growth_rate/100

#           col1= st.columns(1)

#           Discount_rate = st.number_input("Discount Rate(%):", value=WACC)
#           Discount_rate=Discount_rate/100
#           Discount_rate=1+Discount_rate

#           col1= st.columns(1)
#           Years = st.number_input("Years:", value=10,key="Years")

#           Future_intrinsic =eps_diluted_ttm*((1 + Growth_rate) ** Years)*average_value
#           Present_intrinsic =Future_intrinsic/(Discount_rate) ** Years
         

#           col11= st.columns(1)
         
#           #Future_intrinsic_Value = col11.number_input("Future Intrinsic Value:", value=Future_intrinsic)
#           Future_intrinsic_Value = st.number_input("Future Intrinsic Value($):", value=Future_intrinsic)


#           col1= st.columns(1)
#           Present_intrinsic_Value = st.number_input("Present Iintrinsic Value($):", value=Present_intrinsic)

#           col1= st.columns(1)

#           Margin_of_safety = st.number_input("Margin of Safety(%):", value=0.00)
#           Margin_of_safety=(1-((Margin_of_safety)/100))

#           Buy_price_dollar =Present_intrinsic_Value*Margin_of_safety
          
#           try:
#                convert = requests.get(f"https://api.frankfurter.app/latest?amount={Buy_price_dollar}&from={base_currency}&to={target_currency}")
#                data14 = convert.json()
#                # Extract the converted amount from the response
#                Euro = data14['rates'][target_currency]
#                dollar = f"{Buy_price_dollar:.2f} $"
#                Buy_price_euro = Euro

#           except Exception as e:
#                #print("Error occurred. Using alternative conversion method.")Flax
#                c = CurrencyRates()
#                Buy_price_euro= c.convert("USD", "EUR", Buy_price_dollar)
#                #print(f"{graham_valuation2} USD is approximately {Euro_equivalent_graham_valuation2:.2f} EUR")
#           # Display the result
#      # .......................................DDM...................

#         #  print("Margin_of_safety",Margin_of_safety)

#           if st.button("Calculate"):
               
#                          #input_box9 = col9.text_input("1.Growth Estimate %:", value=Growth_rate_with_percentage)
#                          #col11.write(f'<span style=Current Price: &euro;"color: green;">; {converted_amount:.2f}</span>',unsafe_allow_html=True)
#                st.write(f'Current Price: <span style="color: green;">{converted_amount:.2f} &euro;</span>', unsafe_allow_html=True)

               

#                if converted_amount < Buy_price_euro:
#                     font_color = "green"
#                     st.write(f"Fair Value: <span style='color:{font_color}'>{Buy_price_euro:.2f} €</span>", unsafe_allow_html=True)

#                else:
#                     font_color = "red"

#                st.write(f"Fair Value: <span style='color:{font_color}'>{Buy_price_euro:.2f} €</span>", unsafe_allow_html=True)
                       
          



with st.container():              
     with Dividend_Discount_Model:

           # .......................................DDM..............................................  
          
          Dividend_annual = annual_data['dividends'][-4:]     
          Dividend_per_share_quarter = quarterly_data['dividends'][-14:]  
          Dividend_growth_quarter = quarterly_data['dividends_per_share_growth'][-14:]
          Dividend_current_dividend_growth_ttm=Dividend_current_dividend*4


          cola, colb, colc, cold,col2 = st.columns(5)

          percentage_increase_1_2 = 0
          percentage_increase_2_3 = 0
          percentage_increase_3_4 = 0
          percentage_increase_4_5 = 0

          for i in range(len(Dividend_per_share_quarter)):
               if i == 0:
                    Dividend_quarter1 = Dividend_per_share_quarter[i]
                    Dividend11 = cola.number_input("quarterly", value=round(Dividend_quarter1,3),key="unique_key1")
               elif i == 12 - 8:
                    Dividend_quarter2 = Dividend_per_share_quarter[i]
                    Dividend12 = colb.number_input("quarterly", value=Dividend_quarter2,key="unique_key2")
                    if Dividend_quarter1 != 0:
                         percentage_increase_1_2 = ((Dividend_quarter2 - Dividend_quarter1) / Dividend_quarter1) * 100
               elif i == 12-4:
                    Dividend_quarter3 = Dividend_per_share_quarter[i] 
                    Dividend13 = colc.number_input("quarterly", value=Dividend_quarter3,key="unique_key3")
                    if Dividend_quarter2 != 0:
                         percentage_increase_2_3 = ((Dividend_quarter3 - Dividend_quarter2) / Dividend_quarter2) * 100
               elif i == 12:
                    Dividend_quarter4 = Dividend_per_share_quarter[i] 
                    Dividend14 = cold.number_input("quarterly", value=Dividend_quarter4,key="unique_key4")
                    if Dividend_quarter3 != 0:
                         percentage_increase_3_4 = ((Dividend_quarter4 - Dividend_quarter3) / Dividend_quarter3) * 100
               elif i == 13:
                    Dividend_quarter5 = Dividend_per_share_quarter[i] 
                    Dividend15 = col2.number_input("current Dividend", value=Dividend_quarter5,key="unique_key5")
                    if Dividend_quarter4 != 0:
                         percentage_increase_4_5 = ((Dividend_quarter5 - Dividend_quarter4) / Dividend_quarter4) * 100


          #if  Dividend_quarter4 and Dividend_quarter5!=0:  
          try:
               Growth_rate= round(((Dividend_quarter5- Dividend_quarter4)/Dividend_quarter4)*100,2)

          except Exception as e:
               Growth_rate= 0
                

          cola, colb, colc, cold,col2 = st.columns(5)
             # for i in range(len(Dividend_growth_quarter)):
          #      if i == 0:
          #           Dividend_growth_quarter1 = Dividend_growth_quarter[i] * 100
          try:
               Dividend101 = cola.number_input("Year 4", value=Dividend_quarter1*4, key="unique_key_for_Dividend101")
          #      elif i == 12-8:
          except Exception as e:
                Dividend101 =0
          #           Dividend_growth_quarter2 = Dividend_growth_quarter[i] * 100
          try:
               Dividend201 = colb.number_input("Year 3", value=Dividend_quarter2*4, key="unique_key_for_Dividend201")

          except Exception as  e:
                Dividend201 =0
          #      elif i == 12-4:
          #           Dividend_growth_quarter3 = Dividend_growth_quarter[i] * 100
          try:
               Dividend301 = colc.number_input("Year 2", value=Dividend_quarter3*4, key="unique_key_for_Dividend301")
          #      elif i == 12:
          except Exception as e:
               Dividend301=0
          #   
          #         Dividend_growth_quarter4 = Dividend_growth_quarter[i] * 100

          try:
               Dividend401 = cold.number_input("Year 1", value=Dividend_quarter4*4, key="unique_key_for_Dividend401")
          except Exception as e:
               Dividend401 = 0

          #      elif i == 13:
          #           Dividend_growth_quarter5 = Dividend_growth_quarter[i] * 100
           
          try:  
           Dividend501 = col2.number_input("Current year", value=Dividend_quarter5*4, key="unique_key_for_Dividend501")

          except Exception as e:
          
           Dividend501 = 0


          cola, colb, colc, cold,col2 = st.columns(5)
             # for i in range(len(Dividend_growth_quarter)):
          #      if i == 0:
          #           Dividend_growth_quarter1 = Dividend_growth_quarter[i] * 100
          Dividend1 = cola.number_input("Growth Rate(%)", value=None, key="unique_key_for_Dividend1")
          #      elif i == 12-8:
          #           Dividend_growth_quarter2 = Dividend_growth_quarter[i] * 100
          Dividend2 = colb.number_input("Growth Rate(%)", value=percentage_increase_1_2, key="unique_key_for_Dividend2")
          #      elif i == 12-4:
          #           Dividend_growth_quarter3 = Dividend_growth_quarter[i] * 100
          Dividend3 = colc.number_input("Growth Rate(%)", value=percentage_increase_2_3, key="unique_key_for_Dividend3")
          #      elif i == 12:
          #           Dividend_growth_quarter4 = Dividend_growth_quarter[i] * 100
          Dividend4 = cold.number_input("Growth Rate(%)", value=percentage_increase_3_4, key="unique_key_for_Dividend4")

          #      elif i == 13:
          #           Dividend_growth_quarter5 = Dividend_growth_quarter[i] * 100
          Dividend5 = col2.number_input("Growth Rate(%)", value=percentage_increase_4_5, key="unique_key_for_Dividend5")

          # Check if any of the dividend inputs contain a value greater than 1
         # List to store the values greater than 1
          # dividends_greater_than_1 = []

          # # Check if any of the dividend inputs contain a value greater than 1
          # for dividend, name in zip([Dividend1, Dividend2, Dividend3, Dividend4, Dividend5],
          #                          ['Dividend1', 'Dividend2', 'Dividend3', 'Dividend4', 'Dividend5']):
          #      if dividend > 1:
          #           dividends_greater_than_1.append((name, dividend))

          # if dividends_greater_than_1:
          #      st.write("The following growth rates are greater than 1%:")
          # for name, value in dividends_greater_than_1:
          #      st.write(f"{name}: {value}%")
          # else:
          #      st.write("None of the growth rates are greater than 1%.")
          
          total_dividend_growth = Dividend5 + Dividend4 + Dividend3 + Dividend2

          # Calculate the average dividend growth rate
          num_dividend_growth_rates = 3  # Total number of dividend growth rates
          try:
               Average_dividend_growth_rate = total_dividend_growth / num_dividend_growth_rates

          except Exception as e:
               Average_dividend_growth_rate=0
                
          cola,colb = st.columns(2)
          #average_input = cola.number_input("Growth rate YOY (%)", value=Average_dividend_growth_rate)
          #Dividend_per_share_cagr_10_quarter =cola.number_input("Quarter Dividend per share Cagr 10 (%)", value=Dividend_per_share_cagr_10_quarter)
          #Dividend_per_share_cagr_10 = colb.number_input("Annual Dividend per share Cagr 10 (%)", value=Dividend_per_share_cagr_10)
          #Growth_rate_dividend = cola[1].number_input("Growth rate (%)", value=0.00)
          #WACC = cola[2].number_input("WACC (%)", value=WACC)

          cola, colb = st.columns(2)

          cola.write(f"Quarter Dividend per share 10 CAGR: {Dividend_per_share_cagr_10_quarter} %")
          colb.write(f"Annual Dividend per share 10 CAGR: {Dividend_per_share_cagr_10} %")

          col10,col11 =st.columns(2)
          Growth_rate_dividend = col10.number_input("Growth Rate %:", value=0.00)
          WACC = col11.number_input("WACC in (%):", value=WACC)

          try: 
           intrinsic_value3 = (Dividend15 * 4) * (1 + (Growth_rate_dividend / 100)) / ((WACC / 100) - (Growth_rate_dividend / 100))

          except Exception as e:
                
           intrinsic_value3 =0
          #st.write(intrinsic_value3)

          #try:
          if st.button("Calculate", key="Calculate_DDM"):
    
            
               DDM_intrinsic_value3 = intrinsic_value3*usd_to_eur_rate
                 
               col1,col2 = st.columns(2)


               if float(converted_amount) < DDM_intrinsic_value3:
                    font_color = "green"

                    with col1:
                         st.write(f'Current Price:    <span style="color: green;">{converted_amount} &euro;</span>', unsafe_allow_html=True,use_container_width=True)
                    with col2:
                         st.write(f"Fair Value:    <span style='color:{font_color}'>{DDM_intrinsic_value3:.2f} €</span>", unsafe_allow_html=True,use_container_width=True)
               else:
                    font_color = "red"

                    with col1:
                         st.write(f'Current Price:    <span style="color: green;">{converted_amount} &euro;</span>', unsafe_allow_html=True,use_container_width=True)
                    with col2:
                         st.write(f"Fair Value:    <span style='color:{font_color}'>{DDM_intrinsic_value3:.2f} €</span>", unsafe_allow_html=True,use_container_width=True)

                         
                              
         # else:     
          #     st.write("")
               

                         

               #print("graham_valuation:", graham_valuation_formated)
               #print("graham_valuation:", Euro_equivalent_graham_valuation)   
               #print("graham_valuation2:", Euro_equivalent_graham_valuation2)
               #print("average_fcf_Annual_funf:",average_fcf_Annual_one)
               #print("DCF2:",Euro_equivalent2)
               #print("average_valuation both high in Euro:", average_sum2)
               #print("average_valuation both low in Euro:", average_sum1)
               #print("average_valuation both low & high in Euro:", average_Middle_multiple_value)
               #print("Average_Middle_DCF",Average_Middle_DCF)
               # print("average_sum1:", average_sum1)
               #print("average_sum2:", average_sum2)
               #print("Average_both_multiples_sum:", Average_both_multiples_sum)
               #convert_value = Intrinsic_value
               #print("discounted to 5 yrs",sum_discounted_values)

               #print("WACC in %:",WACC_prozent)
              
               #print(Marketcap)
               #print("New value ",discounted_values[4])
               #print("New value2 ",discounted_values2[4])
               #print("npv-result:",rounded_npv_result)
               #print("npv-result2:",rounded_npv_result2)
               #print("2027 + terminal value",Sum_terminal_fcf)
               #print("2027 + terminal value2",Sum_terminal_fcf2)
               #print("Equity:",Equity_value)
               #print("Equity2:",Equity_value2)
               #print("intinsic_USD:",Intrinsic_value)
               #print("intinsic_Euro:",Euro_equivalent)
               #print("intinsic_USD2:",Intrinsic_value2)
               #print("intinsic_Euro2:",Euro_equivalent2)
               #print("Market cap:",Marketcap)  
               #print("shares Outstanding:",Average_shares_basic_annual_one)
               #st.write("Total_cash_last_years",Average_eps_basic_annual_five)
with st.container():              
     with Key_ratios:
          Annual, Quarter = st.tabs(["Annual", "Quarterly"])

               #with Annual:
                #    Annual,Quarterly = st.tabs(["Annual","Quarterly"])
                    
          with Annual:
                    #FCF_Margin = annual_data['fcf_margin'][-10:]
                    debt_equity_annual =annual_data['debt_to_equity'][-10:]
                    Price_to_tangible_book = annual_data['price_to_tangible_book'][-10:]
                    EBITDA_growth = annual_data['ebitda_growth'][-10:]
                    Price_to_book = annual_data['price_to_book'][-10:]
                    #Price_to_book = annual_data['price_to_book'][-10:]
                    #Dividend_per_share = annual_data['dividends'][-10:]
                    fcf_per_share_annual = annual_data['fcf_per_share'][-10:]
                    revenue_per_share_annual = annual_data['revenue_per_share'][-10:]
                    ROE_annual = annual_data['roe'][-10:]
                    Payout_ratio_annual = annual_data['payout_ratio'][-10:]
                    #Revenue_growth = annual_data['revenue_growth'][-10:]
                    NetIncome_growth = annual_data['net_income_growth'][-10:]
                    FCF_growth = annual_data['fcf_growth'][-10:]
                    Book_Value_growth = annual_data['book_value'][-10:]
                    Price_to_sales = annual_data['price_to_sales'][-10:]
                    Price_to_earnings=annual_data['price_to_earnings'][-10:]
                    shares_diluted_annual_growth=annual_data['shares_diluted_growth'][-10:]

                     
                    
                    try:
                         
                         Operating_Margin = annual_data['operating_margin'][-10:]
                         gross_margin = annual_data['gross_margin'][-10:]
                         
                         
                         #Cash_Dividends_paid_Total_annual = annual_data['cff_dividend_paid'][-10:]
                         #Shares_basic_annual = annual_data['shares_basic'][-10:]
                              
                    except Exception as e:  
                         Operating_Margin =0 
                         gross_margin  =0 



                    #eps_diluted_ttm = Financial_data['ttm']['debt_to_equity']
                    #st.write("debt_to_equity",eps_diluted_ttm)
                    

                    # Calculate DPS
                    #DPS = Cash_Dividends_paid_Total_annual / Shares_basic_annual

                    # Create a DataFrame for the total calculations
                    Period_end_dates = annual_data['period_end_date'][-10:]
                    index = range(len(Period_end_dates))
                    
                    total = pd.DataFrame({
                    'Period End Date': Period_end_dates,
                    'Revenue growth': Revenue_growth,
                    'Net Income growth': NetIncome_growth,
                    'FCF growth': FCF_growth,
                    'EPS growth':EPS_growth,
                    'FCF Margin':FCF_Margin,
                    'Shares diluted':shares_diluted_annual_growth,
                    'Operating Margin':Operating_Margin,
                    'Gross Margin':gross_margin, 
                    'Debt/Equity':debt_equity_annual,
                    'Book Value': Book_Value_growth,
                    'Price to Sales': Price_to_sales,
                    'Price to Tangible Book': Price_to_tangible_book,
                    'EBITDA growth': EBITDA_growth,
                    'Price to Book': Price_to_book,
                    'PE ratio':Price_to_earnings,
                    'Dividend per share':Dividend_per_share,
                    'FCF per share':fcf_per_share_annual,
                    'Revenue per share':revenue_per_share_annual,
                    'Payout ratio': Payout_ratio_annual,
                    'ROIC':ROIC_annual,
                    'ROE':ROE_annual
                    
                    }, index=index)

                    # Create a DataFrame for the metrics
                    metrics = [
                    ('Revenue growth', Revenue_growth),
                    ('Net Income growth', NetIncome_growth),
                    ('FCF growth', FCF_growth),
                    ('EPS growth',EPS_growth),
                    ('FCF Margin',FCF_Margin), 
                    ('Shares diluted',shares_diluted_annual_growth),
                    ('Operating Margin',Operating_Margin),
                    ('Gross Margin',gross_margin), 
                    ('Book Value', Book_Value_growth),
                    ('Debt/Equity',debt_equity_annual),
                    ('Price to Sales', Price_to_sales),
                    ('Price to Tangible Book', Price_to_tangible_book),
                    ('EBITDA growth', EBITDA_growth),
                    ('Price to Book', Price_to_book),
                    ('PE ratio',Price_to_earnings ),
                    ('Dividend per share',Dividend_per_share),
                    ('FCF per share',fcf_per_share_annual),
                    ('Revenue per share',revenue_per_share_annual),
                    ('Payout ratio', Payout_ratio_annual),
                    ('ROIC',ROIC_annual ),
                    ('ROE',ROE_annual)
                    
               
                    ]

                    merged_data = {}
                    for metric_name, metric_data in metrics:
                         if not isinstance(metric_data, list):
                              metric_data = [metric_data]  # Convert non-iterable values to lists

                         if metric_name in ('Revenue growth', 'Net Income growth', 'FCF growth', 'EPS growth','FCF Margin','Shares diluted','Operating Margin','Gross Margin','Debt/Equity','EBITDA growth','Payout ratio','ROIC','ROE'):
                              formatted_data = ["{:.2f}%".format(data * 100) for data in metric_data]
                         elif metric_name == 'Book Value':
                              formatted_data = ["{:.2f}B".format(data / 1_000_000_000) for data in metric_data]

                         elif metric_name == 'Dividend per share':
                              formatted_data = ["${:.2f}".format(data ) for data in metric_data]
                         else:
                              formatted_data = ["{:.2f}".format(data) for data in metric_data]
                         merged_data[metric_name] = formatted_data

                    merged_df_key_ratio = pd.DataFrame(merged_data, index=Period_end_dates).transpose()

                    st.table(merged_df_key_ratio.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))

                    #st.dataframe(merged_df_key_ratio.style.set_table_attributes('class="scroll-table"'),use_container_width=True)
                    #st.markdown('</div>', unsafe_allow_html=True)

                    with Quarter:
                                        FCF_Margin_quarter = quarterly_data['fcf_margin'][-10:]
                                        debt_equity_quarter =quarterly_data['debt_to_equity'][-10:]
                                        Price_to_tangible_book_quarter = quarterly_data['price_to_tangible_book'][-10:]
                                        EBITDA_growth_quarter = quarterly_data['ebitda_growth'][-10:]
                                        Price_to_book_quarter = quarterly_data['price_to_book'][-10:]
                                        #Price_to_book_quarter = quarterly_data['price_to_book'][-10:]
                                        Dividend_per_share_quarter = quarterly_data['dividends'][-10:]
                                        fcf_per_share_quarter = quarterly_data['fcf_per_share'][-10:]
                                        revenue_per_share_quarter = quarterly_data['revenue_per_share'][-10:]
                                        ROE_quarter = quarterly_data['roe'][-10:]
                                        Payout_ratio_quarter = quarterly_data['payout_ratio'][-10:]
                                        Revenue_growth_quarter = quarterly_data['revenue_growth'][-10:]
                                        NetIncome_growth_quarter = quarterly_data['net_income_growth'][-10:]
                                        FCF_growth_quarter = quarterly_data['fcf_growth'][-10:]
                                        Book_Value_growth_quarter = quarterly_data['book_value'][-10:]
                                        Price_to_sales_quarter = quarterly_data['price_to_sales'][-10:]
                                        Price_to_earnings_quarter=quarterly_data['price_to_earnings'][-10:]
                                        EPS_growth_quarter=quarterly_data['eps_diluted_growth'][-10:]
                                        ROIC_quarter=quarterly_data['roic'][-10:]
                                        shares_diluted_quarter_growth=quarterly_data['shares_diluted_growth'][-10:]
                                        try:
                                             
                                             Operating_Margin_quarter = quarterly_data['operating_margin'][-10:]
                                             gross_margin_quarter = quarterly_data['gross_margin'][-10:]
                                             
                                             
                                             #Cash_Dividends_paid_Total_annual = annual_data['cff_dividend_paid'][-10:]
                                             #Shares_basic_annual = annual_data['shares_basic'][-10:]
                                                  
                                        except Exception as e:  
                                             Operating_Margin_quarter =0 
                                             gross_margin_quarter  =0 



                                        #eps_diluted_ttm = Financial_data['ttm']['debt_to_equity']
                                        #st.write("debt_to_equity",eps_diluted_ttm)
                                        

                                        # Calculate DPS
                                        #DPS = Cash_Dividends_paid_Total_annual / Shares_basic_annual

                                        # Create a DataFrame for the total calculations
                                        Period_end_dates_quarter = quarterly_data['period_end_date'][-10:]
                                        index = range(len(Period_end_dates_quarter))
                                        
                                        total = pd.DataFrame({
                                        'Period End Date': Period_end_dates_quarter,
                                        'Revenue growth': Revenue_growth_quarter,
                                        'Net Income growth': NetIncome_growth_quarter,
                                        'FCF growth': FCF_growth_quarter,
                                        'EPS growth':EPS_growth_quarter,
                                        'FCF Margin':FCF_Margin_quarter,
                                        'Shares diluted':shares_diluted_quarter_growth,
                                        'Operating Margin':Operating_Margin_quarter,
                                        'Gross Margin':gross_margin_quarter, 
                                        'Debt/Equity':debt_equity_quarter,
                                        'Book Value': Book_Value_growth_quarter,
                                        'Price to Sales': Price_to_sales_quarter,
                                        'Price to Tangible Book': Price_to_tangible_book_quarter,
                                        'EBITDA growth': EBITDA_growth_quarter,
                                        'Price to Book': Price_to_book_quarter,
                                        'PE ratio':Price_to_earnings_quarter,
                                        'Dividend per share':Dividend_per_share_quarter,
                                        'FCF per share':fcf_per_share_quarter,
                                        'Revenue per share':revenue_per_share_quarter, 
                                        'Payout ratio': Payout_ratio_quarter,
                                        'ROIC':ROIC_quarter,
                                        'ROE':ROE_quarter
                                        }, index=index)

                                        # Create a DataFrame for the metrics
                                        metrics = [
                                        ('Revenue growth ', Revenue_growth_quarter),
                                        ('Net Income growth', NetIncome_growth_quarter),
                                        ('FCF growth', FCF_growth_quarter),
                                        ('EPS growth',EPS_growth_quarter),
                                        ('FCF Margin',FCF_Margin_quarter), 
                                        ('Shares diluted',shares_diluted_quarter_growth),
                                        ('Operating Margin',Operating_Margin_quarter),
                                        ('Gross Margin',gross_margin_quarter), 
                                        ('Book Value', Book_Value_growth_quarter),
                                        ('Debt/Equity',debt_equity_quarter),
                                        ('Price to Sales', Price_to_sales_quarter),
                                        ('Price to Tangible Book', Price_to_tangible_book_quarter),
                                        ('EBITDA growth', EBITDA_growth_quarter),
                                        ('Price to Book', Price_to_book_quarter),
                                        ('PE ratio',Price_to_earnings_quarter ),
                                        ('Dividend per share',Dividend_per_share_quarter),
                                        ('FCF per share',fcf_per_share_quarter),
                                        ('Revenue per share',revenue_per_share_quarter), 
                                        ('Payout ratio', Payout_ratio_quarter),
                                        ('ROIC',ROIC_quarter),
                                        ('ROE',ROE_quarter)
                                   
                                        ]

                                        merged_data = {}
                                        for metric_name, metric_data in metrics:
                                             if not isinstance(metric_data, list):
                                                  metric_data = [metric_data]  # Convert non-iterable values to lists

                                             if metric_name in ('Revenue growth', 'Net Income growth', 'FCF growth', 'EPS growth','FCF Margin','Shares diluted','Operating Margin','Gross Margin','Debt/Equity','EBITDA growth','Payout ratio','ROIC','ROE'):
                                                  formatted_data = ["{:.2f}%".format(data * 100) for data in metric_data]
                                             elif metric_name == 'Book Value':
                                                  formatted_data = ["{:.2f}B".format(data / 1_000_000_000) for data in metric_data]

                                             elif metric_name == 'Dividend per share':
                                                  formatted_data = ["${:.2f}".format(data ) for data in metric_data]
                                             else:
                                                  formatted_data = ["{:.2f}".format(data) for data in metric_data]
                                             merged_data[metric_name] = formatted_data

                                        merged_df_key_ratio = pd.DataFrame(merged_data, index=Period_end_dates_quarter).transpose()

                                       # st.table(merged_df_key_ratio.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}))
                                        st.table(merged_df_key_ratio.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px', 'margin': 'auto'}))
                                        


                                        #st.dataframe(merged_df_key_ratio.style.set_table_attributes('class="scroll-table"'),use_container_width=True)
                                        #st.markdown('</div>', unsafe_allow_html=True)



with st.container():
     with Charts:
               Annual, Quarter = st.tabs(["Annual", "Quarterly"])
               with Annual:
                    
                    date_annual_20yrs = annual_data['period_end_date'][-21:] 
                    #date_annual = annual_data['period_end_date'][-10:] 
                    
                    revenue_2003= annual_data['revenue'][-21:]                    
                    #revenue_2003 = [round(value, 2) for value in revenue_2003]
                    revenue_2003 = ["{:.2f}".format(value/1e9) for value in revenue_2003]

                    #revenue_2003 = [(value) for value in annual_data['revenue'][-21:]]

                    #dividendPaidInTheLast21Years = [abs(value) for value in annual_data['cff_dividend_paid'][-21:]]

                    # Create a DataFrame for the data
                    data = pd.DataFrame({
                    'Date': date_annual_20yrs,
                    #'Free Cash Flow': Free_cash_flow_annual_2003,
                    'Revenue':revenue_2003,
                    })

                    fig1 = px.bar(data, x='Date', y='Revenue',
                              text='Revenue',    
                              labels={'value': 'Amount()'},
                              title=f"Revenue in Billions USD: 10 YR: {Revenue_Cagr_10}%    5 YR: {Revenue_5_CAGR}%") 
                   
                    fig1.update_layout(title_x=0.05)     

                    
                    revenue_growth_2003= annual_data['revenue_growth'][-21:]                    
                    #revenue_2003 = [round(value, 2) for value in revenue_2003]
                    revenue_growth_2003 = ["{:.2f} %".format(value*100) for value in revenue_growth_2003]



               # Create a DataFrame for the data
                    data = pd.DataFrame({
                    'Date': date_annual_20yrs,
                    #'Free Cash Flow': Free_cash_flow_annual_2003,
                    'Revenue Growth':revenue_growth_2003,
                    })

                    # Create a Streamlit app
                    #st.title('Free Cash Flow and Revenue Data')

                    # Create a Plotly Express bar chart with side-by-side bars
                    fig2 = px.bar(data, x='Date', y='Revenue Growth',
                              text='Revenue Growth', 
                              labels={'value': 'Amount'},
                              title=f"5 YR Revenue Y/Y: {Revenue_growth_5years:.2f}%    1 YR Revenue: {Revenue_growth_1year:.2f}%") 
                    
                     
          
          #colr3.info(f"Revenue Growth: {Revenue_growth_10years}")
                                            #barmode='group')  # Use 'group' to display bars side by side
                    #fig2.update_layout(title_x=0.05)
                              
                    #fig.update_traces(marker_color='royalblue')
                    # Display the chart using Streamlit

                    col1,col2 = st.columns(2)

                    with col1:
                         st.plotly_chart(fig1,use_container_width=True, config=config)

                    with col2:
                         st.plotly_chart(fig2,use_container_width=True, config=config)
               

          #-------------------------------------------------------------------------------------------------
          
                    
                    eps_diluted_annual_2003=annual_data['eps_diluted'][-21:]
                    eps_diluted_annual_2003 = ["$ {:.2f}".format(value) for value in eps_diluted_annual_2003]

                    data = pd.DataFrame({
                    'Date': date_annual_20yrs,
                    'EPS': eps_diluted_annual_2003,
                    })

                    # Create a Streamlit app
                    #st.title('Free Cash Flow and Revenue Data')

                    # Create a Plotly Express bar chart with side-by-side bars
                    
                    fig1 = px.bar(data, x='Date', y='EPS',
                              text='EPS',  # Display the value on top of each bar
                              labels={'value': 'Amount($)'},  # Include the percentage sign in the label
                              title= f"10YR EPS: {EPS_Cagr_10}%   5YR: {EPS_5_CAGR}%  EPS(TTM): $ {eps_diluted_ttm}  Next YR: $ {Earnings_next_yr_in_value} ({Earnings_next_yr_in_prozent})") 
                   



                    # Display the chart using Streamlit
                    
                    #fig1.update_layout(title_x=0.05)

                    shares_diluted_2003=annual_data['shares_diluted'][-21:]
                    shares_diluted_2003 = ["{:.3f}".format(value/1e9) for value in shares_diluted_2003]

                    data = pd.DataFrame({
                    'Date': date_annual_20yrs,
                    'Shares Outstanding': shares_diluted_2003,
                    })

                    # Create a Streamlit app
                    #st.title('Free Cash Flow and Revenue Data')

                    # Create a Plotly Express bar chart with side-by-side bars
                    
                    fig2 = px.bar(data, x='Date', y='Shares Outstanding',
                              text='Shares Outstanding',  # Display the value on top of each bar
                              labels={'value': 'Amount($)'},  # Include the percentage sign in the label
                              title=f"Shares Outstanding in (Billion USD):  {Shares_outstanding_funf_growth:.2f}% share Buyback past 5 YR   ")

                    
                    #fig2.update_traces(texttemplate='%{y}', textposition='outside')
                    fig2.update_layout(title_x=0.05)
                    # Display the chart using Streamlit
                    col1,col2 = st.columns(2)

                    with col1:
                         st.plotly_chart(fig1,use_container_width=True,config=config)
                    with col2:
                         st.plotly_chart(fig2,use_container_width=True,config=config)
          #-------------------------------------------------------------------------------------------------
          # Create a DataFrame for the data
                    #Free_cash_flow_annual_2003 = [round(value, 2) for value in Free_cash_flow_annual_2003]
                         
                    #dividendPaidInTheLast21Years = abs(annual_data['cff_dividend_paid'][-21:])
                    dividendPaidInTheLast21Years = [abs(value) for value in annual_data['cff_dividend_paid'][-21:]]
                     
                    Free_cash_flow_annual_2003 = annual_data['fcf'][-21:]

          #.................................5  Dividend CAGR............................................
                         #dividendPaidInTheLast21Years = [abs(value) for value in annual_data['cff_dividend_paid'][-21:]]

                    # Wert an der 6. Position von hinten erhalten
                    #value_at_index_6 = dividendPaidInTheLast21Years[-6]
                    #value_at_index_11  = dividendPaidInTheLast21Years[-11]
                    #value_at_index_last  = dividendPaidInTheLast21Years[-1]
                     

                    #print("Wert an der 6. Position von hinten in der Liste:", value_at_sixth_from_last)
                    #print("Wert an der 11. Position von hinten in der Liste:", value_at_eleven_from_last)
                    #print("Wert an der last Position :", value_at_last_position)
     

                    try:
                         value_at_index_6 = dividendPaidInTheLast21Years[-6]
                         value_at_index_last  = dividendPaidInTheLast21Years[-1]
                    except Exception as e:
                         value_at_index_6 = 0
                         value_at_index_last = 0
                    try:
                         
                         if value_at_index_6 == 0 or value_at_index_last ==0:
                              Dividend_5_CAGR = 0

                         else:
                                   try:
                                        Dividend_5_CAGR = (pow((value_at_index_last / value_at_index_6), 0.2) - 1) * 100
                                        #CAGR = round(CAGR, 2)

                                        if isinstance(Dividend_5_CAGR, complex):
                                                  Dividend_5_CAGR = 0  # Set CAGR to 0 if it's a complex number
                                        else:
                                             Dividend_5_CAGR = "{:.2f}".format(Dividend_5_CAGR)

                                   except Exception as e:
                                        Dividend_5_CAGR = 0

                    except Exception as e:  

                         Dividend_5_CAGR =0; 
                   
  #.................................10  Dividend CAGR............................................                    

                    try:
                         value_at_index_11  = dividendPaidInTheLast21Years[-11]
                         #st.write(value_at_index_10)
                         #st.write(value_at_index_20)
                         #value_at_index_20 = dividendPaidInTheLast21Years[20]

                    except Exception as e:
                         value_at_index_11 = 0
                         value_at_index_last = 0
                    try:
                         
                         if value_at_index_11 == 0 or value_at_index_last == 0:
                              Dividend_10_CAGR = 0

                         else:
                                   try:
                                        Dividend_10_CAGR = (pow((value_at_index_last / value_at_index_11), 0.1) - 1) * 100
                                        #CAGR = round(CAGR, 2)

                                        if isinstance(Dividend_10_CAGR, complex):
                                                  Dividend_10_CAGR = 0  # Set CAGR to 0 if it's a complex number
                                        else:
                                             Dividend_10_CAGR = "{:.2f}".format(Dividend_10_CAGR, 2)

                                   except Exception as e:
                                        Dividend_10_CAGR = 0

                    except Exception as e:  

                         Dividend_10_CAGR =0; 
                    
  #.................................20  Dividend CAGR............................................                    

                    # try:
                    #      value_at_index_0 = dividendPaidInTheLast21Years[0]
                    #      #value_at_index_20 = dividendPaidInTheLast21Years[20]

                    # except Exception as e:
                    #      value_at_index_0 = 0
                    #      value_at_index_20 = 0
                    # try:
                         
                    #      if value_at_index_0 == 0:
                    #           Dividend_20_CAGR = 0

                    #      else:
                    #                try:
                    #                     Dividend_20_CAGR = (pow((value_at_index_20 / value_at_index_0), 0.05) - 1) * 100
                    #                     #CAGR = round(CAGR, 2)

                    #                     if isinstance(Dividend_20_CAGR, complex):
                    #                               Dividend_20_CAGR = 0  # Set CAGR to 0 if it's a complex number
                    #                     else:
                    #                          Dividend_20_CAGR = round(Dividend_20_CAGR, 2)

                    #                except Exception as e:
                    #                     Dividend_20_CAGR = 0

                    # except Exception as e:  

                    #      Dividend_20_CAGR =0; 

                    
                    #Free_cash_flow_annual_2003 = ["{:.2f}".format(value/1e9) for value in Free_cash_flow_annual_2003]
                    data = pd.DataFrame({
                    'Date': date_annual_20yrs,
                    'Dividends': dividendPaidInTheLast21Years,
                    'Free Cash Flow': Free_cash_flow_annual_2003,
                    })
                    fig = go.Figure()


                    fig.add_trace(go.Bar(x=data['Date'], y=data['Free Cash Flow'], name='Free Cash Flow'))
                    # Add the Dividends bar plot
                    fig.add_trace(go.Bar(x=data['Date'], y=data['Dividends'],marker_color='black',  name='Dividends Paid'))
                    

                    # Add the Free Cash Flow bar plot
                    

                    # Update layout
                    title_text = f"10YR Dividend: {Dividend_10_CAGR}%     5YR Dividend: {Dividend_5_CAGR}%       <span style='color:dodgerblue'>10YR FCF CAGR: {FCF_Cagr_10}%    5YR FCF CAGR: {FCF_5_CAGR}%</span> "  


                    #title_text = f"<span style='color:dodgerblue'>20YR Dividend CAGR: {Dividend_20_CAGR}%</span>"

                    

                    #title_text = f"Dividend 20 CAGR: {Dividend_20_CAGR}% Dividend 10 CAGR: {Dividend_10_CAGR}%  Dividend 5 CAGR: {Dividend_5_CAGR}%"
                    fig.update_layout(barmode='group', xaxis_title='Date', yaxis_title='Amount (B)', title=title_text)
                                        # Update legend placement
                    fig.update_layout(legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=1.1,
                    xanchor="center",
                    x=0.5
                    ))

                    fig.update_traces(texttemplate='%{y}', textposition='inside')

                   
                    #Free_cash_flow_per_share_annual_2003 =annual_data['fcf_per_share'][-21:]
                    #Free_cash_flow_per_share_annual_2003 = ["{:.2f}".format(value) for value in Free_cash_flow_per_share_annual_2003]

#                    data = pd.DataFrame({
 #                   'Date': date_annual_20yrs,
  #                  'Free Cash Flow per share': Free_cash_flow_per_share_annual_2003,
   #                 })

                    # Titel und Plot anzeigen
                    #st.title('Annual Free Cash Flow')
#                    fig2 = px.bar(data, x='Date', y='Free Cash Flow per share',
 #                             text='Free Cash Flow per share',  # Display the value on top of each bar
  #                            labels={'value': 'Amount()'},  # Include the percentage sign in the label
   #                           title='Free Cash Flow per share')
    #                fig2.update_traces(texttemplate='%{y}', textposition='outside')


                    # Diagramm anzeigen
                    #col1,col2=st.columns(2)
                    #with col1:
                    st.plotly_chart(fig,use_container_width=True,config=config)
                    #with col2:
                    #st.plotly_chart(fig2,use_container_width=True,config=config)
#------------------------------------------------------------------------------------------------------------------------------------
                            
   

          #-------------------------------------------------------------------------------------------------
 
                    Dividend_per_share = annual_data['dividends'][-10:]
                    Dividend_per_share = ["${:.2f}".format(value * 1) for value in Dividend_per_share]
                    
                         #Price_to_earnings=annual_data['price_to_earnings'][-10:]
                    data = pd.DataFrame({
                    'Date': date_annual,
                    'Dividend per Share': Dividend_per_share,
                    })

                    # Create a Streamlit app
                    #st.title('Free Cash Flow and Revenue Data')                                    
                    
                    # Create a Plotly Express bar chart with side-by-side bars
                    
                    fig1 = px.bar(data, x='Date', y='Dividend per Share',
                                   text='Dividend per Share',  # Display the value on top of each bar
                                   labels={'value': 'Amount($)'},  # Include the percentage sign in the label
                                   title=f"5 YR Dividend Yield: {Dividend_yield_average}  Current Dividend yield: {Dividend_per_share_yield}")

                    fig1.update_layout(title_x=0.05)
          
                  # Extract the last 21 years of dividends per share growth data
                    Dividends_per_share_growth_annual_2003 = annual_data['dividends_per_share_growth'][-10:]
                    Dividends_per_share_growth_annual_2003 = ["{:.2f}%".format(value * 100) for value in Dividends_per_share_growth_annual_2003]

                    # Create a DataFrame
                    data = pd.DataFrame({
                    'Date': date_annual,
                    'Dividends per Share growth': Dividends_per_share_growth_annual_2003,
                    })



                    # Create a Plotly Express bar chart
                    fig2 = px.bar(data, x='Date', y='Dividends per Share growth',
                              text='Dividends per Share growth',  # Corrected the column name
                              labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                              title='Dividends per Share growth')

                    fig2.update_layout(title_x=0.05)

                    col1, col2 =st.columns(2)
                    with col1:
                         st.plotly_chart(fig1, use_container_width=True,config=config)
                    with col2:
                         st.plotly_chart(fig2, use_container_width=True,config=config)




                         #------------------------------------------------------------------------------------------------------------
                         
                    ROE_annual_10years = annual_data['roe'][-10:]
                    ROIC_annual_10years = annual_data['roic'][-10:]
                    try:
                         ROIC_annual_10years = ["{:.2f}%".format(ROIC_annual_10years * 100) for ROIC_annual_10years in ROIC_annual_10years]
                    except Exception as e:
                         ROIC_annual_10years = 0.0

                   
                         
                    data = pd.DataFrame({
                    'Date': date_annual,
                    'ROIC': ROIC_annual_10years,
                    })

            
                    fig1 = px.bar(data, x='Date', y='ROIC',
                              text='ROIC',  # Display the value on top of each bar
                              labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                              title= f"5 YR ROIC Y/Y: {Average_ROIC_funf}    Current ROIC: {ROIC_annual_one}<br>"
                              "<span style='font-family: Calibri; font-style: italic;'>Indikator für die Fähigkeit eines Unternehmens, Renditen für das investierte Kapital zu <br>erwirtschaften.</span>") 
                    
                    
                   # fig1.update_layout(title_x=0.05)



                    try:
                         ROE_annual_10years = ["{:.2f}%".format(ROE_annual_10years * 100) for ROE_annual_10years in ROE_annual_10years]
                    except Exception as e:
                         ROE_annual_10years = 0.0
                         
                    data = pd.DataFrame({
                    'Date': date_annual,
                    'ROE': ROE_annual_10years,
                    })

                    # Create a Streamlit app
                    #st.title('Free Cash Flow and Revenue Data')                                    
                    
                    # Create a Plotly Express bar chart with side-by-side bars
                    
               
                    fig2 = px.bar(data, x='Date', y='ROE',
                              text='ROE',  # Display the value on top of each bar
                              labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                              title=f"5 YR ROE Y/Y: {five_ROE}%    Current ROE: {ROE_ttm}") 
                    
                    fig2.update_layout(title_x=0.05)

                    col1, col2 = st.columns(2)
                    with col1:

                         st.plotly_chart(fig1,use_container_width=True,config=config)

                    with col2:
                         st.plotly_chart(fig2,use_container_width=True,config=config)

#-------------------------------------------------------------------------------------------------
                    try:
                         gross_margin = ["{:.2f}%".format(gross_margin * 100) for gross_margin in gross_margin]
                    except Exception as e:
                         gross_margin = 0.0


                    title_text = (
                    f"5 YR Gross Margin Y/Y: {five_yrs_average_gross_margin}    Current Gross Margin: {rounded_gross_margin} <br>"
                    "<span style='font-family: Calibri; font-style: italic;'>Die Bruttogewinnmarge ist der Gewinn, der nach Abzug der Herstellkosten (COGS) <br>vom Umsatz übrig bleibt.</span>")          
                  
                    data = pd.DataFrame({
                    'Date': date_annual,
                    'Gross Margin': gross_margin,
                    })

                    # Create a Streamlit app
                    #st.title('Free Cash Flow and Revenue Data')                                    
                    
                    # Create a Plotly Express bar chart with side-by-side bars
                    
               
                    fig1 = px.bar(data, x='Date', y='Gross Margin',
                              text='Gross Margin',  # Display the value on top of each bar
                              labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                              title=title_text) 


                    fig1.update_layout(title_x=0.05)

                    try:
                         Operating_Margin = ["{:.2f}%".format(Operating_Margin * 100) for Operating_Margin in Operating_Margin]
                    except Exception as e:
                         Operating_Margin = 0.0
                         
                    data = pd.DataFrame({
                    'Date': date_annual,
                    'Operating Margin': Operating_Margin,
                    })


               
                    fig2 = px.bar(data, x='Date', y='Operating Margin',
                              text='Operating Margin',  # Display the value on top of each bar
                              labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                              title=f"5 YR Operating Margin Y/Y: {rounded_operating_margin_five}    Current Operating Margin: {rounded_operating_margin}<br>"
                              "<span style='font-family: Calibri; font-style: italic;'>Die Nettogewinnmarge ist der Gewinn, der nach Abzug der Herstellkosten (COGS) <br>und der Betriebskosten(wie Material-, Produktions-, Verwaltungs- und <br>Vertriebskosten) vom Umsatz übrig bleibt.</span>"
                              ) 
                   
                    #fig2.update_layout(title_x=0.05)


                    col1, col2 = st.columns(2)
                    with col1:

                         st.plotly_chart(fig1,use_container_width=True,config=config)

                    with col2:
                         st.plotly_chart(fig2,use_container_width=True,config=config)


#------------------------------------------------------------  
                    try:
                         Net_income_margin_10_ = ["{:.2f}%".format(Net_income_margin_10_ * 100) for Net_income_margin_10_ in Net_income_margin_10_]
                    except Exception as e:
                        Net_income_margin_10_ = 0.0
                         
                    data = pd.DataFrame({
                    'Date': date_annual,
                    'Net Profit Margin': Net_income_margin_10_,
                    })

                    # Create a Streamlit app
                    #st.title('Free Cash Flow and Revenue Data')                                    
                    
                    # Create a Plotly Express bar chart with side-by-side bars

                    title_text = (
                    f"5 YR Net Profit Margin Y/Y: {five_yrs_Nettomarge}%  Current Net Profit Margin: {Net_margin_ttm} <br>"

                    "  <span style='font-family: Calibri; font-style: italic;'>Die Nettogewinnmarge ist der Gewinn, der nach Abzug der Herstellkosten (COGS) <br>, Betriebskosten, Zinsen, Steuern und außerordentlichen Posten vom Umsatz <br>übrig bleibt.</span>"
                    )
                        
                    #wrapped_title = "<br>".join(textwrap.wrap(title_text))

                    fig1 = px.bar(data, x='Date', y='Net Profit Margin',
                              text='Net Profit Margin',  # Display the value on top of each bar
                              labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                              title=title_text)


                    #fig1.update_layout(title_x=0.05)

                    try:
                         FCF_Margin = ["{:.2f}%".format(FCF_Margin * 100) for FCF_Margin in FCF_Margin]
                    except Exception as e:
                         FCF_Margin = 0.0
                         
                    data = pd.DataFrame({
                    'Date': date_annual,
                    'FCF Margin': FCF_Margin,
                    })

                    # Create a Streamlit app
                    #st.title('Free Cash Flow and Revenue Data')                                    
                    
                    # Create a Plotly Express bar chart with side-by-side bars
                    
               
                    fig2 = px.bar(data, x='Date', y='FCF Margin',
                              text='FCF Margin',  # Display the value on top of each bar
                              labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                              title=f"5 YR FCF Margin Y/Y: {FCF_Margin_5}%    Current FCF Margin: {FCF_Margin_1:.2f}%<br>"
                              " <span style='font-family: Calibri; font-style: italic;'>Die FCF-Marge (freier Cashflow) ist ein Indikator dafür, <br>wie effizient ein Unternehmen seinen Umsatz in freien Cashflow umwandelt.</span>") 
                    

                    
                    fig2.update_layout(title_x=0.05)


                    col1, col2 = st.columns(2)
                    with col1:

                         st.plotly_chart(fig2,use_container_width=True,config=config)

                    with col2:
                         st.plotly_chart(fig1,use_container_width=True,config=config)
 
#........  ...................................................................................................................               
                         #Price_to_earnings=annual_data['price_to_earnings'][-10:]
                    Price_to_earnings = ["{:.2f}".format(value) for value in Price_to_earnings]
                    #Price_to_earnings = "{:.2f}".format((Price_to_earnings))
                    data = pd.DataFrame({
                    'Date': date_annual,
                    'PE Ratio': Price_to_earnings,
                    })

                    # Create a Streamlit app
                    #st.title('Free Cash Flow and Revenue Data')                                    
                    
                    # Create a Plotly Express bar chart with side-by-side bars
                    
                    fig21 = px.bar(data, x='Date', y='PE Ratio',
                              labels={'value': 'Ratio'},
                              title=f"-><span style='color:dodgerblue'>10 YR PE:</span> {average_PE_historical}  -><span style='color:dodgerblue'>5 YR PE: </span> {pe_five_}  -><span style='color:dodgerblue'>Current PE: </span> {pe_ttm}  -><span style='color:dodgerblue'>Forward P/E:</span>  {forwardPE}")  # Use 'group' to display bars side by side

                                                                                                                                 
                    fig21.add_shape(
                    type='line',
                    x0=data['Date'].min(),  # Adjust this based on your data
                    x1=data['Date'].max(),  # Adjust this based on your data
                    y0=average_PE_historical,
                    y1=average_PE_historical,
                    line=dict(color='red', width=2, dash='dash'),
                    yref='y',
                    )
                    
                    fig21.add_annotation(
                    text=f'',
                    xref='paper',  # Set xref to 'paper' for center alignment
                    yref='paper',  # Set yref to 'paper' for center alignment
                    x=0.10,  # Adjust to center horizontally
                    y=0.7,  # Adjust to center vertically
                    showarrow=False,  # Remove the arrow
                    font=dict(color='red'),  # Set font color to red
                   )          

                    # Display the chart using Streamlit
                    #st.plotly_chart(fig21,use_container_width=True,config=config)


                                                         #Marketcap_in_Billion 
                    market_cap_history=annual_data['market_cap'][-21:]  
                    date_annual_20yrs = annual_data['period_end_date'][-21:] 

                    #market_cap_history = np.append(market_cap_history, 45.78)
                    #date_annual_20yrs = np.append(date_annual_20yrs, 2023)

                    market_cap_history = ["{:.2f}".format(value) for value in market_cap_history]
                    #Price_to_earnings = "{:.2f}".format((Price_to_earnings))
                    data = pd.DataFrame({
                    'Date': date_annual_20yrs,
                    'Market Cap': market_cap_history,
                    })

                    # Create a Streamlit app
                    #st.title('Free Cash Flow and Revenue Data')                                    
                    
                    # Create a Plotly Express bar chart with side-by-side bars
                    
                                                                                                                                 
                    fig22 = px.bar(data, x='Date', y='Market Cap',
                              labels={'value': 'ratio'},
                              title=f'Market Cap:  Current Market Cap: {Marketcap_in_Billion}')
                              #barmode='group')  # Use 'group' to display bars side by side

                    fig22.update_layout(title_x=0.05)

                    # Display the chart using Streamlit

                    col2, col3 =st.columns(2)
                    with col2:
                         st.plotly_chart(fig21,use_container_width=True,config=config)

                    with col3:
                         st.plotly_chart(fig22,use_container_width=True,config=config)


                    #-------------------------------------------------------------------------------------------------

                    Price_to_tangible_book_quarter = quarterly_data['price_to_tangible_book'][-10:]
                    TBVPS = quarterly_data['tangible_book_per_share'][-1:]
                    PTBVPS=amount/TBVPS
                    PTBVPS = sum(PTBVPS)/len(PTBVPS)
                    #st.write("TBVPS",TBVPS)
                    #st.write("PTBVPS",PTBVPS)
                    data = pd.DataFrame({
                    'Date': date_annual,
                    'Price to Tangible Book Value': Price_to_tangible_book,
                    })

                    # Create a Streamlit app
                    #st.title('Free Cash Flow and Revenue Data')

                    # Create a Plotly Express bar chart with side-by-side bars
                    Average_Price_to_tangible_book =round(sum(Price_to_tangible_book)/len(Price_to_tangible_book))
                    
                    fig11 = px.bar(data, x='Date', y='Price to Tangible Book Value',               
                              labels={'value': 'Ratio'},
                              title=f'10 P/TBV: {Average_Price_to_tangible_book:.2f}  Current P/TBV: {PTBVPS:.2f}')  # Use 'group' to display bars side by side
                    
                    fig11.add_shape(
                    type='line',
                    x0=data['Date'].min(),  # Adjust this based on your data
                    x1=data['Date'].max(),  # Adjust this based on your data
                    y0=Average_Price_to_tangible_book,
                    y1=Average_Price_to_tangible_book,
                    line=dict(color='red', width=2, dash='dash'),
                    yref='y',
                    )
                    
                    fig11.add_annotation(
                    text=f'',
                    xref='paper',  # Set xref to 'paper' for center alignment
                    yref='paper',  # Set yref to 'paper' for center alignment
                    x=0.04,  # Adjust to center horizontally
                    y=0.7,  # Adjust to center vertically
                    showarrow=False,  # Remove the arrow
                    font=dict(color='red'),  # Set font color to red
                    )

                    # Display the chart using Streamlit
                    #st.plotly_chart(fig11,use_container_width=True,config=config)

                    #-------------------------------------------------------------------------------------------------
                    BVPS = quarterly_data['book_value_per_share'][-1:]
                    PBVPS=amount/BVPS
                    PBVPS=sum(PBVPS)/len(PBVPS)
                    #st.write("BVPS",BVPS)
                    #st.write("PBVPS",PBVPS)
                    data = pd.DataFrame({
                    'Date': list(date_annual),
                    'Price to Book Value': Price_to_book,
                    })

                    # Create a Streamlit app
                    #st.title('Free Cash Flow and Revenue Data')

                    # Create a Plotly Express bar chart with side-by-side bars
                    average_price_to_book = round(sum(Price_to_book)/len(Price_to_book),2)

                    fig12 = px.bar(data, x='Date', y='Price to Book Value',
                              labels={'value': 'Ratio'},
                              #title='Price to Book Value,{average_price_to_book:.2f}')
                              title=f'10 P/BV: {average_price_to_book:.2f}  Current P/B: {PBVPS:.2f}')
                    
                    fig12.update_layout(title_x=0.05)

                    fig12.add_shape(
                    type='line',
                    x0=data['Date'].min(),  # Adjust this based on your data
                    x1=data['Date'].max(),  # Adjust this based on your data
                    y0=average_price_to_book,
                    y1=average_price_to_book,
                    line=dict(color='red', width=2, dash='dash'),
                    yref='y',
                    )
                    
                    fig12.add_annotation(
                    text=f'',
                    xref='paper',  # Set xref to 'paper' for center alignment
                    yref='paper',  # Set yref to 'paper' for center alignment
                    x=0.10,  # Adjust to center horizontally
                    y=0.7,  # Adjust to center vertically
                    showarrow=False,  # Remove the arrow
                    font=dict(color='red'),  # Set font color to red
                    )


                    # Display the chart using Streamlit
                    #st.plotly_chart(fig12,use_container_width=True,config=config)


                    col1, col2 =st.columns(2)
                    with col1:
                         st.plotly_chart(fig11,use_container_width=True,config=config)
                          
                    with col2:
                         st.plotly_chart(fig12,use_container_width=True,config=config)
#.........


                         

#...........................................................................................................
                   

                    # NetIncome_annual_2003=annual_data['net_income'][-21:]
                    # NetIncome_annual_2003 = ["$ {:.2f}".format(value/1e9) for value in NetIncome_annual_2003]

                    # #Free_cash_flow_annual_2003 = annual_data['fcf'][-21:]
                    # #Free_cash_flow_annual_2003 = ["{:.2f}".format(value/1e9) for value in Free_cash_flow_annual_2003]

                    # Net_Operating_CashFlow_annual_2003 = annual_data['cf_cfo'][-21:] 
                    # Net_Operating_CashFlow_annual_2003 = ["{:.2f}".format(value/1e9) for value in Net_Operating_CashFlow_annual_2003]

                    # SGA_Expense_annual_2003 = annual_data['total_opex'][-21:]
                    # SGA_Expense_annual_2003 = ["{:.2f}".format(value/1e9) for value in SGA_Expense_annual_2003]


                    #                # Create a DataFrame with the data
                    # data = pd.DataFrame({
                    # 'Date': date_annual_20yrs,
                    # 'Revenue': revenue_2003,
                    # 'Net Income': NetIncome_annual_2003,
                    # 'Free Cash Flow': Free_cash_flow_annual_2003,
                    # 'Operating Cash Flow': Net_Operating_CashFlow_annual_2003,
                    # 'Operating Expenses': SGA_Expense_annual_2003
                    # })


                    # # Plot the data using Plotly Express
                    # fig = px.line(data, x='Date', y=['Revenue', 'Net Income', 'Free Cash Flow',
                    #                               'Operating Cash Flow', 'Operating Expenses'],
                    #           title='Financial Metrics Over Time')

                    # # Adjust line width
                    # #fig.update_traces(line=dict(width=5))

                    # # Display the plot
                    # st.plotly_chart(fig, use_container_width=True,config=config)
                                                            
#.......................................................................................................

                    # with Quarter:
                    #                         #revenue_2013 = annual_data['revenue'][-10:] 
                    #      date_quarter_20yrs = quarterly_data['period_end_date'][-21:] 
                         
                    #      revenue_quarter_2003= quarterly_data['revenue'][-21:]                    
                    #      #revenue_2003 = [round(value, 2) for value in revenue_2003]
                    #      revenue_quarter_2003 = ["{:.2f}".format(value) for value in revenue_quarter_2003]

                    # # Create a DataFrame for the data
                    #      data = pd.DataFrame({
                    #      'Date': date_quarter_20yrs,
                    #      #'Free Cash Flow': Free_cash_flow_annual_2003,
                    #      'Revenue':revenue_quarter_2003,
                    #      })

                    #      # Create a Streamlit app
                    #      #st.title('Free Cash Flow and Revenue Data')

                    #      # Create a Plotly Express bar chart with side-by-side bars
                    #      fig = px.bar(data, x='Date', y='Revenue',
                    #                labels={'value': 'Amount'},
                    #                title='Annual Revenue',
                    #                barmode='group')  # Use 'group' to display bars side by side

                                   
                    #      #fig.update_traces(marker_color='royalblue')
                    #      # Display the chart using Streamlit
                    #      st.plotly_chart(fig,use_container_width=True, config=config)




with st.container():
     with Retirement_Calculator:


          #if 'keys_type' not in st.session_state:
           #     st.session_state.key_type='values'


          # image = st.image('fcf estimate.png', caption='FCF projection', use_column_width=True)

          # image = st.image('Terminal-Value.png', caption='Terminal Value', use_column_width=True)
                    
          # image = st.image('Wacc.png', caption='Discount rate Calculation', use_column_width=True)

          # image = st.image('NPV.png', caption='Net Present Value', use_column_width=True)
          

          #st.write("FCF Projection")
          #st.image('fcf estimate.png', use_column_width=True)

          st.write("DCF Calculation")
          st.image('DCF Update.png', use_column_width=True)

          st.write("Terminal Value")
          st.image('Terminal-Value.png', use_column_width=True)

          st.write("Multiple of Earnings Valuation")
          st.image('Multiples of Earnings.png', use_column_width=True)

          st.write("Net Present Value")
          st.image('NPV.png', use_column_width=True)

          st.write("Dividend Discount Model")
          st.image('DDM.png', use_column_width=True) 

          st.write("CAGR")
          st.image('CAGR.png', use_column_width=True) 

          

      # Display the first 20 characters of the description
          st.write("DCF")
          short_description = """
          - Die Discounted-Cashflow-Methode (DCF) ist eine sehr effiziente Bewertungsmethode, um den inneren Wert oder Fair Value einer Investition zu bestimmen.

          - Der erste Schritt in der Discounted-Cashflow-Analyse besteht in der Prognose der zukünftigen Cashflows, die von einer Investition erwartet werden.

          - Die Prognose des Cashflows werden über einen bestimmten Zeitraum, in unserem Beispiel 5/10 Jahre, ermittelt.

          - Sobald die zukünftigen Cashflows geschätzt sind, werden sie unter Verwendung eines Diskontsatzes auf ihren heutigen Wert diskontiert.
            Die verwendete Diskontsatz ist in der Regel der gewichtete durchschnittliche Kapitalkostensatz (WACC).

          - Der Grundgedanke hinter dieser Diskontierung ist, dass ein in der Zukunft gezahlter Euro aufgrund des Zinseffekts weniger wert ist als ein heute gezahlter Euro.

          - Durch die Diskontierung werden künftige Cashflows so angepasst, dass sie ihren heutigen Wert in Euro haben.

          - Der Endwert wird in der Regel anhand der ewigen Wachstumsrate berechnet, die die Wachstumsrate darstellt, mit der die Cashflows auf unbestimmte Zeit in die Zukunft wachsen sollen.

          - Der Endwert wird zum diskontierten Present Value der geschätzten Cashflows addiert, um den gesamten Wert der Investition über den gesamten Investitionszeitraum zu erfassen (Unternehmenwert oder Enterprise Value)..

          - Enterprise Value wird um den Wert der Cash und Cash-Äquivalente ergänzt, und dann wird die Gesamtschuld abgezogen, um den Eigenkapitalwert zu ermitteln. Der Eigenkapitalwert wird dann durch die Zahl der im Umlauf befindlichen Aktien dividiert, um einen fairen Wert pro Aktie zu erhalten.          """

          st.write(short_description)

          Net_debt =annual_data['net_debt'][-5:]
          #st.write("Net_debt",Net_debt)


          #st.write(f"1 USD is equivalent to {usd_to_eur_rate} EUR")





          # if isinstance(eps_diluted_ttm, float):
          #      eps_diluted_ttm = [eps_diluted_ttm]

          # data = pd.DataFrame({
          # 'Date': ['TTM'] * len(eps_diluted_ttm) + list(date_annual_20yrs),
          # 'EPS': [eps_diluted_ttm[0]] * len(eps_diluted_ttm) + eps_diluted_annual_2003
          # })
          

         
          # fig11 = px.bar(data, x='Date', y='EPS', text='EPS',
          #           labels={'value': 'EPS'},
          #           title='EPS Diluted TTM vs EPS Diluted Annual 2003',
          #           hover_data={'EPS': True},
          #           color='Date')
          # # Show the plot
          # st.plotly_chart(fig11, use_container_width=True, config=config)



     
      
                         

with st.container():
     with news:
          try:
               news = stock_info.news[:10]  # Get the top ten news articles

               # Display the news headlines and links
               for i, item in enumerate(news, 1):
                    headline = item['title']
                    link = item['link']
                    st.write(f"Headline: {headline}")
                    st.write(f"{link}")
               

          except Exception as e:    
          
               st.error("No news available for this stock:")
          yf.pdr_override()  # Clear the cached data


          # links = quote.outer_news_df[['title', 'link']].head(10)

          # # Display the headlines and links
          # for i, row in links.iterrows():
          #      headline = row['title']
          #      link = row['link']
          #      st.write(f"Headline: {headline}")
          #      st.write(f"Link: {link}")



        #  link = quote.outer_news_df  # Assuming outer_news_df contains the link information


#          st.write(f"[{link}]({link})")        
          



#if st.sidebar.button("Open SEC Link 10K"):
#cik = "your_cik_here"  # Replace with your CIK value


        
           

#--------------------------------------------------------------------------


          
          #stock = finvizfinance(ticker)      
          #stock_description = stock.ticker_description()
          #inside_trader_df = stock.ticker_inside_trader()
          #print("inside_trader_df:",inside_trader_df)
          #print("stock_description:",stock_description)


          

# available variables:
          #print("Does Data exist:",quote.exists) 
          #st.write("Fundamental",quote.fundamental_df)
          

# Display the "Market Cap" using Streamlit

          #try:
          st.write("Fundamental",quote.fundamental_df)
            #   st.write("Market Cap:", quote.fundamental_df.at[0, "Market Cap"])
             #  st.write("Forward P/E:", quote.fundamental_df.at[0, "Forward P/E"])

#               st.write("RSI",quote.fundamental_df.at[0, "RSI (14)"] )
                   
 #         except KeyError:
  #              print("")
          #st.write("RSI",RSI)    
         
          #col2.write(f'10 years T.Note",{Average_10years_treasury_rate}')

          
          #period_end_price=annual_data['period_end_price'][-11:]
          #st.write(period_end_price)    

           #with news:
         
          #for i in range(10):
          #    st.subheader(f'News {i+1}')
               #st.write("me")
   



          #print(f"Beta of {ticker}: {Average_stock_market_beta}")                
          #print("5 years FCF Average:",average_fcf_Annual_funf)
          #print("sum_discounted_values",discounted_values)
          #print("total debt in prozent:",Total_debt_prozent)
          #print("Marketcap_in_prozent:",Marketcap_in_prozent )
          #print("Cost_of_debt_after_Tax:", Cost_of_debt_after_Tax)
          #print("cost of Equity",Cost_of_equity)
          #print("Cost_of_debt",Cost_of_debt)
          #print("WACC:",WACC_prozent)
          #print("Debt_equity_last_quater",Debt_equity_last_quater)
          #print("Historical_marketkap",Historical_marketkap)
          #print("npv-result:",rounded_npv_result)
          #print("npv-result2:",rounded_npv_result2)
          # print("Enterprise_value",Enterprise_value)
          # print("shares_diluted_ttm:",shares_diluted_ttm)
          # print("shares_basic_ttm",shares_basic_ttm)
          # print("shares_eop_ttm",shares_eop_ttm)
          # print("shares_eop_change_ttm",shares_eop_change_ttm)
          # print("shares_eop_annual",shares_eop_annual)
          # print("shares_eop_quarter",shares_eop_quarter)
          # print("shares_basic_quarter",shares_basic_quarter)
          # #print("shares_diluted_quarter",shares)
          # print("last 5 year price",(annual_data['period_end_price'][-5:]))
          # print("period_end_price_ttm",period_end_price_ttm)
          # print("interest_expense_yr ",interest_expense_yr)
          # #print("average_Dividend_growth_4yrs_percentage",average_Dividend_growth_4yrs_percentage)
          #print(f"The current 10-year Treasury yield is: {Average_10years_treasury_rate:.2f}")
          # print("Total cash",Total_cash_last_years)
          # #st.(WACC_prozent)
          # #print("Intrinsic_Value_DDM",Intrinsic_Value_DDM)
          # print("Total Debt",Total_DEbt_in_billion)
          #print("Total Discounted value:",discounted_values)
          #print("Total Discounted value2:",discounted_values2)
          # print("Terminal value:",Terminal_Value)
          # print("Terminal value2:",Terminal_Value2)
          # #print(finnhub_client.company_peers(ticker))
          # #print("Dividend_ttm",Dividend_ttm)
          # print("Debt_equity_ttm:",Debt_equity_ttm)
          # #print("CIK:",cik)
          #print("usage:",usage)
          # #print("EPS_ttm",eps_diluted_ttm)
         
         # hide_streamlit_style = """
          #  <style>
            #MainMenu {visibility: hidden;}
          #  footer {visibility: hidden;}
          #  </style>
         #   """
         # st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#          st.markdown('''
 #         <style>
  #        .stApp [data-testid="stToolbar"]{
   #       display:none;
    #      }
     #     </style>
#''', unsafe_allow_html=True)
          
 #    hide_streamlit_style = """
  #  <style>
    #MainMenu {visibility: hidden;}
   # footer {visibility: hidden;}
    #.streamlit-container .element-container:nth-child(2) .stPlot {display: none;}
    #</style>
#"""

# Apply the CSS styles using st.markdown
#st.markdown(hide_streamlit_style, unsafe_allow_html=True)