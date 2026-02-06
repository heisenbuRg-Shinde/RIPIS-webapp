class IntentParser:
    """
    IntentParser is responsible for understanding
    what kind of interview question the user is asking.
    This is intentionally rule-based for explainability.
    """

    def parse(self, text: str) -> dict:
        text = text.lower()

        interview_type = self._detect_interview_type(text)
        domain = self._detect_domain(text)
        subtopic = self._detect_subtopic(text, domain)

        return {
            "interview_type": interview_type,
            "domain": domain,
            "subtopic": subtopic
        }

    def _detect_interview_type(self, text: str) -> str:
        """
        Detect whether the question is coding or theory.
        """
        coding_keywords = [
            "code", "implement", "solve", "algorithm",
            "function", "write", "program"
        ]

        for word in coding_keywords:
            if word in text:
                return "coding"

        return "theory"

    def _detect_domain(self, text: str) -> str:
        """
        Detect main subject domain: DSA, OS, or DBMS.
        """
        if any(word in text for word in ["array", "linked list", "stack", "queue", "tree", "graph"]):
            return "DSA"

        if any(word in text for word in ["deadlock", "process", "thread", "semaphore", "cpu", "scheduling"]):
            return "OS"

        if any(word in text for word in ["dbms", "database", "sql", "normalization", "index", "transaction"]):
            return "DBMS"

        # Default fallback
        return "DSA"

    def _detect_subtopic(self, text: str, domain: str) -> str | None:
        """
        Detect a finer-grain subtopic inside the domain.
        """
        dsa_map = {
            "array": ["array", "two sum", "sliding window"],
            "linked list": ["linked list"],
            "stack": ["stack"],
            "queue": ["queue"],
            "tree": ["tree", "binary tree", "bst"],
            "graph": ["graph", "dfs", "bfs"]
        }

        os_map = {
            "deadlock": ["deadlock"],
            "cpu scheduling": ["scheduling", "cpu scheduling"],
            "memory management": ["paging", "segmentation", "virtual memory"]
        }

        dbms_map = {
            "normalization": ["normalization"],
            "indexing": ["index"],
            "transactions": ["acid", "transaction"]
        }

        domain_map = {
            "DSA": dsa_map,
            "OS": os_map,
            "DBMS": dbms_map
        }

        for subtopic, keywords in domain_map.get(domain, {}).items():
            for word in keywords:
                if word in text:
                    return subtopic

        return None
