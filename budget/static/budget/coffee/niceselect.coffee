###  jQuery Nice Select - v1.0
    http://hernansartorio.github.io/jquery-nice-select
    Made by Hernán Sartorio
###

(($) ->

  $.fn.niceSelect = ->
    # Create custom markup
    @each ->
      select = $(this)
      if !select.next().hasClass('nice-select')
        select.after '<div class="nice-select ' + (select.attr('class') or '') + (if select.attr('disabled') then 'disabled' else '" tabindex="0') + '"><span class="current"></span><ul class="list"></ul></div>'
        dropdown = select.next()
        options = select.find('option')
        selected = select.find('option:selected')
        dropdown.find('.current').html selected.data('display') or selected.text()
        options.each ->
          display = $(this).data('display')
          dropdown.find('ul').append '<li class="option ' + (if $(this).is(':selected') then 'selected' else '') + '" data-value="' + $(this).val() + (if display then '" data-display="' + display else '') + '">' + $(this).text() + '</li>'
          return
      return

    ### Event listeners ###

    # Unbind existing events in case that the plugin has been initialized before
    $(document).off '.nice_select'
    # Open/close
    $(document).on 'click.nice_select', '.nice-select', (event) ->
      dropdown = $(this)
      $('.nice-select').not(dropdown).removeClass 'open'
      dropdown.toggleClass 'open'
      if dropdown.hasClass('open')
        dropdown.find '.option'
        dropdown.find('.focus').removeClass 'focus'
        dropdown.find('.selected').addClass 'focus'
      else
        dropdown.focus()
      return
    # Close when clicking outside
    $(document).on 'click.nice_select', (event) ->
      if $(event.target).closest('.nice-select').length == 0
        $('.nice-select').removeClass('open').find '.option'
      return
    # Option click
    $(document).on 'click.nice_select', '.nice-select .option', (event) ->
      option = $(this)
      dropdown = option.closest('.nice-select')
      dropdown.find('.selected').removeClass 'selected'
      option.addClass 'selected'
      text = option.data('display') or option.text()
      dropdown.find('.current').text text
      dropdown.prev('select').val(option.data('value')).trigger 'change'
      return
    # Keyboard events
    $(document).on 'keydown.nice_select', '.nice-select', (event) ->
      dropdown = $(this)
      focused_option = $(dropdown.find('.focus') or dropdown.find('.list .option.selected'))
      # Space or Enter
      if event.keyCode == 32 or event.keyCode == 13
        if dropdown.hasClass('open')
          focused_option.trigger 'click'
        else
          dropdown.trigger 'click'
        return false
        # Down
      else if event.keyCode == 40
        if !dropdown.hasClass('open')
          dropdown.trigger 'click'
        else
          if focused_option.next().length > 0
            dropdown.find('.focus').removeClass 'focus'
            focused_option.next().addClass 'focus'
        return false
        # Up
      else if event.keyCode == 38
        if !dropdown.hasClass('open')
          dropdown.trigger 'click'
        else
          if focused_option.prev().length > 0
            dropdown.find('.focus').removeClass 'focus'
            focused_option.prev().addClass 'focus'
        return false
        # Esc
      else if event.keyCode == 27
        if dropdown.hasClass('open')
          dropdown.trigger 'click'
        # Tab
      else if event.keyCode == 9
        if dropdown.hasClass('open')
          return false
      return
    return

  return
) jQuery