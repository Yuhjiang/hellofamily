var onoff = true//根据此布尔值判断当前为注册状态还是登录状态

//自动居中title
var name_c = document.getElementById("title")
for (var i = 0; i < name.length; i++)
    if (name[i] !== ",")
        name_c.innerHTML += "<i>" + name[i] + "</i>"
//引用hint()在最上方弹出提示
function hint() {
    let hit = document.getElementById("hint")
    hit.style.display = "block"
    setTimeout("hit.style.opacity = 1", 0)
    setTimeout("hit.style.opacity = 0", 2000)
    setTimeout('hit.style.display = "none"', 3000)
}
//注册按钮
function register() {
    let status = document.getElementById("status").getElementsByTagName("i")
    var form = document.querySelector('.form')
    console.log('register_form', onoff)
    if (onoff) {
        status[0].style.top = 35 + "px"
        status[1].style.top = -5 + "px"
        onoff = !onoff
        form.action = '/auth/register'
        var password = form.querySelector('#password')
        var password2 = form.querySelector('#password2')
        if (password2 === null) {
            password.insertAdjacentHTML('afterend', passwordTemplate)
        }
    } else {
        // form.submit()
    }
}

//登录按钮
function login() {
    let status = document.getElementById("status").getElementsByTagName("i")
    var form = document.querySelector('.form')
    console.log('login', onoff)
    if (onoff) {
        // form.submit()
    } else {
        status[1].style.top = 35 + "px"
        status[0].style.top = -5 + "px"
        onoff = !onoff
        form.action = '/auth/login'
        var password = form.querySelector('#password2')
        password.remove()
    }
}

var passwordTemplate = `
    <input class="form-control" id="password2" name="password2" required="" type="password" value="" placeholder="confirm password">
`