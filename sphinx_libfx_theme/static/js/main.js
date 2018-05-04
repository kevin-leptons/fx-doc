var sk_mode_normal = 0;
var sk_mode_search = 1;
var sk_mode_goto = 2;

var msg_linfo = 0;
var msg_lsuccess = 1;
var msg_lwarning = 2;
var msg_ldanger = 3;

var msg_duration = 3000;
var msg_timer = null;

var kb_key_esc = 27;            // escape
var kb_key_search = 192;        // back qoute
var kb_key_info = 73;           // i
var kb_key_goto = 71;           // g
var kb_key_help = 72;           // h
var kb_key_downloads = 68;      // d
var kb_key_toc = 84;            // t
var kb_key_next_section = 78;   // n
var kb_key_prev_section = 80;   // p
var kb_key_parent_section = 85; // u
var kb_key_doc_source = 82;     // r

var sk_now_mode = null;
var sk_goto_items = null
var sk_goto_index = null
var sk_goto_label = null
var sk_goto_label_selected = null

var now_section_node = null;
var search_input_node = null;
var mode_node = null;
var content_body_node = null;
var code_node = null;
var msg_box_node = null;
var msg_box_content_node = null;

//trigger entry point when it is possible
document.addEventListener("DOMContentLoaded", app_entry);

function set_mode_node(text) {
        mode_node.innerHTML = text;
}

function sk_set_mode(mode) {
        sk_now_mode = mode;
        switch (mode) {
                case sk_mode_normal: set_mode_node('NORMAL'); break;
                case sk_mode_search: set_mode_node('SEARCH'); break;
                case sk_mode_goto: set_mode_node('GOTO'); break;
        }
}

function remove_class(e, class_name) {
        e.className = e.className.replace(class_name, '').trim();
}

function add_class(node, class_name) {
        var class_names = ' ' + node.className + ' ';
        var has_class = class_names.indexOf(' ' + class_name + ' ') > -1;
        if (!has_class)
                node.className += ' '  + class_name;
}

function change_section(element) {
        if (now_section_node != null)
                remove_class(now_section_node, 'current');
        add_class(element, 'current');
        now_section_node = element;
}

function section_click_evt_handle(event) {
        change_section(event.target);
}

function sk_active_search() {
        if (!search_input_node)
                return;
        search_input_node.focus();
        search_input_node.select();
}

function sk_release() {
        if (search_input_node)
                search_input_node.blur();
        if (sk_now_mode == sk_mode_goto)
                sk_goto_hide_index();
        sk_set_mode(sk_mode_normal);
        content_body_node.focus();
        clear_message();
}

function sk_next_section(e) {
        var node = document.getElementById('fx-next-section');
        if (node && !link_invalid(node))
                document.location.href = node.href;
        else
                push_message('No next section', msg_lwarning);
}
function sk_prev_section(e) {
        var node = document.getElementById('fx-prev-section');
        if (node && !link_invalid(node))
                document.location.href = node.href;
        else
                push_message('No previous section', msg_lwarning);
}

function sk_doc_source(e) {
        var node = document.getElementById('fx-doc-source');
        if (node && !link_invalid(node))
                document.location.href = node.href;
        else
                push_message('No source file for current page', msg_lwarning);
}

function sk_parent_section(e) {
        var node = document.getElementById('fx-parent-section');
        if (node && !link_invalid(node))
                document.location.href = node.href;
        else
                push_message('No parent section', msg_lwarning);
}

function sk_do_normal(e) {
        switch (e.keyCode) {
                case kb_key_next_section: sk_next_section(); break;
                case kb_key_prev_section: sk_prev_section(); break;
                case kb_key_toc: sk_toc(); break;
                case kb_key_help: sk_help(); break;
                case kb_key_info: sk_info(); break;
                case kb_key_downloads: sk_downloads(); break;
                case kb_key_goto: sk_do_goto(e); break;
                case kb_key_doc_source: sk_doc_source(); break;
                case kb_key_search: sk_do_search(e); break;
                case kb_key_parent_section: sk_parent_section(e); break;
        }
}

function sk_do_search(e) {
        if (sk_now_mode != sk_mode_search) {
                sk_set_mode(sk_mode_search);
                sk_active_search();
                e.preventDefault();
        }
}

function sk_do_goto(e) {
        if (sk_now_mode != sk_mode_goto) {
                sk_set_mode(sk_mode_goto);
                sk_goto_start();
                return;
        }
        if (e.keyCode == 71) {
                sk_release();
        } else if (e.keyCode == 13) {
                sk_goto_end();
                sk_set_mode(sk_mode_normal);
        } else {
                sk_goto_input(e);
        }
}

function keyboard_handler(e) {
        if (e.keyCode == kb_key_esc)
                sk_release();

        switch(sk_now_mode) {
                case sk_mode_normal: sk_do_normal(e); break;
                case sk_mode_search: sk_do_search(e); break;
                case sk_mode_goto: sk_do_goto(e); break;
        }
}

function setup_sk() {
        window.addEventListener('keydown', keyboard_handler);
        sk_set_mode(sk_mode_normal);
}

function sk_toc() {
        document.location.href = '/';
}

function setup_search_input_node() {
        search_input_node = document.getElementById('fx-search-input');
        if (!search_input_node)
                return;
        search_input_node.onfocus = function(e){
                sk_set_mode(sk_mode_search);
        }
        search_input_node.onblur = function(e) {
                sk_set_mode(sk_mode_normal);
        }
}

function remake_table() {
        var tables = document.getElementsByTagName('table');
        for (var i = 0; i < tables.length; ++i) {
                var table = tables[i];
                var table_wrap = document.createElement('div');
                table_wrap.className = 'fx-table-wrap';
                table.parentNode.replaceChild(table_wrap, table);
                table_wrap.appendChild(table);
        }
}

function find_nodes() {
        mode_node = document.getElementById('fx-mode');
        content_body_node = document.getElementById('fx-body');
        msg_box_node = document.getElementById('fx-msg-box');
        msg_box_content_node = document.getElementById('fx-msg-content');
}

function push_message(text, level) {
        if (msg_timer)
                clearInterval(msg_timer);
        msg_box_content_node.innerHTML = text;
        add_class(msg_box_node, 'fx-msg-box-show');
        var msg_level;
        switch (level) {
                case msg_linfo: msg_level = 'fx-info'; break;
                case msg_lsuccess: msg_level = 'fx-success'; break;
                case msg_lwarning: msg_level = 'fx-warning'; break;
                case msg_ldanger: msg_level = 'fx-danger'; break;
        }
        add_class(msg_box_node, msg_level);
        msg_timer = setInterval(function() {
                remove_class(msg_box_node, 'fx-msg-box-show');
                clearInterval(msg_timer);
                msg_timer = null;
        }, msg_duration);
}

function clear_message() {
        if (msg_timer) {
                clearInterval(msg_timer);
                msg_timer = null;
        }
        remove_class(msg_box_node, 'fx-msg-box-show');
}

function find_section_nodes() {
        var toc = document.getElementById('fx-toc');
        if (toc.length == 0)
                return [];
        return toc.getElementsByTagName('a');
}

function find_now_section_node() {
        if (now_sects.length == 0)
                return null;
        else
                return now_sects[0];
}

function setup_table_of_contents() {
        var sections = find_section_nodes();
        now_section_node = document.querySelector('.fx-toc a.current');
        if (!now_section_node && sections.length > 0)
                change_section(sections[0]);
        for (var i = 0; i < sections.length; ++i)
                sections[i].onclick = section_click_evt_handle;
}

function focus_content_node() {
        setTimeout(function() {
                if (content_body_node)
                        content_body_node.focus();
        }, 0); 
}

function jump_to_hashtag() {
        var hash = window.location.hash;
        if (!hash) 
                return;
        setTimeout(function() {
                window.location.hash = "";
                window.location.hash = hash;
        }, 0);
}

function app_entry() {
        remake_table();
        find_nodes();

        setup_table_of_contents();
        setup_search_input_node();
        setup_sk();
        jump_to_hashtag();

        focus_content_node();
}

function sk_help() {
        document.location.href = '/help.html';
}

function sk_info () {
        document.location.href = '/info.html';
}

function sk_downloads() {
        document.location.href = '/downloads.html'
}

function link_invalid(node) {
        var style = window.getComputedStyle(node);
        var pointer_events = style.getPropertyValue('pointer-events');
        return !node.href || pointer_events == 'none' ;
}

function sk_goto_mk_index() {
        links = document.getElementsByTagName('a');
        sk_goto_label = []
        sk_goto_items = []
        var j = 0;
        for (var i = 0; i < links.length; ++i) {
                if (link_invalid(links[i]))
                        continue;
                var label = document.createElement('span');
                label.innerHTML = j;
                label.className = 'fx-goto-label';
                sk_goto_label.push(label);
                links[i].appendChild(label);
                sk_goto_items.push(links[i]);
                j++;
        }
}

function sk_goto_show_index() {
        for (var i = 0; i < sk_goto_label.length; ++i) {
                sk_goto_label[i].style.visibility = 'visible';
                sk_goto_label[i].style.display = 'inline';
        }
}

function sk_goto_hide_index() {
        for (var i = 0; i < sk_goto_label.length; ++i) {
                sk_goto_label[i].style.visibility = 'hidden';
                sk_goto_label[i].style.display = 'none';
        }
}

function sk_goto_start(e) {
        sk_goto_index = []
        if (!sk_goto_items)
                sk_goto_mk_index();
        sk_goto_show_index();
}

function numbers_to_value(codes) {
        if (codes.length == 0)
                return -1;
        var base;
        var dec = 0;
        for (var i = 0; i < codes.length; ++i) {
                base = Math.pow(10, codes.length - i - 1);
                dec += (codes[i]) * base;
        }
        return dec;
}

function catch_number(code) {
        if (code >= 48 && code <= 57)
            return code - 48;
        else if (code >= 96 && code <= 105)
            return code - 96;
        else
            return -1;
}

function sk_goto_input(e) {
        if (e.keyCode == 8) {
                if (sk_goto_index.length > 0)
                        sk_goto_index.splice(sk_goto_index.length - 1, 1);
        } else {
                number = catch_number(e.keyCode);
                if (number < 0)
                    return;
                sk_goto_index.push(number)
        }

        index = numbers_to_value(sk_goto_index);
        if (index < 0) {
                sk_goto_unmark();
                return;
        }
        if (index >= sk_goto_items.length) {
                sk_goto_index.splice(sk_goto_index.length - 1, 1);
                index = numbers_to_value(sk_goto_index);
        }
        sk_goto_mark_label(index);
}

function sk_goto_unmark() {
        if (sk_goto_label_selected)
                remove_class(sk_goto_label_selected, 'fx-selected')
}

function sk_goto_mark_label(index) {
        sk_goto_unmark();
        add_class(sk_goto_label[index], 'fx-selected');
        sk_goto_label_selected = sk_goto_label[index]
}

function sk_goto_end(e) {
        index = numbers_to_value(sk_goto_index);
        sk_goto_hide_index();
        if (index >= 0)
                sk_goto_items[index].click();
}
