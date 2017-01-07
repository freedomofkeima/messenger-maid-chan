# Maid-chan feat Facebook Messenger (Work In Progress)

Maid-chan name is inspired from [Sakurasou's Artificial Intelligence](http://sakurasounopetnakanojo.wikia.com/wiki/Maid).

If you have any other ideas, I am accepting contributions :)

## How to Run

1. For initial configuration, you need to create `maidchan/config.py` based on `maidchan/config.py.example` and fill those values based on your own configuration.

2. Maid-chan are using Redis as the database. Redis can be downloaded via https://redis.io/download. Run Redis as a background process in port 6379 (default port).

3. It is recommended to use `virtualenv` (e.g.: `virtualenv venv` then `source venv/bin/activate`). You need to install all dependencies via `pip install -r requirements.txt`.

4. Run `python setup.py install` to build Maid-chan. Finally, you can execute `maidchan` in the background process to run this bot.


## Available Feature

- Upload image for random image filtering via [Primitive](https://github.com/fogleman/primitive) (**Requires** `maidchan_primitive` running in the background and [ImageMagick](https://www.imagemagick.org/script/index.php) `convert` feature for generating GIF)  
<img src="https://freedomofkeima.com/images/maid-chan/primitive_scr.jpg" height="500">  
<img alt="Combined result" src="https://freedomofkeima.com/images/maid-chan/primitive.gif" height="500">  
- Simple chat (English or Bahasa Indonesia) via [ChatterBot](https://github.com/gunthercox/ChatterBot) feat [langdetect](https://github.com/Mimino666/langdetect). The accuracy is still bad, though (no optimization so far)  
<img src="https://freedomofkeima.com/images/maid-chan/chatterbot.png" height="300">  
- [Command Not Yet Implemented] Daily good morning and good night messages, with "offerings"!
- [Command Not Yet Implemented] Daily Japanese Kanji & Vocabulary

## [IN PROGRESS] Available Command

### All users

- `help`: You will get the list of all available commands from Maid-chan
- `subscribe offerings`: Maid-chan will start giving you a good morning message and a good night messages
- `unsubscribe offerings`: Maid-chan will stop spamming you with those messages, but Maid-chan will be sad :'(
- `update offerings`: Maid-chan will ask you about your usual waking up and sleeping time, because Maid-chan doesn't want to disturb your sleep . . ., usually :p
- `subscribe japanese`: Maid-chan will start sending you random daily Kanji & Vocabulary
- `unsubscribe japanese`: Maid-chan will stop sending you random daily Kanji & Vocabulary
- `update japanese`: Maid-chan will ask about your level preference for Kanji (N1 to N4, old test format)
- `update name`: By default, Maid-chan will call you with `onii-chan`


## Priority Ideas

- Send link to download at home, e.g.: Youtube (feat https://github.com/soimort/you-get), image files, etc
- RSS monitoring (similar to my previous RSS Twilio bot: https://github.com/freedomofkeima/rss-twilio-bot)
- Translate text (feat: https://github.com/soimort/translate-shell)


## Future Ideas 

- Japanese language quiz
- Image recognition, e.g.: waifu recognizer - https://github.com/nagadomi/lbpcascade_animeface or self-created
- Natural Language processing for conversing daily conversation (Naturally we can improve it with IBM Watson or Google Cloud Speech, but the model "probably" differs from Maid-chan requirement)
- IoT with home electronics
- Mini games
- etc


## Reference


- http://gakuran.com/japanese-csv-database/ for raw data of Japanese Vocabulary and Kanji list
- https://github.com/hungtraan/FacebookBot


## License

MIT License.

Last Updated: January 8, 2017

