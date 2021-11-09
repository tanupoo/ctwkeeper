#!/usr/bin/env python

from webexteamssdk import WebexTeamsAPI, exceptions
from typing import List, Union
import os
import json

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

def member_delete(api: WebexTeamsAPI, room_id: str, mail_addr: list) -> None:
    for m in mail_addr:
        try:
           n = api.memberships.list(room_id, personEmail=m)
           ret = api.memberships.delete(list(n)[0].id)
        except IndexError:
            print(f"{m} is not a member.")
        except exceptions.ApiError as e:
            print(str(e))
        else:
            print(f"{m} has been deleted.")

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

def member_show(api: WebexTeamsAPI, room_id: str, mail_addr: list) -> None:
    if mail_addr:
        for m in mail_addr:
            for n in api.memberships.list(room_id, personEmail=m):
                print(f"MembershipId: {n.id}")
    else:
        for n in api.memberships.list(room_id):
            print(f"{n.personDisplayName}: {n.personEmail}: {n.id}")

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
                    help="inform to show the members in the room. "
                    "with the -e option, show the info of the specific members")
    ap.add_argument("--add-members", "-A", action="store_true",
                    dest="add_members",
                    help="with the -e option, inform to add members")
    ap.add_argument("--delete-members", "-D", action="store_true",
                    dest="delete_members",
                    help="with the -e option, inform to delete members")
    ap.add_argument("--email-addrs", "-e", action="store", dest="email_addrs",
                    help="specify the member's email addresses "
                    "separated by a comma.")
    ap.add_argument("-m", action="store", dest="message",
                    help="specify a message to be sent.")
    ap.add_argument("-f", action="append", dest="files", nargs="*",
                    help="specify a file to be sent. "
                        "specify multiple times to send multiple files. ")
    ap.add_argument("--config", "-c", action="store", dest="config",
                    help="NOTYET: specify the config file.")
    ap.add_argument("--update-config", action="store_true", dest="update_config",
                    help="NOTYET: specify to create or update the config file.")
    ap.add_argument("-v", action="store_true", dest="verbose",
                    help="enable verbose mode.")
    opt = ap.parse_args()

    if opt.config:
        config = json.load(open(opt.config))

    # set the access token
    # the one specifyed by the option is preferred than the env variable.
    if opt.access_token is None:
        opt.access_token = os.environ.get("WEBEX_TEAMS_ACCESS_TOKEN", None)
        if opt.access_token is None:
            print("ERROR: access_token must be specified.")
            exit(0)

    email_addrs_list = None
    if opt.email_addrs:
        email_addrs_list = [i for i in opt.email_addrs.replace(" ","").split(",")]
    elif (opt.add_members or opt.delete_members):
        ap.print_help()
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
            member_show(api, opt.room_id, email_addrs_list)
        elif opt.add_members:
            member_add(api, opt.room_id, email_addrs_list)
        elif opt.delete_members:
            member_delete(api, opt.room_id, email_addrs_list)
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

