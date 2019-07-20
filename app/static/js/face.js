var group = document.querySelector('#group')
var member = document.querySelector('#member')
var options = member.querySelectorAll('option')
options = Array.prototype.slice.call(options)

var groups = {
    'morningmusume': [60, 74],
    'angerme': [1, 14],
    'juicejuice': [45, 55],
    'countrygirls': [26, 31],
    'kobushifactory': [55, 60],
    'tsubakifactory': [74, 83],
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

var api_images = function(form, callback) {
    var path = '/face/cp'
    ajax('POST', path, form, callback)
}

var image_template = function(url) {
    t = `<li>
                    <dl class="m_photoItem m_photoItem_a phtItem_hv">
                        <dt class="photo face">
                            <a href="${url}">
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

        var form = {
            member1: member1[member1.selectedIndex].value,
            member2: member1[member2.selectedIndex].value,
            start_time: start_time.value,
            end_time: end_time.value,
        }
        api_images(form, function(images) {
            insertImages(images)
        })
    })
}

bindEvents()
bindEventCp()