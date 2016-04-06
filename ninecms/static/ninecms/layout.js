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
    jQuery.fn.topLink = function(settings) {
      settings = jQuery.extend({
        min: 1,
        fadeSpeed: 200
      }, settings);
      return this.each(function() {
        //listen for scroll
        var el = jQuery(this);
        el.hide(); //in case the user forgot
        jQuery(window).scroll(function() {
          if(jQuery(window).scrollTop() >= settings.min) {
            el.fadeIn(settings.fadeSpeed);
          }
          else {
            el.fadeOut(settings.fadeSpeed);
          }
        });
      });
    };

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

    });

    $(window).load(function () {
        // Loader
        // hide loader and show scrollbars (hidden in document.ready)
        $('#loader, #loader-container').fadeOut('slow');
        $('body').css({'overflow': 'visible'});
    });

}(jQuery));
