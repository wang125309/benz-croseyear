require("../../bower_components/angular/angular.js");
jQuery = require("../../bower_components/jquery/dist/jquery.js");
require("../../bower_components/bootstrap/dist/js/bootstrap.js");
window.getQueryParams = function(name,url) {                                         
    if (!url) url = location.href;
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS  );
    var results = regex.exec( url  );
    return results == null ? null : results[1];
};
loginCtrl = angular.module('app',[]).controller('loginCtrl',['$scope',function($scope){
    var refrash = function() {
        var url = ''; 
        if(getQueryParams("type")=="1") {
            $scope.type = 1;
            url = "/rank1";
        }
        else if(getQueryParams("type")=="2") {
            $scope.type = 2;
            url = '/rank2';
        }
        jQuery.get(url,function(data){
            if(data.status == 'success') {
                $scope.rank1 = [];
                $scope.rank2 = [];
                $scope.total = 0;
                for(i in data.data) {
                    if($scope.type == 1) {
                        $scope.total += data.data[i].like1;
                    }
                    if($scope.type == 2) {
                        $scope.total += data.data[i].like2;
                    }
                }
                $scope.total = "当前投票数：" + $scope.total;
                for(i=0;i<6;i++) {
                    data.data[i].rank = i+1;
                    $scope.rank1.push(data.data[i]);
                }
                for(i=6;i<12;i++) {
                    data.data[i].rank = i+1;
                    $scope.rank2.push(data.data[i]);
                }
                $scope.$apply();
            }
        });
    };
    refrash();
    setInterval(function(){
        refrash();
    },1500); 
}])
loginCtrl.$inject = ['$scope','loginCtrl']; 
