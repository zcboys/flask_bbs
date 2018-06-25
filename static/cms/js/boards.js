/**
 * Created by zc on 2018/5/16.
 */

$(function () {
    $("#save-board-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#board-dialog");
        var name = $("input[name='name']").val();
        var submitType = self.attr('data-type');
        var boardId = self.attr("data-id");

        var url = '';
        if(submitType === 'update'){
            url = '/cms/uboard/';
        }else{
            url = '/cms/aboard/';
        }

        zlajax.post({
            'url':url,
            'data':{
                'name':name,
                'board_id':boardId
            },
            'success':function (data) {
                dialog.modal("hide");
                if(data['code'] === 200 ){
                    window.location.reload();
                }else {
                    swal({
                        title: "Error!",
                        text: data['message'],
                        type: "error",
                        confirmButtonText: "Cool"
                    });
                }
            },
            'fail': function () {
                swal({
                        title: "Error!",
                        text: '网络错误',
                        type: "error",
                        confirmButtonText: "Cool"
                    });
            }
        });
    });
});


$(function () {
    $(".edit-board-btn").click(function (event) {
        var self = $(this);
        var dialog = $("#board-dialog");
        dialog.modal("show");

        var tr = self.parent().parent();
        var name = tr.attr("data-name");

        var nameInput = dialog.find("input[name='name']");
        var saveBtn = dialog.find("#save-board-btn");

        nameInput.val(name);
        saveBtn.attr("data-type",'update');
        saveBtn.attr('data-id',tr.attr('data-id'));
    });
});


$(function () {
    $(".delete-board-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr('data-id');

        swal({
            title: "确定要删除这个板块吗？",
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
                        'url': '/cms/dboard/',
                        'data': {
                            "board_id":board_id
                        },
                        'success':function (data) {
                            if(data['code'] === 200 ){
                                swal("删除！", "板块已经被删除。", "success");
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
