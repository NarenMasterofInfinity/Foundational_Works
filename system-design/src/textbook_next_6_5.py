"""NCERT-inspired additional worked narrative for 6.5."""
INTRO="Think about a notification service that sends email, SMS, or push messages. This chapter, “Structural patterns”, starts with something a person wants to do, then follows the data and the responsibility until a design choice becomes necessary. The original technical lesson follows so that the explanation stays precise, even when an everyday analogy stops being accurate."
TOPICS=["Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy."]
CODE="class LoggingSender:\n    def __init__(self, inner, log): self.inner, self.log = inner, log\n    def send(self, message):\n        self.log('send requested')\n        return self.inner.send(message)"
QUESTIONS=["Apply “Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy” to a notification service that sends email, SMS, or push messages. What is the smallest working design? Which component owns the decision, which observable failure could break it, and what would you test? Name one limitation of the simple approach before adding infrastructure."]
FORMS=["tree"]
