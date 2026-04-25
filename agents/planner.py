def planner_agent(query: str) -> str:
    q = query.lower()

    # FIRST PRIORITY: PDF-related queries
    pdf_keywords = [
        "pdf", "document", "file", "uploaded",
        "my document", "my pdf"
    ]
    if any(word in q for word in pdf_keywords):
        return "research"

    # All queries that need real-time or general knowledge → web
    web_triggers = [
        # Time-based
        "news", "latest", "recent", "today", "2025", "2026",
        "current", "now", "update", "trending", "live",

        # Question words (general knowledge)
        "what is", "what are", "who is", "who are",
        "explain", "define", "meaning of", "definition",
        "how does", "how do", "how is", "how was", "how are",
        "tell me about", "describe",

        # Roles and positions
        "chief minister", "prime minister", "cm of", "pm of",
        "cm ", " cm ", "president of", "governor of",
        "minister", "secretary of", "chairman of", "ceo of",
        "director of", "head of", "leader of",

        # Politics and government
        "government", "election", "party", "parliament",
        "cabinet", "policy", "bill", "law", "act",
        "ruling", "opposition",

        # People and places
        "capital of", "population of", "currency of",
        "language of", "founded", "headquarters",
        "located in", "situated",

        # Companies and orgs
        "company", "startup", "organization", "founded by",
        "acquired", "merger",

        # Sports, events
        "score", "match", "winner", "championship",
        "tournament", "result",

        # Catch-all for facts
        "when did", "when was", "where is", "where was",
        "which is", "which was",
    ]

    if any(t in q for t in web_triggers):
        return "web_search"

    # Default: try RAG (document search)
    return "research"
