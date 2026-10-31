"""Entry point for the CR1-CR4 training application."""
from vulnshop import create_app

app = create_app()

if __name__ == "__main__":
    print("=" * 70)
    print(" cadmus-vulnshop-cr  ·  DELIBERATELY VULNERABLE TRAINING BUILD")
    print(" Sandbox only. Contains an unauthenticated RCE path.")
    print(" http://127.0.0.1:8080/shop   accounts: alice/bob/carol/adminjoe")
    print(" password: Password123")
    print("=" * 70)
    # bound to loopback deliberately — do not change
    app.run(host="127.0.0.1", port=8080, debug=False)
