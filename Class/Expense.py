from firebase_admin import firestore


class Expense():
    def __init__(self, description, user, value, type_data, date_reg):
        self.description = description
        self.date_reg = date_reg
        self.user = user
        self.value = value
        self.type_data = type_data

    def saveExpense(self, user):
        pass

    @staticmethod
    def getExpenses(user=None):
        db = firestore.client()
        if user is None:
            db_ref = db.collection("expenses").get()
        else:
            db_ref = db.collection("expenses").where(
                u'user', u'==', user).get()

        data = []

        for i in db_ref:
            i = i.to_dict()
            data.append(Expense(i["description"], i["user"],
                                i["value"], i["type"], i["date_reg"]))

        return data
