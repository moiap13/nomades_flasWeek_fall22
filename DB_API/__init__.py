import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('DB_API/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def insertDb(collection, id, value):
    if type(value) is dict:
        db.collection(collection).document(id).set(value) # value doit etre un dictionnaire 

def getDocumentDB(collection, id):
    doc = db.collection(collection).document(id).get()
    return doc.to_dict() if doc.exists else None

def getAllDocumentsDB(collection):
    stream = db.collection(collection).stream()
    ret = {}
    for doc in stream:
        ret[doc.id] = doc.to_dict()
    return ret


def updateDB(collection, id, value):
    if type(value) is dict:
        db.collection(collection).document(id).update(value) # value doit etre un dictionnaire

def deleteDB(collection, id):
    db.collection(collection).document(id).delete()

def getDocumentsWhere(collection, field, operator, value):
    stream = db.collection(collection).where(field, operator, value).stream()
    ret = {}
    for doc in stream:
        ret[doc.id] = doc.to_dict()
    return ret

def deleteDB(collection, id):
    db.collection(collection).document(id).delete()