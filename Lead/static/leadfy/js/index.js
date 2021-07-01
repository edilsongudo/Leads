// let word = document.querySelector('#wordchange')
// words = ['programmer?', 'developer?']
// i = 0
// word.innerText = words[i]

// setInterval(function () {
//     word.innerText = words[i]
//     i ++
//     if (i >= words.length) {
//         i = 0
//     }
// }, 2000)


let stack = document.querySelector('#stacks')
stacks = ['Python', 'Javascript', 'Django', 'Flask', 'Java', 'PHP', 'Web Scrapping', 'Automation', 'React JS', 'Vue JS', 'Wordpress', 'Shopify']
j = 0
stack.innerText = stacks[j]

setInterval(function () {
    stack.innerText = `We work with ${stacks[j]}`
    j ++
    if (j >= stacks.length) {
        j = 0
    }
}, 500)


