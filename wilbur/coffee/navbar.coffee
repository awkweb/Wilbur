jQuery(document).ready ($) ->
  navigationContainer = $('#cd-nav')
  mainNavigation = navigationContainer.find('#cd-main-nav ul')

  #open or close the menu clicking on the bottom "menu" link
  $('.cd-nav-trigger').on 'click', ->
    $(this).toggleClass 'menu-is-open'
    #we need to remove the transitionEnd event handler (we add it when scolling up with the menu open)
    mainNavigation.off('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend').toggleClass 'is-visible'
    return
  return