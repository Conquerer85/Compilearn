# Compilearn

**[Live demo →](https://Conquerer85.github.io/compilearn)**

A single page that teaches how compilers work and where automata theory lives inside them. Nothing is pre-recorded — a real compiler runs in the browser, and two labs build the classical constructions live from whatever you type.

---

## What it does

| Section | What you can do |
|---|---|
| **Pipeline** | The six phases as a diagram — front end, middle end, back end, symbol table and error reporter |
| **Compile something** | Type source code; watch it become tokens → syntax tree → typed tree → IR → optimised IR → assembly |
| **Each phase** | Internal structure, data structures, what each phase uniquely catches |
| **Chomsky hierarchy** | Regular, context-free and context-sensitive mapped onto the phases |
| **Regex → NFA → DFA → minimal DFA** | Type a pattern; get Thompson's construction, the subset construction, partition refinement — every step drawn as a state diagram with its transition table |
| **Grammar lab** | Type a grammar; get LL(1), LR(0), SLR(1), LALR(1) and CLR(1) tables, item-set automata, conflict reports and a live parse trace |
| **Which parser** | Containment diagram and a card for each parsing method |

No framework. No build step. Plain HTML + CSS + JS.

---

## File structure

```
compilearn/
│
├── index.html               ← the whole page, just links to the files below
│
├── assets/
│   ├── favicon.svg
│   ├── css/
│   │   └── compilearn.css   ← design tokens, layout, light/dark themes
│   └── js/
│       ├── util.js          ← two shared helpers ($ and esc)
│       ├── compiler.js      ← scanner · parser · semantic analyser · IR · optimiser · codegen
│       ├── automata.js      ← regex parser · Thompson NFA · subset DFA · minimal DFA
│       ├── grammar.js       ← FIRST/FOLLOW · LR item sets · LALR merge · all five tables
│       └── ui.js            ← everything that touches the DOM
│
├── test/
│   └── run.js               ← 54 regression tests, no dependencies (node test/run.js)
│
├── build.py                 ← optional: bundles everything into one dist/compilearn.html
│
├── .github/
│   └── workflows/
│       ├── deploy.yml       ← publishes to GitHub Pages on every push to main
│       └── test.yml         ← runs the tests on every push and pull request
│
├── .gitignore
├── .nojekyll                ← tells Pages not to run Jekyll
└── LICENSE                  ← MIT
```


## Running locally

Open `index.html` directly in a browser — the `file://` protocol works because the scripts are plain `<script>` tags, not ES modules.

Or with a local server:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

### Tests

```bash
node test/run.js
```

54 assertions against results from the literature (Aho, Lam, Sethi & Ullman). No packages to install.

### Single-file build

```bash
python3 build.py
# → dist/compilearn.html  (~142 KB, all assets inlined)
```

Useful for sharing offline or embedding in a course. Not needed to run or deploy.

---

## The toy language

```
let x = 3 + 4 * 2;         // int declaration
let flag = x > 5;           // bool declaration
print x;                    // print statement
if (flag) { print 1; }      // if / else
while (x > 0) { x = x - 1; print x; }   // while
```

Types: `int` and `bool`. `//` comments. Errors from all three front-end phases are reported with line and column; one mistake does not cascade into fifty.

## Writing grammars in the lab

```
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
```

- `->`, `→` and `::=` all work as the arrow
- `|` separates alternatives
- Symbols are whitespace-separated, so multi-character terminals (`id`, `else`) work
- `ε`, `epsilon`, `''` or `#` means the empty production
- First left-hand side is the start symbol
- Input strings to parse must be space-separated (`id + id * id`)

---

## License

MIT — see [LICENSE](LICENSE).  
The page loads IBM Plex Sans, Serif and Mono from Google Fonts (SIL Open Font License).  
Run `python3 build.py --no-fonts` to strip the external font request.
