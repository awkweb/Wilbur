select = $('select')
form = $('form')

select.change ->
  option = $('select option:selected')
  year = option.data 'year'
  month = option.data 'month'
  $.ajaxSetup headers: 'X-CSRFToken': Cookies.get('csrftoken')
  $.ajax
    url: form.attr('action')
    type: form.attr('method')
    data: {'year': year, 'month': month}
    success: (data) ->
      if data['success']
        table = $('#table-transactions')
        table.replaceWith data['html']
      return
    error: ->
      form.find('.error-message').show()
      return
  return