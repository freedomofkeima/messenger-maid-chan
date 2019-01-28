# Maid-chan feat Facebook Messenger

[![CircleCI](https://circleci.com/gh/freedomofkeima/messenger-maid-chan/tree/master.svg?style=shield)](https://circleci.com/gh/freedomofkeima/messenger-maid-chan/tree/master)
[![readthedocs](https://readthedocs.org/projects/messenger-maid-chan/badge/?version=latest)](https://messenger-maid-chan.readthedocs.io/en/latest/)

**Note**: As of October 5, 2018, Maid-chan is now migrated to Python 3.6+.

Maid-chan name is inspired from [Sakurasou's Artificial Intelligence](http://sakurasounopetnakanojo.wikia.com/wiki/Maid).

If you have any other ideas, I am accepting contributions :) For developers, you could access [the documentation pages for developers here](https://messenger-maid-chan.readthedocs.io/). For others who are interested in using Maid-chan features, please ask me directly and head to [Maid-chan Facebook Page](https://www.facebook.com/maidchan2/).

Maid-chan is featured in:
- [Chatbot's Life](https://chatbotslife.com/building-personalized-maid-assistant-for-dummies-23ce7196fa35)
- [PyCon JP 2017](https://pycon.jp/2017/en/schedule/presentation/4/) | [Presentation](https://freedomofkeima.com/pyconjp2017/)
- [PyCon MY 2018](https://pycon.my/pycon-my-2018-program-schedule/) | [Presentation](https://freedomofkeima.com/pyconmy2018.pdf)


## Available Features

- Upload image for random image filtering via [Primitive](https://github.com/fogleman/primitive) (**Requires** `maidchan_primitive` running in the background and [ImageMagick](https://www.imagemagick.org/script/index.php) `convert` feature for generating GIF)  
<img src="https://freedomofkeima.com/images/maid-chan/primitive_scr.jpg" width="350">  
<img alt="Combined result" src="https://freedomofkeima.com/images/maid-chan/primitive.gif" width="350">

- Simple chat (English or Bahasa Indonesia) via [ChatterBot](https://github.com/gunthercox/ChatterBot) feat [langdetect](https://github.com/Mimino666/langdetect). The accuracy is still bad, though  
<img src="https://freedomofkeima.com/images/maid-chan/chatterbot.png" width="350">

- Daily good morning and good night messages, with "offerings"! (**Requires** `maidchan_scheduler` running in the background)  
<img src="https://freedomofkeima.com/images/maid-chan/daily_morning_offerings.png" width="350">  
<img src="https://freedomofkeima.com/images/maid-chan/daily_night_offerings.png" width="350">

- Daily Japanese Kanji & Vocabulary (**Requires** `maidchan_scheduler` running in the background)  
<img src="https://freedomofkeima.com/images/maid-chan/daily_japanese.png" width="350">

- RSS Feed Notifier for Anime, Manga, etc which is similar to [my previous RSS Twilio bot](https://github.com/freedomofkeima/rss-twilio-bot) (**Requires** `maidchan_scheduler` running in the background)  
<img src="https://freedomofkeima.com/images/maid-chan/rss_notification.png" width="350">

- Translate text via Google Translate feat [translate-shell](https://github.com/soimort/translate-shell)  
<img src="https://freedomofkeima.com/images/maid-chan/translate_normal.png" width="350">  
<img src="https://freedomofkeima.com/images/maid-chan/translate_using_from.png" width="350">

- [Experimental] Tokyo train status feat [Yahoo Japan](https://transit.yahoo.co.jp/traininfo/area/4/) (**Requires** `maidchan_scheduler` running in the background)  
<img src="https://freedomofkeima.com/images/maid-chan/train_status.png" width="350">

All time-related features are currently handled in **UTC+9 (Japan Time)**.


## Available Commands

### All users

- `help`: You will get the list of all available commands from Maid-chan
- `subscribe offerings`: Maid-chan will start giving you a good morning message and a good night messages
- `unsubscribe offerings`: Maid-chan will stop spamming you with those messages, but Maid-chan will be sad :'(
- `update offerings`: Maid-chan will ask you about your usual waking up and sleeping time, because Maid-chan doesn't want to disturb your sleep . . ., usually :p (some surprises inside!)  
<img src="https://freedomofkeima.com/images/maid-chan/offerings_subscribe.png" width="350">

- `subscribe japanese`: Maid-chan will start sending you random daily Kanji & Vocabulary
- `unsubscribe japanese`: Maid-chan will stop sending you random daily Kanji & Vocabulary
- `update japanese`: Maid-chan will ask about your level preference for Kanji (N1 to N4, old test format)  
<img src="https://freedomofkeima.com/images/maid-chan/japanese_subscribe.png" width="350">

- `update name`: By default, Maid-chan will call you with `onii-chan`  
<img src="https://freedomofkeima.com/images/maid-chan/name.png" width="350">

- `subscribe rss`: You could add an RSS feed with its pattern and let Maid-chan notify you when there is an update
- `unsubscribe rss`: You could remove one of your RSS feed subscription each time you call this command  
<img src="https://freedomofkeima.com/images/maid-chan/rss_1_manga.png" width="350">

- [Experimental] `subscribe train`: Maid-chan will give you updates related to Tokyo train status (currently, it only supports admin's train line :p)
- [Experimental] `unsubscribe train`: Maid-chan will stop sending you information related to Tokyo train status
- `show profile`: Do you want to know what Maid-chan knows about you? Then, you could use this command!


## How to Run

1. For initial configuration, you need to create `maidchan/config.py` based on `maidchan/config.py.example` and fill those values based on your own configuration.

2. Maid-chan is using Redis as the database. Redis can be downloaded via https://redis.io/download. Run Redis as a background process in port 6379 (default port).

3. ChatterBot 0.8.X has dropped support for simple JSON storage because of performance issues. Depending on your choice, you need to have either SQLite or MongoDB and modify `maidchan/config.py` accordingly. [MongoDB Installation Guide](https://docs.mongodb.com/manual/administration/install-community/))

4. It is recommended to use `venv` (e.g.: `python3 -m venv venv` then `source venv/bin/activate`). You need to install all dependencies via `pip install -r requirements.txt`.

5. Run `python setup.py install` to build Maid-chan. Finally, you can execute `maidchan` in the background process to run this bot.


## Priority Ideas

- (Admin only) Send link to download at home, e.g.: Youtube (feat https://github.com/soimort/you-get), image files, etc


## Existing Feature Improvement Ideas

- (Admin only) Broadcast message to all users which have talked to Maid-chan at least once
- Modifiable daily Japanese Kanji & Vocabulary time
- Automatic offerings update from upstream


## Future Ideas 

- Japanese language quiz
- Image recognition, e.g.: waifu recognizer - https://github.com/nagadomi/lbpcascade_animeface or self-created
- Natural Language processing for conversing daily conversation (Naturally we can improve it with IBM Watson or Google Cloud Speech, but the model "probably" differs from Maid-chan requirement)
- Mini games
- Location-aware features: Recommendation, weather, etc
- IoT with home electronics
- etc


## Reference

- http://gakuran.com/japanese-csv-database/ for raw data of Japanese Vocabulary and Kanji list
- https://github.com/hungtraan/FacebookBot


## License

This project itself is licensed under MIT License. All images are owned by their respective creators.

Last Updated: October 5, 2018
