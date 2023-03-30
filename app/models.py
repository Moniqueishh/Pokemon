from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from flask_bootstrap import Bootstrap


db = SQLAlchemy()

# POKEMON TABLE

class Pokemon(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    poke_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    abilities = db.Column(db.String)
    base_exp = db.Column(db.Integer)
    base_atk = db.Column(db.Integer)
    base_hp = db.Column(db.Integer)
    base_def = db.Column(db.Integer)

    def __init__(self, poke_id, name, abilities, base_exp, base_atk, base_hp, base_def):
        self.poke_id = poke_id
        self.name = name
        self.abilities = abilities
        self.base_exp = base_exp
        self.base_atk = base_atk
        self.base_hp = base_hp
        self.base_def = base_def

    def pokeInfo(self):
        return{
            "id" : self.poke_id,
            "name" : self.name,
            "abilities" : self.abilities,
            "base_exp" : self.base_exp,
            "base_atk" : self.base_atk,
            "base_hp" : self.base_hp,
            "base_def" : self.base_def
        }

# USER TABLE

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password) 
        #self.password = password   ---OLD  not hashed

    def saveUser(self):
        db.session.add(self)
        db.session.commit()


# CATCH TABLE

class CatchPoke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    poke_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'))

    def __init__(self, user_id, poke_id):
        self.user_id = user_id
        self.poke_id = poke_id

#     def Create(self):
#         db.session.add(self)
#         db.session.commit()

    # def Update(self):
    #     db.session.commit()

    # def Delete(self):
    #     db.session.delete(self)
    #     db.session.commit()





# BLOG POST TABLE

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String)
    body = db.Column(db.String)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
                                

    def __init__(self, title, img_url, body, user_id):
        self.title = title
        self.img_url = img_url
        self.body = body
        self.user_id = user_id

    def savePoke(self):
        db.session.add(self)
        db.session.commit()

    def savChanges(self):
        db.session.commit()

    def deletePoke(self):
        db.session.delete(self)
        db.session.commit()


