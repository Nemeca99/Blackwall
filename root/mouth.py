"""
Mouth

Output generation and delivery for Lyra Blackwall.
Handles stylization and delivery of system responses.

Expected Interface:
- speak(response, fragment_weights): output a response
- Optionally register for 'output_sent' events from body
"""

class Mouth:
    def __init__(self):
        """Initialize mouth state."""
        pass

    def speak(self, response, fragment_weights):
        """Stylize and deliver a response."""
        print(f"[LYRA] {response}")
        return response
