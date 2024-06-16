import datetime
import json

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from argon2 import PasswordHasher

import backend.databasestuff.nodes.user as User
import backend.databasestuff.nodes.patient as Patient
import backend.databasestuff.nodes.doctor as Doctor
import backend.databasestuff.nodes.clinic as Clinic
import backend.databasestuff.nodes.document as Document

from backend.mongodb.collections.billing_documents import Billing_documents

from backend.databasestuff.nodes.nodeenums.sex import Sex as Sex
from backend.databasestuff.nodes.nodeenums.title import Title as Title
from backend.databasestuff.nodes.nodeenums.document_type import DocumentType as DocumentType
from neomodel import db, DoesNotExist, UniqueProperty, RequiredProperty

ph = PasswordHasher()


def create_app() -> Flask:
    """this function is used to create a flask app.
    
    Keyword arguments:
    Return: flask instance
    """

    app = Flask(__name__)
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

    app.secret_key = "ourAppShallBeGuardedByTheseWords(c)DocPortalplzdontHack#2023"

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Beispielcode zum Laden des Benutzers anhand der Benutzer-ID
        # Achte darauf, dass du hier den Code entsprechend deiner Anwendungslogik anpasst
        try:
            return User.search(uid=user_id).first()
        except DoesNotExist:
            pass

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.login_manager.unauthorized_handler
    def unauthorized():
        flash('Sie müssen angemeldet sein, um diese Seite zu sehen.', 'error')
        return redirect(url_for('login'))

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            user = current_user
            relation = User.get_relationship(user)
            return render_template("index.html", user=user.is_active, role=relation[1])
        else:
            return render_template("index.html")

    @app.route('/features')
    def features():
        if current_user.is_authenticated:
            user = current_user
            relation = User.get_relationship(user)
            return render_template("lobby/features.html", user=user.is_active, role=relation[1])
        else:
            return render_template("lobby/features.html")

    @app.route('/pricing')
    def pricing():
        if current_user.is_authenticated:
            user = current_user
            relation = User.get_relationship(user)
            return render_template("lobby/pricing.html", user=user.is_active, role=relation[1])
        else:
            return render_template("lobby/pricing.html")

    @app.route('/about')
    def about():
        if current_user.is_authenticated:
            user = current_user
            relation = User.get_relationship(user)
            return render_template("lobby/about.html", user=user.is_active, role=relation[1])
        else:
            return render_template("lobby/about.html")

    @app.route('/team')
    def team():
        if current_user.is_authenticated:
            user = current_user
            relation = User.get_relationship(user)
            return render_template("lobby/team.html", user=user.is_active, role=relation[1])
        else:
            return render_template("lobby/team.html")

    @app.route('/community')
    def community():
        if current_user.is_authenticated:
            user = current_user
            relation = User.get_relationship(user)
            return render_template("lobby/community.html", user=user.is_active, role=relation[1])
        else:
            return render_template("lobby/community.html")

    @app.route('/help')
    def help():
        if current_user.is_authenticated:
            user = current_user
            relation = User.get_relationship(user)
            return render_template("lobby/help.html", user=user.is_active, role=relation[1])
        else:
            return render_template("lobby/help.html")

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            # Überprüfen, ob die E-Mail-Adresse im System existiert
            try:
                user = User.search(email=email).first()
                if not user:
                    flash('Ungültige E-Mail-Adresse.', 'error')
                    return redirect(url_for('login'))
            except DoesNotExist:
                flash('Ungültige E-Mail-Adresse.', 'error')
                return redirect(url_for('login'))
                pass

            # Überprüfen, ob das eingegebene Passwort korrekt ist
            if ph.verify(user.password, password):
                # Anmelden des Benutzers
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Ungültiges Passwort.', 'error')
                return redirect(url_for('login'))

        return render_template("app/login.html")

    @app.route('/forgot', methods=['POST', 'GET'])
    def forgot():
        if request.method == 'POST':
            email = request.form['email']

            # Überprüfen, ob die E-Mail-Adresse im System existiert
            try:
                user = User.search(email=email).first()
                if not user:
                    flash('Ungültige E-Mail-Adresse.', 'error')
                    return redirect(url_for('forgot'))
                else:
                    flash('Eine E-Mail mit weiteren Anweisungen wurde an die angegebene E-Mail-Adresse gesendet.',
                          'success')
                    return redirect(url_for('login'))
            except DoesNotExist:
                flash('Ungültige E-Mail-Adresse.', 'error')
                return redirect(url_for('forgot'))
                pass

        return render_template("app/forgot.html")

    @app.route('/forgor', methods=['POST', 'GET'])
    def forgor():
        if request.method == 'POST':
            email = request.form['email']

            # Überprüfen, ob die E-Mail-Adresse im System existiert
            try:
                user = User.search(email=email).first()
                if not user:
                    flash('Ungültige E-Mail-Adresse.', 'error')
                    return redirect(url_for('forgor'))
                else:
                    User.update(user, password=ph.hash("forgor"))
                    return redirect(url_for('login'))
            except DoesNotExist:
                flash('Ungültige E-Mail-Adresse.', 'error')
                return redirect(url_for('forgor'))
                pass

        return render_template("app/forgor.html")

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Sie wurden abgemeldet.', 'success')
        return redirect(url_for('index'))

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def get_fileextension(filename):
        return filename.rsplit('.', 1)[1].lower()

    @app.route('/uploadfile', methods=['POST'])
    @login_required
    def uploadfile():
        if request.method == 'POST':
            type = request.form['collection']
            file = request.files['file']
            user = current_user
            relation = User.get_relationship(user)
            doc_type = DocumentType
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('index'))
            # Get Filename-Extension
            if file and allowed_file(file.filename):
                if get_fileextension(file.filename) == 'txt':
                    text = file.read()
                    json_dict = {
                        "filename": file.filename,
                        "content": text.decode('utf-8')
                    }
                    # MongoDB - Dokument erstellen
                    match type:
                        case "Billing_documents":
                            doc_type = DocumentType.BILLING_DOCUMENT
                            document = Billing_documents()
                            inserted_id = document.create(user.uid, 1, json.dumps(json_dict))

                    if inserted_id:
                        inserted_id = str(inserted_id)
                        if relation[1] == 'patient':
                            Document.create(inserted_id, doc_type, patient=relation[0])

        return redirect(url_for('index'))

    @app.route('/register', methods=['POST', 'GET'])
    def registerProd():
        return render_template("app/registerProd.html")


    @app.route('/registerUser', methods=['POST', 'GET'])
    def register():
        if request.method == 'POST':
            email = request.form['email']
            role = request.form['role']
            password = request.form['pwd']
            password_repeat = request.form['pwd2']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            birthdate = request.form['birthdate']
            sex = request.form['sex']
            title = request.form['title']
            phone = request.form['phone']

            if password != password_repeat:
                flash('Die Passwörter stimmen nicht überein.', 'error')
                return redirect(url_for('register'))

            # Überprüfen, ob die E-Mail-Adresse bereits registriert ist
            try:
                if User.search(email=email).first():
                    flash('Diese E-Mail-Adresse ist bereits registriert.', 'error')
                    return redirect(url_for('register'))
            except DoesNotExist:
                pass

            match sex:
                case "male":
                    sex = Sex.MALE
                case "female":
                    sex = Sex.FEMALE
                case _:
                    sex = Sex.NON_BINARY

            match title:
                case "doctor":
                    title = Title.DOCTOR
                case "professor":
                    title = Title.PROFESSOR
                case "profdoc":
                    title = Title.PROF_DOC
                case "diploma":
                    title = Title.DIPLOMA
                case "bachelor":
                    title = Title.BACHELOR
                case "master":
                    title = Title.MASTER
                case "magister":
                    title = Title.MAGISTER
                case _:
                    title = Title.BLANC

            if role == "patient":
                user = User.create(email, ph.hash(password))
                patient = Patient.create(firstname, lastname, datetime.datetime.strptime(birthdate, '%Y-%m-%d'), sex,
                                         title, phone=phone)
                User.add_relationship(user, patient)
            elif role == "doctor":
                user = User.create(email, ph.hash(password))
                doctor = Doctor.create(firstname, lastname, datetime.datetime.strptime(birthdate, '%Y-%m-%d'), sex,
                                       title, phone=phone)
                User.add_relationship(user, doctor)
            else:
                flash('Es wurde keine Rolle ausgewählt', 'error')
                return redirect(url_for('register'))

            # Anmelden des Benutzers
            login_user(user)

            # Weiterleitung zur Dashboard-Seite nach erfolgreicher Registrierung
            return redirect(url_for('dashboard'))

        return render_template("app/register.html")

    @app.route('/clinic/register', methods=['POST', 'GET'])
    def registerClinic():
        if request.method == 'POST':
            securitycode = request.form['security']
            if securitycode == "imaclinicnotarandomperson":
                email = request.form['email']
                password = request.form['pwd']
                password_repeat = request.form['pwd2']
                clinic = request.form['clinic']
                phone = request.form['phone']

                if password != password_repeat:
                    flash('Die Passwörter stimmen nicht überein.', 'error')
                    return redirect(url_for('registerClinic'))

                # Überprüfen, ob die E-Mail-Adresse bereits registriert ist
                try:
                    if User.search(email=email).first():
                        flash('Diese E-Mail-Adresse ist bereits registriert.', 'error')
                        return redirect(url_for('registerClinic'))
                except DoesNotExist:
                    pass

                user = User.create(email, ph.hash(password))
                clinic = Clinic.create(clinic,
                                       "Musterstrasse",
                                       1,
                                       {"monday": "08:00-12:00", "tuesday": "08:00-12:00",
                                        "wednesday": "08:00-12:00", },
                                       phone,
                                       email)
                User.add_relationship(user, clinic)

                # Anmelden des Benutzers
                login_user(user)

                # Weiterleitung zur Dashboard-Seite nach erfolgreicher Registrierung
                return redirect(url_for('clinicDashboard'))
            else:
                flash('Der Sicherheitscode ist falsch.', 'error')
                return redirect(url_for('clinicRegister'))

        return render_template("app/clinic/register.html")

    @app.route('/clinic/login', methods=['POST', 'GET'])
    def clinicLogin():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            # Überprüfen, ob die E-Mail-Adresse im System existiert
            try:
                user = User.search(email=email).first()
                if not user:
                    flash('Ungültige E-Mail-Adresse.', 'error')
                    return redirect(url_for('clinicLogin'))
            except DoesNotExist:
                flash('Ungültige E-Mail-Adresse.', 'error')
                return redirect(url_for('clinicLogin'))
                pass

            # Überprüfen, ob das eingegebene Passwort korrekt ist
            if ph.verify(user.password, password):
                # Anmelden des Benutzers
                login_user(user)
                return redirect(url_for('clinicDashboard'))
            else:
                flash('Ungültiges Passwort.', 'error')
                return redirect(url_for('clinicLogin'))

        return render_template("app/clinic/login.html")

    @app.route('/clinic/registerDoctor', methods=['POST'])
    @login_required
    def registerDoctorFromClinic():
        if request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            birthdate = request.form['birthdate']
            sex = request.form['sex']
            title = request.form['title']

            match sex:
                case "male":
                    sex = Sex.MALE
                case "female":
                    sex = Sex.FEMALE
                case _:
                    sex = Sex.NON_BINARY

            match title:
                case "doctor":
                    title = Title.DOCTOR
                case "professor":
                    title = Title.PROFESSOR
                case "profdoc":
                    title = Title.PROF_DOC
                case "diploma":
                    title = Title.DIPLOMA
                case "bachelor":
                    title = Title.BACHELOR
                case "master":
                    title = Title.MASTER
                case "magister":
                    title = Title.MAGISTER
                case _:
                    title = Title.BLANC

            try:
                doctor = Doctor.create(firstname, lastname, datetime.datetime.strptime(birthdate, '%Y-%m-%d'), sex,
                                       title)
                print(doctor)
                user = current_user
                relation = User.get_relationship(user)
                print(relation[1])
                clinic = relation[0]
                print(clinic)
                Doctor.add_relationship(doctor, clinic)
                flash(f'Doktor {firstname} {lastname} wurde erfolgreich angelegt UID: {doctor.uid}', 'info')
                return redirect(url_for('clinicDashboard'))
            except:
                flash('Ein Fehler ist aufgetreten.', 'error')
                return redirect(url_for('clinicDashboard'))

    @app.route('/doctor/register', methods=['POST', 'GET'])
    def registerDoctor():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['pwd']
            password_repeat = request.form['pwd2']
            uid = request.form['uid']

            if password != password_repeat:
                flash('Die Passwörter stimmen nicht überein.', 'error')
                return redirect(url_for('registerDoctor'))

            # Überprüfen, ob die E-Mail-Adresse bereits registriert ist
            try:
                if User.search(email=email).first():
                    flash('Diese E-Mail-Adresse ist bereits registriert.', 'error')
                    return redirect(url_for('registerDoctor'))
            except DoesNotExist:
                pass

            # try to find the doctor with the uid and check if it is already registered by checking for a user relationship
            try:
                doctor = Doctor.search(uid=uid).first()
                if Doctor.check_if_doctor_has_user(doctor):
                    flash('Dieser Arzt ist bereits registriert.', 'error')
                    return redirect(url_for('registerDoctor'))
            except DoesNotExist:
                flash('Dieser Arzt existiert nicht.', 'error')
                return redirect(url_for('registerDoctor'))
                pass

            user = User.create(email, ph.hash(password))
            User.add_relationship(user, doctor)

            login_user(user)

            return redirect(url_for('dashboard'))

        return render_template("app/doctor/register.html")

    @app.route('/clinic/dashboard', methods=['POST', 'GET'])
    @login_required
    def clinicDashboard():
        user = current_user
        print(current_user)
        relation = User.get_relationship(user)
        if relation[1] == "clinic":
            print(relation[0])
            fullname = str(relation[0].name)
            return render_template("app/clinic/dashboard.html", user=fullname, role=relation[1])
        else:
            return redirect(url_for('index'))

    @app.route('/clinic/employees', methods=['POST', 'GET'])
    @login_required
    def clinicEmployees():
        user = current_user
        relation = User.get_relationship(user)
        if relation[1] == "clinic":
            print(relation[0])
            fullname = str(relation[0].name)
            print(Clinic.list_doctors(relation[0]))
            employees = []
            for doctor in Clinic.list_doctors(relation[0]):
                employees.append((doctor.uid, doctor.firstname, doctor.lastname, "Arzt"))
            return render_template("app/clinic/sites/employees.html",
                                   user=fullname,
                                   role=relation[1],
                                   employees=employees)
        else:
            return redirect(url_for('index'))

    @app.route('/clinic/appointments', methods=['POST', 'GET'])
    @login_required
    def clinicAppointments():
        user = current_user
        relation = User.get_relationship(user)
        if relation[1] == "clinic":
            print(relation[0])
            fullname = str(relation[0].name)
            return render_template("app/clinic/sites/appointments.html", user=fullname, role=relation[1], appointments=[
                ("ID1", "Leter Pustig", "weihnachten", "mind. 12 Uhr", "DR. med. Fred Feuerstein"),
                ("ID2", "Leter Pustig", "weihnachten", "mind. 12 Uhr", "DR. med. Fred Feuerstein"),
                ("ID3", "Leter Pustig", "weihnachten", "mind. 12 Uhr", "DR. med. Fred Feuerstein"),
                ("ID4", "Leter Pustig", "weihnachten", "mind. 12 Uhr", "DR. med. Fred Feuerstein"),
                ("ID5", "Leter Pustig", "weihnachten", "mind. 12 Uhr", "DR. med. Fred Feuerstein"),
                ("ID6", "Leter Pustig", "weihnachten", "mind. 12 Uhr", "DR. med. Fred Feuerstein"),
                ("ID7", "Leter Pustig", "weihnachten", "mind. 12 Uhr", "DR. med. Fred Feuerstein"),
                ("ID8", "Leter Pustig", "weihnachten", "mind. 12 Uhr", "DR. med. Fred Feuerstein"),
                ("ID9", "Leter Pustig", "weihnachten", "mind. 12 Uhr", "DR. med. Fred Feuerstein"),
                ], doctors=[("Dr. Sacknase"), ("Dr. Nacksase"), ("Dr. Kackhase"),("Dr. Hackkase"),])
        else:
            return redirect(url_for('index'))

    @app.route('/clinic/Patients', methods=['POST', 'GET'])
    @login_required
    def clinicPatients():
        user = current_user
        relation = User.get_relationship(user)
        if relation[1] == "clinic":
            print(relation[0])
            fullname = str(relation[0].name)
            return render_template("app/clinic/sites/patients.html", user=fullname, role=relation[1], patients=[("ID1", "Schmacko Fatz", "Dr. Nacksase")])
        else:
            return redirect(url_for('index'))

    @app.route('/clinic/Inventory', methods=['POST', 'GET'])
    @login_required
    def clinicInventory():
        user = current_user
        relation = User.get_relationship(user)
        if relation[1] == "clinic":
            print(relation[0])
            fullname = str(relation[0].name)
            return render_template("app/clinic/sites/inventory.html",
                                   user=fullname,
                                   role=relation[1],
                                   inventory=[
                                       ("ID1", "Paracetamol 600mg", "100", "01.01.2027"),
                                   ],
                                   inventory2=[
                                       ("ID1", "Codein Konzentrat", "50", "05.01.2024")
                                   ])
        else:
            return redirect(url_for('index'))

    @app.route('/clinic/documents', methods=['POST', 'GET'])
    @login_required
    def clinicDocuments():
        user = current_user
        relation = User.get_relationship(user)
        if relation[1] == "clinic":
            print(relation[0])
            fullname = str(relation[0].name)
            return render_template("app/clinic/sites/documents.html", user=fullname, role=relation[1])
        else:
            return redirect(url_for('index'))

    @app.route('/app/dashboard')
    @login_required
    def dashboard():
        user = current_user
        print(current_user)
        relation = User.get_relationship(user)
        if relation[1] == "patient":
            print(relation[0])
            fullname = str(relation[0].firstname) + " " + str(relation[0].lastname)
            return render_template("app/dashboard.html", user=fullname, role=relation[1])
        elif relation[1] == "doctor":
            print(relation[0])
            fullname = str(relation[0].firstname) + " " + str(relation[0].lastname)
            # check if the doctor is connected to the clinic
            if Doctor.get_relationship(relation[0], "clinic"):
                # check if the clinic is connected to the doctor
                # if not Clinic.get_relationship(Doctor.get_relationship(relation[0], "clinic")[0], "doctor"):
                # this cant work if more than one doctor is connected to the clinic therefore
                # we need to check for the doctor in the clinic by searching for the uid
                if not Clinic.check_if_doctor_is_in_clinic(Doctor.get_relationship(relation[0], "clinic")[0], relation[0]):
                    # if not, connect them
                    Clinic.add_relationship(Doctor.get_relationship(relation[0], "clinic")[0], relation[0])
            return render_template("app/dashboard.html", user=fullname, role=relation[1])
        else:
            return redirect(url_for('index'))

    @app.route('/app/mydocs')
    @login_required
    def meineärzte():
        user = current_user
        relation = User.get_relationship(user)
        fullname = str(relation[0].firstname) + " " + str(relation[0].lastname)
        return render_template("app/meineärzte.html", user=fullname, role=relation[1])

    @app.route('/app/appointments')
    @login_required
    def termine():
        user = current_user
        relation = User.get_relationship(user)
        fullname = str(relation[0].firstname) + " " + str(relation[0].lastname)
        return render_template("app/termine.html", user=fullname, role=relation[1])

    @app.route('/app/mymed')
    @login_required
    def meinemedikamente():
        user = current_user
        relation = User.get_relationship(user)
        fullname = str(relation[0].firstname) + " " + str(relation[0].lastname)
        return render_template("app/meinemedikamente.html", user=fullname, role=relation[1])

    @app.route('/app/anamnesebogen')
    @login_required
    def anamnesebogen():
        user = current_user
        relation = User.get_relationship(user)
        fullname = str(relation[0].firstname) + " " + str(relation[0].lastname)
        return render_template("app/anamnesebogen.html", user=fullname, role=relation[1])

    @app.route('/app/documents')
    @login_required
    def dokumente():
        user = current_user
        relation = User.get_relationship(user)
        fullname = str(relation[0].firstname) + " " + str(relation[0].lastname)
        return render_template("app/dokumente.html", user=fullname, role=relation[1])

    @app.route('/app/inbox')
    @login_required
    def postfach():
        user = current_user
        relation = User.get_relationship(user)
        fullname = str(relation[0].firstname) + " " + str(relation[0].lastname)
        return render_template("app/postfach.html", user=fullname, role=relation[1])

    @app.route('/app/settings')
    @login_required
    def einstellungen():
        user = current_user
        relation = User.get_relationship(user)
        fullname = str(relation[0].firstname) + " " + str(relation[0].lastname)
        firstname = str(relation[0].firstname)
        lastname = str(relation[0].lastname)
        return render_template(
            "app/einstellungen.html",
            user=fullname,
            email=user.email,
            firstname=firstname,
            lastname=lastname,
            role=relation[1],
        )

    @app.route('/app/update_settings', methods=['POST'])
    @login_required
    def update_settings():
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        # Überprüfen, ob das eingegebene Passwort korrekt ist
        if password != confirm_password:
            flash('Die Passwörter stimmen nicht überein.', 'error')
            return redirect(url_for('einstellungen'))

        try:
            user = User.search(uid=current_user.uid).first()
            if not user:
                flash('Benutzer nicht gefunden.', 'error')
                return redirect(url_for('einstellungen'))
        except DoesNotExist:
            flash('Benutzer nicht gefunden.', 'error')
            return redirect(url_for('einstellungen'))

        # Aktualisieren der Benutzereinstellungen

        User.update(user, email=email)

        Patient.update(
            User.get_relationship(current_user)[0],
            firstname=firstname,
            lastname=lastname
        )

        User.update(user, lastname=lastname)

        if password:
            User.update(user, password=ph.hash(password))

        flash('Einstellungen erfolgreich aktualisiert.', 'success')
        return redirect(url_for('einstellungen'))

    @app.route('/macros/sidebar')
    def sidebar():
        return render_template("macros/sidebar.html")

    @app.route('/macros/userheader')
    def userheader():
        return render_template("macros/userheader.html")

    @app.route('/macros/table')
    def table():
        return render_template("macros/table.html")

    return app
