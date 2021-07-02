#!/usr/bin/env python

from webexteamssdk import WebexTeamsAPI, exceptions
from typing import List, Union
import os

"""
https://github.com/CiscoDevNet/webexteamssdk
"""

# Find all rooms that have 'webexteamssdk Demo' in their title
def room_list(api: WebexTeamsAPI) -> None:
    for r in api.rooms.list():
        print(f"{r.title}: {r.id}")

def member_add(api: WebexTeamsAPI, room_id: str, mail_addr: list) -> None:
    for m in mail_addr:
        try:
            ret = api.memberships.create(room_id, personEmail=m)
        except exceptions.ApiError as e:
            if "User is already a participant" in str(e):
                print(f"{m} is already participated.")
            else:
                print(str(e))
        else:
            print(f"{m} has been added.")

def send_msg(
        api: WebexTeamsAPI,
        room_id: str,
        message: Union[str,None] = None,
        files: Union[List,None] = None
        ) -> None:
    if len(files) > 1:
        raise NotImplementedError(
                "ERROR: don't specify multiple files. "
                "It currently doesn't support the feature "
                "due to the SDK's constraints.")
    file_list = None
    if files is not None:
        file_list = []
        for f in files[0]:
            file_list.append(os.path.abspath(f))
    ret = api.messages.create(room_id,
                                text=message,
                                files=file_list)
    print(ret)

def member_list(api: WebexTeamsAPI, room_id: str) -> None:
    for m in api.memberships.list(room_id):
        print(f"{m.personEmail}: {m.personDisplayName}")

def main():
    from argparse import ArgumentParser
    from argparse import ArgumentDefaultsHelpFormatter
    ap = ArgumentParser(
            description="Webex Teams Keeper.",
            formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument("--token", "-t", action="store", dest="access_token",
                    help="specify the access token.")
    ap.add_argument("--show-rooms", "-L", action="store_true",
                    dest="show_room_list",
                    help="specify to show the list of rooms.")
    ap.add_argument("--room-id", "-r", action="store", dest="room_id",
                    help="specify the room id.")
    ap.add_argument("--show-members", "-M", action="store_true",
                    dest="show_members",
                    help="specify to show the members in the room.")
    ap.add_argument("--add-members", "-a", action="store", dest="member_emails",
                    help="specify a list of the member's email address "
                    "separated by a comma.")
    ap.add_argument("-m", action="store", dest="message",
                    help="specify a message to be sent.")
    ap.add_argument("-f", action="append", dest="files", nargs="*",
                    help="specify a file to be sent. "
                        "specify multiple times to send multiple files. ")
    ap.add_argument("-v", action="store_true", dest="verbose",
                    help="enable verbose mode.")
    ap.add_argument("-d", action="store_true", dest="debug",
                    help="enable debug mode.")
    opt = ap.parse_args()

    # set the access token
    # the one specifyed by the option is preferred than the env variable.
    if opt.access_token is None:
        opt.access_token = os.environ.get("WEBEX_TEAMS_ACCESS_TOKEN", None)
        if opt.access_token is None:
            print("ERROR: access_token must be specified.")
            exit(0)

    # just try to set the room id if available.
    if opt.room_id is None:
        opt.room_id = os.environ.get("WEBEX_TEAMS_ROOM_ID", None)

    api = WebexTeamsAPI(access_token=opt.access_token)
    if opt.show_room_list:
        room_list(api)
        exit(0)
    if opt.room_id:
        if opt.show_members:
            member_list(api, opt.room_id)
        elif opt.member_emails:
            member_add(
                    api,
                    opt.room_id,
                    [i for i in opt.member_emails.replace(" ","").split(",")])
        elif opt.message:
            send_msg(
                    api,
                    opt.room_id,
                    message=opt.message,
                    files=opt.files)

#
# main
#
if __name__ == "__main__" :
    main()

