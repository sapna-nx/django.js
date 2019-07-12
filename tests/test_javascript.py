
from tests.runners import JsTestCase, JsTemplateTestCase, JasmineSuite, QUnitSuite


class DjangoJsTests(JasmineSuite, JsTestCase):
    url_name = 'tests'


class JasmineTests(JasmineSuite, JsTestCase):
    url_name = 'jasmine_tests'


class JasmineTemplateTests(JasmineSuite, JsTemplateTestCase):
    js_files = 'test/jasmine/*Spec.js'


class QUnitTests(QUnitSuite, JsTestCase):
    url_name = 'qunit_tests'


class QUnitTemplateTests(QUnitSuite, JsTemplateTestCase):
    template_name = 'djangojs/test/qunit-test-runner.html'
    js_files = 'test/qunit/qunit-*.js'
