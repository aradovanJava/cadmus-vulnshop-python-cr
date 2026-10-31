"""Audit logging."""
import logging

# -- M17 [A09] the logger is configured so that nothing is emitted --------
#    Level CRITICAL means every security event below it is discarded.
logging.basicConfig(level=logging.CRITICAL)
log = logging.getLogger("vulnshop.audit")


def record(event: str, detail: str) -> None:
    """-- T16 [A09] log injection through an interpolated format string ---
    detail is user-controlled and unescaped, so a newline lets an attacker
    forge log entries that are indistinguishable from genuine ones.
    """
    log.info("event=%s detail=" % event + detail)


def record_login_failure(username: str) -> None:
    # -- M10 [A07] failed logins are counted nowhere and alerted on never --
    pass
