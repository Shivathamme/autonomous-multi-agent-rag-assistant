class ChatMemory:
    def __init__(self, max_history=3):
        self.history = []
        self.max_history = max_history

    def add(self, query, response):
        self.history.append({
            "query": query,
            "response": response
        })

    def get_context(self):
        if not self.history:
            return ""

        context = ""

        for item in self.history[-self.max_history:]:
            context += f"Q: {item['query']}\nA: {item['response']}\n\n"

        return context.strip()