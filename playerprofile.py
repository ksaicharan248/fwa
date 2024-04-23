import io
import os

import requests
from PIL import Image , ImageDraw , ImageFont , ImageFilter , ImageChops
import urllib.request
import datetime
import COC




TROOPS = ["Barbarian" , "Archer" , "Giant" , "Goblin" , "Wall Breaker" , "Balloon" , "Wizard" , "Healer" , "Dragon" ,
          "P.E.K.K.A" , "Baby Dragon" , "Miner" , "Electro Dragon" , "Yeti" , "Electro Titan" , "Root Rider" ,
          "Minion" , "Hog Rider" , "Valkyrie" , "Golem" , "Witch" , "Lava Hound" , "Bowler" , "Ice Golem" ,
          "Headhunter" , "Dragon Rider" , "Apprentice Warden"]
SPELLS = ["Lightning Spell" , "Healing Spell" , "Rage Spell" , "Jump Spell" , "Freeze Spell" , "Clone Spell" ,
          "Invisibility Spell" , "Recall Spell" , "Poison Spell" , "Earthquake Spell" , "Haste Spell" ,
          "Skeleton Spell" , "Bat Spell" , "Overgrowth Spell"]
BUILDER_TROOPS = ["Raged Barbarian" , "Sneaky Archer" , "Boxer Giant" , "Beta Minion" , "Bomber" , "Baby Dragon" ,
                  "Cannon Cart" , "Night Witch" , "Drop Ship" , "Super P.E.K.K.A" , "Hog Glider" , "Electrofire Wizard"]
SUPER_TROOPS = ["Super Barbarian" , "Super Archer" , "Super Giant" , "Sneaky Goblin" , "Super Wall Breaker" ,
                "Super Wizard" , "Inferno Dragon" , "Super Minion" , "Super Valkyrie" , "Super Witch" , "Ice Hound" ,
                "Rocket Balloon" , "Super Dragon" , "Super Bowler"]
HEROES = ["Barbarian King" , "Archer Queen" , "Grand Warden" , "Royal Champion" , "Battle Machine","Battle Copter"]
MACHINES = ["Wall Wrecker" , "Battle Blimp" , "Stone Slammer" , "Siege Barracks" , "Log Launcher" , "Flame Flinger" ,
            "Battle Drill"]
PETS = ["L.A.S.S.I" , "Electro Owl" , "Mighty Yak" , "Unicorn" , "Diggy" , "Poison Lizard" , "Phoenix" , "Spirit Fox" ,
        "Angry Jelly"]


def draw_centered_text(drawt , rect , fontt , text , size , align="center") :
    fontt = fontt.font_variant(size=size)
    text_bbox = drawt.textbbox((0 , 0) , text , align=align , font=fontt)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (rect[0] + (rect[2] - text_width)) // 2
    y = (rect[1] + (rect[3] - text_height)) // 2
    draw_shadow_text(drawt , x , y , fontt , text , size)


def simple_text(drawt , x , y , fontt , text , size , colour=(255 , 255 , 255)) :
    fontt = fontt.font_variant(size=size)
    drawt.text((x , y) , text , fill=colour , font=fontt)


def draw_shadow_troops(drawt , x , y , fontt , text , size) :
    if size :
        fontt = fontt.font_variant(size=size)
    drawt.text((x , y +2) , text , fill="black" , font=fontt)
    drawt.text((x , y) , text , fill=(255 , 255 , 255) , font=fontt)


def draw_shadow_text(drawt , x , y , fontt , text , size) :
    if size :
        fontt = fontt.font_variant(size=size)
    drawt.text((x - 2 , y) , text , fill="black" , font=fontt)
    drawt.text((x , y) , text , fill=(255 , 255 , 255) , font=fontt)


def draw_image(image , path , x , y , resize=44) :
    paste_image = Image.open(path).convert("RGBA")
    paste_image = paste_image.resize((resize , resize))
    image.paste(paste_image , (x , y) , paste_image)
def draw_url_image(image , img , x , y , resize=44) :
    img= img.resize((resize , resize))
    image.paste(img , (x , y) , img)

def draw_image_troop(image , path , x , y , font , data , resize=44 , size=10) :
    paste_image = Image.open(path).convert("RGBA")
    if data[0] == data[1] :
        level = Image.open("resources/icons/level-label-max.png").resize((16 , 16))
    else :
        level = Image.open("resources/icons/level-label.png").resize((16 , 16))
    textdraw = ImageDraw.Draw(level)
    draw_shadow_troops(textdraw , 4 , 1 , font , str(data[0]) , size)
    paste_image = paste_image
    paste_image.paste(level , (1 , 44 - 18) , level)
    image.paste(paste_image , (x , y) , paste_image)


def draw_image_super_troop(image , path , x , y , font , data , resize=44 , size=10) :
    paste_image = Image.open(path).convert("RGBA")
    image.paste(paste_image , (x , y) , paste_image)


def playerprofile_(tag) :
    global TROOPS , HEROES , BUILDER_TROOPS , SUPER_TROOPS , SPELLS , MACHINES , PETS
    try :
        player_data = COC.get_user(tag)
    except Exception as e :
        print(e)
        return
    if player_data :
        FONT_SIZE = 12
        ARMY_TOPLINE = 238
        ARMY_BOTLINE = 500
        TROOP_SIZE = 44
        font = ImageFont.truetype("resources/fonts/Supercell.ttf" , FONT_SIZE)
        image = Image.open("resources/template.png")
        draw = ImageDraw.Draw(image)
        draw_shadow_text(draw , 75 , 16 , font , player_data.get("name") , FONT_SIZE + 8)
        draw_shadow_text(draw , 75 , 45 , font , player_data.get("tag") , FONT_SIZE - 2)
        draw_centered_text(draw , (35 , 42 , 52 , 32) , font ,
                           str(player_data.get('expLevel')) if player_data.get('expLevel') else "0" , FONT_SIZE + 5)
        # townahall
        townhall = str(player_data.get('townHallLevel')) if player_data.get('townHallLevel') else "1"
        draw_image(image , f"resources/buildings/townhalls/home/th{townhall}.png" , 90 , 80 , resize=100)
        draw_shadow_text(draw , 22 , 125 , font , f"Level {townhall}" , FONT_SIZE + 8)
        builder_hall = str(player_data.get('builderHallLevel')) if player_data.get('builderHallLevel') else "1"
        draw_image(image , f"resources/buildings/townhalls/builder/bh{builder_hall}.png" , 270 , 80 , resize=100)
        draw_shadow_text(draw , 200 , 125 , font , f"Level {builder_hall}" , FONT_SIZE + 8)
        if player_data.get('league') is not None :
            response = requests.get(player_data.get('league').get('iconUrls').get('medium'))
            img = Image.open(io.BytesIO(response.content))
            draw_url_image(image , img , 383 , 30 , resize=90)

        else :
            draw_image(image , "resources/icons/noleague.png" , 383 , 30 , resize=90)
        draw_centered_text(draw , (382 , 142 , 450 , 170) , font , str(player_data.get("trophies")) , FONT_SIZE + 6)
        simple_text(draw , 692 , 65 , font ,
                    str(player_data.get("bestTrophies")) if player_data.get('bestTrophies') is not None else "0" ,
                    FONT_SIZE - 1 , (68 , 69 , 69))
        simple_text(draw , 692 , 95 , font ,
                    str(player_data.get("warStars")) if player_data.get('warStars') is not None else "0" ,
                    FONT_SIZE - 1 , (68 , 69 , 69))
        simple_text(draw , 692 , 130 , font ,
                    str(player_data.get("achievements")[-5].get("value")) if player_data.get('achievements')[
                                                                                 -5] is not None else "0" ,
                    FONT_SIZE - 1 , (68 , 69 , 69))
        simple_text(draw , 692 , 160 , font ,
                    str(player_data.get("achievements")[-4].get("value")) if player_data.get('achievements')[
                                                                                 -4] is not None else "0" ,
                    FONT_SIZE - 1 , (68 , 69 , 69))
        if player_data.get("clan") is not None :
            response = requests.get(player_data.get("clan").get("badgeUrls").get("large"))
            img = Image.open(io.BytesIO(response.content))
            draw_url_image(image , img , 800 , 30 , resize=105)

            draw_centered_text(draw , (775 , 130 , 923 , 160) , font , player_data.get("clan").get("name") ,
                               FONT_SIZE + 2)
            draw_centered_text(draw , (775 , 151 , 923 , 181) , font ,
                               COC.get_role(player_data.get('role')) if player_data.get(
                                   'role') is not None else COC.get_role("member") , FONT_SIZE - 2)
        else :
            draw_image(image , "resources/icons/noclan.png" , 800 , 30 , resize=105)
        current_date = datetime.datetime.now()
        current_month = current_date.strftime("%B")
        current_year = current_date.year
        draw_shadow_text(draw , 495 , 18 , font , f"Season {current_month} {current_year}" , FONT_SIZE + 5)

        troop_names_set = {troop['name'] : [troop['level'] , troop['maxLevel']] for troop in player_data['troops']}
        troop_x = 20
        troop_y = ARMY_TOPLINE
        for troop in TROOPS :
            if troop in troop_names_set :

                draw_image_troop(image , f"resources/troops/{troop}.png" , troop_x , troop_y , font=font ,
                                 data=troop_names_set[troop] , resize=44)
                troop_x += TROOP_SIZE + 8
                if troop_x >= 210 :
                    troop_x = 20
                    troop_y += TROOP_SIZE + 6
            else :
                troop_x += TROOP_SIZE + 8
                if troop_x >= 210 :
                    troop_x = 20
                    troop_y += TROOP_SIZE + 6
        spell_x = 250
        spell_y = ARMY_TOPLINE
        spells_set = {spell['name'] : [spell['level'] , spell['maxLevel']] for spell in player_data['spells']}
        for spell_name in SPELLS :
            if spell_name in spells_set :
                draw_image_troop(image , f"resources/troops/{spell_name}.png" , spell_x , spell_y , font=font ,
                                 data=spells_set[spell_name] , resize=44)
                spell_x += TROOP_SIZE + 8
                if spell_x >= 420 :
                    spell_x = 250
                    spell_y += TROOP_SIZE + 6
            else :
                spell_x += TROOP_SIZE + 8
                if spell_x >= 420 :
                    spell_x = 250
                    spell_y += TROOP_SIZE + 6

        builder_x = 480
        builder_y = ARMY_TOPLINE

        for builder_troops in BUILDER_TROOPS :
            if builder_troops in troop_names_set :
                draw_image_troop(image , f"resources/troops/{builder_troops}.png" , builder_x , builder_y , font=font ,
                                 data=troop_names_set[builder_troops] , resize=44 , size=7)
                builder_x += TROOP_SIZE + 8
                if builder_x >= 650 :
                    builder_x = 480
                    builder_y += TROOP_SIZE + 6
            else :
                builder_x += TROOP_SIZE + 8
                if builder_x >= 650 :
                    builder_x = 480
                    builder_y += TROOP_SIZE + 6
        super_trops = [troop['name'] for troop in player_data.get('troops') if
                       troop.get("superTroopIsActive") is not None]
        super_troops_x = 710
        super_troops_y = ARMY_TOPLINE
        for super_troops in SUPER_TROOPS :
            if super_troops in super_trops :
                draw_image_super_troop(image , f"resources/troops/{super_troops}.png" , super_troops_x ,
                                       super_troops_y , font=font , data=troop_names_set[super_troops] , resize=44)
                super_troops_x += TROOP_SIZE + 8
                if super_troops_x >= 880 :
                    super_troops_x = 710
                    super_troops_y += TROOP_SIZE + 6
            else :
                super_troops_x += TROOP_SIZE + 8
                if super_troops_x >= 880 :
                    super_troops_x = 710
                    super_troops_y += TROOP_SIZE + 6

        heros = {hero['name'] : [hero['level'] , hero['maxLevel']] for hero in player_data['heroes']}
        hero_x = 250
        hero_y = ARMY_BOTLINE + 12
        for hero in HEROES :
            if hero in heros.keys():
                draw_image_troop(image , f"resources/troops/{hero}.png" , hero_x ,
                                       hero_y , font=font , data=heros[hero] , resize=44,size=6)
                hero_x += TROOP_SIZE + 8
                if hero_x >= 420 :
                    hero_x = 250
                    hero_y += TROOP_SIZE + 6
            else:
                hero_x += TROOP_SIZE + 8
                if hero_x >= 420 :
                    hero_x = 250
                    hero_y += TROOP_SIZE + 6

        machines_x = 480
        machines_y = ARMY_BOTLINE + 12

        for machine in MACHINES :
            if machine in troop_names_set.keys():
                draw_image_troop(image , f"resources/troops/{machine}.png" , machines_x , machines_y , font=font ,
                                 data=troop_names_set[machine] , resize=44)
                machines_x += TROOP_SIZE + 8
                if machines_x >= 650 :
                    machines_x = 480
                    machines_y += TROOP_SIZE + 6
            else:
                machines_x += TROOP_SIZE + 8
                if machines_x >= 650 :
                    machines_x = 480
                    machines_y += TROOP_SIZE + 6

        pet_x = 710
        pet_y = ARMY_BOTLINE - 12
        for pet in PETS :
            if pet in troop_names_set.keys():
                draw_image_troop(image , f"resources/troops/{pet}.png" , pet_x , pet_y , font=font ,
                                 data=troop_names_set[pet] , resize=44 , size=7)
                pet_x += TROOP_SIZE + 8
                if pet_x >= 880 :
                    pet_x = 710
                    pet_y += TROOP_SIZE + 6
            else:
                pet_x += TROOP_SIZE + 8
                if pet_x >= 880 :
                    pet_x = 710
                    pet_y += TROOP_SIZE + 6

        image_buffer = io.BytesIO()
        image.save(image_buffer , format='PNG')  # Convert image to PNG format
        image_buffer.seek(0)
        return image_buffer


if __name__ == '__main__' :
    playerprofile_('9LPY0JVVG')
