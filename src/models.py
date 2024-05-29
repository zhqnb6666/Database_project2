from app import db


class Station(db.Model):
    __tablename__ = 'stations'
    station_id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255), unique=True, nullable=False)
    district = db.Column(db.String(255))
    intro = db.Column(db.Text)
    chinese_name = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)


class Chukou(db.Model):
    __tablename__ = 'chukous'
    chukou_id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id'), nullable=False)
    chukou_name = db.Column(db.String(255), unique=True, nullable=False)


class Out(db.Model):
    __tablename__ = 'outs'
    out_id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id'), nullable=False)
    outt = db.Column(db.String(255), unique=True, nullable=False)
    textt = db.Column(db.Text)


class Bus(db.Model):
    __tablename__ = 'buses'
    bus_id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id'), nullable=False)
    bus_name = db.Column(db.String(255))
    bus_info = db.Column(db.Text)
    chukou = db.Column(db.String(255))


class Passenger(db.Model):
    __tablename__ = 'passengers'
    passenger_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    id_number = db.Column(db.Text, unique=True, nullable=False)
    phone_number = db.Column(db.Text)
    gender = db.Column(db.Text)
    district = db.Column(db.Text)
    def to_dict(self):
        return {
            'name': self.name,
            'id_number': self.id_number,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'district': self.district
        }


class Card(db.Model):
    __tablename__ = 'cards'
    card_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text, unique=True, nullable=False)
    money = db.Column(db.Numeric, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    def to_dict(self):
        return {
            'code': self.code,
            'money': self.money,
            'create_time': self.create_time
        }


class Line(db.Model):
    __tablename__ = 'lines'
    line_id = db.Column(db.Integer, primary_key=True)
    line_name = db.Column(db.Text, unique=True, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    intro = db.Column(db.Text)
    mileage = db.Column(db.Numeric, nullable=False)
    color = db.Column(db.Text)
    first_opening = db.Column(db.Date)
    url = db.Column(db.Text)


class LineStation(db.Model):
    __tablename__ = 'line_stations'
    line_station_id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.Integer, db.ForeignKey('lines.line_id'), nullable=False)
    station_name = db.Column(db.Text, db.ForeignKey('stations.english_name'), nullable=False)
    station_order = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint('line_id', 'station_name'),)


class RidePassenger(db.Model):
    __tablename__ = 'ride_passenger'
    ride_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text, db.ForeignKey('passengers.id_number'), nullable=False)
    start_station = db.Column(db.Text, db.ForeignKey('stations.english_name'), nullable=False)
    end_station = db.Column(db.Text, db.ForeignKey('stations.english_name'), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    level = db.Column(db.Integer, nullable=False, default=0)


class RideCard(db.Model):
    __tablename__ = 'ride_card'
    ride_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text, db.ForeignKey('cards.code'), nullable=False)
    start_station = db.Column(db.Text, db.ForeignKey('stations.english_name'), nullable=False)
    end_station = db.Column(db.Text, db.ForeignKey('stations.english_name'), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    level = db.Column(db.Integer, nullable=False, default=0)


class UnexitedRidePassenger(db.Model):
    __tablename__ = 'UnexitedRidePassenger'
    ride_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text, db.ForeignKey('passengers.id_number'), nullable=False)
    start_station = db.Column(db.Text, db.ForeignKey('stations.english_name'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    level = db.Column(db.Integer, nullable=False, default=0)
    # Add a relationship to the Passenger model
    passenger = db.relationship('Passenger', backref=db.backref('unexited_rides', lazy=True))



class UnexitedRideCard(db.Model):
    __tablename__ = 'UnexitedRideCard'
    ride_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text, db.ForeignKey('cards.code'), nullable=False)
    start_station = db.Column(db.Text, db.ForeignKey('stations.english_name'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    level = db.Column(db.Integer, nullable=False, default=0)
    # Add a relationship to the Card model
    card = db.relationship('Card', backref=db.backref('unexited_rides', lazy=True))
