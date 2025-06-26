    def test_heart(self):
        """Test the Heart component."""
        logging.info("\n" + "=" * 60)
        logging.info("TESTING HEART COMPONENT")
        logging.info("=" * 60)
        
        try:
            # Create mock dependencies
            mock_brainstem = MagicMock()
            mock_body = MagicMock()
            mock_body.register_module = MagicMock(return_value=True)
            mock_body.emit_event = MagicMock(return_value=True)
            
            # Test 1: Basic initialization
            heart = Heart(brainstem=mock_brainstem, body=mock_body)
            if heart.heartbeat_rate != 1.0 or heart.pulse_capacity != 10:
                self.results.record_fail("Heart initialization", "Default parameters not set correctly")
            else:
                self.results.record_pass("Heart initialization")
            
            # Test 2: Heart rate adjustment
            heart.set_rate(0.5)
            if heart.heartbeat_rate != 0.5:
                self.results.record_fail("Heart rate adjustment", "Rate not updated correctly")
            else:
                self.results.record_pass("Heart rate adjustment")
            
            # Test 3: Pulse capacity adjustment
            heart.set_pulse_capacity(20)
            if heart.pulse_capacity != 20:
                self.results.record_fail("Pulse capacity adjustment", "Capacity not updated correctly")
            else:
                self.results.record_pass("Pulse capacity adjustment")
            
            # Test 4: Run a few heartbeats and check brainstem pulses
            heart.start(cycles=5)
            # Verify brainstem was called
            if not mock_brainstem.pulse.called:
                self.results.record_fail("Heart pulse to brainstem", "Brainstem pulse method not called")
            else:
                self.results.record_pass("Heart pulse to brainstem")
            
            # Test 5: Check event emission
            if not mock_body.emit_event.called:
                self.results.record_fail("Heart event emission", "Body emit_event method not called")
            else:
                self.results.record_pass("Heart event emission")
            
            # Test 6: Status reporting
            status = heart.get_status()
            if not isinstance(status, dict) or 'state' not in status:
                self.results.record_fail("Heart status reporting", "Status not returned as expected")
            else:
                self.results.record_pass("Heart status reporting")
                
            # Test 7: Background thread operation
            heart = Heart(brainstem=mock_brainstem, body=mock_body)
            heart.set_rate(0.1)  # Fast rate for testing
            heart.start()  # Start in background
            
            # Wait a moment and check that beats occurred
            time.sleep(0.5)
            initial_count = heart.beat_count
            
            # Wait more time and check for more beats
            time.sleep(0.5)
            if heart.beat_count <= initial_count:
                self.results.record_fail("Heart background operation", "Beat count did not increase")
            else:
                self.results.record_pass("Heart background operation")
                
            # Stop the heart and ensure it's stopped
            heart.stop()
            time.sleep(0.2)
            if heart.alive:
                self.results.record_fail("Heart stop function", "Heart still alive after stop")
            else:
                self.results.record_pass("Heart stop function")
                
            # Test 8: Integration with real Body
            try:
                real_body = Body()
                heart = Heart(brainstem=mock_brainstem, body=real_body)
                heart.set_rate(0.1)
                
                # Register with body - pass body as parameter
                if not heart.register_with_body(body=real_body):
                    self.results.record_fail("Heart-Body integration", "Failed to register with Body")
                else:
                    self.results.record_pass("Heart-Body integration")
                    
                # Run a few heartbeats
                heart.start(cycles=2)
                
                # Clean up
                if heart.thread and heart.thread.is_alive():
                    heart.stop()
            except Exception as e:
                self.results.record_fail("Heart-Body integration", str(e))
            
        except Exception as e:
            self.results.record_fail("Heart component", str(e))
            
        return True
