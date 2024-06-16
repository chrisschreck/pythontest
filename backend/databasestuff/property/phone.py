from neomodel import RegexProperty


class PhoneProperty(RegexProperty):
    """
    Store phone numbers
    """

    form_field_class = "PhoneField"
    expression = r"(\(?([\d \-\)\–\+\/\(]+){6,}\)?([ .\-–\/]?)([\d]+))"
