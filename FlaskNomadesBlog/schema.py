class User(object):
    def __init__(self, uid, email, pwd) -> None:
        self.uid = uid
        self.email = email
        self.pwd = pwd
    def toDict(self):
        return self.__dict__

class Posts(object):
    def __init__(self,titre,corps,uid):
        self.uid=uid
        self.corps=corps
        self.titre=titre
    def todict(self):
        return self.__dict__