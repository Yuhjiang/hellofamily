var group = document.querySelector('#group')
var member = document.querySelector('#member')
var options = member.querySelectorAll('option')
options = Array.prototype.slice.call(options)

var groups = {
    'morningmusume': [60, 75],
    'angerme': [1, 14],
    'juicejuice': [45, 55],
    'countrygirls': [26, 31],
    'kobushifactory': [55, 60],
    'tsubakifactory': [75, 83],
    'beyooooonds': [14, 26],
    'helloprokenshusei': [31, 42],
    'helloprokenshuseihokkaido': [42, 45]
}

// 绑定group选择事件
var bindEventGroup = function() {
    group.addEventListener('click', function() {

        var option = group.options[group.selectedIndex].value
        console.log(option)
        var new_options = options.slice(groups[option][0], groups[option][1])
        console.log(new_options)
        var t = template(new_options)
        console.log(t)
        member.innerHTML = t

    })
}

var template = function(data) {
    var t = templateOption(options[0].value, options[0].innerText)
    for (var i = 0; i < data.length; i++) {
        t += templateOption(data[i].value, data[i].innerText)
    }
    return t
}

var templateOption = function(value, text) {
    return `<option value="${value}">${text}</option>`
}

var bindEvents = function() {
    bindEventGroup()
}

var option = group.options[group.selectedIndex].value
var new_options = options.slice(groups[option][0], groups[option][1])
var t = template(new_options)
member.innerHTML = t

bindEvents()
