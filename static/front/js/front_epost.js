/**
 *  * Created by zc on 2018/5/18.
 *   */

$(function () {
    var ue = UE.getEditor('editor', {
      serverUrl: "/ueditor/upload/"
   });

    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleInput = $("input[name='title']");
        var boardSelect = $("select[name='board_id']");

        var title = titleInput.val();
        var board_id = boardSelect.val();
        var content = ue.getContent();
        var url_edit = window.location.pathname;
        zlajax.post({
            'url': url_edit,
            'data': {
                'title': title,
                'content': content,
                'board_id': board_id
            },
            'success':function (data) {
                if(data['code'] === 200 ){
                    swal({
                        title: "OK！",
                        text: "修改帖子成功!",
                        timer: 2000,
                        icon: "success",
                        button: false
                    });
                    window.location = '/';
                }
                else {
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
                swal("出错啦。。。", error, "error");
            }
        });
    });
});



