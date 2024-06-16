import json

from neomodel import (StructuredNode, StringProperty, UniqueIdProperty, IntegerProperty, JSONProperty, EmailProperty,
                      Relationship, One, NodeSet)
from ..property.phone import PhoneProperty
from .city import City
from .doctor import Doctor
from .patient import Patient


class Clinic(StructuredNode):
    """
        Clinic Node Class

        Attributes:
            uid (UniqueIdProperty): Clinic Unique ID
            name (StringProperty): Clinic Name
            street (StringProperty): Clinic Street
            street_number (IntegerProperty): Clinic Street Number
            opening_hours (JSONProperty): Clinic Opening Hours
            phone (PhoneProperty): Clinic Phone
            email (EmailProperty): Clinic Email
    """
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    street = StringProperty(required=True)
    street_number = IntegerProperty(required=True)
    opening_hours = JSONProperty(required=True)
    phone = PhoneProperty()
    email = EmailProperty()

    # Relationships
    city = Relationship('.city.City', 'SURGERY_IN_CITY', cardinality=One)
    doctor = Relationship('.doctor.Doctor', 'DOCTOR_WORKS_IN_CLINIC')
    patient = Relationship('.patient.Patient', 'PATIENT_INSURED_IN_CLINIC')


def create(name: str, street: str, street_number: int, opening_hours: dict, phone: str, email: str) -> Clinic:
    """
        Creates a new Surgery

        Args:
            name (str): Surgery Name
            street (str): Surgery Street
            street_number (int): Surgery Street Number
            opening_hours (dict): Surgery Opening Hours
            phone (str): Surgery Phone
            email (str): Surgery Email

        Returns:
            Clinic: Surgery Object
    """
    surgery = Clinic(name=name, street=street, street_number=street_number, opening_hours=json.dumps(opening_hours), phone=phone,
                     email=email).save()
    return surgery


def update(clinic: Clinic, **kwargs) -> Clinic:
    """
        Updates an existing Surgery

        Args:
            clinic (Clinic): Surgery Object
            kwargs (dict): Surgery Properties

        Returns:
            Clinic: Surgery Object
    """
    for key, value in kwargs.items():
        setattr(clinic, key, value)
    return clinic.save()


def delete(clinic: Clinic) -> bool:
    """
        Deletes an existing Surgery

        Args:
            clinic (Clinic): Surgery Object

        Returns:
            bool: True if successful, False otherwise
    """
    return clinic.delete()


def search(**kwargs) -> NodeSet:
    """ 
        Searches Surgeries

        Keyword Args:
            name (str): Surgery Name
            street (str): Surgery Street
            street_number (int): Surgery Street Number
            opening_hours (dict): Surgery Opening Hours
            phone (str): Surgery Phone
            email (str): Surgery Email

        Returns:
            NodeSet: Surgeries
    """
    return Clinic.nodes.filter(**kwargs)


def add_relationship(clinic: Clinic, *args) -> Clinic:
    """
        Adds a relationship to Surgery

        Args:
            clinic (Clinic): Surgery Object
            args (Relationship): Relationships

        Returns:
            Clinic: Surgery Object
    """
    if clinic is None:
        raise ValueError('Surgery is None')
    for arg in args:
        if arg.__class__.__name__ == 'Doctor':
            clinic.doctor.connect(arg)
        if arg.__class__.__name__ == 'Patient':
            clinic.patient.connect(arg)
        if arg.__class__.__name__ == 'City':
            clinic.city.connect(arg)
    return clinic.save()


def add_doctor_relationship(clinic: Clinic, doctor: Doctor) -> Clinic:
    """
    Adds a doctor relationship to the surgery.

    Args:
        clinic (Clinic): Surgery object.
        doctor (Doctor): Doctor object.

    Returns:
        Clinic: Updated surgery object.
    """
    if clinic is None:
        raise ValueError('Surgery is None')
    if doctor is None:
        raise ValueError('Doctor is None')
    clinic.doctor.connect(doctor)
    return clinic.save()


def add_patient_relationship(clinic: Clinic, patient: Patient) -> Clinic:
    """
    Adds a patient relationship to the surgery.

    Args:
        clinic (Clinic): Surgery object.
        patient (Patient): Patient object.

    Returns:
        Clinic: Updated surgery object.
    """
    if clinic is None:
        raise ValueError('Surgery is None')
    if patient is None:
        raise ValueError('Patient is None')
    clinic.patient.connect(patient)
    return clinic.save()


def add_city_relationship(clinic: Clinic, city: City) -> Clinic:
    """
    Adds a city relationship to the surgery.

    Args:
        surgery (Clinic): Surgery object.
        city (City): City object.

    Returns:
        Clinic: Updated surgery object.
    """
    if clinic is None:
        raise ValueError('Surgery is None')
    if city is None:
        raise ValueError('City is None')
    clinic.city.connect(city)
    return clinic.save()



def remove_relationship(clinic: Clinic, *args) -> Clinic:
    """
        Removes a relationship to Surgery

        Args:
            surgery (Clinic): Surgery Object
            args (Relationship): Relationships

        Returns:
            Clinic: Surgery Object
    """
    if clinic is None:
        raise ValueError('Surgery is None')
    for arg in args:
        if arg.__class__.__name__ == 'Doctor':
            clinic.doctor.disconnect(arg)
        if arg.__class__.__name__ == 'Patient':
            clinic.patient.disconnect(arg)
        if arg.__class__.__name__ == 'City':
            clinic.city.disconnect(arg)
    return clinic.save()


def replace_relationship(clinic: Clinic, *args) -> Clinic:
    """
        Replaces a relationship to Surgery

        Args:
            surgery (Clinic): Surgery Object
            args (Relationship): Relationships

        Returns:
            Clinic: Surgery Object
    """
    if clinic is None:
        raise ValueError('Surgery is None')
    for arg in args:
        if arg.__class__.__name__ == 'Doctor':
            clinic.doctor.replace(arg)
        if arg.__class__.__name__ == 'Patient':
            clinic.patient.replace(arg)
        if arg.__class__.__name__ == 'City':
            clinic.city.replace(arg)
    return clinic.save()


def get_relationship(clinic: Clinic, reltype: str) -> Relationship:
    """
        Gets a relationship to Surgery

        Args:
            surgery (Clinic): Surgery Object
            reltype (str): Relationship Type (doctor, patient, city)

        Raises:
            ValueError: Invalid Relationship Type

        Returns:
            Relationship: Relationship
    """
    if clinic is None:
        raise ValueError('Surgery is None')
    if reltype == 'doctor':
        return clinic.doctor.all()
    if reltype == 'patient':
        return clinic.patient.all()
    if reltype == 'city':
        return clinic.city.all()
    raise ValueError('Invalid Relationship Type')


def list_doctors(clinic: Clinic) -> NodeSet:
    """Lists all doctors in a clinic.

    Args:
        clinic (Clinic): Clinic object.

    Returns:
        NodeSet: Doctors in clinic.
    """
    if clinic is None:
        raise ValueError('Clinic is None')
    return clinic.doctor.all()


def check_if_doctor_is_in_clinic(clinic: Clinic, doctor: Doctor) -> bool:
    """Checks if a doctor is in a clinic.

    Args:
        clinic (Clinic): Clinic object.
        doctor (Doctor): Doctor object.

    Returns:
        bool: True if doctor is in clinic, False otherwise.
    """
    if clinic is None:
        raise ValueError('Clinic is None')
    if doctor is None:
        raise ValueError('Doctor is None')
    return clinic.doctor.is_connected(doctor)
