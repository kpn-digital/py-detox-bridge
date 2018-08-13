from textwrap import dedent

from detox_bridge import js, node
from pytest import raises


def test_node_which_pick_up_installed_node(node_environment):
    assert node_environment.which().endswith("v8.11.3/bin/node")


def test_node_server_responds_with_a_timeout_error_if_code_executioin_takes_longer_than_default_timeout(node_server):
    node_server.default_timeout = 4
    with raises(node.TimeoutError):
        node_server("while(true);")


def test_node_allows_for_default_timeout_overidden_by_timeout_in_call(node_server):
    sleep_for_5_seconds_and_return_4 =\
        "return new Promise((resolve) => { setTimeout(()=> { console.error(\"resolved\"); resolve(4); }, 5000); });"

    node_server.default_timeout = 10
    assert node_server(sleep_for_5_seconds_and_return_4) == 4

    with raises(node.TimeoutError):
        assert node_server(sleep_for_5_seconds_and_return_4, timeout=1)


def test_node_server_executes_code_keeping_global_state(node_server):
    assert node_server("global.b=1+3; return global.b;", timeout=5) == 4
    assert node_server("return global.b;", timeout=5) == 4


def test_node_server_executes_code_without_return(node_server):
    assert node_server("global.b=1+3;", timeout=5) is None
    assert node_server("return global.b;", timeout=5) == 4


def test_node_server_executes_uses_str_if_object_is_JSObject(node_server):
    node_server(js.Identifier("global").b, timeout=5)


def test_node_server_executes_code_reporting_exceptions_and_then_we_can_execute_another_statement(node_server):
    with raises(node.NodeError) as excinfo:
        node_server("throw new Error('hello')", timeout=5)
    assert excinfo.value.message == "hello"
    assert excinfo.value.stack

    node_server("return 4") == 4


def test_node_error_str_prints_multiline_exceptions_nicely():
    assert str(node.NodeError({
        "stack": "Line 1\nLine 2",
    })) == dedent("""\
    stack:
      Line 1
      Line 2""")


def test_node_error_str_prints_numbers():
    assert str(node.NodeError({
        "code": 127
    })) == dedent("""\
    code: 127""")
