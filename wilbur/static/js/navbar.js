(function() {
  jQuery(document).ready(function($) {
    var mainNavigation, navigationContainer;
    navigationContainer = $('#cd-nav');
    mainNavigation = navigationContainer.find('#cd-main-nav ul');
    $('.cd-nav-trigger').on('click', function() {
      $(this).toggleClass('menu-is-open');
      mainNavigation.off('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend').toggleClass('is-visible');
    });
  });

}).call(this);
