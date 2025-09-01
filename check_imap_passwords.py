#!/usr/bin/env python3
import argparse
import csv
import imaplib
import socket
import ssl
from getpass import getpass
from typing import Optional, Tuple

DEFAULT_TIMEOUT = 15  # seconds

class Result:
    def __init__(self, account_label: str, ok: bool, detail: str):
        self.account_label = account_label
        self.ok = ok
        self.detail = detail

    def __str__(self):
        status = "✅ OK" if self.ok else "❌ FAIL"
        return f"[{status}] {self.account_label}: {self.detail}"

def try_imap_login(
    server: str,
    username: str,
    password: str,
    port: int,
    security: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> Result:
    label = f"{username}@{server}:{port} ({security})"
    socket.setdefaulttimeout(timeout)

    try:
        if security.lower() == "ssl":
            imap = imaplib.IMAP4_SSL(host=server, port=port)
        else:
            imap = imaplib.IMAP4(host=server, port=port)
            if security.lower() == "starttls":
                imap.starttls(ssl_context=ssl.create_default_context())
            elif security.lower() != "plain":
                return Result(label, False, "Unknown security type (use ssl|starttls|plain)")

        typ, _ = imap.login(username, password)
        if typ != "OK":
            try:
                imap.logout()
            except Exception:
                pass
            return Result(label, False, f"Login failed: server returned {typ}")

        # optional: sanity check a simple command
        typ, _ = imap.select(readonly=True)
        imap.logout()
        return Result(label, True, "Authenticated and IMAP responded normally")

    except imaplib.IMAP4.error as e:
        # Often indicates auth failure; IMAP servers sometimes return descriptive text
        return Result(label, False, f"IMAP error: {str(e)}")
    except ssl.SSLError as e:
        return Result(label, False, f"TLS/SSL error: {e}")
    except socket.gaierror as e:
        return Result(label, False, f"DNS/host error: {e}")
    except (ConnectionRefusedError, TimeoutError, socket.timeout) as e:
        return Result(label, False, f"Network error: {e}")
    except Exception as e:
        return Result(label, False, f"Unexpected error: {type(e).__name__}: {e}")

def parse_security(s: Optional[str]) -> str:
    if not s:
        return "ssl"
    s = s.strip().lower()
    if s in {"ssl", "starttls", "plain"}:
        return s
    raise ValueError("security must be one of: ssl, starttls, plain")

def prompt_password(prompt_label: str) -> str:
    return getpass(f"Enter password for {prompt_label}: ")

def run_single(args) -> int:
    security = parse_security(args.security)
    password = args.password or prompt_password(f"{args.username}@{args.server}")
    result = try_imap_login(
        server=args.server,
        username=args.username,
        password=password,
        port=args.port,
        security=security,
        timeout=args.timeout,
    )
    print(result)
    return 0 if result.ok else 2

def run_csv(args) -> int:
    failures = 0
    with open(args.csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"server", "username"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"CSV is missing required columns: {', '.join(sorted(missing))}")

        # Optional columns with defaults
        # port (int), security (ssl|starttls|plain), label (for display)
        for row in reader:
            server = row["server"].strip()
            username = row["username"].strip()
            label = row.get("label", "").strip() or f"{username}@{server}"
            security = parse_security(row.get("security", "ssl"))
            try:
                port = int(row.get("port", "993" if security == "ssl" else "143"))
            except ValueError:
                print(f"Skipping {label}: invalid port '{row.get('port')}'")
                failures += 1
                continue

            password = prompt_password(label)
            result = try_imap_login(
                server=server,
                username=username,
                password=password,
                port=port,
                security=security,
                timeout=args.timeout,
            )
            print(result)
            if not result.ok:
                failures += 1

    return 0 if failures == 0 else 2

def main():
    p = argparse.ArgumentParser(
        description="Verify IMAP passwords safely (no passwords stored)."
    )
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--csv", help="Path to CSV with accounts (server,username[,port,security,label])")
    mode.add_argument("--server", help="IMAP server hostname (e.g., imap.example.com)")

    p.add_argument("--username", help="Username (email address)")
    p.add_argument("--port", type=int, help="IMAP port (default: 993 for ssl, 143 otherwise)")
    p.add_argument("--security", default="ssl", help="ssl|starttls|plain (default: ssl)")
    p.add_argument("--password", help="Password (not recommended; prefer interactive prompt)")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Network timeout seconds (default: 15)")

    args = p.parse_args()

    if args.csv:
        exit(run_csv(args))
    else:
        if not args.username:
            raise SystemExit("--username is required with --server")
        if args.port is None:
            args.port = 993 if parse_security(args.security) == "ssl" else 143
        exit(run_single(args))

if __name__ == "__main__":
    main()
