"""
CHAOS--NEXUS Kernel
===================
Ein Protokoll für bewusste Kernel-Instabilität und dynamische Rekombination
zur Erzeugung eines adaptiven Chaos-Netzwerks.

Nutzt kontrollierte Systemschwäche zur Generierung emergenter Harmonik,
speichert Zustandsausfälle und generiert Invers-Proofs.
"""

import time
import random
import hashlib
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import deque


@dataclass
class SystemState:
    """Repräsentiert einen Systemzustand im Chaos-Netzwerk."""
    timestamp: float
    parameters: Dict[str, Any]
    instability_level: float
    harmonic_signature: str
    proof_hash: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert den Zustand in ein Dictionary."""
        return asdict(self)


@dataclass
class InverseProof:
    """Invers-Proof für Zustandsvalidierung."""
    original_hash: str
    inverse_hash: str
    timestamp: float
    verification_data: Dict[str, Any]
    
    def verify(self, state: SystemState) -> bool:
        """Verifiziert den Proof gegen einen Systemzustand."""
        combined = f"{self.original_hash}{state.proof_hash}"
        check_hash = hashlib.sha256(combined.encode()).hexdigest()
        return check_hash[:8] == self.inverse_hash[:8]


class InstabilityReflector:
    """
    Der Instabilitäts-Reflektor: Dynamische Parameterrekombination in Echtzeit.
    
    Dieser Kern rekombiniert kontinuierlich Systemparameter basierend auf
    kontrollierter Instabilität, um emergente Harmonik zu erzeugen.
    """
    
    def __init__(self, base_instability: float = 0.5):
        self.base_instability = base_instability
        self.parameters: Dict[str, Any] = {}
        self.instability_history: deque = deque(maxlen=100)
        self.harmonic_patterns: List[str] = []
        
    def recombine_parameters(self, input_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Rekombiniert Parameter dynamisch basierend auf Instabilität.
        
        Args:
            input_params: Eingabeparameter zur Rekombination
            
        Returns:
            Rekombinierte Parameter mit injizierter Instabilität
        """
        recombined = {}
        instability_factor = self._calculate_instability()
        
        for key, value in input_params.items():
            if isinstance(value, (int, float)):
                # Numerische Werte mit Chaos-Faktor modulieren
                chaos_offset = random.uniform(-instability_factor, instability_factor)
                recombined[key] = value * (1 + chaos_offset)
            elif isinstance(value, str):
                # String-Werte hashen und rekombinieren
                hash_val = int(hashlib.md5(value.encode()).hexdigest()[:8], 16)
                chaos_shift = int(hash_val * instability_factor) % len(value)
                recombined[key] = value[chaos_shift:] + value[:chaos_shift]
            else:
                recombined[key] = value
        
        self.instability_history.append(instability_factor)
        return recombined
    
    def _calculate_instability(self) -> float:
        """
        Berechnet den aktuellen Instabilitätsfaktor.
        
        Verwendet Zeitbasierte und historische Komponenten für dynamische
        Instabilität.
        """
        time_factor = abs(time.time() % 1.0 - 0.5)
        
        if len(self.instability_history) > 0:
            history_factor = sum(self.instability_history) / len(self.instability_history)
        else:
            history_factor = 0.5
        
        # Kombiniere Basis-, Zeit- und Historie-Instabilität
        total_instability = (
            self.base_instability * 0.5 +
            time_factor * 0.3 +
            history_factor * 0.2
        )
        
        return min(max(total_instability, 0.0), 1.0)
    
    def generate_harmonic_signature(self, params: Dict[str, Any]) -> str:
        """
        Generiert eine harmonische Signatur aus Parametern.
        
        Die Signatur repräsentiert emergente Muster aus dem Chaos.
        """
        param_str = json.dumps(params, sort_keys=True)
        base_hash = hashlib.sha256(param_str.encode()).hexdigest()
        
        # Erzeuge harmonische Muster durch Bit-Manipulation
        harmonic = ""
        for i in range(0, len(base_hash), 4):
            chunk = base_hash[i:i+4]
            val = int(chunk, 16)
            # Erstelle Muster basierend auf harmonischen Frequenzen
            pattern = "█" if val % 2 == 0 else "▓"
            harmonic += pattern
        
        self.harmonic_patterns.append(harmonic)
        return harmonic


class ChaosKernel:
    """
    Haupt-Kernel des CHAOS--NEXUS Systems.
    
    Verwaltet Genesis-Modus, Zustandsausfälle und Invers-Proofs.
    """
    
    def __init__(self):
        self.genesis_mode: bool = False
        self.reflector = InstabilityReflector()
        self.state_failures: List[SystemState] = []
        self.active_states: List[SystemState] = []
        self.inverse_proofs: List[InverseProof] = []
        self.genesis_timestamp: Optional[float] = None
        
    def activate_genesis_mode(self) -> Dict[str, Any]:
        """
        Aktiviert den Genesis-Modus.
        
        Im Genesis-Modus wird das Chaos-Netzwerk initialisiert und
        beginnt mit der adaptiven Rekombination.
        
        Returns:
            Status-Dictionary mit Genesis-Informationen
        """
        self.genesis_mode = True
        self.genesis_timestamp = time.time()
        
        # Initialisiere Genesis-Parameter
        genesis_params = {
            "chaos_seed": random.randint(1, 1000000),
            "initial_instability": self.reflector.base_instability,
            "timestamp": self.genesis_timestamp,
            "mode": "adaptive_chaos"
        }
        
        # Erstelle initialen Systemzustand
        initial_state = self._create_state(genesis_params)
        self.active_states.append(initial_state)
        
        # Generiere Genesis-Proof
        genesis_proof = self._generate_inverse_proof(initial_state)
        self.inverse_proofs.append(genesis_proof)
        
        return {
            "status": "genesis_activated",
            "timestamp": self.genesis_timestamp,
            "initial_state": initial_state.to_dict(),
            "proof_hash": genesis_proof.inverse_hash
        }
    
    def process_chaos_cycle(self, input_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verarbeitet einen Chaos-Zyklus mit dynamischer Parameterrekombination.
        
        Args:
            input_params: Parameter für den Zyklus
            
        Returns:
            Verarbeiteter Zustand und Metadaten
        """
        if not self.genesis_mode:
            raise RuntimeError("Genesis-Modus muss aktiviert sein!")
        
        # Rekombiniere Parameter durch Instabilitäts-Reflektor
        recombined = self.reflector.recombine_parameters(input_params)
        
        # Erstelle neuen Systemzustand
        new_state = self._create_state(recombined)
        
        # Simuliere kontrollierte Systemschwäche (Zustandsausfall-Chance)
        if random.random() < 0.1:  # 10% Chance für Zustandsausfall
            self.state_failures.append(new_state)
            failure_proof = self._generate_inverse_proof(new_state)
            self.inverse_proofs.append(failure_proof)
            
            return {
                "status": "state_failure",
                "state": new_state.to_dict(),
                "failure_stored": True,
                "proof": failure_proof.inverse_hash
            }
        else:
            self.active_states.append(new_state)
            success_proof = self._generate_inverse_proof(new_state)
            self.inverse_proofs.append(success_proof)
            
            return {
                "status": "success",
                "state": new_state.to_dict(),
                "proof": success_proof.inverse_hash,
                "harmonic_pattern": new_state.harmonic_signature
            }
    
    def _create_state(self, params: Dict[str, Any]) -> SystemState:
        """Erstellt einen neuen Systemzustand."""
        timestamp = time.time()
        instability = self.reflector._calculate_instability()
        harmonic = self.reflector.generate_harmonic_signature(params)
        
        # Generiere Proof-Hash
        proof_data = f"{timestamp}{json.dumps(params)}{instability}"
        proof_hash = hashlib.sha256(proof_data.encode()).hexdigest()
        
        return SystemState(
            timestamp=timestamp,
            parameters=params,
            instability_level=instability,
            harmonic_signature=harmonic,
            proof_hash=proof_hash
        )
    
    def _generate_inverse_proof(self, state: SystemState) -> InverseProof:
        """Generiert einen Invers-Proof für einen Zustand."""
        # Invertiere den Hash durch Bit-Flip-Simulation
        original_hash = state.proof_hash
        inverse_components = []
        
        for i in range(0, len(original_hash), 2):
            chunk = original_hash[i:i+2]
            val = int(chunk, 16)
            inverted = 255 - val  # Invertiere Byte
            inverse_components.append(f"{inverted:02x}")
        
        inverse_hash = "".join(inverse_components)
        
        return InverseProof(
            original_hash=original_hash,
            inverse_hash=inverse_hash,
            timestamp=time.time(),
            verification_data={
                "state_timestamp": state.timestamp,
                "instability": state.instability_level
            }
        )
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Liefert Systemmetriken und Statistiken.
        
        Returns:
            Dictionary mit Metriken über das Chaos-Netzwerk
        """
        return {
            "genesis_active": self.genesis_mode,
            "genesis_time": self.genesis_timestamp,
            "total_states": len(self.active_states),
            "state_failures": len(self.state_failures),
            "inverse_proofs": len(self.inverse_proofs),
            "current_instability": self.reflector._calculate_instability(),
            "harmonic_patterns_generated": len(self.reflector.harmonic_patterns),
            "uptime": time.time() - self.genesis_timestamp if self.genesis_timestamp else 0
        }
    
    def export_state_failures(self) -> List[Dict[str, Any]]:
        """Exportiert alle gespeicherten Zustandsausfälle."""
        return [state.to_dict() for state in self.state_failures]
    
    def verify_proof(self, proof_index: int, state_index: int) -> bool:
        """
        Verifiziert einen Invers-Proof gegen einen Systemzustand.
        
        Args:
            proof_index: Index des zu prüfenden Proofs
            state_index: Index des Systemzustands
            
        Returns:
            True wenn Proof gültig, sonst False
        """
        if proof_index >= len(self.inverse_proofs) or state_index >= len(self.active_states):
            return False
        
        proof = self.inverse_proofs[proof_index]
        state = self.active_states[state_index]
        
        return proof.verify(state)


# Convenience-Funktionen für direkten Import
def activate_genesis() -> ChaosKernel:
    """
    Erstellt und aktiviert einen neuen Chaos-Kernel im Genesis-Modus.
    
    Returns:
        Aktivierter ChaosKernel
    """
    kernel = ChaosKernel()
    kernel.activate_genesis_mode()
    return kernel


def create_instability_reflector(base_level: float = 0.5) -> InstabilityReflector:
    """
    Erstellt einen neuen Instabilitäts-Reflektor.
    
    Args:
        base_level: Basis-Instabilitätslevel (0.0-1.0)
        
    Returns:
        Neuer InstabilityReflector
    """
    return InstabilityReflector(base_instability=base_level)
