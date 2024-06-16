from neomodel import (StructuredNode, StringProperty, UniqueIdProperty, Relationship, NodeSet)


class City(StructuredNode):
    """
    City node in the database.\n
    A city has a unique ID, a name, a ZIP code and relationships to other nodes (in both ways).\n

    Attributes:
        uid: Unique ID of the city (UID)
        name: Name of the city (String)
        zip: ZIP code of the city (String)
    """
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    zip = StringProperty(required=True, unique_index=True)

    # Relationships
    healthinsurance = Relationship('.healthinsurance.HealthInsurance', 'HEALTHINSURANCE_IN_CITY')
    patient = Relationship('.patient.Patient', 'PATIENT_IN_CITY')
    surgery = Relationship('.surgery.Surgery', 'SURGERY_IN_CITY')


def search(**kwargs) -> NodeSet:
    """Searches for a city by any attribute and returns a NodeSet of all cities with that attribute

        Keyword Args:
            name: Name of the city (String)
            zip: ZIP code of the city (String)

        Returns:
            NodeSet: NodeSet of all cities with that attribute

        Raises:
            ValueError: If kwargs is empty
    """
    if kwargs == {}:
        raise ValueError('Kwargs cannot be empty')
    return City.nodes.filter(**kwargs)


def create(name: str, zipcode: str) -> City:
    """Creates a new city and returns it
        
    Args:
        name: Name of the city
        zipcode: ZIP code of the city

    Returns:
        City: Newly created city node
        
    Raises:
        ValueError: If name or zip is empty
    """
    return City(name=name, zip=zipcode).save()


def delete(city: City) -> bool:
    """Deletes a city by node and returns True if successful
        
    Args:
        city: City node

    Returns:
        bool: True if successful, False otherwise
        
    Raises:
        ValueError: If city is None
    """
    if city is None:
        raise ValueError('City cannot be None')
    return city.delete()


def update(city: City, **kwargs) -> City:
    """
    Updates a city by node and returns it.
        
    Args:
        city: City node
        **kwargs: Attributes of the city

    Returns:
        city: Updated city node

    Raises:
        ValueError: If city is None, If kwargs is empty, If name or zip is empty, If zip is not a 5-digit number
    """
    if city is None:
        raise ValueError('City cannot be None')
    if kwargs == {}:
        raise ValueError('Kwargs cannot be empty')
    for key, value in kwargs.items():
        if key == 'name':
            if value == '':
                raise ValueError('Name cannot be empty')
        if key == 'zip':
            if value == '':
                raise ValueError('ZIP cannot be empty')
            if len(str(value)) != 5:
                raise ValueError('ZIP must be a 5-digit number')
        setattr(city, key, value)
    return city.save()


def add_relationship(city: City, *args) -> City:
    """Adds a relationship between a city and a node.

        Args:
            city: City node
            args: Nodes to add relationship to

        Returns:
            City: Updated city

        Raises:
            ValueError: If no city node was provided
    """
    if city is not None:
        for arg in args:
            if arg.__class__.__name__ == 'HealthInsurance':
                city.healthinsurance.connect(arg)
            elif arg.__class__.__name__ == 'Patient':
                city.patient.connect(arg)
            elif arg.__class__.__name__ == 'Surgery':
                city.surgery.connect(arg)
        return city.save()
    else:
        raise ValueError('No city node was provided')


def remove_relationship(city: City, *args) -> City:
    """Removes a relationship between a city and a node.

        Args:
            city: City node
            args: Nodes to remove relationship from

        Returns:
            City: Updated city

        Raises:
            ValueError: If no city node was provided
    """
    if city is not None:
        for arg in args:
            if arg.__class__.__name__ == 'HealthInsurance':
                city.healthinsurance.disconnect(arg)
            elif arg.__class__.__name__ == 'Patient':
                city.patient.disconnect(arg)
            elif arg.__class__.__name__ == 'Surgery':
                city.surgery.disconnect(arg)
        return city.save()
    else:
        raise ValueError('No city node was provided')


def replace_relationship(city: City, *args) -> City:
    """Replaces a relationship between a city and a node.

        Args:
            city: City node
            args: Nodes to replace relationship with

        Returns:
            City: Updated city

        Raises:
            ValueError: If no city node was provided
    """
    if city is not None:
        for arg in args:
            if arg.__class__.__name__ == 'HealthInsurance':
                city.healthinsurance.replace(arg)
            elif arg.__class__.__name__ == 'Patient':
                city.patient.replace(arg)
            elif arg.__class__.__name__ == 'Surgery':
                city.surgery.replace(arg)
        return city.save()
    else:
        raise ValueError('No city node was provided')


def get_relationship(city: City, reltype: str) -> Relationship:
    """Gets a relationship between a city and a node.

        Args:
            city: City node
            reltype: Type of relationship to get (surgery, patient, healthinsurance)

        Returns:
            Relationship: Relationship between city and node

        Raises:
            ValueError: If no city node was provided
    """
    if city is not None:
        if reltype == 'surgery':
            return city.surgery
        elif reltype == 'patient':
            return city.patient
        elif reltype == 'healthinsurance':
            return city.healthinsurance
        else:
            raise ValueError('Invalid relationship type')
    else:
        raise ValueError('No city node was provided')
