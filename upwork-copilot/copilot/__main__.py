import argparse
import json
import sys

from . import analytics, db, server


def main(argv=None):
    ap = argparse.ArgumentParser(prog="copilot", description="Upwork Copilot (human-in-the-loop)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("serve", help="start the local web app")
    s.add_argument("--port", type=int, default=8765)
    s.add_argument("--host", default="127.0.0.1")
    sub.add_parser("report", help="print the weekly optimisation report (cron-friendly)")
    sub.add_parser("demo", help="load example data into an empty database")
    a = ap.parse_args(argv)
    if a.cmd == "serve":
        server.serve(a.host, a.port)
    elif a.cmd == "report":
        print(analytics.weekly_report(db.connect()))
    elif a.cmd == "demo":
        from .demo import load_demo
        print(json.dumps(load_demo(db.connect()), indent=2))


if __name__ == "__main__":
    sys.exit(main())
