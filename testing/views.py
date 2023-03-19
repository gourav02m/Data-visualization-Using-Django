from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import matplotlib.pyplot as plt
# %matplotlib inline
import pandas as pd
import time

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


def index(request):
    return render(request,'index.html')

# def login(request):
#     return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
     return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

# def registration(request):
#     return render(request, 'registration.html')

def pricing(request):
    return render(request, 'pricing.html')





# Create your views here.
def greetings(request):
    return render(request,'home.html')


def search(request):
    if request.method == 'POST':
        state_name = request.POST['search_text'].capitalize()
        state_code_data = pd.read_csv("state_code.csv")
        print(state_code_data.head())
        state_code = state_code_data.loc[state_code_data['State'] == state_name, 'State_code'].iloc[0]
       

     
        # right hand side portion
        state_wise_daily = pd.read_csv("state_wise_daily.csv")
        print(state_wise_daily.head())
        for_confirmed = state_wise_daily.loc[state_wise_daily['Status']=="Confirmed",['Date',state_code]]
        for_confirmed.rename(columns = {state_code: "Confirmed"},inplace=True)

        for_recovered = state_wise_daily.loc[state_wise_daily['Status']=="Recovered",['Date',state_code]]
        for_recovered.rename(columns = {state_code: "Recovered"},inplace=True)

        for_deceased = state_wise_daily.loc[state_wise_daily['Status']=="Deceased",['Date',state_code]]
        for_deceased.rename(columns = {state_code: "Deceased"},inplace=True)

        temp = pd.merge(for_confirmed,for_recovered,on="Date",how="inner")
        final_state_wise = pd.merge(temp,for_deceased,on="Date",how="inner")

        final_state_wise['Active'] = final_state_wise['Confirmed'] - final_state_wise['Recovered'] - final_state_wise['Deceased']

        final_state_wise['cf_Confirmed'] = final_state_wise['Confirmed'].cumsum()
        final_state_wise['cf_Recovered'] = final_state_wise['Recovered'].cumsum()
        final_state_wise['cf_Deceased'] = final_state_wise['Deceased'].cumsum()
        final_state_wise['cf_Active'] = final_state_wise['Active'].cumsum()

        final_state_wise = final_state_wise[['Date','cf_Confirmed','cf_Recovered','cf_Deceased','cf_Active']]

        print(final_state_wise.tail(2))

        total_state_data = final_state_wise.tail(1)

        final_state_wise.Date = pd.to_datetime(final_state_wise.Date)
        final_state_wise.set_index('Date', inplace=True)

        plot = final_state_wise.plot(figsize=(20,10), linewidth=5, fontsize=20,color = ['steelBlue','Green','Red','Orange'])
        plot.set_xlabel('Date', fontsize=20)
        plot.set_ylabel('No. of Cases', fontsize=20)
        plot.set_title(state_name, fontsize=20)
        plot.legend(["Confirmed","Recovered","Death","Active"],fontsize=20)
        fig = plot.get_figure()
        fig.savefig("assets/images/output.png")

        res = render(request,'home.html',{"state_name":state_name,"total_state_data":total_state_data,"img_name":"output.png"})
        return res
