"""
Tests für CHAOS--NEXUS Kernel
==============================

Grundlegende Tests für die Kernfunktionalität.
"""

import unittest
from chaos_kernel import ChaosKernel, InstabilityReflector, activate_genesis


class TestInstabilityReflector(unittest.TestCase):
    """Tests für den Instabilitäts-Reflektor."""
    
    def setUp(self):
        """Setup für jeden Test."""
        self.reflector = InstabilityReflector(base_instability=0.5)
    
    def test_initialization(self):
        """Test: Reflektor wird korrekt initialisiert."""
        self.assertEqual(self.reflector.base_instability, 0.5)
        self.assertEqual(len(self.reflector.parameters), 0)
        self.assertEqual(len(self.reflector.harmonic_patterns), 0)
    
    def test_recombine_parameters(self):
        """Test: Parameter werden rekombiniert."""
        params = {"value1": 100.0, "value2": 50.0}
        recombined = self.reflector.recombine_parameters(params)
        
        # Prüfe dass Parameter existieren
        self.assertIn("value1", recombined)
        self.assertIn("value2", recombined)
        
        # Prüfe dass Werte sich ändern (mit hoher Wahrscheinlichkeit)
        # Bei sehr niedriger Instabilität könnten sie ähnlich sein
        self.assertIsInstance(recombined["value1"], float)
        self.assertIsInstance(recombined["value2"], float)
    
    def test_instability_calculation(self):
        """Test: Instabilität liegt im gültigen Bereich."""
        instability = self.reflector._calculate_instability()
        self.assertGreaterEqual(instability, 0.0)
        self.assertLessEqual(instability, 1.0)
    
    def test_harmonic_signature_generation(self):
        """Test: Harmonische Signatur wird generiert."""
        params = {"test": "value"}
        signature = self.reflector.generate_harmonic_signature(params)
        
        self.assertIsInstance(signature, str)
        self.assertGreater(len(signature), 0)
        # Prüfe dass nur harmonische Zeichen verwendet werden
        for char in signature:
            self.assertIn(char, ["█", "▓"])


class TestChaosKernel(unittest.TestCase):
    """Tests für den Chaos-Kernel."""
    
    def setUp(self):
        """Setup für jeden Test."""
        self.kernel = ChaosKernel()
    
    def test_initialization(self):
        """Test: Kernel wird korrekt initialisiert."""
        self.assertFalse(self.kernel.genesis_mode)
        self.assertIsNone(self.kernel.genesis_timestamp)
        self.assertEqual(len(self.kernel.state_failures), 0)
        self.assertEqual(len(self.kernel.active_states), 0)
    
    def test_activate_genesis_mode(self):
        """Test: Genesis-Modus kann aktiviert werden."""
        result = self.kernel.activate_genesis_mode()
        
        self.assertTrue(self.kernel.genesis_mode)
        self.assertIsNotNone(self.kernel.genesis_timestamp)
        self.assertEqual(result["status"], "genesis_activated")
        self.assertIn("timestamp", result)
        self.assertIn("initial_state", result)
        self.assertIn("proof_hash", result)
    
    def test_genesis_required_for_cycle(self):
        """Test: Chaos-Zyklus erfordert aktiven Genesis-Modus."""
        with self.assertRaises(RuntimeError):
            self.kernel.process_chaos_cycle({"test": "value"})
    
    def test_process_chaos_cycle(self):
        """Test: Chaos-Zyklus kann verarbeitet werden."""
        self.kernel.activate_genesis_mode()
        
        params = {"value": 100.0, "name": "test"}
        result = self.kernel.process_chaos_cycle(params)
        
        self.assertIn(result["status"], ["success", "state_failure"])
        self.assertIn("state", result)
        self.assertIn("proof", result)
    
    def test_multiple_chaos_cycles(self):
        """Test: Mehrere Chaos-Zyklen können verarbeitet werden."""
        self.kernel.activate_genesis_mode()
        
        for i in range(10):
            params = {"index": i, "value": i * 10}
            result = self.kernel.process_chaos_cycle(params)
            self.assertIn(result["status"], ["success", "state_failure"])
        
        # Mindestens einige Zustände sollten vorhanden sein
        total_states = len(self.kernel.active_states) + len(self.kernel.state_failures)
        self.assertGreaterEqual(total_states, 10)
    
    def test_system_metrics(self):
        """Test: System-Metriken werden korrekt geliefert."""
        self.kernel.activate_genesis_mode()
        
        # Verarbeite einige Zyklen
        for i in range(5):
            self.kernel.process_chaos_cycle({"index": i})
        
        metrics = self.kernel.get_system_metrics()
        
        self.assertTrue(metrics["genesis_active"])
        self.assertGreaterEqual(metrics["total_states"], 0)
        self.assertGreaterEqual(metrics["inverse_proofs"], 0)
        self.assertGreaterEqual(metrics["uptime"], 0)
    
    def test_export_state_failures(self):
        """Test: Zustandsausfälle können exportiert werden."""
        self.kernel.activate_genesis_mode()
        
        # Verarbeite viele Zyklen um Ausfälle zu provozieren
        for i in range(50):
            self.kernel.process_chaos_cycle({"index": i})
        
        failures = self.kernel.export_state_failures()
        self.assertIsInstance(failures, list)
        
        # Mit 50 Zyklen und 10% Ausfallrate sollten einige Ausfälle existieren
        # (probabilistisch, könnte auch 0 sein)
        for failure in failures:
            self.assertIn("timestamp", failure)
            self.assertIn("instability_level", failure)
            self.assertIn("proof_hash", failure)


class TestConvenienceFunctions(unittest.TestCase):
    """Tests für Convenience-Funktionen."""
    
    def test_activate_genesis_function(self):
        """Test: activate_genesis() Convenience-Funktion."""
        kernel = activate_genesis()
        
        self.assertIsInstance(kernel, ChaosKernel)
        self.assertTrue(kernel.genesis_mode)
        self.assertIsNotNone(kernel.genesis_timestamp)


class TestSystemState(unittest.TestCase):
    """Tests für SystemState."""
    
    def test_state_creation(self):
        """Test: Systemzustand wird korrekt erstellt."""
        kernel = ChaosKernel()
        kernel.activate_genesis_mode()
        
        params = {"test": "value"}
        state = kernel._create_state(params)
        
        self.assertIsNotNone(state.timestamp)
        self.assertEqual(state.parameters, params)
        self.assertGreaterEqual(state.instability_level, 0.0)
        self.assertLessEqual(state.instability_level, 1.0)
        self.assertIsNotNone(state.harmonic_signature)
        self.assertIsNotNone(state.proof_hash)


class TestInverseProof(unittest.TestCase):
    """Tests für Invers-Proofs."""
    
    def test_proof_generation(self):
        """Test: Invers-Proof wird generiert."""
        kernel = ChaosKernel()
        kernel.activate_genesis_mode()
        
        params = {"test": "value"}
        state = kernel._create_state(params)
        proof = kernel._generate_inverse_proof(state)
        
        self.assertIsNotNone(proof.original_hash)
        self.assertIsNotNone(proof.inverse_hash)
        self.assertIsNotNone(proof.timestamp)
        self.assertIn("state_timestamp", proof.verification_data)
    
    def test_proof_hashes_differ(self):
        """Test: Original und Inverse Hash unterscheiden sich."""
        kernel = ChaosKernel()
        kernel.activate_genesis_mode()
        
        params = {"test": "value"}
        state = kernel._create_state(params)
        proof = kernel._generate_inverse_proof(state)
        
        self.assertNotEqual(proof.original_hash, proof.inverse_hash)


if __name__ == "__main__":
    unittest.main()
