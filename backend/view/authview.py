from config import ERRCODE
from model.user import USER_LEVEL
from view import AjaxLoginView


class _AjaxPermissionView(AjaxLoginView):
    _level = USER_LEVEL.NORMAL

    def prepare(self):
        if not self.current_user():
            return self.finish({'code': ERRCODE.NOT_USER})
        elif self.current_user().level != self._level:
            return self.finish({'code': ERRCODE.PERMISSION_DENIED})
        super(_AjaxPermissionView, self).prepare()


class AjaxNormalView(_AjaxPermissionView):
    _level = USER_LEVEL.NORMAL


class AjaxWriterView(_AjaxPermissionView):
    _level = USER_LEVEL.WRITER


class AjaxAdminView(_AjaxPermissionView):
    _level = USER_LEVEL.ADMIN
