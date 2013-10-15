Python - Programming for Scientists
===================================

Please Note: this syllabus is provisional and may change during the semester.

Duration: 14 weeks

Practice problem solutions are only given out on Friday evenings. You can
submit these via Gist and I will comment on them, but I will not grade them.

Problem Sets are graded and should be done individually. Total of 110 points
to be gained from problem sets, 60% required to pass, i.e. 66 points. Solutions
will be graded on correctness, readability, presentation, PEP8 compliance.

Week 1
------

- About the course
- What is Python?
- How to run Python code
- Numbers, Strings, Lists
- Control flow

Practice:
  - Write a script to find prime numbers
  - Write a script to find the Fibonnacci sequence

Week 2
------

- Functions and Modules
- PEP8 style guide

Practice:
  - Write a function to find the factorial of a number (and try doing it
    recursively)
  - Write functions to encode and decode strings using the Caesar shift
    (cryptography)

Week 3
------

- Tuples, booleans, and dictionaries
- Reading and writing files
- Introduction to os.path and glob

Practice:
  - Randomly sample normal numbers, make histogram, overplot gaussian
  - Sample values from a dice and make plot. Roll dice multiple times and
    demonstrate the central limit theorem.

Problem Set I (2 weeks):
  - Bio-informatics problem - fun with DNA. The idea is to read in a gene
    sequence, translate to amino acids, compare to a larger strand of DNA, etc.
    Good practice of using simple strings, functions, etc. on real scientific
    data (loosely based on
    http://www.cs.grinnell.edu/~rebelsky/ExBioPy/Projects/project-2.5.html)
    [requires basic Python, reading files, string matching, dictionaries]

Week 4
------

No formal lecture

Work on Problem Set I

HAND IN PROBLEM SET I

Week 5
------

- Introduction to Matplotlib
- Introduction to Numpy (including masking)
- Introduction to the IPython Notebook. From now on, all problem sets handed in
  via IPython notebook!

Practice:
  - Read in data of temperature in Munich vs time, make simple plot. The data
    includes bad values that need to be masked.
  - Monte-Carlo error propagation (gets tested in RV problem set later)

Problem Set II (3 weeks):
  - Kepler transit lightcurve lightcurve extraction/analysis
    [requires glob, files, numpy, plotting, fitting]

Week 6
------

- Reading and handling exceptions

Work on Problem Set II

Week 7
------

- Scipy (interpolation, integration, fitting)

Practice:
  - Fit the temperature in Munich vs time data with some functions.
  - Fit data showing radioactive decay (fitting for half-life)

Work on Problem Set II

HAND IN PROBLEM SET II

Week 8
------

- String formatting

Problem Set III (3 weeks):
  - Arctic ice maps (requires plotting, numpy, glob, string formatting)

Week 9
------

No formal lecture

Work on Problem Set III

Week 10
------

- A close look at memory management (reference vs copy)

Practice:
  - exercises to understand variable assignment

Work on Problem Set III

HAND IN PROBLEM SET III

Week 11
------

- Accessing remote resources

Practice:
  - Try and retrieve online data. Parse webpage and extract some data.

Problem Set IV (3 weeks):
  - 51Peg radial velocity curve analysis (Files, Numpy, Plotting, Fitting).
    Includes finding the folded RV curve, fitting this curve, then doing MC
    error propagation to get planet probability. Need to download the RV curve from the web directly.

Week 12
-------

No formal lecture

Work on Problem Set IV

Week 13
-------

No formal lecture

Work on Problem Set IV

HAND IN PROBLEM SET IV
  
Week 14
-------

- Object-oriented programming

Practice:
  - Write classes to represent various particles

Misc Resources
--------------

http://peak5390.wordpress.com/2013/09/22/how-ipython-notebook-and-github-have-changed-the-way-i-teach-python/

