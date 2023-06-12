Webex Teams Keeper
==================

You have to specify your access key by either below methods.
define it into WEBEX_TEAMS_ACCESS_TOKEN as an environment variable.
or, specify it using the --token option.

You can set your room id:
define it into WEBEX_TEAMS_ROOM_ID as an environment variable.
or, specify it using the --room-id option.

## Usage

```
usage: cwtkeeper.py [-h] [--token ACCESS_TOKEN] [--show-rooms]
                    [--room-id ROOM_ID] [--show-members]
                    [--add-members MEMBER_EMAILS] [-m MESSAGE]
                    [-f [FILES ...]] [-v] [-d]

Webex Teams Keeper.

optional arguments:
  -h, --help            show this help message and exit
  --token ACCESS_TOKEN, -t ACCESS_TOKEN
                        specify the access token. (default: None)
  --show-rooms, -L      specify to show the list of rooms. (default: False)
  --room-id ROOM_ID, -r ROOM_ID
                        specify the room id. (default: None)
  --show-members, -M    specify to show the members in the room. (default:
                        False)
  --add-members MEMBER_EMAILS, -a MEMBER_EMAILS
                        specify a list of the member's email address separated
                        by a comma. (default: None)
  -m MESSAGE            specify a message to be sent. (default: None)
  -f [FILES ...]        specify a file to be sent. specify multiple times to
                        send multiple files. (default: None)
  -v                    enable verbose mode. (default: False)
  -d                    enable debug mode. (default: False)
```

## References

- https://developer.webex.com/docs/messaging

