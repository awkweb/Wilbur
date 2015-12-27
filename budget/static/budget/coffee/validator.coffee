$('#form-submit').click (event) ->
  event.preventDefault()
  form = $('#form-grab')
  $.ajax
    url: form.attr('action')
    type: form.attr('method')
    data: form.serialize()
    success: (data) ->
      if !data['success']
        form.replaceWith data['form_html']
      else
        next = form.attr('next')
        window.location.replace next
      return
    error: ->
      form.find('.error-message').show()
      return
  return false