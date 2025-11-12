"""
Beispiel: Programmgesteuerte Verwendung von CHAOS--NEXUS
=========================================================

Zeigt, wie man den Chaos-Kernel in eigenen Anwendungen nutzt.
"""

from chaos_kernel import ChaosKernel, activate_genesis
import json


def example_basic_usage():
    """Basis-Beispiel für den Genesis-Modus."""
    print("=== Basis-Verwendung ===\n")
    
    # Methode 1: Convenience-Funktion
    kernel = activate_genesis()
    print(f"Genesis aktiviert: {kernel.genesis_mode}")
    
    # Verarbeite einen Zyklus
    result = kernel.process_chaos_cycle({
        "amplitude": 1.0,
        "frequency": 440.0,
        "message": "Hello Chaos"
    })
    
    print(f"Status: {result['status']}")
    print(f"Proof: {result['proof'][:16]}...\n")


def example_custom_instability():
    """Beispiel mit benutzerdefinierter Instabilität."""
    print("=== Benutzerdefinierte Instabilität ===\n")
    
    from chaos_kernel import InstabilityReflector
    
    # Erstelle Kernel mit höherer Instabilität
    kernel = ChaosKernel()
    kernel.reflector = InstabilityReflector(base_instability=0.8)
    kernel.activate_genesis_mode()
    
    # Verarbeite mehrere Zyklen
    successes = 0
    failures = 0
    
    for i in range(20):
        result = kernel.process_chaos_cycle({
            "iteration": i,
            "value": i * 2.5
        })
        
        if result['status'] == 'success':
            successes += 1
        else:
            failures += 1
    
    print(f"Erfolge: {successes}")
    print(f"Ausfälle: {failures}")
    print(f"Instabilität: {kernel.reflector.base_instability}\n")


def example_state_analysis():
    """Beispiel für Zustandsanalyse."""
    print("=== Zustandsanalyse ===\n")
    
    kernel = activate_genesis()
    
    # Generiere viele Zustände
    for i in range(30):
        kernel.process_chaos_cycle({
            "index": i,
            "energy": 100 + i * 5,
            "phase": f"wave_{i}"
        })
    
    # Analysiere Metriken
    metrics = kernel.get_system_metrics()
    
    print(f"Gesamtzustände: {metrics['total_states']}")
    print(f"Zustandsausfälle: {metrics['state_failures']}")
    print(f"Ausfallrate: {metrics['state_failures'] / (metrics['total_states'] + metrics['state_failures']) * 100:.1f}%")
    print(f"Invers-Proofs: {metrics['inverse_proofs']}")
    print(f"Harmonische Muster: {metrics['harmonic_patterns_generated']}\n")


def example_failure_export():
    """Beispiel für Ausfall-Export."""
    print("=== Ausfall-Export ===\n")
    
    kernel = activate_genesis()
    
    # Erzeuge viele Zyklen um Ausfälle zu sammeln
    for i in range(50):
        kernel.process_chaos_cycle({
            "id": i,
            "data": f"test_data_{i}"
        })
    
    # Exportiere Ausfälle
    failures = kernel.export_state_failures()
    
    if failures:
        print(f"Exportierte {len(failures)} Ausfälle:")
        
        # Speichere in JSON
        with open('/tmp/chaos_failures.json', 'w') as f:
            json.dump(failures, f, indent=2)
        
        print(f"Gespeichert in: /tmp/chaos_failures.json")
        
        # Zeige ersten Ausfall
        if len(failures) > 0:
            print("\nErster Ausfall:")
            print(f"  Timestamp: {failures[0]['timestamp']}")
            print(f"  Instabilität: {failures[0]['instability_level']:.4f}")
    else:
        print("Keine Ausfälle aufgetreten")
    
    print()


def example_harmonic_patterns():
    """Beispiel für harmonische Muster."""
    print("=== Harmonische Muster ===\n")
    
    kernel = activate_genesis()
    
    patterns = []
    
    # Generiere Muster
    for i in range(10):
        result = kernel.process_chaos_cycle({
            "frequency": 440.0 + i * 10,
            "amplitude": 1.0
        })
        
        if 'harmonic_pattern' in result:
            patterns.append(result['harmonic_pattern'])
    
    # Zeige Muster
    print("Generierte harmonische Muster:")
    for i, pattern in enumerate(patterns):
        print(f"  {i+1}: {pattern[:30]}...")
    
    print()


def example_parameter_recombination():
    """Beispiel für Parameterrekombination."""
    print("=== Parameterrekombination ===\n")
    
    from chaos_kernel import InstabilityReflector
    
    reflector = InstabilityReflector(base_instability=0.6)
    
    original_params = {
        "temperature": 273.15,
        "pressure": 101.325,
        "volume": 22.4,
        "label": "IDEAL_GAS"
    }
    
    print("Original:")
    for key, val in original_params.items():
        print(f"  {key}: {val}")
    
    print("\nRekombiniert:")
    for iteration in range(3):
        recombined = reflector.recombine_parameters(original_params.copy())
        print(f"\n  Iteration {iteration + 1}:")
        for key, val in recombined.items():
            print(f"    {key}: {val}")


def main():
    """Hauptfunktion - führt alle Beispiele aus."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         CHAOS--NEXUS Programmier-Beispiele                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    example_basic_usage()
    example_custom_instability()
    example_state_analysis()
    example_failure_export()
    example_harmonic_patterns()
    example_parameter_recombination()
    
    print("=== Alle Beispiele abgeschlossen ===")


if __name__ == "__main__":
    main()
