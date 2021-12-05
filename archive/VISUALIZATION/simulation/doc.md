# DOCUMENTATION

### Directory structure

```
/param
├── projects
│   ├── project1
│   │  ├── project1.sqlite
│   │  ├── main.py
│   │  ├── components.py
│   │  └── experiments
│   │         ├── doe1.json
│   │         ├── doe2.json
│   │         └── doe3.json
│   ├── project2
│   └── project3
├── backend
│   ├── doe.py
│   └── system.py
└── frontend
    ├── home.py
    ├── database.py - pkg
    ├── paramexp.py
    └── dataviz.py
    
```

### TODO
* feed data into sqlite database

### TECH STACK
* sqlite browser - https://github.com/coleifer/sqlite-web

### Big Decisions
Remove all dictionaries and convert standard into single data values? output_probabilities_a, etc.

### Structure
* in processing data handling - pandas dataframe
* database - SQLite
* frontend and backend - Dash UI
  * call in functions in dash.py to run simulations

### UI Inputs
**DOE**
* Options: full factorial, fractional factorial, custom
* Define: factors, levels


### References
1. [DOE - JMP](https://www.jmp.com/en_hk/statistics-knowledge-portal/what-is-design-of-experiments/types-of-design-of-experiments.html)
2. [Fractional Factorial Designs - Summary, NIST](https://www.itl.nist.gov/div898/handbook/pri/section3/pri3347.htm)
3. [Guide on Fractional Factorial Desings - AFIT](https://www.afit.edu/stat/statcoe_files/Classical%20Designs-Fractional%20Fractorial%20Designs%20Rev1.pdf)