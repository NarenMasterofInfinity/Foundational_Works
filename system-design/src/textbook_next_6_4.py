"""NCERT-inspired additional worked narrative for 6.4."""
INTRO="Think about a notification service that sends email, SMS, or push messages. This chapter, “Creational patterns”, starts with something a person wants to do, then follows the data and the responsibility until a design choice becomes necessary. The original technical lesson follows so that the explanation stays precise, even when an everyday analogy stops being accurate."
TOPICS=["Factory Method, Abstract Factory, Builder, Prototype, Singleton."]
CODE="class MessageBuilder:\n    def __init__(self): self.payload = {}\n    def subject(self, text):\n        self.payload['subject'] = text\n        return self\n    def build(self): return dict(self.payload)"
QUESTIONS=["Apply “Factory Method, Abstract Factory, Builder, Prototype, Singleton” to a notification service that sends email, SMS, or push messages. What is the smallest working design? Which component owns the decision, which observable failure could break it, and what would you test? Name one limitation of the simple approach before adding infrastructure."]
FORMS=["contrast"]
