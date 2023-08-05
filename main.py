import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

filepaths = glob.glob("invoices/*.xlsx")

for filepath in filepaths:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    filename = Path(filepath).stem
    invoice_nr, date = filename.split("-")

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1)

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

    df = pd.read_excel(filepath, sheet_name="Sheet 1")

    # add header
    colunas = [item.replace("_", " ").title() for item in df.columns]
    pdf.set_font(family="Times", size=10, style="B")
    pdf.cell(w=30, h=8, txt=colunas[0], border=1)
    pdf.cell(w=70, h=8, txt=colunas[1], border=1)
    pdf.cell(w=33, h=8, txt=colunas[2], border=1)
    pdf.cell(w=30, h=8, txt=colunas[3], border=1)
    pdf.cell(w=30, h=8, txt=colunas[4], border=1, ln=1)

    # add rows to the table
    for index, row in df.iterrows():
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1)
        pdf.cell(w=70, h=8, txt=str(row["product_name"]), border=1)
        pdf.cell(w=33, h=8, txt=str(row["amount_purchased"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)

    total = df["total_price"].sum()

    # add total in table
    pdf.cell(w=163, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt=str(total), border=1, ln=1)

    # add total sum sentence
    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=30, h=10, txt=f"The total price is {total}", ln=1)

    # add company name and logo
    pdf.set_font(family="Times", size=14, style="B")
    pdf.cell(w=27, h=10, txt="PythonHow")
    pdf.image("pythonhow.png", w=10)

    pdf.output(f"PDFs/{filename}.pdf")
