from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging
from flask_cors import CORS  # 导入 CORS
from datetime import datetime
from function import *

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)  # Enable CORS on the entire app

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    # Register routes
    register_routes(app)

    # Route to serve the HTML file
    @app.route('/')
    def serve_html():
        return send_from_directory('static', 'Transit_system.html')

    return app


def register_routes(app):
    from models import Station, Line, LineStation, Passenger, Card, RidePassenger, RideCard, Bus, Out, UnexitedRidePassenger, UnexitedRideCard

    @app.route('/test_connection', methods=['GET'])
    def test_connection():
        return jsonify({'message': 'Connection successful!'}), 200

    # 1. Station Management
    # Add a station
    @app.route('/stations', methods=['POST'])
    def add_station():
        data = request.json
        try:
            new_station = Station(english_name=data['english_name'], district=data['district'], intro=data['intro'],
                                  chinese_name=data['chinese_name'], status=data['status'])
            db.session.add(new_station)
            db.session.commit()
            return jsonify({'message': 'Station added'}), 201
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    # Update a station
    @app.route('/stations/<string:station_name>', methods=['PUT'])
    def update_station(station_name):
        data = request.json
        try:
            station = db.session.query(Station).filter(Station.english_name == station_name).first()
            if not station:
                return jsonify({'message': 'Station not found'}), 404

            station.english_name = data.get('english_name', station.english_name)
            station.district = data.get('district', station.district)
            station.intro = data.get('intro', station.intro)
            station.chinese_name = data.get('chinese_name', station.chinese_name)
            station.status = data.get('status', station.status)
            db.session.commit()
            return jsonify({'message': 'Station updated'}), 200
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    @app.route('/stations/<string:station_name>', methods=['DELETE'])
    def delete_station(station_name):
        try:
            station = db.session.query(Station).filter(Station.english_name == station_name).first()
            if not station:
                return jsonify({'message': 'Station not found'}), 404

            db.session.delete(station)
            db.session.commit()
            return jsonify({'message': 'Station deleted'}), 200
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    # 2. line Management

    @app.route('/lines', methods=['POST'])
    def add_line():
        data = request.json
        try:
            line = Line(line_name=data['line_name'], start_time=data['start_time'], end_time=data['end_time'],
                        intro=data['intro'], mileage=data['mileage'], color=data['color'],
                        first_opening=data['first_opening'],
                        url=data['url'])
            db.session.add(line)
            db.session.commit()
            return jsonify({'message': 'Line added'}), 201
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    @app.route('/lines/<string:line_name>', methods=['PUT'])
    def update_line(line_name):
        data = request.json
        try:
            line = db.session.query(Line).filter(Line.line_name == line_name).first()
            if not line:
                return jsonify({'message': 'Line not found'}), 404

            line.line_name = data.get('line_name', line.line_name)
            line.start_time = data.get('start_time', line.start_time)
            line.end_time = data.get('end_time', line.end_time)
            line.intro = data.get('intro', line.intro)
            line.mileage = data.get('mileage', line.mileage)
            line.color = data.get('color', line.color)
            line.first_opening = data.get('first_opening', line.first_opening)
            line.url = data.get('url', line.url)
            db.session.commit()
            return jsonify({'message': 'Line updated'}), 200
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    @app.route('/lines/<string:line_name>', methods=['DELETE'])
    def delete_line(line_name):
        try:
            line = db.session.query(Line).filter(Line.line_name == line_name).first()
            if not line:
                return jsonify({'message': 'Line not found'}), 404

            db.session.delete(line)
            db.session.commit()
            return jsonify({'message': 'Line deleted'}), 200
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    # 3. Line Station Management

    @app.route('/line_stations', methods=['POST', 'DELETE'])
    def manage_line_stations():
        if request.method == 'POST':
            # Adding a station to a line
            data = request.json
            line = db.session.query(Line).filter(Line.line_name == data['line_name']).first()
            if line:
                line_id = line.line_id
            else:
                return jsonify({'message': 'Line not found'}), 400
            try:
                new_station = LineStation(
                    line_id=line_id,
                    station_name=data['station_name'],
                    station_order=data['station_order']
                )
                db.session.add(new_station)
                db.session.commit()
                return jsonify({'message': 'Station added to line successfully'}), 201
            except Exception as e:
                print(str(e))
                db.session.rollback()
                return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

        elif request.method == 'DELETE':
            # Removing a station from a line
            data = request.json
            line = db.session.query(Line).filter(Line.line_name == data['line_name']).first()
            if line:
                line_id = line.line_id
            else:
                return jsonify({'message': 'Line not found'}), 400
            try:
                line_station = db.session.query(LineStation).filter(
                    LineStation.line_id == line_id,
                    LineStation.station_name == data['station_name']
                ).first()
                if line_station:
                    db.session.delete(line_station)
                    db.session.commit()
                    return jsonify({'message': 'Station removed from line successfully'}), 200
                else:
                    return jsonify({'message': 'Station not found on the specified line'}), 404
            except Exception as e:
                print(str(e))
                db.session.rollback()
                return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

        else:
            return jsonify({'message': 'Invalid request method'}), 405

    # 4. Station Search@app.route('/search_stations/<string:line_name>/<int:station_order>/<int:n>', methods=['GET'])
    @app.route('/search_stations/<string:line_name>/<int:station_order>/<int:n>', methods=['GET'])
    def search_stations(line_name, station_order, n):
        # Find the station order for the stations we are interested in
        order_ahead = station_order - n
        order_behind = station_order + n

        # Query for the line_id from Line model
        line = db.session.query(Line).filter(Line.line_name == line_name).first()
        if line:
            line_id = line.line_id
        else:
            return jsonify({'message': 'Line not found'}), 400

        # Query for the station n positions ahead
        station_ahead = db.session.query(LineStation).filter(
            LineStation.line_id == line_id,
            LineStation.station_order == order_ahead
        ).first()

        # Query for the station n positions behind
        station_behind = db.session.query(LineStation).filter(
            LineStation.line_id == line_id,
            LineStation.station_order == order_behind
        ).first()

        # Prepare the response
        stations_data = {
            'station_ahead': station_ahead.station_name if station_ahead else None,
            'station_behind': station_behind.station_name if station_behind else None
        }

        if station_ahead or station_behind:
            return jsonify(stations_data), 200
        else:
            return jsonify({'message': 'No stations found'}), 404

    # 5. Boarding Functionality
    @app.route('/board_passenger', methods=['POST'])
    def board_passenger():
        data = request.json
        try:
            ride = UnexitedRidePassenger(user_id=data['user_id'], start_station=data['start_station'],
                                         start_time=datetime.now(), level=data['carriage_type'])
            start_station = (db.session.query(Station)
                             .filter(Station.english_name == data['start_station']).first())
            if start_station.status == 1 or start_station.status == 2:
                return jsonify({'message': 'Start station is not operational'}), 400
            db.session.add(ride)
            db.session.commit()
            return jsonify({'message': 'Passenger boarded'}), 201
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    @app.route('/exit_passenger', methods=['POST'])
    def exit_passenger():
        data = request.json
        try:
            # Query for the ride that needs to be exited
            ride = db.session.query(UnexitedRidePassenger).filter(
                UnexitedRidePassenger.user_id == data['user_id'],
                UnexitedRidePassenger.start_station == data['start_station'],
            ).first()

            if ride:
                # Get the Chinese names of the start and end stations
                start_station_chinese = db.session.query(Station.chinese_name).filter(
                    Station.english_name == ride.start_station).first()[0]
                end_station = db.session.query(Station).filter(
                    Station.english_name == data['end_station']).first()

                if end_station.status in [1, 2]:
                    return jsonify({'message': 'End station is not operational'}), 400

                end_station_chinese = end_station.chinese_name

                # Get the price
                price = get_price(start_station_chinese, end_station_chinese)
                if ride.level == 1:
                    price = price * 2

                # Create a new RidePassenger object with the same data
                completed_ride = RidePassenger(
                    user_id=ride.user_id,
                    start_station=ride.start_station,
                    start_time=ride.start_time,
                    end_station=data['end_station'],
                    end_time=datetime.now(),
                    price=price
                )

                # Add the completed ride to the RidePassenger table
                db.session.add(completed_ride)

                # Delete the ride from the UnexitedRidePassenger table
                db.session.delete(ride)

                db.session.commit()
                return jsonify({'message': 'Passenger exited', 'price': price}), 200
            else:
                return jsonify({'message': 'No active ride found for this passenger'}), 404
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    @app.route('/board_card', methods=['POST'])
    def board_card():
        data = request.json
        # Create a new ride record for a card
        try:
            ride = UnexitedRideCard(
                user_id=data['user_id'],
                start_station=data['start_station'],
                start_time=datetime.now(),
                level=data['carriage_type']
            )
            start_station = db.session.query(Station).filter(
                Station.english_name == data['start_station']).first()
            if start_station.status == 1 or start_station.status == 2:
                return jsonify({'message': 'Start station is not operational'}), 400
            db.session.add(ride)
            db.session.commit()
            return jsonify({'message': 'Card user boarded'}), 201
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    @app.route('/exit_card', methods=['POST'])
    def exit_card():
        data = request.json
        try:
            # Query for the ride that needs to be exited
            ride = db.session.query(UnexitedRideCard).filter(
                UnexitedRideCard.user_id == data['user_id'],
                UnexitedRideCard.start_station == data['start_station'],
            ).first()

            if ride:
                # Create a new RideCard object with the same data
                start_station_chinese = db.session.query(Station.chinese_name).filter(
                    Station.english_name == ride.start_station).first()[0]

                end_station = db.session.query(Station).filter(
                    Station.english_name == data['end_station']).first()

                if end_station.status in [1, 2]:
                    return jsonify({'message': 'End station is not operational'}), 400

                end_station_chinese = end_station.chinese_name
                price = get_price(start_station_chinese, end_station_chinese)
                if ride.level == 1:
                    price = price * 2
                completed_ride = RideCard(
                    user_id=ride.user_id,
                    start_station=ride.start_station,
                    start_time=ride.start_time,
                    end_station=data['end_station'],
                    price=price,
                    end_time=datetime.now()
                )

                # Add the completed ride to the RideCard table
                db.session.add(completed_ride)

                # Delete the ride from the UnexitedRideCard table
                db.session.delete(ride)

                db.session.commit()
                return jsonify({'message': 'Card user exited', 'price': price}), 200
            else:
                return jsonify({'message': 'No active ride found for this card'}), 404
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    # 7. Current Boarders
    @app.route('/search_passenger/<passenger_id>', methods=['GET'])
    def search_passenger(passenger_id):
        try:
            # Query for the passenger's boarding information
            board_info = db.session.query(UnexitedRidePassenger).filter(
                UnexitedRidePassenger.user_id == passenger_id
            ).all()
            board_info = [{'user_id': b.user_id, 'start_station': b.start_station, 'start_time': b.start_time} for b in
                          board_info]
            return jsonify(board_info), 200
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    @app.route('/search_card/<card_id>', methods=['GET'])
    def search_card(card_id):
        try:
            # Query for the card's boarding information
            board_info = db.session.query(UnexitedRideCard).filter(
                UnexitedRideCard.user_id == card_id
            ).all()
            board_info = [{'user_id': b.user_id, 'start_station': b.start_station, 'start_time': b.start_time} for b in
                          board_info]
            return jsonify(board_info), 200
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

        # 8. Records search

    @app.route('/search_records', methods=['POST'])
    def search_records():
        # Get query parameters
        data = request.json
        station = data.get('station')
        passenger = data.get('passenger')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        # Start with all records
        try:
            query = db.session.query(RidePassenger)

            # Filter by station if provided
            if station:
                query = query.filter(RidePassenger.start_station == station)

            # Filter by passenger if provided
            if passenger:
                query = query.filter(RidePassenger.user_id == passenger)

            # Filter by time range if provided
            if start_time and end_time:
                query = query.filter(RidePassenger.start_time >= start_time, RidePassenger.end_time <= end_time)

            # Execute the query and fetch all results
            records = query.all()

            # Convert records to JSON
            records_json = [{'user_id': r.user_id, 'start_station': r.start_station, 'start_time': r.start_time,
                             'end_station': r.end_station, 'end_time': r.end_time, 'price': r.price} for r in records]
            return jsonify(records_json), 200
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    @app.route('/search_bus/<string:station_name>', methods=['GET'])
    def search_bus(station_name):
        # Start with all records
        try:
            query = db.session.query(Bus)

            # Filter by station if provided
            if station_name:
                station_id = db.session.query(Station.station_id).filter(Station.english_name == station_name).first()[0]
                query = query.filter(Bus.station_id == station_id)

            # Execute the query and fetch all results
            buses = query.all()

            # Convert records to JSON
            buses_json = [
                {'bus_id': b.bus_id, 'station_id': b.station_id, 'bus_name': b.bus_name, 'bus_info': b.bus_info,
                 'chukou': b.chukou} for b in buses]

            return jsonify(buses_json), 200
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    @app.route('/search_out/<string:station_name>', methods=['GET'])
    def search_out(station_name):
        # Start with all records
        try:
            query = db.session.query(Out)

            # Filter by station if provided
            if station_name:
                station_id = db.session.query(Station.station_id).filter(Station.english_name == station_name).first()[0]
                query = query.filter(Out.station_id == station_id)

            # Execute the query and fetch all results
            outs = query.all()

            # Convert records to JSON
            outs_json = [{'out_id': o.out_id, 'station_id': o.station_id, 'outt': o.outt, 'textt': o.textt} for o in
                         outs]

            return jsonify(outs_json), 200
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400

    @app.route('/search_route', methods=['GET'])
    def search_route():
        # Get query parameters
        try:
            start_station = request.args.get('start_station')
            end_station = request.args.get('end_station')

            # Call get_route method with the provided start and end stations
            route = get_route(start_station, end_station)

            # Check if a route was found
            if route is None:
                return jsonify({'message': 'No route found between the provided stations'}), 404

            # Convert the route to JSON and return
            return jsonify({'route': route}), 200
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error occurred', 'error': str(e)}), 400


if __name__ == '__main__':
    app = create_app()
    app.run()
