from statsbombpy import sb
import pandas as pd
import warnings

warnings.filterwarnings('ignore', message='credentials were not supplied')

def extract_master_scouting_data():
    print("Fetching 2022 World Cup matches...")
    matches = sb.matches(competition_id=43, season_id=106)
    match_ids = matches['match_id'].tolist()

    player_stats = {}

    print(f"Processing {len(match_ids)} matches. This will take 1-2 minutes...")

    for idx, mid in enumerate(match_ids):
        if idx % 10 == 0:
            print(f"Processed {idx} / {len(match_ids)} matches...")
            
        try:
            events = sb.events(match_id=mid)
            if 'type' not in events.columns or 'pass_end_location' not in events.columns:
                continue

            # We only want successful passes
            passes = events[(events['type'] == 'Pass') & (events['pass_outcome'].isnull())].copy()
            
            # Extract coordinates
            passes[['start_x', 'start_y']] = pd.DataFrame(passes['location'].tolist(), index=passes.index)
            passes[['end_x', 'end_y']] = pd.DataFrame(passes['pass_end_location'].tolist(), index=passes.index)
            
            # Metrics logic
            passes['vertical_yards'] = passes['end_x'] - passes['start_x']
            passes['is_progressive'] = passes['vertical_yards'] >= 15
            passes['is_final_third'] = (passes['start_x'] < 80) & (passes['end_x'] >= 80)
            passes['is_box'] = (passes['end_x'] >= 102) & (passes['end_y'] >= 18) & (passes['end_y'] <= 62)
            passes['is_key_pass'] = passes.get('pass_shot_assist', False) == True

            for _, row in passes.iterrows():
                player = row['player']
                if pd.isna(player): continue

                if player not in player_stats:
                    player_stats[player] = {
                        'player': player,
                        'team': row['team'],
                        'positions': [],
                        'matches': set(),
                        'total_passes': 0,
                        'progressive_passes': 0,
                        'final_third_passes': 0,
                        'box_passes': 0,
                        'key_passes': 0
                    }

                p_data = player_stats[player]
                p_data['matches'].add(mid)
                p_data['total_passes'] += 1
                if row['is_progressive']: p_data['progressive_passes'] += 1
                if row['is_final_third']: p_data['final_third_passes'] += 1
                if row['is_box']: p_data['box_passes'] += 1
                if row['is_key_pass']: p_data['key_passes'] += 1
                
                # Track position to find their primary role later
                if pd.notna(row.get('position')):
                    p_data['positions'].append(row['position'])

        except Exception as e:
            pass 

    # Compile final dataframe
    final_data = []
    for player, data in player_stats.items():
        if data['total_passes'] >= 100: # Filter out players with very few minutes
            # Calculate primary position (most common position played)
            primary_pos = pd.Series(data['positions']).mode()[0] if data['positions'] else 'Unknown'
            
            matches_played = len(data['matches'])
            
            final_data.append({
                'player': player,
                'team': data['team'],
                'primary_position': primary_pos,
                'matches_played': matches_played,
                'passes_per_match': round(data['total_passes'] / matches_played, 1),
                'progression_rate_pct': round((data['progressive_passes'] / data['total_passes']) * 100, 2),
                'final_third_per_match': round(data['final_third_passes'] / matches_played, 2),
                'box_passes_per_match': round(data['box_passes'] / matches_played, 2),
                'key_passes_per_match': round(data['key_passes'] / matches_played, 2)
            })

    df = pd.DataFrame(final_data)
    df.to_csv('master_player_scouting.csv', index=False)
    print("\nExtraction complete! Saved to master_player_scouting.csv")

if __name__ == '__main__':
    extract_master_scouting_data()