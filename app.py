from flask import Flask, request, jsonify, send_file
from nba_shotchart import get_player_shotchart_details, get_player_shotchart

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/shot_chart.png')
def serve_shot_chart():
    return send_file('shot_chart.png')

@app.route('/generate-shot-chart', methods=['POST'])
def generate_shot_chart():
    data = request.json
    player_name = data.get('playerName', 'Kyrie Irving')
    season_id = data.get('seasonId', '2024-25')
    shot_filter = data.get('filter', 'both')

    try:
        player_fg_pct, shotchart_data, league_avg_data = get_player_shotchart_details(player_name, season_id)
        
        if shotchart_data.empty:
            return jsonify({'error': f"No data found for {player_name} in season {season_id}"}), 404
        
        if shot_filter == 'made':
            shotchart_data = shotchart_data[shotchart_data['EVENT_TYPE'] == 'Made Shot']
        elif shot_filter == 'missed':
            shotchart_data = shotchart_data[shotchart_data['EVENT_TYPE'] == 'Missed Shot']
            
        get_player_shotchart(shotchart_data, player_fg_pct, player_name, season_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 

    """
npm init
npm install create-react-app
npx create-react-app myapp
    """