from src.app.infrastructure.session_manager import InMemorySessionManager

def test_session_manager_basic():
    sm = InMemorySessionManager()
    sm.add("sid", "chat_obj")
    assert sm.get("sid") == "chat_obj"
    sm.remove("sid")
    assert sm.get("sid") is None

def test_get_nonexistent_session():
    sm = InMemorySessionManager()
    assert sm.get("doesnotexist") is None