import datetime
import json

import pandas as pd
from flask import Flask, request, render_template

log_file_name = "logs/formatted.csv"

app = Flask(__name__)


class Log(object):
    class LogLevels(object):
        info = "INFO"
        warning = "WARN"
        error = "ERROR"
        debug = "DEBUG"

    time, logger, level, ip, data, form = "", "", "", "", "", ""

    def __init__(self, level, logger, ip, form, data, time=datetime.datetime.now(), extra=None):
        self.time, self.logger, self.level, self.ip, self.data, self.form, self.extra = \
            time, logger, level, ip, data, form, extra

    @staticmethod
    def from_request(level, request):
        return Log(level=level, logger=__name__, ip=request.remote_addr, form=json.dumps(request.form),
                   data=json.dumps(request.args))

    def __iter__(self):
        return iter([self.time, self.logger, self.level, self.ip, self.data, self.form, self.extra])

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}".format(self.time, self.logger, self.level, self.ip, self.data, self.form,
                                                   self.extra)

    @staticmethod
    def get_current_logs():
        try:
            return pd.read_csv(log_file_name)
        except pd.errors.EmptyDataError as e:
            field_names = ["time", "logger", "level", "ip", "data", "form"]
            return pd.DataFrame(columns=field_names)

    @staticmethod
    def write_logs(logs_list: list, filename):
            current_logs = Log.get_current_logs()
            logs_list = [l.to_dict() for l in logs_list]
            new_logs = current_logs.append(logs_list)
            with open(filename, "w+") as f:
                f.write(new_logs.to_csv())

    def to_dict(self):
        return {
            "time": self.time,
            "logger": self.logger,
            "level": self.level,
            "ip": self.ip,
            "data": self.data,
            "form": self.form
        }


@app.route('/', methods=["POST", 'PATCH', 'PUT', 'GET'])
def logger():
    if request.method in "GET":
        logs = Log.get_current_logs()
        return logs.to_json(orient='index')
    else:
        log = Log.from_request(Log.LogLevels.info, request)
        Log.write_logs([log, ], filename=log_file_name)
        return str(log)
