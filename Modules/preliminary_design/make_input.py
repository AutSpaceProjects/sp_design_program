# ==============================================================
# JSON input maker for the EPS Power code
# ==============================================================


import json

def ask_number(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("  Please enter a valid number.")


def main():
    data = {}

    # 1) Propulsion type
    print("Propulsion type options: chemical / liquid")
    ptype = input("Propulsion type: ").strip().lower()
    while ptype not in ("chemical", "liquid"):
        ptype = input("Please type 'chemical' or 'liquid': ").strip().lower()
    data["propulsion_type"] = ptype

    # 2) Common inputs (used by both types)
    print("\n--- Control electronics ---")
    data["N_control"] = ask_number("Number of control units (N_control): ")
    data["P_unit"] = ask_number("Power per control unit [W] (P_unit): ")

    print("\n--- Sensors ---")
    data["N_sensor"] = ask_number("Number of sensors (N_sensor): ")
    data["P_sensor"] = ask_number("Power per sensor [W] (P_sensor): ")

    print("\n--- Valves ---")
    data["N_valve"] = ask_number("Number of valves (N_valve): ")
    data["P_valve"] = ask_number("Power per valve [W] (P_valve): ")
    data["duty_cycle"] = ask_number("Valve duty cycle [0..1] (duty_cycle): ")

    print("\n--- Heater ---")
    data["UA"] = ask_number("Heat transfer coefficient [W/K] (UA): ")
    data["T_prop"] = ask_number("Propellant temperature [K] (T_prop): ")
    data["T_spacecraft"] = ask_number("Spacecraft temperature [K] (T_spacecraft): ")

    # 3) Extra inputs that depend on the propulsion type
    if ptype == "chemical":
        print("\n--- Chemical extra ---")
        data["P_catalyst_bed_heater"] = ask_number("Catalyst bed heater power [W]: ")
    else:
        print("\n--- Liquid (pump) extra ---")
        data["delta_p"] = ask_number("Pump pressure rise [Pa] (delta_p): ")
        data["rho"] = ask_number("Propellant density [kg/m^3] (rho): ")
        data["m_dot"] = ask_number("Mass flow rate [kg/s] (m_dot): ")
        data["eta_pump"] = ask_number("Pump efficiency [0..1] (eta_pump): ")

    # 4) Margin
    print("\n--- Margin ---")
    data["margin"] = ask_number("Power margin [e.g. 0.20 = 20%] (margin): ")

    # 5) Save the JSON file
    with open("input.json", "w") as f:
        json.dump(data, f, indent=2)

    print("\nDone! 'input.json' was created successfully.")
    print("You can now run: python eps_power_simple.py")


main()
