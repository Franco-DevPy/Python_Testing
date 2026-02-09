import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions
    

# Limit 12 places per club
def get_club_booking(competition, club_id):
    for booking in competition.get("bookings", []):
        if booking["club_id"] == club_id:
            return booking
    return None

def get_total_booked_places(competition, club_id):
    booking = get_club_booking(competition, club_id)
    if booking:
        return booking["places"]
    return 0




MESSAGES = {
    "OK": "Great-booking complete!",
    "NOT_ENOUGH_PLACES": "Not enough places available in the competition.",
    "NOT_ENOUGH_POINTS": "You cannot book more places than you have points.",
    "TOO_MANY_PLACES": "You cannot book more than 12 places per competition.",
    "PAST_COMPETITION": "You cannot book places for past competitions.",
    "EMAIL_NOT_FOUND": "Email not found.",
    "NEGATIVE_PLACES": "You cannot book a negative number of places.",
    "TOTAL_BOOKING_LIMIT_EXCEEDED": "You cannot book more than 12 places total for this competition."

}


def validate_booking(
    placesRequired,
    club_points,
    competition_places,
    competition_date,
    club_id=None,
    competition=None
):

    if placesRequired <= 0:
        return "NEGATIVE_PLACES"

    if datetime.strptime(competition_date, "%Y-%m-%d %H:%M:%S") < datetime.now():
        return "PAST_COMPETITION"

    if placesRequired > competition_places:
        return "NOT_ENOUGH_PLACES"

    if placesRequired > club_points:
        return "NOT_ENOUGH_POINTS"

    if placesRequired > 12:
        return "TOO_MANY_PLACES"

    already_booked = 0
    if competition is not None and club_id is not None:
        already_booked = get_total_booked_places(competition, club_id)

    if already_booked + placesRequired > 12:
        return "TOTAL_BOOKING_LIMIT_EXCEEDED"

    return "OK"



    
        


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')


#7 : Implement Points Display Board
@app.route('/displayBoard',methods=['GET'])
def displayBoard():

    clubs_sorted = sorted(clubs, key=lambda x: int(x['points']), reverse=True)

    return render_template('displayBoard.html',clubs=clubs_sorted)



# BUG #1 : Unknown email crashes the app
@app.route('/showSummary',methods=['POST'])
def showSummary():

    # club = [club for club in clubs if club['email'] == request.form['email']][0]
    matching_club = None
    for club in clubs:
        if club['email'] == request.form['email']:
            matching_club = club
            break

    if not matching_club :
        flash("Email not found.")
        return redirect(url_for('index'))
    
    return render_template('welcome.html',club=matching_club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    date_now = datetime.now()
    competition_date = foundCompetition['date']
    
    # BUG #5 : Booking places in past competitions
    if datetime.strptime(competition_date, "%Y-%m-%d %H:%M:%S") < date_now:
        flash("You cannot book places for past competitions.")
        return render_template('welcome.html', club=foundClub, competitions=competitions)

    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)




@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    placesRequired = int(request.form['places'])

    competition_date = competition['date']
    points_club = int(club['points'])
    places_competition = int(competition['numberOfPlaces'])

    club_id = club['id']

    validation_result = validate_booking(
        placesRequired,
        points_club,
        places_competition,
        competition_date,
        club_id=club_id,
        competition=competition
    )

    if validation_result != "OK":
        flash(MESSAGES[validation_result])
        return render_template('welcome.html', club=club, competitions=competitions)

    # SAVE BOOKING
    booking = get_club_booking(competition, club_id)

    if booking:
        booking["places"] += placesRequired
    else:
        competition.setdefault("bookings", []).append({
            "club_id": club_id,
            "places": placesRequired
        })

    # UPDATE DATA
    club['points'] = int(club['points']) - placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired

    flash(MESSAGES["OK"])
    return render_template('welcome.html', club=club, competitions=competitions)



# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
