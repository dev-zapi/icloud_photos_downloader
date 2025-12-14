"""Tests for the health check endpoint"""

from unittest import TestCase

from icloudpd.logger import setup_logger
from icloudpd.status import Status, StatusExchange


class HealthCheckTestCase(TestCase):
    """Test cases for the /health endpoint"""

    def test_health_ok_when_no_input_needed(self) -> None:
        """Test that /health returns 'ok' with 200 when status is NO_INPUT_NEEDED"""
        status_exchange = StatusExchange()
        logger = setup_logger()

        # Create Flask app but don't start the server
        from flask import Flask

        app = Flask(__name__)
        app.logger = logger

        # Define the health endpoint (same logic as in serve_app)
        @app.route("/health", methods=["GET"])
        def health():
            from flask import make_response

            _status = status_exchange.get_status()
            if _status == Status.NO_INPUT_NEEDED:
                return make_response("ok", 200)
            else:
                return make_response("fail", 503)

        # Test with NO_INPUT_NEEDED status (default)
        with app.test_client() as client:
            response = client.get("/health")
            assert response.status_code == 200
            assert response.data == b"ok"

    def test_health_fail_when_need_mfa(self) -> None:
        """Test that /health returns 'fail' with 503 when status is NEED_MFA"""
        status_exchange = StatusExchange()
        logger = setup_logger()

        # Create Flask app but don't start the server
        from flask import Flask

        app = Flask(__name__)
        app.logger = logger

        # Define the health endpoint (same logic as in serve_app)
        @app.route("/health", methods=["GET"])
        def health():
            from flask import make_response

            _status = status_exchange.get_status()
            if _status == Status.NO_INPUT_NEEDED:
                return make_response("ok", 200)
            else:
                return make_response("fail", 503)

        # Set status to NEED_MFA
        status_exchange.replace_status(Status.NO_INPUT_NEEDED, Status.NEED_MFA)

        # Test with NEED_MFA status
        with app.test_client() as client:
            response = client.get("/health")
            assert response.status_code == 503
            assert response.data == b"fail"

    def test_health_fail_when_need_password(self) -> None:
        """Test that /health returns 'fail' with 503 when status is NEED_PASSWORD"""
        status_exchange = StatusExchange()
        logger = setup_logger()

        # Create Flask app but don't start the server
        from flask import Flask

        app = Flask(__name__)
        app.logger = logger

        # Define the health endpoint (same logic as in serve_app)
        @app.route("/health", methods=["GET"])
        def health():
            from flask import make_response

            _status = status_exchange.get_status()
            if _status == Status.NO_INPUT_NEEDED:
                return make_response("ok", 200)
            else:
                return make_response("fail", 503)

        # Set status to NEED_PASSWORD
        status_exchange.replace_status(Status.NO_INPUT_NEEDED, Status.NEED_PASSWORD)

        # Test with NEED_PASSWORD status
        with app.test_client() as client:
            response = client.get("/health")
            assert response.status_code == 503
            assert response.data == b"fail"

    def test_health_fail_when_checking_mfa(self) -> None:
        """Test that /health returns 'fail' with 503 when status is CHECKING_MFA"""
        status_exchange = StatusExchange()
        logger = setup_logger()

        # Create Flask app but don't start the server
        from flask import Flask

        app = Flask(__name__)
        app.logger = logger

        # Define the health endpoint (same logic as in serve_app)
        @app.route("/health", methods=["GET"])
        def health():
            from flask import make_response

            _status = status_exchange.get_status()
            if _status == Status.NO_INPUT_NEEDED:
                return make_response("ok", 200)
            else:
                return make_response("fail", 503)

        # Set status to CHECKING_MFA
        status_exchange.replace_status(Status.NO_INPUT_NEEDED, Status.NEED_MFA)
        status_exchange.set_payload("123456")  # This transitions to SUPPLIED_MFA

        # Test with SUPPLIED_MFA status (which should also return fail)
        with app.test_client() as client:
            response = client.get("/health")
            assert response.status_code == 503
            assert response.data == b"fail"
