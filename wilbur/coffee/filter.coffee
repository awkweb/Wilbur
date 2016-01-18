select = $('#filter')

select.change ->
  option = $('#filter option:selected')
  value = option.val()
  link = if value != '-1' then "/transactions/budget/#{ value }/" else '/transactions/'
  window.location.replace link