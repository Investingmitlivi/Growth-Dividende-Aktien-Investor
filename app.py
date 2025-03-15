
import google.auth.transport.requests
import requests, json, time
import streamlit as st, pandas as pd, numpy as np, yfinance as yf
from streamlit.components.v1 import html
import plotly.express as px
import plotly.graph_objs as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import firebase_admin
import os
import secrets
import math




from typing import List, Dict, Union
from datetime import datetime, timedelta, date, timezone
from numpy_financial import npv
from firebase_admin import credentials,firestore,auth
from pandas_datareader import data
from pyfinviz.quote import Quote
from stocknews import StockNews
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
from typing import Dict,Any,Union
from itsdangerous import URLSafeTimedSerializer
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from fpdf import FPDF
from PIL import Image
from scipy import optimize



#st.set_page_config(page_title="Verstehdieaktie", page_icon="📘", layout="wide")
st.set_page_config(page_title="Verstehdieaktie", page_icon="VA.png", layout="wide")



st.markdown("""
<style>
/* Target all number inputs in the form */
div[data-testid="stNumberInput"] input::-webkit-outer-spin-button,
div[data-testid="stNumberInput"] input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
 
div[data-testid="stNumberInput"] input[type=number] {
    -moz-appearance: textfield;
}
</style>
""", unsafe_allow_html=True)


hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
    #stHeaderLogo {
        visibility: hidden;
    }
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)




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


cred = credentials.Certificate('verstehdieaktie-firebase.json')

secret_key = secrets.token_hex(32)  
#cred = credentials.Certificate('.streamlit/investingmitlivi-firebase key.json')

# cred = credentials.Certificate({
#     "type": "service_account",  # Add this line
#     "project_id": os.getenv("PROJECT_ID"),
#     "private_key_id": os.getenv("PRIVATE_KEY_ID"),
#     "private_key": os.getenv("-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCs+Qkt9XOTgQGs\niMsuHdBHF32nWHHYBe9ztGIe/regG4hifHo0CvhwOlsQp7kEgZFlooYJk4oWFL7w\n+tfeYqhGmdoVbcYJxC5H+uVNYhM+I0bK9GkVPjCEdZH33VqhdTBpDTCDWbKzQeMD\nsjBwpSnu5A6lV1QJt0UsQPQlw3N3qTdBljejv9OKiUoPWg79edHIHKE6TF0PEfy5\nLiZF+LEdrot9IN+Yx7XOkutmZLttUkl1mHJdQrIqJlyRrp304Jt4N5oP82LgQQyS\nlXcAt22Rn2nvPv5V8gCVYfzjt96Q3pcDrv5pINor4XwSkGuEwxEThhSieeRAkU2V\naRDR8V4NAgMBAAECggEAB4mMVKF36ylSZnaCMHzsidOg46RbqLl+0eev5Rz6Ihnt\ne0YPGLiSjC+ey1s4/PEOqR/IHFh+n7AkoP3Q0PLd1WzbvYEVgampsp8LjK/pKBUg\nG3vuHohoxUP5Ys0x0gwxBPSl9MGHo0XTDX9KDKIbKldPDrzw/2xGlO35bnkq+Aa2\nNmb+spWMmDC3SalKA4xccMw674wvFBK7XeiCHjkmVbJ8qBA3H9fBo4ApCxAjDTcm\n28xkNBvhD6t+G37QbxFgZlCNw91l7HLejpjCSPt8TnuXxp/ee5/nGtPfAQlL8OmH\nqycsFADWV7OB3ayhJ3PmIYJyW4c4ahCoT2ArA+mOaQKBgQDz7T2/kdwpskRzpaJo\nvwQvH1TS5ABd9mbzGMwknk9bfoE1ySa93SaTk4SQtVbNcaTToVroHvQM1eM/TUp3\nj/BaRuL4ZxEbB/hD3lmCvPFy8ThoQKbgLcIpxQsVi48h4lCtl/do5X3gDDZkA17k\n9mg3Biou9Kw5uVd5sARis30YjwKBgQC1iL+E+fFIeegseeGNOnEYL81ZEHlrTVXY\n8V8TZf0wrDsq9ruN4HahNixyB03203/V3GU4w1Rq4fKikS6rYAPiZe9oWbHaRnQ4\nbUxjqgbOAdfaidUnqieBtQpYCKEChleYj7zpeVC7zbVaITeRJX92nyBOe8z0Qj6J\nAu68IskVowKBgGcERNXJJjA954bn5wVR1tSH6Oz/+d+1FpmIWX8FlQJRFQTAJSp+\nYbJl1NDApR4y5qeyN5BcsjlRg53SaKbCFYIq+eRqsuC1pvYSy77ZSSeAFJCC7Xc0\nHBJD84Bv5k0rJWOLEKQud9DNl5L5kXQlVLIYWmxmTO48BmOQIOoGX8ilAoGBAJnD\n8zXX4KDbYeYKdxsBXbp3AyFl6vMQ1p6kFTyBLy2DNbr2s3dBojp7gLo1pbxk+etU\nfAjQqzi9mqBJCZbwBVpHrbpd/2A8PUVujz38TzdAKG5cQckPP9eGWfSnmnphAOGh\nHwtETzZE0FA/wqmXcZgwwVS5WKmtUvsLGN0TOfCxAoGAXY3A+q17zNKoY3S3+UUg\n7RrI0qfwmnwIVY/dGmL05Mm4gvyc1Gyhz1VOwjp33TuUFI4LPJji9YcoEIRf69sP\nNzVHS/aR2z7TFE0fguja+Uikv4QkeAlWs2ozbqsmrPoSYbg20KS3MKrpVVbIO8sh\nIA7tnJBZjpJqVTh38Npyol8=\n-----END PRIVATE KEY-----\n"),
#     "client_email": os.getenv("CLIENT_EMAIL"),
#     "client_id": os.getenv("CLIENT_ID"),
#     "auth_uri": os.getenv("AUTH_URI"),
#     "token_uri": os.getenv("TOKEN_URI"),
#     "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
#     "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL")
# })

try:
     firebase_admin.initialize_app(cred)

except ValueError:
      
     print(" ")


fig = go.Figure()


config = {'displayModeBar': False}

global ticker, name, symbol

base_currency = "USD"  # Example
target_currency = "EUR"  # Example


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


selected = option_menu(
     menu_title= None, #required
     options=["Home","Stock Analysis Tool","Contacts"], #required
     icons=["house","graph-up","envelope"],
     menu_icon="cast", #optional
     default_index=0,
     orientation="horizontal", 
     
)

if selected == "Home":

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
          st.write("[Youtube Channel >](https://www.youtube.com/@Verstehdieaktie)")
#########################################################################################################################
          #right,left = st.columns(2, gap="small")
          col1,col2 = st.columns(2)
          # Load the PDF document
          pdf_file_path = 'Key_Financial_Ratios_Verstehdieaktie.pdf'
          # Download button for the PDF
          

          with col1:
               #st.image('Key_Financial_Ratios_Verstehdieaktie.png', use_container_width=True)
               st.image('Key_Financial_Ratios_Verstehdieaktie.png')
               with open(pdf_file_path, 'rb') as pdf_file:
                    pdf_data = pdf_file.read()
                    st.download_button(
                         label=" 📁 " 'Download',
                         data=pdf_data,
                         file_name="Key_Financial_Ratios_Verstehdieaktie.pdf",  # This will be the name of the downloaded file
                         mime="application/pdf"  # MIME type for PDF files
                    )

#########################################################################################################################
          pdf_file_path = 'DCF Update.png'
          with col2:
               #st.image('DCF Update.png',use_container_width =True)
               st.image('DCF Update.png')
               with open(pdf_file_path, 'rb') as pdf_file:
                    pdf_data = pdf_file.read()
                    st.download_button(
                         label=" 📁 " 'Download',
                         data=pdf_data,
                         file_name="DCF Update.png",  # This will be the name of the downloaded file
                         mime="application/png"  # MIME type for PDF files
                    )
#########################################################################################################################

          col1,col2 = st.columns(2)
          pdf_file_path = 'Verstehdieaktie_Financial_Ratios_calculation.pdf'
          with col1:
               #st.image('Verstehdieaktie_Financial_Ratios_calculation.jpg',use_container_width =True)
               st.image('Verstehdieaktie_Financial_Ratios_calculation.jpg')
               with open(pdf_file_path, 'rb') as pdf_file:
                    pdf_data = pdf_file.read()
                    st.download_button(
                         label=" 📁 " 'Download',
                         data=pdf_data,
                         file_name="Verstehdieaktie_Financial_Ratios_calculation.pdf",  # This will be the name of the downloaded file
                         mime="application/pdf"  # MIME type for PDF files
                    )

                    



#########################################################################################################################
          col1,col2 = st.columns(2)
          # Function to format currency
          def format_currency(amount):
               return f"€ {amount:,.2f}"

          # Function to calculate the future value of an investment for each year
          def calculate_investment_over_time(initial_investment, annual_contribution, years, annual_return, compounding_frequency):
               rate_per_period = (annual_return / 100) / compounding_frequency
               ending_balances = []
               returns = []
               
               # Calculate the balance and return for each year
               for year in range(1, years + 1):
                    periods = year * compounding_frequency
                    
                    # Future value of initial investment (compound interest formula)
                    future_value_initial = initial_investment * (1 + rate_per_period) ** periods
                    
                    # Future value of regular contributions (future value of series formula)
                    future_value_contributions = annual_contribution * (((1 + rate_per_period) ** periods - 1) / rate_per_period)
                    
                    # Total future value (ending balance)
                    ending_balance = future_value_initial + future_value_contributions
                    ending_balances.append(ending_balance)
                    
                    # Expected return is the difference between this year's balance and last year's balance
                    if year > 1:
                         annual_return_value = ending_balance - ending_balances[-2] - annual_contribution
                    else:
                         annual_return_value = ending_balance - initial_investment
                    
                    returns.append(annual_return_value)
               
               return ending_balances, returns

               # Function to create and save chart as PDF
          def create_chart_pdf(periods, ending_balances, returns):
               # Create the bar plot with Plotly Express
               fig2 = px.bar(x=periods, 
                              y=ending_balances, 
                              labels={'x': 'Years', 'y': 'Ending Balance (€)'},
                              title='Ending Balance Over Time', 
                              text=[format_currency(balance) for balance in ending_balances])  # Format text


                              
               fig2.add_bar(x=periods, y=returns, name='Expected Return (€)', 
                              text=[format_currency(return_value) for return_value in returns])  # Format text for returns

               
               # Save the chart as a static image (PNG) to embed in the PDF
               fig2.write_image("investment_growth_chart.png")
               
               # Create a PDF with the image
               pdf = FPDF()
               pdf.add_page()
               pdf.image("investment_growth_chart.png", x=10, y=8, w=190)
               pdf.output("investment_growth_chart.pdf", "F")

               # Clean up the image file
               os.remove("investment_growth_chart.png")

               return "investment_growth_chart.pdf"

          with col1:
               st.title("Investment Calculator")
               with st.expander("Click to Expand/minimize for Investment Inputs"):
                    # User inputs
                    initial_investment = st.number_input("Initial Investment Amount (€)", value=20000.0, min_value=0.0, step=100.0)
                    annual_contribution = st.number_input("Additional Contribution (€)", value=1000.0, min_value=0.0, step=100.0)
                    years = st.number_input("Investment Time Horizon (years)", value=10, min_value=1, step=1)
                    annual_return = st.number_input("Expected Annual Return (%)", value=9.0, min_value=0.0, step=0.1)
                    compounding_frequency = st.selectbox("Compounding Frequency", [1, 4, 6, 12], index=2)  # Annually, Quarterly, Semi-annually, Monthly
               
               # Calculate the future value over time
                    if st.button("Calculate"):
                         ending_balances, returns = calculate_investment_over_time(initial_investment, annual_contribution, years, annual_return, compounding_frequency)
                         periods = np.arange(1, years + 1)
                         
                         st.write(f"### Final Investment Balance after {years} years: {format_currency(ending_balances[-1])}")
                         
                         fig2 = px.bar(
                         x=periods,
                         y=ending_balances,
                         text=[format_currency(balance) for balance in ending_balances],
                         labels={'x': 'Years', 'y': 'Ending Balance'},
                         title="Investment Growth Over Time"
                         )

                         # Customize the layout to show the text properly
                         fig2.update_traces(texttemplate='%{text}', textposition='inside')
                         fig2.update_layout(yaxis_tickprefix='€', yaxis_tickformat='.2f')  # To format y-axis ticks

                         fig2.update_layout(
                              dragmode=False,  # Disable dragging for zooming
                              )
                         st.plotly_chart(fig2,use_container_width=True,config={'displayModeBar': False})

                         
                         # Automatically generate the PDF and provide a download link icon
                         pdf_file = create_chart_pdf(periods, ending_balances, returns)
                         with open(pdf_file, "rb") as pdf:
                              st.download_button(
                                   label="📁 Download as PDF file",
                                   data=pdf,
                                   file_name="investment_growth_chart.pdf",
                                   mime="application/pdf",
                                   use_container_width=True
                              )

                         # Explanation of the calculator
                         st.write("""
                         This investment calculator estimates the future value of your investments by taking into account the initial investment, additional contributions, the expected rate of return, and the compounding frequency (e.g., annually, quarterly, or monthly).
                         The chart shows the total ending balance and the expected return at the end of each year using bar charts.
                         """)



#########################################################################################################################

          def calculate_dividends(starting_principal, annual_contribution, dividend_tax_rate, tax_exempt_income,
                        initial_dividend_yield, dividend_increase_rate, share_price_appreciation, years):
               total_investment = starting_principal
               dividends_over_years = []
               total_dividends_before_tax = 0

               current_dividend_yield = initial_dividend_yield

               for year in range(1, years + 1):
                    # Calculate annual dividend before tax based on start-of-year investment
                    annual_dividend = total_investment * (current_dividend_yield / 100)
                    total_dividends_before_tax += annual_dividend
                    
                    # Apply tax exemption and calculate after-tax dividend for display purposes
                    taxable_dividend = max(0, annual_dividend - tax_exempt_income)
                    net_dividend = annual_dividend - (taxable_dividend * dividend_tax_rate / 100)
                    dividends_over_years.append(net_dividend)
                    
                    # Update investment with contributions and appreciation
                    total_investment += annual_contribution
                    total_investment *= (1 + share_price_appreciation / 100)
                    
                    # Update dividend yield for next year
                    current_dividend_yield *= (1 + dividend_increase_rate / 100)

               return total_dividends_before_tax, dividends_over_years
          with col2:
               st.title("Dividend Calculator")
               with st.expander("Click to Expand/minimize for your Inputs"):
                    # User inputs
                    starting_principal = st.number_input("Starting Principal (€)", min_value=0.0, value=100000.0, format="%.2f")
                    annual_contribution = st.number_input("Annual Contribution (€)", min_value=0.0, value=20000.0, format="%.2f")
                    dividend_tax_rate = st.number_input("Dividend Tax Rate (%)", min_value=0.0, value=15.0, format="%.2f")
                    tax_exempt_income = st.number_input("Tax-Exempt Dividend Income Allowed Per Year (€)", min_value=0.0, value=0.0, format="%.2f")
                    initial_dividend_yield = st.number_input("Initial Annual Dividend Yield (%)", min_value=0.0, value=5.0, format="%.2f")
                    dividend_increase_rate = st.number_input("Expected Annual Dividend Amount Increase (%)", min_value=0.0, value=3.0, format="%.2f")
                    share_price_appreciation = st.number_input("Expected Annual Share Price Appreciation (%)", min_value=0.0, value=3.0, format="%.2f")
                    years = st.number_input("Years Invested", min_value=1, value=20)

                    # Button for calculating dividends and plotting
                    if st.button("Calculate Dividends"):
                         total_dividends_before_tax, dividends_over_years = calculate_dividends(
                              starting_principal, annual_contribution, dividend_tax_rate, tax_exempt_income,
                              initial_dividend_yield, dividend_increase_rate, share_price_appreciation, years
                         )
                         
                         # Format the output to include commas and a currency symbol
                         formatted_total_dividends = f"€ {total_dividends_before_tax:,.2f}"
                         st.success(f"Total Dividends (Before Tax) after {years} years: {formatted_total_dividends}")

                         # Create a Plotly chart
                         year_list = list(range(1, years + 1))
                         
                         # Create a bar plot for dividends over years
                         fig = go.Figure()
                         fig.add_trace(go.Bar(
                              x=year_list,
                              y=dividends_over_years,
                              marker=dict(color='royalblue'),
                              text=[f'€ {dividend:,.2f}' for dividend in dividends_over_years],
                              textposition='inside'
                         ))

                         # Customize the layout
                         fig.update_layout(
                              title='Projected Dividends Over the Years (After Tax)',
                              xaxis_title='Years',
                              yaxis_title='Dividends After Tax (€)',
                              yaxis_tickprefix='€',
                              yaxis_tickformat='.2f',
                              template='plotly_white'
                         )

                         # Display the Plotly chart with mode bar hidden
                         st.plotly_chart(fig,use_container_width=True,config={'displayModeBar': False})   

                    # Additional information
                    st.markdown("""
                    ### How It Works:
                    1. Enter the starting principal amount in euros.
                    2. Input the annual contribution you plan to make.
                    3. Specify the dividend tax rate.
                    4. Enter the tax-exempt dividend income allowed per year.
                    5. Input the initial annual dividend yield as a percentage.
                    6. Enter the expected annual dividend amount increase percentage.
                    7. Specify the expected annual share price appreciation.
                    8. Click the "Calculate Dividends" button to see the total dividends before tax you can expect after the specified years.
                    """)


#########################################################################################################################
          st.markdown("---")

#########################################################################################################################

          #st.write("#")
          st.write("Tip: To invest in shares, ETFs, Cryptos and funds, you need a securities account. You can find the best providers in the following overview:"
          )
          st.write("[Trade Republic >](https://ref.trade.re/6q9kgz11)")
          st.write("[Scalable Capital >](https://de.scalable.capital/einladung/b9hqfs)")
          st.write("[Crypto.com >](https://crypto.com/app/7drn8pkx35)")
          st.write(
          """
          Track your portfolio and dividends with this app 
           """
          )
          st.write("[Getquin >](https://getqu.in/xFbQ9n/YqUbcT/)")
          st.write("[open a free current account: N26>](https://n26.com/r/livinuso3606)")
          st.write("[Investing in P2P loans Bondora >](https://bondora.com/ref/livinusc)")

          st.write(
          """
          Track Super Investor portfolio like Warren Buffet, Ruane Cunniff, B.Tweedy, Ch. Browne
           """
          )
          st.write("[Superinvestor Portfolios >](https://valuesider.com/)")
          st.write("[Superinvestor Portfolios 13F fillings >](https://dataroma.com/m/home.php)")
          st.write("[Hedge Fund Manager 13F Portfolio >](https://hedgefollow.com/)")

          st.write(
          """
          S&P 500 PE ratio, Price to Sales ratio, Earnings etc
           """
         )
          st.write("[Shiller PE ratio for the S&P 500 >](https://www.multpl.com/shiller-pe)")

          # Generates a 64-character hexadecimal string
          #st.write("Your secret key:", secret_key)
 

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .login-signup {
        position: fixed;
        top: 0;
        right: 0;
        padding: 10px;
        z-index: 1000;
    }
    </style>
""", unsafe_allow_html=True)


if selected == "Stock Analysis Tool":
     serializer = URLSafeTimedSerializer("secret_key") 
     COOKIE_NAME = "login_token"
     COOKIE_EXPIRY_DAYS = 1  # Token expires in 1 day

     # JavaScript to handle cookies
     def set_cookie(key, value, expiry_days=1):
          expiry_date = (datetime.now(timezone.utc) + timedelta(days=expiry_days)).strftime("%a, %d-%b-%Y %H:%M:%S GMT")
          js_code = f"document.cookie = '{key}={value}; expires={expiry_date}; path=/';"
          # Removed the line to execute JS code to set the cookie in the browser

     def get_cookie(key):
          js_code = f"""
          <script>
               let cookie = document.cookie;
               let value = cookie.split('; ').find(row => row.startsWith('{key}=')).split('=')[1];
               window.parent.postMessage(value, "*");
          </script>
          """
          # Removed the line to execute JS code to retrieve cookie value

     def delete_cookie(key):
          js_code = f"document.cookie = '{key}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';"
          # Removed the line to execute JS code to delete the cookie


     def app():


     # Usernm = []
          #st.title('Welcome to verstehdieaktie')
          
          if 'username' not in st.session_state:
               st.session_state.username = ''
          if 'useremail' not in st.session_state:
               st.session_state.useremail = ''  
          if 'is_logged_in' not in st.session_state:
               st.session_state.is_logged_in = False
          if 'needs_rerun' not in st.session_state:
               st.session_state.needs_rerun = False

          # Check for login token in cookies
          cookie_token = get_cookie(COOKIE_NAME)
          if cookie_token and 'login_token' not in st.session_state:
               try:
                    user_data = serializer.loads(cookie_token, max_age=86400)  # 24-hour expiry
                    st.session_state.username = user_data['username']
                    st.session_state.useremail = user_data['email']
                    st.session_state.is_logged_in = True
                    st.session_state.login_token = cookie_token
               except Exception:
                    delete_cookie(COOKIE_NAME)  # Remove invalid/expired cookie


          # Function to sign up with email and password
          def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
               try:
                    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
                    payload = {
                         "email": email,
                         "password": password,
                         "returnSecureToken": return_secure_token
                    }
                    if username:
                         payload["displayName"] = username 
                    payload = json.dumps(payload)
                    r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
                    # try:
                    #      return r.json()['email']
                    # except:
                    #      st.warning(r.json())
                    return r.json().get('email', None)

               except Exception as e:
                    st.warning(f'Signup failed: {e}')

          # # Function to sign in with email and password
          # def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
          #      rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

          #      try:
          #           payload = {
          #                "returnSecureToken": return_secure_token,
          #                "email": email,
          #                "password": password
          #           }
          #           payload = json.dumps(payload)
          #           r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
          #           data = r.json()
          #           user_info = {
          #                'email': data['email'],
          #                'username': data.get('displayName')  # Retrieve username if available
          #           }
          #           return user_info
                  
          #      except Exception as e:
          #           st.warning(f'Signin failed: {e}')
              # Function to sign in with email and password
          def sign_in_with_email_and_password(email=None, password=None):
               rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
               try:
                    payload = {"returnSecureToken": True, "email": email, "password": password}
                    r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, json=payload)
                    data = r.json()
                    if 'email' in data:
                         return {'email': data['email'], 'username': data.get('displayName')}
               except Exception as e:
                    st.warning(f'Sign-in failed: {e}')
               return None

#######################################################################################################
          # Login function
          def login():
               userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)

               if userinfo:
                    st.session_state.username = userinfo['username']
                    st.session_state.useremail = userinfo['email']
                    st.session_state.is_logged_in = True

                    # Create a secure login token
                    login_token = serializer.dumps({'username': userinfo['username'], 'email': userinfo['email']})
                    st.session_state.login_token = login_token
                    # Update query parameters
                    #st.query_params['login_token'] = login_token
                    set_cookie(COOKIE_NAME, login_token, expiry_days=COOKIE_EXPIRY_DAYS)

                    st.session_state.needs_rerun = True
               else:
                    st.warning('Login Failed')
###########################################################################

          def logout():
               for key in ['username', 'useremail', 'is_logged_in', 'login_token']:
                    if key in st.session_state:
                         del st.session_state[key]
               #st.query_params.clear()
               delete_cookie(COOKIE_NAME)  # Remove cookie on logout

               #st.rerun()
               st.session_state.needs_rerun = True
############################# email reset##########################################################
          def reset_password(email):
               try:
                    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
                    payload = {
                         "email": email,
                         "requestType": "PASSWORD_RESET"
                    }
                    payload = json.dumps(payload)
                    r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
                    return r.status_code == 200, r.json().get('error', {}).get('message')

               except Exception as e:
                    return False, str(e)


#####################################################email reeset ########################################################
          def forget():
               email = st.text_input('Email')
               if st.button('Send Reset Link'):
                    print(email)
                    success, message = reset_password(email)
                    if success:
                         st.success("Password reset email sent successfully.")
                    else:
                         st.warning(f"Password reset failed: {message}") 
               
 #############################################################################################################

          right, middle, left = st.columns(3)
          # Check if we need to rerun the app
          if st.session_state.get("needs_rerun"):
               st.session_state.needs_rerun = False
               st.rerun()

          if st.session_state.is_logged_in:

               with left:
                    #st.success(f"Welcome, {st.session_state.username}!")
                    st.button('Sign out', on_click=logout, key='signout_button')

               st.markdown("""
               <style>
               .stSelectbox > div:first-child {
                    width: 100px;  /* Set the width you want for the selectbox */
               }
               </style>
               """, unsafe_allow_html=True)


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
                         'ASHTF':'Ashtead Group PLC',
                         'AI':'C3.ai Inc.  ',
                         'AIB':'AIB Acquisition Corporation ',
                         'AIBBU':'AIB Acquisition Corporation Unit',
                         'AIC':'Arlington Asset Investment Corp ',
                         'AIF':'Apollo Tactical Income Fund Inc. ',
                         'AIG':'American International Group Inc.',
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
                         'FLUT':'Flutter Entertainment plc',
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
                         'HHH':'Howard Hughes Holdings Inc. ',
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
                         'SIEGY':'Siemens Aktiengesellschaft',
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
                         'XYZ':'Block Inc.  ',
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
                         'ZYXI':'Zynex Inc. ',
                         'NPSNY':'Naspers Ltd.',
                         'EHMEF':'goeasy Ltd',
                         'CNSWF':'Constellation Software Inc.',
                         'SDZNY':'Sandoz Group AG',
                         'EVVTY':'Evolution AB (Publ)',
                         'RHHBY':'Roche Holding AG',
                         'WOLTF':'Wolters Kluwer N.V',
                    }
 
               ticker_symbol_name = {f'{name} : {symbol}': symbol for symbol, name in ticker_symbol_name.items()} 

               with right:   
                    # #selected_ticker = st.selectbox('Select a ticker', list(ticker_symbol_name.keys()), key='symbol')  
                    # selected_ticker = st.selectbox(
                    # 'Select a ticker',
                    # options=list(ticker_symbol_name.keys()),
                    # key='symbol'
                    selected_ticker = st.selectbox('Select a ticker', options=ticker_symbol_name.keys(), key='symbol')

                    #help='Start typing to search for a ticker'
                    #)
  


               if selected_ticker:
                    ticker = ticker_symbol_name.get(selected_ticker) 
                    name, symbol = selected_ticker.split(' : ')

               #............................... api key.................
          
               load_dotenv()

               api_key = os.getenv("api_key")
               base_url = os.getenv("base_url")


               if not api_key or not base_url:
                    st.error("API_KEY or BASE_URL not found in environment variables.")
                    st.stop()
               header = {'x-qfs-api-key': api_key}
               
               def clear_cache():
                    st.cache_data.clear()

               @st.cache_data(show_spinner=False,ttl=3600) #for caching results for an hour.
               def fetch_data_from_api(ticker):
                    try:
                         url = f"{base_url}{ticker}?api_key={api_key}"
                         response = requests.get(url, headers=header)
                    
          
                         if response.status_code == 200:
                              return response.json()
                         # Continue processing the data as required
                         else:
                              st.error(f"Error fetching data:")
                              clear_cache()  # Clear the cache if there is an error
                              return  None

                    except Exception as e:
                         st.error(f"An error occurred:")
                         clear_cache()  # Clear the cache in case of an exception
                         return None


               data= fetch_data_from_api(ticker)
               #data = response.json()
               #usage = response.json()
               #st.write(data)
               #st.write(usage)
               #response.json()
               
               #--------------------------------------------------------------
               Financial_data = data['data']['financials']
               annual_data = Financial_data['annual']
               quarterly_data = Financial_data['quarterly']
               eps_diluted_ttm = Financial_data['ttm']['eps_diluted']
               fcf_per_share = Financial_data['ttm']['fcf_per_share']
               Dividend_ttm = Financial_data['ttm']['cff_dividend_paid'] 
               fcf_ttm = Financial_data['ttm']['fcf']/1000000000 
               ROE_TTM =Financial_data['ttm']['roe']*100  
               ROIC_TTM =Financial_data['ttm']['roic']*100   
               EBITDA_MARGIN_TTM =Financial_data['ttm']['ebitda_margin']*100   
               ROA_TTM =Financial_data['ttm']['roa']*100          
               netincome_ttm = Financial_data['ttm']['net_income']/1000000000
               revenue_ttm = Financial_data['ttm']['revenue']/1000000000
               shares_eop_ttm=(Financial_data['ttm']['shares_eop'])/1000000000
               current_Operating_cash_Flow =Financial_data['ttm']['cf_cfo']
               Revenue_ttm = (Financial_data['ttm']['revenue'])
               date_quarter = quarterly_data['period_end_date'][-10:] 
               date_annual = annual_data['period_end_date'][-10:] 
               Stock_description=data["data"]["metadata"]["description"]
               stock_sector=data["data"]["metadata"]["sector"]
               cik=data["data"]["metadata"]["CIK"]
               Net_Purchases_of_Property_Equipment =annual_data['cfi_ppe_purchases'][-5:] 
               Net_Purchases_of_Property_Equipment =annual_data['cfi_ppe_purchases'][-5:] 
               date_list_quarter = [period_end_date for period_end_date in date_quarter]
               date_list_annual = [period_end_date for period_end_date in date_annual]

               shares_basic_annual_one = annual_data['shares_basic'][-1:]
               shares_basic_annual_funf_unpacked = annual_data['shares_basic'][-5:]
               Average_shares_basic_annual_one = (sum(shares_basic_annual_one) / len(shares_basic_annual_one)) / 1000000000
               
               #---------------------------pyfinanz-----------------------------------
               try:

                    quote = Quote(ticker)
                  

               except Exception:
                    st.write()
                  
               
               #--------------------------10K-----------------------------------

               link = f"https://www.sec.gov/edgar/browse/?CIK={cik}&owner=exclude"

               styled_link = f'<div style="display: flex; justify-content: center;"><a href="{link}" style="color: green; font-family: serif;" target="_blank">Annual/Quarterly Reports &rarr;</a></div>'
          


               

               st.text("")


               right, middle, left = st.columns(3, gap="small")
               with right:
                    st.write(f"Sector: {stock_sector}", unsafe_allow_html=True)

               with left:
                    st.write(styled_link, unsafe_allow_html=True)
               #.............................................................................................
               
               ticker_mapping = {
               'ADS:DE': 'ADS.DE',
               'BRK.A': 'BRK-A',
               'BRK.B': 'BRK-B'
               }

               # Use the dictionary to get the correct ticker or fallback to the original one
               ticker = ticker_mapping.get(ticker, ticker)

               stock_info = yf.Ticker(ticker)


          ###########################################################################################################

               #@st.cache_data(show_spinner=False)
               def get_current_price(ticker):
                    stock_info = yf.Ticker(ticker)
                    #quote = Quote(ticker)
                    try:
                         current_price = stock_info.history(period="1d", interval="1m")["Close"].iloc[-1]
                         #fundamental_df = quote.fundamental_df
                         
                    except Exception:
                         try:
                              # Fallback to previous close
                              current_price = float(stock_info.info["previousClose"])
                              
                         except Exception:
                              try:
                                   current_price = stock_info.history(period="2d", interval="1d")["Close"].iloc[-1]

                              except Exception:
                                   
                                   current_price = float(quote.fundamental_df.at[0, "Price"])
                                   current_price = float(current_price.replace(',', ''))
                              except Exception:
                                   current_price =  None


                    return current_price
#--------------------------------------------------percentage_difference-----------------------------

               start_date = datetime.now() - timedelta(days=39 * 365)
               end_date=datetime.now() 
               # Function to format date
               def format_date(date):
                    return date.strftime('%Y/%m/%d')


               def get_price_data(ticker, current_price, usd_to_eur_rate):
                    start_date = datetime.now() - timedelta(days=39 * 365)
                    end_date=datetime.now() 
               
                    try:
                         data = yf.download(ticker, start=start_date, end=end_date)
                         close_price = round(data['Close'][-2], 2)
                         percentage_difference =round(((float(round(current_price,2))) - (float((close_price)))) / (float((close_price))) * 100,2)
                         
                         converted_amount = "{:.2f}".format(current_price * usd_to_eur_rate)
                    except Exception as e:
                         close_price = None
                         percentage_difference = None
                         converted_amount = None
                    
                    return close_price, percentage_difference, converted_amount
   #-------------------------------------------------------------------------------
                 

               def convert_to_eur(usd_price, conversion_rate=usd_to_eur_rate):
                    return float(usd_price) * float(conversion_rate)

               def main():

                    if ticker not in st.session_state or st.session_state.ticker != ticker:
                         st.session_state.ticker = ticker
                         st.session_state.current_price = get_current_price(ticker)
                         st.session_state.converted_amount = convert_to_eur(st.session_state.current_price)

                    display_price_analysis()

               def display_price_analysis():
                    st.write("")


               if __name__ == "__main__":
                    main()

               current_price = st.session_state.current_price
               amount = current_price 
               
          ########################################################################################################     

               # start_date = datetime.now() - timedelta(days=39 * 365)
               # end_date=datetime.now() 
               # # Function to format date
               # def format_date(date):
               #      return date.strftime('%Y/%m/%d')


               # def get_price_data(ticker, current_price, usd_to_eur_rate):
               #      start_date = datetime.now() - timedelta(days=39 * 365)
               #      end_date=datetime.now() 
               
               #      try:
               #           data = yf.download(ticker, start=start_date, end=end_date)
               #           close_price = round(data['Close'][-2], 2)
               #           percentage_difference =round(((float(round(current_price,2))) - (float((close_price)))) / (float((close_price))) * 100,2)
                         
               #           converted_amount = "{:.2f}".format(current_price * usd_to_eur_rate)
               #      except Exception as e:
               #           close_price = None
               #           percentage_difference = None
               #           converted_amount = None
                    
               #      return close_price, percentage_difference, converted_amount
               


               

               # Main function to run the app
               def main():

                    if ticker not in st.session_state or st.session_state.ticker != ticker:
                         st.session_state.ticker = ticker
                         st.session_state.current_price = get_current_price(ticker)  # Define this function as needed
                         st.session_state.price_data = get_price_data(ticker, st.session_state.current_price, usd_to_eur_rate)

                    current_price = st.session_state.current_price
                    close_price,percentage_difference,converted_amount= st.session_state.price_data
                    converted_amount = "{:.2f}".format(current_price * usd_to_eur_rate)

                    green_style = "color: green;"
                    red_style = "color: red;"

                    formatted_price_usd = f"{current_price:.2f} $"
                    formatted_price_eur = f"{converted_amount} €"

                    percentage_text = ""
                    if percentage_difference is not None:
                         if percentage_difference > 0:

                              percentage_text = f"(<span style='{green_style}'>+{percentage_difference}%</span>)"

                         elif percentage_difference < 0:
                              percentage_text = f"(<span style='{red_style}'>{percentage_difference}%</span>)"

                         else:
                                   percentage_text = "(0%)"  # In case of zero percentage difference


                    with st.container():

                         with middle:
 
                              st.markdown(
                              f"""
                              <div style="text-align: center; width: 100%;">
                                   Current Price: <span style='{green_style}'>{formatted_price_usd}</span> &nbsp;&nbsp;
                                   Aktueller Preis: <span style='{green_style}'>{formatted_price_eur}</span> &nbsp;&nbsp;
                                   {percentage_text}
                              </div>
                              """,
                              unsafe_allow_html=True,
                         )


               if __name__ == "__main__":
                    main()

               current_price = get_current_price(ticker)  # Get current price
               converted_amount = "{:.2f}".format(current_price * usd_to_eur_rate)


               ########################
          
               def format_date(date):
                    return date.strftime('%Y/%m/%d')

          
               def get_all_time_high_and_low_date(ticker):
                    stock_info = yf.Ticker(ticker)
                    data = stock_info.history(period="max", actions=False)

                    # Get all-time high date and price
                    all_time_highs = data[data['Close'] == data['Close'].max()]
                    if not all_time_highs.empty:
                         first_all_time_high = all_time_highs.iloc[0]
                         all_time_high_date = first_all_time_high.name
                         all_time_high_price = first_all_time_high['Close']
                    else:
                         all_time_high_date, all_time_high_price = None, None

                    # Get 52-week low date and price
                    fifty_two_week_low_data = data.iloc[-260:]  # Last 52 weeks
                    fifty_two_week_low = fifty_two_week_low_data['Close'].min()
                    fifty_two_week_low_date = fifty_two_week_low_data[fifty_two_week_low_data['Close'] == fifty_two_week_low].index[0] if not fifty_two_week_low_data.empty else None

                    return all_time_high_date, all_time_high_price, fifty_two_week_low_date, fifty_two_week_low
               
          

               # Streamlit App
               def main():
                    
                    if ticker not in st.session_state or st.session_state.ticker != ticker:
                         st.session_state.ticker = ticker
                         (
                              st.session_state.all_time_high_date,
                              st.session_state.all_time_high_price,
                              st.session_state.fifty_two_week_low_date,
                              st.session_state.fifty_two_week_low
                         ) = get_all_time_high_and_low_date(ticker)

                    # Access all_time_high_date and fifty_two_week_low_date from session state
                    all_time_high_date = st.session_state.all_time_high_date
                    all_time_high_price = st.session_state.all_time_high_price
                    fifty_two_week_low_date = st.session_state.fifty_two_week_low_date
                    fifty_two_week_low = st.session_state.fifty_two_week_low

               
                    if all_time_high_date and all_time_high_price:
                         formatted_high_date = format_date(all_time_high_date)
          
                    if fifty_two_week_low_date and fifty_two_week_low:
                         formatted_low_date = format_date(fifty_two_week_low_date)

                    display_price_analysis()

               # Example function using session state values
               def display_price_analysis():
                    st.write("")
               

               if __name__ == "__main__":
                    main()
          

               all_time_high_price,fifty_two_week_low,all_time_high_date,fifty_two_week_low_date=get_all_time_high_and_low_date(ticker)

          ###########################################################################################################################


               start_date_input=start_date

               if start_date_input is None:
               # Set the default start date to "2002-03-04"
                    #start_date_input = start_date
                    start_date_input = start_date


               #data = yf.download(ticker,start=start_date_input, end=end_date) decemeber



              # data['Adj Close'] = data['Adj Close'].round(2) december

          ############################################################################################################
               
               @st.cache_data(show_spinner=False,ttl=3600)
               def calculate_stock_performance(ticker):
                    periods = {
                         "1mo": "1 Month",
                         "3mo": "3 Months",
                         "6mo": "6 Months",
                         #"1y": "1 Year",
                         "2y": "2 Years",
                         "5y": "5 Years",
                         "10y": "10 Years",
                         "max": "MAX"
                    }

                    #stock = yf.Ticker(ticker)
                    performances = {}
                    
                    for period, label in periods.items():
                         try:
                              hist = stock_info.history(period=period)
                              if len(hist) > 0:
                                   start_price = hist['Close'].iloc[0]
                                   end_price = hist['Close'].iloc[-1]
                                   performance = ((end_price - start_price) / start_price) * 100
                                   performances[label] = f"{performance:.2f}%"
                              else:
                                   performances[label] = "No data"
                         except Exception as e:
                              performances[label] = f"Error: {str(e)}"
                    
                    # Store the performances in session state
                    st.session_state[f'{ticker}_performances'] = performances
                    return performances
          
               def get_detailed_data(ticker, period):
                    stock_info = yf.Ticker(ticker)
                    detailed_data = stock_info.history(period=period)
                    return detailed_data
          

               def create_figure(detailed_data):
               
                    fig = go.Figure()

                    # Add the area fill
                    fig.add_trace(go.Scatter(
                         x=detailed_data.index,
                         y=detailed_data['Close'],
                         fill='tozeroy',
                         fillcolor='rgba(34, 139, 34, 0.2)',  # Very light green, adjust as needed
                         line_color='rgba(0, 0, 0, 0)',  # Transparent line for fill
                         showlegend=False
                    ))

                    # Add the line trace
                    fig.add_trace(go.Scatter(
                         x=detailed_data.index,
                         y=detailed_data['Close'],
                         line=dict(color='rgba(34, 139, 34, 0.7)', width=4),  # Darker green line, adjust as needed
                         #name=None
                         showlegend=False  # Hide legend
                    ))

                    # Update the layout
                    fig.update_layout(
                         xaxis_title='Date',
                         #yaxis_title='Price ($)',
                         plot_bgcolor='white',  # White background
                         paper_bgcolor='white',  # White surrounding area
                         xaxis=dict(
                              showgrid=True,
                              gridcolor='lightgrey',
                              showline=True,
                              linecolor='lightgrey'
                    ),
                    yaxis=dict(
                         showgrid=True,
                         gridcolor='lightgrey',
                         showline=True,
                         linecolor='lightgrey',
                         tickprefix='$'  # Add dollar sign prefix to y-axis ticks
                    ),
                    margin=dict(l=40, r=40, t=40, b=40),
                    showlegend=False  # Hide legend
                    )

                    fig.update_traces(
                    hovertemplate='Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'
                    )
                    fig.update_layout(
                    dragmode=False,  # Disable dragging for zooming
                    hoverlabel=dict(
                         bgcolor='rgba(139, 57, 34, 0.76)',  # Dark green background
                         font_size=15,                      # Font size
                         font_color='white'                 # Font color
                    )
                    )

                    return fig

               def display_stock_chart():
                    if 'previous_ticker' not in st.session_state or st.session_state.previous_ticker != ticker:
                         st.session_state.selected_period = None
                         st.session_state.previous_ticker = ticker

                    with st.container():
                         if f'{ticker}_performances' not in st.session_state:
                              performances = calculate_stock_performance(ticker)
                              st.session_state[f'{ticker}_performances'] = performances

                         else:
                              performances = st.session_state[f'{ticker}_performances']

                         options = [f"{period} ({perf})" for period, perf in performances.items()]
                         
                         
                         if 'selected_period' not in st.session_state:
                              st.session_state.selected_period = "5 Years" if "5 Years" in performances else "MAX"


                         try:
                              default_index = options.index(f"5 Years ({performances['5 Years']})" 
                                   if "5 Years" in performances 
                                   else f"MAX ({performances['MAX']})" 
                                   if f"MAX ({performances['MAX']})" in options 
                                   else 0
                              )
                         except ValueError:
                              default_index = 0

                         selected = option_menu(
                              menu_title=None,
                              options=options,
                              icons=["None"] * len(options),
                              menu_icon="cast",
                              default_index=default_index,
                              orientation="horizontal",
                              key=f"option_menu_{ticker}"
                         )

                         # Update selected period
                         st.session_state.selected_period = selected.split(" (")[0]


                         period_mapping = {
                              "1 Month": "1mo", 
                              "3 Months": "3mo", 
                              "6 Months": "6mo", 
                              #"1 Year ": '1y', 
                              "2 Years": "2y", 
                              "5 Years": "5y", 
                              "10 Years": "10y", 
                              "MAX": "max"
                         }
                         

                         detailed_data = get_detailed_data(ticker, period_mapping[st.session_state.selected_period])

                         fig = create_figure(detailed_data)

               
                         st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
               #@st.cache_data
               #@st.fragment
               def main():
         
                    if ticker:
                         display_stock_chart()          
               # Run the app
               if __name__ == "__main__":
                    main()


          ###############################################################################################

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


          ############################################################################################################


           
               # st.markdown(
               #      """
               #      <style>
               #      .stTabs > div > div > div > button {
               #           flex: 1;
               #           text-align: center;
               #      }
               #      </style>
               #      """,
               #      unsafe_allow_html=True
               #      )

               st.markdown(
                    """
                    <style>
                    /* Expand main content area to full width */
                    .main {
                         max-width: 100%;
                         padding-left: 1rem;
                         padding-right: 1rem;
                    }

                    /* Make tabs take full width */
                    .stTabs > div > div > div > button {
                         flex: 1;
                         text-align: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                         )
                                                            
               tabs = ["Key Statistics", "Financials", "12 Pillar Stock Screener", "Discounted Cash Flow (DCF)", 
                    "Reversed DCF (rDCF)", "Multiple of Earnings Valuation", "Charts", "Key Ratios", "Calculator", "Top 10 News"]

               # Create tabs
               Metric, Financials, Pillar_Analysis, Stock_Analyser, Reversed_DCF, Multiple_Valuation, Charts, Key_ratios, Retirement_Calculator, news = st.tabs(tabs)
                         

               with st.container():

                    with Metric:  

                         #@st.cache_data(show_spinner=False)
                         def get_market_cap(stock_info, ticker):
                         #stock_info = yf.Ticker(ticker)

                              if f'{ticker}_market_cap' in st.session_state:
                                   return st.session_state[f'{ticker}_market_cap'], st.session_state[f'{ticker}_market_cap_formatted']

                              try:
                                   # Get market capitalization
                                   Marketcap = stock_info.info['marketCap']
                                   Marketcap_in_million=Marketcap
                                   Marketcap =Marketcap /1000000000
                                   Marketcap_in_Billion = (
                                        "{:.2f}T".format(Marketcap / 1000) if abs(Marketcap) >= 1000 else "{:,.2f}B".format(Marketcap / 1)
                                   )
                                   st.session_state[f'{ticker}_market_cap'] = Marketcap
                                   st.session_state[f'{ticker}_market_cap_formatted'] = Marketcap_in_Billion
                                   return Marketcap, Marketcap_in_Billion
                              
                              except Exception as e:

                                   try:

                             # fundamental_df = quote.fundamental_df
                                        
                                        market_cap_original = quote.fundamental_df.at[0, "Market Cap"] 
                                        #print("market_cap",market_cap_original)

                                        try:
                                             Marketcap = float(market_cap_original.replace('B', ''))  
                                             #Marketcap = float(market_cap.replace('B', '').replace('M', '')) 
                                             # Remove 'B' and convert to float

                                             #Marketcap =Marketcap /1000000000
                                             Marketcap_in_Billion = (
                                                  "{:.2f}T".format(Marketcap / 1000) if abs(Marketcap) >= 1000 else "{:,.2f}B".format(Marketcap / 1)
                                             )

                                             st.session_state[f'{ticker}_market_cap'] = Marketcap
                                             st.session_state[f'{ticker}_market_cap_formatted'] = Marketcap_in_Billion
                                             return Marketcap, Marketcap_in_Billion
                                        
                                        except Exception as e:
                                             Marketcap_in_Billion=market_cap_original
                                             st.session_state[f'{ticker}_market_cap'] = None
                                             st.session_state[f'{ticker}_market_cap_formatted'] = Marketcap_in_Billion
                                             return None, Marketcap_in_Billion   
                                             
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

                                             Marketcap_in_Billion = (
                                                  "{:.2f}T".format(Marketcap / 1000) if abs(Marketcap) >= 1000 else "{:,.2f}B".format(Marketcap / 1)
                                             )        

                                             st.session_state[f'{ticker}_market_cap'] = Marketcap
                                             st.session_state[f'{ticker}_market_cap_formatted'] = Marketcap_in_Billion
                                             return Marketcap, Marketcap_in_Billion
                                        
                                        else:
                                             st.write("Insufficient data to calculate market cap.")
                                             return None, "N/A"         
                                                                                

                                        #Marketcap_in_Billion = "{:.2f}B".format(current_price * shares_eop_ttm) 
                                        
                         Marketcap, Marketcap_in_Billion = get_market_cap(stock_info, ticker)
                         Marketcap_in_million =Marketcap
          ###################################################################################################             

                         def calculate_eps_growth(annual_data,quarterly_data, ticker):

                              if f'{ticker}_eps_last' in st.session_state:
                                   return (st.session_state[f'{ticker}_eps_last'],
                                             st.session_state[f'{ticker}_eps_growth_3yrs'],
                                             st.session_state[f'{ticker}_eps_growth_5yrs'],
                                             st.session_state[f'{ticker}_eps_basic_annual_5_unpacked'],
                                             st.session_state[f'{ticker}_eps_growth_10yrs'],
                                             st.session_state[f'{ticker}_eps_basic_annual_10_unpacked'],
                                             st.session_state[f'{ticker}_eps_diluted_annual_10_unpacked'],
                                             st.session_state[f'{ticker}_Eps_diluted_quarterly_10_unpacked'],
                                             st.session_state[f'{ticker}_eps_basic_quarterly_10_unpacked'])
                              
          
                              EPS_last = annual_data['eps_basic'][-1:]
                              EPS_last_average  = ((sum(EPS_last) / len(EPS_last))) 
                              #EPS_last_average_one=EPS_last_average

                              EPS_growth_3years = annual_data['eps_diluted_growth'][-3:]
                              EPS_growth_3years = sum(EPS_growth_3years)/len(EPS_growth_3years)
                              EPS_growth_3years =EPS_growth_3years*100

                              EPS_growth_5yrs = annual_data['eps_diluted_growth'][-5:]
                              EPS_growth_5yrs = (sum(EPS_growth_5yrs)/len(EPS_growth_5yrs))*100
                         

                              #eps_basic_annual_5_unpacked = annual_data['eps_basic'][-5:]
                              eps_basic_annual_5_unpacked = annual_data['eps_basic'][-5:] 

                              EPS_growth_annual_10yrs_unpacked= annual_data['eps_diluted_growth'][-10:]

                              eps_basic_annual_10_unpacked = annual_data['eps_basic'][-10:]

                              eps_diluted_annual_10_unpacked = annual_data['eps_diluted'][-10:]

                              Eps_diluted_quarterly_10_unpacked = quarterly_data['eps_diluted'][-10:]

                              eps_basic_quarterly_10_unpacked =quarterly_data['eps_basic'][-10:] 




                              # Store results in session state
                              st.session_state[f'{ticker}_eps_last'] = EPS_last_average
                              st.session_state[f'{ticker}_eps_growth_3yrs'] = EPS_growth_3years
                              st.session_state[f'{ticker}_eps_growth_5yrs'] = EPS_growth_5yrs
                              st.session_state[f'{ticker}_eps_basic_annual_5_unpacked'] = eps_basic_annual_5_unpacked
                              st.session_state[f'{ticker}_eps_growth_10yrs'] = EPS_growth_annual_10yrs_unpacked
                              st.session_state[f'{ticker}_eps_basic_annual_10_unpacked'] = eps_basic_annual_10_unpacked
                              st.session_state[f'{ticker}_eps_diluted_annual_10_unpacked'] = eps_diluted_annual_10_unpacked
                              st.session_state[f'{ticker}_Eps_diluted_quarterly_10_unpacked'] = Eps_diluted_quarterly_10_unpacked
                              st.session_state[f'{ticker}_eps_basic_quarterly_10_unpacked'] = eps_basic_quarterly_10_unpacked
                         

                              return (EPS_last_average, EPS_growth_3years, EPS_growth_5yrs, eps_basic_annual_5_unpacked,
                                   EPS_growth_annual_10yrs_unpacked,eps_basic_annual_10_unpacked,
                                   eps_diluted_annual_10_unpacked,Eps_diluted_quarterly_10_unpacked,eps_basic_quarterly_10_unpacked)


                         (EPS_last_average, EPS_growth_3years,EPS_growth_5yrs,eps_basic_annual_5_unpacked,EPS_growth_annual_10yrs_unpacked, eps_basic_annual_10_unpacked,
                         eps_diluted_annual_10_unpacked,Eps_diluted_quarterly_10_unpacked,eps_basic_quarterly_10_unpacked
                         ) = calculate_eps_growth(annual_data,quarterly_data, ticker)
          ###################################################################################################             

                         EPS_growth_10yrs = (sum(EPS_growth_annual_10yrs_unpacked)/len(EPS_growth_annual_10yrs_unpacked)*100)
                         Average_eps_basic_annual_five = sum(eps_basic_annual_5_unpacked)/len(eps_basic_annual_5_unpacked) 

                    
          ###################################################################################################             
                         def calculate_fcf_averages(annual_data,quarterly_data, ticker):
                              if f'{ticker}_fcf_last' in st.session_state:
                                   return (st.session_state[f'{ticker}_fcf_last'],
                                        #st.session_state[f'{ticker}_fcf_five_years'],
                                        st.session_state[f'{ticker}_fcf_ten_years'],
                                        st.session_state[f'{ticker}_FCF_annual_five_unpacked'],
                                        st.session_state[f'{ticker}_fcf_ten_years_unpacked'],

                                        st.session_state[f'{ticker}_FCF_quarter_10_unpacked'],

                                        st.session_state[f'{ticker}_fcf_growth_annual_3_unpacked'],
                                        st.session_state[f'{ticker}_fcf_growth_annual_5_unpacked'],
                                        st.session_state[f'{ticker}_fcf_growth_annual_10_unpacked'])

                              FCF_annual1_unpacked =annual_data['fcf'][-1:]



                              FCF_annual_ten =annual_data['fcf'][-10:]
                              rounded_fcf_Annual_ten = float((sum(FCF_annual_ten) / len(FCF_annual_ten)))

                              FCF_annual_five_unpacked =annual_data['fcf'][-5:]

                              FCF_annual_ten_unpacked =annual_data['fcf'][-10:]

                              FCF_quarter_10_unpacked =quarterly_data['fcf'][-10:]

                              fcf_growth_annual_3_unpacked =annual_data['fcf_growth'][-3:]

                              fcf_growth_annual_5_unpacked =annual_data['fcf_growth'][-5:]
                              fcf_growth_annual_10_unpacked =annual_data['fcf_growth'][-10:]


                              st.session_state[f'{ticker}_fcf_last'] = FCF_annual1_unpacked
                              st.session_state[f'{ticker}_fcf_ten_years'] = rounded_fcf_Annual_ten
                              st.session_state[f'{ticker}_FCF_annual_five_unpacked'] = FCF_annual_five_unpacked
                              st.session_state[f'{ticker}_fcf_ten_years_unpacked'] = FCF_annual_ten_unpacked

                              st.session_state[f'{ticker}_FCF_quarter_10_unpacked'] = FCF_quarter_10_unpacked

                              st.session_state[f'{ticker}_fcf_growth_annual_3_unpacked'] = fcf_growth_annual_3_unpacked
                              st.session_state[f'{ticker}_fcf_growth_annual_5_unpacked'] = fcf_growth_annual_5_unpacked
                              st.session_state[f'{ticker}_fcf_growth_annual_10_unpacked'] = fcf_growth_annual_10_unpacked

                              return FCF_annual1_unpacked, rounded_fcf_Annual_ten,FCF_annual_five_unpacked,FCF_annual_ten_unpacked,FCF_quarter_10_unpacked,fcf_growth_annual_3_unpacked,fcf_growth_annual_5_unpacked,fcf_growth_annual_10_unpacked

                              # Assuming `annual_data` and `ticker` are defined elsewhere
                         FCF_annual1_unpacked, rounded_fcf_Annual_ten,FCF_annual_five_unpacked,FCF_annual_ten_unpacked,FCF_quarter_10_unpacked,fcf_growth_annual_3_unpacked,fcf_growth_annual_5_unpacked,fcf_growth_annual_10_unpacked = calculate_fcf_averages(annual_data,quarterly_data, ticker)
          ###################################################################################################
                         rounded_fcf_Annual_five = (sum(FCF_annual_five_unpacked) / len(FCF_annual_five_unpacked))
                         Average_fcf_growth_3years =  "{:.2f}%".format(((sum(fcf_growth_annual_3_unpacked) / len(fcf_growth_annual_3_unpacked)))*100)

                         average_fcf_Annual_one = ((sum(FCF_annual1_unpacked) / len(FCF_annual1_unpacked)))/1000000000
                         rounded_fcf_Annual_one = "{:.2f}B".format(average_fcf_Annual_one)
          ###################################################################################################

                         def calculate_roic_averages(annual_data, ticker):
                              if f'{ticker}_roic_last' in st.session_state:
                                   return (st.session_state[f'{ticker}_roic_last'],
                                        st.session_state[f'{ticker}_ROIC_annual_5_unpacked'],
                                        st.session_state[f'{ticker}_ROIC_annual_10_unpacked'],
                                        st.session_state[f'{ticker}_roic_three_years'],
                                        st.session_state[f'{ticker}_ROE_annual_5_unpacked'],
                                        st.session_state[f'{ticker}_ROE_annual_10_unpacked'])


                              ROIC_annual_one = "{:.2f}%".format(annual_data['roic'][-1]*100)

                              ROIC_annual_5_unpacked =annual_data['roic'][-5:]
                              
                              ROIC_annual_10_unpacked =annual_data['roic'][-10:]

                              ROIC_annual_3years = annual_data['roic'][-3:]
                              ROIC_annual_3years=sum(ROIC_annual_3years)/len(ROIC_annual_3years)
                              ROIC_annual_3years = "{:.2f}%".format(ROIC_annual_3years*100)

                              ROE_annual_5_unpacked =annual_data['roe'][-5:]
                              ROE_annual_10_unpacked =annual_data['roe'][-10:]

                              st.session_state[f'{ticker}_roic_last'] = ROIC_annual_one
                              st.session_state[f'{ticker}_ROIC_annual_5_unpacked'] = ROIC_annual_5_unpacked
                              st.session_state[f'{ticker}_ROIC_annual_10_unpacked'] = ROIC_annual_10_unpacked
                              st.session_state[f'{ticker}_roic_three_years'] = ROIC_annual_3years
                              st.session_state[f'{ticker}_ROE_annual_5_unpacked'] = ROE_annual_5_unpacked
                              st.session_state[f'{ticker}_ROE_annual_10_unpacked'] = ROE_annual_10_unpacked

                              return ROIC_annual_one,ROIC_annual_5_unpacked,ROIC_annual_10_unpacked, ROIC_annual_3years,ROE_annual_5_unpacked,ROE_annual_10_unpacked

                    
                         ROIC_annual_one, ROIC_annual_5_unpacked,ROIC_annual_10_unpacked, ROIC_annual_3years,ROE_annual_5_unpacked,ROE_annual_10_unpacked = calculate_roic_averages(annual_data, ticker)
                         
                         Average_ROIC_funf = ((sum(ROIC_annual_5_unpacked) / len(ROIC_annual_5_unpacked))*100)
          ###################################################################################################
                         def calculate_net_income_averages(annual_data, quarterly_data,ticker):
                              # Check if the results are already in session state
                              if f'{ticker}_net_income_last' in st.session_state:
                                   return (st.session_state[f'{ticker}_net_income_last'],
                                             st.session_state[f'{ticker}_net_income_annual_funf_unpacked'],
                                             st.session_state[f'{ticker}_net_income_annual_10_unpacked'],
                                             st.session_state[f'{ticker}_net_income_five_years'],
                                             st.session_state[f'{ticker}_net_income_quarter_10_unpacked'],

                                             st.session_state[f'{ticker}_price_to_fcf_annual21_unpacked'],
                                             st.session_state[f'{ticker}_date_annual_20yrs'],
                                             st.session_state[f'{ticker}_Price_TBV_quarter10_unpacked'],
                                             st.session_state[f'{ticker}_pe_annual_5_unpacked'],
                                             st.session_state[f'{ticker}_pe_annual_10_unpacked'],

                                             st.session_state[f'{ticker}_TBVPS_quater1_unpacked'],
                                             st.session_state[f'{ticker}_BVPS_quater1_unpacked'],

                                             st.session_state[f'{ticker}_AverageEndPrice_annual5_unpacked'],
                                             st.session_state[f'{ticker}_Net_Operating_CashFlow_annual_5_unpacked'],
                                             st.session_state[f'{ticker}_revenue_5years'],
                                             st.session_state[f'{ticker}_len_5_annual'],

                                             st.session_state[f'{ticker}_revenue_10years'],
                                             st.session_state[f'{ticker}_len_10_annual'],

                                             st.session_state[f'{ticker}_revenue_quarter_10'],
                                             st.session_state[f'{ticker}_len_10_quarter'],

                                             st.session_state[f'{ticker}_shares_diluted_annual_10_unpacked'],
                                             st.session_state[f'{ticker}_shares_basic_annual_10_unpacked'],
                                             st.session_state[f'{ticker}_shares_diluted_quarter_10_unpacked'],
                                             st.session_state[f'{ticker}_shares_basic_quarterly_10_unpacked'])


                              net_income_annual_one = annual_data['net_income'][-1:]
                              round_net_income_annual_one =(sum(net_income_annual_one) / len(net_income_annual_one))


                              net_income_annual_funf_unpacked = annual_data['net_income'][-5:] 

                              net_income_annual_10_unpacked =annual_data['net_income'][-10:]


                              net_income_annual_funf = annual_data['net_income'][-5:] 
                              Average_net_income_annual_funf = sum(net_income_annual_funf) / len(net_income_annual_funf)

                              net_income_quarter_10_unpacked = quarterly_data['net_income'][-10:] 

                              price_to_fcf_annual21_unpacked=annual_data['price_to_fcf'][-21:]  
                              date_annual_20yrs = annual_data['period_end_date'][-21:] 
                              Price_TBV_quarter10_unpacked = quarterly_data['price_to_tangible_book'][-10:]

                              pe_annual_5_unpacked  =annual_data['price_to_earnings'][-5:]
                              pe_annual_10_unpacked  =annual_data['price_to_earnings'][-10:]

                              TBVPS_quater1_unpacked = quarterly_data['tangible_book_per_share'][-1:]
                              BVPS_quater1_unpacked = quarterly_data['book_value_per_share'][-1:]

                              AverageEndPrice_annual5_unpacked = annual_data['period_end_price'][-5:]
                              Net_Operating_CashFlow_annual_5_unpacked = annual_data['cf_cfo'][-5:]

                              Revenue_annual_5_unpacked = annual_data['revenue'][-5:]

                              len_5_annual = len(Revenue_annual_5_unpacked) 
                              

                              Revenue_annual_10_unpacked  = annual_data['revenue'][-10:] 

                              len_10_annual = len(Revenue_annual_10_unpacked)

                              Revenue_quarter_10_unpacked  = quarterly_data['revenue'][-10:]
                              len_10_quarter =len(Revenue_quarter_10_unpacked)

                              shares_diluted_annual_10_unpacked=annual_data['shares_diluted'][-len_10_annual:]
                              shares_basic_annual_10_unpacked=annual_data['shares_basic'][-10:]
                              shares_diluted_quarter_10_unpacked =quarterly_data['shares_diluted'][-len_10_quarter:]
                              shares_basic_quarterly_10_unpacked =quarterly_data['shares_basic'][-10:]

                              st.session_state[f'{ticker}_net_income_last'] = round_net_income_annual_one
                              st.session_state[f'{ticker}_net_income_annual_funf_unpacked'] = net_income_annual_funf_unpacked
                              st.session_state[f'{ticker}_net_income_annual_10_unpacked'] = net_income_annual_10_unpacked
                              st.session_state[f'{ticker}_net_income_five_years'] = Average_net_income_annual_funf
                              st.session_state[f'{ticker}_net_income_quarter_10_unpacked'] =net_income_quarter_10_unpacked
                              st.session_state[f'{ticker}_price_to_fcf_annual21_unpacked'] = price_to_fcf_annual21_unpacked
                              st.session_state[f'{ticker}_date_annual_20yrs'] = date_annual_20yrs
                              st.session_state[f'{ticker}_Price_TBV_quarter10_unpacked'] = Price_TBV_quarter10_unpacked
                              st.session_state[f'{ticker}_pe_annual_5_unpacked']= pe_annual_5_unpacked
                              st.session_state[f'{ticker}_pe_annual_10_unpacked']= pe_annual_10_unpacked

                              st.session_state[f'{ticker}_TBVPS_quater1_unpacked']= TBVPS_quater1_unpacked
                              st.session_state[f'{ticker}_BVPS_quater1_unpacked']= BVPS_quater1_unpacked

                              st.session_state[f'{ticker}_AverageEndPrice_annual5_unpacked']= AverageEndPrice_annual5_unpacked
                              st.session_state[f'{ticker}_Net_Operating_CashFlow_annual_5_unpacked']= Net_Operating_CashFlow_annual_5_unpacked
                              st.session_state[f'{ticker}_revenue_5years'] = Revenue_annual_5_unpacked
                              st.session_state[f'{ticker}_len_5_annual'] =len_5_annual

                              st.session_state[f'{ticker}_revenue_10years'] = Revenue_annual_10_unpacked
                              st.session_state[f'{ticker}_len_10_annual'] =len_10_annual

                              st.session_state[f'{ticker}_revenue_quarter_10'] = Revenue_quarter_10_unpacked

                              st.session_state[f'{ticker}_len_10_quarter'] =len_10_quarter


                              st.session_state[f'{ticker}_shares_diluted_annual_10_unpacked']=shares_diluted_annual_10_unpacked
                              st.session_state[f'{ticker}_shares_basic_annual_10_unpacked']=shares_basic_annual_10_unpacked
                              st.session_state[f'{ticker}_shares_diluted_quarter_10_unpacked'] =shares_diluted_quarter_10_unpacked
                              st.session_state[f'{ticker}_shares_basic_quarterly_10_unpacked']=shares_basic_quarterly_10_unpacked

               

                              return (round_net_income_annual_one,net_income_annual_funf_unpacked, net_income_annual_10_unpacked,
                                   Average_net_income_annual_funf,net_income_quarter_10_unpacked,
                                   price_to_fcf_annual21_unpacked,date_annual_20yrs,Price_TBV_quarter10_unpacked,pe_annual_5_unpacked,
                                        pe_annual_10_unpacked, 
                                        TBVPS_quater1_unpacked,
                                        BVPS_quater1_unpacked,
                                        AverageEndPrice_annual5_unpacked,
                                        Net_Operating_CashFlow_annual_5_unpacked,
                                        Revenue_annual_5_unpacked,len_5_annual,
                                        Revenue_annual_10_unpacked,len_10_annual,
                                        Revenue_quarter_10_unpacked,len_10_quarter,                                             
                                        shares_diluted_annual_10_unpacked,
                                        shares_basic_annual_10_unpacked,
                                        shares_diluted_quarter_10_unpacked,
                                        shares_basic_quarterly_10_unpacked
                                        )

                         (round_net_income_annual_one, net_income_annual_funf_unpacked,net_income_annual_10_unpacked,
                         Average_net_income_annual_funf,net_income_quarter_10_unpacked,price_to_fcf_annual21_unpacked,date_annual_20yrs,
                         Price_TBV_quarter10_unpacked,pe_annual_5_unpacked,
                              pe_annual_10_unpacked, 
                              TBVPS_quater1_unpacked,
                              BVPS_quater1_unpacked,
                              AverageEndPrice_annual5_unpacked,
                              Net_Operating_CashFlow_annual_5_unpacked,
                              Revenue_annual_5_unpacked,len_5_annual,
                              Revenue_annual_10_unpacked,len_10_annual,
                              Revenue_quarter_10_unpacked,len_10_quarter,
                              shares_diluted_annual_10_unpacked,
                              shares_basic_annual_10_unpacked,
                              shares_diluted_quarter_10_unpacked,
                              shares_basic_quarterly_10_unpacked
                              ) = calculate_net_income_averages(annual_data,quarterly_data, ticker)

          ###################################################################################################
                    

                         Average_net_income_annual_funf_Billion_Million = (
                         "{:.2f}B".format(Average_net_income_annual_funf / 1e9) 
                         if Average_net_income_annual_funf >= 1e9
                         else "{:,.1f}M".format(Average_net_income_annual_funf / 1e6)

                         )               

                         Average_net_income_annual_one_Bill_Milli ="{:.2f}B".format(round_net_income_annual_one/ 1000000000) if(round_net_income_annual_one) >= 1000000000 else "{:,.1f}M".format(round_net_income_annual_one / 1000000)

          ###################################################################################################

                         def calculate_revenue_and_growth(annual_data,quarterly_data, ticker):
                         # Check if the results are already in session state
                              if f'{ticker}_revenue_last' in st.session_state:
                                   return (st.session_state[f'{ticker}_revenue_last'],
                                             st.session_state[f'{ticker}_revenue_10years_growth'],
                                             st.session_state[f'{ticker}_Revenue_growth_10quarter_unpacked'],

                                             st.session_state[f'{ticker}_revenue_growth_1year'],
                                             st.session_state[f'{ticker}_revenue_growth_3years'],
                                             st.session_state[f'{ticker}_revenue_growth_5years'],
                                             st.session_state[f'{ticker}_revenue_growth_10years'],
                                             st.session_state[f'{ticker}_Net_interest_Income_annual_10'],
                                             st.session_state[f'{ticker}_Net_interest_Income_annual_10_growth'],
                                             st.session_state[f'{ticker}_Net_interest_Income_quarter_10_growth'])
                                   
                              revenue_annual_ttm = annual_data['revenue'][-1:] 
                              average_revenue_annual_ttm = ((sum(revenue_annual_ttm) / len(revenue_annual_ttm)) / 1000000000)

                              Revenue_growth_10_unpacked = annual_data['revenue_growth'][-10:]
                              Revenue_growth_10quarter_unpacked= quarterly_data['revenue_growth'][-10:]

                              Revenue_growth_1year = annual_data['revenue_growth'][-1:]

                              Revenue_growth_1year=sum(Revenue_growth_1year)/len(Revenue_growth_1year)
                              Revenue_growth_1year = (Revenue_growth_1year*100)

                              Revenue_growth_3years = annual_data['revenue_growth'][-3:]
                              Revenue_growth_3years=sum(Revenue_growth_3years)/len(Revenue_growth_3years)
                              Revenue_growth_3years = (Revenue_growth_3years*100)

                              Revenue_growth_5years = annual_data['revenue_growth'][-5:]
                              Revenue_growth_5years=sum(Revenue_growth_5years)/len(Revenue_growth_5years)
                              Revenue_growth_5years = (Revenue_growth_5years*100)


                              #print("Revenue_growth_10quarter_unpacked",Revenue_growth_10quarter_unpacked)

                              Revenue_growth_10years = annual_data['revenue_growth'][-10:]
                              Revenue_growth_10years=sum(Revenue_growth_10years)/len(Revenue_growth_10years)

                              Revenue_growth_10years = (Revenue_growth_10years*100)




                              try:
                                   Net_interest_Income_annual_10_unpacked = annual_data['net_interest_income'][-10:]
                                   Net_interest_Income_annual_10_growth_unpacked = annual_data['net_interest_income_growth'][-10:]
                                   Net_interest_Income_quarter_10_growth_unpacked = quarterly_data['net_interest_income_growth'][-10:]       
                              except Exception as e:
                                   Net_interest_Income_annual_10_unpacked =[0]*len_10_annual
                                   Net_interest_Income_annual_10_growth_unpacked =[0]*len_10_annual
                                   Net_interest_Income_quarter_10_growth_unpacked =[0]*len_10_quarter          




                              # Store results in session state
                              st.session_state[f'{ticker}_revenue_last'] = average_revenue_annual_ttm
                              st.session_state[f'{ticker}_revenue_10years_growth'] = Revenue_growth_10_unpacked
                              st.session_state[f'{ticker}_Revenue_growth_10quarter_unpacked'] = Revenue_growth_10quarter_unpacked

                              st.session_state[f'{ticker}_revenue_growth_1year'] = Revenue_growth_1year
                              st.session_state[f'{ticker}_revenue_growth_3years'] = Revenue_growth_3years
                              st.session_state[f'{ticker}_revenue_growth_5years'] = Revenue_growth_5years
                              st.session_state[f'{ticker}_revenue_growth_10years'] = Revenue_growth_10years
               
                              st.session_state[f'{ticker}_Net_interest_Income_annual_10'] =Net_interest_Income_annual_10_unpacked

                              st.session_state[f'{ticker}_Net_interest_Income_annual_10_growth'] =Net_interest_Income_annual_10_growth_unpacked
                              st.session_state[f'{ticker}_Net_interest_Income_quarter_10_growth'] =Net_interest_Income_quarter_10_growth_unpacked




                              return (average_revenue_annual_ttm,
                                        Revenue_growth_10_unpacked,
                                        Revenue_growth_10quarter_unpacked,
                                        Revenue_growth_1year,
                                        Revenue_growth_3years,
                                        Revenue_growth_5years,
                                        
                                        Revenue_growth_10years, 
                                        Net_interest_Income_annual_10_unpacked,Net_interest_Income_annual_10_growth_unpacked,
                                        Net_interest_Income_quarter_10_growth_unpacked
                                        )

                         # Assuming `annual_data` and `ticker` are defined elsewhere
                         (average_revenue_annual_ttm,
                    
                         Revenue_growth_10_unpacked,
                         Revenue_growth_10quarter_unpacked,
                         Revenue_growth_1year,
                         Revenue_growth_3years,
                         Revenue_growth_5years,Revenue_growth_10years,
                         Net_interest_Income_annual_10_unpacked,
                         Net_interest_Income_annual_10_growth_unpacked,
                         Net_interest_Income_quarter_10_growth_unpacked
                         ) = calculate_revenue_and_growth(annual_data,quarterly_data, ticker)

          ###################################################################################################
                         def calculate_dividend_cagr(annual_data, quarterly_data, ticker):
                              if f'{ticker}_dividend_cagr_10' in st.session_state:
                                   return (st.session_state[f'{ticker}_dividend_cagr_10'],
                                        st.session_state[f'{ticker}_dividend_cagr_10_quarter'],
                                        st.session_state[f'{ticker}_Divdend_per_share_ttm'],
                                        st.session_state[f'{ticker}_Dividend_per_share_annual10_unpacked'],
                                        st.session_state[f'{ticker}_Dividend_per_share_quarter14_unpacked'],
                                        st.session_state[f'{ticker}_Divdends_paid_annual_5_unpacked'])

                              Dividend_per_share_cagr_10 = annual_data['dividends_per_share_cagr_10'][-1:]  
                              Dividend_per_share_cagr_10 = sum(Dividend_per_share_cagr_10)/len(Dividend_per_share_cagr_10)
                              Dividend_per_share_cagr_10= round((Dividend_per_share_cagr_10*100),2)

                              Dividend_per_share_cagr_10_quarter = quarterly_data['dividends_per_share_cagr_10'][-1:]  
                              Dividend_per_share_cagr_10_quarter = sum(Dividend_per_share_cagr_10_quarter)/len(Dividend_per_share_cagr_10_quarter)
                              Dividend_per_share_cagr_10_quarter= round((Dividend_per_share_cagr_10_quarter*100),2)

                              Divdend_per_share_ttm =Financial_data['ttm']['dividends']

                              Dividend_per_share_annual10_unpacked = annual_data['dividends'][-10:]

                              Dividend_per_share_quarter14_unpacked = quarterly_data['dividends'][-14:] 

                              Divdends_paid_annual_5_unpacked =annual_data['dividends'][-5:]

                              

                              # Store results in session state
                              st.session_state[f'{ticker}_dividend_cagr_10'] = Dividend_per_share_cagr_10
                              st.session_state[f'{ticker}_dividend_cagr_10_quarter'] = Dividend_per_share_cagr_10_quarter
                              st.session_state[f'{ticker}_Divdend_per_share_ttm'] = Divdend_per_share_ttm
                              st.session_state[f'{ticker}_Dividend_per_share_annual10_unpacked'] = Dividend_per_share_annual10_unpacked
                              st.session_state[f'{ticker}_Dividend_per_share_quarter14_unpacked'] = Dividend_per_share_quarter14_unpacked
                              st.session_state[f'{ticker}_Divdends_paid_annual_5_unpacked'] = Divdends_paid_annual_5_unpacked

                              return (Dividend_per_share_cagr_10, Dividend_per_share_cagr_10_quarter,
                              Divdend_per_share_ttm,Dividend_per_share_annual10_unpacked,Dividend_per_share_quarter14_unpacked,Divdends_paid_annual_5_unpacked)

                         (Dividend_per_share_cagr_10, Dividend_per_share_cagr_10_quarter,Divdend_per_share_ttm,
                         Dividend_per_share_annual10_unpacked,Dividend_per_share_quarter14_unpacked,Divdends_paid_annual_5_unpacked) = calculate_dividend_cagr(annual_data, quarterly_data, ticker)

          ###################################################################################################
                         def calculate_cagr_10_years(annual_data, ticker):
                         # Check if the results are already in session state
                              if f'{ticker}_fcf_cagr_10' in st.session_state:
                                   return (st.session_state[f'{ticker}_fcf_cagr_10'],
                                             st.session_state[f'{ticker}_eps_cagr_10'],
                                             st.session_state[f'{ticker}_revenue_cagr_10'],
                                             st.session_state[f'{ticker}_net_interest_income_cagr_10'])


                         
                              
                              
                              FCF_Cagr_10 = annual_data['fcf_cagr_10'][-1:]
                              FCF_Cagr_10 = sum(FCF_Cagr_10)/len(FCF_Cagr_10)
                              FCF_Cagr_10 =round((FCF_Cagr_10*100),2)

                              EPS_Cagr_10 = annual_data['eps_diluted_cagr_10'][-1:]
                              EPS_Cagr_10 = sum(EPS_Cagr_10)/len(EPS_Cagr_10)
                              EPS_Cagr_10 =round((EPS_Cagr_10*100),2)

                              Revenue_Cagr_10 = annual_data['revenue_cagr_10'][-1:]
                              Revenue_Cagr_10 = sum(Revenue_Cagr_10)/len(Revenue_Cagr_10)
                              Revenue_Cagr_10= round((Revenue_Cagr_10*100),2)
                              try:
                              
                                   Net_interest_Income_annual_Cagr_10 = annual_data['net_interest_income_cagr_10'][-1:]
                                   Net_interest_Income_annual_Cagr_10 = sum(Net_interest_Income_annual_Cagr_10)/len(Net_interest_Income_annual_Cagr_10)
                                   Net_interest_Income_annual_Cagr_10= round((Net_interest_Income_annual_Cagr_10*100),2)

                              except Exception as e:

                                   Net_interest_Income_annual_Cagr_10 = "{:.2f}".format(0.00)

                              st.session_state[f'{ticker}_fcf_cagr_10'] = FCF_Cagr_10
                              st.session_state[f'{ticker}_eps_cagr_10'] = EPS_Cagr_10
                              st.session_state[f'{ticker}_revenue_cagr_10'] = Revenue_Cagr_10
                              st.session_state[f'{ticker}_net_interest_income_cagr_10'] = Net_interest_Income_annual_Cagr_10

                              return FCF_Cagr_10, EPS_Cagr_10, Revenue_Cagr_10,Net_interest_Income_annual_Cagr_10

                         FCF_Cagr_10, EPS_Cagr_10, Revenue_Cagr_10,Net_interest_Income_annual_Cagr_10 = calculate_cagr_10_years(annual_data, ticker)

          ###################################################################################################

                    #....................................................

                         Free_cash_flow_annual_one = annual_data['fcf'][-1:] 
                         Average_Free_cash_flow_annual_one = ((sum(Free_cash_flow_annual_one) / len(Free_cash_flow_annual_one)))/1000000000
                         Average_Free_cash_flow_annual_one_one =Average_Free_cash_flow_annual_one
          ###################################################################################################
                         def calculate_financial_ratios(annual_data, quarterly_data, ticker):
                         # Check if the results are already in session state
                              if f'{ticker}_roa_ttm' in st.session_state:
                                   return (st.session_state[f'{ticker}_roa_ttm'],
                                             st.session_state[f'{ticker}_one_yr_roce'],
                                             st.session_state[f'{ticker}_five_yrs_roce'],
                                             st.session_state[f'{ticker}_total_equity'],
                                             st.session_state[f'{ticker}_net_income_margin_10_unpacked'],
                                             st.session_state[f'{ticker}_net_income_margin_annual5_unpacked'],
                                             st.session_state[f'{ticker}_net_income_margin_1'],
                                             st.session_state[f'{ticker}_FCF_Margin_annual_10unpacked'],
                                             st.session_state[f'{ticker}_fcf_margin_5'],
                                             st.session_state[f'{ticker}_fcf_margin_1'],
                                             st.session_state[f'{ticker}_debt_equity_annual_10'] ,
                                             st.session_state[f'{ticker}_Price_to_tangible_book_annual_10'] ,
                                             st.session_state[f'{ticker}_EBITDA_growth_annual_10'] ,
                                             st.session_state[f'{ticker}_Price_to_book_annual_5'] ,
                                             st.session_state[f'{ticker}_Price_to_book_annual_10'] ,
                                             st.session_state[f'{ticker}_fcf_per_share_annual_10'] ,
                                             st.session_state[f'{ticker}_revenue_per_share_annual_10'] ,
                                             st.session_state[f'{ticker}_Payout_ratio_annual_10'],
                                             st.session_state[f'{ticker}_NetIncome_growth_annual_10'] ,
                                             st.session_state[f'{ticker}_Book_Value_growth_annual_10'] ,
                                             st.session_state[f'{ticker}_Price_to_sales_annual_10'] ,
                                             st.session_state[f'{ticker}_Price_to_earnings_annual_10'] ,
                                             st.session_state[f'{ticker}_shares_diluted_growth_annual_10'] ,
                                             st.session_state[f'{ticker}_FCF_Margin_quarter_10'],
                                             st.session_state[f'{ticker}_ebitda_Margin_quarter_10'],
                                             st.session_state[f'{ticker}_ebitda_Margin_annual_10'],
                                             st.session_state[f'{ticker}_ebitda_Margin_annual_5'],
                                             st.session_state[f'{ticker}_debt_equity_quarter_10'] ,
                                             st.session_state[f'{ticker}_EBITDA_growth_quarter_10'] ,
                                             st.session_state[f'{ticker}_Price_to_book_quarter_10'] ,
                                             st.session_state[f'{ticker}_Dividend_per_share_quarter_10'],
                                             st.session_state[f'{ticker}_fcf_per_share_quarter_10'] ,
                                             st.session_state[f'{ticker}_revenue_per_share_quarter_10'] ,
                                             st.session_state[f'{ticker}_ROE_quarter_10'],
                                             st.session_state[f'{ticker}_Payout_ratio_quarter_10'] ,
                                             st.session_state[f'{ticker}_NetIncome_growth_quarter_10'] ,
                                             st.session_state[f'{ticker}_FCF_growth_quarter_10'],
                                             st.session_state[f'{ticker}_Book_Value_growth_quarter_10'] ,
                                             st.session_state[f'{ticker}_Price_to_sales_quarter_10'] ,
                                             st.session_state[f'{ticker}_Price_to_earnings_quarter_10'] ,
                                             st.session_state[f'{ticker}_EPS_growth_quarter_10'],
                                             st.session_state[f'{ticker}_ROIC_quarter_10'],
                                             st.session_state[f'{ticker}_shares_diluted_growth_quarter_10'] ,
                                             st.session_state[f'{ticker}_Dividend_per_share_growth_quarter_10'],
                                             st.session_state[f'{ticker}_gross_margin_quarter1_unpacked'],
                                             st.session_state[f'{ticker}_gross_margin_quarter10_unpacked']
                                        )

                              ROA_annual_ttm = annual_data['roa'][-1:] 
                              average_ROA_annual_ttm = "{:.2f}%".format((sum(ROA_annual_ttm) / len(ROA_annual_ttm))*100)


                              One_YR_ROCE = annual_data['roce'][-1:]  
                              One_YR_ROCE=sum(One_YR_ROCE)/len(One_YR_ROCE)
                              One_YR_ROCE = (One_YR_ROCE*100)


                              five_yrs_ROCE = annual_data['roce'][-5:]
                              five_yrs_ROCE=sum(five_yrs_ROCE)/len(five_yrs_ROCE)
                              five_yrs_ROCE = (five_yrs_ROCE*100)

                              Total_Equity_annual_one = annual_data['total_equity'][-1:]
                              Average_total_equity_annual = (sum(Total_Equity_annual_one) / len(Total_Equity_annual_one)) / 1000000000
                         
                              Net_income_margin_10_unpacked = annual_data['net_income_margin'][-10:]

                              Net_income_margin_annual5_unpacked = annual_data['net_income_margin'][-5:]
                              

                              Net_income_margin_1 = annual_data['net_income_margin'][-1:]
                              

                              FCF_Margin_annual_10unpacked = annual_data['fcf_margin'][-10:]

                              #FCF_Margin_annual10_unpacked = annual_data['fcf_margin'][-10:] #10years
                              #FCF_Margin_10 =float(sum(FCF_Margin)/len(FCF_Margin))

                              FCF_Margin_5 = annual_data['fcf_margin'][-5:] 
                              FCF_Margin_5=sum(FCF_Margin_5)/len(FCF_Margin_5)

                              FCF_Margin_1 = annual_data['fcf_margin'][-1:]
                              FCF_Margin_1=sum(FCF_Margin_1)/len(FCF_Margin_1)
                              FCF_Margin_1 = (FCF_Margin_1*100)



                              debt_equity_annual_10_unpacked = annual_data['debt_to_equity'][-10:]
                              Price_to_tangible_book_annual_10_unpacked = annual_data['price_to_tangible_book'][-10:]
                              EBITDA_growth_annual_10_unpacked = annual_data['ebitda_growth'][-10:]
                              Price_to_book_5_annual_unpacked = annual_data['price_to_book'][-5:]
                              Price_to_book_10_annual_unpacked = annual_data['price_to_book'][-10:]
                              fcf_per_share_annual_10_unpacked = annual_data['fcf_per_share'][-10:]
                              revenue_per_share_annual_10_unpacked = annual_data['revenue_per_share'][-10:]
                              Payout_ratio_annual_10_unpacked = annual_data['payout_ratio'][-10:]
                              NetIncome_growth_annual_10_unpacked = annual_data['net_income_growth'][-10:]
                              Book_Value_growth_annual_10_unpacked = annual_data['book_value'][-10:]
                              Price_to_sales_annual_10_unpacked = annual_data['price_to_sales'][-10:]
                              Price_to_earnings_annual_10_unpacked = annual_data['price_to_earnings'][-10:]
                              shares_diluted_annual_growth_10_unpacked = annual_data['shares_diluted_growth'][-10:]

                              # Calculate the financial ratios (quarterly data)
                              FCF_Margin_quarter_10_unpacked = quarterly_data['fcf_margin'][-10:]
                              ebitda_Margin_quarter_10_unpacked = quarterly_data['ebitda_margin'][-10:]
                              ebitda_Margin_annual_10_unpacked = annual_data['ebitda_margin'][-10:]
                              ebitda_Margin_annual_5_unpacked = annual_data['ebitda_margin'][-5:]
                              debt_equity_quarter_10_unpacked = quarterly_data['debt_to_equity'][-10:]
                              EBITDA_growth_quarter_10_unpacked = quarterly_data['ebitda_growth'][-10:]
                              Price_to_book_quarter_10_unpacked = quarterly_data['price_to_book'][-10:]
                              Dividend_per_share_quarter_10_unpacked = quarterly_data['dividends'][-10:]
                              fcf_per_share_quarter_10_unpacked = quarterly_data['fcf_per_share'][-10:]
                              revenue_per_share_quarter_10_unpacked = quarterly_data['revenue_per_share'][-10:]
                              ROE_quarter_10_unpacked = quarterly_data['roe'][-10:]
                              Payout_ratio_quarter_10_unpacked = quarterly_data['payout_ratio'][-10:]
                              NetIncome_growth_quarter_10_unpacked = quarterly_data['net_income_growth'][-10:]
                              FCF_growth_quarter_10_unpacked = quarterly_data['fcf_growth'][-10:]
                              Book_Value_growth_quarter_10_unpacked = quarterly_data['book_value'][-10:]
                              Price_to_sales_quarter_10_unpacked = quarterly_data['price_to_sales'][-10:]
                              Price_to_earnings_quarter_10_unpacked = quarterly_data['price_to_earnings'][-10:]
                              EPS_growth_quarter_10_unpacked = quarterly_data['eps_diluted_growth'][-10:]
                              ROIC_quarter_10_unpacked = quarterly_data['roic'][-10:]
                              shares_diluted_quarter_growth_10_unpacked = quarterly_data['shares_diluted_growth'][-10:]
                              Dividend_per_share_growth_quarter_10_unpacked = quarterly_data['dividends_per_share_growth'][-10:]

                              try:
                                   gross_margin_quarter1_unpacked = quarterly_data['gross_margin'][-1:]
                                   gross_margin_quarter10_unpacked = quarterly_data['gross_margin'][-10:]
                                   

                              except Exception as e:

                                   gross_margin_quarter1_unpacked = [0]*1
                                   gross_margin_quarter10_unpacked = [0]*len_10_quarter

                              # Store results in session state
                              st.session_state[f'{ticker}_roa_ttm'] = average_ROA_annual_ttm
                              st.session_state[f'{ticker}_one_yr_roce'] = One_YR_ROCE
                              st.session_state[f'{ticker}_five_yrs_roce'] = five_yrs_ROCE
                              st.session_state[f'{ticker}_total_equity'] = Average_total_equity_annual
                              st.session_state[f'{ticker}_net_income_margin_10_unpacked'] = Net_income_margin_10_unpacked
                              st.session_state[f'{ticker}_net_income_margin_annual5_unpacked'] = Net_income_margin_annual5_unpacked
                              st.session_state[f'{ticker}_net_income_margin_1'] = Net_income_margin_1
                              st.session_state[f'{ticker}_FCF_Margin_annual_10unpacked'] = FCF_Margin_annual_10unpacked
                              st.session_state[f'{ticker}_fcf_margin_5'] = FCF_Margin_5
                              st.session_state[f'{ticker}_fcf_margin_1'] = FCF_Margin_1
                              st.session_state[f'{ticker}_debt_equity_annual_10'] = debt_equity_annual_10_unpacked
                              st.session_state[f'{ticker}_Price_to_tangible_book_annual_10'] = Price_to_tangible_book_annual_10_unpacked
                              st.session_state[f'{ticker}_EBITDA_growth_annual_10'] = EBITDA_growth_annual_10_unpacked
                              st.session_state[f'{ticker}_Price_to_book_annual_5'] = Price_to_book_5_annual_unpacked
                              st.session_state[f'{ticker}_Price_to_book_annual_10'] = Price_to_book_10_annual_unpacked
                              st.session_state[f'{ticker}_fcf_per_share_annual_10'] = fcf_per_share_annual_10_unpacked
                              st.session_state[f'{ticker}_revenue_per_share_annual_10'] = revenue_per_share_annual_10_unpacked
                              st.session_state[f'{ticker}_Payout_ratio_annual_10'] = Payout_ratio_annual_10_unpacked
                              st.session_state[f'{ticker}_NetIncome_growth_annual_10'] = NetIncome_growth_annual_10_unpacked
                              st.session_state[f'{ticker}_Book_Value_growth_annual_10'] = Book_Value_growth_annual_10_unpacked
                              st.session_state[f'{ticker}_Price_to_sales_annual_10'] = Price_to_sales_annual_10_unpacked
                              st.session_state[f'{ticker}_Price_to_earnings_annual_10'] = Price_to_earnings_annual_10_unpacked
                              st.session_state[f'{ticker}_shares_diluted_growth_annual_10'] = shares_diluted_annual_growth_10_unpacked

                              st.session_state[f'{ticker}_FCF_Margin_quarter_10'] = FCF_Margin_quarter_10_unpacked
                              st.session_state[f'{ticker}_ebitda_Margin_quarter_10']= ebitda_Margin_quarter_10_unpacked
                              st.session_state[f'{ticker}_ebitda_Margin_annual_10']= ebitda_Margin_annual_10_unpacked
                              st.session_state[f'{ticker}_ebitda_Margin_annual_5']= ebitda_Margin_annual_5_unpacked
                              st.session_state[f'{ticker}_debt_equity_quarter_10'] = debt_equity_quarter_10_unpacked
                              st.session_state[f'{ticker}_EBITDA_growth_quarter_10'] = EBITDA_growth_quarter_10_unpacked
                              st.session_state[f'{ticker}_Price_to_book_quarter_10'] = Price_to_book_quarter_10_unpacked
                              st.session_state[f'{ticker}_Dividend_per_share_quarter_10'] = Dividend_per_share_quarter_10_unpacked
                              st.session_state[f'{ticker}_fcf_per_share_quarter_10'] = fcf_per_share_quarter_10_unpacked
                              st.session_state[f'{ticker}_revenue_per_share_quarter_10'] = revenue_per_share_quarter_10_unpacked
                              st.session_state[f'{ticker}_ROE_quarter_10'] = ROE_quarter_10_unpacked
                              st.session_state[f'{ticker}_Payout_ratio_quarter_10'] = Payout_ratio_quarter_10_unpacked
                              st.session_state[f'{ticker}_NetIncome_growth_quarter_10'] = NetIncome_growth_quarter_10_unpacked
                              st.session_state[f'{ticker}_FCF_growth_quarter_10'] = FCF_growth_quarter_10_unpacked
                              st.session_state[f'{ticker}_Book_Value_growth_quarter_10'] = Book_Value_growth_quarter_10_unpacked
                              st.session_state[f'{ticker}_Price_to_sales_quarter_10'] = Price_to_sales_quarter_10_unpacked
                              st.session_state[f'{ticker}_Price_to_earnings_quarter_10'] = Price_to_earnings_quarter_10_unpacked
                              st.session_state[f'{ticker}_EPS_growth_quarter_10'] = EPS_growth_quarter_10_unpacked
                              st.session_state[f'{ticker}_ROIC_quarter_10'] = ROIC_quarter_10_unpacked
                              st.session_state[f'{ticker}_shares_diluted_growth_quarter_10'] = shares_diluted_quarter_growth_10_unpacked
                              st.session_state[f'{ticker}_Dividend_per_share_growth_quarter_10'] = Dividend_per_share_growth_quarter_10_unpacked
                              st.session_state[f'{ticker}_gross_margin_quarter1_unpacked'] = gross_margin_quarter1_unpacked
                              st.session_state[f'{ticker}_gross_margin_quarter10_unpacked'] = gross_margin_quarter10_unpacked

                              return (
                                   average_ROA_annual_ttm, One_YR_ROCE, five_yrs_ROCE, Average_total_equity_annual,
                                   Net_income_margin_10_unpacked, Net_income_margin_annual5_unpacked, Net_income_margin_1,
                                   FCF_Margin_annual_10unpacked, FCF_Margin_5, FCF_Margin_1,
                                   debt_equity_annual_10_unpacked, Price_to_tangible_book_annual_10_unpacked,
                                   EBITDA_growth_annual_10_unpacked, Price_to_book_5_annual_unpacked,Price_to_book_10_annual_unpacked, 
                                   fcf_per_share_annual_10_unpacked, revenue_per_share_annual_10_unpacked,
                                   Payout_ratio_annual_10_unpacked, NetIncome_growth_annual_10_unpacked,
                                   Book_Value_growth_annual_10_unpacked, Price_to_sales_annual_10_unpacked,
                                   Price_to_earnings_annual_10_unpacked, shares_diluted_annual_growth_10_unpacked,
                                   FCF_Margin_quarter_10_unpacked, ebitda_Margin_quarter_10_unpacked,
                                   ebitda_Margin_annual_10_unpacked,ebitda_Margin_annual_5_unpacked,
                                   debt_equity_quarter_10_unpacked,EBITDA_growth_quarter_10_unpacked,
                                   Price_to_book_quarter_10_unpacked, Dividend_per_share_quarter_10_unpacked,
                                   fcf_per_share_quarter_10_unpacked, revenue_per_share_quarter_10_unpacked,
                                   ROE_quarter_10_unpacked, Payout_ratio_quarter_10_unpacked, NetIncome_growth_quarter_10_unpacked,
                                   FCF_growth_quarter_10_unpacked, Book_Value_growth_quarter_10_unpacked,
                                   Price_to_sales_quarter_10_unpacked, Price_to_earnings_quarter_10_unpacked,
                                   EPS_growth_quarter_10_unpacked, ROIC_quarter_10_unpacked,
                                   shares_diluted_quarter_growth_10_unpacked, Dividend_per_share_growth_quarter_10_unpacked,
                                   gross_margin_quarter1_unpacked,gross_margin_quarter10_unpacked
                              )

                         # Example call to the function
                         (average_ROA_annual_ttm, One_YR_ROCE, five_yrs_ROCE, Average_total_equity_annual,
                         Net_income_margin_10_unpacked, Net_income_margin_annual5_unpacked, Net_income_margin_1,
                         FCF_Margin_annual_10unpacked, FCF_Margin_5, FCF_Margin_1,
                         debt_equity_annual_10_unpacked, Price_to_tangible_book_annual_10_unpacked,
                         EBITDA_growth_annual_10_unpacked,Price_to_book_5_annual_unpacked,Price_to_book_10_annual_unpacked, 
                         fcf_per_share_annual_10_unpacked, revenue_per_share_annual_10_unpacked,
                         Payout_ratio_annual_10_unpacked, NetIncome_growth_annual_10_unpacked,
                         Book_Value_growth_annual_10_unpacked, Price_to_sales_annual_10_unpacked,
                         Price_to_earnings_annual_10_unpacked, shares_diluted_annual_growth_10_unpacked,
                         FCF_Margin_quarter_10_unpacked,ebitda_Margin_quarter_10_unpacked,
                         ebitda_Margin_annual_10_unpacked,ebitda_Margin_annual_5_unpacked,
                         debt_equity_quarter_10_unpacked, EBITDA_growth_quarter_10_unpacked,
                         Price_to_book_quarter_10_unpacked, Dividend_per_share_quarter_10_unpacked,
                         fcf_per_share_quarter_10_unpacked, revenue_per_share_quarter_10_unpacked,
                         ROE_quarter_10_unpacked, Payout_ratio_quarter_10_unpacked, NetIncome_growth_quarter_10_unpacked,
                         FCF_growth_quarter_10_unpacked, Book_Value_growth_quarter_10_unpacked,
                         Price_to_sales_quarter_10_unpacked, Price_to_earnings_quarter_10_unpacked,
                         EPS_growth_quarter_10_unpacked, ROIC_quarter_10_unpacked,
                         shares_diluted_quarter_growth_10_unpacked, Dividend_per_share_growth_quarter_10_unpacked,
                         gross_margin_quarter1_unpacked,gross_margin_quarter10_unpacked) = calculate_financial_ratios(annual_data, quarterly_data, ticker)
          ###################################################################################################
                         FCF_Margin_10 =(sum(FCF_Margin_annual_10unpacked)/len(FCF_Margin_annual_10unpacked))*100
                         Net_income_margin_1 = sum(Net_income_margin_1)/len(Net_income_margin_1)

                         Net_income_margin_10years = sum(Net_income_margin_10_unpacked)/len(Net_income_margin_10_unpacked)
                         Net_income_margin_annual5 = sum(Net_income_margin_annual5_unpacked)/len(Net_income_margin_annual5_unpacked)

                         ebitda_Margin_annual_5_average = sum(ebitda_Margin_annual_5_unpacked)/len(ebitda_Margin_annual_5_unpacked)

                         BVPS_quater1=sum(BVPS_quater1_unpacked)/len(BVPS_quater1_unpacked)
                                                     
                         TBVPS_quater1 =sum(TBVPS_quater1_unpacked)/len(TBVPS_quater1_unpacked)
                                   
                                   


                         try:
                              PBVPS = amount / BVPS_quater1 if BVPS_quater1 > 0 else 0.00
                              PBVPS = PBVPS if math.isfinite(PBVPS) and PBVPS > 0 else 0.00

                              PTBVPS=amount/TBVPS_quater1 if BVPS_quater1 > 0 else 0.00
                              PTBVPS = PTBVPS if math.isfinite(PTBVPS) and PTBVPS > 0 else 0.00

                         except Exception as e:
                              PBVPS = 0.00
                              PTBVPS = 0.00

                         if len_10_annual == 10:
                              average_price_to_book = "{:.2f}".format(sum(Price_to_book_10_annual_unpacked)/len(Price_to_book_10_annual_unpacked))
                              Average_Price_to_tangible_book ="{:.2f}".format(sum(Price_to_tangible_book_annual_10_unpacked)/len(Price_to_tangible_book_annual_10_unpacked))

                         else:
                              average_price_to_book = "{:.2f}".format(0.00)
                              Average_Price_to_tangible_book = "{:.2f}".format(0.00)

                         if len_5_annual == 5:

                              average_price_to_book_annual_5=  "{:.2f}".format(sum(Price_to_book_5_annual_unpacked)/len(Price_to_book_5_annual_unpacked))
                         else:
                              average_price_to_book_annual_5 = "{:.2f}".format(0.00)
          ###################################################################################################
                         def unpack_annual21_data(annual_data,ticker):

                              if f'{ticker}_revenue_annual21' in st.session_state:
                                   return (st.session_state[f'{ticker}_revenue_annual21'],
                                        st.session_state[f'{ticker}_eps_diluted_annual21'],
                                        st.session_state[f'{ticker}_dividendPaidInTheLast21Years'],
                                        st.session_state[f'{ticker}_Dividends_per_share_growth_annual10'],
                                        st.session_state[f'{ticker}_revenue_growth_annual21'],
                                        st.session_state[f'{ticker}_shares_diluted_annual21'],
                                        st.session_state[f'{ticker}_Free_cash_flow_annual_21_unpacked'])

                         # Unpacking the last 21 years of revenue data
                              revenue_annual21_unpacked = annual_data['revenue'][-21:]

                              eps_diluted_annual_21_unpacked = annual_data['eps_diluted'][-21:]

                              dividendPaidInTheLast21Years_unpacked = [abs(value) for value in annual_data['cff_dividend_paid'][-21:]]

                              Dividends_per_share_growth_annual10_unpacked = annual_data['dividends_per_share_growth'][-10:]

                              revenue_growth_annual21_unpacked = annual_data['revenue_growth'][-21:]

                              shares_diluted_annual21_unpacked = annual_data['shares_diluted'][-21:]

                              Free_cash_flow_annual_21_unpacked = annual_data['fcf'][-21:]

                              # Storing the unpacked data in session state
                              st.session_state[f'{ticker}_revenue_annual21'] = revenue_annual21_unpacked
                              st.session_state[f'{ticker}_eps_diluted_annual21'] = eps_diluted_annual_21_unpacked
                              st.session_state[f'{ticker}_dividendPaidInTheLast21Years'] = dividendPaidInTheLast21Years_unpacked
                              st.session_state[f'{ticker}_Dividends_per_share_growth_annual10'] = Dividends_per_share_growth_annual10_unpacked
                              st.session_state[f'{ticker}_revenue_growth_annual21'] = revenue_growth_annual21_unpacked
                              st.session_state[f'{ticker}_shares_diluted_annual21'] = shares_diluted_annual21_unpacked
                              st.session_state[f'{ticker}_Free_cash_flow_annual_21_unpacked'] = Free_cash_flow_annual_21_unpacked



                              return (revenue_annual21_unpacked, eps_diluted_annual_21_unpacked, 
                                        dividendPaidInTheLast21Years_unpacked, Dividends_per_share_growth_annual10_unpacked, 
                                        revenue_growth_annual21_unpacked, shares_diluted_annual21_unpacked,Free_cash_flow_annual_21_unpacked)

                         (revenue_annual21_unpacked, eps_diluted_annual_21_unpacked, 
                                        dividendPaidInTheLast21Years_unpacked, Dividends_per_share_growth_annual10_unpacked, 
                                        revenue_growth_annual21_unpacked, shares_diluted_annual21_unpacked,Free_cash_flow_annual_21_unpacked) = unpack_annual21_data(annual_data,ticker)


          ###################################################################################################
                         def calculate_fcf_5_cagr(FCF_annual_ten_unpacked, ticker):
                         # Check if the result is already in session state
                              if f'{ticker}_FCF_5_CAGR' in st.session_state:
                                   return st.session_state[f'{ticker}_FCF_5_CAGR']

                              try:
                                   # Get the value at index -6 (5 years ago) and the most recent value
                                   value_at_index_6 = FCF_annual_ten_unpacked[-6]
                                   

                                   value_at_index_last = FCF_annual_ten_unpacked[-1]
                              except Exception as e:
                                   # If there's an error (e.g., insufficient data), set both to 0
                                   value_at_index_6 = 0
                                   value_at_index_last = 0

                              try:
                                   if value_at_index_6 == 0:
                                        # If value at index -6 is 0, CAGR is 0
                                        FCF_5_CAGR = "{:.2f}".format(0.00)
                                   else:
                                        try:
                                             # Calculate CAGR
                                             FCF_5_CAGR = (pow((value_at_index_last / value_at_index_6), 1/5) - 1) * 100
                                             # Handle complex number case
                                             if isinstance(FCF_5_CAGR, complex):
                                                  FCF_5_CAGR = "{:.2f}".format(0.00)
                                             else:
                                                  FCF_5_CAGR = "{:.2f}".format(FCF_5_CAGR)
                                        except Exception as e:
                                             FCF_5_CAGR = "{:.2f}".format(0.00)
                              except Exception as e:
                                   FCF_5_CAGR = "{:.2f}".format(0.00)

                              # Store the result in session state
                              st.session_state[f'{ticker}_FCF_5_CAGR'] = FCF_5_CAGR

                              return FCF_5_CAGR
                         
                    

                              # Usage example:
                         
                         FCF_5_CAGR = calculate_fcf_5_cagr(FCF_annual_ten_unpacked, ticker)
          ###################################################################################################
                         

                         def calculate_eps_5_cagr(eps_basic_annual_10_unpacked, ticker):
                              # Check if the result is already in session state
                              if f'{ticker}_EPS_5_CAGR' in st.session_state:
                                   return st.session_state[f'{ticker}_EPS_5_CAGR']

                              try:
                                   # Get the value at index -6 (5 years ago) and the most recent value
                                   value_at_index_6 = eps_basic_annual_10_unpacked[-6]
                                   value_at_index_last = eps_basic_annual_10_unpacked[-1]
                              except Exception as e:
                                   # If there's an error (e.g., insufficient data), set both to 0
                                   value_at_index_6 = 0
                                   value_at_index_last = 0

                              try:
                                   if value_at_index_6 == 0:
                                        # If value at index -6 is 0, CAGR is 0
                                        EPS_5_CAGR = "{:.2f}".format(0.00)
                                   else:
                                        try:
                                             # Calculate CAGR
                                             EPS_5_CAGR = (pow((value_at_index_last / value_at_index_6), 0.2) - 1) * 100
                                             # Handle complex number case
                                             if isinstance(EPS_5_CAGR, complex):
                                                  EPS_5_CAGR = "{:.2f}".format(0.00)
                                             else:
                                                  EPS_5_CAGR = "{:.2f}".format(EPS_5_CAGR)
                                        except Exception as e:
                                             EPS_5_CAGR = "{:.2f}".format(0.00)
                              except Exception as e:
                                   EPS_5_CAGR = "{:.2f}".format(0.00)

                              # Store the result in session state
                              st.session_state[f'{ticker}_EPS_5_CAGR'] = EPS_5_CAGR

                              return EPS_5_CAGR


                         EPS_5_CAGR = calculate_eps_5_cagr(eps_basic_annual_10_unpacked, ticker)

          ###################################################################################################
                         
                         def calculate_revenue_5_cagr(Revenue_annual_10_unpacked, ticker):
                              # Check if the result is already in session state
                              if f'{ticker}_Revenue_5_CAGR' in st.session_state:
                                   return st.session_state[f'{ticker}_Revenue_5_CAGR']

                              try:
                                   # Get the value at index -6 (5 years ago) and the most recent value
                                   value_at_index_6 = Revenue_annual_10_unpacked[-6]
                                   value_at_index_last = Revenue_annual_10_unpacked[-1]
                              except Exception as e:
                                   # If there's an error (e.g., insufficient data), set both to 0
                                   value_at_index_6 = 0
                                   value_at_index_last = 0

                              try:
                                   if value_at_index_6 == 0:
                                        # If value at index -6 is 0, CAGR is 0
                                        Revenue_5_CAGR = "{:.2f}".format(0.00)
                                   else:
                                        try:
                                             # Calculate CAGR
                                             Revenue_5_CAGR = (pow((value_at_index_last / value_at_index_6), 0.2) - 1) * 100
                                             # Handle complex number case
                                             if isinstance(Revenue_5_CAGR, complex):
                                                  Revenue_5_CAGR = "{:.2f}".format(0.00)
                                             else:
                                                  Revenue_5_CAGR = "{:.2f}".format(Revenue_5_CAGR)
                                        except Exception as e:
                                             Revenue_5_CAGR = "{:.2f}".format(0.00)
                              except Exception as e:
                                   Revenue_5_CAGR = "{:.2f}".format(0.00)

                              # Store the result in session state
                              st.session_state[f'{ticker}_Revenue_5_CAGR'] = Revenue_5_CAGR

                              return Revenue_5_CAGR



                         Revenue_5_CAGR = calculate_revenue_5_cagr(Revenue_annual_10_unpacked, ticker)
          
                              
          ###################################################################################################
                         #print("Net_interest_Income_annual_10_unpacked",Net_interest_Income_annual_10_unpacked)
                         def calculate_Net_interest_Income_CAGR_5(Net_interest_Income_annual_10_unpacked, ticker):
                              # Check if the result is already in session state
                              if f'{ticker}_Net_interest_Income_annual_Cagr_5' in st.session_state:
                                   return st.session_state[f'{ticker}_Net_interest_Income_annual_Cagr_5']

                              try:
                                   # Get the value at index -6 (5 years ago) and the most recent value
                                   value_at_index_6 = Net_interest_Income_annual_10_unpacked[-6]
                                   value_at_index_last = Net_interest_Income_annual_10_unpacked[-1]
                              except Exception as e:
                                   # If there's an error (e.g., insufficient data), set both to 0
                                   value_at_index_6 = 0
                                   value_at_index_last = 0

                              try:
                                   if value_at_index_6 == 0  or all(x == 0 for x in Net_interest_Income_annual_10_unpacked):
                                        # If value at index -6 is 0, CAGR is 0
                                        Net_interest_Income_annual_Cagr_5 = "{:.2f}".format(0.00)
                                   else:
                                        try:
                                             # Calculate CAGR
                                             Net_interest_Income_annual_Cagr_5 = (pow((value_at_index_last / value_at_index_6), 0.2) - 1) * 100
                                             # Handle complex number case
                                             if isinstance(Net_interest_Income_annual_Cagr_5, complex):
                                                  Net_interest_Income_annual_Cagr_5 = "{:.2f}".format(0.00)
                                             else:
                                                  Net_interest_Income_annual_Cagr_5 = "{:.2f}".format(Net_interest_Income_annual_Cagr_5)
                                        except Exception as e:
                                             Net_interest_Income_annual_Cagr_5 = "{:.2f}".format(0.00)
                              except Exception as e:
                                   Net_interest_Income_annual_Cagr_5 = "{:.2f}".format(0.00)

                              # Store the result in session state
                              st.session_state[f'{ticker}_Net_interest_Income_annual_Cagr_5'] = Net_interest_Income_annual_Cagr_5

                              return Net_interest_Income_annual_Cagr_5



                         Net_interest_Income_annual_Cagr_5 = calculate_Net_interest_Income_CAGR_5(Net_interest_Income_annual_10_unpacked, ticker)

#--------------------------------------------------------------------------------------------

                         def calculate_Revenue_per_share_5_cagr(revenue_per_share_annual_10_unpacked, ticker):
                         # Check if the result is already in session state
                              if f'{ticker}_Revenue_per_share_5_cagr(' in st.session_state:
                                   return st.session_state[f'{ticker}_Revenue_per_share_5_cagr(']

                              try:
                                   # Get the value at index -6 (5 years ago) and the most recent value
                                   value_at_index_6 = revenue_per_share_annual_10_unpacked[-6]

                                   value_at_index_last = revenue_per_share_annual_10_unpacked[-1]
                              except Exception as e:
                                   # If there's an error (e.g., insufficient data), set both to 0
                                   value_at_index_6 = 0
                                   value_at_index_last = 0

                              try:
                                   if value_at_index_6 == 0:
                                        # If value at index -6 is 0, CAGR is 0
                                        Revenue_per_share_5_cagr = "{:.2f}".format(0.00)
                                   else:
                                        try:
                                             # Calculate CAGR
                                             Revenue_per_share_5_cagr = (pow((value_at_index_last / value_at_index_6), 1/5) - 1) * 100
                                             # Handle complex number case
                                             if isinstance(Revenue_per_share_5_cagr, complex):
                                                  Revenue_per_share_5_cagr = "{:.2f}".format(0.00)
                                             else:
                                                  Revenue_per_share_5_cagr = "{:.2f}".format(Revenue_per_share_5_cagr)
                                        except Exception as e:
                                             Revenue_per_share_5_cagr = "{:.2f}".format(0.00)
                              except Exception as e:
                                   Revenue_per_share_5_cagr = "{:.2f}".format(0.00)

                              # Store the result in session state
                              st.session_state[f'{ticker}_Revenue_per_share_5_cagr'] = Revenue_per_share_5_cagr

                              return Revenue_per_share_5_cagr
                         
                    

                              # Usage example:
                         
                         Revenue_per_share_5_cagr = calculate_Revenue_per_share_5_cagr(revenue_per_share_annual_10_unpacked, ticker)
                    ###################################################################################################

                         try:
                              value_at_index_2 = revenue_per_share_annual_10_unpacked[-2]
                              value_at_index_last = revenue_per_share_annual_10_unpacked[-1]

                              # Calculate percentage increase
                              if value_at_index_2 != 0:  # Avoid division by zero
                                   percentage_increase = ((value_at_index_last - value_at_index_2) / value_at_index_2) * 100
                                   formatted_percentage = f"{percentage_increase:.2f}%"
                              else:
                                   formatted_percentage = 0.0

                         except Exception as e:
                              formatted_percentage = 0.0

          ###################################################################################################


                         def unpack_data_Cashflow_statement(annual_data, quarterly_data, ticker):
                         # Annual data unpacking (10 years)
                              if f'{ticker}_Changes_in_working_capital_annual_10' in st.session_state:
                                   # If the data already exists in session state, return the unpacked values
                                   return (st.session_state[f'{ticker}_Changes_in_working_capital_annual_10'],
                                             st.session_state[f'{ticker}_Net_Operating_CashFlow_annual_10_unpacked'],
                                             st.session_state[f'{ticker}_Capex_annual_10'],
                                             st.session_state[f'{ticker}_Purchase_of_Investment_annual_10'],
                                             st.session_state[f'{ticker}_Sale_maturity_of_Investments_annual_10'],
                                             st.session_state[f'{ticker}_Net_investing_CashFlow_annual_10'],
                                             st.session_state[f'{ticker}_Insurance_Reduction_of_DebtNet_annual_10'],
                                             st.session_state[f'{ticker}_Debt_issued_annual_10'],
                                             st.session_state[f'{ticker}_Debt_repaid_annual_10'],
                                             st.session_state[f'{ticker}_Stock_issued_of_common_Preferred_stock_annual_10'],
                                             st.session_state[f'{ticker}_Net_Assets_from_Acquisitions_annual_10'],
                                             st.session_state[f'{ticker}_StockBased_Compansation_annual_10'],
                                             st.session_state[f'{ticker}_Repurchase_of_common_Preferred_stock_annual_10'],
                                             st.session_state[f'{ticker}_Cash_Dividends_paid_Total_annual_10'],
                                             st.session_state[f'{ticker}_Net_Financing_cashFlow_annual_10'],
                                             st.session_state[f'{ticker}_Net_change_in_cash_annual_10'],
                                             st.session_state[f'{ticker}_Net_Operating_CashFlow_quarter_10'],
                                             st.session_state[f'{ticker}_changes_in_working_capital_quarter_10'],
                                             st.session_state[f'{ticker}_Capex_quarter_10'],
                                             st.session_state[f'{ticker}_Purchase_of_Investment_quarter_10'],
                                             st.session_state[f'{ticker}_Sale_maturity_of_Investments_quarter_10'],
                                             st.session_state[f'{ticker}_Net_investing_CashFlow_quarter_10'],
                                             st.session_state[f'{ticker}_Cash_Dividends_paid_Total_quarter_10'],
                                             st.session_state[f'{ticker}_Insurance_Reduction_of_DebtNet_quarter_10'],
                                             st.session_state[f'{ticker}_Repurchase_of_common_Preferred_stock_quarter_10'],
                                             st.session_state[f'{ticker}_Net_Financing_cashFlow_quarter_10'],
                                             st.session_state[f'{ticker}_Net_change_in_cash_quarter_10'],
                                             st.session_state[f'{ticker}_Debt_issued_quarter_10'],
                                             st.session_state[f'{ticker}_Debt_repaid_quarter_10'],
                                             st.session_state[f'{ticker}_Stock_issued_of_common_Preferred_stock_quarter_10'],
                                             st.session_state[f'{ticker}_Net_Assets_from_Acquisitions_quarter_10'],
                                             st.session_state[f'{ticker}_StockBased_Compansation_quarter_10'])

                              # Unpacking annual data (last 10 years)
     
                              Changes_in_working_capital_annual_10_unpacked = annual_data['cfo_change_in_working_capital'][-10:]
                              Net_Operating_CashFlow_annual_10_unpacked = annual_data['cf_cfo'][-10:]
                              Capex_annual_10_unpacked = annual_data['cfi_ppe_purchases'][-10:]
                              Purchase_of_Investment_annual_10_unpacked = annual_data['cfi_investment_purchases'][-10:]
                              Sale_maturity_of_Investments_annual_10_unpacked = annual_data['cfi_investment_sales'][-10:]
                              Net_investing_CashFlow_annual_10_unpacked = annual_data['cf_cfi'][-10:]
                              Insurance_Reduction_of_DebtNet_annual_10_unpacked = annual_data['cff_debt_net'][-10:]

                              try:
                                   Debt_issued_annual_10_unpacked = annual_data['cff_debt_issued'][-10:]
                                   Debt_repaid_annual_10_unpacked = annual_data['cff_debt_repaid'][-10:]
                                   Stock_issued_of_common_Preferred_stock_annual_10_unpacked = annual_data['cff_common_stock_issued'][-10:]
                                   Net_Assets_from_Acquisitions_annual_10_unpacked = annual_data['cfi_acquisitions'][-10:]
                                   StockBased_Compansation_annual_10_unpacked = annual_data['cfo_stock_comp'][-10:]
                              except Exception as e:
                                   Debt_issued_annual_10_unpacked = [0] * len_10_annual
                                   Debt_repaid_annual_10_unpacked = [0] * len_10_annual
                                   Stock_issued_of_common_Preferred_stock_annual_10_unpacked = [0] * len_10_annual
                                   Net_Assets_from_Acquisitions_annual_10_unpacked = [0] * len_10_annual
                                   StockBased_Compansation_annual_10_unpacked = [0] * len_10_annual

                              Repurchase_of_common_Preferred_stock_annual_10_unpacked = annual_data['cff_common_stock_repurchased'][-10:]
                              Cash_Dividends_paid_Total_annual_10_unpacked = annual_data['cff_dividend_paid'][-10:]
                              Net_Financing_cashFlow_annual_10_unpacked = annual_data['cf_cff'][-10:]
                              Net_change_in_cash_annual_10_unpacked = annual_data['cf_net_change_in_cash'][-10:]

                              # Unpacking quarterly data (last 10 quarters)
                              Net_Operating_CashFlow_quarter_10_unpacked = quarterly_data['cf_cfo'][-10:]
                              changes_in_working_capital_quarter_10_unpacked = quarterly_data['cfo_change_in_working_capital'][-10:]
                              Capex_quarter_10_unpacked = quarterly_data['cfi_ppe_purchases'][-10:]
                              Purchase_of_Investment_quarter_10_unpacked = quarterly_data['cfi_investment_purchases'][-10:]
                              Sale_maturity_of_Investments_quarter_10_unpacked = quarterly_data['cfi_investment_sales'][-10:]
                              Net_investing_CashFlow_quarter_10_unpacked = quarterly_data['cf_cfi'][-10:]
                              Cash_Dividends_paid_Total_quarter_10_unpacked = quarterly_data['cff_dividend_paid'][-10:]
                              Insurance_Reduction_of_DebtNet_quarter_10_unpacked = quarterly_data['cff_debt_net'][-10:]

                              try:
                                   Debt_issued_quarter_10_unpacked = quarterly_data['cff_debt_issued'][-10:]
                                   Debt_repaid_quarter_10_unpacked = quarterly_data['cff_debt_repaid'][-10:]
                                   Stock_issued_of_common_Preferred_stock_quarter_10_unpacked = quarterly_data['cff_common_stock_issued'][-10:]
                                   Net_Assets_from_Acquisitions_quarter_10_unpacked = quarterly_data['cfi_acquisitions'][-10:]
                                   StockBased_Compansation_quarter_10_unpacked = quarterly_data['cfo_stock_comp'][-10:]
                              except Exception as e:
                                   Debt_issued_quarter_10_unpacked = [0] * len_10_quarter
                                   Debt_repaid_quarter_10_unpacked = [0] * len_10_quarter
                                   Stock_issued_of_common_Preferred_stock_quarter_10_unpacked = [0] * len_10_quarter
                                   Net_Assets_from_Acquisitions_quarter_10_unpacked = [0] * len_10_quarter
                                   StockBased_Compansation_quarter_10_unpacked = [0] * len_10_quarter

                              Repurchase_of_common_Preferred_stock_quarter_10_unpacked = quarterly_data['cff_common_stock_repurchased'][-10:]
                              Net_Financing_cashFlow_quarter_10_unpacked = quarterly_data['cf_cff'][-10:]
                              Net_change_in_cash_quarter_10_unpacked = quarterly_data['cf_net_change_in_cash'][-10:]

                              # Store annual data in session state
                              st.session_state[f'{ticker}_Changes_in_working_capital_annual_10'] = Changes_in_working_capital_annual_10_unpacked
                              st.session_state[f'{ticker}_Net_Operating_CashFlow_annual_10_unpacked'] = Net_Operating_CashFlow_annual_10_unpacked 
                              st.session_state[f'{ticker}_Capex_annual_10'] = Capex_annual_10_unpacked
                              st.session_state[f'{ticker}_Purchase_of_Investment_annual_10'] = Purchase_of_Investment_annual_10_unpacked
                              st.session_state[f'{ticker}_Sale_maturity_of_Investments_annual_10'] = Sale_maturity_of_Investments_annual_10_unpacked
                              st.session_state[f'{ticker}_Net_investing_CashFlow_annual_10'] = Net_investing_CashFlow_annual_10_unpacked
                              st.session_state[f'{ticker}_Insurance_Reduction_of_DebtNet_annual_10'] = Insurance_Reduction_of_DebtNet_annual_10_unpacked
                              st.session_state[f'{ticker}_Debt_issued_annual_10'] = Debt_issued_annual_10_unpacked
                              st.session_state[f'{ticker}_Debt_repaid_annual_10'] = Debt_repaid_annual_10_unpacked
                              st.session_state[f'{ticker}_Stock_issued_of_common_Preferred_stock_annual_10'] = Stock_issued_of_common_Preferred_stock_annual_10_unpacked
                              st.session_state[f'{ticker}_Net_Assets_from_Acquisitions_annual_10'] = Net_Assets_from_Acquisitions_annual_10_unpacked
                              st.session_state[f'{ticker}_StockBased_Compansation_annual_10'] = StockBased_Compansation_annual_10_unpacked
                              st.session_state[f'{ticker}_Repurchase_of_common_Preferred_stock_annual_10'] = Repurchase_of_common_Preferred_stock_annual_10_unpacked
                              st.session_state[f'{ticker}_Cash_Dividends_paid_Total_annual_10'] = Cash_Dividends_paid_Total_annual_10_unpacked
                              st.session_state[f'{ticker}_Net_Financing_cashFlow_annual_10'] = Net_Financing_cashFlow_annual_10_unpacked
                              st.session_state[f'{ticker}_Net_change_in_cash_annual_10'] = Net_change_in_cash_annual_10_unpacked

                              # Store quarterly data in session state
                              st.session_state[f'{ticker}_Net_Operating_CashFlow_quarter_10'] = Net_Operating_CashFlow_quarter_10_unpacked
                              st.session_state[f'{ticker}_changes_in_working_capital_quarter_10'] = changes_in_working_capital_quarter_10_unpacked
                              st.session_state[f'{ticker}_Capex_quarter_10'] = Capex_quarter_10_unpacked
                              st.session_state[f'{ticker}_Purchase_of_Investment_quarter_10'] = Purchase_of_Investment_quarter_10_unpacked
                              st.session_state[f'{ticker}_Sale_maturity_of_Investments_quarter_10'] = Sale_maturity_of_Investments_quarter_10_unpacked
                              st.session_state[f'{ticker}_Net_investing_CashFlow_quarter_10'] = Net_investing_CashFlow_quarter_10_unpacked
                              st.session_state[f'{ticker}_Cash_Dividends_paid_Total_quarter_10'] = Cash_Dividends_paid_Total_quarter_10_unpacked
                              st.session_state[f'{ticker}_Insurance_Reduction_of_DebtNet_quarter_10'] = Insurance_Reduction_of_DebtNet_quarter_10_unpacked
                              st.session_state[f'{ticker}_Debt_issued_quarter_10'] = Debt_issued_quarter_10_unpacked
                              st.session_state[f'{ticker}_Debt_repaid_quarter_10'] = Debt_repaid_quarter_10_unpacked
                              st.session_state[f'{ticker}_Stock_issued_of_common_Preferred_stock_quarter_10'] = Stock_issued_of_common_Preferred_stock_quarter_10_unpacked
                              st.session_state[f'{ticker}_Net_Assets_from_Acquisitions_quarter_10'] = Net_Assets_from_Acquisitions_quarter_10_unpacked
                              st.session_state[f'{ticker}_StockBased_Compansation_quarter_10'] = StockBased_Compansation_quarter_10_unpacked
                              st.session_state[f'{ticker}_Repurchase_of_common_Preferred_stock_quarter_10'] = Repurchase_of_common_Preferred_stock_quarter_10_unpacked
                              st.session_state[f'{ticker}_Net_Financing_cashFlow_quarter_10'] = Net_Financing_cashFlow_quarter_10_unpacked
                              st.session_state[f'{ticker}_Net_change_in_cash_quarter_10'] = Net_change_in_cash_quarter_10_unpacked

                              return (Changes_in_working_capital_annual_10_unpacked, Net_Operating_CashFlow_annual_10_unpacked ,Capex_annual_10_unpacked,
                                        Purchase_of_Investment_annual_10_unpacked, Sale_maturity_of_Investments_annual_10_unpacked,
                                        Net_investing_CashFlow_annual_10_unpacked, Insurance_Reduction_of_DebtNet_annual_10_unpacked,
                                        Debt_issued_annual_10_unpacked, Debt_repaid_annual_10_unpacked,
                                        Stock_issued_of_common_Preferred_stock_annual_10_unpacked, Net_Assets_from_Acquisitions_annual_10_unpacked,
                                        StockBased_Compansation_annual_10_unpacked, Repurchase_of_common_Preferred_stock_annual_10_unpacked,
                                        Cash_Dividends_paid_Total_annual_10_unpacked, Net_Financing_cashFlow_annual_10_unpacked,
                                        Net_change_in_cash_annual_10_unpacked, Net_Operating_CashFlow_quarter_10_unpacked,
                                        changes_in_working_capital_quarter_10_unpacked, Capex_quarter_10_unpacked,
                                        Purchase_of_Investment_quarter_10_unpacked, Sale_maturity_of_Investments_quarter_10_unpacked,
                                        Net_investing_CashFlow_quarter_10_unpacked, Cash_Dividends_paid_Total_quarter_10_unpacked,
                                        Insurance_Reduction_of_DebtNet_quarter_10_unpacked, Debt_issued_quarter_10_unpacked,
                                        Debt_repaid_quarter_10_unpacked, Stock_issued_of_common_Preferred_stock_quarter_10_unpacked,
                                        Net_Assets_from_Acquisitions_quarter_10_unpacked, StockBased_Compansation_quarter_10_unpacked,
                                        Repurchase_of_common_Preferred_stock_quarter_10_unpacked, Net_Financing_cashFlow_quarter_10_unpacked,
                                        Net_change_in_cash_quarter_10_unpacked)
                         
                         (Changes_in_working_capital_annual_10_unpacked,Net_Operating_CashFlow_annual_10_unpacked,Capex_annual_10_unpacked,
                                        Purchase_of_Investment_annual_10_unpacked, Sale_maturity_of_Investments_annual_10_unpacked,
                                        Net_investing_CashFlow_annual_10_unpacked, Insurance_Reduction_of_DebtNet_annual_10_unpacked,
                                        Debt_issued_annual_10_unpacked, Debt_repaid_annual_10_unpacked,
                                        Stock_issued_of_common_Preferred_stock_annual_10_unpacked, Net_Assets_from_Acquisitions_annual_10_unpacked,
                                        StockBased_Compansation_annual_10_unpacked, Repurchase_of_common_Preferred_stock_annual_10_unpacked,
                                        Cash_Dividends_paid_Total_annual_10_unpacked, Net_Financing_cashFlow_annual_10_unpacked,
                                        Net_change_in_cash_annual_10_unpacked, Net_Operating_CashFlow_quarter_10_unpacked,
                                        changes_in_working_capital_quarter_10_unpacked, Capex_quarter_10_unpacked,
                                        Purchase_of_Investment_quarter_10_unpacked, Sale_maturity_of_Investments_quarter_10_unpacked,
                                        Net_investing_CashFlow_quarter_10_unpacked, Cash_Dividends_paid_Total_quarter_10_unpacked,
                                        Insurance_Reduction_of_DebtNet_quarter_10_unpacked, Debt_issued_quarter_10_unpacked,
                                        Debt_repaid_quarter_10_unpacked, Stock_issued_of_common_Preferred_stock_quarter_10_unpacked,
                                        Net_Assets_from_Acquisitions_quarter_10_unpacked, StockBased_Compansation_quarter_10_unpacked,
                                        Repurchase_of_common_Preferred_stock_quarter_10_unpacked, Net_Financing_cashFlow_quarter_10_unpacked,
                                        Net_change_in_cash_quarter_10_unpacked) =unpack_data_Cashflow_statement(annual_data, quarterly_data, ticker)

          ###################################################################################################


          ###################################################################################################
                         def data_totalCashDebt(quarterly_data, annual_data, Financial_data):
                              if f'{ticker}_Ebita_ttm' in st.session_state:
                                   return (
                                        st.session_state[f'{ticker}_Ebita_ttm'],
                                        st.session_state[f'{ticker}_Accounts_payable_quarter10'],
                                        st.session_state[f'{ticker}_Current_accrued_liab_quarter10'],
                                        st.session_state[f'{ticker}_Tax_payable_quarter10'],
                                        st.session_state[f'{ticker}_Other_current_liabilities_quarter10'],
                                        st.session_state[f'{ticker}_Current_deferred_revenue_quarter10'],
                                        st.session_state[f'{ticker}_Total_current_liabilities_quarter10'],
                                        st.session_state[f'{ticker}_capital_leases_quarter10'],
                                        st.session_state[f'{ticker}_LongTerm_debt_quarter10'],
                                        st.session_state[f'{ticker}_current_portion_of_lease_obligation_quarter10'],
                                        st.session_state[f'{ticker}_st_investments_quarter1'],
                                        st.session_state[f'{ticker}_Short_term_debt_quarter10'],
                                        st.session_state[f'{ticker}_Other_longterm_liabilities_quarter10'],
                                        st.session_state[f'{ticker}_Total_liabilities_quarter10'],
                                        st.session_state[f'{ticker}_Total_Equity_quarter10'],
                                        st.session_state[f'{ticker}_Total_Equity_quarter1'],
                                        st.session_state[f'{ticker}_Total_Equity_annual1'],
                                        st.session_state[f'{ticker}_gross_margin_annual5'],
                                        st.session_state[f'{ticker}_gross_margin_annual10'],
                                        st.session_state[f'{ticker}_operating_margin_quater1'],
                                        st.session_state[f'{ticker}_operating_margin_quater10'],
                                        st.session_state[f'{ticker}_operating_margin_annual1'],
                                        st.session_state[f'{ticker}_operating_margin_annual5'],
                                        st.session_state[f'{ticker}_operating_margin_annual10'],
                                        
                                        st.session_state[f'{ticker}_debt_Assets_annual1'],
                                        st.session_state[f'{ticker}_debt_equity_annual1'],
                                        st.session_state[f'{ticker}_debt_Assets_annual10'],
                                        st.session_state[f'{ticker}_LongTerm_debt_annual1'],
                                        st.session_state[f'{ticker}_Short_term_debt_annual1'],
                                        st.session_state[f'{ticker}_Total_assets_annual1'],
                                        st.session_state[f'{ticker}_Cash_Dividends_paid_Total_annual1'],
                                        st.session_state[f'{ticker}_cash_equiv_quarter1']
                                   )

                              Ebita_ttm = Financial_data['ttm']['ebitda'] / 1_000_000_000
                              # Unpacking data with error handling
                              try:
                                   Accounts_payable_quarter10_unpacked = quarterly_data['accounts_payable'][-10:]
                              except KeyError:
                                   Accounts_payable_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   Current_accrued_liab_quarter10_unpacked = quarterly_data['current_accrued_liabilities'][-10:]
                              except KeyError:
                                   Current_accrued_liab_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   Tax_payable_quarter10_unpacked = quarterly_data['tax_payable'][-10:]
                              except KeyError:
                                   Tax_payable_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   Other_current_liabilities_quarter10_unpacked = quarterly_data['other_current_liabilities'][-10:]
                              except KeyError:
                                   Other_current_liabilities_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   Current_deferred_revenue_quarter10_unpacked = quarterly_data['current_deferred_revenue'][-10:]
                              except KeyError:
                                   Current_deferred_revenue_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   Total_current_liabilities_quarter10_unpacked = quarterly_data['total_current_liabilities'][-10:]
                              except KeyError:
                                   Total_current_liabilities_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   capital_leases_quarter10_unpacked = quarterly_data['noncurrent_capital_leases'][-10:]
                              except KeyError:
                                   capital_leases_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   LongTerm_debt_quarter10_unpacked = quarterly_data['lt_debt'][-10:]
                              except KeyError:
                                   LongTerm_debt_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   current_portion_of_lease_obligation_quarter10_unpacked = quarterly_data['current_capital_leases'][-10:]
                              except KeyError:
                                   current_portion_of_lease_obligation_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   st_investments_quarter1_unpacked = quarterly_data['st_investments'][-1:]
                              except KeyError:
                                   st_investments_quarter1_unpacked = [0] * 1

                              try:
                                   Short_term_debt_quarter10_unpacked = quarterly_data['st_debt'][-10:]
                              except KeyError:
                                   Short_term_debt_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   Other_longterm_liabilities_quarter10_unpacked = quarterly_data['other_lt_liabilities'][-10:]
                              except KeyError:
                                   Other_longterm_liabilities_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   Total_liabilities_quarter10_unpacked = quarterly_data['total_liabilities'][-10:]
                              except KeyError:
                                   Total_liabilities_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   Total_Equity_quarter10_unpacked = quarterly_data['total_equity'][-10:]
                              except KeyError:
                                   Total_Equity_quarter10_unpacked = [0] * len_10_quarter

                              try:
                                   Total_Equity_quarter1_unpacked = quarterly_data['total_equity'][-1:]
                              except KeyError:
                                   Total_Equity_quarter1_unpacked = [0] * 1

                              try:
                                   Total_Equity_annual1_unpacked = annual_data['total_equity'][-1:]
                              except KeyError:
                                   Total_Equity_annual1_unpacked = [0] * 1

                              try:
                                   gross_margin_annual5_unpacked = annual_data['gross_margin'][-5:]
                              except KeyError:
                                   gross_margin_annual5_unpacked = [0] * len_5_annual

                              try:
                                   gross_margin_annual10_unpacked = annual_data['gross_margin'][-10:]
                              except KeyError:
                                   gross_margin_annual10_unpacked = [0] * len_10_annual

                              try:
                                   operating_margin_quater1_unpacked = quarterly_data['operating_margin'][-1:]
                              except KeyError:
                                   operating_margin_quater1_unpacked = [0] * 1

                              try:
                                   operating_margin_quater10_unpacked = quarterly_data['operating_margin'][-10:]
                              except KeyError:
                                   operating_margin_quater10_unpacked = [0] * len_10_quarter

                              try:
                                   operating_margin_annual1_unpacked = annual_data['operating_margin'][-1:]
                              except KeyError:
                                   operating_margin_annual1_unpacked = [0] * 1

                              try:
                                   operating_margin_annual5_unpacked = annual_data['operating_margin'][-5:]
                              except KeyError:
                                   operating_margin_annual5_unpacked = [0] * len_5_annual

                              try:
                                   operating_margin_annual10_unpacked = annual_data['operating_margin'][-10:]
                              except KeyError:
                                   operating_margin_annual10_unpacked = [0] * len_10_annual

                              try:
                                   debt_Assets_annual1_unpacked = annual_data['debt_to_assets'][-1:]
                              except KeyError:
                                   debt_Assets_annual1_unpacked = [0] * 1

                              try:
                                   debt_equity_annual1_unpacked = quarterly_data['debt_to_equity'][-1:]
                              except KeyError:
                                   debt_equity_annual1_unpacked = [0] * 1

                              try:
                                   debt_Assets_annual10_unpacked = annual_data['debt_to_assets'][-10:]
                              except KeyError:
                                   debt_Assets_annual10_unpacked = [0] * len_10_annual

                              try:
                                   LongTerm_debt_annual1_unpacked = annual_data['lt_debt'][-1:]
                              except KeyError:
                                   LongTerm_debt_annual1_unpacked = [0] * 1

                              try:
                                   Short_term_debt_annual1_unpacked = annual_data['st_debt'][-1:]
                              except KeyError:
                                   Short_term_debt_annual1_unpacked = [0] * 1

                              try:
                                   Total_assets_annual1_unpacked = annual_data['total_assets'][-1:]
                              except KeyError:
                                   Total_assets_annual1_unpacked = [0] * 1

                              try:
                                   Cash_Dividends_paid_Total_annual1_unpacked = annual_data['cff_dividend_paid'][-1:]
                              except KeyError:
                                   Cash_Dividends_paid_Total_annual1_unpacked = [0] * 1

                              try:
                                   cash_equiv_quarter1_unpacked = quarterly_data['cash_and_equiv'][-1:]
                              except KeyError:
                                   cash_equiv_quarter1_unpacked = [0] * 1

                              # Store the unpacked data in session state
                              st.session_state[f'{ticker}_Ebita_ttm'] = Ebita_ttm
                              st.session_state[f'{ticker}_Accounts_payable_quarter10'] = Accounts_payable_quarter10_unpacked
                              st.session_state[f'{ticker}_Current_accrued_liab_quarter10'] = Current_accrued_liab_quarter10_unpacked
                              st.session_state[f'{ticker}_Tax_payable_quarter10'] = Tax_payable_quarter10_unpacked
                              st.session_state[f'{ticker}_Other_current_liabilities_quarter10'] = Other_current_liabilities_quarter10_unpacked
                              st.session_state[f'{ticker}_Current_deferred_revenue_quarter10'] = Current_deferred_revenue_quarter10_unpacked
                              st.session_state[f'{ticker}_Total_current_liabilities_quarter10'] = Total_current_liabilities_quarter10_unpacked
                              st.session_state[f'{ticker}_current_portion_of_lease_obligation_quarter10'] = current_portion_of_lease_obligation_quarter10_unpacked
                              st.session_state[f'{ticker}_capital_leases_quarter10'] = capital_leases_quarter10_unpacked
                              st.session_state[f'{ticker}_LongTerm_debt_quarter10'] = LongTerm_debt_quarter10_unpacked
                              st.session_state[f'{ticker}_st_investments_quarter1'] = st_investments_quarter1_unpacked
                              st.session_state[f'{ticker}_Short_term_debt_quarter10'] = Short_term_debt_quarter10_unpacked
                              st.session_state[f'{ticker}_Other_longterm_liabilities_quarter10'] = Other_longterm_liabilities_quarter10_unpacked
                              st.session_state[f'{ticker}_Total_liabilities_quarter10'] = Total_liabilities_quarter10_unpacked
                              st.session_state[f'{ticker}_Total_Equity_quarter10'] = Total_Equity_quarter10_unpacked
                              st.session_state[f'{ticker}_Total_Equity_quarter1'] = Total_Equity_quarter1_unpacked
                              st.session_state[f'{ticker}_Total_Equity_annual1'] = Total_Equity_annual1_unpacked
                              st.session_state[f'{ticker}_gross_margin_annual5'] = gross_margin_annual5_unpacked
                              st.session_state[f'{ticker}_gross_margin_annual10'] = gross_margin_annual10_unpacked
                              st.session_state[f'{ticker}_operating_margin_quater1'] = operating_margin_quater1_unpacked
                              st.session_state[f'{ticker}_operating_margin_quater10'] = operating_margin_quater10_unpacked
                              st.session_state[f'{ticker}_operating_margin_annual1'] = operating_margin_annual1_unpacked
                              st.session_state[f'{ticker}_operating_margin_annual5'] = operating_margin_annual5_unpacked
                              st.session_state[f'{ticker}_operating_margin_annual10'] = operating_margin_annual10_unpacked
                              st.session_state[f'{ticker}_debt_Assets_annual1'] = debt_Assets_annual1_unpacked
                              st.session_state[f'{ticker}_debt_equity_annual1'] = debt_equity_annual1_unpacked
                              st.session_state[f'{ticker}_debt_Assets_annual10'] = debt_Assets_annual10_unpacked
                              st.session_state[f'{ticker}_LongTerm_debt_annual1'] = LongTerm_debt_annual1_unpacked
                              st.session_state[f'{ticker}_Short_term_debt_annual1'] = Short_term_debt_annual1_unpacked
                              st.session_state[f'{ticker}_Total_assets_annual1'] = Total_assets_annual1_unpacked
                              st.session_state[f'{ticker}_Cash_Dividends_paid_Total_annual1'] = Cash_Dividends_paid_Total_annual1_unpacked
                              st.session_state[f'{ticker}_cash_equiv_quarter1'] = cash_equiv_quarter1_unpacked

                              return (
                                   Ebita_ttm,
                                   Accounts_payable_quarter10_unpacked,
                                   Current_accrued_liab_quarter10_unpacked,
                                   Tax_payable_quarter10_unpacked,
                                   Other_current_liabilities_quarter10_unpacked,
                                   Current_deferred_revenue_quarter10_unpacked,
                                   Total_current_liabilities_quarter10_unpacked,
                                   current_portion_of_lease_obligation_quarter10_unpacked,
                                   capital_leases_quarter10_unpacked,
                                   LongTerm_debt_quarter10_unpacked,
                                   st_investments_quarter1_unpacked,
                                   Short_term_debt_quarter10_unpacked,
                                   Other_longterm_liabilities_quarter10_unpacked,
                                   Total_liabilities_quarter10_unpacked,
                                   Total_Equity_quarter10_unpacked,
                                   Total_Equity_quarter1_unpacked,
                                   Total_Equity_annual1_unpacked,
                                   gross_margin_annual5_unpacked,
                                   gross_margin_annual10_unpacked,
                                   operating_margin_quater1_unpacked,
                                   operating_margin_quater10_unpacked,
                                   operating_margin_annual1_unpacked,
                                   operating_margin_annual5_unpacked,
                                   operating_margin_annual10_unpacked,
                              
                                   debt_Assets_annual1_unpacked,
                                   debt_equity_annual1_unpacked,
                                   debt_Assets_annual10_unpacked,
                                   LongTerm_debt_annual1_unpacked,
                                   Short_term_debt_annual1_unpacked,
                                   Total_assets_annual1_unpacked,
                                   Cash_Dividends_paid_Total_annual1_unpacked,
                                   cash_equiv_quarter1_unpacked
                              )

                         (
                         Ebita_ttm,
                         Accounts_payable_quarter10_unpacked,
                         Current_accrued_liab_quarter10_unpacked,
                         Tax_payable_quarter10_unpacked,
                         Other_current_liabilities_quarter10_unpacked,
                         Current_deferred_revenue_quarter10_unpacked,
                         Total_current_liabilities_quarter10_unpacked,
                         current_portion_of_lease_obligation_quarter10_unpacked,
                         capital_leases_quarter10_unpacked,
                         LongTerm_debt_quarter10_unpacked,
                         st_investments_quarter1_unpacked,
                         Short_term_debt_quarter10_unpacked,
                         Other_longterm_liabilities_quarter10_unpacked,
                         Total_liabilities_quarter10_unpacked,
                         Total_Equity_quarter10_unpacked,
                         Total_Equity_quarter1_unpacked,
                         Total_Equity_annual1_unpacked,
                         gross_margin_annual5_unpacked,
                         gross_margin_annual10_unpacked,
                         operating_margin_quater1_unpacked,
                         operating_margin_quater10_unpacked,
                         operating_margin_annual1_unpacked,
                         operating_margin_annual5_unpacked,
                         operating_margin_annual10_unpacked,
                         
                         debt_Assets_annual1_unpacked,
                         debt_equity_annual1_unpacked,
                         debt_Assets_annual10_unpacked,
                         LongTerm_debt_annual1_unpacked,
                         Short_term_debt_annual1_unpacked,
                         Total_assets_annual1_unpacked,
                         Cash_Dividends_paid_Total_annual1_unpacked,
                         cash_equiv_quarter1_unpacked
                         ) = data_totalCashDebt(quarterly_data, annual_data, Financial_data)


          ###################################################################################################
                         try:
                              def unpack_and_store_fundamental_data(quote, ticker):
                                   # Check if data is already in session state
                              
                                   if f'{ticker}_forwardPE' in st.session_state:
                                        return (
                                             st.session_state[f'{ticker}_forwardPE'],
                                             st.session_state[f'{ticker}_RSI'],
                                             st.session_state[f'{ticker}_PEG'],
                                             st.session_state[f'{ticker}_Beta'],
                                             st.session_state[f'{ticker}_Moving_200'],
                                             st.session_state[f'{ticker}_Moving_50'],
                                             st.session_state[f'{ticker}_Target_Price'],
                                             st.session_state[f'{ticker}_Dividend_TTM'],
                                             st.session_state[f'{ticker}_Dividend_Est'],
                                             st.session_state[f'{ticker}_Dividend_Ex_Date'],
                                             st.session_state[f'{ticker}_Earnings_this_yr'],
                                             st.session_state[f'{ticker}_Earnings_next_yr_in_prozent'],
                                             st.session_state[f'{ticker}_Earnings_next_yr_in_value'],
                                             st.session_state[f'{ticker}_Earnings_next_5_yrs'],
                                             st.session_state[f'{ticker}_debt_equity_ttm']
                                        )

                         
                              
                                   # Unpacking the data from quote.fundamental_df
                                   try:            
                                        #quote = Quote(ticker)

                                        forwardPE = quote.fundamental_df.at[0, "Forward P/E"]
                                        RSI = quote.fundamental_df.at[0, "RSI (14)"]
                                        PEG = quote.fundamental_df.at[0, "PEG"]
                                        Beta = quote.fundamental_df.at[0, "Beta"]
                                        Moving_200 = quote.fundamental_df.at[0, "SMA200"]
                                        Moving_50 = quote.fundamental_df.at[0, "SMA50"]
                                        Target_Price = quote.fundamental_df.at[0, "Target Price"]
                                        Dividend_TTM = quote.fundamental_df.at[0, "Dividend TTM"]
                                        Dividend_Est = quote.fundamental_df.at[0, "Dividend Est."]
                                        Dividend_Ex_Date = quote.fundamental_df.at[0, "Dividend Ex-Date"]
                                        Earnings_this_yr = quote.fundamental_df.at[0, "EPS this Y"]
                                        Earnings_next_yr_in_prozent = quote.fundamental_df.at[0, "EPS next Y - EPS growth next year"]
                                        Earnings_next_yr_in_value = quote.fundamental_df.at[0, "EPS next Y - EPS estimate for next year"]
                                        Earnings_next_5_yrs = quote.fundamental_df.at[0, "EPS next 5Y"]
                                        debt_equity_ttm = quote.fundamental_df.at[0, "Debt/Eq"]

                         

                                   except Exception as e:
                                        forwardPE = "{:.2f}".format(00.00)
                                        RSI = "{:.2f}".format(0.00)
                                        PEG = "{:.2f}".format(0.00)
                                        Beta = beta
                                        Moving_200 = "{:.2f}".format(0.00)
                                        Moving_50 = "{:.2f}".format(0.00)
                                        Target_Price = "{:.2f}".format(0.00)
                                        Dividend_TTM = "{:.2f}".format(0.00)
                                        Dividend_Est = "{:.2f}".format(0.00)
                                        Dividend_Ex_Date = "{:.2f}".format(0.00)
                                        Earnings_this_yr = "{:.2f}".format(0.00)
                                        Earnings_next_yr_in_prozent = "{:.2f}".format(0.00)
                                        Earnings_next_yr_in_value = "{:.2f}".format(0.00)
                                        Earnings_next_5_yrs = "{:.2f}".format(0.00)


                                   # Store the data in session state
                                   st.session_state[f'{ticker}_forwardPE'] = forwardPE
                                   st.session_state[f'{ticker}_RSI'] = RSI
                                   st.session_state[f'{ticker}_PEG'] = PEG
                                   st.session_state[f'{ticker}_Beta'] = Beta
                                   st.session_state[f'{ticker}_Moving_200'] = Moving_200
                                   st.session_state[f'{ticker}_Moving_50'] = Moving_50
                                   st.session_state[f'{ticker}_Target_Price'] = Target_Price
                                   st.session_state[f'{ticker}_Dividend_TTM'] = Dividend_TTM
                                   st.session_state[f'{ticker}_Dividend_Est'] = Dividend_Est
                                   st.session_state[f'{ticker}_Dividend_Ex_Date'] = Dividend_Ex_Date
                                   st.session_state[f'{ticker}_Earnings_this_yr'] = Earnings_this_yr
                                   st.session_state[f'{ticker}_Earnings_next_yr_in_prozent'] = Earnings_next_yr_in_prozent
                                   st.session_state[f'{ticker}_Earnings_next_yr_in_value'] = Earnings_next_yr_in_value
                                   st.session_state[f'{ticker}_Earnings_next_5_yrs'] = Earnings_next_5_yrs
                                   st.session_state[f'{ticker}_debt_equity_ttm'] = debt_equity_ttm

                                   return (forwardPE, RSI, PEG, Beta, Moving_200, Moving_50, 
                                        Target_Price, Dividend_TTM, Dividend_Est, Dividend_Ex_Date, 
                                        Earnings_this_yr, Earnings_next_yr_in_prozent, Earnings_next_yr_in_value, 
                                        Earnings_next_5_yrs, debt_equity_ttm)

                              (forwardPE, RSI, PEG, Beta, Moving_200, Moving_50, Target_Price, Dividend_TTM, Dividend_Est, Dividend_Ex_Date, Earnings_this_yr, 
                              Earnings_next_yr_in_prozent, Earnings_next_yr_in_value, Earnings_next_5_yrs, debt_equity_ttm) = unpack_and_store_fundamental_data(quote, ticker)

                         except Exception as e:
                              forwardPE = "{:.2f}".format(00.00)
                              RSI = "{:.2f}".format(0.00)
                              PEG = "{:.2f}".format(0.00)
                              Beta = beta
                              Moving_200 = "{:.2f}".format(0.00)
                              Moving_50 = "{:.2f}".format(0.00)
                              Target_Price = "{:.2f}".format(0.00)
                              Dividend_TTM = "{:.2f}".format(0.00)
                              Dividend_Est = "{:.2f}".format(0.00)
                              Dividend_Ex_Date = "{:.2f}".format(0.00)
                              Earnings_this_yr = "{:.2f}".format(0.00)
                              Earnings_next_yr_in_prozent = "{:.2f}".format(0.00)
                              Earnings_next_yr_in_value = "{:.2f}".format(0.00)
                              Earnings_next_5_yrs = "{:.2f}".format(0.00)
                              debt_equity_ttm = "{:.2f}".format(0.0)

          ###################################################################################################

                         debt_equity_ttm = round((((sum(debt_equity_annual1_unpacked) / len(debt_equity_annual1_unpacked)))), 2)
                         try:
                              debt_equity_ttm ="{:.2f}".format(Financial_data['ttm']['debt_to_equity'])

                         except Exception as e:
                              
                              debt_equity_ttm =debt_equity_ttm
                        

          
                         if Revenue_ttm!=0 and average_revenue_annual_ttm !=0 :
                              Price_to_sales_last = "{:.2f}".format(Marketcap/(Revenue_ttm/1000000000))
                              Net_margin_ttm ="{:.2f}%".format((Net_income_margin_1)*100)
                         else:
                              Price_to_sales_last = "NA"
                              Net_margin_ttm="NA"
                         
                         
                    

                    

                         if not pd.isna(Marketcap) and not pd.isna(netincome_ttm) and netincome_ttm != 0 and fcf_ttm !=0:
                    
                              try:
                                   pe_ttm =quote.fundamental_df.at[0, "P/E"]

                              except Exception as e:
                                   pe_ttm = "{:.2f} ".format(Marketcap / netincome_ttm)
                                   
                              pfcf_ttm="{:.2f} ".format(Marketcap / fcf_ttm)  
                              

                         elif not pd.isna(amount) and not pd.isna(eps_diluted_ttm) and eps_diluted_ttm != 0:
                              pe_ttm = "{:.2f} ".format(amount / eps_diluted_ttm)




                         if netincome_ttm is None:
                              pe_ttm = "{:.2f} ".format(amount / eps_diluted_ttm)
                         
                         if fcf_ttm is None or fcf_ttm < 0.0:
                              pfcf_ttm="-"
                         if netincome_ttm < 0:
                              pe_ttm = "-"    
                         else:
                              pfcf_ttm="-" 
                              
                         try:
                              if fcf_ttm == 0.00:
                                   pfcf_ttm= "-"
                              else:
                                   pfcf_ttm="{:.2f} ".format(Marketcap / fcf_ttm) 
                         

                         except Exception as a:
                              
                              pfcf_ttm="-"
                              


                         if len(Revenue_annual_10_unpacked) >= 10:
                              P_OCF_10="{:.2f}".format(Marketcap/((sum(Net_Operating_CashFlow_annual_10_unpacked)/len(Net_Operating_CashFlow_annual_10_unpacked))/1000000000))
                              P_sales_10="{:.2f}".format(Marketcap/((sum(Revenue_annual_10_unpacked)/len(Revenue_annual_10_unpacked))/1000000000))
                              Average_fcf_growth_ten =  "{:.2f}".format(((sum(fcf_growth_annual_10_unpacked) / len(fcf_growth_annual_10_unpacked)))*100)
                              average_PE_historical = "{:.2f}".format((sum(pe_annual_10_unpacked) / len(pe_annual_10_unpacked)))
                              pfcf_ten="{:.2f}".format(Marketcap/(rounded_fcf_Annual_ten/1000000000))

                              Net_income_margin_10 = "{:.2f}".format((Net_income_margin_10years)*100)
                              FCF_Margin_10 = "{:.2f}".format(FCF_Margin_10)
                              EPS_growth_10yrs="{:.2f}".format(EPS_growth_10yrs)
                              Average_pe_ten = "{:.2f}".format(sum(pe_annual_10_unpacked) / len(pe_annual_10_unpacked))

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
                              P_sales_10 = "-"
                              

                         try:

                              AverageEndPrice_annual5 =sum(AverageEndPrice_annual5_unpacked)/len(AverageEndPrice_annual5_unpacked)


                         except Exception as e: 
                              
                              AverageEndPrice_annual10_unpacked = 0.0
          

                         if len(Divdends_paid_annual_5_unpacked) >= 5:
                              Divdend_per_share_yield_average =sum(Divdends_paid_annual_5_unpacked) / len(Divdends_paid_annual_5_unpacked)
                              Dividend_yield_average ="{:.2f}%".format(abs((Divdend_per_share_yield_average)/AverageEndPrice_annual5)*100)
                              

                         else:
                                   
                              Dividend_yield_average ="{:.2f}%".format(0.00)


                         try:
                              if len(Revenue_annual_5_unpacked) >= 5:
                                   Average_ROIC_funf = "{:.2f}%".format(Average_ROIC_funf)
                                   average_FCF_annual_five_we = (
                                        "{:.2f}B".format(rounded_fcf_Annual_five / 1_000_000_000)
                                        if abs(rounded_fcf_Annual_five) >= 1_000_000_000
                                        else "{:,.1f}M".format(rounded_fcf_Annual_five / 1_000_000)
                                   )
                                   five_ROE = "{:.2f}".format(
                                        (sum(ROE_annual_5_unpacked) / len(ROE_annual_5_unpacked)) * 100
                                   )
                                   pe_five_ = "{:.2f}".format(
                                        float(Marketcap) / (Average_net_income_annual_funf / 1_000_000_000)
                                   )
                                   pfcf_funf = "{:.2f}".format(
                                        Marketcap / (rounded_fcf_Annual_five / 1_000_000_000)
                                   )
                                   P_OCF_5= "{:.2f}".format(Marketcap/((sum(Net_Operating_CashFlow_annual_5_unpacked)/len(Net_Operating_CashFlow_annual_5_unpacked))/1000000000))

                                   KCV = pfcf_funf
                                   KGV = pe_five_
                                   five_Yrs_ROE = "{:.2f}".format(
                                        (sum(ROE_annual_5_unpacked) / len(ROE_annual_5_unpacked)) * 100
                                   )
                                   Average_fcf_growth_five = "{:.2f}%".format(
                                        (sum(fcf_growth_annual_5_unpacked) / len(fcf_growth_annual_5_unpacked)) * 100
                                   )
                                   Average_pe_five = "{:.2f}".format(
                                        sum(pe_annual_5_unpacked) / len(pe_annual_5_unpacked)
                                   )
                                   five_yrs_Nettomarge = "{:.2f}".format(Net_income_margin_annual5 * 100)
                                   FCF_Margin_5 = "{:.2f}".format(FCF_Margin_5 * 100)
                                   P_sales_5="{:.2f}".format(Marketcap/((sum(Revenue_annual_5_unpacked)/len(Revenue_annual_5_unpacked))/1000000000))
                              else:
                                   raise ValueError(" ")

                         except Exception as e:

                              # Set fallback/default values
                              Average_ROIC_funf = "NA"
                              average_FCF_annual_five_we = "{:.2f}".format(0.0)
                              five_yrs_Nettomarge = "0.00"
                              five_ROE = "0.00"
                              pfcf_funf = "-"
                              pe_five_ = "-"
                              average_PE_historical = "-"
                              P_OCF_5 = "-"
                              KGV = 0.0
                              KCV = 0.0
                              five_Yrs_ROE = 0.0
                              Average_fcf_growth_five = "0.00"
                              Average_pe_five = "0.00"
                              FCF_Margin_5 = "-"
                              P_sales_5 = "-"
                         
 

                         
                         Dividend_per_share_yield_no_percentage =abs((Divdend_per_share_ttm)/current_price)*100
                         Dividend_per_share_yield ="{:.2f}%".format(abs((Divdend_per_share_ttm)/current_price)*100)

                         Average_total_equity_annual = (sum(Total_Equity_annual1_unpacked) / len(Total_Equity_annual1_unpacked))

                         average_gross_margin_quater1 = "{:.2f}%".format(((sum(gross_margin_quarter1_unpacked) / len(gross_margin_quarter1_unpacked)) * 100))

                         five_yrs_average_gross_margin = "{:.2f}%".format((sum(gross_margin_annual5_unpacked) / len(gross_margin_annual5_unpacked)) * 100)

                         average_operating_margin1_quarter = "{:.2f}%".format((sum(operating_margin_quater1_unpacked) / len(operating_margin_quater1_unpacked)) * 100)

                         five_yrs_average_operating_margin= "{:.2f}%".format((sum(operating_margin_annual5_unpacked) / len(operating_margin_annual5_unpacked)) * 100)

                    
                         st_investments_quarter1 = ((sum(st_investments_quarter1_unpacked) / len(st_investments_quarter1_unpacked)) / 1000000000)
                         cash_equiv_quarter1 = ((sum(cash_equiv_quarter1_unpacked) / len(cash_equiv_quarter1_unpacked)) / 1000000000)
                         Total_cash_last_years = (st_investments_quarter1+cash_equiv_quarter1)

                         #print("Total_cash_last_years",Total_cash_last_years)
                    
                    

                         
                         try:

                              Buyback_yield = ((shares_basic_annual_funf_unpacked[-2]-shares_basic_annual_funf_unpacked[-1])/abs(shares_basic_annual_funf_unpacked[-2]))*100
                    
                              if shares_basic_annual_funf_unpacked[-2] ==0:
                                   
                                   Buyback_yield=0

                         except (IndexError, ZeroDivisionError): 
                              Buyback_yield=0   

                         Share_holder_yield="{:.2f}%".format(Dividend_per_share_yield_no_percentage+Buyback_yield)
                         
                         
                    
                         try:
                              ROE_ttm_ohne = (ROE_TTM)
                              ROE_ttm="{:.2f}%".format(ROE_ttm_ohne)
                              fcf_yield_ttm = "{:.2f}%".format((fcf_per_share/amount)*100)
                              ROIC_TTM="{:.2f}".format(ROIC_TTM)
                              ROA_TTM =ROA_TTM
                         except Exception as e: 
                              ROE_ttm  ="{:.2f}%".format(0.00)
                              fcf_yield_ttm ="{:.2f}%".format(0.00)
                              ROIC_TTM = ROIC_annual_one
                              ROA_TTM =average_ROA_annual_ttm

          #######################################################################################################################
                         #print("ROE_TTM",ROE_TTM)

          #####################################################################################################
                         def calculate_total_debt(ticker, date_quarter, 
                                                  Accounts_payable_quarter10_unpacked, Current_accrued_liab_quarter10_unpacked, 
                                                  Tax_payable_quarter10_unpacked, Other_current_liabilities_quarter10_unpacked, 
                                                  Current_deferred_revenue_quarter10_unpacked, Total_current_liabilities_quarter10_unpacked, 
                                                  capital_leases_quarter10_unpacked, current_portion_of_lease_obligation_quarter10_unpacked, LongTerm_debt_quarter10_unpacked):
                              # Check if the result is already in session state
                              if f'{ticker}_Total_Debt' in st.session_state:
                                   return st.session_state[f'{ticker}_Total_Debt']

                              # Create DataFrame
                              index = range(len(date_quarter))
                              df = pd.DataFrame({
                                   'period_end_date': date_quarter,
                                   'accounts_payable': Accounts_payable_quarter10_unpacked,
                                   'current_accrued_liabilities': Current_accrued_liab_quarter10_unpacked,
                                   'tax_payable': Tax_payable_quarter10_unpacked,
                                   'other_current_liabilities': Other_current_liabilities_quarter10_unpacked,
                                   'current_deferred_revenue': Current_deferred_revenue_quarter10_unpacked,
                                   'total_current_liabilities': Total_current_liabilities_quarter10_unpacked,
                                   'noncurrent_capital_leases': capital_leases_quarter10_unpacked,
                              # 'current_capital_leases': current_portion_of_lease_obligation_quarter10_unpacked,
                                   'lt_debt': LongTerm_debt_quarter10_unpacked
                              }, index=index)

                              # Perform calculations
                              df['Total Difference'] = df['total_current_liabilities'] - (
                                   df['accounts_payable'] + df['current_accrued_liabilities'] + df['tax_payable'] +
                                   df['other_current_liabilities'] + df['current_deferred_revenue']
                              )

                              df['Total add'] = df['noncurrent_capital_leases'] + df['lt_debt']
                              df['Total Debt'] = df['Total Difference'] + df['Total add']

                              # Transpose and format the DataFrame
                              total = df.T
                              total.columns = total.iloc[0]  # Use the first row as column names
                              total = total[1:]
                              #total = total.applymap(lambda x: "{:,.0f}".format(x / 1000000))
                              total = total.apply(lambda x: x.map(lambda val: "{:,.0f}".format(val / 1000000) if isinstance(val, (int, float)) else val))


                              total_debt_column = df['Total Debt']
                              last_value_total_debt = total_debt_column.iloc[-1]

                              # Store the result in session state
                              st.session_state[f'{ticker}_Total_Debt'] = last_value_total_debt

                              return last_value_total_debt

                         # Call the function to calculate total debt and store it in session state
                         Total_Debt_from_all_calc = calculate_total_debt(
                         ticker, date_quarter, Accounts_payable_quarter10_unpacked, Current_accrued_liab_quarter10_unpacked, 
                         Tax_payable_quarter10_unpacked, Other_current_liabilities_quarter10_unpacked, 
                         Current_deferred_revenue_quarter10_unpacked, Total_current_liabilities_quarter10_unpacked, 
                         capital_leases_quarter10_unpacked, current_portion_of_lease_obligation_quarter10_unpacked, LongTerm_debt_quarter10_unpacked
                         )
          #####################################################################################################


                         def calculate_financial_metrics(ticker, Marketcap, Total_Debt_from_all_calc, Total_cash_last_years, 
                                                            Ebita_ttm, revenue_ttm, Dividend_ttm, netincome_ttm, 
                                                            fcf_ttm, current_Operating_cash_Flow):
                              # Check if financial metrics are already in session state
                              if f'{ticker}_Enterprise_value' in st.session_state:
                                   return (
                                        st.session_state[f'{ticker}_Enterprise_value'],
                                        st.session_state[f'{ticker}_Enterprise_value_in_Billion'],
                                        st.session_state[f'{ticker}_Debt_to_EBITDA'],
                                        st.session_state[f'{ticker}_Ebita_ttm_Billion'],
                                        st.session_state[f'{ticker}_revenue_ttm'],
                                        st.session_state[f'{ticker}_Dividend_ttm'],
                                        st.session_state[f'{ticker}_netincome_ttm'],
                                        st.session_state[f'{ticker}_fcf_ttm'],
                                        st.session_state[f'{ticker}_current_Operating_cash_Flow_Value'],
                                        st.session_state[f'{ticker}_P_OCF_ttm']
                                   )

                              try:
                                   # Calculate Enterprise value
                                   Enterprise_value = ((Marketcap) + (Total_Debt_from_all_calc/1000000000) - Total_cash_last_years)
                                   Enterprise_value_in_Billion = "{:.2f}T".format(Enterprise_value / 1000) if abs(Enterprise_value) >= 1000 else "{:,.2f}B".format(Enterprise_value)
                                   Debt_to_EBITDA = "{:.2f}".format((Total_Debt_from_all_calc / 1000000000) / Ebita_ttm)
                                   Ebita_ttm_Billion = "{:.2f}T".format(Ebita_ttm / 1000) if abs(Ebita_ttm) >= 1000 else "{:,.2f}B".format(Ebita_ttm)

                              except Exception as e:
                                   Enterprise_value = "N/A"
                                   Enterprise_value_in_Billion = "N/A"
                                   Debt_to_EBITDA = "{:.2f}".format(0.00)
                                   Ebita_ttm_Billion = "{:.2f}".format(0.00)

                              revenue_ttm *= 1000000000
                              if revenue_ttm != 0.00 or Dividend_ttm > 0:
                                   Dividend_ttm = "{:.2f}B".format(abs(Dividend_ttm / 1000000000)) if abs(Dividend_ttm) >= 1000000000 else "{:,.1f}M".format(abs(Dividend_ttm / 1000000))
                                   revenue_ttm = "{:.2f}B".format(revenue_ttm / 1000000000) if abs(revenue_ttm) >= 1000000000 else "{:,.1f}M".format(revenue_ttm / 1000000)
                              else:
                                   revenue_ttm = "-"
                                   Dividend_ttm = "-"

                              # Formatting net income, free cash flow, and operating cash flow values
                              netincome_ttm *= 1000000000
                              netincome_ttm = "{:.2f}B".format(netincome_ttm / 1000000000) if abs(netincome_ttm) >= 1000000000 else "{:,.1f}M".format(netincome_ttm / 1000000)

                              fcf_ttm *= 1000000000
                              fcf_ttm = "{:.2f}B".format(fcf_ttm / 1000000000) if abs(fcf_ttm) >= 1000000000 else "{:,.1f}M".format(fcf_ttm / 1000000)

                              current_Operating_cash_Flow_Value = "{:.2f}B".format(current_Operating_cash_Flow / 1000000000) if abs(current_Operating_cash_Flow) >= 1000000000 else "{:,.1f}M".format(current_Operating_cash_Flow / 1000000)

                              if current_Operating_cash_Flow != 0:
                                   P_OCF_ttm = "{:.2f}".format(Marketcap / (current_Operating_cash_Flow / 1000000000))
                              else:
                                   P_OCF_ttm = "-"

                              # Store calculated values in session_state
                              st.session_state[f'{ticker}_Enterprise_value'] = Enterprise_value
                              st.session_state[f'{ticker}_Enterprise_value_in_Billion'] = Enterprise_value_in_Billion
                              st.session_state[f'{ticker}_Debt_to_EBITDA'] = Debt_to_EBITDA
                              st.session_state[f'{ticker}_Ebita_ttm_Billion'] = Ebita_ttm_Billion
                              st.session_state[f'{ticker}_revenue_ttm'] = revenue_ttm
                              st.session_state[f'{ticker}_Dividend_ttm'] = Dividend_ttm
                              st.session_state[f'{ticker}_netincome_ttm'] = netincome_ttm
                              st.session_state[f'{ticker}_fcf_ttm'] = fcf_ttm
                              st.session_state[f'{ticker}_current_Operating_cash_Flow_Value'] = current_Operating_cash_Flow_Value
                              st.session_state[f'{ticker}_P_OCF_ttm'] = P_OCF_ttm

                              return (
                                   Enterprise_value,
                                   Enterprise_value_in_Billion,
                                   Debt_to_EBITDA,
                                   Ebita_ttm_Billion,
                                   revenue_ttm,
                                   Dividend_ttm,
                                   netincome_ttm,
                                   fcf_ttm,
                                   current_Operating_cash_Flow_Value,
                                   P_OCF_ttm
                              )

                         (Enterprise_value,
                                   Enterprise_value_in_Billion,
                                   Debt_to_EBITDA,
                                   Ebita_ttm_Billion,
                                   revenue_ttm,
                                   Dividend_ttm,
                                   netincome_ttm,
                                   fcf_ttm,
                                   current_Operating_cash_Flow_Value,
                                   P_OCF_ttm)=calculate_financial_metrics(ticker, Marketcap, Total_Debt_from_all_calc, Total_cash_last_years, 
                                                            Ebita_ttm,revenue_ttm, Dividend_ttm, netincome_ttm, 
                                                            fcf_ttm, current_Operating_cash_Flow)

          ############################################################################



          #################################################################################

                         def create_dataframe(data):
                               df = pd.DataFrame(data).transpose()
                               df = df.rename(columns={i: " " for i in df.columns})  # Remove column headers
                               return df

                         # def style_dataframe(df):
                         #      def highlight_negative(val):
                         #           """Apply color styles based on the value."""
                         #           if isinstance(val, (int, float)) and val < 0:
                         #                return 'color: green'
                         #           return ''  
                         #      # Default styling (no additional styling)
                         #      styled_df = df.style.applymap(highlight_negative) \
                         #           .set_table_styles(

                         #           [
                         #                {'selector': 'th.col0',  # Apply to the first column header
                         #                'props': [('background-color', 'white'),  # Green background for the first header
                         #                          ('color', 'white'),# White text color for the first header
                         #                          ('text-align', 'left')]},  # Centered text
                         #                {'selector': 'th:not(.col0)',  # Apply to other headers
                         #                'props': [('color', '#2E8B57'), 
                         #                          # Green text color for other headers
                         #                          ('text-align', 'left')]},  # Centered text for other headers
                         #           ],
                         #           overwrite=False
                         #      ).hide(axis='index')#.set_caption("")
                              
                         #      return styled_df
                         

                         # def create_dataframe(data):
                         #      """Erstellt ein DataFrame und entfernt Spaltenüberschriften."""
                         #      df = pd.DataFrame(data).transpose()
                         #      df = df.rename(columns={i: " " for i in df.columns})  # Entfernt Spaltenüberschriften
                         #      return df
#--------------------------------------------------------------
                         def style_dataframe(df):
                              """Stylt das DataFrame mit Farben für negative Werte und Kopfzeilenanpassungen."""
                              
                              def highlight_negative(val):
                                   """Färbt negative Werte grün."""
                                   if isinstance(val, (int, float)) and val < 0:
                                        return 'color: green'
                                   return ''  

                              # Wendet das Styling an
                              styled_df = df.style.map(lambda x: highlight_negative(x)) \
                                   .set_table_styles([
                                        {'selector': 'th.col0',  # Erste Spaltenüberschrift (Index-Spalte)
                                        'props': [('background-color', 'white'), 
                                                  ('color', 'white'),
                                                  ('text-align', 'left')]},
                                        {'selector': 'th:not(.col0)',  # Andere Spaltenüberschriften
                                        'props': [('color', '#2E8B57'), 
                                                  ('text-align', 'left')]},
                                   ], overwrite=False).hide(axis='index')  # Index ausblenden
                              
                              return styled_df


          #################################################################################



 

                         def display_dataframes(dfs, cols):
                              for df, col in zip(dfs, cols):
                                   with col:
                                        st.table(df)
                      
                                                  # Data for the tables
                         data1 = {
                         'Market Cap (intraday)': [Marketcap_in_Billion],
                         'Enterprise Value': [Enterprise_value_in_Billion],
                         'EBITDA (TTM)': [Ebita_ttm_Billion], 
                         'Debt/EBITDA': [Debt_to_EBITDA],
                         'Revenue (TTM)': [revenue_ttm],      
                         '5 YR Net Income': [Average_net_income_annual_funf_Billion_Million], 
                         'Net Income (TTM)': [netincome_ttm], 
                         'PEG': [PEG],
                         'Forward P/E': [forwardPE], 
                         'P/E (TTM)': [pe_ttm],
                         '5 YR P/E': [pe_five_],
                         '10 YR P/E': [average_PE_historical],
                         'Operating Cashflow (TTM)': [current_Operating_cash_Flow_Value], 
                         'Price/OCF (TTM)': [P_OCF_ttm],  
                         '5 YR Price/OCF ': [P_OCF_5],  
                         '10 YR Price/OCF': [P_OCF_10],  
                         '5 YR Gross Profit Margin': [five_yrs_average_gross_margin],
                         'Gross Profit Margin (TTM)': [average_gross_margin_quater1],
                         }


                         data2 = {
                         '5 YR Dividend Yield': [Dividend_yield_average], 
                         'Dividend Yield': [Dividend_per_share_yield],
                         'Shareholder Yield': [Share_holder_yield],
                         'Dividend Paid (TTM)': [Dividend_ttm], 
                         'Dividend/Share (TTM)': f"{Dividend_TTM}",
                         'Dividend Estimate': f" {Dividend_Est}",
                         'Dividend Ex-Date': [Dividend_Ex_Date],
                         '5 YR Avg FCF': [average_FCF_annual_five_we], 
                         'Free Cash Flow (TTM)': [fcf_ttm],
                         'Price/FCF (TTM)': [pfcf_ttm], 
                         '5 YR Avg Price/FCF': [pfcf_funf],
                         '10 YR Avg Price/FCF': [pfcf_ten],
                         '5 YR Operating Margin': [five_yrs_average_operating_margin],
                         'Operating Margin': [average_operating_margin1_quarter],
                         '5 YR Net Profit Margin': f"{five_yrs_Nettomarge}%",
                         'Net Profit Margin': [Net_margin_ttm],
                         #'5 YR FCF Margin':[FCF_Margin_5],
                         '5 YR FCF Margin': f"{FCF_Margin_5}%",
                         'FCF Margin': ' {:.2f}%'.format(FCF_Margin_1)
                         }

                         data3 = {
                         'FCF Yield': [fcf_yield_ttm],
                         'P/S': [Price_to_sales_last],
                         '5 YR P/S': [P_sales_5],
                         '10 YR P/S': [P_sales_10],
                         'P/B': '{:.2f}'.format(PBVPS),
                         '5 YR P/B': [average_price_to_book_annual_5],
                         '10 YR P/B':[average_price_to_book],
                         'ROA': ["{:.5}%".format(ROA_TTM)],
                         '5 YR ROE': ["{:.5}%".format(five_ROE)],
                         'ROE': [ROE_ttm],
                         '5 YR ROIC': [Average_ROIC_funf],
                         'ROIC': ["{:.5}%".format(ROIC_TTM)],
                         '5 YR ROCE': [ "{:.2f}%".format(five_yrs_ROCE)],
                         'ROCE': [ "{:.2f}%".format(One_YR_ROCE)],
                         f'ATH ({format_date(st.session_state.all_time_high_date)})': f"$ {st.session_state.all_time_high_price:.2f}",
                         f'52WK LOW ({format_date(st.session_state.fifty_two_week_low_date)})': f"$ {st.session_state.fifty_two_week_low:.2f}",
                         'Analyst Target Price': [f"$ {Target_Price}"],
                         'Current price': ["$ {:.2f}".format(amount)] 
                         }
          

                         data4 = {
                         'EPS (TTM)': " {:.2f}".format(eps_diluted_ttm),
                         'EPS Estimate this YR': f"{Earnings_this_yr}",
                         'EPS Estimate next YR': f" {Earnings_next_yr_in_value} ({Earnings_next_yr_in_prozent})",
                         'EPS Estimate 5 YR (per annum)': [Earnings_next_5_yrs],
                         'EPS CAGR 10 YR': f"{EPS_Cagr_10}%",
                         'EPS CAGR 5 YR': f"{EPS_5_CAGR}% ",
                         'Revenue CAGR 10 YR': f"{Revenue_Cagr_10}%",
                         'Revenue CAGR 5 YR': f"{Revenue_5_CAGR}%",
                         'FCF CAGR 10 YR': f"{FCF_Cagr_10}%",
                         'FCF CAGR 5 YR': f"{FCF_5_CAGR}%",
                         'Net Interest Income CAGR 10 YR': f"{Net_interest_Income_annual_Cagr_10 }%",
                         'Net Interest Income CAGR 5 YR': f"{Net_interest_Income_annual_Cagr_5 }%",
                         'RSI (14)': [RSI],
                         '50 SMA': [Moving_50],
                         '200 SMA': [Moving_200]
                         
                         }

                         # # Convert data into styled DataFrames
                         # df1 = style_dataframe(create_dataframe(data1).iloc[0:])
                         # df2 = style_dataframe(create_dataframe(data2).iloc[0:])
                         # df3 = style_dataframe(create_dataframe(data3).iloc[0:])
                         # df4 = style_dataframe(create_dataframe(data4).iloc[0:])


                         # # Create a responsive layout with four columns
                         # col1, col2, col3, col4 = st.columns(4)

                         # Display the dataframes in each column
                         #display_dataframes([df1, df2, df3, df4], [col1, col2, col3, col4])  

                         # 🖥 **Daten in DataFrames umwandeln & stylen**
                         df1 = style_dataframe(create_dataframe(data1))
                         df2 = style_dataframe(create_dataframe(data2))
                         df3 = style_dataframe(create_dataframe(data3))
                         df4 = style_dataframe(create_dataframe(data4))

                         # 📌 **Streamlit Layout mit vier Spalten**
                         col1, col2, col3, col4 = st.columns(4)

                         # 🔥 **Daten in den Spalten anzeigen**
                         display_dataframes([df1, df2, df3, df4], [col1, col2, col3, col4])   



          #################################################################################


                    #----------------------------------------------------------------------------
                         # Display the first 20 characters of the description
                         short_description = Stock_description[:20]

                         st.markdown(f"About <u style='color:green;'>{name}</u>", unsafe_allow_html=True)


                         st.write(Stock_description)

                         st.markdown('<div class="my-header">Found an error or have an idea? Write us an Email!</div>', unsafe_allow_html=True)
                         
                    # ---- Documentation : https://formsubmit.co/
                         contact_form = """
                              <form action="https://formsubmit.co/verstehdieaktie@gmail.com" method="POST">
                                   <input type = "hidden" name="_captcha" value="false">
                                   <input type="text" name="name" placeholder="Your name" required>
                                   <input type="email" name="email" placeholder="Your email" required>
                                   <input type="country" name="country" placeholder="Your country" required>
                                   <textarea name ="message" placeholder="Your message here" required></textarea>
                                   <button type="submit">Send</button>
                              </form>
                              """

                              
                         st.markdown(contact_form, unsafe_allow_html = True)
          #################################################################################
               
                         @st.cache_data(show_spinner=False,ttl=3600)
                         def local_css(file_name):
                                   with open(file_name)as f:
                                        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)      
                         local_css("style.css")
          #################################################################################
               def unpack_financial_data(annual_data, ticker):
               # Define session state keys based on ticker
                    session_keys = {
                         'Total_interest_income_annual_10': f'{ticker}_Total_interest_income_annual_10',
                         'Total_interest_expense_annual_10': f'{ticker}_Total_interest_expense_annual_10',
                         'Net_interest_Income_annual_10': f'{ticker}_Net_interest_Income_annual_10',
                         'Prov_Credit_losses_annual_10': f'{ticker}_Prov_Credit_losses_annual_10',
                         'Netinterest_Prov_Credit_losses_annual_10': f'{ticker}_Netinterest_Prov_Credit_losses_annual_10',
                         'Total_Non_interest_expenses_annual_10': f'{ticker}_Total_Non_interest_expenses_annual_10',
                         'Total_Non_interest_revenue_annual_10': f'{ticker}_Total_Non_interest_revenue_annual_10',
                         'Net_premiums_earned_annual_10': f'{ticker}_Net_premiums_earned_annual_10',
                         'Net_investment_income_annual_10': f'{ticker}_Net_investment_income_annual_10',
                         'Fees_and_other_income_annual_10': f'{ticker}_Fees_and_other_income_annual_10',
                         'Interest_Expense_insurance_annual_10': f'{ticker}_Interest_Expense_insurance_annual_10',
                         'Policy_benefits_claim_annual_10': f'{ticker}_Policy_benefits_claim_annual_10',
                         'Operating_income_annual_10': f'{ticker}_Operating_income_annual_10',
                         'cogs_list_annual_10': f'{ticker}_cogs_list_annual_10',
                         'gross_profit_annual_10': f'{ticker}_gross_profit_annual_10',
                         'SGA_Expense_annual_10': f'{ticker}_SGA_Expense_annual_10',
                         'Depreciation_Depletion_Amortisation_annual_10': f'{ticker}_Depreciation_Depletion_Amortisation_annual_10',
                         'Interest_Income_annual_10': f'{ticker}_Interest_Income_annual_10',
                         'Research_Dev_annual_10': f'{ticker}_Research_Dev_annual_10',
                         'interest_expense_list_annual_10': f'{ticker}_interest_expense_list_annual_10',
                         'operating_income_list_annual_10': f'{ticker}_operating_income_list_annual_10'
                    }

                    # Check if all data is in session state
                    if all(key in st.session_state for key in session_keys.values()):
                         return tuple(st.session_state[key] for key in session_keys.values())

                    # Unpack the data if not present in session state
                    try:
                         Total_interest_income_annual_10_unpacked = annual_data['total_interest_income'][-10:]
                         Total_interest_expense_annual_10_unpacked = annual_data['total_interest_expense'][-10:]
                         #Net_interest_Income_annual_10_unpacked = annual_data['net_interest_income'][-10:]
                         Prov_Credit_losses_annual_10_unpacked = annual_data['credit_losses_provision'][-10:]
                         Netinterest_Prov_Credit_losses_annual_10_unpacked = annual_data['net_interest_income_after_credit_losses_provision'][-10:]
                         Total_Non_interest_expenses_annual_10_unpacked = annual_data['total_noninterest_expense'][-10:]
                         Total_Non_interest_revenue_annual_10_unpacked = annual_data['total_noninterest_revenue'][-10:]

                         # Store unpacked data in session state
                         st.session_state.update({
                              session_keys['Total_interest_income_annual_10']: Total_interest_income_annual_10_unpacked,
                              session_keys['Total_interest_expense_annual_10']: Total_interest_expense_annual_10_unpacked,
                              session_keys['Net_interest_Income_annual_10']: Net_interest_Income_annual_10_unpacked,
                              session_keys['Prov_Credit_losses_annual_10']: Prov_Credit_losses_annual_10_unpacked,
                              session_keys['Netinterest_Prov_Credit_losses_annual_10']: Netinterest_Prov_Credit_losses_annual_10_unpacked,
                              session_keys['Total_Non_interest_expenses_annual_10']: Total_Non_interest_expenses_annual_10_unpacked,
                              session_keys['Total_Non_interest_revenue_annual_10']: Total_Non_interest_revenue_annual_10_unpacked
                         })

                         return (
                              Total_interest_income_annual_10_unpacked,
                              Total_interest_expense_annual_10_unpacked,
                              Net_interest_Income_annual_10_unpacked,
                              Prov_Credit_losses_annual_10_unpacked,
                              Netinterest_Prov_Credit_losses_annual_10_unpacked,
                              Total_Non_interest_expenses_annual_10_unpacked,
                              Total_Non_interest_revenue_annual_10_unpacked
                         )

                    except KeyError:
                         try:
                              Net_premiums_earned_annual_10_unpacked = annual_data['premiums_earned'][-10:]
                              Net_investment_income_annual_10_unpacked = annual_data['net_investment_income'][-10:]
                              Fees_and_other_income_annual_10_unpacked = annual_data['fees_and_other_income'][-10:]
                              Interest_Expense_insurance_annual_10_unpacked = annual_data['interest_expense_insurance'][-10:]
                              Policy_benefits_claim_annual_10_unpacked = annual_data['net_policyholder_claims_expense'][-10:]
                              Operating_income_annual_10_unpacked = annual_data['operating_income'][-10:]

                              # Store unpacked data in session state
                              st.session_state.update({
                                   session_keys['Net_premiums_earned_annual_10']: Net_premiums_earned_annual_10_unpacked,
                                   session_keys['Net_investment_income_annual_10']: Net_investment_income_annual_10_unpacked,
                                   session_keys['Fees_and_other_income_annual_10']: Fees_and_other_income_annual_10_unpacked,
                                   session_keys['Interest_Expense_insurance_annual_10']: Interest_Expense_insurance_annual_10_unpacked,
                                   session_keys['Policy_benefits_claim_annual_10']: Policy_benefits_claim_annual_10_unpacked,
                                   session_keys['Operating_income_annual_10']: Operating_income_annual_10_unpacked
                              })

                              return (
                                   Net_premiums_earned_annual_10_unpacked,
                                   Net_investment_income_annual_10_unpacked,
                                   Fees_and_other_income_annual_10_unpacked,
                                   Interest_Expense_insurance_annual_10_unpacked,
                                   Policy_benefits_claim_annual_10_unpacked,
                                   Operating_income_annual_10_unpacked
                              )

                         except KeyError:
                              try:
                                   cogs_list_annual_10_unpacked = annual_data['cogs'][-10:]
                                   gross_profit_annual_10_unpacked = annual_data['gross_profit'][-10:]
                                   SGA_Expense_annual_10_unpacked = annual_data['total_opex'][-10:]
                                   Research_Dev_annual_10_unpacked = annual_data['rnd'][-10:]
                                   interest_expense_list_annual_10_unpacked = annual_data['interest_expense'][-10:]
                                   operating_income_list_annual_10_unpacked = annual_data['operating_income'][-10:]


                                   try:
                                        Depreciation_Depletion_Amortisation_annual_10_unpacked = annual_data['cfo_da'][-10:]
                                        Interest_Income_annual_10_unpacked = annual_data['interest_income'][-10:]
                                   except KeyError:
                                        Depreciation_Depletion_Amortisation_annual_10_unpacked = [0] * len_10_annual
                                        Interest_Income_annual_10_unpacked = [0] * len_10_annual


                                   # Store unpacked data in session state
                                   st.session_state.update({
                                        session_keys['cogs_list_annual_10']: cogs_list_annual_10_unpacked,
                                        session_keys['gross_profit_annual_10']: gross_profit_annual_10_unpacked,
                                        session_keys['SGA_Expense_annual_10']: SGA_Expense_annual_10_unpacked,
                                        session_keys['Research_Dev_annual_10']: Research_Dev_annual_10_unpacked,
                                        session_keys['interest_expense_list_annual_10']: interest_expense_list_annual_10_unpacked,
                                        session_keys['operating_income_list_annual_10']: operating_income_list_annual_10_unpacked,
                                        session_keys['Depreciation_Depletion_Amortisation_annual_10']: Depreciation_Depletion_Amortisation_annual_10_unpacked,
                                        session_keys['Interest_Income_annual_10']: Interest_Income_annual_10_unpacked
                                   
                                   })

                                   return (
                                        cogs_list_annual_10_unpacked,
                                        gross_profit_annual_10_unpacked,
                                        SGA_Expense_annual_10_unpacked,
                                        Research_Dev_annual_10_unpacked,
                                        interest_expense_list_annual_10_unpacked,
                                        operating_income_list_annual_10_unpacked,
                                        Depreciation_Depletion_Amortisation_annual_10_unpacked,
                                        Interest_Income_annual_10_unpacked
                                   
                                   )

                              except KeyError:
                                   st.write("Data not available.")
                                   return ()


          #################################################################################

               #@st.cache_data(show_spinner=False)
               def financials_df(data_list, date_list, column_name):

                    formatted_data = [
                    "{:.2f}B".format(value / 1000000000) if abs(value) >= 1000000000 else
                    "{:.1f}M".format(value / 1000000) if abs(value) >= 1000000 else
                    "{:.0f}K".format(value / 1000) if abs(value) >= 1000 else
                    "{:.2f}".format(value)
                    for value in data_list
                    ]
                              
                    df = pd.DataFrame(formatted_data, index=date_list, columns=[column_name])
                    return df.transpose()   
               # Define session state keys based on ticker


               
               with st.container():
                    use_container_width=True
                    with Financials:
                         Income_Statement, Balance_Sheet, Cash_Flow = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])
               #...........................................................................
                         with Income_Statement:
                              Annual,Quarterly = st.tabs(["Annual","Quarterly"])
                              date_annual = annual_data['period_end_date'][-10:]
                              date_quarter = quarterly_data['period_end_date'][-10:]


                              with Annual: 
                                   try:

                                        if f'{ticker}_Total_interest_income_annual_10' in st.session_state:
                                             Total_interest_income_annual_10_unpacked = st.session_state[f'{ticker}_Total_interest_income_annual_10']
                                             Pretax_income_annual_10_unpacked = st.session_state[f'{ticker}_Pretax_income_annual_10']
                                             Income_tax_annual_10_unpacked = st.session_state[f'{ticker}_Income_tax_annual_10']
                                             Total_interest_expense_annual_10_unpacked = st.session_state[f'{ticker}_Total_interest_expense_annual_10']
                                             Net_interest_Income_annual_10_unpacked = st.session_state[f'{ticker}_Net_interest_Income_annual_10']
                                             Prov_Credit_losses_annual_10_unpacked = st.session_state[f'{ticker}_Prov_Credit_losses_annual_10']
                                             Netinterest_Prov_Credit_losses_annual_10_unpacked = st.session_state[f'{ticker}_Netinterest_Prov_Credit_losses_annual_10']
                                             Total_Non_interest_expenses_annual_10_unpacked = st.session_state[f'{ticker}_Total_Non_interest_expenses_annual_10']
                                             Total_Non_interest_revenue_annual_10_unpacked = st.session_state[f'{ticker}_Total_Non_interest_revenue_annual_10']
                                             Ebita_annual_10_unpacked = st.session_state[f'{ticker}_Ebita_annual_10']
                                             
                                                  ################################ Quarter###############################
                                             Total_interest_income_list_quarterly_10_unpacked = st.session_state[f'{ticker}_Total_interest_income_list_quarterly_10']
                                             Pretax_income_quarterly_10_unpacked = st.session_state[f'{ticker}_Pretax_income_quarterly_10']
                                             Income_tax_quarterly_10_unpacked = st.session_state[f'{ticker}_Income_tax_quarterly_10']
                                             net_income_quarterly_10_unpacked = st.session_state[f'{ticker}_net_income_quarterly_10']
                                             Total_interest_expense_list_quarterly_10_unpacked = st.session_state[f'{ticker}_Total_interest_expense_list_quarterly_10']
                                             Net_interest_Income_quarterly_10_unpacked = st.session_state[f'{ticker}_Net_interest_Income_quarterly_10']
                                             Prov_Credit_losses_quarterly_10_unpacked = st.session_state[f'{ticker}_Prov_Credit_losses_quarterly_10']
                                             Netinterest_Prov_Credit_losses_quarterly_10_unpacked = st.session_state[f'{ticker}_Netinterest_Prov_Credit_losses_quarterly_10']
                                             Total_Non_interest_expenses_quarterly_10_unpacked = st.session_state[f'{ticker}_Total_Non_interest_expenses_quarterly_10']
                                             Total_Non_interest_revenue_quarterly_10_unpacked = st.session_state[f'{ticker}_Total_Non_interest_revenue_quarterly_10']
                                             Ebita_quarter_10_unpacked = st.session_state[f'{ticker}_Ebita_quarter_10']
                                        else:
                                        
                                             Pretax_income_annual_10_unpacked = annual_data['pretax_income'][-10:]
                                             Income_tax_annual_10_unpacked  = annual_data['income_tax'][-10:]
                                             Total_interest_income_annual_10_unpacked = annual_data['total_interest_income'][-10:]
                                             Total_interest_expense_annual_10_unpacked = annual_data['total_interest_expense'][-10:]
                                             #Net_interest_Income_annual_10_unpacked  = annual_data['net_interest_income'][-10:]
                                             Prov_Credit_losses_annual_10_unpacked  = annual_data['credit_losses_provision'][-10:]
                                             Netinterest_Prov_Credit_losses_annual_10_unpacked = annual_data['net_interest_income_after_credit_losses_provision'][-10:]
                                             Total_Non_interest_expenses_annual_10_unpacked  = annual_data['total_noninterest_expense'][-10:]
                                             Total_Non_interest_revenue_annual_10_unpacked  = annual_data['total_noninterest_revenue'][-10:]
                                             Ebita_annual_10_unpacked = annual_data['ebitda'][-10:]

                                                       ################################ Quarter###############################

                                             Pretax_income_quarterly_10_unpacked  = quarterly_data['pretax_income'][-10:]
                                             Income_tax_quarterly_10_unpacked  = quarterly_data['income_tax'][-10:]
                                             net_income_quarterly_10_unpacked  = quarterly_data['net_income'][-10:]
                                             Total_interest_income_list_quarterly_10_unpacked  = quarterly_data['total_interest_income'][-10:]
                                             Total_interest_expense_list_quarterly_10_unpacked  = quarterly_data['total_interest_expense'][-10:]
                                             Net_interest_Income_quarterly_10_unpacked  = quarterly_data['net_interest_income'][-10:]
                                             Prov_Credit_losses_quarterly_10_unpacked = quarterly_data['credit_losses_provision'][-10:]
                                             Netinterest_Prov_Credit_losses_quarterly_10_unpacked = quarterly_data['net_interest_income_after_credit_losses_provision'][-10:]
                                             Total_Non_interest_expenses_quarterly_10_unpacked = quarterly_data['total_noninterest_expense'][-10:]
                                             Total_Non_interest_revenue_quarterly_10_unpacked = quarterly_data['total_noninterest_revenue'][-10:]
                                             Ebita_quarter_10_unpacked = quarterly_data['ebitda'][-10:]



                                             # Store unpacked data in session state
                                             st.session_state[f'{ticker}_Pretax_income_annual_10'] = Pretax_income_annual_10_unpacked
                                             st.session_state[f'{ticker}_Income_tax_annual_10'] = Income_tax_annual_10_unpacked
                                             st.session_state[f'{ticker}_Total_interest_income_annual_10'] = Total_interest_income_annual_10_unpacked
                                             st.session_state[f'{ticker}_Total_interest_expense_annual_10'] = Total_interest_expense_annual_10_unpacked
                                             st.session_state[f'{ticker}_Net_interest_Income_annual_10'] = Net_interest_Income_annual_10_unpacked
                                             st.session_state[f'{ticker}_Prov_Credit_losses_annual_10'] = Prov_Credit_losses_annual_10_unpacked
                                             st.session_state[f'{ticker}_Netinterest_Prov_Credit_losses_annual_10'] = Netinterest_Prov_Credit_losses_annual_10_unpacked
                                             st.session_state[f'{ticker}_Total_Non_interest_expenses_annual_10'] = Total_Non_interest_expenses_annual_10_unpacked
                                             st.session_state[f'{ticker}_Total_Non_interest_revenue_annual_10'] = Total_Non_interest_revenue_annual_10_unpacked
                                             st.session_state[f'{ticker}_Ebita_annual_10'] = Ebita_annual_10_unpacked


                                                       ################################ Quarter###############################

                                                  # Store unpacked data in session state
                                             st.session_state[f'{ticker}_Pretax_income_quarterly_10'] = Pretax_income_quarterly_10_unpacked
                                             st.session_state[f'{ticker}_Income_tax_quarterly_10'] = Income_tax_quarterly_10_unpacked
                                             st.session_state[f'{ticker}_net_income_quarterly_10'] = net_income_quarterly_10_unpacked
                                             st.session_state[f'{ticker}_Total_interest_income_list_quarterly_10'] = Total_interest_income_list_quarterly_10_unpacked
                                             st.session_state[f'{ticker}_Total_interest_expense_list_quarterly_10'] = Total_interest_expense_list_quarterly_10_unpacked
                                             st.session_state[f'{ticker}_Net_interest_Income_quarterly_10'] = Net_interest_Income_quarterly_10_unpacked
                                             st.session_state[f'{ticker}_Prov_Credit_losses_quarterly_10'] = Prov_Credit_losses_quarterly_10_unpacked
                                             st.session_state[f'{ticker}_Netinterest_Prov_Credit_losses_quarterly_10'] = Netinterest_Prov_Credit_losses_quarterly_10_unpacked
                                             st.session_state[f'{ticker}_Total_Non_interest_expenses_quarterly_10'] = Total_Non_interest_expenses_quarterly_10_unpacked
                                             st.session_state[f'{ticker}_Total_Non_interest_revenue_quarterly_10'] = Total_Non_interest_revenue_quarterly_10_unpacked
                                             st.session_state[f'{ticker}_Ebita_quarter_10'] = Ebita_quarter_10_unpacked


                                             #      # Store unpacked data in session state
                                   

                                        revenue_2013_annual_df = financials_df(Revenue_annual_10_unpacked, date_annual, "Revenue")
                                        Pretax_income_annual_df = financials_df(Pretax_income_annual_10_unpacked, date_annual, "Pretax Income")
                                        eps_basic_annual_df = financials_df(eps_basic_annual_10_unpacked, date_annual, "EPS Basic")
                                        shares_basic_annual_df = financials_df(shares_basic_annual_10_unpacked, date_annual, "Shares Basic")
                                        eps_diluted_annual_df = financials_df(eps_diluted_annual_10_unpacked, date_annual, "EPS Diluted")
                                        shares_diluted_annual_df = financials_df(shares_diluted_annual_10_unpacked, date_annual, "Shares Diluted")
                                        Income_tax_annual_df = financials_df(Income_tax_annual_10_unpacked, date_annual, "Income Tax Expense")
                                        net_income_annual_df = financials_df(net_income_annual_10_unpacked, date_annual, "Net Income")
                                        Total_interest_income_list_annual_df = financials_df(Total_interest_income_annual_10_unpacked, date_annual, "Total Interest Income")
                                        Total_interest_expense_list_annual_df = financials_df(Total_interest_expense_annual_10_unpacked, date_annual, "Total Interest Expense")
                                        Net_interest_Income_annual_df = financials_df(Net_interest_Income_annual_10_unpacked, date_annual, "Net Interest Income")
                                        Prov_Credit_losses_annual_df = financials_df(Prov_Credit_losses_annual_10_unpacked, date_annual, "Provision for Credit Losses")
                                        Netinterest_Prov_Credit_losses_annual_df = financials_df(Netinterest_Prov_Credit_losses_annual_10_unpacked, date_annual, "Net Interest Income After Credit Losses Provision")
                                        Total_Non_interest_expenses_annual_df = financials_df(Total_Non_interest_expenses_annual_10_unpacked, date_annual, "Total Non Interest Expenses")
                                        Total_Non_interest_revenue_annual_df = financials_df(Total_Non_interest_revenue_annual_10_unpacked, date_annual, "Total Non-Interest Revenue")
                                        Ebita_annual_df = financials_df(Ebita_annual_10_unpacked, date_annual, "EBITDA")

                                                       ################################ Quarter###############################

                                        revenue_10_quarterly_df = financials_df(Revenue_quarter_10_unpacked, date_quarter, "Revenue")
                                        Pretax_income_quarterly_df = financials_df(Pretax_income_quarterly_10_unpacked, date_quarter, "Pretax Income")
                                        eps_basic_quarterly_df = financials_df(eps_basic_quarterly_10_unpacked, date_quarter, "EPS Basic")
                                        shares_basic_quarterly_df = financials_df(shares_basic_quarterly_10_unpacked, date_quarter, "Shares Basic")
                                        eps_diluted_quarterly_df = financials_df(Eps_diluted_quarterly_10_unpacked,date_quarter, "EPS Diluted")
                                        shares_diluted_quarterly_df = financials_df(shares_diluted_quarter_10_unpacked,date_quarter,"Shares Diluted")
                                        Income_tax_quarterly_df = financials_df(Income_tax_quarterly_10_unpacked, date_quarter, "Income Tax Expense")
                                        net_income_quarterly_df = financials_df(net_income_quarterly_10_unpacked, date_quarter, "Net Income")
                                        Total_interest_income_list_quarterly_df = financials_df(Total_interest_income_list_quarterly_10_unpacked, date_quarter, "Total Interest Income")
                                        Total_interest_expense_list_quarterly_df = financials_df(Total_interest_expense_list_quarterly_10_unpacked, date_quarter, "Total Interest Expense")
                                        Net_interest_Income_quarterly_df = financials_df(Net_interest_Income_quarterly_10_unpacked, date_quarter, "Net Interest Income")
                                        Prov_Credit_losses_quarterly_df = financials_df(Prov_Credit_losses_quarterly_10_unpacked, date_quarter, "Provision for Credit Losses")
                                        Netinterest_Prov_Credit_losses_quarterly_df = financials_df(Netinterest_Prov_Credit_losses_quarterly_10_unpacked, date_quarter, "Net Interest Income After Credit Losses Provision")
                                        Total_Non_interest_expenses_quarterly_df = financials_df(Total_Non_interest_expenses_quarterly_10_unpacked, date_quarter, "Total Non Interest Expenses")
                                        Total_Non_interest_revenue_quarterly_df = financials_df(Total_Non_interest_revenue_quarterly_10_unpacked, date_quarter, "Total Non-Interest Revenue")
                                        Ebita_quarter_10_unpacked_df = financials_df(Ebita_quarter_10_unpacked, date_quarter, "EBITDA")

                                        merged_df_annual = pd.concat([
                                                            Total_interest_income_list_annual_df,Total_interest_expense_list_annual_df,Net_interest_Income_annual_df,
                                                            Total_Non_interest_revenue_annual_df,Prov_Credit_losses_annual_df,revenue_2013_annual_df,
                                                            Netinterest_Prov_Credit_losses_annual_df, Total_Non_interest_expenses_annual_df,
                                                            Pretax_income_annual_df,Income_tax_annual_df,net_income_annual_df,eps_basic_annual_df,shares_basic_annual_df,
                                                            eps_diluted_annual_df,shares_diluted_annual_df,Ebita_annual_df
                                        
                                        ])
                                                       ################################ Quarter###############################

                                                                 
                                        merged_df_quarter = pd.concat([Total_interest_income_list_quarterly_df,Total_interest_expense_list_quarterly_df,
                                                            Net_interest_Income_quarterly_df,Total_Non_interest_revenue_quarterly_df,
                                                            Prov_Credit_losses_quarterly_df,revenue_10_quarterly_df,
                                                            Netinterest_Prov_Credit_losses_quarterly_df,Total_Non_interest_expenses_quarterly_df,
                                                            Pretax_income_quarterly_df,Income_tax_quarterly_df,net_income_quarterly_df,
                                                            eps_basic_quarterly_df,shares_basic_quarterly_df,
                                                            eps_diluted_quarterly_df,shares_diluted_quarterly_df,Ebita_quarter_10_unpacked_df])   


                                        st.table(merged_df_annual.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'})
                                             .set_table_styles(
                                             [{'selector': 'thead th', 'props': [('color', 'black')]}],  # Set font color of header (first row) to blue
                                             axis=1
                                        )
                                        )
                                                  
                                        pass
                                             

                                   except KeyError:
                                        try:
                                             if   f'{ticker}_Net_premiums_earned_annual_10' in st.session_state:
                                                  Net_premiums_earned_annual_10_unpacked = st.session_state[f'{ticker}_Net_premiums_earned_annual_10']
                                                  Net_investment_income_annual_10_unpacked = st.session_state[f'{ticker}_Net_investment_income_annual_10']
                                                  Fees_and_other_income_annual_10_unpacked = st.session_state[f'{ticker}_Fees_and_other_income_annual_10']
                                                  Interest_Expense_insurance_annual_10_unpacked = st.session_state[f'{ticker}_Interest_Expense_insurance_annual_10']
                                                  Policy_benefits_claim_annual_10_unpacked = st.session_state[f'{ticker}_Policy_benefits_claim_annual_10']
                                                  Operating_income_annual_10_unpacked = st.session_state[f'{ticker}_Operating_income_annual_10']
                                                  Pretax_income_annual_10_unpacked = st.session_state[f'{ticker}_Pretax_income_annual_10']
                                                  Income_tax_annual_10_unpacked = st.session_state[f'{ticker}_Income_tax_annual_10']
                                                  Ebita_annual_10_unpacked = st.session_state[f'{ticker}_Ebita_annual_10']

                                                  Net_premiums_earned_annual_10_unpacked = st.session_state[f'{ticker}_Net_premiums_earned_annual_10']
                                                  Net_investment_income_annual_10_unpacked = st.session_state[f'{ticker}_Net_investment_income_annual_10']
                                                  Fees_and_other_income_annual_10_unpacked = st.session_state[f'{ticker}_Fees_and_other_income_annual_10']
                                                  Interest_Expense_insurance_annual_10_unpacked = st.session_state[f'{ticker}_Interest_Expense_insurance_annual_10']
                                                  Policy_benefits_claim_annual_10_unpacked = st.session_state[f'{ticker}_Policy_benefits_claim_annual_10']
                                                  Operating_income_annual_10_unpacked = st.session_state[f'{ticker}_Operating_income_annual_10']
                                                  Pretax_income_annual_10_unpacked = st.session_state[f'{ticker}_Pretax_income_annual_10']
                                                  Income_tax_annual_10_unpacked = st.session_state[f'{ticker}_Income_tax_annual_10']
                                                  Ebita_annual_10_unpacked = st.session_state[f'{ticker}_Ebita_annual_10']

                                                       ################################ Quarter###############################


                                                  Net_premiums_earned_quarter_10_unpacked = st.session_state[f'{ticker}_Net_premiums_earned_quarter_10']
                                                  Net_investment_income_quarter_10_unpacked = st.session_state[f'{ticker}_Net_investment_income_quarter_10']
                                                  Fees_and_other_income_quarter_10_unpacked = st.session_state[f'{ticker}_Fees_and_other_income_quarter_10']
                                                  Interest_Expense_insurance_quarter_10_unpacked = st.session_state[f'{ticker}_Interest_Expense_insurance_quarter_10']
                                                  Policy_benenfits_claim_quarter_quarter_10_unpacked = st.session_state[f'{ticker}_Policy_benenfits_claim_quarter_quarter_10']
                                                  Operating_income_quarter_quarter_10_unpacked = st.session_state[f'{ticker}_Operating_income_quarter_quarter_10']
                                                  Pretax_income_quarter_10_unpacked = st.session_state[f'{ticker}_Pretax_income_quarter_10']
                                                  Income_tax_quarter_10_unpacked = st.session_state[f'{ticker}_Income_tax_quarter_10']
                                                  Ebita_quarter_10_unpacked = st.session_state[f'{ticker}_Ebita_quarter_10']

                                             else:
                                                       # Unpack data from annual_data
                                                  Net_premiums_earned_annual_10_unpacked = annual_data['premiums_earned'][-10:]
                                                  Net_investment_income_annual_10_unpacked = annual_data['net_investment_income'][-10:]
                                                  Fees_and_other_income_annual_10_unpacked = annual_data['fees_and_other_income'][-10:]
                                                  Interest_Expense_insurance_annual_10_unpacked = annual_data['interest_expense_insurance'][-10:]
                                                  Policy_benefits_claim_annual_10_unpacked = annual_data['net_policyholder_claims_expense'][-10:]
                                                  Operating_income_annual_10_unpacked = annual_data['operating_income'][-10:]
                                                  Pretax_income_annual_10_unpacked = annual_data['pretax_income'][-10:]
                                                  Income_tax_annual_10_unpacked = annual_data['income_tax'][-10:]
                                                  Ebita_annual_10_unpacked = annual_data['ebitda'][-10:]

                                                       ################################ Quarter###############################

                                                  Net_premiums_earned_quarter_10_unpacked = quarterly_data['premiums_earned'][-10:]
                                                  Net_investment_income_quarter_10_unpacked = quarterly_data['net_investment_income'][-10:]
                                                  Fees_and_other_income_quarter_10_unpacked = quarterly_data['fees_and_other_income'][-10:]
                                                  Interest_Expense_insurance_quarter_10_unpacked = quarterly_data['interest_expense_insurance'][-10:]
                                                  Policy_benenfits_claim_quarter_quarter_10_unpacked = quarterly_data['net_policyholder_claims_expense'][-10:]
                                                  Operating_income_quarter_quarter_10_unpacked = quarterly_data['operating_income'][-10:]
                                                  Pretax_income_quarter_10_unpacked = quarterly_data['pretax_income'][-10:]
                                                  Income_tax_quarter_10_unpacked = quarterly_data['income_tax'][-10:]
                                                  Ebita_quarter_10_unpacked = quarterly_data['ebitda'][-10:]


                                                  # Store unpacked data in session state
                                                  st.session_state[f'{ticker}_Net_premiums_earned_annual_10'] = Net_premiums_earned_annual_10_unpacked
                                                  st.session_state[f'{ticker}_Net_investment_income_annual_10'] = Net_investment_income_annual_10_unpacked
                                                  st.session_state[f'{ticker}_Fees_and_other_income_annual_10'] = Fees_and_other_income_annual_10_unpacked
                                                  st.session_state[f'{ticker}_Interest_Expense_insurance_annual_10'] = Interest_Expense_insurance_annual_10_unpacked
                                                  st.session_state[f'{ticker}_Policy_benefits_claim_annual_10'] = Policy_benefits_claim_annual_10_unpacked
                                                  st.session_state[f'{ticker}_Operating_income_annual_10'] = Operating_income_annual_10_unpacked
                                                  st.session_state[f'{ticker}_Pretax_income_annual_10'] = Pretax_income_annual_10_unpacked
                                                  st.session_state[f'{ticker}_Income_tax_annual_10'] = Income_tax_annual_10_unpacked
                                                  st.session_state[f'{ticker}_Ebita_annual_10'] = Ebita_annual_10_unpacked

                                                            ################################ Quarter###############################
                                                                                                                                       # Store unpacked data in session state
                                                  st.session_state[f'{ticker}_Net_premiums_earned_quarter_10'] = Net_premiums_earned_quarter_10_unpacked
                                                  st.session_state[f'{ticker}_Net_investment_income_quarter_10'] = Net_investment_income_quarter_10_unpacked
                                                  st.session_state[f'{ticker}_Fees_and_other_income_quarter_10'] = Fees_and_other_income_quarter_10_unpacked
                                                  st.session_state[f'{ticker}_Interest_Expense_insurance_quarter_10'] = Interest_Expense_insurance_quarter_10_unpacked
                                                  st.session_state[f'{ticker}_Policy_benenfits_claim_quarter_quarter_10'] = Policy_benenfits_claim_quarter_quarter_10_unpacked
                                                  st.session_state[f'{ticker}_Operating_income_quarter_quarter_10'] = Operating_income_quarter_quarter_10_unpacked
                                                  st.session_state[f'{ticker}_Pretax_income_quarter_10'] = Pretax_income_quarter_10_unpacked
                                                  st.session_state[f'{ticker}_Income_tax_quarter_10'] = Income_tax_quarter_10_unpacked
                                                  st.session_state[f'{ticker}_Ebita_quarter_10'] = Ebita_quarter_10_unpacked
                                                  st.session_state[f'{ticker}_shares_diluted_quarter_10_unpacked'] =shares_diluted_quarter_10_unpacked



                                             Net_premiums_earned_annual_10_unpacked = annual_data['premiums_earned'][-10:] 
                                             Net_investment_income_annual_10_unpacked  = annual_data['net_investment_income'][-10:] 
                                             Fees_and_other_income_annual_10_unpacked  = annual_data['fees_and_other_income'][-10:] 
                                             Interest_Expense_insurance_annual_10_unpacked  = annual_data['interest_expense_insurance'][-10:] 
                                             Policy_benenfits_claim_annual_10_unpacked = annual_data['net_policyholder_claims_expense'][-10:]
                                             Operating_income_annual_10_unpacked  = annual_data['operating_income'][-10:]
                                             Pretax_income_annual_10_unpacked  = annual_data['pretax_income'][-10:]
                                             Income_tax_annual_10_unpacked = annual_data['income_tax'][-10:]
                                             Ebita_annual_10_unpacked = annual_data['ebitda'][-10:]
          

                                             Net_premiums_earned_df = financials_df(Net_premiums_earned_annual_10_unpacked, date_annual, "Net Premiums Earned")
                                             Net_investment_income_df = financials_df(Net_investment_income_annual_10_unpacked, date_annual, "Net Investment Income")
                                             Fees_and_other_income_df = financials_df(Fees_and_other_income_annual_10_unpacked, date_annual, "Fees and Other Income")
                                             revenue_2013_df = financials_df(Revenue_annual_10_unpacked, date_annual, "Total Revenue")
                                             Policy_benenfits_claim_annual_df = financials_df(Policy_benefits_claim_annual_10_unpacked, date_annual, "Policy Benefits & Claims")
                                             Operating_income_annual_df = financials_df(Operating_income_annual_10_unpacked, date_annual, "Operating Income")
                                             Interest_Expense_insurance_df = financials_df(Interest_Expense_insurance_annual_10_unpacked, date_annual, "Interest Expense")

                                             Pretax_income_annual_df = financials_df(Pretax_income_annual_10_unpacked, date_annual, "Pretax Income")
                                             net_income_annual_df = financials_df(net_income_annual_10_unpacked, date_annual, "Net Income")
                                             eps_basic_annual_df = financials_df(eps_basic_annual_10_unpacked, date_annual, "EPS Basic")
                                             shares_basic_annual_df = financials_df(shares_basic_annual_10_unpacked, date_annual, "Shares Basic")
                                             eps_diluted_annual_df = financials_df(eps_diluted_annual_10_unpacked, date_annual, "EPS Diluted")
                                             shares_diluted_annual_df = financials_df(shares_diluted_annual_10_unpacked, date_annual, "Shares Diluted")
                                             Income_tax_annual_df = financials_df(Income_tax_annual_10_unpacked, date_annual, "Income Tax Expense")
                                             Ebita_annual_df = financials_df(Ebita_annual_10_unpacked, date_annual, "EBITDA")

                                                            ################################ Quarter###############################


                                             Net_premiums_earned_quarter_df = financials_df(Net_premiums_earned_quarter_10_unpacked, date_quarter, "Net Premiums Earned")
                                             Net_investment_income_quarter_df = financials_df(Net_investment_income_quarter_10_unpacked, date_quarter, "Net Investment Income")
                                             Fees_and_other_income_quarter_df = financials_df(Fees_and_other_income_quarter_10_unpacked, date_quarter, "Fees and Other Income")
                                             Interest_Expense_insurance_quarter_df = financials_df(Interest_Expense_insurance_quarter_10_unpacked, date_quarter, "Interest Expense")
                                             revenue_2013_quarter_df = financials_df(Revenue_quarter_10_unpacked, date_quarter, "Total Revenue")
                                             Policy_benenfits_claim_quarter_df = financials_df(Policy_benenfits_claim_quarter_quarter_10_unpacked, date_quarter, "Policy Benefits & Claims")
                                             Operating_income_quarter_df = financials_df(Operating_income_quarter_quarter_10_unpacked, date_quarter, "Operating Income")                   
                                             Pretax_income_quarter_df = financials_df(Pretax_income_quarter_10_unpacked, date_quarter, "Pretax Income")
                                             net_income_quarter_df = financials_df(net_income_quarter_10_unpacked, date_quarter, "Net Income")
                                             eps_basic_quarter_df = financials_df(eps_basic_quarterly_10_unpacked, date_quarter, "EPS Basic")
                                             shares_basic_quarter_df = financials_df(shares_basic_quarterly_10_unpacked, date_quarter, "Shares Basic")
                                             eps_diluted_quarter_df = financials_df(Eps_diluted_quarterly_10_unpacked, date_quarter, "EPS Diluted")
                                             shares_diluted_quarter_df = financials_df(shares_diluted_quarter_10_unpacked, date_quarter, "Shares Diluted")
                                             Income_tax_quarter_df = financials_df(Income_tax_quarter_10_unpacked, date_quarter, "Income Tax Expense")
                                             Ebita_quarter_10_unpacked_df = financials_df(Ebita_quarter_10_unpacked, date_quarter, "EBITDA")


                                             merged_df = pd.concat([Net_premiums_earned_df,Net_investment_income_df,Fees_and_other_income_df,revenue_2013_df,
                                                                 Policy_benenfits_claim_annual_df,Operating_income_annual_df,Interest_Expense_insurance_df,Pretax_income_annual_df,
                                                                 Income_tax_annual_df,net_income_annual_df,
                                                                 eps_basic_annual_df,shares_basic_annual_df,eps_diluted_annual_df,shares_diluted_annual_df,Ebita_annual_df]) 
                                                                                               ################################ Quarter###############################

                                             merged_df_quarter= pd.concat([
                                                            Net_premiums_earned_quarter_df, Net_investment_income_quarter_df, Fees_and_other_income_quarter_df, revenue_2013_quarter_df, Policy_benenfits_claim_quarter_df,
                                                            Operating_income_quarter_df,Interest_Expense_insurance_quarter_df,
                                                            Pretax_income_quarter_df,Income_tax_quarter_df,net_income_quarter_df, eps_basic_quarter_df, shares_basic_quarter_df,
                                                            eps_diluted_quarter_df, shares_diluted_quarter_df,Ebita_quarter_10_unpacked_df
                                                            ])

                                             st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'})                                             .set_table_styles(
                                             [{'selector': 'thead th', 'props': [('color', 'black')]}],  # Set font color of header (first row) to blue
                                             axis=1
                                        )
                                        )

                                             pass


                                        except KeyError:
                                             
                                             try: 
                                                  if f'{ticker}_Pretax_income_annual_10' in st.session_state:
                                                       Pretax_income_annual_10_unpacked = st.session_state[f'{ticker}_Pretax_income_annual_10']
                                                       Income_tax_annual_10_unpacked = st.session_state[f'{ticker}_Income_tax_annual_10']
                                                       cogs_list_annual_10_unpacked = st.session_state[f'{ticker}_COGS_annual_10']
                                                       gross_profit_annual_10_unpacked = st.session_state[f'{ticker}_Gross_profit_annual_10']
                                                       SGA_Expense_annual_10_unpacked = st.session_state[f'{ticker}_SGA_Expense_annual_10']
                                                       Depreciation_Depletion_Amortisation_annual_10_unpacked = st.session_state[f'{ticker}_Depreciation_Depletion_Amortisation_annual_10']
                                                       Interest_Income_annual_10_unpacked = st.session_state[f'{ticker}_Interest_Income_annual_10']
                                                       Research_Dev_annual_10_unpacked = st.session_state[f'{ticker}_Research_Dev_annual_10']
                                                       interest_expense_list_annual_10_unpacked = st.session_state[f'{ticker}_Interest_Expense_annual_10']
                                                       Ebita_annual_10_unpacked = st.session_state[f'{ticker}_EBITDA_annual_10']
                                                       operating_income_list_annual_10_unpacked = st.session_state[f'{ticker}_Operating_Income_annual_10']
                                                       

                                                       ################################ Quarter###############################
                                                       Pretax_income_quarter_10_unpacked = st.session_state[f'{ticker}_Pretax_income_quarter_10']
                                                       Income_tax_quarter_10_unpacked = st.session_state[f'{ticker}_Income_tax_quarter_10']
                                                       cogs_list_quarter_10_unpacked = st.session_state[f'{ticker}_cogs_list_quarter_10']
                                                       gross_profit_quarter_10_unpacked = st.session_state[f'{ticker}_gross_profit_quarter_10']
                                                       SGA_Expense_quarter_10_unpacked = st.session_state[f'{ticker}_SGA_Expense_quarter_10']
                                                       Depreciation_Depletion_Amortisation_quater_10_unpacked = st.session_state[f'{ticker}_Depreciation_Depletion_Amortisation_quater_10']
                                                       Interest_Income_quarter_10_unpacked = st.session_state[f'{ticker}_Interest_Income_quarter_10']
                                                       Research_Dev_quarter_10_unpacked = st.session_state[f'{ticker}_Research_Dev_quarter_10']
                                                       interest_expense_list_quarter_10_unpacked = st.session_state[f'{ticker}_interest_expense_list_quarter_10']
                                                       Ebita_quarter_10_unpacked = st.session_state[f'{ticker}_Ebita_quarter_10']
                                                       operating_income_list_quarter_10_unpacked = st.session_state[f'{ticker}_operating_income_list_quarter_10']
                                                                                                              

                                                  else:             
                                                       Pretax_income_annual_10_unpacked  = annual_data['pretax_income'][-10:]
                                                       Income_tax_annual_10_unpacked   = annual_data['income_tax'][-10:]
                                                       cogs_list_annual_10_unpacked  = annual_data['cogs'][-10:]
                                                       gross_profit_annual_10_unpacked  = annual_data['gross_profit'][-10:]
                                                       SGA_Expense_annual_10_unpacked   = annual_data['total_opex'][-10:]

                                                       Research_Dev_annual_10_unpacked  = annual_data['rnd'][-10:]
                                                       interest_expense_list_annual_10_unpacked  = annual_data['interest_expense'][-10:]
                                                       Ebita_annual_10_unpacked = annual_data['ebitda'][-10:]
                                                       operating_income_list_annual_10_unpacked = annual_data['operating_income'][-10:] 


                                                       ################################ Quarter###############################

                                                       Pretax_income_quarter_10_unpacked  = quarterly_data['pretax_income'][-10:]
                                                       Income_tax_quarter_10_unpacked  = quarterly_data['income_tax'][-10:]
                                                       cogs_list_quarter_10_unpacked  = quarterly_data['cogs'][-10:]
                                                       gross_profit_quarter_10_unpacked  = quarterly_data['gross_profit'][-10:]
                                                       SGA_Expense_quarter_10_unpacked  = quarterly_data['total_opex'][-10:]
                                                       Research_Dev_quarter_10_unpacked   = quarterly_data['rnd'][-10:]
                                                       interest_expense_list_quarter_10_unpacked   = quarterly_data['interest_expense'][-10:]
                                                       Ebita_quarter_10_unpacked = quarterly_data['ebitda'][-10:]
                                                       operating_income_list_quarter_10_unpacked  = quarterly_data['operating_income'][-10:] 


                                                       try:
                                                            Depreciation_Depletion_Amortisation_annual_10_unpacked  = annual_data['cfo_da'][-10:]
                                                            Interest_Income_annual_10_unpacked = annual_data['interest_income'][-10:]

                                                                      ################################ Quarter###############################
                                                            Depreciation_Depletion_Amortisation_quater_10_unpacked = quarterly_data['cfo_da'][-10:]
                                                            Interest_Income_quarter_10_unpacked = quarterly_data['interest_income'][-10:]

                                                       
                                                       except Exception as e:
                                                            Depreciation_Depletion_Amortisation_annual_10_unpacked = [0] * len_10_annual
                                                            Interest_Income_annual_10_unpacked = [0] * len_10_annual
                                                                      ################################ Quarter###############################

                                                            Depreciation_Depletion_Amortisation_quater_10_unpacked= [0] * len_10_quarter 
                                                            Interest_Income_quarter_10_unpacked= [0] * len_10_quarter 


                                                  
                                                                      ################################ Quarter###############################

                                                       Research_Dev_quarter_10_unpacked  = quarterly_data['rnd'][-10:]
                                                       interest_expense_list_quarter_10_unpacked  = quarterly_data['interest_expense'][-10:]
                                                       Ebita_quarter_10_unpacked = quarterly_data['ebitda'][-10:]
                                                       operating_income_list_quarter_10_unpacked = quarterly_data['operating_income'][-10:] 


                                                                                                    # Store unpacked data in session state
                                                       st.session_state[f'{ticker}_Pretax_income_annual_10'] = Pretax_income_annual_10_unpacked
                                                       st.session_state[f'{ticker}_Income_tax_annual_10'] = Income_tax_annual_10_unpacked
                                                       st.session_state[f'{ticker}_COGS_annual_10'] = cogs_list_annual_10_unpacked
                                                       st.session_state[f'{ticker}_Gross_profit_annual_10'] = gross_profit_annual_10_unpacked
                                                       st.session_state[f'{ticker}_SGA_Expense_annual_10'] = SGA_Expense_annual_10_unpacked
                                                       st.session_state[f'{ticker}_Depreciation_Depletion_Amortisation_annual_10'] = Depreciation_Depletion_Amortisation_annual_10_unpacked
                                                       st.session_state[f'{ticker}_Interest_Income_annual_10'] = Interest_Income_annual_10_unpacked
                                                       st.session_state[f'{ticker}_Research_Dev_annual_10'] = Research_Dev_annual_10_unpacked
                                                       st.session_state[f'{ticker}_Interest_Expense_annual_10'] = interest_expense_list_annual_10_unpacked
                                                       st.session_state[f'{ticker}_EBITDA_annual_10'] = Ebita_annual_10_unpacked
                                                       st.session_state[f'{ticker}_Operating_Income_annual_10'] = operating_income_list_annual_10_unpacked

                                                                      ################################ Quarter###############################

                                                                                               # Store unpacked data in session state
                                                       st.session_state[f'{ticker}_Pretax_income_quarter_10'] = Pretax_income_quarter_10_unpacked
                                                       st.session_state[f'{ticker}_Income_tax_quarter_10'] = Income_tax_quarter_10_unpacked
                                                       st.session_state[f'{ticker}_cogs_list_quarter_10'] = cogs_list_quarter_10_unpacked
                                                       st.session_state[f'{ticker}_gross_profit_quarter_10'] = gross_profit_quarter_10_unpacked
                                                       st.session_state[f'{ticker}_SGA_Expense_quarter_10'] = SGA_Expense_quarter_10_unpacked
                                                       st.session_state[f'{ticker}_Depreciation_Depletion_Amortisation_quater_10'] = Depreciation_Depletion_Amortisation_quater_10_unpacked
                                                       st.session_state[f'{ticker}_Interest_Income_quarter_10'] = Interest_Income_quarter_10_unpacked
                                                       st.session_state[f'{ticker}_Research_Dev_quarter_10'] = Research_Dev_quarter_10_unpacked
                                                       st.session_state[f'{ticker}_interest_expense_list_quarter_10'] = interest_expense_list_quarter_10_unpacked
                                                       st.session_state[f'{ticker}_Ebita_quarter_10'] = Ebita_quarter_10_unpacked
                                                       st.session_state[f'{ticker}_operating_income_list_quarter_10'] = operating_income_list_quarter_10_unpacked




                                                  revenue_2013_annual_df = financials_df(Revenue_annual_10_unpacked, date_annual, "Revenue")
                                                  Pretax_income_annual_df = financials_df(Pretax_income_annual_10_unpacked, date_annual, "Pretax Income")
                                                  eps_basic_annual_df = financials_df(eps_basic_annual_10_unpacked, date_annual, "EPS Basic")
                                                  shares_basic_annual_df = financials_df(shares_basic_annual_10_unpacked, date_annual, "Shares Basic")
                                                  eps_diluted_annual_df = financials_df(eps_diluted_annual_10_unpacked, date_annual, "EPS Diluted")
                                                  shares_diluted_annual_df = financials_df(shares_diluted_annual_10_unpacked, date_annual, "Shares Diluted")
                                                  Income_tax_annual_df = financials_df(Income_tax_annual_10_unpacked, date_annual, "Income Tax Expense")
                                                  net_income_annual_df = financials_df(net_income_annual_10_unpacked, date_annual, "Net Income")
                                                  cogs_list_annual_df = financials_df(cogs_list_annual_10_unpacked, date_annual, "COGS")
                                                  gross_profit_annual_df = financials_df(gross_profit_annual_10_unpacked, date_annual, "Gross Profit")
                                                  SGA_Expense_annual_df = financials_df(SGA_Expense_annual_10_unpacked, date_annual, "SGA Expense")
                                                  Depreciation_Depletion_Amortisation_annual_df = financials_df(Depreciation_Depletion_Amortisation_annual_10_unpacked, date_annual, "Depreciation & Amortization")
                                                  Interest_Income_annual_df = financials_df(Interest_Income_annual_10_unpacked, date_annual, "Interest Income")
                                                  Research_Dev_annual_df = financials_df(Research_Dev_annual_10_unpacked, date_annual, "R&D Expense")
                                                  interest_expense_list_annual_df = financials_df(interest_expense_list_annual_10_unpacked, date_annual, "Interest Expense")
                                                  Ebita_annual_df = financials_df(Ebita_annual_10_unpacked, date_annual, "EBITDA")
                                                  operating_income_list_annual_df = financials_df(operating_income_list_annual_10_unpacked, date_annual, "Operating Income")
                                                                      ################################ Quarter###############################

                                                  revenue_2013_quarter_df = financials_df(Revenue_quarter_10_unpacked, date_quarter, "Revenue")
                                                  Pretax_income_quarter_df = financials_df(Pretax_income_quarter_10_unpacked, date_quarter, "Pretax Income")
                                                  eps_basic_quarter_df = financials_df(eps_basic_quarterly_10_unpacked, date_quarter, "EPS Basic")
                                                  shares_basic_quarter_df = financials_df(shares_basic_quarterly_10_unpacked, date_quarter, "Shares Basic")
                                                  eps_diluted_quarter_df = financials_df(Eps_diluted_quarterly_10_unpacked, date_quarter, "EPS Diluted")
                                                  shares_diluted_quarter_df = financials_df(shares_diluted_quarter_10_unpacked, date_quarter, "Shares Diluted")
                                                  Income_tax_quarter_df = financials_df(Income_tax_quarter_10_unpacked, date_quarter, "Income Tax Expense")
                                                  net_income_quarter_df = financials_df(net_income_quarter_10_unpacked, date_quarter, "Net Income")
                                                  cogs_list_quarter_df = financials_df(cogs_list_quarter_10_unpacked, date_quarter, "COGS")
                                                  gross_profit_quarter_df = financials_df(gross_profit_quarter_10_unpacked, date_quarter, "Gross Profit")
                                                  SGA_Expense_quarter_df = financials_df(SGA_Expense_quarter_10_unpacked, date_quarter, "SGA Expense")
                                                  Research_Dev_quarter_df = financials_df(Research_Dev_quarter_10_unpacked, date_quarter, "R&D Expense")
                                                  Depreciation_Depletion_Amortisation_quater_df = financials_df(Depreciation_Depletion_Amortisation_quater_10_unpacked, date_quarter, "Depreciation & Amortization")
                                                  Interest_Income_quarter_df = financials_df(Interest_Income_quarter_10_unpacked, date_quarter, "Interest Income")
                                                  interest_expense_list_quarter_df = financials_df(interest_expense_list_quarter_10_unpacked, date_quarter, "Interest Expense")
                                                  Ebita_quarter_10_unpacked_df = financials_df(Ebita_quarter_10_unpacked, date_quarter, "EBITDA")
                                                  operating_income_list_quarter_df = financials_df(operating_income_list_quarter_10_unpacked, date_quarter, "Operating Income")

                                                  merged_df = pd.concat([
                                                  revenue_2013_annual_df,cogs_list_annual_df,gross_profit_annual_df, SGA_Expense_annual_df, Research_Dev_annual_df,
                                                  Depreciation_Depletion_Amortisation_annual_df,
                                                  operating_income_list_annual_df,interest_expense_list_annual_df,
                                                  Interest_Income_annual_df,Pretax_income_annual_df,Income_tax_annual_df,
                                                  net_income_annual_df ,eps_basic_annual_df, 
                                                  shares_basic_annual_df,
                                                  eps_diluted_annual_df, shares_diluted_annual_df,Ebita_annual_df
                                                  ])
                                                  
                                                                      ################################ Quarter###############################


                                                  merged_df_quarter = pd.concat([
                                                  revenue_2013_quarter_df, cogs_list_quarter_df,gross_profit_quarter_df, SGA_Expense_quarter_df, Research_Dev_quarter_df,
                                                  Depreciation_Depletion_Amortisation_quater_df,operating_income_list_quarter_df,
                                                  interest_expense_list_quarter_df,Interest_Income_quarter_df,Pretax_income_quarter_df,
                                                  Income_tax_quarter_df,
                                                  net_income_quarter_df,eps_basic_quarter_df, shares_basic_quarter_df,
                                                  eps_diluted_quarter_df, shares_diluted_quarter_df,
                                                  Ebita_quarter_10_unpacked_df
                                                  ])


                                                  st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'})                                             .set_table_styles(
                                             [{'selector': 'thead th', 'props': [('color', 'black')]}],  # Set font color of header (first row) to blue
                                             axis=1
                                                  )
                                                  )

                                                  pass
                                             except KeyError:
                                                  st.write("") 
                                                  pass      

                              with Quarterly:
                                   st.table(merged_df_quarter.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'})                                             .set_table_styles(
                                             [{'selector': 'thead th', 'props': [('color', 'black')]}],  # Set font color of header (first row) to blue
                                             axis=1
                                        ))

 

                         with Balance_Sheet:
                              Annual,Quarterly = st.tabs(["Annual","Quarterly"])
                              date_annual = annual_data['period_end_date'][-10:]
                              date_quarter = quarterly_data['period_end_date'][-10:]

                                             
                              with Annual:

                                                  
                                   try:

                                        if f'{ticker}_cash_and_cash_investments_annual' in st.session_state:
                                             cash_und_cash_investments = st.session_state[f'{ticker}_cash_and_cash_investments_annual']
                                             Total_investments_annual = st.session_state[f'{ticker}_Total_investments_annual']
                                             Gross_loans_annual = st.session_state[f'{ticker}_Gross_loans_annual']
                                             Loans_loss_annual = st.session_state[f'{ticker}_Loans_loss_annual']
                                             Net_Loan_annual = st.session_state[f'{ticker}_Net_Loan_annual']
                                             Unearned_income_annual = st.session_state[f'{ticker}_Unearned_income_annual']
                                             Net_goodwill_annual = st.session_state[f'{ticker}_Net_goodwill_annual']
                                             Intangible_assets_annual = st.session_state[f'{ticker}_Intangible_assets_annual']
                                             Other_lt_assets_annual = st.session_state[f'{ticker}_Other_lt_assets_annual']
                                             Total_assets_annual = st.session_state[f'{ticker}_Total_assets_annual']
                                             Deposits_annual = st.session_state[f'{ticker}_Deposits_annual']
                                             Short_term_debt_annual = st.session_state[f'{ticker}_Short_term_debt_annual']
                                             LongTerm_debt_annual = st.session_state[f'{ticker}_LongTerm_debt_annual']
                                             Other_longterm_liabilities_annual = st.session_state[f'{ticker}_Other_longterm_liabilities_annual']
                                             Retained_earnings_annual = st.session_state[f'{ticker}_Retained_earnings_annual']
                                             Total_liabilities_annual = st.session_state[f'{ticker}_Total_liabilities_annual']
                                             Total_Equity_annual = st.session_state[f'{ticker}_Total_Equity_annual']

                                             ################################ Quarter###############################
                                             cash_and_equiv_quarterly_Balance_Sheet = st.session_state[f'{ticker}_cash_and_equiv_quarterly_Balance_Sheet']
                                             Total_investments_quarterly_Balance_Sheet = st.session_state[f'{ticker}_Total_investments_quarterly_Balance_Sheet']
                                             Gross_loans_quarter = st.session_state[f'{ticker}_Gross_loans_quarter']
                                             Loans_loss_quarter = st.session_state[f'{ticker}_Loans_loss_quarter']
                                             Net_Loan_quarter = st.session_state[f'{ticker}_Net_Loan_quarter']
                                             Unearned_income_quarter = st.session_state[f'{ticker}_Unearned_income_quarter']
                                             Net_goodwill_quarter = st.session_state[f'{ticker}_Net_goodwill_quarter']
                                             Intangible_assets_quarter = st.session_state[f'{ticker}_Intangible_assets_quarter']
                                             Other_lt_assets_quarter = st.session_state[f'{ticker}_Other_lt_assets_quarter']
                                             Total_assets_quarter = st.session_state[f'{ticker}_Total_assets_quarter']
                                             Deposits_quarter = st.session_state[f'{ticker}_Deposits_quarter']
                                             Short_term_debt_quarter10_unpacked = st.session_state[f'{ticker}_Short_term_debt_quarter']
                                             LongTerm_debt_quarter10_unpacked = st.session_state[f'{ticker}_LongTerm_debt_quarter']
                                             Other_longterm_liabilities_quarter10_unpacked = st.session_state[f'{ticker}_Other_longterm_liabilities_quarter']
                                             Retained_earnings_quarter = st.session_state[f'{ticker}_Retained_earnings_quarter']
                                             Total_liabilities_quarter = st.session_state[f'{ticker}_Total_liabilities_quarter']
                                             Total_Equity_quarter10_unpacked = st.session_state[f'{ticker}_Total_Equity_quarter']

                                        else:
                                             cash_und_cash_investments = annual_data['cash_and_equiv'][-10:]
                                             Total_investments_annual = annual_data['total_investments'][-10:]
                                             Gross_loans_annual = annual_data['loans_gross'][-10:]
                                             Loans_loss_annual = annual_data['allowance_for_loan_losses'][-10:]
                                             Net_Loan_annual = annual_data['loans_net'][-10:]
                                             Unearned_income_annual = annual_data['unearned_income'][-10:]
                                             Net_goodwill_annual = annual_data['goodwill'][-10:]
                                             Intangible_assets_annual = annual_data['intangible_assets'][-10:]
                                             Other_lt_assets_annual = annual_data['other_lt_assets'][-10:]
                                             Total_assets_annual = annual_data['total_assets'][-10:]
                                             Deposits_annual = annual_data['deposits_liability'][-10:]
                                             Short_term_debt_annual = annual_data['st_debt'][-10:]
                                             LongTerm_debt_annual = annual_data['lt_debt'][-10:]
                                             Other_longterm_liabilities_annual = annual_data['other_lt_liabilities'][-10:]
                                             Retained_earnings_annual = annual_data['retained_earnings'][-10:]
                                             Total_liabilities_annual = annual_data['total_liabilities'][-10:]
                                             Total_Equity_annual = annual_data['total_equity'][-10:]
                                             ################################ Quarter###############################

                                             cash_and_equiv_quarterly_Balance_Sheet = quarterly_data['cash_and_equiv'][-10:]
                                             Total_investments_quarterly_Balance_Sheet = quarterly_data['total_investments'][-10:]
                                             Gross_loans_quarter = quarterly_data['loans_gross'][-10:]
                                             Loans_loss_quarter = quarterly_data['allowance_for_loan_losses'][-10:]
                                             Net_Loan_quarter = quarterly_data['loans_net'][-10:]
                                             Unearned_income_quarter = quarterly_data['unearned_income'][-10:]
                                             Net_goodwill_quarter= quarterly_data['goodwill'][-10:]
                                             Intangible_assets_quarter= quarterly_data['intangible_assets'][-10:]
                                             Other_lt_assets_quarter = quarterly_data['other_lt_assets'][-10:]
                                             Total_assets_quarter = quarterly_data['total_assets'][-10:]
                                             Deposits_quarter = quarterly_data['deposits_liability'][-10:]
                                             Short_term_debt_quarter10_unpacked = quarterly_data['st_debt'][-10:]
                                             LongTerm_debt_quarter10_unpacked = quarterly_data['lt_debt'][-10:]
                                             Other_longterm_liabilities_quarter10_unpacked = quarterly_data['other_lt_liabilities'][-10:]
                                             Retained_earnings_quarter = quarterly_data['retained_earnings'][-10:]
                                             Total_liabilities_quarter10_unpacked = quarterly_data['total_liabilities'][-10:]
                                             Total_Equity_quarter10_unpacked = quarterly_data['total_equity'][-10:]

                                             
                                             # Store unpacked data in session state
                                             st.session_state[f'{ticker}_cash_and_cash_investments_annual'] = cash_und_cash_investments
                                             st.session_state[f'{ticker}_Total_investments_annual'] = Total_investments_annual
                                             st.session_state[f'{ticker}_Gross_loans_annual'] = Gross_loans_annual
                                             st.session_state[f'{ticker}_Loans_loss_annual'] = Loans_loss_annual
                                             st.session_state[f'{ticker}_Net_Loan_annual'] = Net_Loan_annual
                                             st.session_state[f'{ticker}_Unearned_income_annual'] = Unearned_income_annual
                                             st.session_state[f'{ticker}_Net_goodwill_annual'] = Net_goodwill_annual
                                             st.session_state[f'{ticker}_Intangible_assets_annual'] = Intangible_assets_annual
                                             st.session_state[f'{ticker}_Other_lt_assets_annual'] = Other_lt_assets_annual
                                             st.session_state[f'{ticker}_Total_assets_annual'] = Total_assets_annual
                                             st.session_state[f'{ticker}_Deposits_annual'] = Deposits_annual
                                             st.session_state[f'{ticker}_Short_term_debt_annual'] = Short_term_debt_annual
                                             st.session_state[f'{ticker}_LongTerm_debt_annual'] = LongTerm_debt_annual
                                             st.session_state[f'{ticker}_Other_longterm_liabilities_annual'] = Other_longterm_liabilities_annual
                                             st.session_state[f'{ticker}_Retained_earnings_annual'] = Retained_earnings_annual
                                             st.session_state[f'{ticker}_Total_liabilities_annual'] = Total_liabilities_annual
                                             st.session_state[f'{ticker}_Total_Equity_annual'] = Total_Equity_annual

                                             ################################ Quarter###############################
                                                                                          
                                             #Store unpacked data in session state
                                             st.session_state[f'{ticker}_cash_and_equiv_quarterly_Balance_Sheet'] = cash_and_equiv_quarterly_Balance_Sheet
                                             st.session_state[f'{ticker}_Total_investments_quarterly_Balance_Sheet'] = Total_investments_quarterly_Balance_Sheet
                                             st.session_state[f'{ticker}_Gross_loans_quarter'] = Gross_loans_quarter
                                             st.session_state[f'{ticker}_Loans_loss_quarter'] = Loans_loss_quarter
                                             st.session_state[f'{ticker}_Net_Loan_quarter'] = Net_Loan_quarter
                                             st.session_state[f'{ticker}_Unearned_income_quarter'] = Unearned_income_quarter
                                             st.session_state[f'{ticker}_Net_goodwill_quarter'] = Net_goodwill_quarter
                                             st.session_state[f'{ticker}_Intangible_assets_quarter'] = Intangible_assets_quarter
                                             st.session_state[f'{ticker}_Other_lt_assets_quarter'] = Other_lt_assets_quarter
                                             st.session_state[f'{ticker}_Total_assets_quarter'] = Total_assets_quarter
                                             st.session_state[f'{ticker}_Deposits_quarter'] = Deposits_quarter
                                             st.session_state[f'{ticker}_Short_term_debt_quarter'] = Short_term_debt_quarter10_unpacked
                                             st.session_state[f'{ticker}_LongTerm_debt_quarter'] = LongTerm_debt_quarter10_unpacked
                                             st.session_state[f'{ticker}_Other_longterm_liabilities_quarter'] = Other_longterm_liabilities_quarter10_unpacked
                                             st.session_state[f'{ticker}_Retained_earnings_quarter'] = Retained_earnings_quarter
                                             st.session_state[f'{ticker}_Total_liabilities_quarter'] = Total_liabilities_quarter10_unpacked
                                             st.session_state[f'{ticker}_Total_Equity_quarter'] = Total_Equity_quarter10_unpacked
                                                                      



                                        cash_und_cash_investments_df = financials_df(cash_und_cash_investments, date_annual, "Cash & Equivalents")
                                        Total_investments_annual_df = financials_df(Total_investments_annual, date_annual, "Total Investments")
                                        Gross_loans_annual_df = financials_df(Gross_loans_annual, date_annual, "Gross Loans")
                                        Loans_loss_annual_df = financials_df(Loans_loss_annual, date_annual, "Allowance for Loan Losses")
                                        Net_Loan_annual_df = financials_df(Net_Loan_annual, date_annual, "Net Loans")
                                        Unearned_income_annual_df = financials_df(Unearned_income_annual, date_annual, "Unearned Income")
                                        Net_goodwill_annual_df = financials_df(Net_goodwill_annual, date_annual, "Net Goodwill")
                                        Intangible_assets_annual_df = financials_df(Intangible_assets_annual, date_annual, "Intangible Assets")
                                        Other_lt_assets_annual_df = financials_df(Other_lt_assets_annual, date_annual, "Other longterm Assets")
                                        Total_assets_annual_df = financials_df(Total_assets_annual, date_annual, "Total Assets")
                                        Deposits_annual_df = financials_df(Deposits_annual, date_annual, "Total Deposits")
                                        Short_term_debt_annual_df = financials_df(Short_term_debt_annual, date_annual, "Short-Term Debt")
                                        LongTerm_debt_annual_df = financials_df(LongTerm_debt_annual, date_annual, "Long-Term Debt")
                                        Other_longterm_liabilities_annual_df = financials_df(Other_longterm_liabilities_annual, date_annual, "Other Long-Term Liabilities")
                                        Retained_earnings_annual_df = financials_df(Retained_earnings_annual, date_annual, "Retained Earnings")
                                        Total_liabilities_annual_df = financials_df(Total_liabilities_annual, date_annual, "Total Liabilities")
                                        Total_Equity_annual_df = financials_df(Total_Equity_annual, date_annual, "Total Equity")

                                        ################################ Quarter###############################

                                        cash_and_equiv_quarterly_Balance_Sheet_df = financials_df(cash_and_equiv_quarterly_Balance_Sheet, date_quarter, "Cash & Equivalents")
                                        Total_investments_quarterly_Balance_Sheet_df = financials_df(Total_investments_quarterly_Balance_Sheet, date_quarter, "Total Investments")
                                        Gross_loans_quarter_df = financials_df(Gross_loans_quarter, date_quarter, "Gross Loans")
                                        Loans_loss_quarter_df = financials_df(Loans_loss_quarter, date_quarter, "Allowance for Loan Losses")
                                        Net_Loan_quarter_df = financials_df(Net_Loan_quarter, date_quarter, "Net Loans")
                                        Unearned_income_quarter_df = financials_df(Unearned_income_quarter, date_quarter, "Unearned Income")
                                        Net_goodwill_quarter_df = financials_df(Net_goodwill_quarter, date_quarter, "Net Goodwill")
                                        Intangible_assets_quarter_df = financials_df(Intangible_assets_quarter, date_quarter, "Intangible Assets")
                                        Other_lt_assets_quarter_df = financials_df(Other_lt_assets_quarter, date_quarter, "Other longterm Assets")
                                        Total_assets_quarter_df = financials_df(Total_assets_quarter, date_quarter, "Total Assets")
                                        Deposits_quarter_df = financials_df(Deposits_quarter, date_quarter, "Total Deposits")
                                        Short_term_debt_quarter_df = financials_df(Short_term_debt_quarter10_unpacked, date_quarter, "Short-Term Debt")
                                        LongTerm_debt_quarter_df = financials_df(LongTerm_debt_quarter10_unpacked, date_quarter, "Long-Term Debt")
                                        Other_longterm_liabilities_quarter_df = financials_df(Other_longterm_liabilities_quarter10_unpacked, date_quarter, "Other Long-Term Liabilities")
                                        Retained_earnings_quarter_df = financials_df(Retained_earnings_quarter, date_quarter, "Retained Earnings")
                                        Total_liabilities_quarter_df = financials_df(Total_liabilities_quarter10_unpacked, date_quarter, "Total Liabilities")
                                        Total_Equity_quarter_df = financials_df(Total_Equity_quarter10_unpacked, date_quarter, "Total Equity")


                                        merged_df = pd.concat([cash_und_cash_investments_df,Total_investments_annual_df,Gross_loans_annual_df,
                                                            Loans_loss_annual_df,Net_Loan_annual_df,Unearned_income_annual_df,
                                                            Net_goodwill_annual_df,Intangible_assets_annual_df,
                                                            Other_lt_assets_annual_df,Total_assets_annual_df,Deposits_annual_df,
                                                            Short_term_debt_annual_df,LongTerm_debt_annual_df,
                                                            Other_longterm_liabilities_annual_df,Retained_earnings_annual_df,
                                                            Total_liabilities_annual_df,Total_Equity_annual_df
                                                            ])           
                                                  
                                                  ################################ Quarter###############################

                                        merged_df_quarter = pd.concat([cash_and_equiv_quarterly_Balance_Sheet_df,Total_investments_quarterly_Balance_Sheet_df,
                                                                      Gross_loans_quarter_df,Loans_loss_quarter_df,Net_Loan_quarter_df,Unearned_income_quarter_df,
                                                                      Net_goodwill_quarter_df,Intangible_assets_quarter_df,
                                                                      Other_lt_assets_quarter_df,Total_assets_quarter_df,Deposits_quarter_df,
                                                                      Short_term_debt_quarter_df,LongTerm_debt_quarter_df,
                                                                      Other_longterm_liabilities_quarter_df,
                                                                      Retained_earnings_quarter_df,Total_liabilities_quarter_df,Total_Equity_quarter_df])          

                                        st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'})                                             .set_table_styles(
                                             [{'selector': 'thead th', 'props': [('color', 'black')]}],  # Set font color of header (first row) to blue
                                             axis=1
                                        ))

                                        pass
                                   except KeyError:
                                        try:
                                             if f'{ticker}_cash_and_cash_investments_annual' in st.session_state:
                                                  cash_und_cash_investments_annual = st.session_state[f'{ticker}_cash_and_cash_investments_annual']
                                                  st_investments_annual = st.session_state[f'{ticker}_st_investments_annual']
                                                  Inventories_annual = st.session_state[f'{ticker}_Inventories_annual']
                                                  Total_current_assets_annual = st.session_state[f'{ticker}_Total_current_assets_annual']
                                                  Income_Tax_payable_annual = st.session_state[f'{ticker}_Income_Tax_payable_annual']
                                                  Total_current_liabilities_annual = st.session_state[f'{ticker}_Total_current_liabilities_annual']
                                                  Intangible_assets_annual = st.session_state[f'{ticker}_Intangible_assets_annual']
                                                  Net_goodwill_annual = st.session_state[f'{ticker}_Net_goodwill_annual']
                                                  Other_lt_assets_annual = st.session_state[f'{ticker}_Other_lt_assets_annual']
                                                  Total_assets_annual = st.session_state[f'{ticker}_Total_assets_annual']
                                                  Short_term_debt_annual = st.session_state[f'{ticker}_Short_term_debt_annual']
                                                  LongTerm_debt_annual = st.session_state[f'{ticker}_LongTerm_debt_annual']
                                                  Other_longterm_liabilities_annual = st.session_state[f'{ticker}_Other_longterm_liabilities_annual']
                                                  Retained_earnings_annual = st.session_state[f'{ticker}_Retained_earnings_annual']
                                                  Total_liabilities_annual = st.session_state[f'{ticker}_Total_liabilities_annual']
                                                  Total_Equity_annual = st.session_state[f'{ticker}_Total_Equity_annual']
                                                  ################################ Quarter###############################
                                                  cash_and_equiv_quarterly_Balance_Sheet = st.session_state[f'{ticker}_cash_and_equiv_quarterly_Balance_Sheet']
                                                  st_investments_quarterly_Balance_Sheet = st.session_state[f'{ticker}_st_investments_quarterly_Balance_Sheet']
                                                  Inventories_quarter = st.session_state[f'{ticker}_Inventories_quarter']
                                                  Total_current_assets_quarter = st.session_state[f'{ticker}_Total_current_assets_quarter']
                                                  Intangible_assets_quarter = st.session_state[f'{ticker}_Intangible_assets_quarter']
                                                  Net_goodwill_quarter = st.session_state[f'{ticker}_Net_goodwill_quarter']
                                                  Other_lt_assets_quarter = st.session_state[f'{ticker}_Other_lt_assets_quarter']
                                                  Total_assets_quarter = st.session_state[f'{ticker}_Total_assets_quarter']
                                                  Accounts_payable_quarter = st.session_state[f'{ticker}_Accounts_payable_quarter']
                                                  Current_accrued_liab_quarter = st.session_state[f'{ticker}_Current_accrued_liab_quarter']
                                                  Tax_payable_quarter = st.session_state[f'{ticker}_Tax_payable_quarter']
                                                  Other_current_liabilities_quarter10_unpacked = st.session_state[f'{ticker}_Other_current_liabilities_quarter']
                                                  Current_deferred_revenue_quarter = st.session_state[f'{ticker}_Current_deferred_revenue_quarter']
                                                  Total_current_liabilities_quarter10_unpacked = st.session_state[f'{ticker}_Total_current_liabilities_quarter']
                                                  Short_term_debt_quarter10_unpacked = st.session_state[f'{ticker}_Short_term_debt_quarter']
                                                  current_portion_of_lease_obligation_quarter  = st.session_state[f'{ticker}_current_portion_of_lease_obligation']
                                                  capital_leases_quarter  = st.session_state[f'{ticker}_capital_leases']
                                                  LongTerm_debt_quarter10_unpacked = st.session_state[f'{ticker}_LongTerm_debt_quarter']
                                                  Other_longterm_liabilities_quarter10_unpacked = st.session_state[f'{ticker}_Other_longterm_liabilities_quarter']
                                                  Retained_earnings_quarter = st.session_state[f'{ticker}_Retained_earnings_quarter']
                                                  Total_liabilities_quarter10_unpacked = st.session_state[f'{ticker}_Total_liabilities_quarter']
                                                  Total_Equity_quarter10_unpacked = st.session_state[f'{ticker}_Total_Equity_quarter']

                                             else:

                                                  cash_und_cash_investments_annual = annual_data['cash_and_equiv'][-10:]
                                                  st_investments_annual = annual_data['st_investments'][-10:]
                                                  Inventories_annual = annual_data['inventories'][-10:]
                                                  Total_current_assets_annual = annual_data['total_current_assets'][-10:]
                                                  Income_Tax_payable_annual = annual_data['tax_payable'][-10:]
                                                  Total_current_liabilities_annual = annual_data['total_current_liabilities'][-10:]
                                                  Intangible_assets_annual = annual_data['intangible_assets'][-10:]
                                                  Net_goodwill_annual = annual_data['goodwill'][-10:]
                                                  Other_lt_assets_annual =annual_data['other_lt_assets'][-10:]
                                                  Total_assets_annual = annual_data['total_assets'][-10:]
                                                  Short_term_debt_annual = annual_data['st_debt'][-10:]
                                                  LongTerm_debt_annual = annual_data['lt_debt'][-10:]
                                                  Other_longterm_liabilities_annual = annual_data['other_lt_liabilities'][-10:]
                                                  Retained_earnings_annual = annual_data['retained_earnings'][-10:]
                                                  Total_liabilities_annual = annual_data['total_liabilities'][-10:]
                                                  Total_Equity_annual = annual_data['total_equity'][-10:]
                                                  ################################ Quarter###############################
                                                  cash_and_equiv_quarterly_Balance_Sheet = quarterly_data['cash_and_equiv'][-10:]
                                                  st_investments_quarterly_Balance_Sheet = quarterly_data['st_investments'][-10:]
                                                  Inventories_quarter = quarterly_data['inventories'][-10:]
                                                  Total_current_assets_quarter = quarterly_data['total_current_assets'][-10:]
                                                  Intangible_assets_quarter= quarterly_data['intangible_assets'][-10:]
                                                  Net_goodwill_quarter= quarterly_data['goodwill'][-10:]
                                                  Other_lt_assets_quarter = quarterly_data['other_lt_assets'][-10:]
                                                  Total_assets_quarter = quarterly_data['total_assets'][-10:]
                                             # st_investments_quarterly_Balance_Sheet = quarterly_data['st_investments'][-10:]
                                                  Accounts_payable_quarter = quarterly_data['accounts_payable'][-10:]
                                                  Current_accrued_liab_quarter = quarterly_data['current_accrued_liabilities'][-10:]
                                                  Tax_payable_quarter = quarterly_data['tax_payable'][-10:]
                                                  Other_current_liabilities_quarter10_unpacked = quarterly_data['other_current_liabilities'][-10:]
                                                  Current_deferred_revenue_quarter = quarterly_data['current_deferred_revenue'][-10:]
                                                  Total_current_liabilities_quarter10_unpacked = quarterly_data['total_current_liabilities'][-10:]
                                                  Short_term_debt_quarter10_unpacked = quarterly_data['st_debt'][-10:]
                                                  current_portion_of_lease_obligation_quarter  = quarterly_data['current_capital_leases'][-10:]
                                                  capital_leases_quarter  = quarterly_data['noncurrent_capital_leases'][-10:]
                                                  LongTerm_debt_quarter10_unpacked = quarterly_data['lt_debt'][-10:]
                                                  Other_longterm_liabilities_quarter10_unpacked = quarterly_data['other_lt_liabilities'][-10:]
                                                  Retained_earnings_quarter = quarterly_data['retained_earnings'][-10:]
                                                  Total_liabilities_quarter10_unpacked = quarterly_data['total_liabilities'][-10:]
                                                  Total_Equity_quarter10_unpacked = quarterly_data['total_equity'][-10:]

                                                  # Store unpacked data in session state
                                                  st.session_state[f'{ticker}_cash_and_cash_investments_annual'] = cash_und_cash_investments_annual
                                                  st.session_state[f'{ticker}_st_investments_annual'] = st_investments_annual
                                                  st.session_state[f'{ticker}_Inventories_annual'] = Inventories_annual
                                                  st.session_state[f'{ticker}_Total_current_assets_annual'] = Total_current_assets_annual
                                                  st.session_state[f'{ticker}_Income_Tax_payable_annual'] = Income_Tax_payable_annual
                                                  st.session_state[f'{ticker}_Total_current_liabilities_annual'] = Total_current_liabilities_annual
                                                  st.session_state[f'{ticker}_Intangible_assets_annual'] = Intangible_assets_annual
                                                  st.session_state[f'{ticker}_Net_goodwill_annual'] = Net_goodwill_annual
                                                  st.session_state[f'{ticker}_Other_lt_assets_annual'] = Other_lt_assets_annual
                                                  st.session_state[f'{ticker}_Total_assets_annual'] = Total_assets_annual
                                                  st.session_state[f'{ticker}_Short_term_debt_annual'] = Short_term_debt_annual
                                                  st.session_state[f'{ticker}_LongTerm_debt_annual'] = LongTerm_debt_annual
                                                  st.session_state[f'{ticker}_Other_longterm_liabilities_annual'] = Other_longterm_liabilities_annual
                                                  st.session_state[f'{ticker}_Retained_earnings_annual'] = Retained_earnings_annual
                                                  st.session_state[f'{ticker}_Total_liabilities_annual'] = Total_liabilities_annual
                                                  st.session_state[f'{ticker}_Total_Equity_annual'] = Total_Equity_annual
                                                  ################################ Quarter###############################

                                                  #Store unpacked data in session state
                                                  st.session_state[f'{ticker}_cash_and_equiv_quarterly_Balance_Sheet'] = cash_and_equiv_quarterly_Balance_Sheet
                                                  st.session_state[f'{ticker}_st_investments_quarterly_Balance_Sheet'] = st_investments_quarterly_Balance_Sheet
                                                  st.session_state[f'{ticker}_Inventories_quarter'] = Inventories_quarter
                                                  st.session_state[f'{ticker}_Total_current_assets_quarter'] = Total_current_assets_quarter
                                                  st.session_state[f'{ticker}_Intangible_assets_quarter'] = Intangible_assets_quarter
                                                  st.session_state[f'{ticker}_Net_goodwill_quarter'] = Net_goodwill_quarter
                                                  st.session_state[f'{ticker}_Other_lt_assets_quarter'] = Other_lt_assets_quarter
                                                  st.session_state[f'{ticker}_Total_assets_quarter'] = Total_assets_quarter
                                                  st.session_state[f'{ticker}_Accounts_payable_quarter'] = Accounts_payable_quarter
                                                  st.session_state[f'{ticker}_Current_accrued_liab_quarter'] = Current_accrued_liab_quarter
                                                  st.session_state[f'{ticker}_Tax_payable_quarter'] = Tax_payable_quarter
                                                  st.session_state[f'{ticker}_Other_current_liabilities_quarter'] = Other_current_liabilities_quarter10_unpacked

                                                  st.session_state[f'{ticker}_Current_deferred_revenue_quarter'] = Current_deferred_revenue_quarter
                                                  st.session_state[f'{ticker}_Total_current_liabilities_quarter'] = Total_current_liabilities_quarter10_unpacked
                                                  st.session_state[f'{ticker}_Short_term_debt_quarter'] = Short_term_debt_quarter10_unpacked
                                                  st.session_state[f'{ticker}_current_portion_of_lease_obligation'] = current_portion_of_lease_obligation_quarter 
                                                  st.session_state[f'{ticker}_capital_leases'] = capital_leases_quarter 
                                                  st.session_state[f'{ticker}_LongTerm_debt_quarter'] = LongTerm_debt_quarter10_unpacked
                                                  st.session_state[f'{ticker}_Other_longterm_liabilities_quarter'] = Other_longterm_liabilities_quarter10_unpacked
                                                  st.session_state[f'{ticker}_Retained_earnings_quarter'] = Retained_earnings_quarter
                                                  st.session_state[f'{ticker}_Total_liabilities_quarter'] = Total_liabilities_quarter10_unpacked
                                                  st.session_state[f'{ticker}_Total_Equity_quarter'] = Total_Equity_quarter10_unpacked


                                             index = range(len(date_annual))
                                             df = pd.DataFrame({'Period End Date': date_annual,
                                                                           'Cash and Equivalents': cash_und_cash_investments_annual,
                                                                           'Short term Investments': st_investments_annual
                                                                           }, index=index)

                                             if 'Short term Investments' in df.columns:
                                                  df['Total Cash'] = df['Cash and Equivalents'] + df['Short term Investments']
                                             else:
                                                  df['Total Cash'] = df['Cash and Equivalents']
                                             total = df.T

                                             total.columns = total.iloc[0]  
                                             total = total[1:]  # Remove the first row

                                             #total_annual = total.applymap(lambda x: "{:.2f}B".format(x / 1e9) if abs(x) >= 1e9 else "{:,.1f}M".format(x / 1e6))
                                             total_annual = total.apply(lambda col: col.map(lambda x: "{:.2f}B".format(x / 1e9) if abs(x) >= 1e9 else "{:,.1f}M".format(x / 1e6)))


                                             ################################ Quarter###############################



                                             index = range(len(date_list_quarter))
                                             df = pd.DataFrame({'Period End Date': date_list_quarter,
                                                                 'Cash and Equivalents': cash_and_equiv_quarterly_Balance_Sheet,
                                                                 'Short term Investments': st_investments_quarterly_Balance_Sheet
                                                                      }, index=index)




                                             if 'Short term Investments' in df.columns:
                                                  df['Total Cash'] = df['Cash and Equivalents'] + df['Short term Investments']
                                             else:
                                                  df['Total Cash'] = df['Cash and Equivalents']
                                                                 
                                             total = df.T
                                                                 


                                             total.columns = total.iloc[0]  # Use the first row as column names
                                             total = total[1:]  # Remove the first row


                                             #total_quarter = total.applymap(lambda x: "{:.2f}B".format(x / 1e9) if abs(x) >= 1e9 else "{:,.1f}M".format(x / 1e6))
                                             total_quarter = total.apply(lambda col: col.map(lambda x: "{:.2f}B".format(x / 1e9) if abs(x) >= 1e9 else "{:,.1f}M".format(x / 1e6)))



          
                                                            
                                             cash_und_cash_investments_annual_df = financials_df(cash_und_cash_investments_annual, date_annual, "Cash & Equivalents")
                                             st_investments_annual_df = financials_df(st_investments_annual, date_annual, "Short-Term Investments")
                                             Inventories_annual_df = financials_df(Inventories_annual, date_annual, "Inventories")
                                             Total_current_assets_annual_df = financials_df(Total_current_assets_annual, date_annual, "Total Current Assets")
                                             Income_Tax_payable_annual_df = financials_df(Income_Tax_payable_annual, date_annual, "Income Tax Payable")
                                             Total_current_liabilities_annual_df = financials_df(Total_current_liabilities_annual, date_annual, "Total Current Liabilities")
                                             Intangible_assets_annual_df = financials_df(Intangible_assets_annual, date_annual, "Intangible Assets")
                                             Net_goodwill_annual_df = financials_df(Net_goodwill_annual, date_annual, "Net Goodwill")
                                             Other_lt_assets_annual_df = financials_df(Other_lt_assets_annual, date_annual, "Other longterm Assets")
                                             Total_assets_annual_df = financials_df(Total_assets_annual, date_annual, "Total Assets")
                                             Short_term_debt_annual_df = financials_df(Short_term_debt_annual, date_annual, "Short-Term Debt")
                                             LongTerm_debt_annual_df = financials_df(LongTerm_debt_annual, date_annual, "Long-Term Debt")
                                             Other_longterm_liabilities_annual_df = financials_df(Other_longterm_liabilities_annual, date_annual, "Other Long-Term Liabilities")
                                             Retained_earnings_annual_df = financials_df(Retained_earnings_annual, date_annual, "Retained Earnings")
                                             Total_liabilities_annual_df = financials_df(Total_liabilities_annual, date_annual, "Total Liabilities")
                                             Total_Equity_annual_df = financials_df(Total_Equity_annual, date_annual, "Total Equity")

                                             ################################ Quarter###############################

                                             cash_and_equiv_quarterly_Balance_Sheet_df = financials_df(cash_and_equiv_quarterly_Balance_Sheet, date_quarter, "Cash & Equivalents")
                                             st_investments_quarterly_Balance_Sheet_df = financials_df(st_investments_quarterly_Balance_Sheet, date_quarter, "Short-Term Investments")
                                             Inventories_quarter_df = financials_df(Inventories_quarter, date_quarter, "Inventories")
                                             Total_current_assets_quarter_df = financials_df(Total_current_assets_quarter, date_quarter, "Total Current Assets")
                                             Intangible_assets_quarter_df = financials_df(Intangible_assets_quarter, date_quarter, "Intangible Assets")
                                             Net_goodwill_quarter_df = financials_df(Net_goodwill_quarter, date_quarter, "Net Goodwill")
                                             Other_lt_assets_quarter_df = financials_df(Other_lt_assets_quarter, date_quarter, "Other longterm Assets")
                                             Total_assets_quarter_df = financials_df(Total_assets_quarter, date_quarter, "Total Assets")
                                             Accounts_payable_quarter_df = financials_df(Accounts_payable_quarter, date_quarter, "Accounts Payable")
                                             Current_accrued_liab_quarter_df = financials_df(Current_accrued_liab_quarter, date_quarter, "Current Accrued Liabilities")
                                             Tax_payable_quarter_df = financials_df(Tax_payable_quarter, date_quarter, "Income Tax Payable")
                                             Other_current_liabilities_quarter_df = financials_df(Other_current_liabilities_quarter10_unpacked, date_quarter, "Other Current Liabilities")
                                             Current_deferred_revenue_quarter_df = financials_df(Current_deferred_revenue_quarter, date_quarter, "Current Deferred Revenue")
                                             Total_current_liabilities_quarter_df = financials_df(Total_current_liabilities_quarter10_unpacked, date_quarter, "Total Current Liabilities")
                                             Short_term_debt_quarter_df = financials_df(Short_term_debt_quarter10_unpacked, date_quarter, "Short-Term Debt")
                                             current_portion_of_lease_obligation_quarter_df = financials_df(current_portion_of_lease_obligation_quarter , date_quarter, "Current Portion of Lease Obligation")
                                             capital_leases_quarter_df = financials_df(capital_leases_quarter , date_quarter, "Capital Leases (Noncurrent)")
                                             LongTerm_debt_quarter_df = financials_df(LongTerm_debt_quarter10_unpacked, date_quarter, "Long-Term Debt")
                                             Retained_earnings_quarter_df = financials_df(Retained_earnings_quarter, date_quarter, "Retained Earnings")
                                             Other_longterm_liabilities_quarter_df = financials_df(Other_longterm_liabilities_quarter10_unpacked, date_quarter, "Other Long-Term Liabilities")
                                             Total_liabilities_quarter_df = financials_df(Total_liabilities_quarter10_unpacked, date_quarter, "Total Liabilities")
                                             Total_Equity_quarter_df = financials_df(Total_Equity_quarter10_unpacked, date_quarter, "Total Equity")


               
                                             merged_df =pd.concat([total_annual,Inventories_annual_df,Total_current_assets_annual_df,
                                                                 Net_goodwill_annual_df,Intangible_assets_annual_df,Other_lt_assets_annual_df,Total_assets_annual_df,
                                                                 Short_term_debt_annual_df,Total_current_liabilities_annual_df,LongTerm_debt_annual_df,
                                                                 Other_longterm_liabilities_annual_df,Retained_earnings_annual_df,Total_liabilities_annual_df,Total_Equity_annual_df])           

                                             ############################### Quarter###############################
                                             merged_df_quarter = pd.concat([total_quarter
                                                                           ,Inventories_quarter_df,Total_current_assets_quarter_df,Net_goodwill_quarter_df,
                                                                           Intangible_assets_quarter_df,
                                                                           Other_lt_assets_quarter_df,Total_assets_quarter_df,Short_term_debt_quarter_df,
                                                                           Total_current_liabilities_quarter_df,LongTerm_debt_quarter_df,Other_longterm_liabilities_quarter_df,
                                                                           Retained_earnings_quarter_df,Total_liabilities_quarter_df,Total_Equity_quarter_df]) 


                                             st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'})                                             .set_table_styles(
                                             [{'selector': 'thead th', 'props': [('color', 'black')]}],  # Set font color of header (first row) to blue
                                             axis=1
                                        ))

                                             pass    
                                                  #else:      
                                        except KeyError:


                                             if f'{ticker}_Total_investments' in st.session_state:
                                                  Total_investments = st.session_state[f'{ticker}_Total_investments']
                                                  cash_und_cash_investments = st.session_state[f'{ticker}_cash_and_cash_investments']
                                                  Intangible_assets_annual = st.session_state[f'{ticker}_Intangible_assets_annual']
                                                  Net_goodwill_annual = st.session_state[f'{ticker}_Net_goodwill_annual']
                                                  Other_longterm_assets_annual = st.session_state[f'{ticker}_Other_longterm_assets_annual']
                                                  Total_assets_annual = st.session_state[f'{ticker}_Total_assets_annual']
                                                  Unearned_Premiums_annual = st.session_state[f'{ticker}_Unearned_Premiums_annual']
                                                  Short_term_debt_annual = st.session_state[f'{ticker}_Short_term_debt_annual']
                                                  LongTerm_debt_annual = st.session_state[f'{ticker}_LongTerm_debt_annual']
                                                  Other_longterm_liabilities_annual = st.session_state[f'{ticker}_Other_longterm_liabilities_annual']
                                                  Total_liabilities_annual = st.session_state[f'{ticker}_Total_liabilities_annual']
                                                  Retained_earnings_annual = st.session_state[f'{ticker}_Retained_earnings_annual']
                                                  Total_Equity_annual = st.session_state[f'{ticker}_Total_Equity_annual']
                                                  ############################### Quarter###############################
                                                  Total_investments_quarter  = st.session_state[f'{ticker}_Total_investments_quarterly']
                                                  cash_and_equiv_quarterly = st.session_state[f'{ticker}_cash_and_equiv_quarterly']
                                                  Net_goodwill_quarter = st.session_state[f'{ticker}_Net_goodwill_quarter']
                                                  Intangible_assets_quarter = st.session_state[f'{ticker}_Intangible_assets_quarter']
                                                  Other_longterm_assets_quarter = st.session_state[f'{ticker}_Other_longterm_assets_quarter']
                                                  Total_assets_quarter = st.session_state[f'{ticker}_Total_assets_quarter']
                                                  Unearned_Premiums_quarter = st.session_state[f'{ticker}_Unearned_Premiums_quarter']
                                                  Short_term_debt_quarter10_unpacked = st.session_state[f'{ticker}_Short_term_debt_quarter']
                                                  LongTerm_debt_quarter10_unpacked = st.session_state[f'{ticker}_LongTerm_debt_quarter']
                                                  Other_longterm_liabilities_quarter = st.session_state[f'{ticker}_Other_longterm_liabilities_quarter']
                                                  Total_liabilities_quarter10_unpacked = st.session_state[f'{ticker}_Total_liabilities_quarter']
                                                  Total_Equity_quarter10_unpacked = st.session_state[f'{ticker}_Total_Equity_quarter']
                                                  Retained_earnings_quarter = st.session_state[f'{ticker}_Retained_earnings_quarter']

                                             else:    

                                                  Total_investments = annual_data['total_investments'][-10:]
                                                  cash_und_cash_investments = annual_data['cash_and_equiv'][-10:]
                                                  Intangible_assets_annual = annual_data['intangible_assets'][-10:]
                                                  Net_goodwill_annual = annual_data['goodwill'][-10:]
                                                  Other_longterm_assets_annual = annual_data['other_lt_assets'][-10:]
                                                  Total_assets_annual = annual_data['total_assets'][-10:]
                                                  Unearned_Premiums_annual = annual_data['unearned_premiums'][-10:]
                                                  Short_term_debt_annual = annual_data['st_debt'][-10:]
                                                  LongTerm_debt_annual = annual_data['lt_debt'][-10:]
                                                  Other_longterm_liabilities_annual = annual_data['other_lt_liabilities'][-10:]
                                                  Total_liabilities_annual = annual_data['total_liabilities'][-10:]
                                                  Retained_earnings_annual =annual_data['retained_earnings'][-10:]
                                                  Total_Equity_annual = annual_data['total_equity'][-10:]

                                                  ############################### Quarter###############################

                                                  Total_investments_quarter  = quarterly_data['total_investments'][-10:]
                                                  cash_and_equiv_quarterly = quarterly_data['cash_and_equiv'][-10:]
                                                  Net_goodwill_quarter= quarterly_data['goodwill'][-10:]
                                                  Intangible_assets_quarter= quarterly_data['intangible_assets'][-10:]
                                                  Other_longterm_assets_quarter = quarterly_data['other_lt_assets'][-10:]
                                                  Total_assets_quarter = quarterly_data['total_assets'][-10:]
                                                  Unearned_Premiums_quarter  = quarterly_data['unearned_premiums'][-10:]
                                                  Short_term_debt_quarter10_unpacked = quarterly_data['st_debt'][-10:]
                                                  LongTerm_debt_quarter10_unpacked = quarterly_data['lt_debt'][-10:]
                                                  Other_longterm_liabilities_quarter = quarterly_data['other_lt_liabilities'][-10:]
                                                  Total_liabilities_quarter10_unpacked = quarterly_data['total_liabilities'][-10:]
                                                  Total_Equity_quarter10_unpacked = quarterly_data['total_equity'][-10:]
                                                  Retained_earnings_quarter  =quarterly_data['retained_earnings'][-10:]


                                                  # Store unpacked data in session state
                                                  st.session_state[f'{ticker}_Total_investments'] = Total_investments
                                                  st.session_state[f'{ticker}_cash_and_cash_investments'] = cash_und_cash_investments
                                                  st.session_state[f'{ticker}_Intangible_assets_annual'] = Intangible_assets_annual
                                                  st.session_state[f'{ticker}_Net_goodwill_annual'] = Net_goodwill_annual
                                                  st.session_state[f'{ticker}_Other_longterm_assets_annual'] = Other_longterm_assets_annual
                                                  st.session_state[f'{ticker}_Total_assets_annual'] = Total_assets_annual
                                                  st.session_state[f'{ticker}_Unearned_Premiums_annual'] = Unearned_Premiums_annual
                                                  st.session_state[f'{ticker}_Short_term_debt_annual'] = Short_term_debt_annual
                                                  st.session_state[f'{ticker}_LongTerm_debt_annual'] = LongTerm_debt_annual
                                                  st.session_state[f'{ticker}_Other_longterm_liabilities_annual'] = Other_longterm_liabilities_annual
                                                  st.session_state[f'{ticker}_Total_liabilities_annual'] = Total_liabilities_annual
                                                  st.session_state[f'{ticker}_Retained_earnings_annual'] = Retained_earnings_annual
                                                  st.session_state[f'{ticker}_Total_Equity_annual'] = Total_Equity_annual
                                                  ############################### Quarter###############################

                                                  st.session_state[f'{ticker}_Total_investments_quarterly'] = Total_investments_quarter 
                                                  st.session_state[f'{ticker}_cash_and_equiv_quarterly'] = cash_and_equiv_quarterly
                                                  st.session_state[f'{ticker}_Net_goodwill_quarter'] = Net_goodwill_quarter
                                                  st.session_state[f'{ticker}_Intangible_assets_quarter'] = Intangible_assets_quarter
                                                  st.session_state[f'{ticker}_Other_longterm_assets_quarter'] = Other_longterm_assets_quarter
                                                  st.session_state[f'{ticker}_Total_assets_quarter'] = Total_assets_quarter
                                                  st.session_state[f'{ticker}_Unearned_Premiums_quarter'] = Unearned_Premiums_quarter
                                                  st.session_state[f'{ticker}_Short_term_debt_quarter'] = Short_term_debt_quarter10_unpacked
                                                  st.session_state[f'{ticker}_LongTerm_debt_quarter'] = LongTerm_debt_quarter10_unpacked
                                                  st.session_state[f'{ticker}_Other_longterm_liabilities_quarter'] = Other_longterm_liabilities_quarter
                                                  st.session_state[f'{ticker}_Total_liabilities_quarter'] = Total_liabilities_quarter10_unpacked
                                                  st.session_state[f'{ticker}_Total_Equity_quarter'] = Total_Equity_quarter10_unpacked
                                                  st.session_state[f'{ticker}_Retained_earnings_quarter'] = Retained_earnings_quarter



                                             Total_investments_annual_df = financials_df(Total_investments, date_annual, "Other Investments")
                                             cash_und_cash_investments_annual_df = financials_df(cash_und_cash_investments, date_annual, "Cash & Equivalents")
                                             Intangible_assets_annual_df = financials_df(Intangible_assets_annual, date_annual, "Intangible Assets")
                                             Net_goodwill_annual_df = financials_df(Net_goodwill_annual, date_annual, "Net Goodwill")
                                             Other_longterm_assets_annual_df = financials_df(Other_longterm_assets_annual, date_annual, "Other Longterm Assets")
                                             Total_assets_annual_df = financials_df(Total_assets_annual, date_annual, "Total Assets")
                                             Unearned_Premiums_annual_df=financials_df(Unearned_Premiums_annual, date_annual, "Unearned Premiums")
                                             Retained_earnings_annual_df=financials_df(Retained_earnings_annual, date_annual, "Retained Earnings")
                                             Short_term_debt_annual_df = financials_df(Short_term_debt_annual, date_annual, "Short-Term Debt")
                                             LongTerm_debt_annual_df = financials_df(LongTerm_debt_annual, date_annual, "Long-Term Debt")
                                             Other_longterm_liabilities_annual_df = financials_df(Other_longterm_liabilities_annual, date_annual, "Other Long-Term Liabilities")
                                             Total_liabilities_annual_df = financials_df(Total_liabilities_annual, date_annual, "Total Liabilities")
                                             Total_Equity_annual_df = financials_df(Total_Equity_annual, date_annual, "Total Equity")
                                             ############################### Quarter###############################
                                             Total_investments_quarter_df = financials_df(Total_investments_quarter , date_quarter, "Other Investments")
                                             cash_and_equiv_quarterly_df = financials_df(cash_and_equiv_quarterly, date_quarter, "Cash & Equivalents")
                                             Net_goodwill_quarter_df = financials_df(Net_goodwill_quarter, date_quarter, "Net Goodwill")
                                             Intangible_assets_quarter_df = financials_df(Intangible_assets_quarter, date_quarter, "Intangible Assets")
                                             Other_longterm_assets_quarter_df = financials_df(Other_longterm_assets_quarter , date_quarter, "Other Longterm Assets")
                                             Total_assets_quarter_df = financials_df(Total_assets_quarter, date_quarter, "Total Assets")
                                             Unearned_Premiums_quarter_df=financials_df(Unearned_Premiums_quarter , date_quarter, "Unearned Premiums")
                                             Short_term_debt_quarter_df = financials_df(Short_term_debt_quarter10_unpacked, date_quarter, "Short-Term Debt")
                                             LongTerm_debt_quarter_df = financials_df(LongTerm_debt_quarter10_unpacked, date_quarter, "Long-Term Debt")
                                             Other_longterm_liabilities_quarter_df = financials_df(Other_longterm_liabilities_quarter, date_quarter, "Other Long-Term Liabilities")
                                             Total_liabilities_quarter_df = financials_df(Total_liabilities_quarter10_unpacked, date_quarter, "Total Liabilities")
                                             Retained_earnings_quarter_df=financials_df(Retained_earnings_quarter , date_quarter, "Retained Earnings")
                                             Total_Equity_quarter_df = financials_df(Total_Equity_quarter10_unpacked, date_quarter, "Total Equity")

                                                                      

                                             merged_df = pd.concat([Total_investments_annual_df,cash_und_cash_investments_annual_df,Net_goodwill_annual_df,
                                                                 Intangible_assets_annual_df,Other_longterm_assets_annual_df,
                                                                 Total_assets_annual_df,Unearned_Premiums_annual_df,Short_term_debt_annual_df,
                                                                 LongTerm_debt_annual_df,Other_longterm_liabilities_annual_df,
                                                                 Total_liabilities_annual_df,Retained_earnings_annual_df,Total_Equity_annual_df
                                                                 ])           
                                                                                               
                                             ############################### Quarter###############################  
                                             merged_df_quarter = pd.concat([Total_investments_quarter_df,cash_and_equiv_quarterly_df,Net_goodwill_quarter_df,Intangible_assets_quarter_df,
                                                                           Other_longterm_assets_quarter_df,Total_assets_quarter_df,
                                                                           Unearned_Premiums_quarter_df,Short_term_debt_quarter_df,LongTerm_debt_quarter_df,
                                                                           Other_longterm_liabilities_quarter_df,Total_liabilities_quarter_df,Retained_earnings_quarter_df,
                                                                           Total_Equity_quarter_df]) 
                                   
                                                            
                                             st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'})                                             .set_table_styles(
                                             [{'selector': 'thead th', 'props': [('color', 'black')]}],  # Set font color of header (first row) to blue
                                             axis=1
                                        ))




                              with Quarterly:
                                   st.table(merged_df_quarter.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'})                                             .set_table_styles(
                                             [{'selector': 'thead th', 'props': [('color', 'black')]}],  # Set font color of header (first row) to blue
                                             axis=1
                                        ))



                         with Cash_Flow:
                              Annual,Quarterly = st.tabs(["Annual","Quarterly"])
                              date_annual = annual_data['period_end_date'][-10:]
                              date_quarter = quarterly_data['period_end_date'][-10:]
          
                              
                              with Annual:

                                   index = range(len(date_list_annual))
                                   FFO = pd.DataFrame({'Period End Date': date_list_annual,
                                                                      'Operating Cash Flow': Net_Operating_CashFlow_annual_10_unpacked,
                                                                      'Changes In Working Capital': Changes_in_working_capital_annual_10_unpacked
                                                                      }, index=index)
                                   df = pd.DataFrame(FFO)

                                   df["Funds from Operations"] = df["Operating Cash Flow"] + df["Changes In Working Capital"]
                                        
                                   total = df.T
                                   total.columns = total.iloc[0]  # Use the first row as column names
                                   total = total[1:]  

                                   #total_annual = total.applymap(lambda x: "{:.2f}B".format(x / 1e9) if abs(x)>= 1e9 else "{:,.1f}M".format(x / 1e6))
                                   total_annual = total.apply(lambda col: col.map(lambda x: "{:.2f}B".format(x / 1e9) if abs(x) >= 1e9 else "{:,.1f}M".format(x / 1e6)))



                                   Changes_in_working_capital_annual_df = financials_df(Changes_in_working_capital_annual_10_unpacked, date_annual, "Changes in Working Capital")
                                   Capex_annual_df = financials_df(Capex_annual_10_unpacked, date_annual, "Capital Expenditure")
                                   Purchase_of_Investment_annual_df = financials_df(Purchase_of_Investment_annual_10_unpacked, date_annual, "Purchase of Investments")
                                   Sale_maturity_of_Investments_annual_df = financials_df(Sale_maturity_of_Investments_annual_10_unpacked, date_annual, "Sale/Maturity of Investments")
                                   Net_investing_CashFlow_annual_df = financials_df(Net_investing_CashFlow_annual_10_unpacked, date_annual, "Net Investing Cash Flow")
                                   Insurance_Reduction_of_DebtNet_annual_df = financials_df(Insurance_Reduction_of_DebtNet_annual_10_unpacked, date_annual, "Issuance/Reduction of Net Debt")
                                   Debt_issued_annual_df = financials_df(Debt_issued_annual_10_unpacked, date_annual, "Longterm Debt Issued")
                                   Debt_repaid_annual_df = financials_df(Debt_repaid_annual_10_unpacked, date_annual, "Longterm Debt Repaid")
                                   Stock_issued_of_common_Preferred_stock_annual_df  = financials_df(Stock_issued_of_common_Preferred_stock_annual_10_unpacked, date_annual, "Common Stock Repurchased")
                                   Net_Assets_from_Acquisitions_annual_df = financials_df(Net_Assets_from_Acquisitions_annual_10_unpacked, date_annual, "Acquisitions, net")
                                   StockBased_Compansation_annual_df= financials_df(StockBased_Compansation_annual_10_unpacked, date_annual, "Stock Based Compensation ")                       
                                   Repurchase_of_common_Preferred_stock_annual_df = financials_df(Repurchase_of_common_Preferred_stock_annual_10_unpacked, date_annual, "Repurchase Comm. & Pref. Stks")
                                   Cash_Dividends_paid_Total_annual_df = financials_df(Cash_Dividends_paid_Total_annual_10_unpacked, date_annual, "Cash Dividends Paid")
                                   Net_Financing_cashFlow_annual_df = financials_df(Net_Financing_cashFlow_annual_10_unpacked, date_annual, "Net Financing Cash Flow")
                                   Net_change_in_cash_annual_df = financials_df(Net_change_in_cash_annual_10_unpacked, date_annual, "Net Change in Cash")
                                   
                                   Free_cash_flow_annual_df = financials_df(FCF_annual_ten_unpacked, date_annual, "Free Cash Flow")




                                   merged_df = pd.concat([total_annual,Capex_annual_df,Net_Assets_from_Acquisitions_annual_df,
                                                       Purchase_of_Investment_annual_df,Sale_maturity_of_Investments_annual_df,Net_investing_CashFlow_annual_df,
                                                       Debt_issued_annual_df,
                                                       Debt_repaid_annual_df,
                                                       Stock_issued_of_common_Preferred_stock_annual_df,Insurance_Reduction_of_DebtNet_annual_df,
                                                       StockBased_Compansation_annual_df,Cash_Dividends_paid_Total_annual_df,
                                                       Repurchase_of_common_Preferred_stock_annual_df,Net_Financing_cashFlow_annual_df,
                                                       Net_change_in_cash_annual_df,Free_cash_flow_annual_df]) 

                                   st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'}).set_table_styles(
                                                       [{'selector': 'thead th', 'props': [('color', 'black')]}],  # Set font color of header (first row) to blue
                                                       axis=1
                                                  ))
                             


                                   with Quarterly:

                                   
                                        index = range(len(date_quarter))
                                        FFO = pd.DataFrame({'Period End Date': date_quarter,
                                                                      'Operating Cash Flow': Net_Operating_CashFlow_quarter_10_unpacked ,
                                                                      'Changes In Working Capital': changes_in_working_capital_quarter_10_unpacked 
                                                                      }, index=index)
                                             # Convert JSON data to a DataFrame
                                        df = pd.DataFrame(FFO)

                                        df["Funds from Operations"] = df["Operating Cash Flow"] + df["Changes In Working Capital"]
                                        
                                        total = df.T

                                        total.columns = total.iloc[0]  # Use the first row as column names
                                        total = total[1:]  # Remove the first row

                                        #total_quarter = total.applymap(lambda x: "{:.2f}B".format(x / 1e9) if abs(x) >= 1e9 else "{:,.1f}M".format(x / 1e6))
                                        total_quarter = total.apply(lambda col: col.map(lambda x: "{:.2f}B".format(x / 1e9) if abs(x) >= 1e9 else "{:,.1f}M".format(x / 1e6)))



                                        Net_Operating_CashFlow_quarter_df = financials_df(Net_Operating_CashFlow_quarter_10_unpacked , date_quarter, "Net Operating Cash Flow")
                                        changes_in_working_capital_quarter_df = financials_df(changes_in_working_capital_quarter_10_unpacked , date_quarter, "Changes in Working Capital")
                                        Capex_quarter_df = financials_df(Capex_quarter_10_unpacked , date_quarter, "Capital Expenditure")
                                        
                                        Purchase_of_Investment_quarter_df = financials_df(Purchase_of_Investment_quarter_10_unpacked , date_quarter, "Purchase of Investments")
                                        Sale_maturity_of_Investments_quarter_df = financials_df(Sale_maturity_of_Investments_quarter_10_unpacked , date_quarter, "Sale/Maturity of Investments")
                                        Net_investing_CashFlow_quarter_df = financials_df(Net_investing_CashFlow_quarter_10_unpacked , date_quarter, "Net Investing Cash Flow")
                                        Cash_Dividends_paid_Total_quarter_df = financials_df(Cash_Dividends_paid_Total_quarter_10_unpacked , date_quarter, "Cash Dividends Paid")
                                        
                                        Net_Assets_from_Acquisitions_quarter_df = financials_df(Net_Assets_from_Acquisitions_quarter_10_unpacked , date_quarter, "Acquisitions, net")
                                        Debt_issued_quarter_df = financials_df(Debt_issued_quarter_10_unpacked , date_quarter, "Longterm Debt Issued")
                                        Debt_repaid_quarter_df = financials_df(Debt_repaid_quarter_10_unpacked , date_quarter, "Longterm Debt Repaid")
                                        Stock_issued_of_common_Preferred_stock_quarter_df  = financials_df(Stock_issued_of_common_Preferred_stock_quarter_10_unpacked , date_quarter, "Common Stock Repurchased")
                                        StockBased_Compansation_quarter_df= financials_df(StockBased_Compansation_quarter_10_unpacked , date_quarter, "Stock Based Compensation ")

                                        Insurance_Reduction_of_DebtNet_quarter_df = financials_df(Insurance_Reduction_of_DebtNet_quarter_10_unpacked , date_quarter, "Issuance/Reduction of Net Debt")
                                        Repurchase_of_common_Preferred_stock_quarter_df = financials_df(Repurchase_of_common_Preferred_stock_quarter_10_unpacked , date_quarter, "Repurchase Comm. & Pref. Stks")
                                        Net_Financing_cashFlow_quarter_df = financials_df(Net_Financing_cashFlow_quarter_10_unpacked , date_quarter, "Net Financing Cash Flow")
                                        Net_change_in_cash_quarter_df = financials_df(Net_change_in_cash_quarter_10_unpacked , date_quarter, "Net Change in Cash")
                                        Free_cash_flow_quarter_df = financials_df(FCF_quarter_10_unpacked , date_quarter, "Free Cash Flow")


                                        merged_df = pd.concat([total_quarter,Capex_quarter_df,Net_Assets_from_Acquisitions_quarter_df,
                                                            Purchase_of_Investment_quarter_df,Sale_maturity_of_Investments_quarter_df,
                                                            Net_investing_CashFlow_quarter_df,
                                                            Debt_issued_quarter_df,
                                                            Debt_repaid_quarter_df,
                                                            Stock_issued_of_common_Preferred_stock_quarter_df,
                                                            Insurance_Reduction_of_DebtNet_quarter_df,
                                                            StockBased_Compansation_quarter_df,Cash_Dividends_paid_Total_quarter_df,
                                                            Repurchase_of_common_Preferred_stock_quarter_df,Net_Financing_cashFlow_quarter_df,
                                                            Net_change_in_cash_quarter_df,Free_cash_flow_quarter_df])           
                                        
                                        st.table(merged_df.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'})                                             .set_table_styles(
                                             [{'selector': 'thead th', 'props': [('color', 'black')]}],  # Set font color of header (first row) to blue
                                             axis=1
                                        ))



                    #................................................................................................................................................


               #def display_pillar_analysis():
               with st.container():
                    use_container_width=True
                    with Pillar_Analysis: 


                         if fcf_ttm == 0: 


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

                              
                              
                              
                    #--------------------------------------------------------------------------------------------------------------------------------
                         try:
                              revenue_annual_funf_Growth =(Revenue_annual_5_unpacked[-1]-Revenue_annual_5_unpacked[-5])/abs(Revenue_annual_5_unpacked[-5])*100

                              if Revenue_annual_5_unpacked[0] ==0:
                                   revenue_annual_funf_Growth=0

                         except (IndexError, ZeroDivisionError):
                              revenue_annual_funf_Growth = 0
                                                            
                    #-----------------------------------------------------------------------------------------------------------------------------

                         try:
                              FCF_funf_growth = ((FCF_annual_ten_unpacked[-1]-FCF_annual_ten_unpacked[-5])/abs(FCF_annual_ten_unpacked[-5]))*100

                              if FCF_annual_ten_unpacked[0] ==0:
                                   FCF_funf_growth=0
                         except (IndexError, ZeroDivisionError): 
                              FCF_funf_growth=0                                 
                    #----------------------------------------------------------------------------------------------------------------

                         try:

                              Shares_outstanding_funf_growth = ((shares_basic_annual_funf_unpacked[-1]-shares_basic_annual_funf_unpacked[-5])/abs(shares_basic_annual_funf_unpacked[-5]))*100

                              if shares_basic_annual_funf_unpacked[0] ==0:
                                   
                                   Shares_outstanding_funf_growth=0

                         except (IndexError, ZeroDivisionError): 
                              Shares_outstanding_funf_growth=0              
                                                            
                    #------------------------------------------------------------------------------------------------------------------

                         try:
                              netincome_annual_funf_growth_ = ((net_income_annual_funf_unpacked[-1] - net_income_annual_funf_unpacked[-5])/abs(net_income_annual_funf_unpacked[-5]))*100

                              if net_income_annual_funf_unpacked[0] ==0:
                                   netincome_annual_funf_growth =0
                         except Exception as e:  

                              netincome_annual_funf_growth_ =0    
                    #...............................................................................................................................


                    
                    #...........................................................................................................


                         Total_liabilities_quarter = quarterly_data['total_liabilities'][-1:]
                         Average_Total_liabilities_quarter = sum(Total_liabilities_quarter)/len(Total_liabilities_quarter)

                         if   Total_Debt_from_all_calc != 0:
                              try:
                                   Schuldentillgung = round(1 / (rounded_fcf_Annual_five / Total_Debt_from_all_calc), 2)
                                   Schuldentillgung = abs(Schuldentillgung)
                              except Exception as e:
                                   Schuldentillgung =0


                         elif Total_Debt_from_all_calc != 0:
                              if Average_Total_liabilities_quarter != 0: 
                                   Total_debt_= Average_Total_liabilities_quarter/1000000000
                                   Schuldentillgung=round(1/(rounded_fcf_Annual_five/Total_debt_),2)
                                   Schuldentillgung = abs(Schuldentillgung)

                              
                         else:
                              try:
                                   Total_liabilities_annual = annual_data['total_liabilities'][-1:]
                                   Total_liabilities_annual = sum(Total_liabilities_annual)/len(Total_liabilities_annual)
                                   Total_debt_= Total_liabilities_annual/1000000000
                                   Schuldentillgung=round(1/(rounded_fcf_Annual_five/Total_debt_),2)

                                   Schuldentillgung = abs(Schuldentillgung)
                              except Exception as e:
                                   Schuldentillgung = 0

                         try:
                              if float(KGV) > 23.00:
                                        pe = "🔴"  # Red X for KCV greater than 23
                              elif float(KGV) < 0.00:
                                        pe = "🔴"  # Red X for KCV smaller than 0
                              else:
                                        pe = "🟢"  # Green checkmark for KGV greater than or equal to 23      
                         except Exception as e:
                              pe = "🔴" 
                         
                         try:
                              if float(KCV) > 23.00:
                                        pcf = "🔴"  # Red X for KCV greater than 23
                              elif float(KCV) < 0.00:
                                        pcf = "🔴"  # Red X for KCV smaller than 0
                              else:
                                        pcf= "🟢"  # Green checkmark for KGV greater than or equal to 23
                                   
                         except Exception as e:
                              pcf = "🔴" 


                         try:
                              if float(five_ROE) < 14.00:
                                        roe = "🔴"  # Red X for KGV less than 23
                              
                              else:
                                        roe= "🟢"  # Green checkmark for KGV greater than or equal to 23          

                              if float(five_yrs_Nettomarge) > 5:
                                        
                                   netmarge = "🟢"  
                              else:
                                   netmarge = "🔴"    
                         except Exception as e:
                              netmarge = "🔴"    

                         try:
                              if one_FCF_annual_payout > 60:
                                        payout = "🔴"  # Red X for KGV less than 23

                              elif one_FCF_annual_payout < 0:
                                        payout = "🔴"  # Red X for KCV smaller than 0           
                              else:
                                        payout= "🟢"  # Green checkmark for KGV greater than or equal to 23
                         except Exception as e:

                              payout = "🔴" 

                         try:
                              if netincome_annual_funf_growth_ < 0:
                                        netincome = "🔴"  # Red X for KGV less than 23
                              else:
                                        netincome= "🟢"  # Green checkmark for KGV greater than or equal to 23


                              if revenue_annual_funf_Growth < 0:
                                        rev = "🔴"  # Red X for KGV less than 23
                              else:
                                        rev= "🟢"  # Green checkmark for KGV greater than or equal to 23
                         except Exception as e:
                              rev = "🔴" 
                              netincome = "🔴"

                         try:
                              if FCF_funf_growth < 0:
                                        fcf = "🔴"  # Red X for KGV less than 23
                              else:
                                        fcf= "🟢"  # Green checkmark for KGV greater than or equal to 23


                              if Shares_outstanding_funf_growth > 0:
                                        share = "🔴"  # Red X for KGV less than 23
                              else:
                                        share= "🟢"  # Green checkmark for KGV greater than or equal to 23
                         except Exception as e:

                              share = "🔴" 
                              fcf = "🔴"
                         try:
                              if Average_ROIC_funf == 'NA' or float(Average_ROIC_funf[:-1]) < 9:
                                        roic = "🔴"  # Red X for 'NA' or less than 9
                              else:
                                        roic= "🟢"  # Green checkmark for KGV greater than or equal to 23
                         except Exception as e:

                              roic = "🔴" 

                         try:
                              if float(debt_equity_ttm) > 2.0:
                                        dt_equt = "🔴"  # Red X for KGV less than 23

                              elif float(debt_equity_ttm) < 0:
                                   
                                   dt_equt = "🔴"  # Red X for KGV less than 23

                              else:
                                        dt_equt= "🟢"  # Gree

                         except Exception as e:

                              dt_equt= "🔴" 

                         try:
                              if Schuldentillgung > 5:
                                   schuld = "🔴"  # Red X for KGV less than 23
                              elif Schuldentillgung < 0:
                                   
                                   schuld = "🔴"  # Red X for KGV less than 23
                              else:
                                   schuld= "🟢"  # Gree
                         except Exception as e:
                              schuld ="🔴" 

          #################################################      
                         #@st.cache_data(show_spinner=False)
                         def display_metrics():
                              st.markdown("""
                              <style>
                              .metrics-container {
                                   display: flex;
                                   justify-content: center;
                                   width: 100%;
                                   margin: 0 auto;
                              }            
                              .metric-table {
                                   width: 100%;
                                   max-width: 1200px;
                                   border-collapse: collapse;
                                   margin: 0 auto;
                              }
                              .metric-table th, .metric-table td {
                                   border: 1px solid #ddd;
                                   padding: 8px;
                                   text-align: left;
                              }
                              .metric-table th {
                                 
                                   background-color: #f0f0f0; /* Hier war #f00ff00, was nicht gültig ist */

                              }
                              .metric-table .section-header {
                                   color: green;
                                   font-weight: bold;
                              }
                              </style>
                              
                              """, unsafe_allow_html=True)

                              st.markdown("""
                              <div style='text-align: center;'>
                                   <table class="metric-table">
                                        <tr>
                                             <td>
                                                  <table class="metric-table">
                                                       <tr>
                                                       <td class="section-header">Earnings Multiples</td>
                                                       <th>Value</th>
                                                       <th>Change</th>
                                                       </tr>
                                                       <tr>
                                                       <td>5 YR P/E < 23</td>
                                                       <td><b>{KGV}</b></td>
                                                       <td>{pe}</td>
                                                       </tr>
                                                       <tr>
                                                       <td>5 YR P/FCF < 23</td>
                                                       <td><b>{KCV}</b></td>
                                                       <td>{pcf}</td>
                                                       </tr>
                                                  </table>
                                             </td>
                                             <td>
                                                  <table class="metric-table">
                                                       <tr>
                                                       <td class="section-header">Leverage ratio/Bilanzkennzahl</td>
                                                       <th>Value</th>
                                                       <th>Change</th>
                                                       </tr>
                                                       <tr>
                                                       <td>5 YR FCF / DEBT < 5</td>
                                                       <td><b>{Schuldentillgung}</b></td>
                                                       <td>{schuld}</td>
                                                       </tr>
                                                       <tr>
                                                       <td>DEBT / EQUITY < 2</td>
                                                       <td><b>{debt_equity_ttm}</b></td>
                                                       <td>{dt_equt}</td>
                                                       </tr>
                                                  </table>
                                             </td>
                                        </tr>
                                        <tr>
                                             <td>
                                                  <table class="metric-table">
                                                       <tr>
                                                       <td class="section-header">Gewinnkennzahl/Ausschüttungsquote</td>
                                                       <th>Value</th>
                                                       <th>Change</th>
                                                       </tr>
                                                       <tr>
                                                       <td>5 YR ROIC > 9%</td>
                                                       <td><b>{Average_ROIC_funf}</b></td>
                                                       <td>{roic}</td>
                                                       </tr>
                                                       <tr>
                                                       <td>5 YR ROE > 14%</td>
                                                       <td><b>{five_Yrs_ROE}%</b></td>
                                                       <td>{roe}</td>
                                                       </tr>
                                                       <tr>
                                                       <td>5 YR NET MARGIN > 5%</td>
                                                       <td><b>{five_yrs_Nettomarge}%</b></td>
                                                       <td>{netmarge}</td>
                                                       </tr>
                                                       <tr>
                                                       <td>FCF PAYOUT RATIO < 60 %</td>
                                                       <td><b>{one_FCF_annual_payout}%</b></td>
                                                       <td>{payout}</td>
                                                       </tr>
                                                  </table>
                                             </td>
                                             <td>
                                                  <table class="metric-table">
                                                       <tr>
                                                       <td class="section-header">Wachstum/Aktienrückkauf</td>
                                                       <th>Value</th>
                                                       <th>Change</th>
                                                       </tr>
                                                       <tr>
                                                       <td>Revenue Growth 5 YR</td>
                                                       <td><b>{revenue_annual_funf_Growth:.2f}%</b></td>
                                                       <td>{rev}</td>
                                                       </tr>
                                                       <tr>
                                                       <td>Net Income Growth 5 YR</td>
                                                       <td><b>{netincome_annual_funf_growth_:.2f}%</b></td>
                                                       <td>{netincome}</td>
                                                       </tr>
                                                       <tr>
                                                       <td>FCF Growth 5 YR</td>
                                                       <td><b>{FCF_funf_growth:.2f}%</b></td>
                                                       <td>{fcf}</td>
                                                       </tr>
                                                       <tr>
                                                       <td>Shares Outstanding 5 YR</td>
                                                       <td><b>{Shares_outstanding_funf_growth:.2f}%</b></td>
                                                       <td>{share}</td>
                                                       </tr>
                                                  </table>
                                             </td>
                                        </tr>
                                   </table>
                              </div>
                              """.format(
                                   KGV=KGV, pe=pe,
                                   KCV=KCV, pcf=pcf,
                                   Schuldentillgung=Schuldentillgung, schuld=schuld,
                                   debt_equity_ttm=debt_equity_ttm, dt_equt=dt_equt,
                                   Average_ROIC_funf=Average_ROIC_funf, roic=roic,
                                   five_Yrs_ROE=five_Yrs_ROE, roe=roe,
                                   five_yrs_Nettomarge=five_yrs_Nettomarge, netmarge=netmarge,
                                   one_FCF_annual_payout=one_FCF_annual_payout, payout=payout,
                                   revenue_annual_funf_Growth=revenue_annual_funf_Growth, rev=rev,
                                   netincome_annual_funf_growth_=netincome_annual_funf_growth_, netincome=netincome,
                                   FCF_funf_growth=FCF_funf_growth, fcf=fcf,
                                   Shares_outstanding_funf_growth=Shares_outstanding_funf_growth, share=share
                              ), unsafe_allow_html=True)


                         display_metrics()

                         
                         st.write("")
                         col5, col6, col7, col8 = st.columns(4)

                         if Average_ROIC_funf == 'NA':
                              Average_ROIC_funf = 0.0
############################################################################################################################                             


               with st.container():   
                    with Stock_Analyser:

                         # Function to calculate NPV
                         #def calculate_npv(wacc, discounted_values,):
                          #    return npv(wacc / 100, discounted_values)
                         
                         def calculate_pv(fcf, wacc, year):
                              return fcf/ ((1 + wacc / 100) ** year)

                         @st.fragment
                         def simple_chart(fig, present_values_df_horizontal,average_fcf_values1, average_fcf_values2, npv_result, npv_result2):
                              if st.form_submit_button(label="Display FCF Calculation"):
                                   st.plotly_chart(fig,use_container_width=True, config=config)

                                   st.dataframe(present_values_df_horizontal,use_container_width=True)
          

                         #@st.cache_data(show_spinner=False,ttl=3600) 
                         def display_growth_rate_formexer():

                              with st.form(key='growth_rate_formex'):

                                   if "Average_10years_treasury_rate" not in st.session_state:
                                        st.session_state["Average_10years_treasury_rate"] = 4.25
                                        #print("treasury_yield_data",Average_10years_treasury_rate)


                                   if "Pepetual_growth_rate" not in st.session_state:
                                        st.session_state["Pepetual_growth_rate"] = 0.025
                                        


                                   col1, col2,col3,col4,col5 = st.columns(5)

                                   col1.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color:white;'>FCF 10Y CAGR :<br> {FCF_Cagr_10}%</div>", unsafe_allow_html=True)
                                   
                                   col2.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color:white;'>FCF 5Y CAGR:<br> {FCF_5_CAGR}%</div>", unsafe_allow_html=True)
                                   
                                   col3.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color:white;'>EPS 10Y CAGR:<br> {EPS_Cagr_10}%</div>", unsafe_allow_html=True)

                                   col4.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color:white;'>EPS 5Y CAGR:<br> {EPS_5_CAGR}%</div>", unsafe_allow_html=True)

                                   col5.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color:white;'>EPS next 5 YR (per annum):<br> {Earnings_next_5_yrs}</div>", unsafe_allow_html=True)


                              #to add space
                                   st.write("")


                                   col1,col2,col3 = st.columns(3)
                              
                                   with col1:
                                        st.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color:white;'>FCF Growth YOY: <br> {Average_fcf_growth_ten}%</div>", unsafe_allow_html=True)
                                        
                                   with col2:    
                                        st.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color:white;'>5 YR FCF Growth YOY:<br> {Average_fcf_growth_five}<br></div>", unsafe_allow_html=True)
                              
                                   with col3:    
                                        st.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color:white;'>3 YR FCF Growth YOY: <br> {Average_fcf_growth_3years}</div>", unsafe_allow_html=True)

                                   st.write("")
                                   col5,col4= st.columns(2)

                                   #WACC = float(col5.text_input("WACC (%):", value="8.00").replace(',', '.'))
                                   WACC = float(col5.text_input("WACC (%):", value=st.session_state.get('WACC', 8.00)).replace(',', '.'))

                         
                                   #FCF_discount_in_years = int(col4.text_input("Years:", value=int(10)).replace(',', '.'))
                                   FCF_discount_in_years = int(col4.text_input("Years:", value=st.session_state.get('FCF_discount_in_years', 10)).replace(',', '.'))


                              
                              #------------------------------------------------------------------------------------------------------------------------
                                   col9, col8,col34,col10= st.columns(4)
                                   
                                   Growth_rate1 = float(col9.text_input("Growth Rate (Base Case) in %:",value=0.00,key="growth_rate1ex").replace(',', '.'))
                                   col8.write('')
                                   col34.write('')
                                   Growth_rate2 = float(col10.text_input("Growth Rate (Bullish Case) in %:", value=0.00, key="growth_rate2ex").replace(',', '.'))
                              

                              
                              #---------------------------------------------------------Margin of Safety -------------------------------------------------------------

                                   cola, col8,col34,colc= st.columns(4)
                                   Margin_of_safety1 = float(cola.text_input("1.Margin of Safety (%):", value=9.00).replace(',', '.'))
                                   col8.write('')
                                   col34.write('')
                                   Margin_of_safety3 = float(colc.text_input("2.Margin of Safety (%):", value=9.00).replace(',', '.'))
                              #-------------------------------------------------------------------------------------------------------------------------------------------


                                   if st.form_submit_button(label="Calculate"):
                                        if average_fcf_Annual_one <= 0.00:

                                             average_fcf_Annual_DCF1 = rounded_fcf_Annual_five/1000000000
                                             average_fcf_Annual_DCF2 = rounded_fcf_Annual_five/1000000000
                                             print("last 5 years FCF:",rounded_fcf_Annual_five/1000000000)
                                        else:

                                             average_fcf_Annual_DCF1=average_fcf_Annual_one
                                             average_fcf_Annual_DCF2=average_fcf_Annual_one
                                             print("last FCF:",average_fcf_Annual_one)


                                        discounted_values = [] 
                                        average_fcf_values1 = []
                                        # Array for average FCF values (Base Case)

                                   
                                        for i in range(FCF_discount_in_years):
                                             discounted_value = average_fcf_Annual_DCF1 * (1 + (Growth_rate1/100))
                                             average_fcf_Annual_DCF1 = discounted_value
                                             average_fcf_values1.append(average_fcf_Annual_DCF1)  # Store in the array

                                             discounted_values.append(discounted_value) 

                                             # Calculate present values up to the second-to-last year
                                             present_values_base_case = [calculate_pv(fcf, WACC, year) for year, fcf in enumerate(average_fcf_values1[:-1], start=1)]

                                             #print(average_fcf_Annual_DCF1)

                                             if i == FCF_discount_in_years - 1:
                                                  second_to_last_discounted_value = discounted_values[-2]  # Access second-to-last element

                                                  Terminal_Value = second_to_last_discounted_value * (1 + st.session_state["Pepetual_growth_rate"]) / ((WACC/100) - st.session_state["Pepetual_growth_rate"])

                                                  # Discount the Terminal Value to its present value
                                                  Terminal_Value_pv = Terminal_Value / ((1 + WACC / 100) ** FCF_discount_in_years)

                                                  # Add the Terminal Value (PV) into the present_values_base_case array
                                                  present_values_base_case.append(Terminal_Value_pv)

                                                  # Calculate the total sum of present values (including Terminal Value)
                                                  total_present_value = sum(present_values_base_case)



                                        print("Total_Debt_from_all_calc",(Total_Debt_from_all_calc/1000000000))
                                        print("Total_cash_last_years",Total_cash_last_years)
                                        Equity_value_ = total_present_value+Total_cash_last_years-(Total_Debt_from_all_calc/1000000000)
                                        Intrinsic_value =Equity_value_/Average_shares_basic_annual_one
                                        print("Average_shares_basic_annual_one",Average_shares_basic_annual_one)

                                        Euro_equivalent = Intrinsic_value*usd_to_eur_rate

                                   

                              #----------------------------------------------------------2:Growth rate Estimate------------------------------------------------------------------------

                                   
                                        discounted_values2 = [] 
                                        average_fcf_values2 = []  # Array for average FCF values (Bullish Case)
                                        # Create an empty list to store discounted values
                                        for j in range(FCF_discount_in_years):
                                             discounted_value2 = average_fcf_Annual_DCF2 * (1 + (Growth_rate2/100))
                                             average_fcf_Annual_DCF2 = discounted_value2
                                             average_fcf_values2.append(average_fcf_Annual_DCF2)  # Store in the array

                                             discounted_values2.append(discounted_value2)  # Add the discounted value to the list
                                        
                                             present_values_bullish_case = [calculate_pv(fcf, WACC, year) for year, fcf in enumerate(average_fcf_values2[:-1], start=1)]

                                             if j == FCF_discount_in_years - 1:
                                                  second_to_last_discounted_value2 = discounted_values2[-2]  # Access second-to-last element

                                                  Terminal_Value2 = second_to_last_discounted_value2 * (1 + st.session_state["Pepetual_growth_rate"]) / ((WACC/100) - st.session_state["Pepetual_growth_rate"])

                                                  # Discount the Terminal Value to its present value
                                                  Terminal_Value_pv2 = Terminal_Value2 / ((1 + WACC / 100) ** FCF_discount_in_years)

                                                  # Add the Terminal Value (PV) into the present_values_base_case array
                                                  present_values_bullish_case.append(Terminal_Value_pv2)

                                                  # Calculate the total sum of present values (including Terminal Value)
                                                  total_present_value2 = sum(present_values_bullish_case)


     
                                        #rounded_npv_result2 = round(npv_result2, 2)  

                                        Equity_value2 = total_present_value2+Total_cash_last_years-(Total_Debt_from_all_calc/1000000000)
                                        Intrinsic_value2 =Equity_value2/Average_shares_basic_annual_one

                                        Euro_equivalent2 = Intrinsic_value2*usd_to_eur_rate

                                   
                                        #------------------------------------------Graham 1.Estimate--------------------------------------------------------------

                                        
                                        

                                        if EPS_last_average < 0:
                                             EPS_last_average_graham = Average_eps_basic_annual_five
                                             EPS_last_average_graham2 =Average_eps_basic_annual_five
                                        else:
                                             EPS_last_average_graham =EPS_last_average
                                             EPS_last_average_graham2 =EPS_last_average

                                        graham_valuation = (EPS_last_average_graham * (7+1.5 * Growth_rate1) * 4.4)/ st.session_state["Average_10years_treasury_rate"]
                                        
                                        Euro_equivalent_graham_valuation = graham_valuation*usd_to_eur_rate
                                             #print(f"{graham_valuation} USD is approximately {Euro_equivalent_graham_valuation:.2f} EUR")
                                        # Display the result
                                   # .   ...........................................Graham 2.Estimate.........................................   
                                   
                                        graham_valuation2 = (EPS_last_average_graham2 * (7+1.5*Growth_rate2)*4.4)/ st.session_state["Average_10years_treasury_rate"]
                                   
                                        Euro_equivalent_graham_valuation2 = graham_valuation2*usd_to_eur_rate


                                   #........................................................................................


                                        Multiples_valuation1 =Euro_equivalent + Euro_equivalent_graham_valuation
                                   
                                        average_sum1 = Multiples_valuation1 / 2
                                        average_sum_both1 =  round(average_sum1*(1-Margin_of_safety1/100),2)
                                        
                                        #st.write(average_sum_both1,converted_amount)


                                        Multiples_valuation2 =Euro_equivalent2+Euro_equivalent_graham_valuation2
                                        average_sum2 = Multiples_valuation2 / 2
                                        average_sum_both2=round(average_sum2 *(1-Margin_of_safety3/100),2)

                                        Middle_multiple_value = average_sum_both1+average_sum_both2
                                        average_Middle_multiple_value =round(Middle_multiple_value/2,2)


                                        low_DCF=(Euro_equivalent*(1-Margin_of_safety1/100))
                                        high_DCF=(Euro_equivalent2*(1-Margin_of_safety3/100))

                                        Average_Middle_DCF=round((low_DCF+high_DCF)/2)



                                        col11, col12,col13, col14= st.columns(4)

                                        col11.write(f'Current Price: <span style="color: green;">{converted_amount} &euro;</span>', unsafe_allow_html=True)

                                        col12.write(f"Low Estimate:")
                                        col13.write(f"Middle Estimate: ")
                                        col14.write(f"High Estimate:")


                                        col15, col16, col17, col18 = st.columns(4)


                                        col15.write(f" Benjamin Graham Fair Value + DCF:  ")
                                        # Adding a help expander below

                                             
                                        if float(average_sum_both1) > float(converted_amount):
                                             font_color = "green"
                                        else:
                                             font_color = "red"
                                        col16.write(f"<span style='color:{font_color}'>{average_sum_both1} €</span>", unsafe_allow_html=True)

                                        if float(average_Middle_multiple_value) > float(converted_amount):
                                             font_color = "green"
                                        else:
                                             font_color = "red"
                                             #col17.write(f"{average_Middle_multiple_value:.2f} €")
                                        
                                        col17.write(f"<span style='color:{font_color}'>{average_Middle_multiple_value} €</span>", unsafe_allow_html=True)
                                             #col18.write(f"{average_sum_both2:.2f} €")
                                             

                                        if float(average_sum_both2) > float(converted_amount):
                                             font_color = "green"
                                        else:
                                             font_color = "red"
                                        col18.write(f"<span style='color:{font_color}'>{average_sum_both2} €</span>", unsafe_allow_html=True)

                                                  # Display number outputs for each estimate
                                        col19, col20, col21, col22 = st.columns(4)

                                        col19.write(f"Discounted Cash Flow Analysis (DCF):")
                                             #col20.write(f"{low_DCF:.2f} €")
                                        if float(low_DCF) > float(converted_amount):
                                             font_color = "green"
                                        else:
                                             font_color = "red"
                                        col20.write(f"<span style='color:{font_color}'>{low_DCF:.2f} €</span>", unsafe_allow_html=True)
                                             #col21.write(f"{Average_Middle_DCF:.2f} €")

                                        if float(Average_Middle_DCF) > float(converted_amount):
                                             font_color = "green"
                                        else:
                                             font_color = "red"
                                        col21.write(f"<span style='color:{font_color}'>{Average_Middle_DCF:.2f} €</span>", unsafe_allow_html=True)
                                             #col22.write(f"{high_DCF:.2f} €")

                                        if float(high_DCF) > float(converted_amount):
                                             font_color = "green"
                                        else:
                                             font_color = "red"
                                        col22.write(f"<span style='color:{font_color}'>{high_DCF:.2f} €</span>", unsafe_allow_html=True)


                                        present_values_df = pd.DataFrame({
                                        #'Year': range(1, FCF_discount_in_years + 1),
                                        'Year': [str(i) for i in range(1, FCF_discount_in_years)] + ['Terminal Value'],  # Label the last year as "Terminal Value"

                                        'Present Value (Base Case)': present_values_base_case,
                                        'Present Value (Bullish Case)': present_values_bullish_case
                                        })

                                        # Transpose the DataFrame to make it horizontal
                                        present_values_df_horizontal = present_values_df.set_index('Year').T                                        

                                        # Save average FCF values to a DataFrame for plotting
                                        fcf_df = pd.DataFrame({
                                             'Year': range(1, FCF_discount_in_years+1),
                                             #'Year': [str(i) for i in range(1, FCF_discount_in_years)] + ['Terminal Value'],  # Label the last year as "Terminal Value"
                                             'Discounted Cash Flow (Base Case)': average_fcf_values1,
                                             'Discounted Cash Flow (Bullish Case)': average_fcf_values2
                                             
                                        })


                                                                  # Plot the chart using Plotly as a bar chart
                                        fig = px.bar(fcf_df, x='Year', y=['Discounted Cash Flow (Base Case)', 'Discounted Cash Flow (Bullish Case)'],
                                                       title='Discounted Cash Flows Comparison in Billion USD',
                                                       labels={'value': 'Discounted Cash Flow', 'Year': 'Year'},
                                                       text_auto=True  # Automatically display values on bars
                                                       )
                                        fig.update_traces(textposition='inside')  # Automatically position text labels

                                        fig.update_layout(
                                        xaxis_type='category',  # Ensure x-axis is treated as categorical
                                        dragmode=False,  # Disable dragging for zooming
                                        yaxis_title="Discounted Cash Flow (in Billion USD)",
                                        xaxis_title="Year",
                                        barmode='group'  # Grouped bar chart
                                        )

                                        # Call the chart display function
                                        simple_chart(fig, present_values_df_horizontal,average_fcf_values1, average_fcf_values2,Equity_value_, total_present_value2)


                                   
                         display_growth_rate_formexer()


     #.........................................................
     
          #################

               with st.container():   
                    with Reversed_DCF:                         

                         # Discounted Cash Flow function with reverse DCF logic
                         @st.cache_data(show_spinner=False, ttl=3600) 
                         
                         def present_value(g, fcf, r, t, years):
                              pv = 0
                              for i in range(1, years + 1):
                                   pv += fcf * (1 + g)**i / (1 + r)**i
                              terminal_value = fcf * (1 + g)**years * (1 + t) / (r - t)
                              pv += terminal_value / (1 + r)**years
                              return pv

                         def find_growth_rate(fcf, r, t, years, current_price):
                              def objective(g):
                                   return present_value(g, fcf, r, t, years) - current_price
                              return optimize.brentq(objective, -0.5, 0.5)
                              

                         st.write("""
                         This app calculates the Implied Growth Rate using a Two-Stage Reverse DCF model.
                         The default forecast period is set to 10 years.
                         """)

                         with st.form("reverse_dcf_form"):
                              st.markdown(
                              f"""<span style='color: green;'>**{name}**</span> FCF (TTM): <span style='color: green;'>**{fcf_ttm:.2f} B**</span> 
                              , Market Capitalization: <span style='color: green;'>**{Marketcap_in_Billion}**</span>
                              , FCF 10Y CAGR %: <span style='color: green;'>**{FCF_Cagr_10}%**</span>
                              , FCF 5Y CAGR %: <span style='color: green;'>**{FCF_5_CAGR}%**</span>
                              , FCF Growth YOY: <span style='color: green;'>**{Average_fcf_growth_ten}%**</span>""",
                              unsafe_allow_html=True
                              )
                              col1, col2 = st.columns(2)

                              with col1:
                                   fcf = st.number_input("Current FCF in Billion USD:", value=0.00, key="fcf_input",help="Enter Free Cash Flow value")

                                   r = st.number_input("Discount rate WACC (%):", value=8.0, format="%.1f")
                             
                                   years =10
                              with col2:
                                   t = st.number_input("Terminal Growth Rate (%):", value=2.5, format="%.1f")
                                   current_price = st.number_input("Marketcap.in Billion USD:", value=0.00, format="%.2f")
                                 

                              submitted = st.form_submit_button("Calculate")

                         if submitted:
                              try:
                                   r = r / 100  # Convert to decimal
                                   t = t / 100  # Convert to decimal

                                   implied_growth = find_growth_rate(fcf, r, t, years, current_price)
                                   
                                   st.write(f"Implied Growth Rate: {implied_growth*100:.3f}%")

                                   st.write("### Interpretation")
                                   st.write(f"""
                                   - The implied growth rate of **{implied_growth*100:.3f}%** means the company's Free Cash Flow 
                                        needs to grow at this rate annually for the next **{years}** years to justify the current share price.
                                   - After year {years}, the growth is assumed to slow to the terminal growth rate of {t*100:.1f}%.
                                   - If this growth rate seems unrealistically high compared to historical performance or industry standards, 
                                        the stock might be overvalued.
                                   - Compare this rate with industry averages and the company's historical growth rates for context.
                                   """)

                                   # Additional information
                                   st.write("### Additional Information")
                                   final_fcf = fcf * (1 + implied_growth)**years
                                   projected_fcfs = [fcf * (1 + implied_growth)**i for i in range(1, years + 1)]
                                   projected_fcfs_rounded = [round(fcf, 2) for fcf in projected_fcfs]

                                   st.write(f"- Projected FCF after {years} years: ${final_fcf:.2f}")
                                   terminal_value = final_fcf * (1 + t) / (r - t)
                                   st.write(f"- Terminal Value: ${terminal_value:.2f}")
                                   
                                   # Calculate percentage of value from terminal value
                                   total_value = present_value(implied_growth, fcf, r, t, years)
                                   terminal_value_percentage = (terminal_value / (1 + r)**years) / total_value * 100

                                   st.write(f"- Percentage of value from terminal value: {terminal_value_percentage:.2f}%")


#                                   Use `simple_chart` to generate the FCF projections chart
                                   @st.fragment
                                   def simple_chart():
                                        if st.button(label="Display FCF Calculation"):
                                             # Generate FCF chart
                                             years_list = list(range(1, years + 1))
                                             fig = go.Figure()
                                             fig.add_trace(
                                                  go.Scatter(
                                                  x=years_list, 
                                                  y=projected_fcfs_rounded, 
                                                  mode='lines+markers', 
                                                  name="Projected FCF"
                                                  )
                                             )
                                             fig.update_layout(
                                                  title="Free Cash Flow (FCF) Projections",
                                                  xaxis_title="Year",
                                                  yaxis_title="FCF ($)",
                                                  template="plotly_white",
                                                  dragmode=False,  # Disable dragging for zooming
                                             )
                                             st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                                   # Call the `simple_chart` function to display the plot
                                   simple_chart()

                              except Exception as e:
                                   st.write(f" ")
          ################################experiment2########
               
                                   
               
               with st.container():
                    
                    #use_container_width=True
                    with Multiple_Valuation:        
                    #@st.experimental_fragment
                         

                    
                         def display_growth_rate_form():

                              with st.form(key='growth_rate_form31'):
                              
                                   col1,col2= st.columns(2)

                                   with col1:
                                        st.markdown("<div style='text-align: center;'>Historical:</div>", unsafe_allow_html=True)

                                   with col2:
                                        My_assumption = int(st.text_input("My Assumptions in Years:", value=int(10), key="My_assumption12"))


                                   col1, col2, col3, col4, col5, col6 = st.columns(6)

                                   for col, label in zip([col1, col2, col3, col4, col5, col6], ["1YR:", "5YR:", "10YR:", "LOW", "MID", "HIGH"]):
                                        with col:
                                             st.markdown(f"<div style='text-align: center;'>{label}</div>", unsafe_allow_html=True)

                                   
                                   colr1,colr2,colr3,colr9,colr10,colr11 = st.columns(6)

                                   colr1.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>Revenue Growth: <br> {Revenue_growth_1year:.2f}%</div>", unsafe_allow_html=True)
                                   colr2.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>Revenue Growth: <br> {Revenue_5_CAGR}%</div>", unsafe_allow_html=True)
                                   colr3.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>Revenue Growth: <br> {Revenue_Cagr_10}%</div>", unsafe_allow_html=True)

                                   coln1,coln2,coln3,coln9,coln10,coln11 = st.columns(6)

                                   coln1.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>Net Profit Margin: <br> {Net_margin_ttm}</div>", unsafe_allow_html=True)
                                   coln2.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>Net Profit Margin: <br> {five_yrs_Nettomarge}%</div>", unsafe_allow_html=True)
                                   coln3.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>Net Profit Margin: <br> {Net_income_margin_10}%</div>", unsafe_allow_html=True)

                                   colf1,colf2,colf3,colf9,colf10,colf11 = st.columns(6)

                                   colf1.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>FCF Margin: <br> {FCF_Margin_1:.2f}%</div>", unsafe_allow_html=True)
                                   colf2.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>FCF Margin: <br> {FCF_Margin_5}%</div>", unsafe_allow_html=True)
                                   colf3.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>FCF Margin: <br> {FCF_Margin_10}%</div>", unsafe_allow_html=True)      

                                   colcf1,colcf2,colcf3,colcf9,colcf10,colcf11 = st.columns(6)

                                   colcf1.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>Price/OCF: <br> {P_OCF_ttm}</div>", unsafe_allow_html=True)
                                   colcf2.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>Price/OCF: <br> {P_OCF_5}</div>", unsafe_allow_html=True)
                                   colcf3.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>Price/OCF: <br> {P_OCF_10}</div>", unsafe_allow_html=True)

                                   colfcf1,colfcf2,colfcf3,colfcf9,colfcf10,colfcf11 = st.columns(6)
                                   colfcf1.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>Price/FCF: <br> {pfcf_ttm}</div>", unsafe_allow_html=True)
                                   colfcf2.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>Price/FCF: <br> {pfcf_funf}</div>", unsafe_allow_html=True)
                                   colfcf3.write(f"<div style='background-color:#4b71ff; padding: 10px; border-radius: 5px; color: white;'>Price/FCF: <br> {pfcf_ten}</div>", unsafe_allow_html=True)

                              

                                   col1,col2,colx,cola, colb, colc= st.columns(6)
                                   col1.write('')               
                                   col2.write('')
                                   #st.write(current_price)
                                   #converted_amount = "{:.2f}".format(current_price * usd_to_eur_rate)
                                   col1.write(f'Current Price: <span style="color: green;">{converted_amount} &euro;</span>', unsafe_allow_html=True) 

                                   #colx.write('')
                                   colx.write(f"<div style='background-color:#4b71ff;padding: 10px; border-radius: 5px; color: white;'>Desired Rate of Return: <br><br>{''}</div>", unsafe_allow_html=True)

                                   st.write("")
                                   colx.write('')
                                   colx.write(f"Multiple of Earnings Valuation:")
                              
                                   
                                   Growth_rate_revenue_LOW = float(colr9.text_input(" ", value=0,key="Growth_rate_revenue_LOW22", placeholder="Enter % (e.g. 5)").replace(',', '.'))

                                   Growth_rate_revenue_middle = float(colr10.text_input(" ", value=0,key="Growth_rate_revenue_middle22").replace(',', '.'))
                                   Growth_rate_revenue_high = float(colr11.text_input(" ", value=0,key="Growth_rate_revenue_high22").replace(',', '.'))
                                        
                                   Growth_rate_net_profit_LOW = float(coln9.text_input(" ", value=0,key="Growth_rate_net_profit_LOW23").replace(',', '.'))
                                   Growth_rate__net_profit_middle = float(coln10.text_input(" ", value=0,key="Growth_rate__net_profit_middle23").replace(',', '.'))
                                   Growth_rate__net_profit_high = float(coln11.text_input(" ", value=0,key="Growth_rate__net_profit_high23").replace(',', '.'))

                                   Growth_rate_fcf_margin_LOW = float(colf9.text_input(" ", value=0,key="Growth_rate_fcf_margin_LOW24").replace(',', '.'))
                                   Growth_rate_fcf_margin_middle = float(colf10.text_input(" ", value=0,key="Growth_rate_fcf_margin_middle24").replace(',', '.'))
                                   Growth_rate_fcf_margin_high = float(colf11.text_input(" ", value=0,key="Growth_rate_fcf_margin_high24").replace(',', '.'))

                                   Growth_rate_P_OCF_low = float(colcf9.text_input(" ", value=0,key="Growth_rate_P_OCF_low22").replace(',', '.'))
                                   Growth_rate_P_OCF_middle = float(colcf10.text_input(" ", value=0,key="Growth_rate_P_OCF_middle22").replace(',', '0.0'))
                                   Growth_rate_P_OCF_high = float(colcf11.text_input(" ", value=0,key="Growth_rate_P_OCF_high22").replace(',', '.'))

                                   Growth_rate_P_FCF_low = float(colfcf9.text_input(" ", value=0,key="Growth_rate_P_FCF_low22").replace(',', '.'))
                                   Growth_rate_P_FCF_middle = float(colfcf10.text_input(" ", value=0,key="Growth_rate_P_FCF_middle22").replace(',', '.'))
                                   Growth_rate_P_FCF_high = float(colfcf11.text_input(" ", value=0,key="Growth_rate_P_FCF_high22"))

                                   Margin_of_safety_low = float(cola.text_input(" ", value=9,key="Margin_of_safety_low22").replace(',', '.'))
                                   Margin_of_safety_mid = float(colb.text_input(" ", value=9,key="Margin_of_safety_mid22").replace(',', '.'))
                                   Margin_of_safety_high = float(colc.text_input(" ", value=9,key="Margin_of_safety_high22").replace(',', '.'))

                                   #except Exception as e:
                                   #    st.error("Please use a dot instead of a comma for decimal values.")
                                   with col1:
                                        submit_button = st.form_submit_button(label='Calculate')
                              if submit_button:
                                   st.session_state.converted_amount = converted_amount

                              
                              # -----------------------------LOW-------------
                              
                                   average_FCF_Profit_margin_low=((Growth_rate_fcf_margin_LOW+Growth_rate_net_profit_LOW)/2)/100

                                   average_PFCF_POCF_low=(Growth_rate_P_OCF_low+Growth_rate_P_FCF_low)/2

                                   Revenue_assumption_low=average_revenue_annual_ttm*pow(1+(Growth_rate_revenue_LOW/100),My_assumption)
                                             #

                                   Assumption_low=(Revenue_assumption_low*average_FCF_Profit_margin_low)*average_PFCF_POCF_low
                                   Assumption_low_inklu_shares_outstanding_low =Assumption_low/Average_shares_basic_annual_one

                                   Assumption_low_inklu_shares_outstanding_MarginofSafety_low=Assumption_low_inklu_shares_outstanding_low*(1-(Margin_of_safety_low/100))


                                   Revenue_low_Euro = "{:.2f}".format(Assumption_low_inklu_shares_outstanding_MarginofSafety_low*usd_to_eur_rate)
                                        
                              
                              # -----------------------------MIDDLE-------------
                                   average_FCF_Profit_margin_mid=((Growth_rate_fcf_margin_middle+Growth_rate__net_profit_middle)/2)/100

                                   average_PFCF_POCF_mid=(Growth_rate_P_OCF_middle+Growth_rate_P_FCF_middle)/2

                                   Revenue_assumption_mid=average_revenue_annual_ttm*pow(1+(Growth_rate_revenue_middle/100),My_assumption)

                                   Assumption_mid=(Revenue_assumption_mid*average_FCF_Profit_margin_mid)*average_PFCF_POCF_mid

                                   Assumption_mid_inklu_shares_outstanding_mid =Assumption_mid/Average_shares_basic_annual_one

                                   Assumption_mid_inklu_shares_outstanding_MarginofSafety_mid=Assumption_mid_inklu_shares_outstanding_mid*(1-(Margin_of_safety_mid/100))
                                   

                                   Revenue_mid_Euro = "{:.2f}".format(Assumption_mid_inklu_shares_outstanding_MarginofSafety_mid*usd_to_eur_rate)
                                        

                                        
                              # -----------------------------HIGH-------------

                                   average_FCF_Profit_margin_high=((Growth_rate_fcf_margin_high+Growth_rate__net_profit_high)/2)/100

                                   average_PFCF_POCF_high=(Growth_rate_P_OCF_high+Growth_rate_P_FCF_high)/2

                                   Revenue_assumption_high=average_revenue_annual_ttm*pow(1+(Growth_rate_revenue_high/100),My_assumption)

                                   Assumption_high=(Revenue_assumption_high*average_FCF_Profit_margin_high)*average_PFCF_POCF_high

                                   Assumption_high_inklu_shares_outstanding_high =Assumption_high/Average_shares_basic_annual_one

                                   Assumption_high_inklu_shares_outstanding_MarginofSafety_high=Assumption_high_inklu_shares_outstanding_high*(1-(Margin_of_safety_high/100))
                                   
                                   Revenue_high_Euro = "{:.2f}".format(Assumption_high_inklu_shares_outstanding_MarginofSafety_high*usd_to_eur_rate)
                                        
                                             
                                   st.markdown('</div>', unsafe_allow_html=True)

                    
                                   if float(Revenue_low_Euro) < float(converted_amount):
                                             font_color = "red"
                                   else:
                                             font_color = "green"
                                   cola.write(f"<span style='color:{font_color}'>{Revenue_low_Euro} €</span>", unsafe_allow_html=True)

                                   if float(Revenue_mid_Euro) < float(converted_amount):
                                             font_color = "red"
                                   else:
                                             font_color = "green"
                                   colb.write(f"<span style='color:{font_color}'>{Revenue_mid_Euro} €</span>", unsafe_allow_html=True)

                                   if float(Revenue_high_Euro) < float(converted_amount):
                                             font_color = "red"
                                   else:
                                             font_color = "green"
                                   colc.write(f"<span style='color:{font_color}'>{Revenue_high_Euro} €</span>", unsafe_allow_html=True)

                         #@st.fragment
                         #@st.cache_data
                         #@single_fragment
                         def main():
                              
                              display_growth_rate_form()
                         if __name__ == "__main__":
                              main()
          #####################################################################################################################################################                             


#####################################################################################################################################################          
               with st.container(): 
                    use_container_width=True             
                    with Key_ratios:
                         Annual, Quarter = st.tabs(["Annual", "Quarterly"])

                              #with Annual:
                              #    Annual,Quarterly = st.tabs(["Annual","Quarterly"])
                                   
                         with Annual:
                                   
                                   Period_end_dates_annual = annual_data['period_end_date'][-len_10_annual:]
                                   index = range(len(Period_end_dates_annual))

                                   total = pd.DataFrame({
                                   'Period End Date': Period_end_dates_annual,
                                   'Revenue growth': Revenue_growth_10_unpacked,
                                   'Net Income growth': NetIncome_growth_annual_10_unpacked,
                                   'Net Interest Income growth': Net_interest_Income_annual_10_growth_unpacked,
                                   'FCF growth': fcf_growth_annual_10_unpacked ,
                                   'EPS growth':EPS_growth_annual_10yrs_unpacked,
                                   'FCF Margin':FCF_Margin_annual_10unpacked,
                                   'EBITDA Margin': ebitda_Margin_annual_10_unpacked,
                                   'Shares diluted':shares_diluted_annual_growth_10_unpacked,
                                   'Operating Margin':operating_margin_annual10_unpacked,
                                   'Gross Margin':gross_margin_annual10_unpacked, 
                                   'Debt/Equity':debt_equity_annual_10_unpacked,
                                   'Book Value': Book_Value_growth_annual_10_unpacked,
                                   'Price to Sales': Price_to_sales_annual_10_unpacked,
                                   'Price to Tangible Book': Price_to_tangible_book_annual_10_unpacked,
                                   'EBITDA growth': EBITDA_growth_annual_10_unpacked,
                                   'Price to Book': Price_to_book_10_annual_unpacked,
                                   'PE ratio':Price_to_earnings_annual_10_unpacked,
                                   'Dividend per share':Dividend_per_share_annual10_unpacked,
                                   'Dividend per share growth ':Dividends_per_share_growth_annual10_unpacked,
                                   'FCF per share':fcf_per_share_annual_10_unpacked,
                                   'Revenue per share':revenue_per_share_annual_10_unpacked,
                                   'Payout ratio': Payout_ratio_annual_10_unpacked,
                                   'ROIC':ROIC_annual_10_unpacked,
                                   'ROE':ROE_annual_10_unpacked
                                   
                                   }, index=index)

                                   # Create a DataFrame for the metrics
                                   metrics = [
               
                                   ('Revenue growth', Revenue_growth_10_unpacked),
                                   ('Net Income growth', NetIncome_growth_annual_10_unpacked),
                                   ('Net Interest Income growth', Net_interest_Income_annual_10_growth_unpacked),
                                   ('FCF growth', fcf_growth_annual_10_unpacked ),
                                   ('EPS growth',EPS_growth_annual_10yrs_unpacked),
                                   ('FCF Margin',FCF_Margin_annual_10unpacked), 
                                   ('EBITDA Margin', ebitda_Margin_annual_10_unpacked),
                                   ('Shares diluted',shares_diluted_annual_growth_10_unpacked),
                                   ('Operating Margin',operating_margin_annual10_unpacked),
                                   ('Gross Margin',gross_margin_annual10_unpacked), 
                                   ('Book Value', Book_Value_growth_annual_10_unpacked),
                                   ('Debt/Equity',debt_equity_annual_10_unpacked),
                                   ('Price to Sales', Price_to_sales_annual_10_unpacked),
                                   ('Price to Tangible Book', Price_to_tangible_book_annual_10_unpacked),
                                   ('EBITDA growth', EBITDA_growth_annual_10_unpacked),
                                   ('Price to Book', Price_to_book_10_annual_unpacked),
                                   ('PE ratio',Price_to_earnings_annual_10_unpacked ),
                                   ('Dividend per share',Dividend_per_share_annual10_unpacked),
                                   ('Dividend per share growth',Dividends_per_share_growth_annual10_unpacked),
                                   ('FCF per share',fcf_per_share_annual_10_unpacked),
                                   ('Revenue per share',revenue_per_share_annual_10_unpacked),
                                   ('Payout ratio', Payout_ratio_annual_10_unpacked),
                                   ('ROIC',ROIC_annual_10_unpacked ),
                                   ('ROE',ROE_annual_10_unpacked)
                                   
                              
                                   ]
                              
                                   merged_data = {}
                                   for metric_name, metric_data in metrics:
                                        if not isinstance(metric_data, list):
                                             metric_data = [metric_data]  # Convert non-iterable values to lists

                                        if metric_name in ('Revenue growth', 'Net Income growth','Net Interest Income growth','FCF growth', 'EPS growth','FCF Margin','EBITDA Margin','Shares diluted','Operating Margin','Gross Margin','Debt/Equity','EBITDA growth','Dividend per share growth','Payout ratio','ROIC','ROE'):
                                             formatted_data = ["{:.2f}%".format(data * 100) for data in metric_data]
                                        elif metric_name == 'Book Value':
                                             formatted_data = ["{:.2f}B".format(data / 1_000_000_000) for data in metric_data]

                                        elif metric_name == 'Dividend per share':
                                             formatted_data = ["${:.2f}".format(data ) for data in metric_data]
                                        else:
                                             #formatted_data = ["{:.2f}".format(data) for data in metric_data]
                                             formatted_data = ["{:.2f}".format(data) for data in metric_data]

                                        merged_data[metric_name] = formatted_data

                                   merged_df_key_ratio = pd.DataFrame(merged_data, index=Period_end_dates_annual).transpose()

                                   st.table(merged_df_key_ratio.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px'})                                             .set_table_styles(
                                             [{'selector': 'thead th', 'props': [('color', 'black')]}],  # Set font color of header (first row) to blue
                                             axis=1
                                        ))


                                   with Quarter:
                                                  

                                                       Period_end_dates_quarter = quarterly_data['period_end_date'][-10:]
                                                       index = range(len(Period_end_dates_quarter))
                                                       
                                                       total = pd.DataFrame({
                                                       'Period End Date': Period_end_dates_quarter,
                                                       'Revenue growth': Revenue_growth_10quarter_unpacked,
                                                       'Net Income growth': NetIncome_growth_quarter_10_unpacked,
                                                       'Net Interest Income growth': Net_interest_Income_quarter_10_growth_unpacked,
                                                       'FCF growth': FCF_growth_quarter_10_unpacked,
                                                       'EPS growth':EPS_growth_quarter_10_unpacked,
                                                       'FCF Margin':FCF_Margin_quarter_10_unpacked,
                                                       'EBITDA Margin':ebitda_Margin_quarter_10_unpacked,
                                                       'Shares diluted':shares_diluted_quarter_growth_10_unpacked,
                                                       'Operating Margin':operating_margin_quater10_unpacked,
                                                       'Gross Margin':gross_margin_quarter10_unpacked, 
                                                       'Debt/Equity':debt_equity_quarter_10_unpacked,
                                                       'Book Value': Book_Value_growth_quarter_10_unpacked,
                                                       'Price to Sales': Price_to_sales_quarter_10_unpacked,
                                                       'Price to Tangible Book': Price_TBV_quarter10_unpacked,
                                                       'EBITDA growth': EBITDA_growth_quarter_10_unpacked,
                                                       'Price to Book': Price_to_book_quarter_10_unpacked,
                                                       'PE ratio':Price_to_earnings_quarter_10_unpacked,
                                                       'Dividend per share':Dividend_per_share_quarter_10_unpacked,
                                                       'Dividend per share growth':Dividend_per_share_growth_quarter_10_unpacked,
                                                       'FCF per share':fcf_per_share_quarter_10_unpacked,
                                                       'Revenue per share':revenue_per_share_quarter_10_unpacked, 
                                                       'Payout ratio': Payout_ratio_quarter_10_unpacked,
                                                       'ROIC':ROIC_quarter_10_unpacked,
                                                       'ROE':ROE_quarter_10_unpacked
                                                       }, index=index)

                                                       # Create a DataFrame for the metrics
                                                       metrics = [

                                                       ('Revenue growth ', Revenue_growth_10quarter_unpacked),
                                                       ('Net Income growth', NetIncome_growth_quarter_10_unpacked),
                                                       ('Net Interest Income growth', Net_interest_Income_quarter_10_growth_unpacked),
                                                       ('FCF growth', FCF_growth_quarter_10_unpacked),
                                                       ('EPS growth',EPS_growth_quarter_10_unpacked),
                                                       ('FCF Margin',FCF_Margin_quarter_10_unpacked), 
                                                       ('EBITDA Margin', ebitda_Margin_quarter_10_unpacked),
                                                       ('Shares diluted',shares_diluted_quarter_growth_10_unpacked),
                                                       ('Operating Margin',operating_margin_quater10_unpacked),
                                                       ('Gross Margin',gross_margin_quarter10_unpacked), 
                                                       ('Book Value', Book_Value_growth_quarter_10_unpacked),
                                                       ('Debt/Equity',debt_equity_quarter_10_unpacked),
                                                       ('Price to Sales', Price_to_sales_quarter_10_unpacked),
                                                       ('Price to Tangible Book', Price_TBV_quarter10_unpacked),
                                                       ('EBITDA growth', EBITDA_growth_quarter_10_unpacked),
                                                       ('Price to Book', Price_to_book_quarter_10_unpacked),
                                                       ('PE ratio',Price_to_earnings_quarter_10_unpacked ),
                                                       ('Dividend per share',Dividend_per_share_quarter_10_unpacked),
                                                       ('Dividend per share growth',Dividend_per_share_growth_quarter_10_unpacked),
                                                       ('FCF per share',fcf_per_share_quarter_10_unpacked),
                                                       ('Revenue per share',revenue_per_share_quarter_10_unpacked), 
                                                       ('Payout ratio', Payout_ratio_quarter_10_unpacked),
                                                       ('ROIC',ROIC_quarter_10_unpacked),
                                                       ('ROE',ROE_quarter_10_unpacked)
                                                  
                                                       ]
                                                  

                                                       merged_data = {}
                                                       for metric_name, metric_data in metrics:
                                                            if not isinstance(metric_data, list):
                                                                 metric_data = [metric_data]  # Convert non-iterable values to lists

                                                            if metric_name in ('Revenue growth', 'Net Income growth','Net Interest Income growth', 'FCF growth', 'EPS growth','FCF Margin','EBITDA Margin','Shares diluted','Operating Margin','Gross Margin','Debt/Equity','EBITDA growth','Dividend per share growth','Payout ratio','ROIC','ROE'):
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
                                                       st.table(merged_df_key_ratio.style.set_table_attributes('class="fixed-table"').set_properties(**{'max-width': '1000px', 'margin': 'auto'})                                             .set_table_styles(
                                                            [{'selector': 'thead th', 'props': [('color', 'black')]}],  # Set font color of header (first row) to blue
                                                            axis=1
                                                       )
                                                       )
                                                                      



               with st.container():
                    #use_container_width=True
                    with Charts:
                              Annual, Quarter = st.tabs(["Annual", "Quarterly"])
                              with Annual:
                                   
                                   revenue_annual21 = ["{:.2f}".format(value/1e9) for value in revenue_annual21_unpacked]
                                   revenue_growth_annual21 = ["{:.2f} %".format(value*100) for value in revenue_growth_annual21_unpacked]


                                   # Create a DataFrame for the data
                                   data = pd.DataFrame({
                                   'Date': date_annual_20yrs,
                                   #'Free Cash Flow': Free_cash_flow_annual_2003,
                                   'Revenue in Billion USD':revenue_annual21,
                                   })



                                   fig1 = px.bar(data, x='Date', y='Revenue in Billion USD',
                                             text='Revenue in Billion USD',    
                                             labels={'value': 'Amount()'},
                                        # title=f"Revenue : 10 YR: {Revenue_Cagr_10}%    5 YR: {Revenue_5_CAGR}%"
                                             ) 
    
 
                                   fig1.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )

                                   fig1.update_layout(
                                   xaxis_type='category' 
                                   )
                                   

                              # Create a DataFrame for the data
                                   data = pd.DataFrame({
                                   'Date': date_annual_20yrs,
                                   #'Free Cash Flow': Free_cash_flow_annual_2003,
                                   'Revenue Growth':revenue_growth_annual21,
                                   })

                                   fig2 = px.bar(data, x='Date', y='Revenue Growth',
                                             text='Revenue Growth', 
                                             labels={'value': 'Amount'},
                                             ) 
                                   
                                   fig2.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )

                                   fig2.update_layout(
                                   xaxis_type='category' 
                                   )


                                   col1,col2 = st.columns(2)

                                   

                                   with col1:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b>Revenue : 10 YR: {Revenue_Cagr_10}%
                                        <b>  5 YR: {Revenue_5_CAGR}%
                                        </div>
                                        """, unsafe_allow_html=True)

                                        st.plotly_chart(fig1,use_container_width=True, config=config)

                                   with col2:
                                        st.write(f"""
                                                  <div style='text-align: center;'>
                                        <b>5 YR Revenue Y/Y: {Revenue_growth_5years:.2f}%  1 YR Revenue: {Revenue_growth_1year:.2f}%
                                        </div>
                                        """, unsafe_allow_html=True)

                                        st.plotly_chart(fig2,use_container_width=True, config=config)
                         #...........................................................................................    
                         # 
                         #            

                         #-------------------------------------------------------------------------------------------------
                         # Get the current year and calculate next year
                                   current_year = datetime.now().year
                                   next_year = current_year + 1

                                   TTM =eps_diluted_ttm
                                   try:
                                        EPS_next_year= float(Earnings_next_yr_in_value)

                                   except Exception as e:
                                        EPS_next_year = 0  # or handle it in a way that suits your application

                                   eps_diluted_annual_10 = ["$ {:.2f}".format(value) for value in eps_diluted_annual_10_unpacked]

                                   data = pd.DataFrame({
                                   #'Date': date_annual+ ['TTM', '2025'],
                                   'Date': date_annual + ['TTM', str(next_year)],
                                   'EPS': eps_diluted_annual_10 + [f"$ {TTM:.2f}", f"$ {EPS_next_year:.2f}"]
                                   })

                                   # Create a Streamlit app
                                   data['EPS_float'] = data['EPS'].str.replace('$', '').astype(float)

                                   # Create a Plotly Express bar chart with side-by-side bars
                                   
                                   fig1 = px.bar(data, x='Date', y='EPS',
                                             text='EPS',  # Display the value on top of each bar
                                             labels={'value': 'EPS ($)'},  # Include the percentage sign in the label
                                             ) 

                                   fig1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

                                   #streamlit_blue = '#1f77b4'  # This is Streamlit's default blue color
                                   colors = len(date_annual) 
                                   fig1.update_traces(marker_color=colors)

                                   # Update layout for better readability
                                   fig1.update_layout(
                                   xaxis_title="Date",
                                   yaxis_title="EPS ($)",
                                   legend_title="EPS Type",
                                   font=dict(size=12),
                                   yaxis_range=[0, max(data['EPS_float'].max(), TTM, EPS_next_year) * 1.1],
                                   xaxis_type='category' 
                                   )

                                   fig1.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )


                                   shares_diluted_annual21 = ["{:.3f}".format(value/1e9) for value in shares_diluted_annual21_unpacked]

                                   data = pd.DataFrame({
                                   'Date': date_annual_20yrs,
                                   'Shares Outstanding in Billion USD': shares_diluted_annual21,
                                   })

                                   
                                   fig2 = px.bar(data, x='Date', y='Shares Outstanding in Billion USD',
                                             text='Shares Outstanding in Billion USD',  # Display the value on top of each bar
                                             labels={'value': 'Amount($)'},  # Include the percentage sign in the label
                                             )

                                   fig2.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )
                                                                      # Update layout for better readability
                                   fig2.update_layout(
                                   xaxis_type='category' 
                                   )

                                   col1,col2 = st.columns(2)

                                   with col1:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b>10YR EPS: {EPS_Cagr_10}%   5YR: {EPS_5_CAGR}%  EPS(ttm):  {eps_diluted_ttm}    Next YR: {Earnings_next_yr_in_value} ({Earnings_next_yr_in_prozent})
                                        </div>
                                        """, unsafe_allow_html=True)

                                        st.plotly_chart(fig1,use_container_width=True,config=config)

                                   with col2:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b>Share Buyback/dilution past 5 YR: {Shares_outstanding_funf_growth:.2f}% 
                                        </div> 
                                        """, unsafe_allow_html=True)

                                        st.plotly_chart(fig2,use_container_width=True,config=config)
                         #-------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------
                              

                                   
                                        #Price_to_earnings=annual_data['price_to_earnings'][-10:]
                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'Revenue per Share': revenue_per_share_annual_10_unpacked,
                                   })


                                   
                                   fig1 = px.bar(data, x='Date', y='Revenue per Share',
                                                  text='Revenue per Share',  # Display the value on top of each bar
                                                  labels={'value': 'Amount()'},  # Include the percentage sign in the label
                                                  )
 

                                   fig1.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )
                                   fig1.update_layout(
                                   xaxis_type='category' 
                                   )

                         
                              # Extract the last 21 years of dividends per share growth data
                                   
                 

                                 

                                   col1, col2 =st.columns(2)
                                   with col1:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b>Revenue per Share 5 YR CAGR : {Revenue_per_share_5_cagr}%</b>
                                        <b> Current Revenue per Share: {formatted_percentage}</b><br>
                                        <span style='font-family: Calibri; font-style: italic;'>
                                        Revenue per Share (Umsatz pro Aktie) zeigt, wie viel Umsatz pro ausgegebener Aktie erzielt wird                                        </div>
                                             """, unsafe_allow_html=True)

                                        st.plotly_chart(fig1, use_container_width=True,config=config)


                          #-------------------------------------------------------------------------------------------------
                                   try:
                                        ebitda_Margin_annual_10_unpacked = ["{:.2f}%".format(ebitda_Margin_annual_10_unpacked * 100) for ebitda_Margin_annual_10_unpacked in ebitda_Margin_annual_10_unpacked]
                                        ebitda_Margin_annual_5_average = "{:.2f}".format((ebitda_Margin_annual_5_average)*100)
                                        EBITDA_MARGIN_TTM ="{:.2f}".format(EBITDA_MARGIN_TTM)
                                   except Exception as e:
                                        ebitda_Margin_annual_10_unpacked = 0.0
                                        ebitda_Margin_annual_5_average = 0.0
                                        EBITDA_MARGIN_TTM = 0.0
                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'EBITDA Margin': ebitda_Margin_annual_10_unpacked,
                                   })

                                   
                                   fig1 = px.bar(data, x='Date', y='EBITDA Margin',
                                                  text='EBITDA Margin',  # Display the value on top of each bar
                                                  labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                                                  #title=f"5 YR Dividend Yield: {Dividend_yield_average}  Current Dividend yield: {Dividend_per_share_yield}"
                                                  )
 
 

                                   fig1.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )
                                   fig1.update_layout(
                                   xaxis_type='category' 
                                   )

                         
                                   
                 

                                   with col2:
                                        st.write(f"""
                                         <div style='text-align: center;'>
                                        <b>5 YR EBITDA-Marge Y/Y: {ebitda_Margin_annual_5_average}%</b>
                                        <b> Current EBITDA-Marge: {EBITDA_MARGIN_TTM}%</b><br>
                                        <span style='font-family: Calibri; font-style: italic;'>
                                        Die EBITDA-Marge zeigt, wie effizient ein Unternehmen Umsatz in operativen Gewinn umwandelt, bevor Zinsen, Steuern, Abschreibungen und Amortisationen berücksichtigt werden.                                        </span>
                                        </div>
                                             """, unsafe_allow_html=True)
                                        st.plotly_chart(fig1, use_container_width=True,config=config)
         
         




                    

                                   try:
                                        value_at_index_6 = dividendPaidInTheLast21Years_unpacked[-6]
                                        value_at_index_last  = dividendPaidInTheLast21Years_unpacked[-1]
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
                                        value_at_index_11  = dividendPaidInTheLast21Years_unpacked[-11]

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
                                   
                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'Dividends': [round(abs(x), 2) for x in Cash_Dividends_paid_Total_annual_10_unpacked],
                                   'Free Cash Flow': FCF_annual_ten_unpacked,
                                   'CapEx': [round(abs(x), 2) for x in Capex_annual_10_unpacked ],
                                   'Net Income': net_income_annual_10_unpacked,
                                   'Operating Cash Flow': Net_Operating_CashFlow_annual_10_unpacked
                                   })

                                   fig = go.Figure()

                                   fig.add_trace(go.Bar(x=data['Date'], y=data['Operating Cash Flow'], name='Operating Cash Flow'))

                                   fig.add_trace(go.Bar(x=data['Date'], y=data['CapEx'], marker_color='black', name='CapEx'))

                                   fig.add_trace(go.Bar(x=data['Date'], y=data['Free Cash Flow'], name='Free Cash Flow'))

                                   fig.add_trace(go.Bar(x=data['Date'], y=data['Net Income'],name='Net Income'))
                                   # Add the Dividends bar plot
                                   fig.add_trace(go.Bar(x=data['Date'], y=data['Dividends'],marker_color='green',  name='Dividends Paid'))
                                   
                                   
                                   
                                   fig.update_layout(
                                   xaxis_type='category' 
                                   )
                                   

                           
                                   fig.update_layout(
                                        barmode='group', xaxis_title='Date',
                                                  #title=title_text
                                                  )
                                                       # Update legend placement
                                   fig.update_layout(
                                   legend=dict (
                                   orientation="h",
                                   yanchor="top",
                                   y=1.1,
                                   xanchor="center",
                                   x=0.5
                                   )
                                   )

                                   fig.update_traces(texttemplate='%{y}', textposition='inside')

                                   fig.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )
                                                                 



                                   st.write(f"""
                                        <div style='text-align: center;'>
                                             <b>10YR Dividend: {Dividend_10_CAGR}%     5YR Dividend: {Dividend_5_CAGR}%       <span style='color:dodgerblue'>10YR FCF CAGR: {FCF_Cagr_10}%    5YR FCF CAGR: {FCF_5_CAGR}%
                                        </div>
                                        """, unsafe_allow_html=True)
                                   
                                   st.plotly_chart(fig,use_container_width=True,config=config)
                                   #with col2:
               #------------------------------------------------------------------------------------------------------------------------------------
                                        
               

                         #-------------------------------------------------------------------------------------------------
                              

                                   Dividend_per_share = ["${:.2f}".format(value * 1) for value in Dividend_per_share_annual10_unpacked]
                                   
                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'Dividend per Share': Dividend_per_share,
                                   })

                                   
                                   fig1 = px.bar(data, x='Date', y='Dividend per Share',
                                                  text='Dividend per Share',  # Display the value on top of each bar
                                                  labels={'value': 'Amount($)'},  # Include the percentage sign in the label
                                                  )


                                   fig1.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )
                                   fig1.update_layout(
                                   xaxis_type='category' 
                                   )

                         
                                   Dividends_per_share_growth_average_annual_10 = "{:.2f}%".format((sum(Dividends_per_share_growth_annual10_unpacked)/len(Dividends_per_share_growth_annual10_unpacked)*100))
                                   Dividends_per_share_growth_last_5_years_growth = "{:.2f}%".format((sum(Dividends_per_share_growth_annual10_unpacked[-5:])/len(Dividends_per_share_growth_annual10_unpacked[-5:])*100))  # Extract last 5 years
                                   Dividends_per_share_growth_annual_10 = ["{:.2f}%".format(value * 100) for value in Dividends_per_share_growth_annual10_unpacked]


                                   # Create a DataFrame
                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'Dividend per Share growth': Dividends_per_share_growth_annual_10,
                                   })



                                   # Create a Plotly Express bar chart
                                   fig2 = px.bar(data, x='Date', y='Dividend per Share growth',
                                             text='Dividend per Share growth',  # Corrected the column name
                                             labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                                             )

                                   fig2.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )

                                   fig2.update_layout(
                                   xaxis_type='category' 
                                   )

                                   col1, col2 =st.columns(2)
                                   with col1:
                                        st.write(f"""
                                         <div style='text-align: center;'>
                                        <b>5 YR Dividend Yield: {Dividend_yield_average}  Current Dividend yield: {Dividend_per_share_yield}
                                        </div>
                                        """, unsafe_allow_html=True)

                                        st.plotly_chart(fig1, use_container_width=True,config=config)
                                   with col2:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b> 10 YR Dividend per Share growth Y/Y: {Dividends_per_share_growth_average_annual_10} 5 YR Y/Y: {Dividends_per_share_growth_last_5_years_growth}
                                        </div>
                                        """, unsafe_allow_html=True)
                                        st.plotly_chart(fig2, use_container_width=True,config=config)




                                        #------------------------------------------------------------------------------------------------------------

                                   try:
                                        ROIC_annual_10years = ["{:.2f}%".format(ROE_annual_10_unpacked * 100) for ROE_annual_10_unpacked in ROE_annual_10_unpacked]
                                   except Exception as e:
                                        ROIC_annual_10years = 0.0

                              
                                        
                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'ROIC': ROIC_annual_10years,
                                   })

                         
                                   fig1 = px.bar(data, x='Date', y='ROIC',
                                             text='ROIC',  # Display the value on top of each bar
                                             labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                                             ) 
                                   
                           

                                   fig1.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )

                                   fig1.update_layout(
                                   xaxis_type='category' 
                                   )


                                   try:
                                        ROE_annual_10years = ["{:.2f}%".format(ROE_annual_10_unpacked * 100) for ROE_annual_10_unpacked in ROE_annual_10_unpacked]
                                   except Exception as e:
                                        ROE_annual_10years = 0.0
                                        
                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'ROE': ROE_annual_10years,
                                   })


                              
                                   fig2 = px.bar(data, x='Date', y='ROE',
                                             text='ROE',  # Display the value on top of each bar
                                             labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                                             ) 
                                   
   

                                   fig2.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )

                                   fig2.update_layout(
                                   xaxis_type='category' 
                                   )

                                   col1, col2 = st.columns(2)
                                   with col1:
                                        st.write(f"""
                                         <div style='text-align: center;'>
                                        <b>5 YR ROIC Y/Y: {Average_ROIC_funf}</b>
                                        <b> Current ROIC: {ROIC_TTM}%</b><br>
                                        <span style='font-family: Calibri; font-style: italic;'>
                                        Indikator für die Fähigkeit eines Unternehmens, Renditen für das investierte Kapital zu erwirtschaften.(Investiertes Kapital = Summe von Eigenkapital und Fremdkapital)
                                        </span>
                                        </div>
                                             """, unsafe_allow_html=True)

                                        st.plotly_chart(fig1,use_container_width=True,config=config)

                                   with col2:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b>5 YR ROE Y/Y: {five_ROE}% Current ROE: {ROE_ttm}</b><br>
                                        <span style='font-family: Calibri; font-style: italic;'>
                                        Indikator für die Fähigkeit eines Unternehmens, Renditen für das investierte Kapital zu erwirtschaften.(Investiertes Kapital = Fremdkapital)
                                        </span>
                                        </div>
                                             """, unsafe_allow_html=True)
                                        st.plotly_chart(fig2,use_container_width=True,config=config)
               #-------------------------------------------------------------------------------------------------

          
                                   
                                   gross_margin_annual10 = ["{:.2f}%".format(gross_margin_annual10_unpacked * 100) for gross_margin_annual10_unpacked in gross_margin_annual10_unpacked]
                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'Gross Margin': gross_margin_annual10,
                                   })

                                   fig1 = px.bar(data, x='Date', y='Gross Margin',
                                             text='Gross Margin',  # Display the value on top of each bar
                                             labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                                             #title=title_text
                                             ) 


                                   fig1.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )

                                   fig1.update_layout(
                                   xaxis_type='category' 
                                   )

                                   
                                   Operating_Margin_10_annual = ["{:.2f}%".format(operating_margin_annual10_unpacked * 100) for operating_margin_annual10_unpacked in operating_margin_annual10_unpacked]
                                   
                                        
                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'Operating Margin': Operating_Margin_10_annual,
                                   })
                                   col1, col2 = st.columns(2)
                                   # Create the figure without a title
                                   fig2 = px.bar(data, x='Date', y='Operating Margin',
                                             text='Operating Margin',  # Display the value on top of each bar
                                             labels={'value': 'Amount(%)'}  # Include the percentage sign in the label
                                             )
 

                                   fig2.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )
                                        
                                   fig2.update_layout(
                                   xaxis_type='category' 
                                   )

                              #col1, col2 = st.columns(2)
                                   with col1:
                                        st.write(f"""
                                         <div style='text-align: center;'>
                                        <b>5 YR Gross Margin Y/Y: {five_yrs_average_gross_margin}</b>
                                        <b> Current Gross Margin: {average_gross_margin_quater1}</b><br>
                                        <span style='font-family: Calibri; font-style: italic;'>
                                        Die Bruttogewinnmarge ist der Gewinn, der nach Abzug der Herstellkosten (COGS) vom Umsatz übrig bleibt.
                                        </span>
                                        </div>
                                             """, unsafe_allow_html=True)

                                        st.plotly_chart(fig1,use_container_width=True,config=config)      


                                   with col2:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b>5 YR Operating Margin Y/Y: {five_yrs_average_operating_margin}</b>
                                        <b> Current Operating Margin: {average_operating_margin1_quarter}</b><br>
                                        <span style='font-family: Calibri; font-style: italic;'>
                                        Die Operative Marge ist der Gewinn, der nach Abzug der Herstellkosten (COGS) 
                                        und der Betriebskosten (wie Material-, Produktions-, Verwaltungs- und 
                                        Vertriebskosten) vom Umsatz übrig bleibt.
                                        </span>
                                        </div>
                                             """, unsafe_allow_html=True)
                                        st.plotly_chart(fig2,use_container_width=True,config=config)


               #------------------------------------------------------------  
                                   try:
                                        Net_income_margin_annual10_ = ["{:.2f}%".format(Net_income_margin_10_unpacked * 100) for Net_income_margin_10_unpacked in Net_income_margin_10_unpacked]
                                   except Exception as e:
                                        Net_income_margin_annual10_ = 0.0
                                        
                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'Net Profit Margin': Net_income_margin_annual10_,
                                   })


                                   fig1 = px.bar(data, x='Date', y='Net Profit Margin',
                                             text='Net Profit Margin',  # Display the value on top of each bar
                                             labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                                             #title=title_text
                                             )

                                   fig1.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )

                                   fig1.update_layout(
                                   xaxis_type='category' 
                                   )

                                   try:
                                        FCF_Margin_annual10 = ["{:.2f}%".format(FCF_Margin_annual_10unpacked * 100) for FCF_Margin_annual_10unpacked in FCF_Margin_annual_10unpacked]
                                   except Exception as e:
                                        FCF_Margin_annual10 = 0.0
                                        
                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'FCF Margin': FCF_Margin_annual10,
                                   })

                                   
                              
                                   fig2 = px.bar(data, x='Date', y='FCF Margin',
                                             text='FCF Margin',  # Display the value on top of each bar
                                             labels={'value': 'Amount(%)'},  # Include the percentage sign in the label
                                             ) 
                               

                                   fig2.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )

                                   fig2.update_layout(
                                   xaxis_type='category' 
                                   )

                                   col1, col2 = st.columns(2)
                                   with col1:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b>5 YR FCF Margin Y/Y: {FCF_Margin_5}%</b>
                                        <b> Current FCF Margin: {FCF_Margin_1:.2f}%</b><br>
                                        <span style='font-family: Calibri; font-style: italic;'>
                                        Die FCF-Marge (freier Cashflow) ist ein Indikator dafür, wie effizient ein Unternehmen seinen Umsatz in freien Cashflow umwandelt.
                                        </span>
                                        </div>
                                             """, unsafe_allow_html=True)

                                        st.plotly_chart(fig2,use_container_width=True,config=config)

                                   with col2:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b>5 YR Net Profit Margin Y/Y: {five_yrs_Nettomarge}% </b>
                                        <b> Current Net Profit Margin: {Net_margin_ttm}</b><br>
                                        <span style='font-family: Calibri; font-style: italic;'>
                                        Die Nettogewinnmarge ist der Gewinn, der nach Abzug der Herstellkosten (COGS), Betriebskosten, Zinsen, Steuern und außerordentlichen Posten vom Umsatz übrig bleibt.</span>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        st.plotly_chart(fig1,use_container_width=True,config=config)
               
               #........  ...................................................................................................................               
                                        #Price_to_earnings=annual_data['price_to_earnings'][-10:]
                                   Price_to_earnings = ["{:.2f}".format(value) for value in Price_to_earnings_annual_10_unpacked]
                                   #Price_to_earnings = "{:.2f}".format((Price_to_earnings))
                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'PE Ratio': Price_to_earnings,
                                   })
                                   
                                   fig21 = px.bar(data, x='Date', y='PE Ratio',
                                             text ='PE Ratio',
                                             labels={'value': 'Ratio'},
                                             )  # Use 'group' to display bars side by side

                                                                                                                                            
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

                                   fig21.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )

                                   fig21.update_layout(
                                   xaxis_type='category' 
                                   )


                                   Price_to_fcf_history = ["{:.2f}".format(value) for value in price_to_fcf_annual21_unpacked]
                                   #Price_to_earnings = "{:.2f}".format((Price_to_earnings))
                                   data = pd.DataFrame({
                                   'Date': date_annual_20yrs,
                                   'Price/FCF': price_to_fcf_annual21_unpacked,
                                   })

                                         
                                   fig22 = px.bar(data, x='Date', y='Price/FCF',
                                             text ='Price/FCF',
                                             labels={'value': 'ratio'},
                                             #title=f'Market Cap:  Current Market Cap: {Marketcap_in_Billion}'
                                             )

                                                                                                                                            
                                   fig22.add_shape(
                                   type='line',
                                   x0=data['Date'].min(),  # Adjust this based on your data
                                   x1=data['Date'].max(),  # Adjust this based on your data
                                   y0=pfcf_ten,
                                   y1=pfcf_ten,
                                   line=dict(color='red', width=2, dash='dash'),
                                   yref='y',
                                   )
                                   
                                   fig22.add_annotation(text=f'',
                                   xref='paper',  # Set xref to 'paper' for center alignment
                                   yref='paper',  # Set yref to 'paper' for center alignment
                                   x=0.10,  # Adjust to center horizontally
                                   y=0.7,  # Adjust to center vertically
                                   showarrow=False,  # Remove the arrow
                                   font=dict(color='red'),  # Set font color to red
                                   )          

                                   fig22.update_layout(
                                        dragmode=False,  # Disable dragging for zooming
                                   )


                                   fig22.update_layout(
                                   xaxis_type='category' 
                                   )

                                   col2, col3 =st.columns(2)
                                   with col2:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b><span style='color:dodgerblue'>10 YR P/E:</span> {average_PE_historical}  <span style='color:dodgerblue'>5 YR P/E: </span> {pe_five_}  <span style='color:dodgerblue'>Current P/E: </span> {pe_ttm}  <span style='color:dodgerblue'>Forward P/E:</span>  {forwardPE}
                                        </div>
                                        """, unsafe_allow_html=True)
                                        st.plotly_chart(fig21,use_container_width=True,config=config)

                                   with col3:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b><span style='color:dodgerblue'>10YR Price/FCF:</span>  {pfcf_ten}  <span style='color:dodgerblue'>5YR Price/FCF:  </span> {pfcf_funf}  <span style='color:dodgerblue'>Current Price/FCF:</span>  {pfcf_ttm}
                                        </div>
                                        """, unsafe_allow_html=True)
                                        st.plotly_chart(fig22,use_container_width=True,config=config)


                                   #-------------------------------------------------------------------------------------------------


                                   data = pd.DataFrame({
                                   'Date': date_annual,
                                   'Price/Tangible Book Value': Price_to_tangible_book_annual_10_unpacked,
                                   })


                                   # Create a Plotly Express bar chart with side-by-side bars
                                   fig11 = px.bar(data, x='Date', y='Price/Tangible Book Value', 
                                             text ='Price/Tangible Book Value',              
                                             labels={'value': 'Ratio'},
                                             )  # Use 'group' to display bars side by side
                                   
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

                                   fig11.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )

                                   fig11.update_layout(
                                   xaxis_type='category' 
                                   )

                                   #-------------------------------------------------------------------------------------------------
 
                                   data = pd.DataFrame({
                                   'Date': list(date_annual),
                                   'Price/Book Value': Price_to_book_10_annual_unpacked,
                                   })

                                   # Create a Streamlit app
                                   #st.title('Free Cash Flow and Revenue Data')

                                   # Create a Plotly Express bar chart with side-by-side bars

                                   fig12 = px.bar(data, x='Date', y='Price/Book Value',
                                             text ='Price/Book Value',  
                                             labels={'value': 'Ratio'},

                                             )
                                   

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

                                   fig12.update_layout(
                                   dragmode=False,  # Disable dragging for zooming
                                   )

                                   fig12.update_layout(
                                   xaxis_type='category' 
                                   )

                                   # Display the chart using Streamlit
                                   #st.plotly_chart(fig12,use_container_width=True,config=config)


                                   col1, col2 =st.columns(2)
                                   with col1:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b>10 P/TBV: {Average_Price_to_tangible_book}  Current P/TBV: {PTBVPS:.2f}
                                        </div>
                                        """, unsafe_allow_html=True)
                                        st.plotly_chart(fig11,use_container_width=True,config=config)
                                        
                                   with col2:
                                        st.write(f"""
                                        <div style='text-align: center;'>
                                        <b>10 P/BV: {average_price_to_book}  Current P/B: {PBVPS:.2f}
                                        </div>
                                        """, unsafe_allow_html=True)
                                        st.plotly_chart(fig12,use_container_width=True,config=config)
               #.........


                                        

               #...........................................................................................................
  


               with st.container():
                    use_container_width=True
                    with Retirement_Calculator:


                         st.image('DCF Update.png', caption = 'DCF Calculation')

                         st.image('Terminal-Value.png', caption = 'Terminal Value')


                         st.image('Multiples of Earnings.png', caption = "Multiple of Earnings Valuation")



                         st.image('NPV.png', caption='Net Present Value')



                         st.image('DDM.png', caption='Das Dividend Discount Model basiert auf der Annahme, dass der heutige Kurs einer Aktie dem Barwert aller zukünftigen Dividenden entspricht, wenn diese auf den heutigen Wert abgezinst werden') 

                         st.image('CAGR.png',caption='CAGR')  

                         

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

                    
                                        

               with st.container():
                    with news:
                         def fetch_stock_news(stock_info):
               
                              try:
                                   news = stock_info.news[:10]
                                   return news  # Get the top ten news articles
                              except Exception as e:
                                   st.error(f"No news available for this stock: {e}")
                                   return None
                    
                         def display_news(stock_info):
                              ticker = stock_info.ticker  # Assuming stock_info is from yf.Ticker(ticker)
                              if f'{ticker}_news' not in st.session_state:
                                   # Fetch news and store it in session state
                                   st.session_state[f'{ticker}_news'] = fetch_stock_news(stock_info)
                              
                              news = st.session_state[f'{ticker}_news']
                              try:
                                   if news:
                                        with st.container():
                                             for i, item in enumerate(news, 1):
                                                  headline = item['title'] #december
                                                  link = item['link']
                                                  st.write(f"Headline {i}: {headline}")
                                                  st.write(f"[Read more]({link})")
                                   else:
                                        st.error("No news available for this stock.")
                              except Exception as e:
                                   st.error("No news available for this stock.")


                         # Display the news
                         display_news(stock_info)

          



     
          else:
               with middle:
               # Your existing login/signup form code goes here
               #choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
               #choice = st.selectbox('Login/Signup', ['Login', 'Sign up'], key='login_choice')
                    choice = st.selectbox('Login', ['Login'],key='login_choice')
                    #choice = st.radio('', ['Login', 'Sign up'], horizontal=True)
                    st.markdown('<p style="color: green; font-size: 18px;">Sign up button will be activated soon........</p>', unsafe_allow_html=True)


                    with st.form(key='auth_form'):

                         email = st.text_input('Email Address')
                         password = st.text_input('Password', type='password')
                         st.session_state.email_input = email
                         st.session_state.password_input = password
                              
                         if choice == 'Sign up':
                              username = st.text_input("Enter your unique username")
                              #submit_button = st.form_submit_button(label='Create my account', key='signup_submit')
                              submit_button = st.form_submit_button(label='Login')


                              
                              #if st.button('Create my account'):
                              if submit_button:

                                   try:
                                   # user = auth.create_user(email = email, password = password,uid=username)
                                        user = sign_up_with_email_and_password(email=email,password=password,username=username)
                                        if user:
                                             st.success('Account created successfully! Please login using your email and password.')
                                             st.balloons()
                                        else:
                                             st.error('Failed to create account. Please try again.')
                                   except Exception as e:
                                        st.error(f'An error occurred: {str(e)}')

                         #else:
                         else:
                              submit_button = st.form_submit_button(label='Login')
                             

                              if submit_button:
                                   st.session_state.email_input = email
                                   st.session_state.password_input = password
                                   login()
                              
               with middle:
                    if st.button('Forgot Password', key='forgot_password'):
                         forget()

                         
                         
               #if st.session_state.signout:
               #              st.text('Name '+st.session_state.username)
                              #st.text('Email:id: '+st.session_state.useremail)
                              #st.button('Sign out', on_click=t) 


     if __name__ == "__main__":     
          app()
                              
 
@st.fragment
def display_disclaimer():
     disclaimer = """
               The information provided on this website is intended for informational purposes only and does not constitute financial advice, investment recommendations, or a solicitation to buy or sell any securities. The content and data presented on this website are not tailored to your specific investment goals, financial situation, or risk tolerance. You should always consult with a qualified financial advisor before making investment decisions.
               """


     custom_css = """
     <style>
     body { font-family: serif; }
     </style>
     """

     # Display the disclaimer with custom styling
     st.markdown("<u><h3 style='color:#FF4B4B;'>Disclaimer</h3></u>", unsafe_allow_html=True)
     st.write(disclaimer)
     st.markdown(custom_css, unsafe_allow_html=True)
#####################################################################
if selected == "Contacts":
     st.write("You can reach us at: verstehdieaktie@gmail.com")


     # #st.title('Welcome to :violet[Pondering] :sunglasses:')

     # def app():
     #      st.title('Welcome to Verstehdieaktie')
     #      choice = st.selectbox('Login/Signup',['Login','Sign up'])


     #      def f(): 
     #           try:
     #                user = auth.get_user_by_email(email)
     #                # print(user.uid)
     #                # st.session_state.username = user.uid
     #                # st.session_state.useremail = user.email

     #                #userinfo = sign_in_with_email_and_password(st.session_state.email_input,st.session_state.password_input)
     #                #st.session_state.username = userinfo['username']
     #                #st.session_state.useremail = userinfo['email']

                    
     #                #global Usernm
     #                #Usernm=(userinfo['username'])
                    
     #                #st.session_state.signedout = True
     #                #st.session_state.signout = True  
     #                st.write('Login successful')  

                    
     #           except: 
     #                st.warning('Login Failed')

     #      if choice == 'Login':
     #           email = st.text_input('Email Address')
     #           paswword = st.text_input('Password',type = 'password')

     #           st.button('Login',on_click=f)

     #      else:
     #           email = st.text_input('Email Address')
     #           password = st.text_input('Password',type = 'password')
     #           username = st.text_input('Enter your unique password')

     #           if st.button('Create your account'):
     #                user = auth.create_user (email=email,password =password,uid=username)

     #                st.success ('Account created successfully!')
     #                st.markdown('please login using your email and password')
     #                st.balloons()
     # app()


##############################################################################
     # client_secrets_file = "client_secret.json"
     # SCOPES=[
     #      "openid",
     #      "https://www.googleapis.com/auth/userinfo.email",
     #      "https://www.googleapis.com/auth/userinfo.profile",
     #      "https://www.googleapis.com/auth/calendar.events.readonly",
     # ]
     # #REDIRECT_URI = "http://localhost:8501/callback"
     # REDIRECT_URI = "https://www.verstehdieaktie.com/callback"
    
     # #authorization_url = flow.authorization_url(prompt="consent")
     # #st.session_state.flow =flow
     # #st.redirect(authorization_url)

     # def create_flow():
     #      return Flow.from_client_secrets_file(
     #           client_secrets_file,
     #           scopes=SCOPES,
     #           redirect_uri=REDIRECT_URI
     #      )


     # def login_callback():
     #      flow = create_flow()
     #      authorization_url, _ = flow.authorization_url(prompt="consent")
     #      st.session_state.flow = flow
     #      st.session_state.auth_url = authorization_url

     # def handle_callback():
     #      try:
     #           flow = st.session_state.flow
     #           flow.fetch_token(code=st.query_params['code'])
     #           credentials = flow.credentials
     #           st.session_state.credentials = credentials
     #           st.write("Successfully authenticated!")
     #      except Exception as e:
     #           st.error(f"An error occurred: {str(e)}")


     # if 'code' in st.query_params:
     #      handle_callback()
     # elif 'credentials' not in st.session_state:
     #      if 'auth_url' not in st.session_state:

     #           if st.button("Login with Google", type="primary"):
     #                login_callback()
     #                # Use JavaScript to open a new tab with the auth URL
     #                st.markdown(f'<script>window.open("{st.session_state.auth_url}", "_blank");</script>', unsafe_allow_html=True)
     #      else:
     #           st.write("Please click on the link below to authorize the application:")
     #           st.markdown(f"[Authorize here]({st.session_state.auth_url})")
     # else:
     #      st.write("Already logged in. You can proceed with using the Google Calendar API.")


  #############################################################################   Firebase  
  # 
  # 
  # 
  # def display_login_signup():


     serializer = URLSafeTimedSerializer("secret_key") 

     def app():

     # Usernm = []
          st.title('Welcome to verstehdieaktie')
          

          if 'username' not in st.session_state:
               st.session_state.username = ''
          if 'useremail' not in st.session_state:
               st.session_state.useremail = ''

           #from perplexity    
          if 'is_logged_in' not in st.session_state:
               st.session_state.is_logged_in = False
         # if "signedout" not in st.session_state:
           #    st.session_state["signedout"] = False
         # if 'signout' not in st.session_state:
          #     st.session_state['signout'] = False 

          # Check for login token in query parameters

              
          if 'needs_rerun' not in st.session_state:
               st.session_state.needs_rerun = False

          #     # Check for login token in query parameters or session state
          # if 'login_token' in st.query_params:
          #      st.session_state.login_token = st.query_params['login_token']

          # Retrieve current query parameters
          query_params = st.experimental_get_query_params()

          # Check if 'login_token' is in query parameters
          if 'login_token' in query_params:
          # Save the token to session state and remove it from the URL
               st.session_state.login_token = query_params['login_token'][0]
          
          # Remove the token from the query parameters and update the URL
               del query_params['login_token']
               st.experimental_set_query_params(**query_params)  # Apply the updated query parameters

               

          if 'login_token' in st.session_state:
               try:
                    user_data = serializer.loads(st.session_state.login_token, max_age=86400)  # 24-hour expiry
                    st.session_state.username = user_data['username']
                    st.session_state.useremail = user_data['email']
                    st.session_state.is_logged_in = True

               except Exception:
                    st.warning("Login session expired. Please log in again.")
                    del st.session_state.login_token



          # Function to sign up with email and password
          def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
               try:
                    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
                    payload = {
                         "email": email,
                         "password": password,
                         "returnSecureToken": return_secure_token
                    }
                    if username:
                         payload["displayName"] = username 
                    payload = json.dumps(payload)
                    r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
                    # try:
                    #      return r.json()['email']
                    # except:
                    #      st.warning(r.json())
                    return r.json().get('email', None)

               except Exception as e:
                    st.warning(f'Signup failed: {e}')

          # Function to sign in with email and password
          def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
               rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

               try:
                    payload = {
                         "returnSecureToken": return_secure_token,
                         "email": email,
                         "password": password
                    }
                    payload = json.dumps(payload)
                    r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
                    data = r.json()
                    user_info = {
                         'email': data['email'],
                         'username': data.get('displayName')  # Retrieve username if available
                    }
                    return user_info
                  
               except Exception as e:
                    st.warning(f'Signin failed: {e}')

#######################################################################################################
          # Login function
          def login():
               userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)

               if userinfo:
                    st.session_state.username = userinfo['username']
                    st.session_state.useremail = userinfo['email']
                    st.session_state.is_logged_in = True

                    # Create a secure login token
                    login_token = serializer.dumps({'username': userinfo['username'], 'email': userinfo['email']})
                    st.session_state.login_token = login_token
                    # Update query parameters
                    st.query_params['login_token'] = login_token
                    st.session_state.needs_rerun = True
               else:
                    st.warning('Login Failed')
###########################################################################

          def logout():
               for key in ['username', 'useremail', 'is_logged_in', 'login_token']:
                    if key in st.session_state:
                         del st.session_state[key]
               st.query_params.clear()
               #st.rerun()
               st.session_state.needs_rerun = True
############################# email reset##########################################################
          def reset_password(email):
               try:
                    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
                    payload = {
                         "email": email,
                         "requestType": "PASSWORD_RESET"
                    }
                    payload = json.dumps(payload)
                    r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
                    return r.status_code == 200, r.json().get('error', {}).get('message')

               except Exception as e:
                    return False, str(e)


#####################################################email reeset ########################################################
          def forget():
               email = st.text_input('Email')
               if st.button('Send Reset Link'):
                    print(email)
                    success, message = reset_password(email)
                    if success:
                         st.success("Password reset email sent successfully.")
                    else:
                         st.warning(f"Password reset failed: {message}") 
               
 #############################################################################################################
                   # Check if we need to rerun the app
          if st.session_state.needs_rerun:
               st.session_state.needs_rerun = False
               st.rerun()

               # Main app logic 
          if st.session_state.is_logged_in:
               st.success(f"Welcome, {st.session_state.username}!")
               st.text('Email_id: ' + st.session_state.useremail)
               st.button('Sign out', on_click=logout)

               # Add any other objects you want to show only when logged in
               st.write("This is some content only visible to logged-in users.")
               # For example, you could add a data visualization or a form here
          else:
               # Your existing login/signup form code goes here
              # choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
               choice = st.radio('Login/Signup', ['Login', 'Sign up'])

               email = st.text_input('Email Address')
               password = st.text_input('Password', type='password')
               st.session_state.email_input = email
               st.session_state.password_input = password
                         
               if choice == 'Sign up':
                    username = st.text_input("Enter  your unique username")
                    
                    if st.button('Create my account'):
                         try:
                         # user = auth.create_user(email = email, password = password,uid=username)
                              user = sign_up_with_email_and_password(email=email,password=password,username=username)
                              if user:
                                   st.success('Account created successfully! Please login using your email and password.')
                                   st.balloons()
                              else:
                                   st.error('Failed to create account. Please try again.')
                         except Exception as e:
                              st.error(f'An error occurred: {str(e)}')

               else:
                    if st.button('Login'):
                         login()
                    if st.button('Forgot Password'):
                         forget()

                    
                    
          #if st.session_state.signout:
           #              st.text('Name '+st.session_state.username)
                         #st.text('Email:id: '+st.session_state.useremail)
                         #st.button('Sign out', on_click=t) 
                    

     #if __name__ == "__main__":     
      #    app()
                              
 

###############################################################################################################
# def main():
#      if 'authenticated' not in st.session_state:
#           st.session_state.authenticated = False

#               # Check if this is a callback from Google OAuth
#      if 'code' in st.query_params:
#           handle_callback()
#      elif not st.session_state.authenticated:
#           show_login_button()
#      else:
#           show_authenticated_content()

# def handle_callback():
#      if 'flow' not in st.session_state:
#           st.error("Authentication flow not found. Please start from the beginning.")
#           return
     
#      try:
#           flow = st.session_state.flow
#           flow.fetch_token(code=st.query_params.get('code'))
#           credentials = flow.credentials
#           st.session_state.credentials = credentials
          
#           st.session_state.authenticated = True

#                # Verify the credentials
#           request = google.auth.transport.requests.Request()
#           credentials.refresh(request)
#           st.write ("This is me")
#           st.success("Successfully authenticated!")
#           st.experimental_rerun()

#                   # Add a link button to return to the main page
#           #st.link_button("Return to Main Page", url="http://localhost:8501", type="primary")


#      except Exception as e:
#         st.error(f"An error occurred during authentication: {str(e)}")
#         st.error("Please try logging in again.")


# def show_login_button():
#      flow = Flow.from_client_secrets_file(
#           'client_secret.json',
#           scopes=[
#                "openid",
#                "https://www.googleapis.com/auth/userinfo.email",
#                "https://www.googleapis.com/auth/userinfo.profile",
#                "https://www.googleapis.com/auth/calendar.events.readonly",
#           ]
#      )
     
#      #flow.redirect_uri =  'https://www.verstehdieaktie.com/callback'
#      flow.redirect_uri =  'http://localhost:8501/callback'

#      #authorization_url, _ = flow.authorization_url(prompt='consent')
#      authorization_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

#      #st.markdown(f'Please [click here]({authorization_url}) to log in with Google')

#      st.session_state.flow = flow

#      #return authorization_url
# #auth_url = login_callback()


#      st.link_button(
#           "Login with Google",
#           url=authorization_url,

#           type="primary",
#           #on_click=login_callback,
#           #use_container_width=True

#           )

# def show_authenticated_content():
#     st.write("You are authenticated!")
#     # Add your authenticated content here

# if __name__ == "__main__":
#     main()




st.markdown("---")
display_disclaimer()
current_year = datetime.now().year
 
st.markdown(f'&copy; {2023} - {current_year} Verstehdieaktie. All rights reserved', unsafe_allow_html=True)

