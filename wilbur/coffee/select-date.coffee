select = $('#select-date')

select.change ->
  option = select.find(":selected")
  year = option.data 'year'
  month = option.data 'month'
  $.ajaxSetup headers: 'X-CSRFToken': Cookies.get('csrftoken')
  $.ajax
    url: window.location.pathname
    type: 'post'
    data: {
      'year': year,
      'month': month
    }
    success: (data) ->
      if data['success']
        html = $('#content-ajax')
        html.replaceWith data['html']
      return
    error: ->
      alert 'Error'
      return
  return