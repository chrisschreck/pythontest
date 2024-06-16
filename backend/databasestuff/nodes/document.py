from neomodel import (StructuredNode, StringProperty, Relationship, NodeSet)

from .doctor import Doctor
from .patient import Patient
from ..relationships.has_document import HasDocument
from .nodeenums.document_type import DocumentType


class Document(StructuredNode):
    """
    Document node in the database.\n

    Attributes:
        document_id: The id of the document.
    """
    document_id = StringProperty(required=True)

    # Relationships
    doctor = Relationship('.doctor.Doctor', 'HAS_DOCUMENT', model=HasDocument)
    patient = Relationship('.patient.Patient', 'HAS_DOCUMENT', model=HasDocument)


def create(document_id: str, type: DocumentType, **kwargs) -> Document:
    """
        Creates a new document and returns it.

        Args:
            document_id: The id of the document.

        Returns:
            The created document.
    """
    document = Document(document_id=document_id).save()
    if 'doctor' in kwargs:
        document.doctor.connect(kwargs['doctor'], {'type': type.value})
    elif 'patient' in kwargs:
        document.patient.connect(kwargs['patient'], {'type': type.value})
    return document


def search_by_id(document_id: str) -> Document:
    """
        Searches for a document by its id.

        Args:
            document_id: The id of the document.

        Returns:
            The found document.
    """
    return Document.nodes.get_or_none(document_id=document_id)


def search_by_patient(patient_id: str) -> NodeSet | None:
    """
        Searches for a document by its patient.

        Args:
            patient_id: The id of the patient.

        Returns:
            The found document.
    """
    node = Patient.search_by_id(patient_id)
    if node is not None:
        return node.document.filter()
    else:
        raise ValueError("Patient not found or no document found")


def search_by_doctor(doctor_id: str) -> NodeSet | None:
    """
        Searches for a document by its patient.

        Args:
            doctor_id: The id of the patient.

        Returns:
            The found document.
    """
    node = Doctor.search_by_id(doctor_id)
    if node is not None:
        return node.document.filter()
    else:
        raise ValueError("Doctor not found or no document found")


def delete(document_id: str) -> bool:
    """
        Deletes a document by its id.

        Args:
            document_id: The id of the document.

        Returns:
            True if the document was deleted, False if not.
    """
    document = search_by_id(document_id)
    if document is not None:
        document.delete()
        return True
    return False


def update(document: Document, **kwargs) -> Document:
    """
        Updates a document.

        Args:
            document: The document to update.

        Returns:
            The updated document.
    """
    for key, value in kwargs.items():
        if value is not None:
            setattr(document, key, value)
    return document.save()
