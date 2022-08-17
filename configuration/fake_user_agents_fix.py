import fake_useragent
import inspect

changed_code_str = inspect.getsource(fake_useragent.utils.get_browsers).replace(
    '<table class="w3-table-all notranslate">', '<table class="ws-table-all notranslate">')
exec(changed_code_str)
fake_useragent.utils.get_browsers = get_browsers
