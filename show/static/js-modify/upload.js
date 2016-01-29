require("../../bower_components/zepto/zepto.js");
require("../../bower_components/zeptojs/src/touch.js");
window.onload = function() {
    $(".showPic").on("tap",function(){
        $("#upload-file input").click();
    });
    $("#upload-file").on("change",function(){
        var fReader = new FileReader();
        file_element = $("#upload-file input")[0];
        fReader.readAsDataURL(file_element.files[0]);
        fReader.onloadend = function(event) {
            upload_image = event.target.result;
            $(".showPic").css({
                "background-image":"url("+upload_image+")"
            });
        }
    });
    $("#submit").on("click",function(){
        var formdata = new FormData($("#upload-file")[0]);
        $.ajax({
            type : "POST",
            url : "/upload/",
            processData : false,
            data : formdata,
            beforeSend: function(){
                $("#submit").css("display","none");
                $(".upload-process").css("display","block");
            },
            contentType : false,
            success : function(data) {
                if(data.status == 'success') {
                    $(".upload-process").css("display","none");
                    $(".upload-success").css("display","block");
                    $("#submit").css("display","none");
                }
                else if(data.status == 'error' && data.reason == 'upload not start') {
                    $(".upload-process").css("display","none");
                    alert("当前不在上传时间段内");
                }
                else if(data.reason == 'need login') {
                    location.href = "/template/login.html?s=upload";
                }
                else {
                    alert("暂时还不能上传");
                }

            }
        });
    });
}
       
 
