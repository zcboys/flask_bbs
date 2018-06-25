$(function () {
    $('#captcha-btn').click(function (event) {
        event.preventDefault();
        var email = $('input[name=email]').val();
        if(!email){
            swal({
                title: "error",
                text: "请输入邮箱！",
                timer: 2000,
                button: false
            });
        }
        zlajax.get({
            'url': '/cms/email_captcha/',
            'data': {
                'email': email
            },
            'success': function (data) {
                if(data['code'] === 200){
                     swal({
                        title: "OK！",
                        text: "邮件发送成功,请注意查收！",
                        timer: 2000,
                        icon: "success",
                        button: false
                    });
                }
            },
            'fail': function (error) {
                swal({
                        title: "error！",
                        text: "网络错误！",
                        type: "error",
                        confirmButtonText: "Cool"
                    });
            }
        })
    })
})

$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var emailE = $("input[name='email']");
        var captchaE = $("input[name='captcha']");
        var email = emailE.val();
        var captcha = captchaE.val();

        zlajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if(data['code'] === 200){
                    swal({
                        title: "OK！",
                        text: "邮箱修改成功！",
                        timer: 2000,
                        icon: "success",
                        button: false
                    });
                }else {
                    var message = data['message'];
                    swal({
                        title: "Error!",
                        text: message,
                        type: "error",
                        confirmButtonText: "Cool"
                    });
                }
            },
            'fail': function (error) {
                swal({
                        title: "error！",
                        text: "网络错误！",
                        type: "error",
                        confirmButtonText: "Cool"
                    });
            }
        })
    })
});