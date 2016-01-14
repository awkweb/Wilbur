button = $('#confirm')

button.mouseleave ->
  button.removeClass 'is-clicked'
  ogText = button.data 'original-text'
  button.text ogText
  return

button.mouseenter ->
  if button.hasClass 'is-clicked'
    button.removeClass 'is-clicked'
  return

button.click (e) ->
  e.preventDefault()

  if button.hasClass 'is-clicked'
    link = button.attr 'href'
    document.location.href = link
  else
    button.addClass 'is-clicked'
    altText = button.data 'alt-text'
    button.text altText
  return