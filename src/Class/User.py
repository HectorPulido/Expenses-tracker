from firebase_admin import firestore
from Class.Password import Password

class User():
    def __init__(self, user, id):
        self.user = user
        self.id = id

    @staticmethod
    def validate_user(user, password):
        db = firestore.client()
        db_ref = db.collection("users").where(u'user', u'==', user).limit(1).get()
        
        try:
            data = next(db_ref)
            id = data.id
            data = data.to_dict()            
        except:
            return False, None

        p = Password()

        if p.verify_password(data["pass"], password):
            return True, id

        return False, None