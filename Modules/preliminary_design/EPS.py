# ==============================================================
# Electric Power Subsystem (EPS) - Propulsion Power Budget
# Phase 2 
# ==============================================================

import json

g0 = 9.80665  


# ==============================================================
# Base class: Electric Power
# ==============================================================
class ElectricPower:
    def __init__(self, data):
        # Read all inputs from the JSON dictionary
        self.data = data

    # Relations  

    def power_electronics(self):
        # P_electronics = N_control * P_unit
        return self.data["N_control"] * self.data["P_unit"]

    def power_sensors(self):
        # P_sensors = N_sensor * P_sensor
        return self.data["N_sensor"] * self.data["P_sensor"]

    def power_valves(self):
        # P_valves = N_valve * P_valve * duty_cycle
        return self.data["N_valve"] * self.data["P_valve"] * self.data["duty_cycle"]

    def power_heater(self):
        # P_heater = UA * (T_prop - T_spacecraft)
        return self.data["UA"] * (self.data["T_prop"] - self.data["T_spacecraft"])

    #   Total power 

    def total_power(self):
        # Sum of loads
        return (self.power_electronics()
                + self.power_sensors()
                + self.power_valves()
                + self.power_heater())

    def power_with_margin(self):
        # Add the ECSS margin: P_design = P_total * (1 + margin)
        return self.total_power() * (1 + self.data["margin"])

    # Output section (build a dictionary and save it as JSON) 

    def to_dict(self):
        # Build a dictionary of results 
        return {
            "propulsion_type": self.data["propulsion_type"],
            "P_electronics": round(self.power_electronics(), 3),
            "P_sensors": round(self.power_sensors(), 3),
            "P_valves": round(self.power_valves(), 3),
            "P_heater": round(self.power_heater(), 3)
        }

    def save_json(self, filename="output.json"):
        # Save the results dictionary into a JSON file
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        print("Output saved to:", filename)

    def show(self):
        # Print report on Console
        print("Propulsion type       :", self.data["propulsion_type"])
        print("P_electronics         :", round(self.power_electronics(), 3), "W")
        print("P_sensors             :", round(self.power_sensors(), 3), "W")
        print("P_valves              :", round(self.power_valves(), 3), "W")
        print("P_heater              :", round(self.power_heater(), 3), "W")
        


# ==============================================================
# sub_class 1: Chemical Propulsion
# ==============================================================
class ChemicalPropulsion(ElectricPower):

    def catalyst_bed_heater(self):
        # Extra relation only for chemical engines
        return self.data["P_catalyst_bed_heater"]

    def total_power(self):
        # Common loads + catalyst bed heater
        return super().total_power() + self.catalyst_bed_heater()

    def to_dict(self):
        result = super().to_dict()
        result["P_catalyst_bed_heater"] = round(self.catalyst_bed_heater(), 3)
        result["P_total"]= round(self.total_power(), 3)
        result["P_with_margin"]= round(self.power_with_margin(), 3)
        return result
    def show(self):
        super().show()
        print("P_catalyst_bed_heater :", round(self.catalyst_bed_heater(), 3), "W")
        print("P_total               :", round(self.total_power(), 3), "W")
        print("P_with_margin         :", round(self.power_with_margin(), 3), "W")

# ==============================================================
# sub_class 2: Liquid Propulsion (pump-fed)
# ==============================================================
class LiquidPropulsion(ElectricPower):

    def pump_head(self):
        # H_p = delta_p / (g0 * rho)
        return self.data["delta_p"] / (g0 * self.data["rho"])

    def pump_power(self):
        # P_pump = g0 * m_dot * H_p / eta_pump
        return g0 * self.data["m_dot"] * self.pump_head() / self.data["eta_pump"]

    def total_power(self):
        # Common loads + pump power
        return super().total_power() + self.pump_power()

    def to_dict(self):
        result = super().to_dict()
        result["P_pump"] = round(self.pump_power(), 3)
        result["P_total"]= round(self.total_power(), 3)
        result["P_with_margin"]= round(self.power_with_margin(), 3)
        return result
    def show(self):
        super().show()
        print("P_pump                :", round(self.pump_power(), 3), "W")
        print("P_total               :", round(self.total_power(), 3), "W")
        print("P_with_margin         :", round(self.power_with_margin(), 3), "W")
        

# ==============================================================
# Main program's Function
# ==============================================================
def main():
    # 1) Read the JSON input file
    with open("input.json", "r") as f:
        data = json.load(f)

    # 2) Choose the class based on propulsion type
    if data["propulsion_type"] == "chemical":
        engine = ChemicalPropulsion(data)
    else:
        engine = LiquidPropulsion(data)

    # 3) Print the result
    engine.show()

    # 4) Save the result to a JSON output file
    engine.save_json("Required_Power.json")


main()
