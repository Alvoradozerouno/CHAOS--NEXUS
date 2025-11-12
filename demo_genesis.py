#!/usr/bin/env python3
"""
Demo-Skript für CHAOS--NEXUS Genesis Mode
==========================================

Demonstriert die Funktionalität des Chaos-Kernels mit:
- Genesis-Modus-Aktivierung
- Dynamische Parameterrekombination
- Zustandsausfälle und deren Speicherung
- Invers-Proof-Generierung
"""

import time
from chaos_kernel import ChaosKernel, activate_genesis


def print_separator(title: str = ""):
    """Druckt einen Trennstrich mit optionalem Titel."""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print('='*60)
    else:
        print('-'*60)


def demo_genesis_activation():
    """Demonstriert die Genesis-Modus-Aktivierung."""
    print_separator("GENESIS-MODUS AKTIVIERUNG")
    
    kernel = ChaosKernel()
    result = kernel.activate_genesis_mode()
    
    print(f"Status: {result['status']}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"Proof Hash: {result['proof_hash'][:16]}...")
    print(f"\nInitialer Systemzustand:")
    print(f"  Instabilität: {result['initial_state']['instability_level']:.4f}")
    print(f"  Harmonische Signatur: {result['initial_state']['harmonic_signature'][:20]}...")
    
    return kernel


def demo_chaos_cycles(kernel: ChaosKernel, cycles: int = 10):
    """Demonstriert mehrere Chaos-Zyklen."""
    print_separator("CHAOS-ZYKLEN VERARBEITUNG")
    
    failures = 0
    successes = 0
    
    for i in range(cycles):
        # Erstelle Testparameter
        params = {
            "energy": 100.0 + i * 10,
            "frequency": 440.0 + i * 5,
            "phase": f"cycle_{i}",
            "amplitude": 1.0
        }
        
        result = kernel.process_chaos_cycle(params)
        
        if result['status'] == 'state_failure':
            failures += 1
            print(f"Zyklus {i+1}: ✗ AUSFALL - Gespeichert")
        else:
            successes += 1
            print(f"Zyklus {i+1}: ✓ Erfolg - Pattern: {result['harmonic_pattern'][:10]}...")
    
    print(f"\nZusammenfassung:")
    print(f"  Erfolge: {successes}")
    print(f"  Ausfälle: {failures}")


def demo_instability_reflection(kernel: ChaosKernel):
    """Demonstriert den Instabilitäts-Reflektor."""
    print_separator("INSTABILITÄTS-REFLEKTOR")
    
    test_params = {
        "value1": 100.0,
        "value2": 50.0,
        "text": "CHAOS_PATTERN",
        "constant": 42
    }
    
    print(f"Original-Parameter:")
    for key, val in test_params.items():
        print(f"  {key}: {val}")
    
    print(f"\nRekombinierte Parameter (3 Iterationen):")
    for i in range(3):
        recombined = kernel.reflector.recombine_parameters(test_params.copy())
        print(f"\n  Iteration {i+1}:")
        for key, val in recombined.items():
            print(f"    {key}: {val}")
        time.sleep(0.1)  # Kleine Pause für Zeit-basierte Variation


def demo_system_metrics(kernel: ChaosKernel):
    """Zeigt Systemmetriken an."""
    print_separator("SYSTEM-METRIKEN")
    
    metrics = kernel.get_system_metrics()
    
    print(f"Genesis Aktiv: {metrics['genesis_active']}")
    print(f"Uptime: {metrics['uptime']:.2f} Sekunden")
    print(f"Gesamtzustände: {metrics['total_states']}")
    print(f"Zustandsausfälle: {metrics['state_failures']}")
    print(f"Invers-Proofs: {metrics['inverse_proofs']}")
    print(f"Aktuelle Instabilität: {metrics['current_instability']:.4f}")
    print(f"Harmonische Muster: {metrics['harmonic_patterns_generated']}")


def demo_proof_verification(kernel: ChaosKernel):
    """Demonstriert Proof-Verifikation."""
    print_separator("INVERS-PROOF VERIFIKATION")
    
    if len(kernel.inverse_proofs) > 0 and len(kernel.active_states) > 0:
        # Teste erste Proofs
        for i in range(min(3, len(kernel.inverse_proofs))):
            if i < len(kernel.active_states):
                is_valid = kernel.verify_proof(i, i)
                status = "✓ GÜLTIG" if is_valid else "✗ UNGÜLTIG"
                print(f"Proof {i}: {status}")
                
                proof = kernel.inverse_proofs[i]
                print(f"  Original: {proof.original_hash[:16]}...")
                print(f"  Inverse:  {proof.inverse_hash[:16]}...")
    else:
        print("Keine Proofs zum Verifizieren verfügbar")


def demo_state_failures_export(kernel: ChaosKernel):
    """Exportiert und zeigt Zustandsausfälle."""
    print_separator("ZUSTANDSAUSFÄLLE EXPORT")
    
    failures = kernel.export_state_failures()
    
    if failures:
        print(f"Exportierte {len(failures)} Zustandsausfälle:")
        for i, failure in enumerate(failures[:3]):  # Zeige nur erste 3
            print(f"\n  Ausfall {i+1}:")
            print(f"    Timestamp: {failure['timestamp']}")
            print(f"    Instabilität: {failure['instability_level']:.4f}")
            print(f"    Proof: {failure['proof_hash'][:16]}...")
    else:
        print("Keine Zustandsausfälle aufgetreten")


def main():
    """Haupt-Demo-Funktion."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              CHAOS--NEXUS GENESIS MODE                    ║
    ║          Adaptive Chaos Network Demonstration             ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Genesis-Modus aktivieren
    kernel = demo_genesis_activation()
    time.sleep(0.5)
    
    # Instabilitäts-Reflektor demonstrieren
    demo_instability_reflection(kernel)
    time.sleep(0.5)
    
    # Chaos-Zyklen durchführen
    demo_chaos_cycles(kernel, cycles=15)
    time.sleep(0.5)
    
    # System-Metriken anzeigen
    demo_system_metrics(kernel)
    time.sleep(0.5)
    
    # Proof-Verifikation
    demo_proof_verification(kernel)
    time.sleep(0.5)
    
    # Zustandsausfälle exportieren
    demo_state_failures_export(kernel)
    
    print_separator("DEMO ABGESCHLOSSEN")
    print("\nDas Chaos-Netzwerk ist aktiv und adaptiv!")
    print("Genesis-Modus erfolgreich demonstriert.\n")


if __name__ == "__main__":
    main()
