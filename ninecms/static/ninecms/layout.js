/**
 * @file layout.js
 * Provide js-level formatting
 *
 * @author
 * George Karakostas
 *
 * @copyright
 * (c) 2015 George Karakostas
 *
 * @license
 * BSD-3
 *
 * @email
 * gkarak@9-dev.com
 */

(function ($) {
    /********************
     * Generic functions
     ********************/

    var iOS = /(iPad|iPhone|iPod)/g.test(navigator.userAgent);
    var Opera = /(OPR)/g.test(navigator.userAgent);

    // Formset management
    // Note: browser refresh keeps total_forms number
    $.fn.djangoFormset = function(options) {
        // init
        var t = this;
        var o = options;
        var prefix = o['prefix'];
        if (!prefix) console.error('Misconfigured djangoFormset.');
        var total_forms = t.find('#id_' + prefix + '-TOTAL_FORMS');

        // delete form
        // WARNING: This works only for new record
        // For existing forms in formset, delete field is required
        // @see http://stackoverflow.com/questions/12414248/dynamically-delete-form-from-model-formset-django?rq=1
        // @see https://docs.djangoproject.com/en/1.8/topics/forms/formsets/#understanding-the-managementform
        // @see https://docs.djangoproject.com/en/1.8/topics/forms/formsets/#can-delete
        // @todo fix remove item for existing formsets
        var deleteForm = function() {
            $(this).parents('.formset-form').slideUp(function() {
                // Fix the numbers before removing
                $(this)
                    .nextAll()
                    .find('[id*="id_' + prefix + '-"]')
                    .each(function() {
                        // fix id (+cke_)
                        var i = $(this).attr('id').match(new RegExp('(cke_|)id_' + prefix + '-(\\d+)-(\\w+)'));
                        if (i) $(this).attr('id', i[1] + 'id_' + prefix + '-' + --i[2] + '-' + i[3]);
                        // fix name
                        i = $(this).attr('name').match(new RegExp(prefix + '-(\\d+)-(\\w+)'));
                        if (i) $(this).attr('name', prefix + '-' + --i[1] + '-' + i[2]);
                    });
                $(this).remove();
                // number of forms
                var total_forms_num = parseInt(total_forms.val());
                // update the counter
                total_forms.val(total_forms_num - 1);
            });
            // trigger function if any
            if (o['on_delete'] && typeof(o['on_delete']) === 'function') o['on_delete'].call();
        };
        t.find('.form-remove').on('click', deleteForm);

        // add form
        // @see http://stackoverflow.com/questions/501719/dynamically-adding-a-form-to-a-django-formset-with-ajax
        t.find('.formset-add').on('click', function() {
            // number of forms
            var total_forms_num = parseInt(total_forms.val());
            // the empty form inner elements
            var empty_form = t.find('.' + prefix + '-form-empty');
            // the new form inner elements
            var new_form = empty_form.html().replace(/__prefix__/g, total_forms_num);
            // wrap new form
            new_form = $('<div class="formset-form ' + prefix + '-' + total_forms_num + '">' + new_form +'</div>');
            // handle delete
            new_form.find('.form-remove').on('click', deleteForm);
            // add new form
            empty_form.before(new_form.hide());
            // enable ckeditor
            if (o['ckeditor']) CKEDITOR.replace(prefix + '-' + total_forms_num + '-' + o['ckeditor']);
            // show it
            new_form.slideDown('slow');
            // update the counter
            total_forms.val(total_forms_num + 1);
            // trigger function if any
            if (o['on_add'] && typeof(o['on_add']) === 'function') o['on_add'].call();
        });

        // ensure ckeditor runs properly when form reconstructed from validation error
        if (o['ckeditor']) {
            $(window).load(function () {
                t.find('textarea')
                    .filter('[name^="' + prefix +'-"]')
                    .filter('[name$="-' + o['ckeditor'] +'"]')
                    .not('[name*="__prefix__"]')
                    .not(':first')
                    .each(function() {
                        CKEDITOR.replace(this);
                    });
            });
        }
        return t;
    };

    // ajax setup
    $.fn.djangoAjaxSetup = function(options) {
        // init
        var t = this;
        var o = options;

        // Get cookie function (from django)
        var getCookie = function(name) {
            var cookieValue = null;
            //noinspection JSValidateTypes
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                console.log(cookies);
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        };

        // Get CSRF token
        var getToken = function() {
            if (o['csrf_cookie_httponly']) return $('input[name="csrfmiddlewaretoken"]').val();
            else return getCookie('csrftoken');
        };

        // Check methods that do not require CSRF protection
        var csrfSafeMethod = function(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        };

        // Send csrf on ajax
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getToken());
                }
            }
        });
        return t;
    };

    // ajax support
    $.fn.djangoAjax = function(options) {
        // init
        var t = this;
        var fld = t.find('input');
        var o = options;

        // run for each field (some maybe new from formpanel or other js)
        fld.each(function() {
            // don't run twice
            if($(this).hasClass('django-ajaxified')) return;
            // when user types
            $(this).addClass('django-ajaxified').on('keyup', function() {
                // get the value typed
                var v = $(this).val();
                // don't run if less than 3 chars or some key pressed that did not change the data
                if (v.length < 3 || v == $(this).data('prev-val')) return;
                $(this).data('prev-val', v);
                // ajax call
                $.ajax({
                    url: o['url'],
                    type: 'POST',
                    // send the value for django and the id for the success func
                    data: {value: v, id: $(this).attr('id')},
                    success: o['success']
                    //error: function(xhr, errmsf, err) {}
                });
            });
        });
        return t;
    };

    // ajax selector
    $.fn.djangoAjaxSelector = function(options) {
        // init
        var fld = this;
        var o = options;
        // whatever django returned
        var json = o['json'];
        // this is the form prefix
        var prefix;
        // this is the form id of the formset, if any
        var formset_id = 0;
        if (o['in_formset']) {
            var matches = fld.attr('id').match(/(id_\w+-(\d+)-)\w+/);
            prefix = matches[1];
            formset_id = matches[2];
        }
        else prefix = fld.attr('id').match(/(id_\w+-)\w+/)[1];
        // helper function to assign value to the id field
        var setId = function(v) {
            // if a field name is specified, replace any @ with the formset id and set value
            if (o['id_field']) $(o['id_field'].replace('@', formset_id)).val(v);
            else $('#' + prefix + 'id').val(v);
        };

        // get the selector if any or create
        var selector = fld.next();
        // helper function to close the selector
        var closeSelector = function(e) {
            // if comes from click, get element
            if (e.currentTarget) e = $(e.currentTarget).parent();
            e.slideUp(function() { $(this).remove(); });
        };
        // create selector if necessary
        if (!selector.hasClass('ajax-selector')) {
            selector = $('<div class="ajax-selector"></div>');
            selector.insertAfter(fld);
            selector.append($('<div class="close glyphicon glyphicon-remove-circle" aria-hidden="true"></div>')
                .on('click', closeSelector));
            selector.hide().slideDown('slow');
        }
        // reset items
        selector.find('.item').remove();
        // append items
        for (var i = 0; i < json.length; i++) {
            // django serializer provides a json.fields iterable
            //noinspection JSUnresolvedVariable
            var json_fields = json[i].fields;
            // get the value to be displayed for each item
            var v = o['item_value_callback'](json_fields);
            //noinspection JSUnresolvedVariable
            var item = $('<div class="item"></div>')
                .text(v)
                // store json data on the element
                .data('pk', json[i].pk)
                .data('json', json_fields)
                // Here select item
                .on('click', function() {
                    // retrieve the stored item fields
                    var json_fields = $(this).data('json');
                    // loop through the fields and update relevant html fields!
                    for (var key in json_fields) {
                        // check that is is not a JS thingy but a real property
                        if (json_fields.hasOwnProperty(key))
                            $('#' + prefix + key).val(json_fields[key]);
                    }
                    setId($(this).data('pk'));
                    if (o['disable_on_select']) fld.off('keyup').attr('disabled', 'true');
                    closeSelector(selector);
                });
            selector.append(item);
        }
        // append info: no results
        if (json.length <= 0) {
            selector.append(
                // @todo translate
                $('<div class="item disabled"><em>(no results found)</em></div>'));
        }
        // append info: too many results
        else if (json.length >= 20) {
            selector.append(
                $('<div class="item disabled"><em>(too many results, please refine your search)</em></div>'));
        }
        // add new item
        if (o['add_item_callback']) {
            item = $('<div class="item"><em>add new</em></div>').on('click', function() {
                o['add_item_callback'](selector);
                setId('');
                if (o['disable_on_add']) fld.off('keyup');
                closeSelector(selector);
            });
            selector.append(item);
        }
        return fld;
    };

    /*********************
     * Specific functions
     *********************/

    $(document).ready(function () {
        // Loader
        // hide scroll and show on window.load
        var loader = $('#loader');
        if (loader.length && loader.css('display') != 'none') $('body').css({overflow: 'hidden'});

        // Page top
        $('#top-link')
            // set the link
            .topLink({
                min: 400,
                fadeSpeed: 500
            })
            // smooth scroll
            .click(function(e) {
                e.preventDefault();
                $.scrollTo(0,300);
            });

        // Show/hide toolbar
        $('.toolbar-handler').on('click', 'a', function(e) {
            $('body').toggleClass('toolbar').find('.toolbar').toggleClass('hide');
            e.preventDefault();
        });

        // Shrink
        if ($('.shrinkable').length) {
            $(window).scroll(function() {
                if ($(this).scrollTop() > 50)
                    $('.shrinkable').addClass('shrink');
                else $('.shrinkable').removeClass('shrink');
            });
        }

        // Bookmark smooth scroll
        $('.nav a[href*="#"]').each(function() {
            var bookmark = $(this).attr('href').match(/(#.*)$/g)[0];
            if (bookmark == '#') return;
            if (!$(bookmark).length) return;
            $(this).on('click', function() {
                $.scrollTo(bookmark, 300, {offset: {top: -50, left: 0}});
            });
        });

        // bootstrap
        $('input[type="text"], input[type="number"], input[type="email"], input[type="url"], select')
            .addClass('form-control');

        // Formsets
        $('.panel-name-image-set').djangoFormset({prefix: 'image'});
        $('.panel-name-file-set').djangoFormset({prefix: 'file'});
        $('.panel-name-video-set').djangoFormset({prefix: 'video'});
        $('.panel-name-page-layout-elements').djangoFormset({prefix: 'element'});

    });

    $(window).load(function () {
        // Loader
        // hide loader and show scrollbars (hidden in document.ready)
        $('#loader, #loader-container').fadeOut('slow');
        $('body').css({'overflow': 'visible'});

        // video autoplay for iOS / Opera
        if (iOS || Opera) $('.video-js').attr('controls', '');
    });

}(jQuery));
