from statsbombpy import sb
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore', message='credentials were not supplied')

def extract_advanced_risk_scouting():
    print("Fetching 2022 World Cup matches...")
    matches = sb.matches(competition_id=43, season_id=106)
    match_ids = matches['match_id'].tolist()

    player_stats = {}

    print(f"Processing {len(match_ids)} matches to calculate Completion vs Progression...")

    for idx, mid in enumerate(match_ids):
        if idx % 10 == 0:
            print(f"Processed {idx} / {len(match_ids)} matches...")
            
        try:
            events = sb.events(match_id=mid)
            if 'type' not in events.columns or 'pass_end_location' not in events.columns:
                continue

            # We want ALL passes to calculate completion rate
            passes = events[events['type'] == 'Pass'].copy()
            
            # A pass is successful if 'pass_outcome' is null
            passes['is_completed'] = passes['pass_outcome'].isnull()
            
            # Extract coordinates for calculating progression 
            # (Note: even incomplete passes have an intended end location)
            passes[['start_x', 'start_y']] = pd.DataFrame(passes['location'].tolist(), index=passes.index)
            passes[['end_x', 'end_y']] = pd.DataFrame(passes['pass_end_location'].tolist(), index=passes.index)
            
            # Vertical yards gained (Only counting successful progressive passes for the reward metric)
            passes['vertical_yards'] = passes['end_x'] - passes['start_x']
            passes['is_progressive_success'] = (passes['vertical_yards'] >= 15) & (passes['is_completed'])

            for _, row in passes.iterrows():
                player = row['player']
                if pd.isna(player): continue

                if player not in player_stats:
                    player_stats[player] = {
                        'player': player,
                        'team': row['team'],
                        'positions': [],
                        'matches': set(),
                        'attempted_passes': 0,
                        'completed_passes': 0,
                        'successful_progressions': 0,
                        'x_locations': [] # To filter out center backs
                    }

                p_data = player_stats[player]
                p_data['matches'].add(mid)
                p_data['attempted_passes'] += 1
                
                if row['is_completed']: 
                    p_data['completed_passes'] += 1
                if row['is_progressive_success']: 
                    p_data['successful_progressions'] += 1
                    
                if pd.notna(row.get('position')):
                    p_data['positions'].append(row['position'])
                    
                # Track starting position of passes to filter defenders
                p_data['x_locations'].append(row['start_x'])

        except Exception as e:
            pass 

    final_data = []
    for player, data in player_stats.items():
        # Minimum 150 attempted passes
        if data['attempted_passes'] >= 150: 
            avg_x_position = np.mean(data['x_locations'])
            
            # Filter out Center Backs (Avg X < 45) and Goalkeepers
            if avg_x_position > 45:
                matches_played = len(data['matches'])
                
                completion_pct = (data['completed_passes'] / data['attempted_passes']) * 100
                prog_per_match = data['successful_progressions'] / matches_played
                
                # Simplify names
                display_name = player.split(' ')[0] + ' ' + player.split(' ')[-1]
                if 'Enzo' in player: display_name = 'Enzo Fernandez'
                if 'Modri' in player: display_name = 'Luka Modric'
                if 'Kevin De Bruyne' in player: display_name = 'Kevin De Bruyne'
                
                primary_pos = pd.Series(data['positions']).mode()[0] if data['positions'] else 'Unknown'

                final_data.append({
                    'player': display_name,
                    'team': data['team'],
                    'primary_position': primary_pos,
                    'attempted_passes': data['attempted_passes'],
                    'completion_pct': round(completion_pct, 1),
                    'prog_per_match': round(prog_per_match, 2)
                })

    df = pd.DataFrame(final_data)
    df.to_csv('act1_risk_reward_scouting.csv', index=False)
    print("\nExtraction complete! Saved to act1_risk_reward_scouting.csv")

if __name__ == '__main__':
    extract_advanced_risk_scouting()