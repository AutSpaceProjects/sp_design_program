from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from abc import ABC, abstractmethod
from enum import Enum


# ============================================================
# CONSTANTS
# ============================================================
SIGMA = 5.670374419e-8


# ============================================================
# THRUSTER TYPES
# ============================================================
class ThrusterType(Enum):
    COLD_GAS = "Cold Gas"
    MONO_PROPELLANT = "Mono-propellant"
    BI_PROPELLANT = "Bi-propellant"


# ============================================================
# INPUT FROM OTHER MODULES
# ============================================================
@dataclass
class MissionRequirements:
    orbit_altitude_km: float
    mission_duration_years: float
    eclipse_duration_min: float
    total_delta_v_mps: float


@dataclass
class PropulsionInput:
   
    dissipated_power_W: float
    thruster_type: ThrusterType         
    thruster_efficiency: float = 0.65


# ============================================================
# PROPULSION THERMAL REQUIREMENTS
# ============================================================
@dataclass
class PropulsionThermalRequirements:
    thruster_type: ThrusterType
    operational_min_temp_C: float = 10.0
    operational_max_temp_C: float = 50.0
    survival_min_temp_C: float = 0.0
    survival_max_temp_C: float = 60.0
    max_temperature_gradient_C: float = 20.0


# ============================================================
# BASE CLASSES
# ============================================================
@dataclass
class Subsystem(ABC):
    name: str
    dissipated_power_W: float

    @abstractmethod
    def analyze(self) -> None:
        pass


# ============================================================
# THERMAL ANALYZER
# ============================================================
@dataclass
class PropulsionThermalAnalyzer:
    electrical_power_W: float
    thruster_type: ThrusterType
    thruster_efficiency: float = 0.65
    radiator_emissivity: float = 0.90
    radiator_temperature_C: float = 40.0

    def calculate_thruster_heat(self) -> float:
        return self.electrical_power_W * (1 - self.thruster_efficiency)

    def total_heat_load(self) -> float:
        return self.electrical_power_W + self.calculate_thruster_heat()

    def radiator_area(self) -> float:
        T = self.radiator_temperature_C + 273.15
        return self.total_heat_load() / (self.radiator_emissivity * SIGMA * T**4)

    def dissipated_heat_by_radiator(self, area: float) -> float:
        T = self.radiator_temperature_C + 273.15
        return self.radiator_emissivity * SIGMA * T**4 * area


# ============================================================
# PROPULSION TCS
# ============================================================
@dataclass
class PropulsionThermalControlSubsystem(Subsystem):
    requirements: PropulsionThermalRequirements
    thruster_efficiency: float = 0.65
    radiator_emissivity: float = 0.90
    estimated_cold_case_temp_C: float = 10.0

    required_radiator_area_m2: float = 0.0
    total_heat_load_W: float = 0.0
    dissipated_by_radiator_W: float = 0.0
    max_temp_gradient_C: float = 0.0

    def analyze(self) -> None:
        analyzer = PropulsionThermalAnalyzer(
            electrical_power_W=self.dissipated_power_W,
            thruster_type=self.requirements.thruster_type,
            thruster_efficiency=self.thruster_efficiency,
            radiator_emissivity=self.radiator_emissivity
        )

        self.total_heat_load_W = analyzer.total_heat_load()
        self.required_radiator_area_m2 = analyzer.radiator_area()
        self.dissipated_by_radiator_W = analyzer.dissipated_heat_by_radiator(self.required_radiator_area_m2)
        self.max_temp_gradient_C = abs(self.estimated_cold_case_temp_C - 25.0)

        print(f"[Propulsion TCS] Type: {self.requirements.thruster_type.value}")
        print(f"[Propulsion TCS] Electrical Power = {self.dissipated_power_W:.2f} W")
        print(f"[Propulsion TCS] Thruster Heat = {analyzer.calculate_thruster_heat():.2f} W")
        print(f"[Propulsion TCS] Total Heat Load = {self.total_heat_load_W:.2f} W")
        print(f"[Propulsion TCS] Required Radiator Area = {self.required_radiator_area_m2:.3f} m²")
        print(f"[Propulsion TCS] Heat Dissipated by Radiator = {self.dissipated_by_radiator_W:.2f} W")
        print(f"[Propulsion TCS] Max Temp Gradient = {self.max_temp_gradient_C:.2f} °C")


# ============================================================
# TRADE STUDY
# ============================================================
@dataclass
class ArchitectureCandidate:
    name: str
    mass_score: float
    power_score: float
    reliability_score: float
    complexity_score: float


@dataclass
class TradeStudy:
    candidates: List[ArchitectureCandidate]

    def evaluate(self) -> ArchitectureCandidate:
        weights = {"mass": 0.25, "power": 0.25, "reliability": 0.30, "complexity": 0.20}
        best = max(self.candidates, key=lambda c: 
            c.mass_score*weights["mass"] + c.power_score*weights["power"] +
            c.reliability_score*weights["reliability"] + c.complexity_score*weights["complexity"])
        for c in self.candidates:
            score = (c.mass_score*weights["mass"] + c.power_score*weights["power"] +
                     c.reliability_score*weights["reliability"] + c.complexity_score*weights["complexity"])
            print(f"{c.name} Score = {score:.3f}")
        return best


# ============================================================
# VERIFICATION
# ============================================================
@dataclass
class VerificationModule:
    tcs: PropulsionThermalControlSubsystem

    def verify(self) -> bool:
        ok = self.tcs.max_temp_gradient_C <= self.tcs.requirements.max_temperature_gradient_C
        print("[Propulsion TCS Verification] PASS" if ok else "[Propulsion TCS Verification] FAIL")
        return ok


# ============================================================
# THRUSTER SELECTION
# ============================================================
def select_thruster_type(mission: MissionRequirements) -> ThrusterType:
    if mission.total_delta_v_mps > 1500:
        return ThrusterType.BI_PROPELLANT
    elif mission.total_delta_v_mps > 400:
        return ThrusterType.MONO_PROPELLANT
    else:
        return ThrusterType.COLD_GAS


# ============================================================
# MAIN PUBLIC FUNCTION
# ============================================================
def run_propulsion_thermal_control(
    mission: MissionRequirements,
    propulsion_input: PropulsionInput,
    candidates: List[ArchitectureCandidate]
) -> None:
    thermal_req = PropulsionThermalRequirements(thruster_type=propulsion_input.thruster_type)

    thermal = PropulsionThermalControlSubsystem(
        name="Propulsion_TCS",
        dissipated_power_W=propulsion_input.dissipated_power_W,
        requirements=thermal_req,
        thruster_efficiency=propulsion_input.thruster_efficiency
    )

    print("\n===== Propulsion Thermal Control Analysis =====\n")
    thermal.analyze()

    print("\n===== Trade Study =====\n")
    study = TradeStudy(candidates=candidates)
    best = study.evaluate()
    print(f"\nSelected Architecture = {best.name}")

    print("\n===== Verification =====\n")
    VerificationModule(tcs=thermal).verify()

    print("\nPropulsion TCS Analysis completed successfully!")

