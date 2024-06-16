from neomodel import (StructuredNode, StringProperty, UniqueIdProperty, Relationship, NodeSet)


class DoctorSkill(StructuredNode):
    """
    DoctorSkill node in  the database.\n

    Attributes:
        uid: Unique id of the node. (UID)
        name: Name of the skill. (String)
    """
    uid = UniqueIdProperty()
    name = StringProperty()

    # Relationships
    doctor = Relationship('.doctor.Doctor', 'HAS_SKILL')


def search(**kwargs) -> NodeSet:
    """
    Searches for a DoctorSkill node in the database.

    Keyword arguments:
        uid: Unique id of the node. (UID)
        name: Name of the skill. (String)

    Returns:

        NodeSet: NodeSet of the DoctorSkill nodes.

    Raises:
        ValueError: If the keyword arguments are not valid.
    """
    if not kwargs:
        raise ValueError('No keyword arguments were provided.')
    return DoctorSkill.nodes.filter(**kwargs)


def create(name: str) -> DoctorSkill:
    """
    Creates a DoctorSkill node in the database.

    Args:
        name: Name of the skill. (String)

    Returns:
        DoctorSkill: The created DoctorSkill node.

    Raises:
        ValueError: If no name was provided.
    """
    if not name:
        raise ValueError('No name was provided.')
    return DoctorSkill(name=name).save()


def update(doctor_skill: DoctorSkill, **kwargs) -> DoctorSkill:
    """
    Updates a DoctorSkill node in the database.

    Args:
        doctor_skill: The DoctorSkill node to update. (DoctorSkill)

    Keyword arguments:
        name: Name of the skill. (String)

    Returns:
        DoctorSkill: The updated DoctorSkill node.

    Raises:
        ValueError: If no DoctorSkill node was provided.
    """
    if not doctor_skill:
        raise ValueError('No DoctorSkill node was provided.')
    if 'name' in kwargs:
        doctor_skill.name = kwargs['name']
    return doctor_skill.save()


def delete(doctor_skill: DoctorSkill) -> bool:
    """
    Deletes a DoctorSkill node in the database.

    Args:
        doctor_skill: The DoctorSkill node to delete. (DoctorSkill)

    Returns:
        bool: True if the DoctorSkill node was deleted, False otherwise.

    Raises:
        ValueError: If no DoctorSkill node was provided.
    """
    if not doctor_skill:
        raise ValueError('No DoctorSkill node was provided.')
    return doctor_skill.delete()

