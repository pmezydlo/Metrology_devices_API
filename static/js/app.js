'use strict';   // See note about 'use strict'; below

var myApp = angular.module('myApp', [
 'ngRoute',
]);

myApp.controller('mainController', ($scope, $http) => {

    $scope.formData = {};
    $scope.devData = {};

    $http.get('/api/dev')
    .success((data) => {
        $scope.devData = data;
        console.log(data);
    })
    .error((error) => {
        console.log('Error: ' + error);
    });

    $scope.createDev = () => {
        $http.post('/api/dev', $scope.formData)
        .success((data) => {
            $scope.formData = {};
            $scope.devData = data;
            console.log(data);
        })
        .error((error) => {
            console.log('Error: ' + error);
        });
    };
});
