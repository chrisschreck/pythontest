from neomodel import StructuredNode, StringProperty, UniqueIdProperty, DateTimeProperty, NodeSet, Relationship
import datetime


class Appointment(StructuredNode):
    """
    Appointment node in the database.

    Attributes:
        uid: Unique id of the node. (UID)
        name: Name of the appointment. (String)
        date: Date of the appointment. (DateTime)
    """
    uid = UniqueIdProperty()
    name = StringProperty()
    date = DateTimeProperty()

    # Relationships
    doctor = Relationship('.doctor.Doctor', 'APPOINTED_TO')
    patient = Relationship('.patient.Patient', 'APPOINTED_FOR')


def create(name: str, date: datetime, doctor: 'doctor.Doctor', patient: 'patient.Patient') -> Appointment:
    """
    Creates an Appointment node in the database.

    Args:
        name: Name of the appointment. (String)
        date: Date of the appointment. (datetime)
        doctor: The Doctor node related to the appointment.
        patient: The Patient node related to the appointment.

    Returns:
        Appointment: The created Appointment node.

    Raises:
        ValueError: If no name, date, doctor, or patient was provided.
    """
    if not name or not date or not doctor or not patient:
        raise ValueError('No name, date, doctor, or patient was provided.')

    appointment = Appointment(name=name, date=date)
    appointment.doctor.connect(doctor, {'relationship_type': 'APPOINTED_TO'})
    appointment.patient.connect(patient, {'relationship_type': 'APPOINTED_FOR'})
    appointment.save()

    return appointment


def update(appointment: Appointment, **kwargs) -> Appointment:
    """
    Updates an Appointment node in the database.

    Args:
        appointment: The Appointment node to update. (Appointment)

    Keyword arguments:
        name: Name of the appointment. (String)
        date: Date of the appointment. (datetime)

    Returns:
        Appointment: The updated Appointment node.

    Raises:
        ValueError: If no Appointment node was provided.
    """
    if not appointment:
        raise ValueError('No Appointment node was provided.')
    if 'name' in kwargs:
        appointment.name = kwargs['name']
    if 'date' in kwargs:
        appointment.date = kwargs['date']
    return appointment.save()


def delete(appointment: Appointment) -> bool:
    """
    Deletes an Appointment node in the database.

    Args:
        appointment: The Appointment node to delete. (Appointment)

    Returns:
        bool: True if the Appointment node was deleted, False otherwise.

    Raises:
        ValueError: If no Appointment node was provided.
    """
    if not appointment:
        raise ValueError('No Appointment node was provided.')
    return appointment.delete()


def search(**kwargs) -> NodeSet:
    """
    Searches for Appointment nodes in the database based on the provided criteria.

    Keyword arguments:
        name: Name of the appointment. (String)
        date: Date of the appointment. (datetime)
        doctor: The Doctor node related to the appointment.
        patient: The Patient node related to the appointment.

    Returns:
        NodeSet: NodeSet of the Appointment nodes matching the search criteria.

    Raises:
        ValueError: If no search criteria were provided.
    """
    if not kwargs:
        raise ValueError('No search criteria were provided.')

    query = Appointment.nodes

    if 'name' in kwargs:
        query = query.filter(name=kwargs['name'])

    if 'date' in kwargs:
        query = query.filter(date=kwargs['date'])

    if 'doctor' in kwargs:
        doctor = kwargs['doctor']
        query = query.relationship_match('doctor', 'APPOINTED_TO').where(doctor)

    if 'patient' in kwargs:
        patient = kwargs['patient']
        query = query.relationship_match('patient', 'APPOINTED_FOR').where(patient)

    return query.all()

