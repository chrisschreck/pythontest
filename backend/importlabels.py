from databasestuff.nodes.nodeenums import sex
from databasestuff.nodes.nodeenums import title
from databasestuff.nodes.nodeenums import document_type
from databasestuff.nodes import city
from databasestuff.nodes import doctor
from databasestuff.nodes import healthinsurance
from databasestuff.nodes import patient
from databasestuff.nodes import clinic
from databasestuff.nodes import user
from databasestuff.nodes import appointment
from databasestuff.nodes import document
from databasestuff.property import phone
from databasestuff.relationships import insured
from databasestuff.relationships import has_document
from neomodel import remove_all_labels, install_all_labels, db, config

config.DATABASE_URL = "bolt://neo4j:stock-shock-chief-chamber-harbor-4470@itbt.org:7687"
db.set_connection("bolt://neo4j:stock-shock-chief-chamber-harbor-4470@itbt.org:7687")
remove_all_labels()
install_all_labels()

db.driver.close()
