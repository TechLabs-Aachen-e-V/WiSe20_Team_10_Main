# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ## Cleaning scraped game data
#
# Here we show how to use the data obtained with Scrapy. In order to use it for data analysis and game outcome predictions, we first need to clean the data. 
#
# Let's start with importing the packages we'll use:

import pandas as pd # Dataframes
import numpy as np # number crunching, matrices and all that

# Let's now import the scraped data and perform a first simple cleaning step:
# 1. We import the `.csv` file to a pandas data frame.
# 2. There are games that were scraped multiple times because multiple of the selected top players were involved in them (a game might pop up in our data up to 10 times because of this). As these duplicates would skew the statistics, we remove them via `drop_duplicates`, using the starting time (`timestamp`) and the duration (`duration`) as unique identifiers.
# 3. We reset the index of the data frame, which can be done explicitly (see commented line) or implicitly when removing duplicates via `ignore_index=True`.

df = pd.read_csv('../data/raw/games.csv')
df.drop_duplicates(subset=['duration', 'timestamp', 'team_1', 'team_2', 'winner'], inplace=True, keep='first', ignore_index=True)
# df.reset_index(drop=True, inplace=True)
print(len(df))
df.head()

# As we can see in the print-out of the data frame head above, we now have unique games in `df`, with the columns `duration`, `server`, `summoner_name`, `team_1`, `team_2`, `timestamp` and `winner`. We will usually discard the server, player (summoner) and time information in our analysis.
#
# In order to capture the roles of the played champions, which currently is implicitly stored in their order in `team_1` and `team_2`, we create 10 new columns - 5 for the red and blue team each - and store the champions individually:

# These are the roles, in the same order as they are stored in team_1 and team_2.
roles = ['Top', 'Jng', 'Mid', 'Adc', 'Sup']
# For both teams...
for team_color, team_attr in zip(['B', 'R'], ['team_1', 'team_2']):
    # ...decompose the column in a data frame of champion names...
    team = df[team_attr].str.split(',', expand=True)
    # ...and for all 5 roles, store the role column in the corresponding column of df.
    for i, role in enumerate(roles):
        df[f"{team_color}{role}"] = team[i]
df.drop(columns=['team_1', 'team_2'], inplace=True)

# _Note on performance_: The above splitting of `team_1` and `team_2` is done for the entire data frame "at once" as we are using an internal pandas function (`pd.Series.str.split`) and then assign the full columns to the new role columns `BTop`, `BJng`... of `df`.
#
# Let's now rewrite the `winner` column to use `'Blue'` and `'Red'` instead of `'Team 1'` and `'Team 2'`, and drop the above mentioned columns of information we do not take into account.
#
# We also already can do a first step of data analysis and consider some stats:

df['winner'] = df.apply(lambda x: 'Blue' if x.winner=='Team 1' else 'Red', axis=1)
df.drop(['server', 'summoner_name', 'duration', 'timestamp'],axis=1,inplace=True)
# Some statistics:
num_games = len(df)   # Total number of games
num_blue_wins = len(df[df['winner']=='Blue'])     # No of games blue won
num_red_wins = len(df[df['winner']=='Red'])      # No of games red won
assert num_red_wins + num_blue_wins == num_games # Make sure we do not have a bad row without winner or such.
blue_winrate = num_blue_wins/num_games
red_winrate = num_red_wins/num_games
print(f"There are {num_games} games recorded, the blue team won {num_blue_wins},",
      f"the red team won {num_red_wins} of these games.",
      f"\nThis yields win rates of {blue_winrate*100:.2f}% (blue) and {red_winrate*100:.2f}% (red).")

# ### Looking at the champion stats
# Now we will prepare a second important data frame using the data above: The statistics per champion.
# To get the unique champion names, let's use `np.unique` on all role columns in `df`.

Blue = [f'B{role}' for role in roles]
Red = [f'R{role}' for role in roles]
champions = np.unique(df[Blue+Red])
# cd = pd.DataFrame(champions, columns=['Champion'])

# Now we compute the statistics per champion.
#
# In order to speed up the process by using `dict` lookups (which are very fast), we will not do the following steps in the `cd` data frame directly but make use of four separate dictionaries that capture the numbers of games/wins on the blue/red side for each champion. We also memorize the roles that the champions were played in, using a `dict` with `dict`s as values.
#
# To actually count the values we are interested in, we iterate over the data frame of games `df` _once_. For each row, we iterate over the roles and add to the counters in `blue_played` and `red_played` for the champions played on the respective side. We also memorize the role that each champion was played in. In order to count the wins on either side, we make use of python's automatic type casting and add the boolean `winner_is_blue`/`winner_is_red` to the counters in `blue_won` and `red_won`.

# +
blue_played = {champ: 0 for champ in champions}
blue_won = {champ: 0 for champ in champions}
red_played = {champ: 0 for champ in champions}
red_won = {champ: 0 for champ in champions}
roles_played = {champ: {role: 0 for role in roles} for champ in champions}

for _, row in df.iterrows():
    winner_is_blue = row.winner=='Blue'
    winner_is_red = not winner_is_blue
    for blue_role in Blue:
        champ = row[blue_role]
        blue_played[champ] += 1
        blue_won[champ] += winner_is_blue
        # Strip the "B"/"R" from blue_role to get the role
        roles_played[champ][blue_role[1:]] += 1
    for red_role in Red:
        champ = row[red_role]
        red_played[champ] += 1
        red_won[champ] += winner_is_red
        roles_played[champ][red_role[1:]] += 1
# -

# Before storing everything in a data frame, let's figure out which were the most played roles per champion. For this, we iterate over the champions and sort the roles by their occurences for each champion. The `number_of_roles_to_record` most played roles and their counters are then stored in individual lists and linked to keys, for example `"Role1"` and `"#Role1"`, in a dictionary:

# +
number_of_roles_to_record = 2 # We use 2 roles, could use up to all 5
ordered_roles_played = [[] for _ in range(number_of_roles_to_record)]
numbers_roles_played = [[] for _ in range(number_of_roles_to_record)]
for i, champ in enumerate(champions):
    # This is a list of tuples (role, #plays in the role):
    roles_for_this_champ = list(roles_played[champ].items()) 
    # sort by number of plays, in descending order (reverse=True)
    sorted_roles_for_this_champ = sorted(roles_for_this_champ, key=lambda x: x[1], reverse=True)
    
    # Now let's record the sorted tuples as order of most played roles (and their # of plays) 
    for j in range(number_of_roles_to_record):
        ordered_roles_played[j].append(sorted_roles_for_this_champ[j][0]) # Record the role
        numbers_roles_played[j].append(sorted_roles_for_this_champ[j][1]) # Record the # of plays
        
most_played_roles = {f"Role{j+1}": ordered_roles_played[j] for j in range(number_of_roles_to_record)}
most_played_numbers = {f"#Role{j+1}": numbers_roles_played[j] for j in range(number_of_roles_to_record)}
# -

# Having all statistics sorted out, we can wrap everything up in a data frame. Because of the way we stored the most played roles above, we have a flexible pipeline that will generate the data frame for any number of most-played roles we want to store per champion.

cd = pd.DataFrame({
    'Champion': champions,
    'BluePlayed': [blue_played[champ] for champ in champions],
    'BlueWon': [blue_won[champ] for champ in champions],
    'RedPlayed': [red_played[champ] for champ in champions],
    'RedWon': [red_won[champ] for champ in champions],
    **most_played_roles,
    **most_played_numbers,
})

# We conclude the first round of data analysis by computing the total number of games played and the win rate on either side as well as in total, for each champion. For this, the column-wise operations on a data frame are very handy:

cd['TotalPlayed'] = cd['BluePlayed'] + cd['RedPlayed']
cd['Bluewinrate'] = cd['BlueWon'] / cd['BluePlayed']
cd['Redwinrate'] = cd['RedWon'] / cd['RedPlayed']
cd['Totalwinrate'] = (cd['BlueWon'] + cd['RedWon']) / cd['TotalPlayed']

# The resulting data frame looks like this:

# cd

# For other parts of the project we will want to come back to this data. Let's store it in a new `.csv` file.

cd.to_csv('../data/processed/ChampionStatsDemo.csv',index=False)


