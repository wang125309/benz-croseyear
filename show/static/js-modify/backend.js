require("../../bower_components/angular/angular.js");
require("../../bower_components/angular-animate/angular-animate.js");
jQuery = require("../../bower_components/jquery/dist/jquery.js");
require("../../bower_components/bootstrap/dist/js/bootstrap.js");
require("../../bower_components/bootstrap-multiselect/dist/js/bootstrap-multiselect.js");
loginCtrl = angular.module('app',['ngAnimate']).controller('loginCtrl',['$scope',function($scope){
    $scope.startUpload = function() {
        jQuery.get("/startupload",function(data){
            if(data.status == 'success') {
                alert('可以进行文件上传了');
            }
        });
    };
    $scope.endUpload = function() {
        jQuery.get("/endupload",function(data){
            if(data.status == 'success') {
                alert('文件上传已经不能再继续了');
            }
        });
    };
    $scope.startTicket = function() {
        jQuery.get("/startticket",function(data){
            if(data.status == 'success') {
                alert('开始投票阶段');
            }
        });
    };
    $scope.endTicket = function() {
        jQuery.get("/endticket",function(data){
            if(data.status == 'success') {
                alert('已结束投票阶段');
            }
        });
    };
    $scope.startNewTicket1 = function() {
        jQuery.get("/startticket1",function(data){
            if(data.status == 'success') {
                alert('开始新一次风采投票阶段');
            }
        });
    };
    $scope.startNewTicket2 = function() {
        jQuery.get("/startticket2",function(data){
            if(data.status == 'success') {
                alert('开始新一次pose投票阶段');
            }
        });
    };
}])
loginCtrl.$inject = ['$scope','loginCtrl']; 
