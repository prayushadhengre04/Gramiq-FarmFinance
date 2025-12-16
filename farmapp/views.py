from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import FarmReport
from .forms import FarmReportForm, ExpenseFormSet, IncomeFormSet


def create_report_view(request):
    if request.method == 'POST':
        form = FarmReportForm(request.POST)
        expense_formset = ExpenseFormSet(request.POST, prefix='expenses')
        income_formset = IncomeFormSet(request.POST, prefix='incomes')

        if form.is_valid() and expense_formset.is_valid() and income_formset.is_valid():
            report = form.save()

            expenses = expense_formset.save(commit=False)
            for expense in expenses:
                expense.report = report
                expense.save()
            expense_formset.save_m2m()

            incomes = income_formset.save(commit=False)
            for income in incomes:
                income.report = report
                income.save()
            income_formset.save_m2m()

            return redirect('download_pdf', report_id=report.id)
    else:
        form = FarmReportForm()
        expense_formset = ExpenseFormSet(prefix='expenses')
        income_formset = IncomeFormSet(prefix='incomes')

    return render(request, 'farm_form.html', {
        'form': form,
        'expense_formset': expense_formset,
        'income_formset': income_formset
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import FarmReport
from .forms import FarmReportForm, ExpenseFormSet, IncomeFormSet
from .utils import generate_pdf


def create_report_view(request):
    if request.method == 'POST':
        form = FarmReportForm(request.POST)
        expense_formset = ExpenseFormSet(request.POST, prefix='expenses')
        income_formset = IncomeFormSet(request.POST, prefix='incomes')

        if form.is_valid() and expense_formset.is_valid() and income_formset.is_valid():
            report = form.save()

            expenses = expense_formset.save(commit=False)
            for expense in expenses:
                expense.report = report
                expense.save()
            expense_formset.save_m2m()

            incomes = income_formset.save(commit=False)
            for income in incomes:
                income.report = report
                income.save()
            income_formset.save_m2m()

            return redirect('download_pdf', report_id=report.id)
    else:
        form = FarmReportForm()
        expense_formset = ExpenseFormSet(prefix='expenses')
        income_formset = IncomeFormSet(prefix='incomes')

    return render(request, 'farm_form.html', {
        'form': form,
        'expense_formset': expense_formset,
        'income_formset': income_formset
    })


def download_pdf_view(request, report_id):
    report = get_object_or_404(FarmReport, id=report_id)

    # Generate PDF
    pdf_bytes = generate_pdf(report)

    # Return as downloadable PDF
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="farm_report_{report.id}.pdf"'

    return response

