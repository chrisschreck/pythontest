from neomodel import (StructuredNode, StringProperty, UniqueIdProperty, IntegerProperty,
                      Relationship, NodeSet, DateProperty)
from .nodeenums.sex import Sex
from .nodeenums.title import Title
from .doctorskill import DoctorSkill
from datetime import date

from ..relationships.has_document import HasDocument


class Doctor(StructuredNode):
    """Doctor node in the database\n
    
    Attributes:
        uid: Unique ID of the doctor (UID)
        firstname: First name of the doctor (String)
        lastname: Last name of the doctor (String)
        title: Title of the doctor (Integer)
        sex: Sex of the doctor (Integer)
    """
    uid = UniqueIdProperty()
    firstname = StringProperty(required=True)
    lastname = StringProperty(required=True)
    birthdate = DateProperty(required=True)
    title = IntegerProperty(default=0)
    sex = IntegerProperty(required=True)

    # Relationships
    clinic = Relationship('.clinic.Clinic', 'DOCTOR_IS_EMPLOYEE_IN_CLINIC')
    doctor_skill = Relationship('.doctorskill.DoctorSkill', 'SKILL_IS_USED_BY_DOCTOR')
    document = Relationship('.document.Document', 'HAS_DOCUMENT', model=HasDocument)


def search(**kwargs) -> NodeSet:
    """Searches for a doctor by any attribute and returns a NodeSet of all doctors with that attribute

        Keyword Args:
            uid: Unique ID of the doctor (UID)
            firstname: First name of the doctor (String)
            lastname: Last name of the doctor (String)
            title: Title of the doctor (Integer)
            sex: Sex of the doctor (Integer)

        Returns:
            NodeSet: NodeSet of all doctors with that attribute

        Raises:
            ValueError: If no Kwargs are provided

    """
    if not kwargs:
        raise ValueError('Kwargs cannot be empty')
    else:
        return Doctor.nodes.filter(**kwargs)


def search_by_id(uid: str) -> Doctor:
    """Searches for a doctor by uid and returns it

        Args:
            uid: Unique ID of the doctor (UID)

        Returns:
            Doctor: Doctor with that uid

        Raises:
            ValueError: If no uid is provided

    """
    if not uid:
        raise ValueError('UID cannot be empty')
    else:
        return Doctor.nodes.get_or_none(uid=uid)


def create(firstname: str, lastname: str, birthdate: date, sex: Sex, title: Title = Title.BLANC) -> Doctor:
    """
    Creates a new doctor and returns it

    Args:

        firstname: First name of the doctor (String)
        lastname: Last name of the doctor (String)
        sex: Sex of the doctor (Sex)
        title: Title of the doctor (default=0)

    Returns:
        Doctor: New doctor

    Raises:
        ValueError: If firstname, lastname, sex and title are empty
    """
    if not firstname or not lastname or not sex:
        raise ValueError('Firstname, lastname, sex and title cannot be empty')
    else:
        return Doctor(firstname=firstname, lastname=lastname, birthdate=birthdate, sex=sex.value,
                      title=title.value).save()


def delete(doctor: Doctor) -> bool:
    """Deletes a doctor by node and returns True if successful
        
        Args:
            doctor: Doctor node

        Returns:
            bool: True if successful, False otherwise

        Raises:
            ValueError: If no doctor with that UID is found

    """
    if doctor is not None:
        return doctor.delete()


def update(doctor: Doctor, **kwargs) -> Doctor:
    """Updates a doctor by node and returns it.
        
        Args:
            doctor: Doctor node
            kwargs: Key-value pairs of attributes to update

        Keyword Args:
            firstname: First name of the doctor (String)
            lastname: Last name of the doctor (String)
            title: Title of the doctor (Title)
            sex: Sex of the doctor (Sex)

        Returns:
            Doctor: Updated doctor

        Raises:
            ValueError: If no doctor node was provided
    """
    if doctor is not None:
        for key, value in kwargs.items():
            if key == 'sex':
                value = Sex(value).value
            if key == 'title':
                value = Title(value).value
            setattr(doctor, key, value)
        return doctor.save()
    else:
        raise ValueError('No doctor node was provided')


def add_relationship(doctor: Doctor, *args) -> Doctor:
    """Adds a relationship between a doctor and a node.

        Args:
            doctor: Doctor node
            args: Nodes to add relationship to

        Returns:
            Doctor: Updated doctor

        Raises:
            ValueError: If no doctor node was provided
    """
    if doctor is not None:
        for arg in args:
            if arg.__class__.__name__ == 'Clinic':
                doctor.clinic.connect(arg)
            elif arg.__class__.__name__ == 'DoctorSkill':
                doctor.doctor_skill.connect(arg)
        return doctor.save()
    else:
        raise ValueError('No doctor node was provided')


def remove_relationship(doctor: Doctor, *args) -> Doctor:
    """Removes a relationship between a doctor and a node.

        Args:
            doctor: Doctor node
            args: Nodes to remove relationship from

        Returns:
            Doctor: Updated doctor

        Raises:
            ValueError: If no doctor node was provided
    """
    if doctor is not None:
        for arg in args:
            if arg.__class__.__name__ == 'Clinic':
                doctor.clinic.disconnect(arg)
            elif arg.__class__.__name__ == 'DoctorSkill':
                doctor.doctor_skill.disconnect(arg)
        return doctor.save()
    else:
        raise ValueError('No doctor node was provided')


def replace_relationship(doctor: Doctor, *args) -> Doctor:
    """Replaces a relationship between a doctor and a node.

        Args:
            doctor: Doctor node
            args: Nodes to replace relationship with

        Returns:
            Doctor: Updated doctor

        Raises:
            ValueError: If no doctor node was provided
    """
    if doctor is not None:
        for arg in args:
            if arg.__class__.__name__ == 'Clinic':
                doctor.clinic.replace(arg)
            elif arg.__class__.__name__ == 'DoctorSkill':
                doctor.doctor_skill.replace(arg)
        return doctor.save()
    else:
        raise ValueError('No doctor node was provided')


def get_relationship(doctor: Doctor, reltype: str) -> Relationship:
    """Gets a relationship between a doctor and a node.

        Args:
            doctor: Doctor node
            reltype: Type of relationship to get

        Returns:
            Relationship: Relationship between doctor and node

        Raises:
            ValueError: If no doctor node was provided
    """
    if doctor is not None:
        if reltype == 'clinic':
            return doctor.clinic
        if reltype == 'doctor_skill':
            return doctor.doctor_skill
        else:
            raise ValueError('Invalid relationship type')
    else:
        raise ValueError('No doctor node was provided')


def add_skill(doctor_skill: DoctorSkill, doctor: Doctor) -> DoctorSkill:
    """
    Adds a DoctorSkill node to a Doctor node in the database.

    Args:
        doctor_skill: The DoctorSkill node to add. (DoctorSkill)
        doctor: The Doctor node to add the DoctorSkill node to. (Doctor)

    Returns:
        DoctorSkill: The DoctorSkill node with the relationship added.

    Raises:
        ValueError: If no DoctorSkill node was provided.
    """
    if not doctor_skill:
        raise ValueError('No DoctorSkill node was provided.')
    if not doctor:
        raise ValueError('No Doctor node was provided.')
    doctor_skill.doctor.connect(doctor)
    return doctor_skill.save()


def remove_skill(doctor_skill: DoctorSkill, doctor: Doctor) -> DoctorSkill:
    """
    Removes a DoctorSkill node from a Doctor node in the database.

    Args:
        doctor_skill: The DoctorSkill node to remove. (DoctorSkill)
        doctor: The Doctor node to remove the DoctorSkill node from. (Doctor)

    Returns:
        DoctorSkill: The DoctorSkill node with the relationship removed.

    Raises:
        ValueError: If no DoctorSkill node was provided.
    """
    if not doctor_skill:
        raise ValueError('No DoctorSkill node was provided.')
    if not doctor:
        raise ValueError('No Doctor node was provided.')
    doctor_skill.doctor.disconnect(doctor)
    return doctor_skill.save()


def get_skill(doctor_skill: DoctorSkill) -> Relationship:
    """
    Gets a DoctorSkill node's relationship with a Doctor node in the database.

    Args:
        doctor_skill: The DoctorSkill node. (DoctorSkill)

    Returns:
        Relationship: The DoctorSkill node's relationship with a Doctor node.

    Raises:
        ValueError: If no DoctorSkill node was provided.
    """
    if not doctor_skill:
        raise ValueError('No DoctorSkill node was provided.')
    return doctor_skill.doctor


def check_if_doctor_has_user(doctor: Doctor) -> bool:
    """
    Checks if a Doctor node has a User node in the database.

    Args:
        doctor: The Doctor node to check. (Doctor)

    Returns:
        bool: True if the Doctor node has a User node, False otherwise.

    Raises:
        ValueError: If no Doctor node was provided.
    """
    if not doctor:
        raise ValueError('No Doctor node was provided.')

    try:
        if doctor.user is None:
            return False
        else:
            return True
    except AttributeError:
        return False
