from forex_python.converter import CurrencyRates, CurrencyCodes, Decimal, RatesNotAvailableError

cr = CurrencyRates(force_decimal=True)
cd = CurrencyCodes()

def result(start, end, amt) :
    """ Returns string that states starting and ending currencies as well as the final amount """
    amt_dec = Decimal(amt) # This will allow for input to be either float or integer
    end_amt = round(cr.convert(start.upper(), end.upper(), amt_dec), 2) # Conversion function from forex converter
    curr_symbol = cd.get_symbol(end) # Retrieves symbol for ending currency
    response = f"""{curr_symbol}{end_amt}"""
    return response

def code_is_valid(code) :
    """ Returns true if valid currency code and false if not """
    try:
        if not type(code) == str:
            return False
    except RatesNotAvailableError:
        return False

def num_is_valid(num) :
    """ Returns true if argument is either integer or float. Returns false if anything other than a number """
    try:
        num_float = float(num)
        if num_float <= 0:
                return False
        return True
    except ValueError:
        return False