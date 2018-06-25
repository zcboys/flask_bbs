/**
 * Created by zc on 2018/5/22.
 */

$(function () {
    $(".highlight-btn").click(function () {
        //获取本点击事件的标签
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";

        if (highlight){
            url = "/cms/uhpost/";
        }else {
            url = "/cms/hpost/";
        }

        zlajax.post({
            'url': url,
            'data':{
                'post_id':post_id
            },
            'success':function (data) {
                if(data['code'] === 200){
                    if(url == '/cms/hpost/'){
                        swal("success！", "帖子加精成功。", "success");
                        setTimeout(function () {
                            window.location.reload();
                        }, 500);
                    }else {
                        swal("success！", "取消加精成功。", "success");
                        setTimeout(function () {
                            window.location.reload();
                        }, 500);
                    }

                }else {
                    swal("出错啦。。。", data['message'], "error");
                }
            }
        });
    });
});


$(function () {
    $(".delete-post-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr('data-id');

        swal({
            title: "确定要删除这个帖子吗？",
            text: "删除后可就无法恢复了。",
            type: "warning",
            showCancelButton: true,
            closeOnConfirm: false,
            confirmButtonText: "是的，我要删除！",
            confirmButtonColor: "#ec6c62",
            cancelButtonText: "容我三思"
        },
            function(isConfirm){
                if(isConfirm){
                    zlajax.post({
                        'url': '/cms/dpost/',
                        'data': {
                            "post_id":post_id
                        },
                        'success':function (data) {
                            if(data['code'] === 200 ){
                                swal("删除！", "帖子已经被删除。", "success");
                                window.location.reload();
                            }else {
                                swal("出错啦。。。", data['message'], "error");
                            }

                        },
                        'fail': function (error) {
                            swal("出错啦。。。", error, "error");
                        }
                    });

                }
                else {
                    swal({title:"已取消",
                            text:"您取消了删除操作！",
                            type:"error"
                    })
                }
        });
    });
});
