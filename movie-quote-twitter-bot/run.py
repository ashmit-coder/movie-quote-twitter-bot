#!/usr/bin/python3
import srt
import random
import twitter
import config
from moviepy.editor import *


def main():
    quote = random.choice(get_subs(config.GENERAL_CONFIG['subsURI']))
    video = generate_video_clip(
        config.GENERAL_CONFIG['videoURI'],
        quote.start,
        quote.end
    )
    text = generate_text_clip(quote.content, quote.start, quote.end)
    create_gif(config.GENERAL_CONFIG['outputURI'], video, text)

    api = twitter.Api(
        consumer_key=config.GENERAL_CONFIG['consumerKey'],
        consumer_secret=config.GENERAL_CONFIG['consumerSecret'],
        access_token_key=config.GENERAL_CONFIG['accessTokenKey'],
        access_token_secret=config.GENERAL_CONFIG['accessTokenSecret'],
    )
    post_gif_to_twitter(api, quote.content, config.GENERAL_CONFIG['outputURI'])


def get_subs(subs_file_uri):
    subs_file = open(config.GENERAL_CONFIG['subsURI'], encoding='utf-8-sig')
    return list(srt.parse(subs_file.read()))


def post_gif_to_twitter(api, sentence, gif_path):
    api.PostUpdate(sentence, media=gif_path, media_category='tweet_gif')


def generate_video_clip(video_uri, start, end):
    return (VideoFileClip(video_uri)
            .subclip(str(start), str(end))
            .resize(0.3))


def generate_text_clip(sentence, start, end):
    return TextClip(sentence, fontsize=24, color='yellow',
                    font='Amiri-bold').set_pos('bottom').set_duration(str(end - start))


def create_gif(output_uri, video, text):
    compo = CompositeVideoClip([video, text])
    compo.write_gif(output_uri)


main()
