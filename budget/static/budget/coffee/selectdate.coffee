select = $('select')
form = $('form')

select.change ->
  option = $('select option:selected')
  select_value = option.val()
  year = option.data 'year'
  month = option.data 'month'
  $.ajaxSetup headers: 'X-CSRFToken': Cookies.get('csrftoken')
  $.ajax
    url: form.attr('action')
    type: form.attr('method')
    data: {
      'select_value': select_value,
      'year': year,
      'month': month
    }
    success: (data) ->
      if data['success']
        table = $('#table-transactions')
        table.replaceWith data['html']
      return
    error: ->
      form.find('.error-message').show()
      return
  return