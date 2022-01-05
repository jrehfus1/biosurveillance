"""
created: 2022-01-05
author: JER
this script is useful for adding fake information to real hits data.
"""
import numpy as np

# specify the number of samples to generate
N_SAMPS = 5

# use a seed for reproducibility
np.random.seed(0)

# specify the possible sample types
TYPE_OPTIONS = ['control', 'environmental', 'livestock', 'human']
TYPE_PROBS = [0.10, 0.15, 0.50, 0.25]

# specify the possible number of days between sample collection and submission
DELAY_OPTIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
DELAY_PROBS = [0.01, 0.01, 0.02, 0.02, 0.02, 0.05, 0.15, 0.50, 0.15, 0.05, 0.02]

# specify the possible sample locations
STATE_OPTIONS = ['CA', 'FL', 'KY', 'LA', 'MD', 'WI']
COUNTY_OPTIONS = {'CA': ['San Bernandino', 'Los Angeles', 'Riverside', 'Santa Clara', 'San Diego'],
                  'FL': ['Duval', 'St. Johns', 'Dade', 'Walton', 'Sarasota'],
                  'KY': ['Kenton', 'Boone', 'Fayette', 'Jefferson', 'Bullitt'],
                  'LA': ['Monroe', 'Orleans', 'Jackson', 'Grant', 'Beauregard'],
                  'MD': ['Baltimore City', 'Baltimore', 'Anne Arundel', "Queen Anne's", 'Frederick'],
                  'WI': ['Brown', 'Milwaukee', 'Dane', 'Racine', 'Kenosha']}

# get sample types
SAMP_TYPES = np.random.choice(TYPE_OPTIONS, size=N_SAMPS, p=TYPE_PROBS)
print(SAMP_TYPES)

# get sample collection delays
SAMP_DELAYS = np.random.choice(DELAY_OPTIONS, size=N_SAMPS, p=DELAY_PROBS)
print(SAMP_DELAYS)

# get sample locations
SAMP_STATES = np.random.choice(STATE_OPTIONS, size=N_SAMPS, p=None)
print(SAMP_STATES)

for state in STATE_OPTIONS:
    # N_COUNTIES = SAMP_STATES.count(state)
    N_COUNTIES = np.count_nonzero(SAMP_STATES == state)
    STATE_COUNTIES = np.random.choice(COUNTY_OPTIONS[state], size=N_COUNTIES,
                                      p=None)
print(STATE_COUNTIES)
