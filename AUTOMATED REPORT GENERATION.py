from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
import csv
from datetime import datetime
import statistics

 
def analyze_data(filename):
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)
            
             
            sales = [float(row['sales']) for row in data]
            dates = [row['date'] for row in data]
            products = [row['product'] for row in data]
            
             
            analysis = {
                'total_sales': sum(sales),
                'average_sale': statistics.mean(sales),
                'max_sale': max(sales),
                'min_sale': min(sales),
                'total_transactions': len(sales),
                'top_product': max(set(products), key=products.count)
            }
            return data, analysis
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None, None
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return None, None

 
def create_pdf_report(data, analysis, output_filename):
    if not data or not analysis:
        return False
        
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
     
    elements.append(Paragraph("Sales Analysis Report", styles['Heading1']))
    elements.append(Spacer(1, 12))
    
     
    current_date = datetime.now().strftime("%B %d, %Y")
    elements.append(Paragraph(f"Generated on: {current_date}", styles['Normal']))
    elements.append(Spacer(1, 24))
    
     
    elements.append(Paragraph("Summary Statistics", styles['Heading2']))
    summary_data = [
        ["Metric", "Value"],
        ["Total Sales", f"${analysis['total_sales']:,.2f}"],
        ["Average Sale", f"${analysis['average_sale']:,.2f}"],
        ["Maximum Sale", f"${analysis['max_sale']:,.2f}"],
        ["Minimum Sale", f"${analysis['min_sale']:,.2f}"],
        ["Total Transactions", analysis['total_transactions']],
        ["Top Product", analysis['top_product']]
    ]
    
    summary_table = Table(summary_data)
    summary_table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    elements.append(summary_table)
    elements.append(Spacer(1, 24))
    
     
    elements.append(Paragraph("Transaction Details", styles['Heading2']))
    table_data = [["Date", "Product", "Sales"]] + [
        [row['date'], row['product'], f"${float(row['sales']):,.2f}"] 
        for row in data
    ]
    
    detail_table = Table(table_data)
    detail_table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    elements.append(detail_table)
    
     
    doc.build(elements)
    return True

 
def main():
    input_file = "sales_data.csv"
    output_file = "sales_report.pdf"
    
     
    sample_data = """date,product,sales
2025-03-01,Widget A,100.50
2025-03-02,Widget B,75.25
2025-03-03,Widget A,150.75
2025-03-04,Widget C,200.00"""
    
    with open(input_file, 'w') as f:
        f.write(sample_data)
    
     
    data, analysis = analyze_data(input_file)
    if data and analysis:
        success = create_pdf_report(data, analysis, output_file)
        if success:
            print(f"Report successfully generated: {output_file}")
        else:
            print("Failed to generate report")

if __name__ == "__main__":
    main()
