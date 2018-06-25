$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var nameInput = $("input[name='name']");
        var imageInput = $("input[name='image_url']");
        var linkInput = $("input[name='link_url']");
        var priorityInput = $("input[name='priority']");


        var name = nameInput.val();
        var image_url = imageInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();
        var submitType = self.attr('data-type');
        var bannerId = self.attr("data-id");

        if(!name || !image_url || !link_url || !priority){
            zlalert.alertInfoToast('请输入完整的轮播图数据！');
            return;
        }

        var url = '';
        if(submitType === 'update'){
            url = '/cms/ubanner/';
        }else{
            url = '/cms/abanner/';
        }

        zlajax.post({
            "url": url,
            'data':{
                'name':name,
                'image_url': image_url,
                'link_url': link_url,
                'priority':priority,
                'banner_id': bannerId
            },
            'success': function (data) {
                dialog.modal("hide");
                if(data['code'] == 200){
                    // 重新加载这个页面
                    window.location.reload();
                }else{
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
    $(".edit-banner-btn").click(function (event) {
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");

        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");
        var saveBtn = dialog.find("#save-banner-btn");

        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        saveBtn.attr("data-type",'update');
        saveBtn.attr('data-id',tr.attr('data-id'));
    });
});

$(function () {
    $(".delete-banner-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');

        swal({
            title: "确定要删除这个轮播图吗？",
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
                        'url': '/cms/dbanner/',
                        'data': {
                            "banner_id":banner_id
                        },
                        'success':function (data) {
                            if(data['code'] === 200 ){
                                swal("删除！", "轮播图已经被删除。", "success");
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


$(function () {
    zlqiniu.setUp({
        'domain': 'http://p6lvi6nq8.bkt.clouddn.com/',
        'browse_btn': 'upload-btn',
        'uptoken_url': '/c/uptoken/',
        'success': function (up, file, info) {
            var imageInput = $("input[name='image_url']");
            imageInput.val(file.name);
        }
    });
});