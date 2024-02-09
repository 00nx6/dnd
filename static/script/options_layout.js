// im_sorry_for_this
const options_cont = document.querySelectorAll('.options_cont')[0]

const options = Array.from(document.querySelectorAll('.options'))
const column_count = options.length

options_cont.style.gridTemplateColumns = `repeat(${column_count}, ${1/column_count}fr)`

