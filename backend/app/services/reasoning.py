"""
Reasoning Engine for RIPIS - Real-Time Interview Practice Intelligence System

This module provides rule-based, template-driven reasoning for interview practice.
It generates structured hints and guidance WITHOUT providing final solutions.

Design Philosophy:
- Pure rule-based logic (no LLM/API calls)
- Template-based responses for consistency
- Focus on teaching approach, not giving answers
- Domain-specific knowledge bases for DSA, OS, and DBMS
"""

from typing import Dict, Optional, List


class ReasoningEngine:
    """
    Rule-based reasoning engine that generates structured interview hints.
    
    The engine uses predefined knowledge templates organized by:
    - interview_type: coding or theory
    - domain: DSA, OS, or DBMS
    - subtopic: specific area within the domain
    
    Output provides guidance on concepts, approaches, and common pitfalls
    without revealing complete solutions.
    """
    
    def __init__(self):
        """
        Initialize the reasoning engine with knowledge bases.
        
        Design choice: Using nested dictionaries for O(1) lookup performance.
        Knowledge is organized hierarchically: domain -> subtopic -> content
        """
        # DSA (Data Structures & Algorithms) knowledge base
        self._dsa_knowledge = self._build_dsa_knowledge()
        
        # OS (Operating Systems) knowledge base
        self._os_knowledge = self._build_os_knowledge()
        
        # DBMS (Database Management Systems) knowledge base
        self._dbms_knowledge = self._build_dbms_knowledge()
    
    def generate_reasoning(
        self, 
        interview_type: str, 
        domain: str, 
        subtopic: Optional[str] = None,
        voice_assisted: bool = False
    ) -> Dict[str, str]:
        """
        Generate structured reasoning based on interview context.
        
        Args:
            interview_type: 'coding' or 'theory'
            domain: 'DSA', 'OS', or 'DBMS'
            subtopic: Specific topic within domain (e.g., 'array', 'deadlock')
            voice_assisted: Whether to generate a conversational voice script
        
        Returns:
            Dictionary containing:
            - concept: Core concept explanation
            - approach: High-level problem-solving approach
            - pseudocode: Non-executable algorithmic steps
            - common_mistakes: Typical pitfalls to avoid
            - voice_script: (Optional) Conversational summary for TTS
        
        Design choice: Return structured dict for easy JSON serialization
        and flexible frontend rendering.
        """
        domain = domain.upper()
        
        # Route to appropriate knowledge base
        if domain == 'DSA':
            result = self._get_dsa_reasoning(subtopic, interview_type)
        elif domain == 'OS':
            result = self._get_os_reasoning(subtopic, interview_type)
        elif domain == 'DBMS':
            result = self._get_dbms_reasoning(subtopic, interview_type)
        else:
            result = self._get_fallback_reasoning(domain, subtopic)
            
        # Add voice script if requested
        if voice_assisted:
            result['voice_script'] = self._generate_voice_script(result, domain, subtopic)
            
        return result

    def _generate_voice_script(self, content: Dict[str, str], domain: str, subtopic: str) -> str:
        """Generate a concise, conversational script for Text-to-Speech."""
        topic_name = subtopic.replace('_', ' ').title() if subtopic else domain
        
        # Create a natural summary
        script = f"Here is the reasoning for {topic_name}. "
        script += f"Conceptually, {content['concept'].split('.')[0]}. " # First sentence of concept
        script += "To approach this, " + content['approach'].split('.')[0] + ". " # First sentence of approach
        script += "Be careful to avoid " + content['common_mistakes'].split(',')[0] + "." # First mistake
        
        return script
    
    def _get_dsa_reasoning(self, subtopic: Optional[str], interview_type: str) -> Dict[str, str]:
        """
        Generate DSA-specific reasoning.
        
        Design choice: Subtopic-based lookup with fallback to general guidance.
        This allows extensibility - new subtopics can be added easily.
        """
        if subtopic and subtopic.lower() in self._dsa_knowledge:
            knowledge = self._dsa_knowledge[subtopic.lower()]
        else:
            # Fallback for unknown subtopics
            knowledge = self._dsa_knowledge['general']
        
        return knowledge
    
    def _get_os_reasoning(self, subtopic: Optional[str], interview_type: str) -> Dict[str, str]:
        """Generate OS-specific reasoning."""
        if subtopic and subtopic.lower() in self._os_knowledge:
            knowledge = self._os_knowledge[subtopic.lower()]
        else:
            knowledge = self._os_knowledge['general']
        
        return knowledge
    
    def _get_dbms_reasoning(self, subtopic: Optional[str], interview_type: str) -> Dict[str, str]:
        """Generate DBMS-specific reasoning."""
        if subtopic and subtopic.lower() in self._dbms_knowledge:
            knowledge = self._dbms_knowledge[subtopic.lower()]
        else:
            knowledge = self._dbms_knowledge['general']
        
        return knowledge
    
    def _get_fallback_reasoning(self, domain: str, subtopic: Optional[str]) -> Dict[str, str]:
        """
        Provide generic reasoning when domain is unknown.
        
        Design choice: Always return valid structure to prevent errors downstream.
        """
        return {
            'concept': f'General problem-solving in {domain}',
            'approach': 'Break down the problem into smaller components. Identify inputs, outputs, and constraints.',
            'pseudocode': '1. Understand the requirements\n2. Identify key components\n3. Plan your solution step-by-step\n4. Consider edge cases',
            'common_mistakes': 'Not clarifying requirements, jumping to implementation too quickly, ignoring edge cases',
            'example_code': '# Python Example\ndef solve(problem):\n    parts = break_down(problem)\n    for part in parts:\n        solve_part(part)\n    return combine_results()',
            'syntax_structure': 'Structure: Input -> Process -> Output\nLanguage: Python/Java/C++ common patterns'
        }
    
    # ========== DSA Knowledge Base ==========
    
    def _build_dsa_knowledge(self) -> Dict[str, Dict[str, str]]:
        """
        Build comprehensive DSA knowledge base.
        
        Design choice: Separate method for each knowledge base to maintain
        modularity and make updates easier.
        """
        return {
            'array': {
                'concept': 'Arrays are contiguous memory structures with O(1) random access. Common patterns include two-pointer, sliding window, and hash-based lookups.',
                'approach': 'Consider using a hashmap to track seen elements for O(1) lookup. Think about whether sorting helps. For subarray problems, explore sliding window or prefix sums.',
                'pseudocode': '1. Initialize hashmap to store element -> index mapping\n2. Iterate through array once\n3. For each element, check if complement/target exists in hashmap\n4. Update hashmap with current element\n5. Return result when condition is met',
                'common_mistakes': 'Not handling duplicates, forgetting to check array bounds, using nested loops when hashmap would give O(n) solution, not considering negative numbers or zeros',
                'example_code': '# Python: List (Dynamic Array)\narr = [1, 2, 3, 4, 5]\nval = arr[2]  # O(1) Access\n\n// C++: Static Array\nint arr[5] = {1, 2, 3, 4, 5};\n\n// C++: Vector (Dynamic)\nvector<int> v = {1, 2, 3};',
                'syntax_structure': 'Python: list_name = [elements]\nC++: type name[size]; OR vector<type> name;\nAccess: arr[index]'
            },
            'string': {
                'concept': 'Strings are immutable sequences. Key techniques: character frequency counting, two-pointer, sliding window, pattern matching (KMP, Rabin-Karp).',
                'approach': 'For anagram/permutation problems, use character frequency maps. For substring problems, consider sliding window. For pattern matching, think about preprocessing.',
                'pseudocode': '1. Create frequency map of characters\n2. Use two pointers or sliding window\n3. Track window state (valid/invalid)\n4. Expand/contract window based on conditions\n5. Update result when window is valid',
                'common_mistakes': 'Treating strings as mutable (in languages where they aren\'t), not handling case sensitivity, forgetting about special characters, inefficient substring operations',
                'example_code': '# Python\ns = "hello"\ncount = collections.Counter(s)\n\n// C++\nstring s = "hello";\ns[0] = \'H\'; // Mutable in C++',
                'syntax_structure': 'Python: s = "text" (Immutable)\nC++: string s = "text"; (Mutable)\nJava: String s = "text"; (Immutable)'
            },
            'linked_list': {
                'concept': 'Linked lists provide dynamic size with O(1) insertion/deletion but O(n) access. Key patterns: fast-slow pointers, dummy nodes, reversal.',
                'approach': 'Use dummy node to simplify edge cases. Fast-slow pointer for cycle detection or finding middle. Consider reversing portions of the list.',
                'pseudocode': '1. Create dummy node pointing to head\n2. Initialize slow and fast pointers\n3. Move fast pointer 2x speed of slow\n4. When fast reaches end, slow is at middle\n5. Perform required operation on identified node',
                'common_mistakes': 'Losing reference to head, not handling null pointers, off-by-one errors in pointer movement, forgetting to update next pointers after modification',
                'example_code': '# Python Node\nclass ListNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.next = None\n\n// C++ Struct\nstruct ListNode {\n    int val;\n    ListNode *next;\n};',
                'syntax_structure': 'Node Structure: Value + Pointer to Next\nTraversal: while head: head = head.next'
            },
            'tree': {
                'concept': 'Trees are hierarchical structures. Binary trees have at most 2 children. Key traversals: inorder, preorder, postorder, level-order. BST property: left < root < right.',
                'approach': 'Choose traversal based on problem: inorder for BST sorted order, postorder for bottom-up, preorder for top-down, level-order for breadth-first.',
                'pseudocode': '1. Base case: if node is null, return\n2. Process left subtree (recursive call)\n3. Process current node\n4. Process right subtree (recursive call)\n5. Combine results from subtrees',
                'common_mistakes': 'Not handling null nodes, confusing traversal orders, not considering tree balance, forgetting that BST property applies to entire subtrees not just immediate children',
                'example_code': '# DFS (Recursion)\ndef dfs(root):\n    if not root: return\n    dfs(root.left)\n    print(root.val)\n    dfs(root.right)',
                'syntax_structure': 'Tree: Root Node -> Children Nodes\nBinary Tree: Left Child, Right Child\nTraversals: In/Pre/Post Order (DFS), Level Order (BFS)'
            },
            'graph': {
                'concept': 'Graphs represent relationships between entities. Can be directed/undirected, weighted/unweighted. Key algorithms: BFS, DFS, Dijkstra, Union-Find.',
                'approach': 'For shortest path in unweighted graph, use BFS. For connectivity/cycles, use DFS or Union-Find. For weighted shortest path, use Dijkstra or Bellman-Ford.',
                'pseudocode': '1. Build adjacency list representation\n2. Initialize visited set and queue/stack\n3. Start from source node\n4. For each neighbor, check if visited\n5. Process unvisited neighbors and mark as visited\n6. Continue until queue/stack is empty',
                'common_mistakes': 'Not handling disconnected components, forgetting to mark nodes as visited, using DFS when BFS is needed (or vice versa), not considering directed vs undirected',
                'example_code': '# Adjacency List (Python)\ngraph = {\n  0: [1, 2],\n  1: [2],\n  2: [0]\n}\n\n// Adjacency Matrix (C++)\nvector<vector<int>> adj;',
                'syntax_structure': 'Representations: Adjacency List (Map/Vector of Vectors), Adjacency Matrix (2D Array)\nEdge List: List of (u, v) pairs'
            },
            'dynamic_programming': {
                'concept': 'DP solves problems by breaking them into overlapping subproblems. Key: identify state, recurrence relation, base cases. Memoization (top-down) or tabulation (bottom-up).',
                'approach': 'Define what dp[i] represents. Find recurrence: how does dp[i] relate to previous states? Identify base cases. Decide top-down or bottom-up.',
                'pseudocode': '1. Define state: what does dp[i][j] represent?\n2. Initialize base cases\n3. Fill dp table using recurrence relation\n4. For each state, compute based on previous states\n5. Final answer is in dp[n] or dp[n][m]',
                'common_mistakes': 'Not clearly defining state, incorrect recurrence relation, missing base cases, using too much space when optimization possible, confusing indices',
                'example_code': '# Memoization\nmemo = {}\ndef fib(n):\n    if n in memo: return memo[n]\n    if n <= 1: return n\n    memo[n] = fib(n-1) + fib(n-2)\n    return memo[n]',
                'syntax_structure': 'Pattern: State Definition -> Base Case -> Recurrence Relation\nTop-Down: Recursion + Memoization\nBottom-Up: Iteration + Table'
            },
            'sorting': {
                'concept': 'Sorting arranges elements in order. Comparison-based: O(n log n) lower bound. Non-comparison: counting sort, radix sort can be O(n). Stability matters for some problems.',
                'approach': 'For general sorting, use built-in sort (typically quicksort/mergesort). For nearly sorted data, consider insertion sort. For fixed range integers, consider counting sort.',
                'pseudocode': '1. Choose pivot element (for quicksort)\n2. Partition array: elements < pivot on left, > pivot on right\n3. Recursively sort left partition\n4. Recursively sort right partition\n5. Base case: array of size 0 or 1 is sorted',
                'common_mistakes': 'Not considering stability requirements, using wrong algorithm for data characteristics, not handling equal elements properly, inefficient pivot selection',
                'example_code': '# Python Sort\narr.sort()  # In-place Timsort\n\n// C++ Sort\nstd::sort(arr.begin(), arr.end()); // Introsort',
                'syntax_structure': 'Syntax: sort(collection, key=lambda x: ...)\nComplexity: Usually O(N log N)'
            },
            'searching': {
                'concept': 'Binary search on sorted data gives O(log n) search. Key: maintain invariant that answer is within search space. Works on monotonic functions.',
                'approach': 'Ensure data is sorted. Define search space [left, right]. Calculate mid. Decide which half contains answer. Update search space. Handle edge cases.',
                'pseudocode': '1. Initialize left = 0, right = n - 1\n2. While left <= right:\n3.   mid = left + (right - left) / 2\n4.   If target found at mid, return mid\n5.   If target < arr[mid], search left half\n6.   Else search right half\n7. Return -1 if not found',
                'common_mistakes': 'Off-by-one errors in boundaries, integer overflow in mid calculation, not handling duplicates, using binary search on unsorted data',
                'example_code': 'while left <= right:\n    mid = left + (right - left) // 2\n    if arr[mid] == target: return mid\n    elif arr[mid] < target: left = mid + 1\n    else: right = mid - 1',
                'syntax_structure': 'Requirement: Monotonic/Sorted Space\nPattern: Loop with [L, R] bounds updates'
            },
            'general': {
                'concept': 'Data Structures & Algorithms form the foundation of efficient problem-solving. Choose the right data structure for O(1) or O(log n) operations where possible.',
                'approach': 'Understand the problem constraints. Identify the bottleneck. Choose appropriate data structure. Consider time-space tradeoffs. Start with brute force, then optimize.',
                'pseudocode': '1. Clarify problem requirements and constraints\n2. Identify input/output format\n3. Consider edge cases\n4. Choose appropriate data structure\n5. Outline algorithm steps\n6. Analyze time and space complexity',
                'common_mistakes': 'Premature optimization, not considering edge cases, poor variable naming, not testing with examples, ignoring time/space complexity',
                'example_code': 'def solve():\n    # 1. Inputs\n    # 2. Process\n    # 3. Output',
                'syntax_structure': 'Standard Lib Types: List, Set, Map, Queue, Stack\nControl Flow: Loops, Conditions, Recursion'
            }
        }
    
    # ========== OS Knowledge Base ==========
    
    def _build_os_knowledge(self) -> Dict[str, Dict[str, str]]:
        """Build comprehensive OS knowledge base."""
        return {
            'deadlock': {
                'concept': 'Deadlock occurs when processes wait indefinitely for resources held by each other. Four necessary conditions: mutual exclusion, hold and wait, no preemption, circular wait.',
                'approach': 'To prevent deadlock, break at least one of the four conditions. Common strategies: resource ordering (break circular wait), timeouts, banker\'s algorithm for safe states.',
                'pseudocode': '1. Identify all resources and processes\n2. Create resource allocation graph\n3. Check for cycles in the graph\n4. If cycle exists, deadlock is possible\n5. Apply prevention: order resources, use timeouts, or allow preemption',
                'common_mistakes': 'Thinking all four conditions together cause deadlock (they must ALL be present), confusing deadlock with starvation, not considering livelock scenarios',
                'example_code': '// Circular Wait Risk\npthread_mutex_lock(&m1);\npthread_mutex_lock(&m2);\n// ... critical section ...\n\n// Prevention: Always lock in same order (m1 then m2)',
                'syntax_structure': 'Resource Allocation Graph: Process -> Resource (Request), Resource -> Process (Hold)\nSafety Alg: Banker\'s Algorithm'
            },
            'process_scheduling': {
                'concept': 'CPU scheduling determines which process runs next. Algorithms: FCFS, SJF, Round Robin, Priority. Metrics: turnaround time, waiting time, response time, throughput.',
                'approach': 'Choose algorithm based on goals: FCFS for simplicity, SJF for minimal average waiting, Round Robin for fairness, Priority for importance-based scheduling.',
                'pseudocode': '1. Maintain ready queue of processes\n2. Select process based on scheduling algorithm\n3. Allocate CPU to selected process\n4. If time quantum expires (Round Robin), preempt\n5. Move completed processes to done queue\n6. Repeat until all processes complete',
                'common_mistakes': 'Confusing arrival time with burst time, not considering context switch overhead, forgetting that SJF can cause starvation, not handling priority inversion',
                'example_code': '// FCFS Queue (FIFO)\nstruct Process { int id; int burst_time; };\nqueue<Process> ready_queue;\n\n// Round Robin\nwhile(!ready_queue.empty()) {\n  Process p = ready_queue.front();\n  run_for_quantum(p);\n}',
                'syntax_structure': 'PCB (Process Control Block): State, PID, PC, Registers\nContext Switch: Save State -> Load State'
            },
            'memory_management': {
                'concept': 'Memory management handles allocation and deallocation. Techniques: paging (fixed-size), segmentation (variable-size), virtual memory. Page replacement: FIFO, LRU, Optimal.',
                'approach': 'For page replacement, LRU approximates optimal but needs tracking. FIFO is simple but suffers from Belady\'s anomaly. Consider working set for thrashing prevention.',
                'pseudocode': '1. On page fault, check if free frame exists\n2. If yes, load page into free frame\n3. If no, select victim page using replacement algorithm\n4. If victim is dirty, write back to disk\n5. Load new page into frame\n6. Update page table',
                'common_mistakes': 'Confusing logical and physical addresses, not understanding TLB role, thinking more frames always reduces page faults (Belady\'s anomaly), ignoring thrashing',
                'example_code': '// Page Table Entry Concept\nstruct PTE {\n  int frame_number;\n  bool valid;\n  bool dirty;\n};\n\n// Translation\nphysical_addr = (frame_num * page_size) + offset;',
                'syntax_structure': 'Logical Addr -> MMU -> Physical Addr\nComponents: TLB, Page Table, Frame, Page'
            },
            'synchronization': {
                'concept': 'Synchronization coordinates concurrent processes. Mechanisms: semaphores, mutexes, monitors, condition variables. Critical section problem requires mutual exclusion, progress, bounded waiting.',
                'approach': 'Use mutex for simple mutual exclusion. Semaphores for counting resources. Monitors for higher-level abstraction. Condition variables for waiting on specific conditions.',
                'pseudocode': '1. Acquire lock/semaphore before entering critical section\n2. Execute critical section code\n3. Release lock/semaphore after exiting\n4. For producer-consumer: use two semaphores (empty, full)\n5. Ensure no race conditions or deadlocks',
                'common_mistakes': 'Forgetting to release locks, using wrong semaphore type (binary vs counting), not handling spurious wakeups, creating race conditions in lock acquisition',
                'example_code': '// Mutex Lock\npthread_mutex_lock(&mutex);\ncritical_section();\npthread_mutex_unlock(&mutex);\n\n// Semaphore\nsem_wait(&sem); // Decrement\naccess_resource();\nsem_post(&sem); // Increment',
                'syntax_structure': 'Mutex: Lock(), Unlock()\nSemaphore: Wait() -> P(), Signal() -> V()\nMonitor: Condition Variables (Wait, Signal)'
            },
            'general': {
                'concept': 'Operating Systems manage hardware resources and provide abstraction for applications. Core concepts: processes, threads, memory, I/O, file systems, security.',
                'approach': 'Understand the problem in terms of OS primitives. Consider concurrency issues. Think about resource allocation and scheduling. Analyze tradeoffs between performance and fairness.',
                'pseudocode': '1. Identify OS component involved (process, memory, I/O)\n2. Understand the problem constraints\n3. Consider concurrency and synchronization needs\n4. Choose appropriate OS mechanism\n5. Analyze for deadlocks, race conditions, starvation',
                'common_mistakes': 'Confusing processes and threads, not considering context switch costs, ignoring kernel vs user mode differences, oversimplifying concurrency issues',
                'example_code': '#include <unistd.h>\n\nint main() {\n  if (fork() == 0) {\n    // Child Process\n  } else {\n    // Parent Process\n  }\n}',
                'syntax_structure': 'System Calls: fork(), exec(), wait(), exit()\nKernel Space vs User Space'
            },
        }
    
    # ========== DBMS Knowledge Base ==========
    
    def _build_dbms_knowledge(self) -> Dict[str, Dict[str, str]]:
        """Build comprehensive DBMS knowledge base."""
        return {
            'normalization': {
                'concept': 'Normalization reduces redundancy and anomalies. Forms: 1NF (atomic values), 2NF (no partial dependencies), 3NF (no transitive dependencies), BCNF (every determinant is candidate key).',
                'approach': 'Start with unnormalized data. Apply 1NF: ensure atomic values. Apply 2NF: remove partial dependencies. Apply 3NF: remove transitive dependencies. Consider denormalization for performance.',
                'pseudocode': '1. Identify all functional dependencies\n2. Ensure all attributes are atomic (1NF)\n3. Remove partial dependencies on candidate keys (2NF)\n4. Remove transitive dependencies (3NF)\n5. Verify every determinant is a candidate key (BCNF)\n6. Split tables as needed',
                'common_mistakes': 'Over-normalizing leading to too many joins, not identifying all functional dependencies, confusing 3NF and BCNF, forgetting that normalization can hurt read performance',
                'example_code': '-- Unnormalized\nStudent(ID, Name, Course, Instructor)\n\n-- Normalized (3NF)\nStudent(ID, Name)\nCourse(Code, Instructor)\nEnrollment(StudentID, CourseCode)',
                'syntax_structure': 'Keys: Primary (PK), Foreign (FK), Candidate\nFunctional Dependency: X -> Y'
            },
            'transactions': {
                'concept': 'Transactions ensure ACID properties: Atomicity (all or nothing), Consistency (valid state), Isolation (concurrent execution appears serial), Durability (committed changes persist).',
                'approach': 'Use appropriate isolation level: Read Uncommitted, Read Committed, Repeatable Read, Serializable. Higher isolation reduces concurrency anomalies but impacts performance.',
                'pseudocode': '1. BEGIN TRANSACTION\n2. Execute SQL operations\n3. Check for conflicts/errors\n4. If all successful, COMMIT\n5. If any failure, ROLLBACK\n6. Ensure logs are written before commit',
                'common_mistakes': 'Not handling rollback scenarios, choosing wrong isolation level, ignoring phantom reads, not considering deadlock possibilities in transactions',
                'example_code': 'BEGIN TRANSACTION;\nUPDATE Accounts SET bal = bal - 100 WHERE id = 1;\nUPDATE Accounts SET bal = bal + 100 WHERE id = 2;\nCOMMIT;',
                'syntax_structure': 'SQL: START TRANSACTION / BEGIN -> COMMIT / ROLLBACK\nLevels: READ UNCOMMITTED -> SERIALIZABLE'
            },
            'indexing': {
                'concept': 'Indexes speed up queries but slow down writes. Types: B-tree (range queries), Hash (equality), Bitmap (low cardinality). Clustered index determines physical order.',
                'approach': 'Index columns used in WHERE, JOIN, ORDER BY. Avoid over-indexing. Consider composite indexes for multi-column queries. Analyze query patterns before creating indexes.',
                'pseudocode': '1. Identify frequently queried columns\n2. Analyze query patterns (equality vs range)\n3. Create appropriate index type\n4. For composite index, order columns by selectivity\n5. Monitor index usage and maintenance overhead\n6. Drop unused indexes',
                'common_mistakes': 'Creating too many indexes, wrong column order in composite indexes, not considering write overhead, indexing low-cardinality columns, forgetting index maintenance',
                'example_code': '-- Single Column Index\nCREATE INDEX idx_email ON Users(email);\n\n-- Composite Index\nCREATE INDEX idx_name_age ON Users(lastname, age);',
                'syntax_structure': 'DDL: CREATE [UNIQUE] INDEX name ON table(cols);\nStructure: B+ Tree (Root, Internal, Leaf)'
            },
            'joins': {
                'concept': 'Joins combine rows from multiple tables. Types: INNER (matching rows), LEFT/RIGHT (all from one table), FULL OUTER (all rows), CROSS (cartesian product). Join algorithms: nested loop, hash, merge.',
                'approach': 'Choose join type based on requirements. Use INNER for matching data only. LEFT/RIGHT when you need all rows from one table. Ensure join columns are indexed.',
                'pseudocode': '1. Identify tables to join\n2. Determine join condition (ON clause)\n3. Choose join type (INNER, LEFT, RIGHT, FULL)\n4. Optimizer selects join algorithm\n5. Result combines columns from both tables\n6. Apply WHERE filters after join',
                'common_mistakes': 'Confusing LEFT and RIGHT joins, not understanding NULL behavior in OUTER joins, creating cartesian products accidentally, joining on non-indexed columns',
                'example_code': 'SELECT u.name, o.id\nFROM Users u\nJOIN Orders o ON u.id = o.user_id\nWHERE o.total > 100;',
                'syntax_structure': 'SQL: FROM T1 JOIN T2 ON T1.col = T2.col\nTypes: INNER, LEFT, RIGHT, FULL, CROSS'
            },
            'query_optimization': {
                'concept': 'Query optimization improves performance. Techniques: use indexes, avoid SELECT *, minimize subqueries, use EXPLAIN, consider query rewriting, analyze execution plans.',
                'approach': 'Start with EXPLAIN to see execution plan. Identify full table scans. Add indexes where needed. Rewrite subqueries as joins when possible. Use appropriate join order.',
                'pseudocode': '1. Run EXPLAIN on query\n2. Identify bottlenecks (table scans, sorts)\n3. Check if indexes are used\n4. Rewrite query if needed (subquery to join)\n5. Consider denormalization for read-heavy workloads\n6. Verify improvement with EXPLAIN',
                'common_mistakes': 'Using SELECT * instead of specific columns, not using EXPLAIN, ignoring index hints, premature optimization, not considering data distribution',
                'example_code': '-- Before\nSELECT * FROM Users WHERE YEAR(created_at) = 2023;\n\n-- After (SARGable)\nSELECT id, name FROM Users WHERE created_at >= \'2023-01-01\' AND created_at < \'2024-01-01\';',
                'syntax_structure': 'Command: EXPLAIN [ANALYZE] SELECT ...\nGoal: Reduce Cost, Minimize I/O'
            },
            'general': {
                'concept': 'Database Management Systems store, retrieve, and manage data efficiently. Core concepts: relational model, SQL, transactions, concurrency control, recovery, indexing.',
                'approach': 'Understand data relationships. Design schema with normalization in mind. Use appropriate constraints. Consider query patterns when designing indexes. Balance normalization with performance.',
                'pseudocode': '1. Analyze data requirements\n2. Design schema with entities and relationships\n3. Apply normalization to reduce redundancy\n4. Define constraints (primary key, foreign key, unique)\n5. Create indexes based on query patterns\n6. Test with realistic data volumes',
                'common_mistakes': 'Poor schema design, not using foreign keys, ignoring data integrity, over/under normalization, not planning for scale, ignoring backup and recovery',
                'example_code': 'CREATE TABLE Users (\n    id INT PRIMARY KEY,\n    email VARCHAR(255) UNIQUE,\n    created_at TIMESTAMP\n);',
                'syntax_structure': 'SQL Groups: DDL (Create/Alter), DML (Select/Insert), DCL (Grant/Revoke), TCL (Commit/Rollback)'
            }
        }
