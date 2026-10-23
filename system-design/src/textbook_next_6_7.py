"""NCERT-inspired additional worked narrative for 6.7."""
INTRO="Think about a notification service that sends email, SMS, or push messages. This chapter, “Enterprise patterns & boundaries”, starts with something a person wants to do, then follows the data and the responsibility until a design choice becomes necessary. The original technical lesson follows so that the explanation stays precise, even when an everyday analogy stops being accurate."
TOPICS=["Repository, Unit of Work, Specification, CQRS, and dependency boundaries."]
CODE="def publish_after_commit(db, event):\n    with db.transaction() as tx:\n        tx.save_business_change(event)\n        tx.insert_outbox(event.id, event.payload)\n    # relay publishes later; duplicates remain possible"
QUESTIONS=["Apply “Repository, Unit of Work, Specification, CQRS, and dependency boundaries” to a notification service that sends email, SMS, or push messages. What is the smallest working design? Which component owns the decision, which observable failure could break it, and what would you test? Name one limitation of the simple approach before adding infrastructure."]
FORMS=["ladder"]
