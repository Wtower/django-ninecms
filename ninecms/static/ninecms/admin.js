/**
 * @file admin.js
 * Provide ajax operations for 9cms admin
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

(function($) {
    /**
     * Add a css class on element for a specified time
     * Combine with css transition for a nice effect
     * Alternatively use jQueryUI addClass
     *
     * @param css: the class to add
     * @param time: for how long
     */
    $.fn.addClassTemp = function(css, time) {
        return this
            .addClass(css)
            .delay(time)
            .queue(function() {
                $(this)
                    .removeClass(css)
                    .dequeue();
            });
    };

    $(document).ready(function() {
        /*******************
         * Ajax edit inline
         ******************/
        $(this).djangoAjaxSetup({csrf_cookie_httponly: true});
        $('.edit-inline').on('click', function(e) {
            var t = $(this);
            /**
             * Ajax success callback function (see below)
             * Parse the serialized data returned in form eg. id=1&status=True
             * then find the row, then the a element and set value and glyphicon
             *
             * @param json: data returned
             */
            var ajaxSuccess = function(json) {
                var data = this.data.match(/id=([-_\w\d]+)&([-_\w\d]+)=([-_\w\d]+)/);
                $('tr[data-id="' + data[1] + '"]')
                    .find('a[data-field="' + data[2] + '"]')
                    .each(function() {
                        if (json.result) {
                            var value = data[3];
                            if ($(this).data('type') == 'bool') {
                                value = (value == 'True')? 'ok': 'remove';
                                value = '<span class="glyphicon glyphicon-' + value + '" aria-hidden="true"></span>'
                            }
                            $(this)
                                .data('value', data[3]).html(value)
                                .addClassTemp('text-success', 4000);
                        }
                        else $(this).addClassTemp('text-danger', 4000);
                        console.log(json);
                    });
            };
            // construct the post data
            var data = {id: t.parents('tr').data('id')};
            var value = t.data('value');
            if (t.data('type') == 'bool') {
                if (value == 'True') value = 'False';
                else value = 'True';
            }
            data[t.data('field')] = value;
            $.ajax({
                url: t.parents('tr').data('edit-inline-url'),
                type: 'POST',
                data: data,
                success: ajaxSuccess
            });
            e.preventDefault();
        });
    });
})(jQuery);
