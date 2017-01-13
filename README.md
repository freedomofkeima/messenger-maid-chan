# Maid-chan feat Facebook Messenger (Work In Progress)

Maid-chan name is inspired from [Sakurasou's Artificial Intelligence](http://sakurasounopetnakanojo.wikia.com/wiki/Maid).

If you have any other ideas, I am accepting contributions :) For developers, you could access [the documentation pages for developers here](https://messenger-maid-chan.readthedocs.io/). For others who are interested in using Maid-chan features, please ask me directly and head to [Maid-chan Facebook Page](https://www.facebook.com/maidchan2/).


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
- `show profile`: Do you want to know what Maid-chan knows about you? Then, you could use this command!


## How to Run

1. For initial configuration, you need to create `maidchan/config.py` based on `maidchan/config.py.example` and fill those values based on your own configuration.

2. Maid-chan is using Redis as the database. Redis can be downloaded via https://redis.io/download. Run Redis as a background process in port 6379 (default port).

3. It is recommended to use `virtualenv` (e.g.: `virtualenv venv` then `source venv/bin/activate`). You need to install all dependencies via `pip install -r requirements.txt`.

4. Run `python setup.py install` to build Maid-chan. Finally, you can execute `maidchan` in the background process to run this bot.


## Priority Ideas

- RSS monitoring (similar to my previous RSS Twilio bot: https://github.com/freedomofkeima/rss-twilio-bot)
- Translate text (feat: https://github.com/soimort/translate-shell)
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
- Location-aware features: Recommendation, weather, train status, etc
- IoT with home electronics
- etc


## Reference

- http://gakuran.com/japanese-csv-database/ for raw data of Japanese Vocabulary and Kanji list
- https://github.com/hungtraan/FacebookBot


## License

This project itself is licensed under MIT License. All images are owned by their respective creators.

Last Updated: January 13, 2017
