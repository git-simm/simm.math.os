"""Knowledge base: nodes, pyramid levels, search index for the number theory module."""

KNOWLEDGE_NODES = [
    {
        "id": "natural_numbers",
        "level": 1,
        "title": "Natural Numbers (N)",
        "icon": "1",
        "category": "Foundation",
        "definition": "N = {1, 2, 3, ...}  or  {0, 1, 2, ...}  — the counting numbers.",
        "principles": [
            "Closed under addition and multiplication.",
            "Well-ordering: every non-empty subset has a least element.",
        ],
        "examples": [
            {"title": "Peano axioms", "content": "0 in N; each n has a successor S(n); induction holds."},
        ],
        "links_to": ["Whole numbers", "Integers"],
        "color": "#06b6d4",
    },
    {
        "id": "integers",
        "level": 1,
        "title": "Integers (Z)",
        "icon": "Z",
        "category": "Foundation",
        "definition": "Z = {..., -3, -2, -1, 0, 1, 2, 3, ...} — natural numbers and their negatives.",
        "principles": [
            "Closed under addition, subtraction, multiplication.",
            "Ring structure: every a has additive inverse -a.",
        ],
        "examples": [
            {"title": "a + (-a) = 0", "content": "Additive identity: every integer has a negative counterpart."},
        ],
        "links_to": ["Natural numbers", "Rational numbers"],
        "color": "#06b6d4",
    },
    {
        "id": "rational_numbers",
        "level": 2,
        "title": "Rational Numbers (Q)",
        "icon": "a/b",
        "category": "Numbers",
        "definition": "Q = { p/q | p, q in Z, q != 0 }. Numbers expressible as a ratio of integers.",
        "principles": [
            "Dense: between any two rationals there is another rational.",
            "Decimal expansions are terminating or repeating.",
        ],
        "examples": [
            {"title": "1/3 = 0.333...", "content": "Repeating decimal, period 1."},
            {"title": "1/2 = 0.5", "content": "Terminating decimal."},
        ],
        "links_to": ["Integers", "Real numbers", "Irrational numbers"],
        "color": "#a855f7",
    },
    {
        "id": "irrational_numbers",
        "level": 2,
        "title": "Irrational Numbers",
        "icon": "sqrt(2)",
        "category": "Numbers",
        "definition": "Real numbers that cannot be expressed as p/q. Their decimal expansions are non-terminating and non-repeating.",
        "principles": [
            "sqrt(2) is irrational (first proven by Pythagoreans).",
            "pi and e are transcendental irrationals.",
        ],
        "examples": [
            {"title": "sqrt(2) proof", "content": "Assume sqrt(2)=p/q in lowest terms; then 2q^2=p^2, contradiction."},
        ],
        "links_to": ["Rational numbers", "Real numbers"],
        "color": "#a855f7",
    },
    {
        "id": "real_numbers",
        "level": 2,
        "title": "Real Numbers (R)",
        "icon": "R",
        "category": "Numbers",
        "definition": "R = Q union {irrationals}. A complete ordered field.",
        "principles": [
            "Completeness: every bounded set has a supremum.",
            "Dense ordering; uncountable (Cantor diagonal argument).",
        ],
        "examples": [
            {"title": "Dedekind cuts", "content": "Construction of reals from rationals."},
        ],
        "links_to": ["Rational numbers", "Complex numbers"],
        "color": "#a855f7",
    },
    {
        "id": "complex_numbers",
        "level": 3,
        "title": "Complex Numbers (C)",
        "icon": "i",
        "category": "Extension",
        "definition": "C = { a + bi | a,b in R, i^2 = -1 }. Algebraically closed field.",
        "principles": [
            "Fundamental theorem of algebra: every nth-degree polynomial has n complex roots.",
            "Geometric interpretation: Argand plane; modulus and argument.",
        ],
        "examples": [
            {"title": "i^2 = -1", "content": "Definition of the imaginary unit."},
            {"title": "e^(i*pi) = -1", "content": "Euler identity: e^(i*pi) + 1 = 0."},
        ],
        "links_to": ["Real numbers", "Polynomials"],
        "color": "#f59e0b",
    },
    {
        "id": "quadratic_formula",
        "level": 3,
        "title": "Quadratic Formula",
        "icon": "x=",
        "category": "Formula",
        "definition": "For ax^2 + bx + c = 0 (a != 0): x = (-b +- sqrt(b^2 - 4ac)) / (2a).",
        "principles": [
            "Derived by completing the square.",
            "Discriminant D = b^2 - 4ac: D>0 -> 2 real; D=0 -> 1 real; D<0 -> 2 complex conjugate.",
        ],
        "examples": [
            {"title": "x^2 - 5x + 6 = 0", "content": "x = (5 +- sqrt(25-24))/2 = (5 +- 1)/2 -> x=3 or x=2."},
        ],
        "links_to": ["Polynomials", "Complex numbers"],
        "color": "#f59e0b",
    },
    {
        "id": "discriminant",
        "level": 3,
        "title": "Discriminant",
        "icon": "Delta",
        "category": "Formula",
        "definition": "Delta = b^2 - 4ac determines the nature of roots of ax^2+bx+c=0.",
        "principles": [
            "Delta > 0: two distinct real roots.",
            "Delta = 0: one real root (double root).",
            "Delta < 0: two complex conjugate roots.",
        ],
        "examples": [
            {"title": "D=0 example", "content": "x^2 + 2x + 1 = 0 -> D=0 -> x = -1 (double root)."},
        ],
        "links_to": ["Quadratic formula", "Complex numbers"],
        "color": "#f59e0b",
    },
    {
        "id": "fundamental_theorem_algebra",
        "level": 4,
        "title": "Fundamental Theorem of Algebra",
        "icon": "deg=n",
        "category": "Theorem",
        "definition": "Every non-constant polynomial P(z) in C[z] of degree n has exactly n complex roots (counted with multiplicity).",
        "principles": [
            "Implies C is algebraically closed.",
            "Proved by Gauss (multiple proofs); Liouville theorem approach is common.",
        ],
        "examples": [
            {"title": "x^2 + 1", "content": "Has roots +-i in C, though no real roots."},
        ],
        "links_to": ["Complex numbers", "Polynomials"],
        "color": "#94a3b8",
    },
    {
        "id": "viets_formulas",
        "level": 4,
        "title": "Vieta Formulas",
        "icon": "sum/ prod",
        "category": "Theorem",
        "definition": "For ax^2+bx+c=0 with roots r1,r2: r1+r2=-b/a, r1*r2=c/a.",
        "principles": [
            "For degree n: sum of roots = -a_{n-1}/a_n; product = (-1)^n a_0/a_n.",
            "Relates coefficients to symmetric sums of roots.",
        ],
        "examples": [
            {"title": "x^2-5x+6", "content": "Roots 2 and 3. Check: 2+3=5=-(-5)/1; 2*3=6=6/1."},
        ],
        "links_to": ["Quadratic formula", "Symmetric polynomials"],
        "color": "#94a3b8",
    },
]

PYRAMID_LEVELS = {
    1: {"name": "Foundation", "descr": "Basic number sets and axioms"},
    2: {"name": "Number Types", "descr": "Rational, irrational, real numbers"},
    3: {"name": "Extensions & Formulas", "descr": "Complex numbers, quadratic formula"},
    4: {"name": "Advanced Theorems", "descr": "FTA, Vieta formulas"},
}

SEARCH_INDEX = [
    {"query": "natural numbers", "node_id": "natural_numbers"},
    {"query": "n", "node_id": "natural_numbers"},
    {"query": "integers", "node_id": "integers"},
    {"query": "z", "node_id": "integers"},
    {"query": "rational", "node_id": "rational_numbers"},
    {"query": "q", "node_id": "rational_numbers"},
    {"query": "irrational", "node_id": "irrational_numbers"},
    {"query": "sqrt2", "node_id": "irrational_numbers"},
    {"query": "real numbers", "node_id": "real_numbers"},
    {"query": "r", "node_id": "real_numbers"},
    {"query": "complex", "node_id": "complex_numbers"},
    {"query": "i^2=-1", "node_id": "complex_numbers"},
    {"query": "euler", "node_id": "complex_numbers"},
    {"query": "quadratic", "node_id": "quadratic_formula"},
    {"query": "roots", "node_id": "quadratic_formula"},
    {"query": "discriminant", "node_id": "discriminant"},
    {"query": "delta", "node_id": "discriminant"},
    {"query": "fta", "node_id": "fundamental_theorem_algebra"},
    {"query": "fundamental theorem", "node_id": "fundamental_theorem_algebra"},
    {"query": "vieta", "node_id": "viets_formulas"},
    {"query": "roots sum product", "node_id": "viets_formulas"},
]

HELP_TEXT = "Click any card to expand. Use search to filter. Toggle pyramid levels with the headers."
