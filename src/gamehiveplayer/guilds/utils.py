from sqlalchemy import text
from gamehiveplayer.models import db

def calculate_total_skill_points(guild):
    """ Skill points rule: if a player is in a guild when they pick up an item: if anyone else in the guild has the same item,
        the skill points of the  players with that item are decreased by the same amount first.

        In other words, points are sum of each guild members' skill points, plus, sum of distinct items' skill points which members have.
        return integer
    """
    
    sql_total_player_skill_points = """SELECT SUM(skill_point) from players WHERE guild_id = :guildid"""
    sql_total_item_skill_points = """SELECT SUM(skill_point) from (SELECT distinct i.id, i.skill_point FROM players as p LEFT JOIN player_items as pi on pi.player_id = p.id LEFT JOIN items as i on i.id = pi.item_id WHERE p.guild_id = :guildid) as foo"""
    result_1 = db.engine.execute(text(sql_total_player_skill_points), guildid=guild.id)
    result_2 = db.engine.execute(text(sql_total_item_skill_points), guildid=guild.id)
    return result_1.fetchone()[0] + result_2.fetchone()[0]
