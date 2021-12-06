import io
import os.path
import time

import requests
from PIL import Image, ImageDraw, ImageFont

from utils.helpers import center_text, add_corners
from utils.consts import convertTimeStamp
from utils.wmpvp import get_csgo_history


# wanmei_data = get_csgo_history(76561198848873537, page_size=10, data_source=3)


def create_signature(user_info, results):
    img_cnt = len(results)
    img_width = 40
    img_real_width = 32
    padding = 2
    extra_padding_x = 1
    img_total_width = img_width
    #
    # img = Image.new(
    #     'RGBA', ((img_width + padding) * img_cnt + padding, 128),
    #     color=(255, 255, 255, 0)
    # )
    img = Image.open("./data/img_1.png")

    d = ImageDraw.Draw(img)
    d_aa_off = ImageDraw.Draw(img)
    d_aa_off.fontmode = "1"
    normal_font = ImageFont.truetype('fonts/Poppins-Medium.ttf', 11)
    pixel_font = ImageFont.truetype('fonts/LcdSolid-VPzB.ttf', 10)
    monospace_font = ImageFont.truetype('fonts/AnonymousPro-Bold.ttf', 11)
    unicode_font = ImageFont.truetype('fonts/NotoSansCJKjp-Regular.otf', 15)

    img_width = 500
    title_x = padding + 32
    title_y = padding - 1
    avatar_x = padding + 8
    avatar_y = padding + 24
    avatar_width = 64
    base_y = 8 + padding
    img_start_y = base_y + 24
    text_date_y = img_start_y - 12
    text_y = img_start_y + 30
    text_rating_y = img_start_y + 42
    text_elo_y = img_start_y + 54
    text_start_x = 88
    platform_width = 24
    platform_y = 2
    platform_x = 2
    dxim = 4

    d.text(
        (title_x, title_y),
        user_info['name'],
        font=unicode_font,
        fill="white"
    )

    right_align_text = d.textsize(user_info['code'], font=unicode_font)[0]
    d.text(
        (img_width - right_align_text - padding, title_y),
        user_info['code'],
        font=unicode_font,
        fill="white"
    )

    im = Image.open(user_info['avatar']).resize((avatar_width, avatar_width))
    im = add_corners(im, 10)
    img.paste(im, (avatar_x, avatar_y), im)

    im = Image.open(user_info['platform_icon']).resize((platform_width, platform_width))
    # im = add_corners(im, 10)
    img.paste(im, (platform_x, platform_y), im)


    for i, result in enumerate(results):
        block_start_x = text_start_x + padding + i * (img_total_width + extra_padding_x)
        block_end_x = block_start_x + img_total_width
        text_x_dxim = block_start_x + dxim
        text_start_self = text_x_dxim
        text_start_enemy = text_x_dxim + 22

        im = Image.open(result['map']).resize((img_real_width, img_real_width))
        img.paste(im, (text_x_dxim, img_start_y), im)

        text_time = convertTimeStamp(result["timestamp"], "%H:%M")
        if result["timestamp"] < time.time() - 86400:
            text_time = convertTimeStamp(result["timestamp"], "%m-%d")

        center_text(
            d_aa_off, block_start_x, block_end_x, text_date_y,
            text_time,
            font=pixel_font, fill="white"
        )

        # [40]
        # [2, 16, 4, 16, 2]
        score_self = result['score1']
        score_enemy = result['score2']
        text_rating = "%.2f" % result['rating']
        text_elo = "%d" % result['elo']

        indicator_color = '#ffff00'
        if score_enemy > score_self:
            indicator_color = '#ff6666'
        elif score_enemy < score_self:
            indicator_color = '#00ff00'

        elo_indicator_color = '#ffff00'
        if result['elo_change'] < 0:
            elo_indicator_color = '#ff6666'
        elif result['elo_change'] > 0:
            elo_indicator_color = '#00ff00'

        indicator_rating_color = '#ffff00'
        if result['rating'] < 1.01:
            indicator_rating_color = '#ff6666'
        elif result['rating'] > 0.99:
            indicator_rating_color = '#00ff00'

        center_text(
            d_aa_off, block_start_x, block_end_x, text_rating_y,
            text_rating,
            font=pixel_font, fill=indicator_rating_color
        )
        if result['elo'] > 0:
            center_text(
                d_aa_off, block_start_x, block_end_x, text_elo_y,
                text_elo,
                font=pixel_font, fill=elo_indicator_color
            )
        # scoreboard
        d_aa_off.text(
            (text_start_self, text_y), "%02d" % score_self,
            font=pixel_font, fill=indicator_color
        )
        d_aa_off.text(
            (text_start_enemy, text_y), "%02d" % score_enemy,
            font=pixel_font, fill=(255, 255, 255)
        )

    # img.save('pil_text_font.png')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
