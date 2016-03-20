$.fn.selectFilter = ->
  select = $(this)
  select.change ->
    option = select.find(":selected")
    link = option.data('link')
    location.href = link