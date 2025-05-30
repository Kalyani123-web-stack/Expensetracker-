from django.http import HttpResponse
from django.shortcuts import render,redirect
from.models import Expense
from .forms import ExpenseForm
import plotly.express as px
import pandas as pd
from django.db.models import Sum


# Create your views here.
def index(request):
    return HttpResponse("Welcome to the Expense Tracker App!")

def add_expense(request):
    if request.method=='POST':
        form=ExpenseForm(request.POST)
        if form.is_valid():
            expense=form.save(commit=False)

            if request.user.is_authenticated:
                expense.user = request.user
                expense.save()
                return redirect('expense_list')
            else:
                return redirect('login')
    else:
        form=ExpenseForm()
    return render(request,'expenses/add_expense.html',{'form':form})


def expense_list(request):
    expenses=Expense.objects.filter(user=request.user)
    return render(request,'expenses/expense_list.html',{'expenses':expenses})


def expense_chart(request):
    expenses=Expense.objects.filter(user=request.user).values('category__name','amount')
    df=pd.DataFrame(expenses)

    if df.empty:
        chart_html = "<h3>No expense data available for chart.</h3>"
    else:
        df = df.groupby('category__name')['amount'].sum().reset_index()
        df.columns = ['Category', 'Total Amount']
        fig = px.bar(df, x='Category', y='Total Amount', title="Expense Distribution by Category",color='Category',color_discrete_sequence=px.colors.qualitative.Pastel)

        fig.update_layout(title_font_size=20,plot_bgcolor='white',paper_bgcolor='white',font=dict(family='Arial',size=14,color='black'),xaxis=dict(showgrid=False,title='Category'),yaxis=dict(showgrid=True,title='Total Amount'))

        fig.update_traces(marker_line_width=1.5,marker_line_color='darkblue',opacity=0.8)





        chart_html = fig.to_html(full_html=False)
    return render(request,'expenses/expense_chart.html',{'chart_html':chart_html})

