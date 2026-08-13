#!/usr/bin/env python3
"""Session supervision (SPEC-0085) — the distinguishing hop.

SPEC-0085 is explicit that submitting a prompt and awaiting completion fails the
criterion by definition. What has to be demonstrated on a *live* session is three
things: interrupting generation in flight with the session surviving, injecting an
instruction that observably changes what happens next, and terminating cleanly with an
exit status and a final telemetry event.

That requires holding the session's stdin for its whole life, which is why the CLI runs
in `--input-format stream-json` mode: the harness writes user messages and control
requests onto the stream while output frames come back, rather than handing over a
prompt and waiting. The container's stdin is inherited by the payload through init, so
the harness talks to the session without any new hole in the L0 surface (L0-021).

Provider-agnostic by construction: the supervisor speaks to the CLI, and the CLI speaks
to whatever the adapter points at. The acceptance evidence is produced against the
pinned Anthropic configuration; the same code path is re-run against another provider
as a portability check, and the evidence rows name which.
"""
import json
import queue
import subprocess
import threading
import time


class Session:
    """A live CLI session the harness holds open and steers."""

    def __init__(self, docker_args, cli_args, on_frame=None):
        self.docker_args = list(docker_args)
        self.cli_args = list(cli_args)
        self.on_frame = on_frame
        self.frames = []
        self.raw = []
        self.proc = None
        self._q = queue.Queue()
        self._reader = None
        self._stderr = []

    # -- lifecycle -------------------------------------------------------
    def start(self):
        self.proc = subprocess.Popen(
            self.docker_args + self.cli_args,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1)
        self._reader = threading.Thread(target=self._read_stdout, daemon=True)
        self._reader.start()
        threading.Thread(target=self._read_stderr, daemon=True).start()
        return self

    def _read_stdout(self):
        for line in self.proc.stdout:
            line = line.strip()
            if not line:
                continue
            self.raw.append(line)
            # init prefixes captured payload output; the frame is what follows.
            if line.startswith("[stdout] "):
                line = line[len("[stdout] "):]
            try:
                frame = json.loads(line)
            except ValueError:
                continue
            self.frames.append(frame)
            self._q.put(frame)
            if self.on_frame:
                self.on_frame(frame)

    def _read_stderr(self):
        for line in self.proc.stderr:
            self._stderr.append(line.rstrip())

    # -- steering --------------------------------------------------------
    def send_user(self, text):
        """Inject a user message mid-session. This is the injection SPEC-0085 wants:
        the session is already running and already has state; the harness adds a turn."""
        self._write({"type": "user",
                     "message": {"role": "user", "content": [{"type": "text", "text": text}]}})

    def interrupt(self, request_id="int-1"):
        """Interrupt in-flight generation without ending the session.

        The CLI advertises `interrupt_receipt_v1` in its init frame, so the control
        request is the supported path — signalling the process would terminate it, which
        is the opposite of what the criterion asks for.
        """
        self._write({"type": "control_request", "request_id": request_id,
                     "request": {"subtype": "interrupt"}})

    def _write(self, obj):
        self.proc.stdin.write(json.dumps(obj) + "\n")
        self.proc.stdin.flush()

    # -- observation -----------------------------------------------------
    def wait_for(self, predicate, timeout=120):
        """Wait for a frame satisfying `predicate`, returning it or None on timeout."""
        deadline = time.time() + timeout
        for frame in list(self.frames):
            if predicate(frame):
                return frame
        while time.time() < deadline:
            try:
                frame = self._q.get(timeout=min(2, max(0.1, deadline - time.time())))
            except queue.Empty:
                continue
            if predicate(frame):
                return frame
        return None

    def text_of(self, frame):
        if frame.get("type") != "assistant":
            return ""
        return " ".join(b.get("text", "") for b in frame["message"].get("content", [])
                        if b.get("type") == "text")

    def assistant_text(self):
        return " ".join(self.text_of(f) for f in self.frames if f.get("type") == "assistant")

    # -- termination -----------------------------------------------------
    def terminate(self, timeout=60):
        """Close the stream and let the session end on its own terms.

        Closing stdin is the clean path: the CLI finishes what it is doing and exits,
        so the exit status means something. Killing the process would also stop it, and
        would tell us nothing about whether the session could end well.
        """
        try:
            self.proc.stdin.close()
        except (BrokenPipeError, ValueError):
            pass
        try:
            code = self.proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            code = self.proc.wait(timeout=30)
            return {"exit_status": code, "clean": False,
                    "reason": "session did not end on stdin close; killed"}
        return {"exit_status": code, "clean": code == 0,
                "reason": "ended on stdin close"}

    @property
    def stderr(self):
        return "\n".join(self._stderr)


def cli_session_args(base_url, model, extra=()):
    """The session-mode invocation. `--verbose` is load-bearing for uninterrupted stream
    capture and is one of the two watched instabilities SPEC-0086 re-probes on every pin
    bump; the other is that bare/default mode silently drops configured hooks."""
    return ["/cli/bin/claude", "-p",
            "--input-format", "stream-json", "--output-format", "stream-json",
            "--verbose", "--replay-user-messages", "--model", model, *extra]
