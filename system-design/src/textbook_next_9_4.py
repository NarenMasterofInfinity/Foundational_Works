"""Textbook chapter 9-4: original prompts, case study, and diagrams commission."""
INTRO="At first, a document extraction platform looks straightforward. The chapter “Access patterns, retention & operational cost” follows one real operation through the system and asks what can go wrong. Start with a simple design; add complexity only after naming the observable requirement and the failure to prevent."
TOPICS=["Data retention and lifecycle.","Polyglot persistence and its operational costs."]
CODE="def eligible_for_expiry(created, cutoff, has_hold):\n    return created < cutoff and not has_hold"
QUESTIONS=["Using a document extraction platform, explain Data retention and lifecycle. Who owns the change? Draw the before/after state or sequence. What breaks if a request is repeated, delayed, or interrupted? Which guarantee is demonstrated, and which is not?","Using a document extraction platform, explain Polyglot persistence and its operational costs. Who owns the change? Draw the before/after state or sequence. What breaks if a request is repeated, delayed, or interrupted? Which guarantee is demonstrated, and which is not?"]
FORMS=["ladder","ledger"]
