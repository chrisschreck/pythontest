from neomodel import (StructuredRel, IntegerProperty)


class HasDocument(StructuredRel):
    """
        StructuredRel for has_document relationship (Doctor -> has_document -> Document)
        StructuredRel for has_document relationship (Patient -> has_document -> Document)

        Attributes:
             document_id (str): The id of the document
    """
    type = IntegerProperty(required=True)

