select = $('#filter')

select.change ->
  option = $('#filter option:selected')
  budget = option.val()
  $.ajaxSetup headers: 'X-CSRFToken': Cookies.get('csrftoken')
  $.ajax
    url: window.location.pathname
    type: 'post'
    data: {
      'action': 'filter',
      'budget': budget
    }
    success: (data) ->
      if data['success']
        html = $('#content-ajax')
        html.replaceWith data['html']
      return
    error: ->
      form.find('.error-message').show()
      return
  return