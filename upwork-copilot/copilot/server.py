"""Local JSON API + static UI. Binds to 127.0.0.1 only; nothing here talks to Upwork."""
import json
import os
import re
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import analytics, db, drafting, scoring

STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
ALLOWED_HOSTS = {"localhost", "127.0.0.1", "[::1]"}


class Handler(BaseHTTPRequestHandler):
    server_version = "UpworkCopilot/1.0"

    def log_message(self, *a):
        pass

    # ---- helpers
    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > 1_000_000:
            raise ValueError("body too large")
        return json.loads(self.rfile.read(n) or b"{}")

    def _host_ok(self):
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0] if not (self.headers.get("Host") or "").startswith("[") \
            else (self.headers.get("Host") or "").split("]")[0] + "]"
        return host in ALLOWED_HOSTS

    def _dispatch(self, method):
        if not self._host_ok():  # blocks DNS-rebinding against the local API
            return self._json(403, {"error": "forbidden host"})
        path = self.path.split("?")[0]
        if method == "GET" and not path.startswith("/api/"):
            return self._static(path)
        if method != "GET" and "application/json" not in (self.headers.get("Content-Type") or ""):
            return self._json(415, {"error": "Content-Type must be application/json"})
        conn = db.connect(self.server.db_path)
        try:
            result = route(conn, method, path, self._body() if method != "GET" else {})
            if result is None:
                return self._json(404, {"error": "not found"})
            return self._json(200, result)
        except (ValueError, KeyError) as e:
            return self._json(400, {"error": str(e)})
        except Exception as e:  # pragma: no cover
            return self._json(500, {"error": f"{type(e).__name__}: {e}"})
        finally:
            conn.close()

    def _static(self, path):
        name = "index.html" if path in ("/", "") else path.lstrip("/")
        full = os.path.normpath(os.path.join(STATIC, name))
        if not full.startswith(STATIC + os.sep) or not os.path.isfile(full):
            return self._json(404, {"error": "not found"})
        ctype = {"html": "text/html", "js": "text/javascript", "css": "text/css"}.get(full.rsplit(".", 1)[-1], "application/octet-stream")
        data = open(full, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    do_GET = lambda self: self._dispatch("GET")
    do_POST = lambda self: self._dispatch("POST")
    do_PUT = lambda self: self._dispatch("PUT")
    do_PATCH = lambda self: self._dispatch("PATCH")
    do_DELETE = lambda self: self._dispatch("DELETE")


def route(conn, method, path, body):
    """Pure routing function so the API can be tested without HTTP."""
    if path == "/api/dashboard" and method == "GET":
        return analytics.dashboard(conn)
    if path == "/api/profile":
        if method == "GET":
            p = db.get_profile(conn)
            return {"profile": p, "audit": scoring.audit_profile(p, db.list_jobs(conn)), "versions": db.list_versions(conn)}
        if method == "PUT":
            p = db.save_profile(conn, body, note=body.get("_note", ""))
            return {"profile": p, "audit": scoring.audit_profile(p, db.list_jobs(conn)), "versions": db.list_versions(conn)}
    if path == "/api/jobs/parse" and method == "POST":
        return scoring.parse_job_text(body.get("text", ""))
    if path == "/api/jobs":
        if method == "GET":
            return {"jobs": db.list_jobs(conn)}
        if method == "POST":
            return db.add_job(conn, body)
    m = re.fullmatch(r"/api/jobs/(\d+)", path)
    if m:
        jid = int(m.group(1))
        if method == "GET":
            return db.get_job(conn, jid)
        if method == "DELETE":
            db.delete_job(conn, jid)
            return {"ok": True}
    m = re.fullmatch(r"/api/jobs/(\d+)/draft", path)
    if m and method == "POST":
        job = db.get_job(conn, int(m.group(1)))
        if not job:
            raise KeyError("job not found")
        counts = {}
        for r in conn.execute("SELECT variant, COUNT(*) c FROM proposals GROUP BY variant").fetchall():
            counts[r["variant"]] = r["c"]
        variant = body.get("variant") if body.get("variant") in drafting.VARIANTS else drafting.pick_variant(counts)
        text, source = drafting.draft(db.get_profile(conn), job, variant)
        return db.create_proposal(conn, job["id"], text, variant, source)
    if path == "/api/proposals" and method == "GET":
        return {"proposals": db.list_proposals(conn)}
    m = re.fullmatch(r"/api/proposals/(\d+)", path)
    if m and method == "PATCH":
        return db.update_proposal(conn, int(m.group(1)), body)
    if path == "/api/earnings":
        if method == "GET":
            return {"earnings": db.list_earnings(conn)}
        if method == "POST":
            db.add_earning(conn, body.get("amount"), body.get("date"), body.get("proposal_id"), body.get("note", ""))
            return {"earnings": db.list_earnings(conn)}
    if path == "/api/goal":
        month = analytics.month_of()
        if method == "GET":
            return db.get_goal(conn, month)
        if method == "PUT":
            db.set_goal(conn, month, body.get("revenue_target"), body.get("avg_contract_value"))
            return analytics.pacing(conn)
    return None


def serve(host="127.0.0.1", port=8765, db_path=None):
    srv = ThreadingHTTPServer((host, port), Handler)
    srv.db_path = db_path
    print(f"Upwork Copilot running at http://{host}:{port}  (Ctrl+C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
