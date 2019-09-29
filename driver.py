from reportgen.quantitativedata import main as mn
from reportgen import forecast
from reportgen import reportgen

def main(symbol=None):
    mn(symbol)
    forecast.main()
    reportgen.main(symbol)
