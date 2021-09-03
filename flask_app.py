from flask import Flask, render_template, request


from analysis_files.pattern_calculator import predict_pattern
from analysis_files.score_calculator import calculate_overall_scores
from analysis_files.default_scorer import return_default


app = Flask(__name__)
app.config["DEBUG"] = True


stat_names = ['PT (points)', '3PM (three-pointers made)', 'FGA (field goal attempts)', 'FGM (field goals made)', 'FTA (free-throw attempts)'\
, 'FTM (free-throws made)', 'REB (rebounds)', 'AST (assists)', 'STL (steals)', 'BLK (blocks)', 'TOV (turnovers)']
default_stats = [1, 1, -1, 2, -1, 1, 1, 2, 4, 4, -2]
num_stats = len(stat_names)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method=='GET':
        return render_template("start_page.html")
    choice = request.form['scoring-choice']
    if 'Home' in choice:
        return render_template("start_page.html")
    if 'Default' in choice:
        return render_template('default_page.html', stat_names=stat_names, default_stats=default_stats, num_stats=num_stats)
    if 'Custom' in choice:
        return render_template('custom_page.html', stat_names=stat_names, num_stats=num_stats)
    if 'Calculate' in choice:
        #need to take input here
        point_system = []
        default_vs_custom = []
        name = []
        for (key, val) in request.form.items():
            if key.startswith("contents"):
                try:
                    if not val:
                        point_system.append(float(request.form["default_" + key[9:] + "_contents"]))
                    else:
                        point_system.append(float(val))
                except ValueError:
                    return render_template('error_page.html', stat_names=stat_names, num_stats=num_stats)
        predictions = []
        if point_system == default_stats:
            predictions = return_default()
        else:
            score_and_change = calculate_overall_scores(point_system)
            player_scores = score_and_change['player_scores']
            player_score_changes = score_and_change['player_score_changes']
            predictions = predict_pattern(player_scores, player_score_changes)
        return render_template('calculate_page.html', point_system=point_system, default_vs_custom=default_vs_custom, name=name, predictions=predictions)
