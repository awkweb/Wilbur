$('#form-submit').click (e) ->
  e.preventDefault()
  form = $('#form-grab')
  $.ajaxSetup headers: 'X-CSRFToken': Cookies.get 'csrftoken'
  $.ajax
    url: form.attr 'action'
    type: form.attr 'method'
    data: form.serialize()
    success: (data) ->
      if !data['success']
        alert data['form_html']
        form.replaceWith data['form_html']
      else
        next = form.attr 'next'
        window.location.replace next
      return
    error: ->
      form.find('.error-message').show()
      return
  return
