import argparse

from app.cli.profile_cli import run as run_profile

from app.cli.match_cli import run as run_match

from app.cli.resume_cli import run as run_resume

from app.cli.cover_letter_cli import (
    run as run_cover_letter
)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "command",
        help="""
        Available commands:

        profile
        match
        resume
        cover-letter
        """
    )

    args = parser.parse_args()

    if args.command == "profile":

        run_profile()

    elif args.command == "match":

        run_match()

    elif args.command == "resume":

        run_resume()

    elif args.command == "cover-letter":

        run_cover_letter()

    else:

        print("Unknown command")


if __name__ == "__main__":
    main()