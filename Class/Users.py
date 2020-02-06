from firebase_admin import firestore

class User():
    def __init__(self, user, id):
        self.user = user
        self.id = id

    def saveExpense(self, user):
        pass

    @staticmethod
    def getExpenses(user = None):
        db = firestore.client()
        if user is None:
            db_ref = db.collection("expenses").get()
        else:
            db_ref = db.collection("expenses").where(u'user', u'==', user).get()

        data = []

        for i in db_ref:
            i = i.to_dict()
            data.append(Expense(i["concept"], i["date_reg"], i["user"], i["value"]))

        return data