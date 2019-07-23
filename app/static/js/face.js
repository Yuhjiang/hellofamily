var group = document.querySelector('#group')
var member = document.querySelector('#member')
var options = member.querySelectorAll('option')
options = Array.prototype.slice.call(options)

var groups = {
    'morningmusume': [77, 121],
    'angerme': [1, 19],
    'juicejuice': [62, 72],
    'countrygirls': [38, 43],
    'kobushifactory': [72, 77],
    'tsubakifactory': [123, 132],
    'beyooooonds': [26, 38],
    'helloprokenshusei': [48, 59],
    'helloprokenshuseihokkaido': [59, 62],
    'cute':[43, 48],
    'berrykobo': [19, 26],
    'others': [121, 123]
}

var group_options = {
    'morningmusume': 0,
    'angerme': 1,
    'juicejuice': 2,
    'countrygirls': 3,
    'kobushifactory': 4,
    'tsubakifactory': 5,
    'beyooooonds': 6,
    'helloprokenshusei': 7,
    'helloprokenshuseihokkaido': 8,
    'cute':9,
    'berrykobo': 10,
    'others': 11
}

// 绑定group选择事件
var bindEventGroup = function() {
    group.addEventListener('click', function() {

        var option = group.options[group.selectedIndex].value
        var new_options = options.slice(groups[option][0], groups[option][1])
        var t = template(new_options)
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
    bindEventCp()
    bindEventNormal()
}

var option = group.options[group.selectedIndex].value
var new_options = options.slice(groups[option][0], groups[option][1])
var t = template(new_options)
member.innerHTML = t


var ajax = function(method, path, data, responseCallBack) {
    var r = new XMLHttpRequest()
    r.open(method, path, true)

    r.setRequestHeader('Content-Type', 'application/json')
    r.onreadystatechange = function() {
        if (r.readyState === 4) {
            var json = JSON.parse(r.response)
            responseCallBack(json)
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}

var photo_list = document.querySelector('.photoList')


var image_template = function(url) {
    t = `<li>
                    <dl class="m_photoItem m_photoItem_a phtItem_hv">
                        <dt class="photo face">
                            <a href="${url}" target="_blank">
                                <img src="${url}">
                            </a>
                        </dt>
                    </dl>
                </li>`
    return t
}

var insertImages = function(images) {
    var s = ''
    for (var i = 0; i < images.length; i++) {
        s += image_template(images[i]['url'])
    }
    photo_list.innerHTML = s
}

var cp_form = document.querySelector('.cp-form')
var bindEventCp = function() {
    var cp_button = document.querySelector('#cp')
    cp_button.addEventListener('click', function() {
        var member1 = cp_form.querySelector('#member1')
        var member2 = cp_form.querySelector('#member2')
        var start_time = cp_form.querySelector('#start_time')
        var end_time = cp_form.querySelector('#end_time')

        var args = {
            member1: member1[member1.selectedIndex].value,
            member2: member1[member2.selectedIndex].value,
            start_time: start_time.value,
            end_time: end_time.value,
        }
        var path = `/face/cp/?member1=${args['member1']}&member2=${args['member2']}&start_time=${args['start_time']}&end_time=${args['end_time']}
    `
        window.location.href = path

    })
}

var form = document.querySelector('.form')
var bindEventNormal = function() {
    var button = document.querySelector('#button')
    button.addEventListener('click', function() {
        var group = form.querySelector('#group')
        var member = form.querySelector('#member')
        var start_time = form.querySelector('#start_time')
        var end_time = form.querySelector('#end_time')

        var args = {
            group: group[group.selectedIndex].value,
            member: member[member.selectedIndex].value,
            start_time: start_time.value,
            end_time: end_time.value,
        }
        var path = `/face/normal/?group=${args['group']}&member=${args['member']}&start_time=${args['start_time']}&end_time=${args['end_time']}
    `
        window.location.href=path
    })
}

var remember_choice = function () {
    var args = window.location.search.split('?')
    if (args.length === 1) {
        return
    }
    args = args[1].split('&')
    choices = {}
    for (var i = 0; i < args.length; i++) {
        var key_value = args[i].split('=')
        choices[key_value[0]] = key_value[1]
    }
    console.log(choices)
    if ('group' in choices) {
        form.querySelector('#group').selectedIndex = group_options[choices['group']]
        form.querySelector('#member').selectedIndex = get_option('#member', choices['member'])
        form.querySelector('#start_time').value = choices['start_time']
        form.querySelector('#end_time').value = choices['end_time']
    }
    else {
        cp_form.querySelector('#member1').selectedIndex = get_option('#member1', choices['member1'])
        cp_form.querySelector('#member2').selectedIndex = get_option('#member2', choices['member2'])
        cp_form.querySelector('#start_time').value = choices['start_time']
        cp_form.querySelector('#end_time').value = choices['end_time']
    }


}

var get_option = function(loc, member) {
    var options = document.querySelector(loc).options
    for (var i = 0; i < options.length; i++) {
        if (member === options[i].value) {
            console.log(i)
            return i
        }
    }
    return -1
}

bindEvents()
remember_choice()