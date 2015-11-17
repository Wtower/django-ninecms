/**
 * @file jquery.toplink.js
 * Provide top-link element
 * 
 * @see
 * http://davidwalsh.name/jquery-top-link
 */

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