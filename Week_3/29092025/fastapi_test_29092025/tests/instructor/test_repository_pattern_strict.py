import inspect

def test_services_use_repository_pattern():
    import app.services.practitioner_service as ps
    import app.services.slot_service as ss
    import app.db.repository as repo

    pcls = ps.PractitionerService
    scls = ss.SlotService
    assert "db" in inspect.signature(pcls.__init__).parameters
    assert "db" in inspect.signature(scls.__init__).parameters

    src_p = inspect.getsource(pcls)
    src_s = inspect.getsource(scls)
    assert "Repository(" in src_p or "Repository[" in src_p, "PractitionerService should initialize a Repository"
    assert "Repository(" in src_s or "Repository[" in src_s, "SlotService should initialize a Repository"

    svc = pcls(db=None)
    assert hasattr(svc, "get") and hasattr(svc, "list") and hasattr(svc, "create") and hasattr(svc, "update") and hasattr(svc, "delete")
