$(function () {
    $("#submit").click(function (event) {
        // event.preventDefault是阻止按钮默认的提交表单的事件
        event.preventDefault();

        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd1]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd1 = newpwdE.val();
        var newpwd2 = newpwd2E.val();
        // 1、要在模板的meta标签中渲染一个csrf-token
        // 2、在ajax请求的头部中设置X-CSRFtoken
        zlajax.post({
            'url': '/cms/resetpwd/',
            'data':{
                'oldpwd': oldpwd,
                'newpwd1': newpwd1,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                if (data['code'] === 200){
                    swal({
                        title: "OK！",
                        text: "密码修改成功",
                        timer: 2000,
                        icon: "success",
                        button: false
                    });
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
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
        });
    });
});