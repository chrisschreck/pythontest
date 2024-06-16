from neomodel import (StructuredRel, StringProperty, JSONProperty)


class Insured(StructuredRel):
    """
        StructuredRel for Insured relationship (Patient -> Insured -> Health Insurance)

        Attributes:
             personal_id (str): The personal id of the insured
             cards (dict): The cards of the insured
    """
    personal_id = StringProperty()
    cards = JSONProperty()
