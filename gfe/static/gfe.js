var current_timeouts = {};

function FontsManager() {
    this.name = 'FontsManager';
    this.MAX_LOADED = 10;
    this.displayed_fonts = [];
    this.fonts_index = [];
    this.fonts_data = {};
}

FontsManager.prototype = {
    test: function() {
        return this;
    },
    add_font: function(name, font, display) {
        if(this.fonts_index.indexOf(name) === -1) {
            this.fonts_index.push(name);
            this.fonts_data[name] = font;
        }
        if(display) {
            this.display_font(name);
        }
    },
    get_font: function(name) {
        return this.fonts_data[name];
    },
    many_fonts: function(names) {
        var result = [];
        for (var idx = 0; idx < names.length; idx++) {
            result.push(this.get_font(names[idx]));
        };
        return result;
    },
    has_font: function(name) {
        return this.fonts_data.hasOwnProperty(name);
    },
    slice_fonts: function(begin, end) {
        return this.fonts_index.slice(begin, end)
    },
    clear_displayed: function() {
        this.displayed_fonts = [];
        this.fonts_index = [];
        $('#playground').css('display', 'none');
        $('#playground').empty();
    },
    clear_all: function() {
        this.clear_displayed();
        this.fonts_data = {};
    },
    display_font: function(font) {
        if (this.displayed_fonts.indexOf(font) === -1) {
            this.displayed_fonts.push(font);
        }
        $('head').append(font.style);
        $('#playground').append(font.sample);
        if ($('#playground').css('display') == 'none') {
            $('#playground').css('display', 'block');
        }
    },
    more_fonts: function() {
        var current = this.displayed_fonts.length;
        if(this.fonts_index.length > current) {
            var fonts = this.many_fonts(this.slice_fonts(current, current+this.MAX_LOADED));
            for (var idx = 0; idx < fonts.length; idx++) {
                this.display_font(fonts[idx]);
            };
        }
    }
}

clear_all = function(ignore_font_name) {
    var _sr = $('#search_result');
    fmgr.clear_displayed();
    if(!ignore_font_name) {
        $('#font_name').val('');
    }
    set_search_element($('#search_status'), '&nbsp;');
    if(_sr.hasClass('bordered')) {
        _sr.removeClass('bordered');
    }
    set_search_element(_sr, '&nbsp;');
}

set_search_element = function(obj, value, state, timeout) {
    if(state=='error') {
        obj.addClass('error');
    } else {
        obj.removeClass('error');
    }
    if(timeout>0) {
        if(current_timeouts.hasOwnProperty(obj)) {
            window.clearTimeout(current_timeouts[obj]);
            delete current_timeouts[obj];
        }
        t_out = window.setTimeout(function () {
             obj.empty();
        }, timeout);
        current_timeouts[obj] = t_out
    }
    obj.empty();
    obj.append(value);
}

let_the_magic_talk = function() {
    var _st = $('#search_status');
    var _sr = $('#search_result');
    var crit = $('#font_name').val().trim();
    var count = 0;
    if(crit=='') {
        set_search_element(_st, 'Please input at least some text', 'error', 3000);
    } else {
        $.post('/search_font', {'font_name': crit}, function(data, status) {
            count = data.count;
            if(count==0) {
                var msg = 'no font matching criteria !';
                set_search_element(_st, msg, 'standard', 5000);
            } else {
                clear_all(true);
                var msg = count + ' font' + (count==1?'':'s') +' matching !';
                set_search_element(_sr, msg);
                _sr.addClass('bordered');
            }
            $.each(data.fonts, function(name, font) {
                fmgr.add_font(name, font);
            });
            fmgr.more_fonts();
        }, 'json');
    }
    $('#font_name').focus();
    return count;
}

check_validation = function(event) {
    if (event.keyCode==13) {
        let_the_magic_talk();
    }
}

load_all_the_f_____g_stuff = function() {
    var _st = $('#search_status');
    set_search_element(_st, 'loading all fonts ...', 'standard');
    $.post('/search_font', {'_all_fonts': 'go_for_it'}, function(data, status) {
        $.each(data.fonts, function(name, font) {
            fmgr.add_font(name, font);
        });
        set_search_element(_st, 'all fonts loaded !!!', 'standard', 2000);
        $('#load_all').remove();
    }, 'json');
}

var spinner_options = {
  lines: 13,
  length: 5,
  width: 17,
  radius: 36,
  corners: 0.7,
  rotate: 0,
  color: '#000000',
  speed: 1.7,
  trail: 35,
  shadow: false,
  hwaccel: true,
  className: 'spinner',
  zIndex: 2e9,
  top: 'auto',
  left: 'auto',
};

call_with_spinner = function(fcn) {
    // display container before 'spinning'
    // else spinner is not centered
    var loading = $('#loading');
    loading.show();
    var spinner = loading.spin(spinner_options);
    window.setTimeout(function() {
        fcn();
        window.setTimeout(function (){
            spinner.stop();
            loading.hide();
        }, 500);
    }, 100);
}
