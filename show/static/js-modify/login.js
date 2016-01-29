require("../../bower_components/zepto/zepto.js");
require("../../bower_components/zeptojs/src/touch.js");

window.getQueryParams = function(name,url) {                                         
    if (!url) url = location.href;
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS  );
    var results = regex.exec( url  );
    return results == null ? null : results[1];
};
window.onload = function() {
    $.get("/alreadylogin",function(data){
        if(data.status == 'success') {
            if(getQueryParams("s") == 'upload') {
                location.href = '/template/upload.html';
            }
            else {
                location.href = '/template/like.html';
            }
        }
    });
    $("#submit").on("tap",function(){
        uid = $("#login").val();
        $.get("/login",{
            "userid" : uid
        },function(data){
            if(data.status == 'success') {
                if(getQueryParams("s") == 'upload') {
                    location.href = '/template/upload.html';
                }
                else {
                    location.href = '/template/like.html';
                }
            }
        });
    }); 
}
