from firebase_admin import firestore

class Expense():
    def __init__(self, concept, date_reg, user, value):
        self.concept = concept
        self.date_reg = date_reg
        self.user = user
        self.value = value

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