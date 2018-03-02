# Secret Santa Bot
This bot is going to help you make a combination of people to see who is going to give who a present.

To set up the code first make a Tokens.py and set a variable like this, which is your telegram bot token : 
~~~python
telegram_bot_token = ''
~~~

And after that :
~~~console
$ pip install -r requirements.txt
$ python SecretSanta.py
~~~

## Commands

* /getgroup

This will give you a new code for a new group.You can invite others with this link.

* /sendsanta

This will get your group_id and will send the users of the group a private message.

