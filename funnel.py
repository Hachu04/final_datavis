import pandas as pd

def generate_midfield_funnel():
    # 1. Load the two datasets extracted from StatsBomb
    master = pd.read_csv('master_player_scouting.csv')
    risk = pd.read_csv('act1_risk_reward_scouting.csv')

    # 2. Standardize names to merge successfully (Risk dataset uses simplified names)
    def simplify_name(n):
        n = str(n).lower()
        replacements = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ć': 'c', 'ñ': 'n'}
        for k, v in replacements.items():
            n = n.replace(k, v)
        return n.split(' ')[-1] # Match on last name

    master['match_name'] = master['player'].apply(simplify_name)
    risk['match_name'] = risk['player'].apply(simplify_name)

    # 3. Merge to combine Accuracy metrics with Pitch Zone metrics
    df = pd.merge(
        master, 
        risk[['match_name', 'team', 'attempted_passes', 'completion_pct', 'prog_per_match']], 
        on=['match_name', 'team'], 
        how='inner'
    )

    # 4. Filter strictly for Midfielders
    df = df[df['primary_position'].str.contains('Midfield', na=False)]

    # Save the consolidated data
    df.to_csv('final_midfield_funnel.csv', index=False)
    print(f"Successfully generated funnel data for {len(df)} midfielders.")

if __name__ == '__main__':
    generate_midfield_funnel()