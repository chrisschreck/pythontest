import datetime

from argon2 import PasswordHasher
import backend.databasestuff.nodes.user as User
import backend.databasestuff.nodes.patient as Patient
import backend.databasestuff.nodes.doctor as Doctor
import backend.databasestuff.nodes.healthinsurance as HealthInsurance
import backend.databasestuff.nodes.clinic as Surgery
import backend.databasestuff.nodes.city as City
from backend.databasestuff.nodes.nodeenums.sex import Sex
from backend.databasestuff.nodes.nodeenums.title import Title
from neomodel import db

# user = User.search(email="user100@example.org").first()

# User.update(user,json='{"test":true}')


# patient = Patient.create("Chris", "Schreck", datetime.datetime(2000, 1, 1), Sex.MALE)

# print(patient)

# patientset = Patient.search(firstname="Chris")

# for patient in patientset:
#    print(patient)

# doctor = Doctor.create("Davide", "Castiglione", Sex.MALE, Title.DOCTOR)

# doctorset = Doctor.search(firstname="Davide")

# for insetdoctor in doctorset:
#    print(insetdoctor)

# hi = HealthInsurance.create("Eric benutzter Yoghurtbecher GmbH", "Verschmierte Str.", 7,
#                            {"Monday": "8am to 5pm", "Tuesday": "8am to 4pm"})

# hiset = HealthInsurance.search(name__contains="Eric")

# for item in hiset:
#    print(item)

# HealthInsurance.delete(HealthInsurance.search(name="Eric Gangbang Party Gmbh&CoKG").first())

# surgery = Surgery.create("Eric benutzter Yoghurtbecher GmbH", "Verschmierte Str.", 7,
#                         {"Monday": "8am to 5pm", "Tuesday": "8am to 4pm"}, "086369999356", "test@example.com")


# surgeryset = Surgery.search(name__contains="Eric")

# for item in surgeryset:
#    print(item)

# Surgery.delete(Surgery.search(name__contains="Eric").get(uid="30787b5875574c73bc63ca5212f1b0cd"))

# city = City.create("Seligenstadt", "63500")


# cityset = City.search(zip__contains="63")

# for city in cityset:
#     print(city)

# db.driver.close()

# City.delete(City.search(zip__contains="63").get(uid="7aece318320d40e289eb3fe6139684ff"))


user = User.search(email="test@docportal.com").first()

print(user)

relation = User.get_relationship(user)

print(relation[0])

surgery = Patient.get_relationship(relation[0], "Surgery")[0]

print(surgery)

doctor = Surgery.get_relationship(surgery, "doctor")

print(doctor)



#surgery = Surgery.create("Berufsakademische Krankenkasse", "Am Schwimmbad", 3, {"Monday": "8am to 5pm", "Tuesday": "8am to 4pm"}, "017212345678", "surgery@docportal.com")

#Surgery.add_relationship(surgery, relation[0])

db.driver.close()
