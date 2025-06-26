"""
Body (Bloodstream)

Acts as the main hub and signal carrier for the system. The body routes data, events,
and signals between all other modules, ensuring that every part of Lyra Blackwall
is connected and synchronized.
"""

class Body:
    def __init__(self):
        """Initialize the body interface system."""
        # Registry of connected modules
        self.modules = {}
        
        # Event handlers: event_name -> list of callbacks
        self.event_handlers = {}
        
        print("[Body] Initialized")

    def register_module(self, name, module):
        """Register a module with the body system."""
        self.modules[name] = module
        print(f"[Body] Registered module: {name}")
        return True

    def route_signal(self, source, target, payload):
        """Route a signal from source to target module."""
        if target in self.modules:
            if hasattr(self.modules[target], "receive_signal"):
                self.modules[target].receive_signal(source, payload)
                return True
            else:
                print(f"[Body] Module {target} cannot receive signals")
                return False
        else:
            print(f"[Body] Unknown target module: {target}")
            return False

    def broadcast_signal(self, source, payload, exclude=None):
        """Broadcast a signal to all modules except excluded ones."""
        exclude = exclude or []
        success = True
        
        for name, module in self.modules.items():
            if name != source and name not in exclude:
                if hasattr(module, "receive_signal"):
                    module.receive_signal(source, payload)
                else:
                    success = False
        
        return success
        
    def register_for_event(self, event_name, callback):
        """Register a callback to be run when the specified event is emitted."""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        
        # Store the callback directly without module_name for simpler register_for_event API
        self.event_handlers[event_name].append(callback)
        print(f"[Body] Registered handler for event '{event_name}'")
        return True
        
    def register_handler(self, event_name, module_name, callback):
        """Register an event handler (legacy method, use register_for_event instead)."""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        
        # Store as a tuple to maintain compatibility with existing code
        self.event_handlers[event_name].append((module_name, callback))
        print(f"[Body] Registered handler for event '{event_name}' from {module_name}")
        return True
        
    def emit_event(self, event_name, payload=None):
        """Emit an event to all registered handlers."""
        if event_name not in self.event_handlers:
            print(f"[Body] No handlers registered for event '{event_name}'")
            # If no specific handlers, create empty list
            self.event_handlers[event_name] = []
            
        success = True
        
        # Call registered handlers
        for handler in self.event_handlers[event_name]:
            try:
                # Check if it's a tuple (from register_handler) or a direct callback (from register_for_event)
                if isinstance(handler, tuple):
                    module_name, callback = handler
                    callback(payload)
                    print(f"[Body] Event '{event_name}' handled by {module_name}")
                else:
                    # Direct callback from register_for_event
                    handler(payload)
            except Exception as e:
                print(f"[Body] Error in event handler for '{event_name}': {str(e)}")
                success = False
        
        # Also broadcast the event to all modules that have handle_event method
        for name, module in self.modules.items():
            if hasattr(module, "handle_event"):
                try:
                    module.handle_event(event_name, payload)
                    success = True
                except Exception as e:
                    print(f"[Body] Error in {name} general handler for {event_name}: {e}")
                    success = False
        
        return success

    def pulse(self, interval=1.0):
        """Send a heartbeat pulse to all modules."""
        self.emit_event("heartbeat", {"interval": interval})
        return True

    def speak(self, response, fragment_weights=None):
        """Output a response (typically via the mouth module)."""
        if "mouth" in self.modules:
            if hasattr(self.modules["mouth"], "speak"):
                self.modules["mouth"].speak(response, fragment_weights)
                return True
        
        # Fallback if no mouth module
        print(f"\n[System Output] {response}")
        return True

# For direct testing
if __name__ == "__main__":
    body = Body()
    body.register_handler("test", "test_module", lambda data: print(f"Received: {data}"))
    body.emit_event("test", "Hello World")
    body.speak("Testing the body interface system.")
