from statsbombpy import sb
import pandas as pd
import warnings

warnings.filterwarnings('ignore', message='credentials were not supplied')

def extract_final_4_pitch_data():
    print("Fetching 2022 World Cup matches...")
    matches = sb.matches(competition_id=43, season_id=106)
    match_ids = matches['match_id'].tolist()

    finalists = [
        'Pedro González López', 
        'Joshua Kimmich', 
        'Christian Dannemann Eriksen', 
        'Luka Modrić'
    ]
    
    pitch_data = []

    print(f"Processing matches for the Final 4 Pitch Maps...")

    for mid in match_ids:
        try:
            events = sb.events(match_id=mid)
            if 'type' not in events.columns or 'pass_end_location' not in events.columns:
                continue

            passes = events[(events['type'] == 'Pass') & (events['pass_outcome'].isnull())].copy()
            target_passes = passes[passes['player'].isin(finalists)]
            
            # Extract coordinates
            target_passes[['start_x', 'start_y']] = pd.DataFrame(target_passes['location'].tolist(), index=target_passes.index)
            target_passes[['end_x', 'end_y']] = pd.DataFrame(target_passes['pass_end_location'].tolist(), index=target_passes.index)
            
            # Filter for "Threat Passes" (Progressive OR Final Third OR Box)
            for _, row in target_passes.iterrows():
                vertical_yards = row['end_x'] - row['start_x']
                is_prog = vertical_yards >= 15
                is_final_third = row['end_x'] >= 80 and row['start_x'] < 80
                is_box = row['end_x'] >= 102 and 18 <= row['end_y'] <= 62
                
                if is_prog or is_final_third or is_box:
                    name = row['player']
                    if 'Pedro' in name: name = 'Pedri'
                    if 'Christian' in name: name = 'Eriksen'
                    if 'Joshua' in name: name = 'Kimmich'
                    if 'Luka' in name: name = 'Modrić'

                    pitch_data.append({
                        'player': name,
                        'start_x': row['start_x'],
                        'start_y': row['start_y'],
                        'end_x': row['end_x'],
                        'end_y': row['end_y'],
                        'is_box': 1 if is_box else 0
                    })
        except Exception as e:
            pass 

    df = pd.DataFrame(pitch_data)
    df.to_csv('act3_pitch_passes.csv', index=False)
    print(f"\nSuccess! Saved {len(df)} threat passes to act3_pitch_passes.csv")

if __name__ == '__main__':
    extract_final_4_pitch_data()