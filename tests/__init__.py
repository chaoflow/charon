import os
import threading
from os import path

from charon import deployment

_multiprocess_shared_ = True

db_file = '%s/test.charon' % (path.dirname(__file__))

def setup():
    deployment.open_database(db_file).close()

def destroy(db, uuid):
    depl = deployment.open_deployment(db, uuid)
    depl.auto_response = "y"
    depl.destroy_vms()

def teardown():
    try:
        db = deployment.open_database(db_file)
        uuids = deployment.query_deployments(db)
        threads = []
        for uuid in uuids:
            threads.append(threading.Thread(target=destroy,args=(db, uuid)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    finally:
        db.close()
        os.remove(db_file)
