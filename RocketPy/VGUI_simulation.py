import tkinter as tk
from tkinter import messagebox
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from rocketpy import Function, Rocket, SolidMotor, Flight, Environment
import webbrowser

def open_in_google_earth(file_path):
    google_earth_url = f'https://earth.google.com/web/@?earthdata={file_path}'
    webbrowser.open_new(google_earth_url)

def run_simulation():
    try:
        # Create Environment
        env = Environment(
            latitude=45.039435,
            longitude=10.238164,
            elevation=5,
        ) 

        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        env.set_date(
            (tomorrow.year, tomorrow.month, tomorrow.day, 10), timezone="Europe/Rome"
        )

        env.set_atmospheric_model(type='Forecast', file='GFS')

        # Create Engine
        Laika_Engine = SolidMotor(
            thrust_source="G80.eng",
            dry_mass=0.032,
            dry_inertia=(0.000029, 0.000029, 0.000007),
            center_of_dry_mass_position=0.05,
            grains_center_of_mass_position=0.06,
            burn_time=1.2,
            grain_number=1,
            grain_separation=0,
            grain_density=1900,
            grain_outer_radius=0.0145,
            grain_initial_inner_radius=0.0005,
            grain_initial_height=0.10,
            nozzle_radius=0.000635,
            throat_radius=0.00038,
            interpolation_method="linear",
            nozzle_position=0,
            coordinate_system_orientation="nozzle_to_combustion_chamber",
        )

        # Create Rocket
        Pioneer = Rocket(
            radius=0.0305,
            mass=0.627,
            inertia=(5.321, 5.321, 0.034),
            power_off_drag="powerOffDragCurveG80.csv",
            power_on_drag="powerOnDragCurveG80.csv",
            center_of_mass_without_motor=0,
            coordinate_system_orientation="tail_to_nose",
        )

        buttons = Pioneer.set_rail_buttons(
            upper_button_position=0.10,
            lower_button_position=-0.20,
            angular_position=45,
        )

        Pioneer.add_motor(Laika_Engine, position=-0.42)

        nose = Pioneer.add_nose(
            length=0.14, kind="vonKarman", position=0.54 
        )

        fins = Pioneer.add_trapezoidal_fins(
            n=4,
            root_chord=0.120,
            tip_chord=0.050,
            span=0.04,
            sweep_length=0.06,
            cant_angle=56.3,
            position=0,
        )

        tail = Pioneer.add_tail(
            top_radius=0.061, bottom_radius=0.04, length=0.02, position=-0.02
        )

        main = Pioneer.add_parachute(
            name="main",
            cd_s=10.0,
            trigger=100,
            sampling_rate=105,
            lag=1.5,
            noise=(0, 8.3, 0.5),
        )

        drogue = Pioneer.add_parachute(
            name="drogue",
            cd_s=1.0,
            trigger="apogee",
            sampling_rate=105,
            lag=1.5,
            noise=(0, 8.3, 0.5),
        )

        # Create Flight
        test_flight = Flight(
            rocket=Pioneer, environment=env, rail_length=2, inclination=90, heading=0
        )

        # Plot and display altitude profile
        fig, ax = plt.subplots()
        test_flight.altitude_profile()
        ax.set_title('Altitude Profile')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Altitude (m)')
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=3, column=0, columnspan=2)

        # Export KML
        test_flight.export_kml(file_name="test_flight.kml")
        open_in_google_earth('test_flight.kml')
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create GUI
window = tk.Tk()
window.title("Rocket Simulation")
window.geometry("600x400")
window.configure(bg="#34495E")

# Add GUI elements
label = tk.Label(window, text="Rocket Simulation", font=("Helvetica", 18), bg="#34495E", fg="white")
label.grid(row=0, column=0, columnspan=2, pady=10)

button = tk.Button(window, text="Run Simulation", command=run_simulation, bg="#3498DB", fg="white")
button.grid(row=1, column=0, pady=10)

exit_button = tk.Button(window, text="Exit", command=window.quit, bg="#E74C3C", fg="white")
exit_button.grid(row=1, column=1, pady=10)

# Run GUI
window.mainloop()
