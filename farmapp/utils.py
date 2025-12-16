import io
import base64
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import os


def create_chart_image():
    """Generate a bar chart showing Income vs Expense"""
    fig, ax = plt.subplots(figsize=(8, 4), facecolor='white')
    categories = ['Income', 'Expense']
    values = [25000, 15000]
    colors = ['#28a745', '#dc3545']

    bars = ax.bar(categories, values, color=colors, width=0.6, edgecolor='black', linewidth=1.5)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'₹{int(height)}',
                ha='center', va='bottom', fontweight='bold', fontsize=12)

    ax.set_ylabel('Amount (₹)', fontweight='bold')
    ax.set_title('Income vs Expense Overview', fontweight='bold', fontsize=14)
    ax.set_ylim(0, max(values) * 1.2)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    # Save to bytes
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    buffer.seek(0)
    plt.close(fig)

    # Convert to base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    return f'data:image/png;base64,{image_base64}'


def generate_pdf(report):
    """Generate PDF from farm report using xhtml2pdf"""

    # Calculate financials
    expenses = list(report.expenses.all())
    incomes = list(report.incomes.all())

    total_expense = sum(e.amount for e in expenses)
    total_income = sum(i.amount for i in incomes)
    profit_loss = total_income - total_expense
    cost_per_acre = total_expense / report.total_acres if report.total_acres else 0

    # Create merged ledger
    ledger = []
    for expense in expenses:
        ledger.append({
            'date': expense.date,
            'particulars': expense.category,
            'type': 'Expense',
            'description': expense.description or '',
            'amount': expense.amount,
        })
    for income in incomes:
        ledger.append({
            'date': income.date,
            'particulars': income.category,
            'type': 'Income',
            'description': income.description or '',
            'amount': income.amount,
        })
    ledger = sorted(ledger, key=lambda x: x['date'])

    # Generate chart
    chart_image = create_chart_image()

    # Get logo path
    logo_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'gramiq_logo.png')
    logo_data = None
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_data = base64.b64encode(f.read()).decode()

    # Prepare context
    context = {
        'report': report,
        'expenses': expenses,
        'incomes': incomes,
        'total_expense': total_expense,
        'total_income': total_income,
        'profit_loss': profit_loss,
        'cost_per_acre': round(cost_per_acre, 2),
        'ledger': ledger,
        'generated_at': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        'chart_image': chart_image,
        'logo_data': logo_data,
    }

    # Render HTML template
    html_string = render_to_string('pdf_template.html', context)

    # Generate PDF
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html_string.encode("UTF-8")), result)

    if not pdf.err:
        return result.getvalue()
    return None
