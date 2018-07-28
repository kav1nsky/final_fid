#!/usr/bin/env python
import os
import sys
import subprocess


def nodeos():
    return
    programm = "nodeos"

    args = ["--plugin eosio::wallet_api_plugin", "--plugin eosio::wallet_plugin", "--plugin eosio::producer_plugin",
            "--plugin eosio::history_plugin", "--plugin eosio::chain_api_plugin", "--plugin eosio::history_api_plugin",
            "--plugin eosio::http_plugin", "--replay-blockchain", "--hard-replay-blockchain", "--delete-all-blocks",
            "--enable-stale-production", "--producer-name eosio", "--contracts-console"]

    subprocess.Popen(" ".join([programm] + args), shell=True)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if "runserver" in sys.argv:
        nodeos()

    execute_from_command_line(sys.argv)
