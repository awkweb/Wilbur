$.fn.coffeeCounter = ->
  input = $(this)
  text_max = input.attr 'maxlength'
  text_length = input.val().length
  text_remaining = text_max - text_length
  counter = $("<span></span>").text text_remaining
  counter.addClass 'accessory'
  counter.attr 'id', 'control_counter'

  input_id = input.attr 'id'

  label = $("label[for='"+input_id+"']")
  label.after counter
  control_counter = $('#control_counter')

  # copy and paste case
  input.keydown ->
    text_length = input.val().length
    text_remaining = text_max - text_length
    control_counter.html text_remaining
    return
  return

return