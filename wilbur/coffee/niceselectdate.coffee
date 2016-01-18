select = $('#selectdate')

select.change ->
  option = $('#selectdate option:selected')
  value = option.val()
  year = option.data 'year'
  month = option.data 'month'
  $.ajaxSetup headers: 'X-CSRFToken': Cookies.get('csrftoken')
  $.ajax
    url: window.location.pathname
    type: 'post'
    data: {
      'selectdate_value': value,
      'year': year,
      'month': month
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