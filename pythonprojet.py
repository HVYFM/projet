from flask import Flask,jsonify,request, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

Pythonprojet=Flask(__name__)
Pythonprojet.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:logou@localhost:5432/db_project"
Pythonprojet.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(Pythonprojet)

class Categorie(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    libelle_categorie = db.Column(db.String(30), nullable=True)
    cat=db.relationship('Livre',backref='categories',lazy=True)

    

    def __init__(self, libelle_categorie):
            self.libelle_categorie = libelle_categorie

    def insert(self):
            db.session.add(self)
            db.session.commit()
    
    def update(self):
            db.session.commit()

    def delete(self):
            db.session.delete(self)
            db.session.commit()

    def format(self):
            return {
            'id': self.id,
            'libelle_categorie': self.libelle_categorie,
            }


class Livre(db.Model):
    __tablename__ = 'livres'
    id=db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.Integer, unique=True)
    titre = db.Column(db.String(30), nullable=False)
    date_publication = db.Column(db.DateTime, nullable=False)
    auteur = db.Column(db.String(30), nullable=False)
    editeur = db.Column(db.String(30), nullable=False)
    categories_id=db.Column(db.Integer, db.ForeignKey('categories.id'),nullable=False)

    def __init__(self, isbn, titre, date_publication, auteur, editeur):
            self.isbn = isbn
            self.titre=titre
            self.auteur =auteur
            self.editeur = editeur
            self.date_publication = date_publication

    def insert(self):
            db.session.add(self)
            db.session.commit()
  
    def update(self):
            db.session.commit()

    def delete(self):
            db.session.delete(self)
            db.session.commit()

    
    def format(self):
            return {
            'isbn': self.isbn,
            'auteur': self.auteur,
            'editeur': self.editeur,
            'titre': self.titre,
            'date publication': self.date_publication,
            }
db.create_all()

#liste de tt les livres

@Pythonprojet.route('/livres',methods=['GET'])
def ajout_livres():
    livres=Livre.query.all()
    formated_books=[ liv.format() for liv in livres]
    return jsonify({
        'success':True,
        'livres':formated_books,
        'total':len(Livre.query.all())
    })

#chercher un livre par son id

@Pythonprojet.route('/livres/<int:id>',methods=['GET'])
def get_one_livre(id):
    livres=Livre.query.get(id)
    if livres is None:
        abort(404)
    else:
        return jsonify({
            "sucess":True,
            "selected_id":id,
            "selected_livres":livres.format()
        })

 #Lister la liste des livres d’une catégorie

# Chercher une catégorie par son id

@Pythonprojet.route('/categories/<int:id>',methods=['GET'])
def get_one_categories(id):
    categories=Categorie.query.get(id)
    if categories is None:
        abort(404)
    else:
        return jsonify({
            "sucess":True,
            "selected_id":id,
            "selected_categories":categories.format()
        })

# Listes toutes les catégories


@Pythonprojet.route('/categories',methods=['GET'])
def ajout_categories():
    categories=Categorie.query.all()
    formated_list=[ cat.format() for cat in categories]
    return jsonify({
        'success':True,
        'categories':formated_list,
        'total':len(Categorie.query.all())
    })

  # Supprimer un livre

@Pythonprojet.route('/livres/<int:id>',methods=['DELETE'])
def delete_livre(id):
    livres=Livre.query.get(id)
    if livres is None:
        abort(404)
    else:
        livres.delete()
        return jsonify({  
            "deleted_id":id,
            "sucess":True,
            "deleted_book":livres.format()
        })

#Supprimer une categorie

@Pythonprojet.route('/categories/<int:id>',methods=['DELETE'])
def delete_categories(id):
    categories=Categorie.query.get(id)
    if categories is None:
        abort(404)
    else:
        categories.delete()
        return jsonify({  
            "deleted_id":id,
            "sucess":True,
            "deleted_student":categories.format()
        })

# Modifier les informations d’un livre


@Pythonprojet.route('/livres/<int:id>',methods=['PATCH'])
def update_livres(id):
    body=request.get_json()
    livres=Livre.query.get(id)

    livres.isbn=body.get('isbn',None)
    livres.titre=body.get('titre',None)
    livres.auteur=body.get('auteur',None)
    livres.editeur=body.get('editeur',None)
    livres.date_publication=body.get('date_publication',None)
    livres.categorie_id=body.get('categorie_id',None)

    livres.update()
    return jsonify({   
        "sucess":True,
        "updated_id_livres":id,
        "new_livres":livres.format()
     })

#Modifier le libellé d’une categorie

@Pythonprojet.route('/categories/<int:id>',methods=['PATCH'])
def update_categories(id):
    body=request.get_json()
    categories=Categorie.query.get(id)
    categories.libelle_categorie=body.get('libelle_categorie',None)

    if categories.libelle_categorie is None:
        abort(400)
    else:
        categories.update()
        return jsonify({   
            "sucess":True,
            "updated_id_categories":id,
            "new_categories":categories.format()
     })