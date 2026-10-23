"""NCERT-inspired additional worked narrative for 6.6."""
INTRO="Think about a notification service that sends email, SMS, or push messages. This chapter, “Behavioral patterns”, starts with something a person wants to do, then follows the data and the responsibility until a design choice becomes necessary. The original technical lesson follows so that the explanation stays precise, even when an everyday analogy stops being accurate."
TOPICS=["Strategy, Observer, Command, State, Chain of Responsibility, Template Method, Iterator, Mediator, Memento, Visitor."]
CODE="class EmailStrategy:\n    def send(self, text): return f'email:{text}'\nclass SmsStrategy:\n    def send(self, text): return f'sms:{text}'"
QUESTIONS=["Apply “Strategy, Observer, Command, State, Chain of Responsibility, Template Method, Iterator, Mediator, Memento, Visitor” to a notification service that sends email, SMS, or push messages. What is the smallest working design? Which component owns the decision, which observable failure could break it, and what would you test? Name one limitation of the simple approach before adding infrastructure."]
FORMS=["decision"]
