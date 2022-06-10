from unittest import TestCase, mock

from prostir.chalice_utils.sentry import setup_sentry


class TestSentry(TestCase):
    @mock.patch("prostir.chalice_utils.sentry.sentry_sdk.init")
    def test_init_once(self, sentry_sdk_init):
        setup_sentry(
            dsn="https://example.com/",
            release="0.0.1",
            environment="zone",
        )
        sentry_sdk_init.assert_called_once_with(
            dsn="https://example.com/",
            integrations=[mock.ANY],
            release="0.0.1",
            environment="zone",
        )
        sentry_sdk_init.reset_mock()
        setup_sentry(
            dsn="https://example.com/fooo",
            release="0.0.1",
            environment="zone",
        )
        sentry_sdk_init.assert_not_called()
