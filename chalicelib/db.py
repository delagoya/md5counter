
class Md5Counter(object):
    def incr_error(self):
        pass
    def get_error(self):
        pass
    def incr_success(self):
        pass
    def get_success(self):
        pass
    def reset_counters(self):
        pass

class LocalMd5Counter(Md5Counter):
    def __init__(self, state=None):
        if state is None:
            state = {"error": 0, "success": 0}
        self._state = state

    def _incr(self,k):
        self._state[k] = self._state[k] + 1
        return self._state[k]
    def incr_error(self):
        return self._incr("error")
    def get_error(self):
        return self._state["error"]
    def incr_success(self):
        return self._incr("success")
    def get_success(self):
        return self._state["success"]
    def reset_counters(self):
        self._state = {"error": 0, "success": 0}

class DDBMd5Counter(Md5Counter):
    def __init__(self, table_resource):
        self._table = table_resource

    def _incr(self,key):
        self._table.update_item(
            Key={"status": key},
            UpdateExpression="SET n = n + :incr",
            ExpressionAttributeValues={":incr": 1}
        )
    def _get_value(self, key):
        i = self._table.get_item(Key={"status":key})
        return int(i["Item"]['n'])

    def incr_error(self):
        self._incr("error")
        return self.get_error()

    def get_error(self):
        return self._get_value("error")

    def incr_success(self):
        self._incr("success")
        return self.get_success()

    def get_success(self):
        return self._get_value("success")

    def reset_counters(self):
        for k in ["success","error"]:
            self._table.update_item(
                Key={"status": k},
                UpdateExpression="SET n = :zero",
                ExpressionAttributeValues={":zero": 0}
            )
