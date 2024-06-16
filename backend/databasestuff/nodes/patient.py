from datetime import date

from neomodel import (StructuredNode, StringProperty, DateProperty, UniqueIdProperty, EmailProperty, IntegerProperty,
                      NodeSet, One, Relationship)

from .nodeenums.title import Title
from ..property.phone import PhoneProperty
from .nodeenums.sex import Sex
from ..relationships.has_document import HasDocument
from ..relationships.insured import Insured
import json
from .city import City


class Patient(StructuredNode):
    """
    Patient node in the database. \n
    Attributes:
        uid: The unique id of the patient. (UID)
        firstname: The firstname of the patient. (String)
        lastname: The lastname of the patient. (String)
        address: The address of the patient. (String)
        address_number: The address number of the patient. (Integer)
        birthdate: The birthdate of the patient. (Date)
        sex: The sex of the patient. (Integer)
        title: The title of the patient. (Integer)
        phone: The phone of the patient. (String)
    """
    uid = UniqueIdProperty()
    firstname = StringProperty(required=True)
    lastname = StringProperty(required=True)
    address = StringProperty()
    address_number = IntegerProperty()
    birthdate = DateProperty(required=True)
    sex = IntegerProperty(required=True)
    title = IntegerProperty(default=0)
    phone = PhoneProperty()

    # Relationships
    healthinsurance = Relationship('.healthinsurance.HealthInsurance', 'PATIENT_INSURED_IN_HEALTHINSURANCE', model=Insured,
                                   cardinality=One)
    clinic = Relationship('.clinic.Clinic', 'PATIENT_INSURED_IN_CLINIC')
    city = Relationship('.city.City', 'PATIENT_IN_CITY', cardinality=One)
    document = Relationship('.document.Document', 'HAS_DOCUMENT', model=HasDocument)


def create(firstname: str, lastname: str, birthdate: date, sex: Sex, title: Title = Title.BLANC, **kwargs) -> Patient:
    """
        Creates a new patient and returns it.

        Args:
            title: The title of the patient.
            firstname: The firstname of the patient.
            lastname: The lastname of the patient.
            birthdate: The birthdate of the patient.
            sex: The sex of the patient.

        Keyword Args:
            address: The address of the patient.
            address_number: The address number of the patient.
            title: The title of the patient.
            phone: The phone of the patient.

        Returns:
            Patient: The created patient.

        Raises:
            ValueError: If any of the args are invalid.
    """
    if firstname is None:
        raise ValueError("Firstname is required")
    if lastname is None:
        raise ValueError("Lastname is required")
    if birthdate is None:
        raise ValueError("Birthdate is required")
    if not isinstance(sex, Sex):
        raise ValueError("Invalid sex")
    if not isinstance(title, Title):
        raise ValueError("Invalid title")
    return Patient(firstname=firstname, lastname=lastname, birthdate=birthdate, sex=sex.value, title=title.value,
                   **kwargs).save()


def search(**kwargs) -> NodeSet:
    """
        Searches for patients.

        Keyword Args:
            firstname: The firstname of the patient.
            lastname: The lastname of the patient.
            birthdate: The birthdate of the patient.
            sex: The sex of the patient.
            title: The title of the patient.
            phone: The phone of the patient.

        Returns:
            NodeSet: The found patients.

        Raises:
            ValueError: If kwargs is None.
    """
    if kwargs is None:
        raise ValueError("Kwargs is required")
    return Patient.nodes.filter(**kwargs)


def search_by_id(uid: str) -> Patient:
    """
        Searches for a patient by its id.

        Args:
            uid: The id of the patient.

        Returns:
            Patient: The found patient.

        Raises:
            ValueError: If uid is None.
    """
    if uid is None:
        raise ValueError("UID is required")
    return Patient.nodes.get_or_none(uid=uid)


def update(patient: Patient, **kwargs) -> Patient:
    """
        Updates a patient.

        Args:
            patient: The patient to update.

        Returns:
            Patient: The updated patient.

        Keyword Args:
            firstname: The firstname of the patient.
            lastname: The lastname of the patient.
            birthdate: The birthdate of the patient.
            sex: The sex of the patient.
            title: The title of the patient.
            phone: The phone of the patient.

        Raises:
            ValueError: If patient is None, If kwargs is None.
    """
    if patient is None:
        raise ValueError("Patient is required")
    if kwargs is None:
        raise ValueError("Kwargs is required")
    for key, value in kwargs.items():
        if value is not None:
            setattr(patient, key, value)
    return patient.save()


def delete(patient: Patient) -> bool:
    """
        Deletes a patient.

        Args:
            patient: The patient to delete.

        Returns:
            bool: True if the patient was deleted, false otherwise.

        Raises:
            ValueError: If the patient is not valid.
    """
    if patient is None:
        raise ValueError("Patient is required")
    return patient.delete()


def add_relationship(patient: Patient, *args, personal_id: int = None,
                     cards: dict = None) -> Patient:
    """
        Adds a relationship to a patient.

        Args:
            patient: The patient to add the relationship to.
            args: The relationships to add.
            personal_id: The personal id of the patient. (when Relationship is HealthInsurance)
            cards: The cards of the patient. (when Relationship is HealthInsurance)

        Keyword Args:
            args: The relationships to add.
            personal_id: The personal id of the patient. (when Relationship is HealthInsurance)
            cards: The cards of the patient. (when Relationship is HealthInsurance)

        Returns:
            Patient: The patient with the added relationship.

        Raises:
            ValueError: If the patient is not valid.
    """
    if patient is None:
        raise ValueError("Patient is required")
    for arg in args:
        if arg.__class__.__name__ == 'HealthInsurance':
            patient.healthinsurance.connect(arg, {'personal_id': personal_id, 'cards': json.dumps(cards)})
        elif arg.__class__.__name__ == 'City':
            patient.city.connect(arg)
        elif arg.__class__.__name__ == 'Surgery':
            patient.surgery.connect(arg)
    return patient.save()


def remove_relationship(patient: Patient, *args) -> Patient:
    """
        Removes a relationship from a patient.

        Args:
            patient: The patient to remove the relationship from.
            args: The relationships to remove.

        Returns:
            Patient: The patient with the removed relationship.

        Raises:
            ValueError: If the patient is not valid.
    """
    if patient is None:
        raise ValueError("Patient is required")
    for arg in args:
        if arg.__class__.__name__ == 'HealthInsurance':
            patient.healthinsurance.disconnect(arg)
        elif arg.__class__.__name__ == 'City':
            patient.city.disconnect(arg)
        elif arg.__class__.__name__ == 'Surgery':
            patient.surgery.disconnect(arg)
    return patient.save()


def replace_relationship(patient: Patient, *args, personal_id: int = None,
                         cards: dict = None) -> Patient:
    """
        Replaces a relationship from a patient.

        Args:
            patient: The patient to replace the relationship from.
            args: The relationships to replace.
            personal_id: The personal id of the patient. (when Relationship is HealthInsurance)
            cards: The cards of the patient. (when Relationship is HealthInsurance)

        Returns:
            Patient: The patient with the replaced relationship.

        Raises:
            ValueError: If the patient is not valid.
    """
    if patient is None:
        raise ValueError("Patient is required")
    for arg in args:
        if arg.__class__.__name__ == 'HealthInsurance':
            if personal_id or cards is None:
                raise ValueError('personal_id or Cards cannot be None')
            patient.healthinsurance.replace(arg, {'personal_id': personal_id, 'cards': json.dumps(cards)})
        if arg.__class__.__name__ == 'City':
            patient.city.replace(arg)
        if arg.__class__.__name__ == 'Surgery':
            patient.surgery.replace(arg)
    return patient.save()


def get_relationship(patient: Patient, reltype: str) -> Relationship:
    """
        Gets a relationship from a patient.

        Args:
            patient: The patient to get the relationship from.
            reltype: The type of the relationship.

        Returns:
            Relationship: The relationship.

        Raises:
            ValueError: If the patient is not valid.
    """
    if patient is None:
        raise ValueError("Patient is required")
    if reltype == 'HealthInsurance':
        return patient.healthinsurance.all()
    if reltype == 'City':
        return patient.city.all()
    if reltype == 'Surgery':
        return patient.surgery.all()
    raise ValueError("Invalid relationship")
