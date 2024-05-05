from rocketpy import  Function, Rocket, SolidMotor, Flight, Environment
import datetime


#per vedere le timezone import pytz and run print(pytz.all_timezones)
#import pytz
#print(pytz.all_timezones)

#45.039435, 10.238164
#CAMPI SOTTO MOTTA BALUFFI

#45.16841774,9.95791172
#CASANOVA DEL MORBASCO

#45.13352988,10.02485188
#piazza del duomo CR

#44.52473339,11.62797942
#bologna

env = Environment(
    latitude=45.039435,
    longitude=10.238164,
    elevation=5,
) 

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

env.set_date(
  (tomorrow.year, tomorrow.month, tomorrow.day, 10), timezone="Europe/Rome"
) # Tomorrow's date in year, month, day, hour UTC format

print("Environment and timezone has been setted")

env.set_atmospheric_model(type='Forecast', file='GFS')

print("The atmosferic model has been setted")

env.info()

Laika_Engine = SolidMotor(                  #trust source con openmotor e sistemare tutti i dati del motore
    thrust_source="F64.eng",  #F64 su openrocket
    dry_mass=0.050,
    dry_inertia=(0.000063, 0.000063, 0.000007),   #va d'accordo con la densità, valori accurati per il nostro g80

    #sistema coordinate del motore
    center_of_dry_mass_position=0.05,
    grains_center_of_mass_position=0.06,

    #altre info
    burn_time=0.99,
    grain_number=1,
    grain_separation=0,
    grain_density=1900,
    grain_outer_radius=0.011,
    grain_initial_inner_radius=0.00025,
    grain_initial_height=0.10,
    nozzle_radius=0.01016,
    throat_radius=0.00762,

    interpolation_method="linear",
    nozzle_position=0,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

#Laika_Engine.all_info()
#Laika_Engine.draw()

print("The engine has been setted")

Pioneer = Rocket(
    radius=0.0305,
    mass=0.627,  # without motor
    
    inertia=(5.14, 5.14, 0.1378455648), #Valori ottimali di MMOI
    
    power_off_drag="powerOffDragCurveG80.csv", #determinati per pioneer
    power_on_drag="powerOnDragCurveG80.csv",
    
    center_of_mass_without_motor=0,         
    coordinate_system_orientation="tail_to_nose",
)

buttons = Pioneer.set_rail_buttons(    #da aggiustare
    upper_button_position=0.10,
    lower_button_position=-0.20,
    angular_position=45,
)

Pioneer.add_motor(Laika_Engine, position=-0.42)


#HAACKDEFINITIVO DA PROGETTO
nose = Pioneer.add_nose(
    length=0.14, kind="vonKarman", position=0.54 
).draw()

#ALI DEFINITIVE DA PROGETTO
fins = Pioneer.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.050,
    span=0.04,
    sweep_length=0.06,
    cant_angle=56.3,
    position=0,
).draw()

#TAIL DEFINITIVA DA PROGETTO
tail = Pioneer.add_tail(
    top_radius=0.061, bottom_radius=0.04, length=0.02, position=-0.02
)

main = Pioneer.add_parachute(
    name="main",
    cd_s=10.0,
    trigger=100,  # ejection altitude in meters
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

drogue = Pioneer.add_parachute(
   name="drogue",
   cd_s=1.0,
   trigger="apogee",  # ejection at apogee
   sampling_rate=105,
   lag=1.5,
   noise=(0, 8.3, 0.5),
)

print("The Rocket has been assembled... wait for the complete simulation")

test_flight = Flight(
  rocket=Pioneer, environment=env, rail_length=2, inclination=90, heading=0
)

print("Test flight setted... wait for the complete simulation")

test_flight.info()
test_flight.all_info()

test_flight.export_kml(file_name="test_flight.kml")

import webbrowser

def open_in_google_earth(file_path):
    # Costruisci l'URL per Google Earth Web con il percorso del file KML
    google_earth_url = f'https://earth.google.com/web/@?earthdata={file_path}'
    
    # Apri l'URL in una nuova finestra del browser predefinito
    webbrowser.open_new(google_earth_url)

# Esempio di utilizzo
file_path = 'test_flight.kml'
open_in_google_earth(file_path)
