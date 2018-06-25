/**
 * Created by zc on 2018/5/18.
 */
$(function () {
    var ue = UE.getEditor("editor", {
      "serverUrl": '/ueditor/upload/'
    });
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleInput = $("input[name='title']");
        var boardSelect = $("select[name='board_id']");

        var title = titleInput.val();
        var board_id = boardSelect.val();
        var content = ue.getContent();

        swal(
            {   title:"success",
                text:"帖子发布成功!",
                type:"success",
                showCancelButton:true,
                confirmButtonColor:"#DD6B55",
                confirmButtonText:"再发一篇！",
                cancelButtonText:"回到首页",
                closeOnConfirm:false,
                closeOnCancel:false
            },
            function(isConfirm) {
                if(isConfirm)
                {
                    zlajax.post({
                        'url': '/apost/',
                        'data': {
                            'title': title,
                            'content': content,
                            'board_id': board_id
                        },
                        'success':function (data) {
                            if(data['code'] === 200 ){
                                titleInput.val("");
                                ue.setContent("");
                                window.location.reload();
                            }
                        },
                        'fail': function (error) {
                            swal("出错啦。。。", error, "error");
                        }

                    });

                }
                else{
                    zlajax.post({
                        'url': '/apost/',
                        'data': {
                            'title': title,
                            'content': content,
                            'board_id': board_id
                        },
                        'success':function (data) {
                            if(data['code'] === 200 ){
                                window.location = '/';
                            }
                        },
                        'fail': function (error) {
                            swal("出错啦。。。", error, "error");
                        }
                    });

                }
            });

    });

});