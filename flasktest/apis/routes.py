
import time
import os

from flask import render_template, request, flash
from flask_login import login_required

from flasktest.models import APIData
from flasktest.apis.forms import SearchPUBGForm
from flasktest.apis.utils import get_player_id, get_seasons, get_all_season_stats, \
    create_dataframe, create_kills_bar, create_damage_bar, create_distance_bar,\
    load_old_pubg_data, get_pubg_cooldown_message, update_pubg_api_data

from flask import Blueprint

apis = Blueprint("apis", __name__)


@apis.route("/api/pubg", methods=["POST", "GET"])
@login_required
def pubg():
    pubg_form = SearchPUBGForm()
    kills_img = "../static/images/api/pubg/example_kills.png"
    damage_img = "../static/images/api/pubg/example_damage.png"
    distance_img = "../static/images/api/pubg/example_distance.png"
    df_path = "flasktest/static/data/api/pubg/df_"
    pubg_data = APIData.query.filter_by(api_name="pubg").first()

    if request.method == "GET":
        return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                               damage_img=damage_img, distance_img=distance_img, page="pubg")

    if pubg_form.validate_on_submit():
        name = pubg_form.name.data
        game_mode = pubg_form.game_mode.data + pubg_form.perspective.data
        save_mode = game_mode.replace("-", "_")

        # Check for existing data before contacting API
        if os.path.exists(f"{df_path}{name}_{save_mode}.csv"):
            kills_img, damage_img, distance_img = \
                load_old_pubg_data(df_path, name, game_mode, save_mode)

            return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                                   damage_img=damage_img, distance_img=distance_img,
                                   scrollToAnchor="pubg-section", page="pubg")

        # No data found - contact API
        # Check API availability
        if (pubg_data.last_used + 60) > time.time():
            # API used in last 60 seconds
            flash_message = get_pubg_cooldown_message()
            flash(flash_message)
            return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                                   damage_img=damage_img, distance_img=distance_img,
                                   scrollToAnchor="pubg-section", page="pubg")

        id_code, id_response = get_player_id(name)
        if not id_code == 200:
            # Unsuccessful request - see pubg_imp.py for more info
            if id_code == 429:
                # Request limit reached
                update_pubg_api_data()

            flash_message = id_response
            flash(flash_message)
            return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                                   damage_img=damage_img, distance_img=distance_img,
                                   scrollToAnchor="pubg-section", page="pubg")

        player_id = id_response
        # Player ID retrieved successfully
        seasons_code, seasons_response = get_seasons()
        if not seasons_code == 200:
            # Unsuccessful request - see pubg_imp.py for more info
            flash_message = seasons_response
            if seasons_code == 429:
                # Request limit reached
                update_pubg_api_data()

            flash(flash_message)
            return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                                   damage_img=damage_img, distance_img=distance_img,
                                   scrollToAnchor="pubg-section", page="pubg")

        valid_seasons = seasons_response
        # Valid seasons retrieved successfully
        stats_code, stats_response = get_all_season_stats(player_id, valid_seasons, game_mode)
        if not stats_code == 200:
            # Unsuccessful request - see pubg_imp.py for more info
            flash_message = stats_response
            if stats_code == 429:
                # Request limit reached
                update_pubg_api_data()

            flash(flash_message)
            return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                                   damage_img=damage_img, distance_img=distance_img,
                                   scrollToAnchor="pubg-section", page="pubg")

        player_stats = stats_response
        # Player stats retrieved successfully
        if len(player_stats[0]) < 2:
            # Check if player was active in at least 2 seasons, else draw no graph
            flash("Player has insufficient stats to generate graph")
            return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                                   damage_img=damage_img, distance_img=distance_img,
                                   scrollToAnchor="pubg-section", page="pubg")

        # Success
        new_df = create_dataframe(player_stats, name, save_mode)
        kills_img = create_kills_bar(new_df, name, game_mode)
        damage_img = create_damage_bar(new_df, name, game_mode)
        distance_img = create_distance_bar(new_df, name, game_mode)
        # Update api db with timestamp
        update_pubg_api_data()
        return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                               damage_img=damage_img, distance_img=distance_img,
                               scrollToAnchor="pubg-section", page="pubg")

    # Form not validated
    return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                           damage_img=damage_img, distance_img=distance_img,
                           scrollToAnchor="pubg-section", page="pubg")
