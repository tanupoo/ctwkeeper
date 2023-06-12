Webex Teams Keeper
==================

You have to specify your access key by either below methods.
define it into WEBEX_TEAMS_ACCESS_TOKEN as an environment variable.
or, specify it using the --token option.

You can set your room id:
define it into WEBEX_TEAMS_ROOM_ID as an environment variable.
or, specify it using the --room-id option.

## Usage: room

```
usage: cwtkeeper.py room [-h] [--token ACCESS_TOKEN] [--room-id ROOM_ID]
                         [--list]

options:
  -h, --help            show this help message and exit
  --token ACCESS_TOKEN, -t ACCESS_TOKEN
                        specify the access token.
  --room-id ROOM_ID, -r ROOM_ID
                        specify the room id.
  --list, -l            show the list of rooms.
```

## Usage: member

```
usage: cwtkeeper.py member [-h] [--token ACCESS_TOKEN] --room-id ROOM_ID
                           [--list] [--add] [--delete] [--email _MAIL_ADDRS]

options:
  -h, --help            show this help message and exit
  --token ACCESS_TOKEN, -t ACCESS_TOKEN
                        specify the access token.
  --room-id ROOM_ID, -r ROOM_ID
                        specify the room id.
  --list, -l            inform to show the members in the room. with the
                        --email option, show the info of the specific members
  --add, -a             with the --email-addrs option, inform to add members
  --delete, -d          with the --email-addrs option, inform to delete
                        members
  --email _MAIL_ADDRS, -e _MAIL_ADDRS
                        specify the member's email addresses separated by a
                        comma.
```

## Usage: message

```
usage: cwtkeeper.py message [-h] [--token ACCESS_TOKEN] [--room-id ROOM_ID]
                            [--email _MAIL_ADDRS] [--message MESSAGE]
                            [--file [_FILES ...]] [--list] [--since SINCE]
                            [--max MAX_NB_MAILS]

options:
  -h, --help            show this help message and exit
  --token ACCESS_TOKEN, -t ACCESS_TOKEN
                        specify the access token.
  --room-id ROOM_ID, -r ROOM_ID
                        specify the room id. Ignored with the --email option.
  --email _MAIL_ADDRS, -e _MAIL_ADDRS
                        specify the recipient's email addresses separated by a
                        comma.
  --message MESSAGE, -m MESSAGE
                        specify a message to be sent.
  --file [_FILES ...], -f [_FILES ...]
                        specify a file to be sent. specify multiple times to
                        send multiple files.
  --list, -l            list the messages. Either the --since option or the
                        --max option is required.
  --since SINCE, -a SINCE
                        specify ISO6801 datetime to be listed mails after the
                        datetime.
  --max MAX_NB_MAILS    specify the number of mails to be listed.
```

## Usage: people

```
usage: cwtkeeper.py people [-h] [--token ACCESS_TOKEN]
                           [--email-addrs _MAIL_ADDRS] [--detail]

options:
  -h, --help            show this help message and exit
  --token ACCESS_TOKEN, -t ACCESS_TOKEN
                        specify the access token.
  --email-addrs _MAIL_ADDRS, -e _MAIL_ADDRS
                        specify the member's email addresses separated by a
                        comma. it is required if you are not admin.
  --detail, -L          specify to show a detail info.
```

## Trouble Shooting: 403 Forbidden in the message mode.

You may see the following error when you use an access token for your bot.

```
webexteamssdk.exceptions.ApiError: [403] Forbidden - Failed to get activity.
```

Webex API looks not to allow a bot to access a list of a room.
You should use your own token in this case.

## References

- [Webex Messaging API](https://developer.webex.com/docs/messaging)
- [WebexTeamsAPI in Python](https://webexteamssdk.readthedocs.io/en/latest/user/api.html#webexteamsapi)/[Github](https://github.com/WebexCommunity/WebexPythonSDK)

