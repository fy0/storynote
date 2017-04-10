
import state from "./state.js"

$.get_time = function (timestamp) {
    var date;
    date = new Date();
    date.setTime(timestamp * 1000);
    //return date.toLocaleString();
    return date.format('yyyy-MM-dd');
};

Date.prototype.format = function (format) {
    var date, k;
    date = {
        'M+': this.getMonth() + 1,
        'd+': this.getDate(),
        'h+': this.getHours(),
        'm+': this.getMinutes(),
        's+': this.getSeconds(),
        'q+': Math.floor((this.getMonth() + 3) / 3),
        'S+': this.getMilliseconds()
    };
    if (/(y+)/i.test(format)) {
        format = format.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length));
    }
    for (k in date) {
        if (new RegExp('(' + k + ')').test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length === 1 ? date[k] : ('00' + date[k]).substr(('' + date[k]).length));
        }
    }
    return format;
};

$.time_to_text = function (timestamp) {
    var date, now, offset, str;
    timestamp = Number(timestamp);
    if (timestamp === 0) {
        return '从未';
    }
    date = new Date();
    now = date.getTime() / 1000;
    offset = now - timestamp;
    str = (function() {
        switch (false) {
            case !(offset < 30):
                return '刚刚';
            case !(offset < 60):
                return '一分钟内';
            case !(offset < 60 * 60):
                return Math.floor(offset / 60) + '分钟前';
            case !(offset < 60 * 60 * 24):
                return Math.floor(offset / (60 * 60)) + '小时前';
            case !(offset < 60 * 60 * 24 * 30):
                return Math.floor(offset / (60 * 60 * 24)) + '天前';
            case !(offset < 60 * 60 * 24 * 30 * 12):
                return Math.floor(offset / (60 * 60 * 24 * 30)) + '月前';
            case !(offset < 60 * 60 * 24 * 30 * 12 * 20):
                return (offset / (60 * 60 * 24 * 30 * 12)).toFixed(1) + '年前';
            default:
                date.setTime(timestamp * 1000);
                return date.format('yyyy-MM-dd');
        }
    })();
    return str;
};

$.time_replace = function () {
    var i, item, j, len, ref;
    ref = $('time[timestamp]');
    for (j = 0, len = ref.length; j < len; j++) {
        i = ref[j];
        item = $(i);
        item.text($.time_to_text(item.attr('timestamp')));
    }
};

$.is_login = function() {
    return $.cookie('u') !== undefined;
};


$.message = function (type, text) {
    // type: default, secondary, success, warning, error
    let convert = {
        'default': '',
        'secondary': 'am-alert-secondary',
        'success': 'am-alert-success',
        'warning': 'am-alert-warning',
        'error': 'am-alert-danger',
    }
    let data = {type, text, class: convert[type]};
    state.data.msgs.push(data);
    _.delay(() => {
        state.data.msgs.splice(state.data.msgs.indexOf(data), 1);
    }, 3000);
}

$.message_text = function (text) {
    $.message('default', text);
}

$.message_secondary = function (text) {
    $.message('secondary', text);
}

$.message_success = function (text) {
    $.message('success', text);
}

$.message_warning = function (text) {
    $.message('warning', text);
}

$.message_error = function (text) {
    $.message('error', text);
}
