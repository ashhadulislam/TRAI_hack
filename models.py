from app import db

class STB_User(db.Model):
    __tablename__ = 'stb_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age=db.Column(db.String())
    gender=db.Column(db.String())
    email = db.Column(db.String())
    contact = db.Column(db.String())
    fingerprint_id = db.Column(db.String())
    stb_id = db.Column(db.String())
    

    def __init__(self, name, age, gender, email, contact, fingerprint_id, stb_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.contact = contact
        self.fingerprint_id = fingerprint_id
        self.stb_id = stb_id


    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'email':self.email,
            'contact': self.contact,
            'fingerprint_id':self.fingerprint_id,
            'stb_id': self.stb_id,

        }


class Remote_Press(db.Model):
    __tablename__ = 'remote_press'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String())
    stb_id = db.Column(db.String())
    button_pressed=db.Column(db.String())
    

    def __init__(self, timestamp, stb_id,button_pressed):
        self.timestamp = timestamp
        self.stb_id = stb_id
        self.button_pressed=button_pressed


    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'timestamp': self.timestamp,
            'stb_id': self.stb_id,
            'button_pressed': self.button_pressed
        }        


class STB(db.Model):
    __tablename__ = 'stb'

    id = db.Column(db.Integer, primary_key=True)
    stb_id=db.Column(db.String())
    active_status = db.Column(db.String())
    lat = db.Column(db.String())
    lon=db.Column(db.String())
    

    def __init__(self, stb_id, active_status,lat,lon):
        self.stb_id = stb_id
        self.active_status = active_status
        self.lat=lat
        self.lon=lon


    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'stb_id': self.stb_id,
            'active_status': self.active_status,
            'lat': self.lat,
            'lon': self.lon
        }   



class Finger_Touch(db.Model):
    __tablename__ = 'finger_touch'

    id = db.Column(db.Integer, primary_key=True)
    stb_id=db.Column(db.String())
    fingerprint_id = db.Column(db.String())
    timestamp = db.Column(db.String())
    
    

    def __init__(self, stb_id, active_status,lat,lon):
        self.stb_id = stb_id
        self.fingerprint_id = fingerprint_id
        self.timestamp=timestamp


    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'stb_id': self.stb_id,
            'fingerprint_id': self.fingerprint_id,
            'timestamp': self.timestamp
        }   