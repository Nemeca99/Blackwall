"""
Router/Registry module for dynamic organ discovery and routing table management.
"""

class Router:
    def __init__(self):
        self.routing_table = {}
        self.next_id = 1
        self.organs = {}

    def broadcast_registration_request(self, organs):
        """Ping all organs to register themselves."""
        for organ in organs:
            organ_info = organ.register_with_router(self)
            self.register_organ(organ, organ_info)

    def register_organ(self, organ, organ_info):
        organ_id = f"organ-{self.next_id}"
        self.next_id += 1
        organ_info['id'] = organ_id
        self.routing_table[organ_id] = organ_info
        self.organs[organ_id] = organ
        print(f"[Router] Registered organ: {organ_info['name']} as {organ_id}")
        return organ_id

    def get_routing_table(self):
        return self.routing_table

    def get_organ_by_id(self, organ_id):
        return self.organs.get(organ_id)

    def unregister_organ(self, organ_id):
        if organ_id in self.routing_table:
            print(f"[Router] Unregistering organ: {organ_id}")
            del self.routing_table[organ_id]
            del self.organs[organ_id]

    def write_routing_table_to_file(self, file_path: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Dynamic Routing Table\n====================\n")
            for organ_id, info in self.routing_table.items():
                f.write(f"ID: {organ_id}\n")
                for k, v in info.items():
                    if k != 'id':
                        f.write(f"  {k}: {v}\n")
                f.write("\n")
        print(f"[Router] Routing table written to {file_path}")

    def find_organs_by_capability(self, capability: str):
        """Return a list of organ IDs that provide the given capability."""
        return [oid for oid, info in self.routing_table.items() if capability in info.get('capabilities', [])]

    def route_task(self, capability: str, strategy: str = 'first'):
        """Return the best organ for a given capability. Strategy: 'first', 'random', or 'round_robin'."""
        import random
        candidates = self.find_organs_by_capability(capability)
        if not candidates:
            return None
        if strategy == 'random':
            return random.choice(candidates)
        # For now, just return the first (could add round-robin logic later)
        return candidates[0]

    def print_status(self):
        print("[Router] Current organ status:")
        for organ_id, info in self.routing_table.items():
            print(f"  {organ_id}: {info['name']} ({info['type']}) - {info['capabilities']}")

    def ping_organs(self):
        """Ping all registered organs to check if they are alive/responding."""
        print("[Router] Pinging all organs...")
        results = {}
        for organ_id, organ in self.organs.items():
            try:
                if hasattr(organ, 'ping'):
                    result = organ.ping()
                else:
                    # If no ping method, assume alive for demo
                    result = True
                results[organ_id] = result
                status = 'alive' if result else 'unresponsive'
                print(f"  {organ_id}: {self.routing_table[organ_id]['name']} is {status}")
            except Exception as e:
                results[organ_id] = False
                print(f"  {organ_id}: {self.routing_table[organ_id]['name']} ping failed: {e}")
        return results

    def route_by_context(self, prompt: str, logger=None):
        """Route based on prompt context/keywords. Returns (organ_id, reason)."""
        prompt_lower = prompt.lower()
        # Simple keyword-based context routing
        if any(word in prompt_lower for word in ["integrate", "derivative", "math", "calculate", "sum", "add", "subtract", "multiply", "divide"]):
            candidates = self.find_organs_by_capability("math")
            if candidates:
                if logger: logger.log(f"[Router] Context: math detected. Routing to {candidates[0]}")
                return candidates[0], "math capability"
        if any(word in prompt_lower for word in ["translate", "language", "french", "spanish", "english", "german"]):
            candidates = self.find_organs_by_capability("language")
            if candidates:
                if logger: logger.log(f"[Router] Context: language detected. Routing to {candidates[0]}")
                return candidates[0], "language capability"
        if any(word in prompt_lower for word in ["recall", "memory", "remember", "history", "last input"]):
            candidates = self.find_organs_by_capability("memory")
            if candidates:
                if logger: logger.log(f"[Router] Context: memory detected. Routing to {candidates[0]}")
                return candidates[0], "memory capability"
        # Default: use first organ with 'input_processing' or fallback
        candidates = self.find_organs_by_capability("input_processing")
        if candidates:
            if logger: logger.log(f"[Router] Context: default input_processing. Routing to {candidates[0]}")
            return candidates[0], "default input_processing"
        # Fallback: any organ
        if self.routing_table:
            fallback_id = next(iter(self.routing_table))
            if logger: logger.log(f"[Router] Context: fallback. Routing to {fallback_id}")
            return fallback_id, "fallback"
        return None, "no available organ"

    def route(self, message, destination=None, source=None):
        """
        Route a message to appropriate destination(s) based on content and routing rules.
        
        Args:
            message: The message to route
            destination: Optional specific destination ID
            source: Optional source ID
            
        Returns:
            bool: True if routing succeeded, False otherwise
        """
        if destination:
            # Direct routing to specific destination
            if destination in self.organs:
                organ = self.organs[destination]
                if hasattr(organ, "receive"):
                    organ.receive(message, source)
                    return True
            return False
              # Content-based routing
        if isinstance(message, dict):
            message_type = message.get("type", "")
            
            # Route based on message type
            if message_type == "query":
                # Find organs that can handle queries
                handlers = self.find_organs_by_capability("query_processing")
                for handler_id in handlers:
                    self.organs[handler_id].receive(message, source)
                return len(handlers) > 0
                
            elif message_type == "command":
                # Find organs that can handle commands
                handlers = self.find_organs_by_capability("command_processing") 
                for handler_id in handlers:
                    self.organs[handler_id].receive(message, source)
                return len(handlers) > 0
                  # Broadcast to all organs if no specific routing
        for _, organ in self.organs.items():
            if hasattr(organ, "receive"):
                organ.receive(message, source)
                
        return True
