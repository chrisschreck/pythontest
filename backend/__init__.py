from .databasestuff.nodes.nodeenums import sex
from .databasestuff.nodes.nodeenums import title
from .databasestuff.nodes import city
from .databasestuff.nodes import doctor
from .databasestuff.nodes import healthinsurance
from .databasestuff.nodes import patient
from .databasestuff.nodes import clinic
from .databasestuff.nodes import user
from .databasestuff.nodes import appointment
from .databasestuff.property import phone
from .databasestuff.relationships import insured
from neomodel import db, config

config.DATABASE_URL = "bolt://neo4j:stock-shock-chief-chamber-harbor-4470@itbt.org:7687"

db.set_connection("bolt://neo4j:stock-shock-chief-chamber-harbor-4470@itbt.org:7687")
