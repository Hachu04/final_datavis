from statsbombpy import sb
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore', message='credentials were not supplied')

def extract_final_sonars():
    print("Fetching 2022 World Cup matches...")
    matches = sb.matches(competition_id=43, season_id=106)
    match_ids = matches['match_id'].tolist()

    # The 4 Elite Finalists from our Funnel
    finalists = [
        'Pedro González López', 
        'Joshua Kimmich', 
        'Christian Dannemann Eriksen', 
        'Luka Modrić'
    ]
    
    sonar_data = []

    print(f"Processing matches for the Final 4. This will take 1-2 minutes...")

    for mid in match_ids:
        try:
            events = sb.events(match_id=mid)
            if 'type' not in events.columns or 'pass_end_location' not in events.columns:
                continue

            passes = events[(events['type'] == 'Pass') & (events['pass_outcome'].isnull())].copy()
            target_passes = passes[passes['player'].isin(finalists)]
            
            for _, row in target_passes.iterrows():
                # Simplify names for the D3 visualization
                name = row['player']
                if 'Pedro' in name: name = 'Pedri'
                if 'Christian' in name: name = 'Eriksen'
                if 'Joshua' in name: name = 'Kimmich'
                if 'Luka' in name: name = 'Modrić'

                sonar_data.append({
                    'player': name,
                    'angle': row['pass_angle'],
                    'length': row['pass_length']
                })
        except Exception as e:
            pass 

    df = pd.DataFrame(sonar_data)
    # Convert radians to degrees (StatsBomb 0 degrees is directly toward opponent goal)
    df['angle_degrees'] = df['angle'].apply(lambda x: np.degrees(x) % 360)
    
    df.to_csv('act3_final_sonars.csv', index=False)
    print(f"\nSuccess! Saved {len(df)} passes to act3_final_sonars.csv")

if __name__ == '__main__':
    extract_final_sonars()