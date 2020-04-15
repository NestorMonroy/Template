/*!
 * Stream v1.0 (https://htmlstream.com)
 * Copyright Htmlstream
 * Licensed under MIT
 */


(function ($) {
  'use strict';

  // Activate Tooltips & Popovers
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="popover"]').popover();

    // Dismiss Popovers on next click
    $('.popover-dismiss').popover({
      trigger: 'focus'
    })
  });

  // Hide Navbar on scroll
  /* When the user scrolls down, hide the navbar. When the user scrolls up, show the navbar */
  var prevScrollpos = window.pageYOffset;
  window.onscroll = function () {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos < currentScrollPos && currentScrollPos > 600) {
      document.getElementsByTagName("nav")[0].style.top = "-72px";
    } else {
      document.getElementsByTagName("nav")[0].style.top = "0";
    }
    prevScrollpos = currentScrollPos;
  }

  // Bootstrap Fixed Header
  $(function () {
    // Check to see if there is a bakcground class on loading
    if ($('.js-navbar-scroll').offset().top > 150) {
      $('.js-navbar-scroll').addClass('navbar-bg-onscroll');
    }

    // Check to add a background class on scrolling
    $(window).on('scroll', function () {
      var navbarOffset = $('.js-navbar-scroll').offset().top > 150;
      if (navbarOffset) {
        $('.js-navbar-scroll').addClass('navbar-bg-onscroll');
      }
      else {
        $('.js-navbar-scroll').removeClass('navbar-bg-onscroll');
        $('.js-navbar-scroll').addClass('navbar-bg-onscroll--fade');
      }
    });
  });

  // Scroll to (Section)
  $(function () {
    $('a[href*=#js-scroll-to-]:not([href=#js-scroll-to-])').on('click', function () {
      if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        if (target.length) {
          $('html,body').animate({
            scrollTop: target.offset().top - 10
          }, 1000);
          return false;
        }
      }
    });
  });
}(jQuery));