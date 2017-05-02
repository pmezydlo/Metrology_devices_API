'use strict';   // See note about 'use strict'; below

var myApp = angular.module('myApp', [
 'ngRoute',
]);

myApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/', {
                templateUrl: '/static/partials/index.html',
            }).
            when('/sys', {
                templateUrl: '../static/partials/sys_page.html',
            }).
            when('/dev', {
                templateUrl: '../static/partials/dev_page.html',
            }).
            when('/log', {
                templateUrl: '../static/partials/log_page.html',
            }).
            when('/task', {
                templateUrl: '../static/partials/task_page.html',
            }).
            otherwise({
                redirectTo: '/'
            });
        }]);

myApp.controller('mainController', ($scope, $http) => {

    $scope.formData = {};
    $scope.devData = {};
    $scope.newStatus = 'RUN';
    $scope.logsData = {}

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

    $scope.sysStop = () => {
        $http.post('/api/sysStop')
        .success((data) => {
            console.log(data);
        })
        .error((error) => {
            console.log('Error: ' + error);
        });
    };

    $scope.actDev = (devID) => {
        $http.post('/api/dev/act/'+devID, $scope.newStatus)
        .success((data) => {
            $scope.newStatus = data;
            console.log(data);
        })
        .error((error) => {
            console.log('Error: ' + error);
        });
    };

    $scope.deleteDev = (devID) => {
        $http.delete('/api/dev/' + devID)
        .success((data) => {
            $scope.devData = data;
            console.log(data);
        })
        .error((data) => {
        console.log('Error: ' + data);
        });
    };

    $scope.deleteLogs = () => {
        $http.delete('/api/logs')
        .success((data) => {
            $scope.logsData = data;
            console.log(data);
        })
        .error((data) => {
        console.log('Error: ' + data);
        });
    };

    $http.get('/api/logs')
    .success((data) => {
        $scope.logsData = data;
        console.log(data);
    })
    .error((error) => {
        console.log('Error: ' + error);
    });

});
