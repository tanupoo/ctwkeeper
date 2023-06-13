#!/usr/bin/env python

from webexteamssdk import WebexTeamsAPI, exceptions, WebexTeamsDateTime
import os
import json
from argparse import ArgumentParser

"""
https://github.com/CiscoDevNet/webexteamssdk
"""

#
# room management
#
def room_functions(opt, subp):
    # set the room id if not specified.
    if opt.room_id is None:
        opt.room_id = os.environ.get("WEBEX_TEAMS_ROOM_ID", None)

    api = WebexTeamsAPI(access_token=opt.access_token)

    if opt.show_room_list:
        # Find all rooms where the bot participates.
        for r in api.rooms.list():
            print(f"{r.title}: {r.id}")
    elif opt.room_id:
        ret = api.rooms.get(opt.room_id)
        print(ret)


#
# membership management
#
def member_functions(opt, subp):
    # check room_id
    if opt.room_id is None:
        opt.room_id = os.environ.get("WEBEX_TEAMS_ROOM_ID", None)
    if opt.room_id is None:
        subp.choices[opt.subcommand].print_help()
        return
    # set the mail addrs.
    opt.mail_addrs = []
    if opt._mail_addrs:
        opt.mail_addrs = [i for i in opt._mail_addrs.replace(" ","").split(",")]

    api = WebexTeamsAPI(access_token=opt.access_token)

    if opt.show_members:
        if opt.mail_addrs:
            for a in opt.mail_addrs:
                for n in api.memberships.list(opt.room_id, personEmail=a):
                    print(f"MembershipId: {n.id}")
        else:
            for n in api.memberships.list(opt.room_id):
                print(f"{n.personDisplayName}: {n.personEmail}: {n.id}")

    elif opt.add_members:
        for a in opt.mail_addr:
            try:
                ret = api.memberships.create(opt.room_id, personEmail=a)
            except exceptions.ApiError as e:
                if "User is already a participant" in str(e):
                    print(f"{a} is already participated.")
                else:
                    print(str(e))
            else:
                print(f"{a} has been added.")

    elif opt.delete_members:
        for a in opt.mail_addr:
            try:
                n = api.memberships.list(opt.room_id, personEmail=a)
                ret = api.memberships.delete(list(n)[0].id)
            except IndexError:
                print(f"{a} is not a member.")
            except exceptions.ApiError as e:
                print(str(e))
            else:
                print(f"{a} has been deleted.")

#
# message functions
#
def message_functions(opt, subp):
    # set the room id if not specified.
    if opt.room_id is None:
        opt.room_id = os.environ.get("WEBEX_TEAMS_ROOM_ID", None)
    # set the mail addrs.
    opt.mail_addrs = []
    if opt._mail_addrs:
        opt.mail_addrs = [i for i in opt._mail_addrs.replace(" ","").split(",")]

    api = WebexTeamsAPI(access_token=opt.access_token)

    if opt.show_messages:
        if not (opt.max_nb_mails or opt._since):
            subp.choices[opt.subcommand].print_help()
            return
        # set datetime of opt.since
        since_dt = None
        if opt.since:
            since_dt = WebexTeamsDateTime.strptime(opt.since)
        ret = None
        if opt.mail_addrs:
            for a in opt.mail_addrs:
                ret = api.messages.list(roomId=opt.room_id,
                                        mentionedPeople=a)
                for i,m in enumerate(ret):
                    if since_dt:
                        if since_dt > m.created:
                            break
                    print(m)
                    if i + 1 >= opt.max_nb_mails:
                        break
        else:
            ret = api.messages.list(roomId=opt.room_id)
            for i,m in enumerate(ret):
                if since_dt:
                    if since_dt > m.created:
                        break
                print(m)
                if i + 1 >= opt.max_nb_mails:
                    break
    else:
        file_list = []
        if opt._files:
            for f in files[0]:
                file_list.append(os.path.abspath(f))
        if len(file_list) not in [0, 1]:
            raise NotImplementedError(
                    "ERROR: don't specify multiple files. "
                    "It currently doesn't support the feature "
                    "due to the SDK's constraints.")

        if not (opt.message or file_list):
            subp.choices[opt.subcommand].print_help()
            return

        elif opt.mail_addrs:
            for a in opt.mail_addrs:
                ret = api.messages.create(toPersonEmail=a,
                                          text=opt.message,
                                          files=file_list)
            print(ret)
        elif opt.room_id:
            ret = api.messages.create(roomId=opt.room_id,
                                      text=opt.message,
                                      files=file_list)
            print(ret)
        else:
            subp.choices[opt.subcommand].print_help()
            return

#
# people functions
#
def people_functions(opt, subp):
    # set the mail addrs.
    opt.mail_addrs = []
    if opt._mail_addrs:
        opt.mail_addrs = [i for i in opt._mail_addrs.replace(" ","").split(",")]

    api = WebexTeamsAPI(access_token=opt.access_token)

    for a in opt.mail_addrs:
        for p in api.people.list(email=a):
            if opt.show_detail:
                print(p)
            else:
                print(f"{p.displayName}: {p.id}")

def main(argv):
    ap = ArgumentParser(description="Webex Teams Keeper.")
    """
    ap.add_argument("--config", "-c", action="store", dest="config",
                    help="NOTYET: specify the config file.")
    ap.add_argument("--update-config", action="store_true", dest="update_config",
                    help="NOTYET: specify to create or update the config file.")
    """
    # sub menu
    subp = ap.add_subparsers(title="subcommands",
                             metavar="room, member, message, people",
                             dest="subcommand",
                             required=True,
                             )
    # room
    sap = subp.add_parser("room", aliases=["roo", "rm"],
                          help="the room management.")
    sap.add_argument("--token", "-t", action="store", dest="access_token",
                     help="specify the access token.")
    sap.add_argument("--room-id", "-r", action="store", dest="room_id",
                     help="specify the room id.")
    sap.add_argument("--list", "-l", action="store_true",
                     dest="show_room_list",
                     help="show the list of rooms.")
    sap.set_defaults(func=room_functions)
    # membership
    sap = subp.add_parser("member", aliases=["mem", "mm"],
                          help="the membership management.")
    sap.add_argument("--token", "-t", action="store", dest="access_token",
                    help="specify the access token.")
    sap.add_argument("--room-id", "-r", action="store", dest="room_id",
                     required=True,
                    help="specify the room id.")
    sap.add_argument("--list", "-l", action="store_true", dest="show_members",
                     help="inform to show the members in the room. "
                     "with the --email option, show the info of "
                     "the specific members")
    sap.add_argument("--add", "-a", action="store_true", dest="add_members",
                    help="with the --email-addrs option, inform to add members")
    sap.add_argument("--delete", "-d", action="store_true",
                    dest="delete_members",
                    help="with the --email-addrs option, "
                        "inform to delete members")
    sap.add_argument("--email", "-e", action="store", dest="_mail_addrs",
                    help="specify the member's email addresses "
                    "separated by a comma.")
    sap.set_defaults(func=member_functions)
    # message
    sap = subp.add_parser("message", aliases=["mes", "ms"],
                          help="the message management.")
    sap.add_argument("--token", "-t", action="store", dest="access_token",
                     help="specify the access token.")
    sap.add_argument("--room-id", "-r", action="store", dest="room_id",
                     help="specify the room id. "
                     "Ignored with the --email option.")
    sap.add_argument("--email", "-e", action="store", dest="_mail_addrs",
                     help="specify the recipient's email addresses "
                    "separated by a comma.")
    sap.add_argument("--message", "-m", action="store", dest="message",
                     help="specify a message to be sent.")
    sap.add_argument("--file", "-f", action="append", dest="_files", nargs="*",
                     help="specify a file to be sent. "
                        "specify multiple times to send multiple files. ")
    sap.add_argument("--list", "-l", action="store_true", dest="show_messages",
                     help="list the messages.  "
                     "Either the --since option or the --max option is required.")
    sap.add_argument("--since", "-a", action="store", dest="since",
                     help="specify ISO6801 datetime to be listed mails "
                     "after the datetime.")
    sap.add_argument("--max", action="store", dest="max_nb_mails",
                     type=int, default=16,
                     help="specify the number of mails to be listed.")
    sap.set_defaults(func=message_functions)
    # people
    sap = subp.add_parser("people", aliases=["peo", "pp"],
                          help="the people management. ")
    sap.add_argument("--token", "-t", action="store", dest="access_token",
                    help="specify the access token.")
    sap.add_argument("--email-addrs", "-e", action="store", dest="_mail_addrs",
                     metavar="MAIL_ADDRS",
                    help="specify the member's email addresses "
                    "separated by a comma. "
                    "it is required if you are not admin.")
    sap.add_argument("--detail", "-L", action="store_true", dest="show_detail",
                     help="specify to show a detail info.")
    sap.set_defaults(func=people_functions)
    #
    opt = ap.parse_args(argv)
    """
    if opt.config:
        config = json.load(open(opt.config))
    """
    # set the access token
    # the one specifyed by the option is preferred than the env variable.
    if opt.access_token is None:
        opt.access_token = os.environ.get("WEBEX_TEAMS_ACCESS_TOKEN", None)
        if opt.access_token is None:
            print("ERROR: access_token must be specified.")
            exit(0)
    # call a function.
    opt.func(opt, subp)

#
# main
#
if __name__ == "__main__" :
    import sys
    main(sys.argv[1:])

