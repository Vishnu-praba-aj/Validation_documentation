import threading

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()

    def add(self, session_id, chat):
        with self.lock:
            self.sessions[session_id] = chat

    def get(self, session_id):
        with self.lock:
            return self.sessions.get(session_id)

    def remove(self, session_id):
        with self.lock:
            if session_id in self.sessions:
                del self.sessions[session_id]

session_manager = SessionManager()