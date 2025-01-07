import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from make_court.make_court import shot_chart

from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail, playercareerstats

def get_player_shotchart_details(player_name, season_id):
    all_players = players.get_players()
    player_id = next((player['id'] for player in all_players if player['full_name'] == player_name), None)
    
    if not player_id:
        print(f"Player '{player_name}' not found.")
        return
    
    career_df = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
    team_id = career_df.loc[career_df['SEASON_ID'] == season_id, 'TEAM_ID'].values[0]
    player_fg_pct = float(career_df[career_df['SEASON_ID'] == season_id]['FG_PCT'].iloc[0])
    shotchart = shotchartdetail.ShotChartDetail(player_id=player_id, 
                                                team_id=team_id, 
                                                season_nullable=season_id,
                                                season_type_all_star='Regular Season',
                                                context_measure_simple='FGA')
    return player_fg_pct,shotchart.get_data_frames()[0], shotchart.get_data_frames()[1]

def get_player_shotchart(shotchart_data, player_fg_pct, player_name, season_id):
    plt.figure(figsize=(8, 7))
    shot_chart(shotchart_data, player_fg_pct, title=f"{player_name} Shot Chart {season_id}")
    
    # Create the output directory if it doesn't exist
    output_dir = 'static'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the file in the nba-shot-chart directory
    output_path = os.path.join(output_dir, 'shot_chart.png')
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == "__main__":
    try:
        player_name = input("Enter player name (default: Kyrie Irving): ") or "Kyrie Irving"
        season_id = input("Enter season (format YYYY-YY, default: 2024-25): ") or "2024-25"
        
        player_fg_pct, shotchart_data, league_avg_data = get_player_shotchart_details(player_name, season_id)
        
        if shotchart_data.empty:
            raise ValueError(f"No data found for {player_name} in season {season_id}")
            
        get_player_shotchart(shotchart_data, player_fg_pct, player_name, season_id)
        print(f"Shot chart generated for {player_name} ({season_id})")
        
    except Exception as e:
        print(f"Error: {str(e)}")
   
    


