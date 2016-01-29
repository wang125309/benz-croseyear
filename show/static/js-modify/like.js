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
    $(document).on("touchmove",function(){
        return false;
    });
    var index = 0;
    var r = [];
    var total = 0;
    var setData = function() {
        $(".index").html((index+1)+"/"+total);
        $(".showPic").remove();
        $('<div class="showPic" style="background-image: url(http://benz.importos.com/'+r[index].src+');"></div>').insertBefore(".go-left");
        $(".name").html(r[index].userid);

    };
    var setMyInfo = function() {
        $.get("/info",function(data){
            if(data.status == 'success') {
                $("#like1-tickets").html("剩余" + data.data.tickets1 + "张票");
                $("#like2-tickets").html("剩余" + data.data.tickets2 + "张票");
            }
        });
    };
    setMyInfo();
    var getAllByRank = function() {
        var url = '';
        if(getQueryParams("type") == '1') {
            url = '/rank1';
        }
        else {
            url = '/rank2';
        }
        $.get(url,function(data){
            if(data.status == 'success') {
                for( i in data.data ) {
                    console.log(data.data[i].src);
                    if(data.data[i].src != "") {
                        r.push(data.data[i]);
                    }
                }
                total = r.length;
                setData();
            }
            else if(data.status == 'error' && data.reason == 'need login') {
                location.href = "/template/login.html?s=like";
            }
        });

    }
    var goLeft = function() {
        if(index <= 0) {
            index = total - 1;
            setData();
        }
        else {
            index -= 1;
            setData();
        }
    };
    var goRight = function() {
        if(index >= total - 1) {
            index = 0;
            setData();
        }
        else {
            index += 1;
            setData();
        }
    };
    $(".go-left").on("tap",function(){
        goLeft();
    });
    $(".go-right").on("tap",function(){
        goRight();
    });
    $(".uploadPic").on("swipeRight",function(){
        goLeft();
    });
    $(".uploadPic").on("swipeLeft",function(){
        goRight();
    });

    getAllByRank();
    $("#like1").on("tap",function(){
        $.get("/like1",{
            "uid" : r[index].id,
            "type" : 1
        },function(data){
            if(data.status == 'success') {
                alert("投票成功"); 
                setMyInfo();
            }
            else {
                if(data.reason == 'already send ticket') {
                    alert("您已经给ta投过票了哦");
                }
                else if(data.reason == 'no tickets left') {
                    alert("这个类型的票您已经没有剩余的咯");
                }
                else if(data.reason == 'need login') {
                    location.href = "/template/login.html?s=like";
                }
                else if(data.reason == 'ticket not start') {
                    alert("当前不在投票时间段内");
                }
                else {
                    alert("未知错误");
                }
            }
        });
    });
    $("#like2").on("tap",function(){
        $.get("/like2",{
            "uid" : r[index].id,
            "type" : 2
        },function(data){
            if(data.status == 'success') {
                alert("投票成功"); 
                setMyInfo();
            }
            else {
                if(data.reason == 'already send ticket') {
                    alert("您已经给ta投过票了哦");
                }
                else if(data.reason == 'no tickets left') {
                    alert("这个类型的票您已经没有剩余的咯");
                }
                else if(data.reason == 'need login') {
                    location.href = "/template/login.html?s=like";
                }
                else if(data.reason == 'ticket not start') {
                    alert("当前不在投票时间段内");
                }
                else {
                    alert("未知错误");
                }
            }
        });
            
    });
}
