from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_trade_confirmation_pdf(output_file):
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4

   

    # Contact details
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 100, "To : CITIBANK, N.A / Attn :")
    c.drawString(50, height - 115, "Tel : +91 (44) 4444 4444 / Fax :")
    c.drawString(50, height - 130, "Date : May 11, 2020")

    # Title
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 160, "This is to confirm the following trade with you :")

    # Trade details
    details = [
        ("Buyer", "CITI"),
        ("Seller", "ABC"),
        ("Our reference number", "1234567890/9876543210"),
        ("Note Reference", "VPJ241204"),
        ("Trade Date", "May 10, 2020"),
        ("Settlement Date", "May 24, 2020"),
        ("Issue", "ABCC VPJ VP2412ZYX 22/05/2020"),
        ("Issue Date", "24/05/2020"),
        ("Fixing Date", "22/06/2020"),
        ("Maturity Date", "24/06/2020"),
        ("Currency", "USD"),
        ("ISIN Code", "XL9843377521"),
        ("Valoren Code", "0"),
        ("Nominal Amount", "350,000.00"),
        ("Price", "97.54%"),
        ("Settlement Amount", "346,350.00")
    ]

    y = height - 190
    for key, value in details:
        c.drawString(50, y, f"{key} :")
        c.drawString(200, y, value)
        y -= 15

    # Settlement Instructions
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y - 10, "Your settlement instruction :")
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Security :")
    c.drawString(200, y, "CLEARSTREAM BANKING S.A / CEDELULLXXX")
    y -= 15
    c.drawString(50, y, "                          ")
    c.drawString(200, y, "CITIKHXXXX")
    y -= 15
    c.drawString(50, y, "                          ")
    c.drawString(200, y, "12345")
    y -= 15
    c.drawString(50, y, "Settlement method :")
    c.drawString(200, y, "DAP")

    y -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Our settlement instruction :")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Security :")
    c.drawString(200, y, "CLEARSTREAM BANKING S.A / CEDELULLXXX")
    y -= 15
    c.drawString(50, y, "                          ")
    c.drawString(200, y, "54321")
    y -= 15
    c.drawString(50, y, "Settlement method :")
    c.drawString(200, y, "DAP")

    y -= 30
    c.setFont("Helvetica", 9)
    c.drawString(50, y, "Please revert immediately if there is any discrepancy. Otherwise we will deem that the above-mentioned trade details are correct.")
    y -= 12
    c.drawString(50, y, "Please instruct your agent to settle the trade promptly. We reserve the rights to claim from you any losses incurred from late settlement.")
    y -= 12
    c.drawString(50, y, "Regards, Equity Derivatives Operations.")

    c.save()

# Generate the PDF
generate_trade_confirmation_pdf("Trade_Confirmation.pdf")
