# Maid-chan feat Facebook Messenger (Work In Progress)

Maid-chan name is inspired from [Sakurasou's Artificial Intelligence](http://sakurasounopetnakanojo.wikia.com/wiki/Maid).

If you have any other ideas, I am accepting contributions :)

## How to Run

1. For initial configuration, you need to create `maidchan/config.py` based on `maidchan/config.py.example` and fill those values based on your own configuration.

2. Maid-chan are using Redis as the database. Redis can be downloaded via https://redis.io/download. Run Redis as a background process in port 6379 (default port).

3. It is recommended to use `virtualenv` (e.g.: `virtualenv venv` then `source venv/bin/activate`). You need to install all dependencies via `pip install -r requirements.txt`.

4. Run `python setup.py install` to build Maid-chan. Finally, you can execute `maidchan` in the background process to run this bot.


## Available Feature

- Upload image for random image filtering via https://github.com/fogleman/primitive (**Requires** `maidchan_primitive` running in the background and [ImageMagick](https://www.imagemagick.org/script/index.php) `convert` feature for generating GIF)  
<img src="https://freedomofkeima.com/images/maid-chan/primitive_scr.jpg" height="500">  
<img alt="Combined result" src="https://freedomofkeima.com/images/maid-chan/primitive.gif" height="500">  
- Japanese Kanji & Vocabulary for each reply

## Available Command

-

## Priority Ideas

- Japanese language quiz & daily Kanji
- Send link to download at home, e.g.: Youtube (feat https://github.com/soimort/you-get), image files, etc
- RSS monitoring (similar to my previous RSS Twilio bot: https://github.com/freedomofkeima/rss-twilio-bot)
- Time-based interaction (おはよう, daily "offerings", etc)
- Translate text (feat: https://github.com/soimort/translate-shell)


## Future Ideas 

- Image recognition, e.g.: waifu recognizer - https://github.com/nagadomi/lbpcascade_animeface or self-created
- Natural Language processing for conversing daily conversation (Naturally we can use IBM Watson or Google Cloud Speech, but the model "probably" differs from Maid-chan requirement)
- IoT with home electronics
- Mini games
- etc


## Reference


- http://gakuran.com/japanese-csv-database/ for raw data of Japanese Vocabulary and Kanji list
- https://github.com/hungtraan/FacebookBot


## License

MIT License.

Last Updated: January 5, 2017

