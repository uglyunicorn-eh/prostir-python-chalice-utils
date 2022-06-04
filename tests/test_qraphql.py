from unittest import TestCase, mock

from graphql import ExecutionResult, GraphQLError
from prostir.chalice_utils.graphql.utils import translate_result


class TestTranslateResult(TestCase):
    @mock.patch("prostir.chalice_utils.graphql.utils.CustomResponse")
    def test_translate_result_error(self, CustomResponse):
        res = ExecutionResult(
            data=None,
            errors=[GraphQLError("Foo error")],
        )
        translate_result(res)
        CustomResponse.assert_called_once_with(
            {
                "data": None,
                "code": "GraphQLError",
                "message": "A GraphQL error occurred.",
                "errors": [
                    GraphQLError("Foo error"),
                ],
            },
            status_code=400,
        )

    @mock.patch("prostir.chalice_utils.graphql.utils.CustomResponse")
    def test_translate_result_success(self, CustomResponse):
        res = ExecutionResult(
            data={
                "foo": "bar",
            },
        )
        translate_result(res)
        CustomResponse.assert_called_once_with(
            {
                "data": {
                    "foo": "bar",
                },
                "code": "Success",
                "message": None,
                "errors": None,
            },
            status_code=200,
        )
