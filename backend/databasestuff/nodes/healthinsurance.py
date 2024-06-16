from neomodel import (StructuredNode, StringProperty, UniqueIdProperty, IntegerProperty, JSONProperty, EmailProperty,
                      NodeSet, One, Relationship)
from ..property.phone import PhoneProperty
import json
from .patient import Patient
from .city import City
from ..relationships.insured import Insured


class HealthInsurance(StructuredNode):
    """
        HealthInsurance node in the database.

        Attributes:
            uid:Unique id of the HealthInsurance (UID)
            name:Name of the HealthInsurance (String)
            street: Street of the HealthInsurance (String)
            street_number: Street number of the HealthInsurance (Integer)
            opening_hours: Opening hours of the HealthInsurance (JSON)
            phone: Phone of the HealthInsurance (String)
            email: Email of the HealthInsurance (String)
    """
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    street = StringProperty(required=True)
    street_number = IntegerProperty(required=True)
    opening_hours = JSONProperty(required=True)
    phone = PhoneProperty()
    email = EmailProperty()

    # Relationships
    city = Relationship('.city.City', 'HEALTHINSURANCE_IN_CITY', cardinality=One,model=Insured)
    patient = Relationship('.patient.Patient', 'HEALTHINSURANCE_HAS_PATIENT')


def create(name: str, street: str, street_number: int, opening_hours: dict, **kwargs) -> HealthInsurance:
    """
        Creates a new HealthInsurance node, save in database, return HealthInsurance object.
        
        Arguments:
            name: Name of the HealthInsurance (String)
            street: Street of the HealthInsurance (String)
            street_number: Street number of the HealthInsurance (Integer)
            opening_hours: Opening-hours of the HealthInsurance (JSON)

        Keyword Args:
            phone: Phone of the HealthInsurance (String)
            email: Email of the HealthInsurance (String)

        Raises:
            ValueError: If name or street is empty

        Returns:
            HealthInsurance: HealthInsurance object

    """
    if name == "" or street == "" or street_number == "" or opening_hours == "":
        raise ValueError("Name, street, street_number and opening_hours are required")
    return HealthInsurance(name=name, street=street, street_number=street_number, opening_hours=json.dumps(opening_hours),
                           **kwargs).save()


def search(**kwargs) -> NodeSet:
    """
        Searches for HealthInsurance in database, return list of HealthInsurance objects.
        
        Keyword Arguments:
            name: Name of the HealthInsurance
            street: Street of the HealthInsurance
            street_number: Street number of the HealthInsurance
            opening_hours: Opening hours of the HealthInsurance
            phone: Phone of the HealthInsurance
            email: Email of the HealthInsurance
        
        Returns:
            NodeSet: List of HealthInsurance objects

        Raises:
            ValueError: If kwargs is empty

    """
    if kwargs == {}:
        raise ValueError('Kwargs cannot be empty')
    return HealthInsurance.nodes.filter(**kwargs)


def delete(healthinsurance: HealthInsurance) -> bool:
    """
        Deletes a HealthInsurance from database.
        
        Arguments:
            healthinsurance: HealthInsurance object
        
        Returns:
            bool: True if successful, False if not

        Raises:
            ValueError: If healthinsurance is None
    
    """
    if healthinsurance is None:
        raise ValueError('HealthInsurance cannot be None')
    return healthinsurance.delete()


def update(healthinsurance: HealthInsurance, **kwargs) -> HealthInsurance:
    """
        Updates a HealthInsurance in database.
        
        Arguments:
            healthinsurance: HealthInsurance object
        
        Keyword Arguments:
            name: Name of the HealthInsurance
            street: Street of the HealthInsurance
            street_number: Street number of the HealthInsurance
            opening_hours: Opening hours of the HealthInsurance
            phone: Phone of the HealthInsurance
            email: Email of the HealthInsurance
        
        Returns:
            bool: True if successful, False if not
        
        Raises:
            ValueError: If healthinsurance is None
    
    """
    if healthinsurance is None:
        raise ValueError('HealthInsurance cannot be None')
    for key, value in kwargs.items():
        setattr(healthinsurance, key, value)
    return healthinsurance.save()


def add_relationship(healthinsurance: HealthInsurance, *args, personal_id: int = None,
                     cards: dict = None) -> HealthInsurance:
    """
        Adds a relationship between a HealthInsurance and a Patient.

        Arguments:
            healthinsurance: HealthInsurance object
            cards: HealthInsurance cards (when Relationship is Patient)
            personal_id: personal_id of the Patient (when Relationship is Patient)

        Returns:
            HealthInsurance: HealthInsurance object

        Raises:
            ValueError: If healthinsurance is None
            ValueError: If personal_id is None and cards is None
            ValueError: If personal_id is not None and cards is not None

    """
    if healthinsurance is None:
        raise ValueError('HealthInsurance cannot be None')
    for arg in args:
        if arg.__class__.__name__ == 'Patient':
            if personal_id or cards is None:
                raise ValueError('personal_id or Cards cannot be None')
            healthinsurance.patient.connect(arg, {'personal_id': personal_id, 'cards': json.dumps(cards)})
        if arg.__class__.__name__ == 'City':
            healthinsurance.city.connect(arg)
    return healthinsurance.save()


def remove_relationship(healthinsurance: HealthInsurance, *args) -> HealthInsurance:
    """
        Removes a relationship between a HealthInsurance and a node.

        Arguments:
            healthinsurance: HealthInsurance object

        Returns:
            HealthInsurance: HealthInsurance object

        Raises:
            ValueError: If healthinsurance is None
    """
    if healthinsurance is None:
        raise ValueError('HealthInsurance cannot be None')
    for arg in args:
        if arg.__class__.__name__ == 'Patient':
            healthinsurance.patient.disconnect(arg)
        if arg.__class__.__name__ == 'City':
            healthinsurance.city.disconnect(arg)
    return healthinsurance.save()


def replace_relationship(healthinsurance: HealthInsurance, *args, personal_id: int = None,
                         cards: dict = None) -> HealthInsurance:
    """
        Replaces a relationship between a HealthInsurance and a Patient.

        Arguments:
            healthinsurance: HealthInsurance object
            cards: HealthInsurance cards (when Relationship is Patient)
            personal_id: personal_id of the Patient (when Relationship is Patient)

        Returns:
            HealthInsurance: HealthInsurance object

        Raises:
            ValueError: If healthinsurance is None
            ValueError: If personal_id is None and cards is None
            ValueError: If personal_id is not None and cards is not None

    """
    if healthinsurance is None:
        raise ValueError('HealthInsurance cannot be None')
    for arg in args:
        if arg.__class__.__name__ == 'Patient':
            if personal_id or cards is None:
                raise ValueError('personal_id or Cards cannot be None')
            healthinsurance.patient.replace(arg, {'personal_id': personal_id, 'cards': json.dumps(cards)})
        if arg.__class__.__name__ == 'City':
            healthinsurance.city.replace(arg)
    return healthinsurance.save()


def get_relationship(healthinsurance: HealthInsurance, reltype: str) -> Relationship:
    """
        Returns the relationship of a HealthInsurance and a node.

        Arguments:
            healthinsurance: HealthInsurance object
            reltype: Type of the relationship (Patient or City)

        Keyword Arguments:
            reltype: Type of the relationship (Patient or City)

        Returns:
            Relationship: Relationship object

        Raises:
            ValueError: If healthinsurance is None
            ValueError: If reltype is None

    """
    if healthinsurance is None:
        raise ValueError('HealthInsurance cannot be None')
    if reltype is not None:
        if reltype == 'Patient':
            return healthinsurance.patient
        elif reltype == 'City':
            return healthinsurance.city
        else:
            raise ValueError('Invalid relationship type')
    else:
        raise ValueError('Reltype cannot be None')
