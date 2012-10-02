var loaded_fonts = {};
var displayed_fonts = {};
var current_timeouts = {}

add_font_to_page = function(name, font, display) {
    if(!loaded_fonts.hasOwnProperty(name)) {
        loaded_fonts[name] = 1;
        $('head').append(font.style);
    }
    if(display) {
        if (display && $('#playground').css('display') == 'none') {
            $('#playground').css('display', 'block');
        }
        if (!displayed_fonts.hasOwnProperty(name)) {
            displayed_fonts[name] = 1;
            $('#playground').append(font.sample);
        }
    }
}

clear_all = function(ignore_font_name) {
    var _sr = $('#search_result');
    displayed_fonts = {};
    $('#playground').css('display', 'none');
    $('#playground').empty();
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
    if(crit=='') {
        set_search_element(_st, 'Please input at least some text', 'error', 3000);
    } else {
        $.post('/search_font', {'font_name': crit}, function(data, status) {
            var count = data.count;
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
                add_font_to_page(name, font, true);
            });
        }, 'json');
    }
    $('#font_name').focus();
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
            add_font_to_page(name, font, false);
        });
        set_search_element(_st, 'all fonts loaded !!!', 'standard', 2000);
        $('#load_all').remove();
    }, 'json');
}
