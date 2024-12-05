from config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    builds = db.relationship('Build', backref='user', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)

class Build(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    priority = db.Column(db.Integer, default=0)
    folder_path = db.Column(db.String(200), nullable=True)
    code = db.Column(db.String, unique=True, nullable=True)
    votes = db.relationship('Vote', backref='build', lazy=True)
    perks = db.relationship('Perk', secondary='build_perk', backref=db.backref('builds', lazy='dynamic'))
    __table_args__ = (db.UniqueConstraint('code', name='uq_build_code'),)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    build_id = db.Column(db.Integer, db.ForeignKey('build.id'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)

class Perk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    image = db.Column(db.String(200), nullable=False)

build_perk = db.Table('build_perk',
    db.Column('build_id', db.Integer, db.ForeignKey('build.id'), primary_key=True),
    db.Column('perk_id', db.Integer, db.ForeignKey('perk.id'), primary_key=True)
)