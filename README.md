# Topsis-Naman-102316108
A command-line implementation of the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) multi-criteria decision-making method.

## Installation
```
pip install Topsis-Naman-102316108
```

## Usage
```
topsis <inputDataFile> <Weights> <Impacts> <OutputFile>
```

Example:
```
topsis data.csv "1,1,1,2" "+,+,-,+" result.csv
```

## Input File Requirements

- Must be in .csv format
- contain at least 3 columns
- Number of weights = number of impacts = number of criteria columns
- First column should contain alternatives (non-numeric allowed)
- From second column onward, all values must be numeric
- Impacts must be either '+' or '-'
- Weights and impacts must be comma separated
