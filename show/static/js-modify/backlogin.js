require("../../bower_components/angular/angular.js");
require("../../bower_components/angular-animate/angular-animate.js");
jQuery = require("../../bower_components/jquery/dist/jquery.js");
require("../../bower_components/bootstrap/dist/js/bootstrap.js");
require("../../bower_components/bootstrap-multiselect/dist/js/bootstrap-multiselect.js");
loginCtrl = angular.module('app',['ngAnimate']).controller('loginCtrl',['$scope',function($scope){
    $scope.user = {
        uname : "",
        upwd : ""
    };
    $scope.login = function() {
        jQuery.get("/backendlogin",$scope.user,function(data){
            if(data.status == "success") {
                location.href = "/template/backend.html";
            }
            else {
                alert("用户名或密码错误");
            }
        });
    };
}])
loginCtrl.$inject = ['$scope','loginCtrl']; 
