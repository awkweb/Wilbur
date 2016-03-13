$('.meter-animate').each ->
  width = $(this).data('width')
  width = if width > 100 then 100 else width
  $(this).animate width: "#{ width }%"
  return