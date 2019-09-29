import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def main(symbol=None):

    doc = SimpleDocTemplate("form_letter.pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    Story = []
    logo = "Forecast.png"
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size=14>Forecast for ' + str(symbol) + '</font>'

    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    formatted_time = time.ctime()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    ptext = '<font size=9>Thank you for using Stock4! Below is the report you asked for. The forecast has been made from an ARIMA' \
            ' model that uses historical data to predict future data. Assess the information below as you will. ' \
            '' \
            'The blue line is the projected, the dots are the actual.' \
            '</font>'

    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    im = Image(logo, 5 * inch, 3 * inch)
    Story.append(im)

    doc.build(Story)
