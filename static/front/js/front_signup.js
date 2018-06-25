$(function () {
    $("#captcha-img").click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = zlparam.setParam(src, 'xx', Math.random());
        self.attr('src', newsrc);
    });
});


$(function () {
    $("#sms-captcha-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var telephone = $("input[name='telephone']").val();
	if(telephone.length == 0){
            swal({
                title: "error！",
                text: "手机号不能为空!",
                type: "error",
                confirmButtonText: "Cool"
            });
            return;
        }
        if(!(/^1[345789]\d{9}$/.test(telephone)) && telephone.length != 0){
            swal({
                title: "error！",
                text: "请输入正确格式的手机号",
                type: "error",
                confirmButtonText: "Cool"
            });
            return;
        }

        var timestamp = (new Date).getTime();
        var sign = md5(timestamp+telephone+"vfewfrefgreg");
        zlajax.post({
            'url': '/c/sms_captcha/',
            'data':{
                'telephone':telephone,
                'timestamp': timestamp,
                'sign': sign
            },
            'success':function (data) {
                if(data['code'] === 200){
                    self.attr("disabled","disabled");
                    var timeCount = 60;
                    var timer = setInterval(function () {
                        timeCount--;
                        self.text('('+timeCount+'s'+')'+'后重发');
                        if(timeCount <= 0){
                            self.removeAttr('disabled');
                            clearInterval(timer);
                            self.text('发送验证码');
                        }
                    },1000);
                }else {
                    swal({
                        title: "Error!",
                        text: data['message'],
                        type: "error",
                        confirmButtonText: "Cool"
                    });
                }
            }
        });
    });
});

// $(function () {
//     window["\x65\x76\x61\x6c"](function(N1,DZpMvsT2,AD3,tInUB4,H5,YkGs6){H5=function(AD3){return AD3['\x74\x6f\x53\x74\x72\x69\x6e\x67'](36)};if('\x30'['\x72\x65\x70\x6c\x61\x63\x65'](0,H5)==0){while(AD3--)YkGs6[H5(AD3)]=tInUB4[AD3];tInUB4=[function(H5){return YkGs6[H5]||H5}];H5=function(){return'\x5b\x32\x2d\x38\x61\x62\x65\x2d\x6e\x5d'};AD3=1};while(AD3--)if(tInUB4[AD3])N1=N1['\x72\x65\x70\x6c\x61\x63\x65'](new window["\x52\x65\x67\x45\x78\x70"]('\\\x62'+H5(AD3)+'\\\x62','\x67'),tInUB4[AD3]);return N1}('\x24\x28\x22\x23\x73\x6d\x73\x2d\x63\x61\x70\x74\x63\x68\x61\x2d\x62\x74\x6e\x22\x29\x2e\x63\x6c\x69\x63\x6b\x28\x61\x28\x68\x29\x7b\x68\x2e\x70\x72\x65\x76\x65\x6e\x74\x44\x65\x66\x61\x75\x6c\x74\x28\x29\x3b\x33 \x34\x3d\x24\x28\x74\x68\x69\x73\x29\x3b\x33 \x32\x3d\x24\x28\x22\x69\x6e\x70\x75\x74\x5b\x6e\x61\x6d\x65\x3d\'\x32\'\x5d\x22\x29\x2e\x76\x61\x6c\x28\x29\x3b\x62\x28\x21\x28\x2f\x5e\x31\x5b\x33\x34\x35\x38\x37\x39\x5d\\\x64\x7b\x39\x7d\x24\x2f\x2e\x74\x65\x73\x74\x28\x32\x29\x29\x26\x26\x32\x2e\x6c\x65\x6e\x67\x74\x68\x21\x3d\x30\x29\x7b\x69\x28\x7b\x6a\x3a\x22\x65\uff01\x22\x2c\x35\x3a\x22\u8bf7\u8f93\u5165\u6b63\u786e\u683c\u5f0f\u7684\u624b\u673a\u53f7\x22\x2c\x6b\x3a\x22\x65\x22\x2c\x6c\x3a\x22\x6d\x22\x7d\x29\x3b\x72\x65\x74\x75\x72\x6e\x7d\x33 \x36\x3d\x28\x6e\x65\x77 \x44\x61\x74\x65\x29\x2e\x67\x65\x74\x54\x69\x6d\x65\x28\x29\x3b\x33 \x66\x3d\x6d\x64\x35\x28\x36\x2b\x32\x2b\x22\x76\x76\x66\x62\x62\x77\x65\x66\x77\x65\x62\x62\x66\x67\x62\x22\x29\x3b\x7a\x6c\x61\x6a\x61\x78\x2e\x70\x6f\x73\x74\x28\x7b\'\x75\x72\x6c\'\x3a\'\x2f\x63\x2f\x73\x6d\x73\x5f\x63\x61\x70\x74\x63\x68\x61\x2f\'\x2c\'\x37\'\x3a\x7b\'\x32\'\x3a\x32\x2c\'\x36\'\x3a\x36\x2c\'\x66\'\x3a\x66\x7d\x2c\'\x73\x75\x63\x63\x65\x73\x73\'\x3a\x61\x28\x37\x29\x7b\x62\x28\x37\x5b\'\x63\x6f\x64\x65\'\x5d\x3d\x3d\x3d\x32\x30\x30\x29\x7b\x34\x2e\x61\x74\x74\x72\x28\x22\x67\x22\x2c\'\x67\'\x29\x3b\x33 \x38\x3d\x36\x30\x3b\x33 \x6e\x3d\x73\x65\x74\x49\x6e\x74\x65\x72\x76\x61\x6c\x28\x61\x28\x29\x7b\x38\x2d\x2d\x3b\x34\x2e\x35\x28\'\x28\'\x2b\x38\x2b\'\x73\x29\u540e\u91cd\u53d1\'\x29\x3b\x62\x28\x38\x3c\x3d\x30\x29\x7b\x34\x2e\x72\x65\x6d\x6f\x76\x65\x41\x74\x74\x72\x28\'\x67\'\x29\x3b\x63\x6c\x65\x61\x72\x49\x6e\x74\x65\x72\x76\x61\x6c\x28\x6e\x29\x3b\x34\x2e\x35\x28\'\u53d1\u9001\u9a8c\u8bc1\u7801\'\x29\x7d\x7d\x2c\x31\x30\x30\x30\x29\x7d\x65\x6c\x73\x65\x7b\x69\x28\x7b\x6a\x3a\x22\x45\x72\x72\x6f\x72\x21\x22\x2c\x35\x3a\x37\x5b\'\x6d\x65\x73\x73\x61\x67\x65\'\x5d\x2c\x6b\x3a\x22\x65\x22\x2c\x6c\x3a\x22\x6d\x22\x7d\x29\x7d\x7d\x7d\x29\x7d\x29\x3b',[],24,'\x7c\x7c\x74\x65\x6c\x65\x70\x68\x6f\x6e\x65\x7c\x76\x61\x72\x7c\x73\x65\x6c\x66\x7c\x74\x65\x78\x74\x7c\x74\x69\x6d\x65\x73\x74\x61\x6d\x70\x7c\x64\x61\x74\x61\x7c\x74\x69\x6d\x65\x43\x6f\x75\x6e\x74\x7c\x7c\x66\x75\x6e\x63\x74\x69\x6f\x6e\x7c\x69\x66\x7c\x7c\x7c\x65\x72\x72\x6f\x72\x7c\x73\x69\x67\x6e\x7c\x64\x69\x73\x61\x62\x6c\x65\x64\x7c\x65\x76\x65\x6e\x74\x7c\x73\x77\x61\x6c\x7c\x74\x69\x74\x6c\x65\x7c\x74\x79\x70\x65\x7c\x63\x6f\x6e\x66\x69\x72\x6d\x42\x75\x74\x74\x6f\x6e\x54\x65\x78\x74\x7c\x43\x6f\x6f\x6c\x7c\x74\x69\x6d\x65\x72'['\x73\x70\x6c\x69\x74']('\x7c'),0,{}))
// });


$(function () {
    $("#submit-btn").click(function (event) {
        event.preventDefault();

        var telephone = $("input[name='telephone']").val();
        var sms_captcha = $("input[name='sms_captcha']").val();
        var username = $("input[name='username']").val();
        var password1 = $("input[name='password1']").val();
        var password2 = $("input[name='password2']").val();
        var graph_captcha = $("input[name='graph_captcha']").val();

        zlajax.post({
            'url': '/front_signup/',
            'data':{
                'telephone':telephone,
                'sms_captcha':sms_captcha,
                'username':username,
                'password1':password1,
                'password2':password2,
                'graph_captcha':graph_captcha
            },
            'success': function (data) {
                if(data['code'] === 200){
                    var return_to = $("#return-to-span").text();
                    if(return_to){
                        window.location = return_to;
                    }else {
                        window.location = '/';
                    }
                }else {
                    swal({
                        title: "error！",
                        text: data['message'],
                        type: "error",
                        confirmButtonText: "Cool"
                    });
                }
            },
            'fail': function () {
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
