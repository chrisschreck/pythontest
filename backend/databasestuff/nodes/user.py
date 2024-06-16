from neomodel import (
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    Relationship,
    NodeSet,
    EmailProperty,
    JSONProperty,
    BooleanProperty,
)
from .doctor import Doctor
from .patient import Patient
from .clinic import Clinic


class User(StructuredNode):
    """
        User Node in the database.

        Attributes:
            uid: Unique ID of the user. (UID)
            email: Email of the user. (String)
            password: Password-Hash of the user. (String)
            json: JSON data related to the user.
            is_active: Flag indicating if the user is active (default: True)
    """

    uid = UniqueIdProperty()
    email = EmailProperty(unique_index=True)
    password = StringProperty()
    json = JSONProperty()
    is_active = BooleanProperty(default=True)

    # Relationships
    doctor = Relationship(".doctor.Doctor", "IS_CONNECTED_TO")
    patient = Relationship(".patient.Patient", "IS_CONNECTED_TO")
    clinic = Relationship(".clinic.Clinic", "IS_CONNECTED_TO")

    def get_id(self) -> str:
        """
            Get the unique identifier for the user.

            Returns:
                str: The unique identifier (uid) of the user.
        """
        return str(self.uid)

    def is_authenticated(self) -> bool:
        """
            Check if the user is authenticated.

            Returns:
                bool: Always returns True.
        """
        try:
            user = search(email=self.email).first()
            if user and (user.password == self.password):
                return True
            else:
                return False
        except:
            return False


def create(email: str, password: str) -> User:
    """
        Creates a new user.

        Args:
            email: Email of the user. (String)
            password: Password-Hash of the user. (String)

        Returns:
            User: The created user.

        Raises:
            ValueError: If the email or password is None.

    """
    if email is None:
        raise ValueError("Email cannot be None.")
    if password is None:
        raise ValueError("Password cannot be None.")
    return User(email=email, password=password).save()


def search(**kwargs) -> NodeSet:
    """
        Searches for users based on the given keyword arguments.

        Keyword Args:
            uid: Unique ID of the user. (UID)
            email: Email of the user. (String)
            password: Password-Hash of the user. (String)
            json: JSON-String

        Raises:
            ValueError: If the keyword arguments are None.

        Returns:
            NodeSet: The found users.
    """
    if kwargs is None:
        raise ValueError("Keyword arguments cannot be None.")
    return User.nodes.filter(**kwargs)


def update(user: User, **kwargs) -> User:
    """
        Updates a user with the provided keyword arguments.

        Args:
            user: User to update. (User)

        Keyword Args:
            uid: Unique ID of the user. (UID)
            email: Email of the user. (String)
            password: Password-Hash of the user. (String)
            json: JSON-String

        Raises:
            ValueError: If the keyword arguments are None.

        Returns:
            User: The updated user.
    """
    if kwargs is None:
        raise ValueError("Keyword arguments cannot be None.")
    for key, value in kwargs.items():
        if value is not None:
            setattr(user, key, value)
    return user.save()


def delete(user: User) -> bool:
    """
        Deletes a user.

        Args:
            user: User to delete. (User)

        Returns:
            bool: True if the user was deleted, False otherwise.
    """
    try:
        return user.delete()
    except Exception as e:
        print(e)
        return False

def add_relationship(user: User, entity) -> User:
    """
    Adds a relationship between a user and an entity (patient or doctor).

    Args:
        user: The user to add the relationship to.
        entity: The entity (patient or doctor) to add the relationship to.

    Returns:
        User: The user with the added relationship.

    Raises:
        ValueError: If the user or entity is None.
    """
    if user is None:
        raise ValueError("User is required.")
    if entity is None:
        raise ValueError("Entity (patient or doctor) is required.")

    if isinstance(entity, Patient):
        user.patient.connect(entity)
    elif isinstance(entity, Doctor):
        user.doctor.connect(entity)
    elif isinstance(entity, Clinic):
        user.clinic.connect(entity)
    else:
        raise ValueError("Invalid entity type. Must be a patient or doctor.")

    return user


def remove_relationship(user: User, entity) -> User:
    """
    Removes a relationship between a user and an entity (patient or doctor).

    Args:
        user: The user to remove the relationship from.
        entity: The entity (patient or doctor) to remove the relationship from.

    Returns:
        User: The user with the removed relationship.

    Raises:
        ValueError: If the user or entity is None.
    """
    if user is None:
        raise ValueError("User is required.")
    if entity is None:
        raise ValueError("Entity (patient or doctor) is required.")

    if isinstance(entity, Patient):
        user.patient.disconnect(entity)
    elif isinstance(entity, Doctor):
        user.doctor.disconnect(entity)
    elif isinstance(entity, Clinic):
        user.clinic.disconnect(entity)
    else:
        raise ValueError("Invalid entity type. Must be a patient or doctor.")

    return user


def replace_relationship(user: User, old_entity, new_entity) -> User:
    """
    Replaces a relationship between a user and an entity (patient or doctor) with a new entity.

    Args:
        user: The user to replace the relationship for.
        old_entity: The entity (patient or doctor) to remove the relationship from.
        new_entity: The entity (patient or doctor) to add the relationship to.

    Returns:
        User: The user with the replaced relationship.

    Raises:
        ValueError: If the user, old_entity, or new_entity is None.
    """
    if user is None:
        raise ValueError("User is required.")
    if old_entity is None:
        raise ValueError("Old entity (patient or doctor) is required.")
    if new_entity is None:
        raise ValueError("New entity (patient or doctor) is required.")

    if isinstance(old_entity, Patient) and isinstance(new_entity, Patient):
        user.patient.disconnect(old_entity)
        user.patient.connect(new_entity)
    elif isinstance(old_entity, Doctor) and isinstance(new_entity, Doctor):
        user.doctor.disconnect(old_entity)
        user.doctor.connect(new_entity)
    elif isinstance(old_entity, Clinic) and isinstance(new_entity, Clinic):
        user.clinic.disconnect(old_entity)
        user.clinic.connect(new_entity)
    else:
        raise ValueError("Invalid entity type. Must be a patient or doctor.")

    return user


def get_relationship(user: User):
    """
    Gets the patient or doctor relationship for a user.

    Args:
        user: The user to get the relationship for.

    Returns:
        Tuple[Patient, str] or Tuple[Doctor, str]: A tuple containing the patient or doctor associated with the user and the relationship type.

    Raises:
        ValueError: If the user is None or has both patient and doctor relationships.
    """
    if user is None:
        raise ValueError("User is required.")

    patient_rel = user.patient.single()
    doctor_rel = user.doctor.single()
    clinic_rel = user.clinic.single()

    if (patient_rel and doctor_rel) or (patient_rel and clinic_rel) or (doctor_rel and clinic_rel):
        raise ValueError("User has both patient and doctor relationships.")
    elif patient_rel:
        return patient_rel, "patient"
    elif doctor_rel:
        return doctor_rel, "doctor"
    elif clinic_rel:
        return clinic_rel, "clinic"
    else:
        raise ValueError("User does not have a patient or doctor relationship.")
