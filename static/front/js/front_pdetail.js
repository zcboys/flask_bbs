/**
 * Created by zc on 2018/5/22.
 */


$(function () {
    var ue = UE.getEditor("editor", {
        "serverUrl": '/ueditor/upload/',
        toolbars: [
            ['fullscreen', 'source', 'undo', 'redo'],
            ['bold', 'italic', 'underline', 'fontborder', 'strikethrough', 'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', 'cleardoc']
        ]
    });　
    window.ue = ue;
});

$(function () {
    $("#comment-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr('data-is-login');
        if(!loginTag){
            window.location = '/front_signin/';
        }else {
            var content = window.ue.getContent();
            var post_id = $("#post-content").attr("data-id");
            zlajax.post({
                'url': '/acomment/',
                'data': {
                    'content': content,
                    'post_id': post_id
                },
                'success': function (data) {
                    if (data['code'] === 200){
                        window.location.reload();
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
        }
    });
});