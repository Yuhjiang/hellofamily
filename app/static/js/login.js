var onoff = true//根据此布尔值判断当前为注册状态还是登录状态
var form = document.querySelector('.form')
form.action = '/user/login' + window.location.search
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
        form.action = '/user/register'
        var password = form.querySelector('#password')
        var password2 = form.querySelector('#password2')
        if (password2 === null) {
            password.insertAdjacentHTML('afterend', passwordTemplate)
            password.insertAdjacentHTML('beforebegin', emailTemplate)
        }
        var button = document.querySelector('.button')
        button.innerHTML = registerTemplate
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
        form.action = '/user/login' + window.location.search
        var password = form.querySelector('#password2')
        var email = form.querySelector('#email')
        password.remove()
        email.remove()
        var button = document.querySelector('.button')
        button.innerHTML = loginTemplate
    }
}

var passwordTemplate = `
    <input class="form-control" id="password2" name="password2" required="" type="password" value="" placeholder="confirm password">
`

var emailTemplate = `
    <input class="form-control" id="email" name="email" required="" type="text" placeholder="email">
`

var registerTemplate = `
    <a class="btn btn-primary" onclick="login()">LOG IN</a>
    <button class="btn btn-primary" onclick="register()" style="margin-right: 20px;font-size: 20px">Register</button>
`

var loginTemplate = `
    <button class="btn btn-primary" onclick="login()" style="margin-right: 20px;font-size: 20px">LOG IN</button>
    <a class="btn btn-primary" onclick="register()">SIGN IN</a>
`