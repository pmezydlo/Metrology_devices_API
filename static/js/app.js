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

myApp.controller('mainController', ($scope, $http, $timeout) => {

    $scope.formData = {};
    $scope.devData = {};
    $scope.newStatus = 'RUN';
    $scope.logsData = {};
    $scope.sysData = {};

    $scope.taskData = {};
    $scope.taskFormData = {};
    $scope.verData = {};

    $scope.status = 'Current';
    var runtime_ver = 0;

    function get_data() {
        $http.get('/api/task')
            .success((data) => {
                $scope.taskData = data;
                console.log(data);
            })
            .error((error) => {
                console.log('Error: ' + error);
            });

    $http.get('/api/dev')
    .success((data) => {
        $scope.devData = data;
        console.log(data);
    })
    .error((error) => {
        console.log('Error: ' + error);
    });

    $http.get('/api/sys/info')
    .success((data) => {
        $scope.sysData = data;
        console.log(data);
    })
    .error((error) => {
        console.log('Error: ' + error);
    });

    $http.get('/api/ver')
    .success((data) => {
        $scope.verData = data;
        console.log(data);
    })
    .error((error) => {
        console.log('Error: ' + error);
    });

    $http.get('/api/logs')
    .success((data) => {
        $scope.logsData = data;
        console.log(data);
    })
    .error((error) => {
        console.log('Error: ' + error);
    });
    }

    var timer_fun = function() {
        $http.get('/api/ver')
        .success((data) => {
            $scope.verData = data;
            if (runtime_ver < data.runtime) {
                get_data();
                runtime_ver = data.runtime;
                $scope.status = 'Not Current';
            } else { 
                $scope.status = 'Current';
            }
        })
        $timeout(timer_fun, 500);
    }

    $timeout(timer_fun, 500);
    get_data();
    
    $scope.createTask = () => {
        $http.post('/api/task', $scope.taskFormData)
        .success((data) => {
            console.log()
            $scope.taskFormData = {};
            $scope.taskData = data;
            console.log(data);
        })
        .error((error) => {
            console.log('Error: ' + error);
        });
    };

    $scope.deleteTask = (taskID) => {
        $http.delete('/api/task/' + taskID)
        .success((data) => {
            $scope.taskData = data;
            console.log(data);
        })
        .error((data) => {
        console.log('Error: ' + data);
        });
    };

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
        $http.post('/api/sys/stop')
        .success((data) => {
            console.log(data);
        })
        .error((error) => {
            console.log('Error: ' + error);
        });
    };

    $scope.sysShutdown = () => {
        $http.post('/api/sys/shutdown')
        .success((data) => {
            console.log(data);
        })
        .error((error) => {
            console.log('Error: ' + error);
        });
    };

    $scope.sysStart = () => {
        $http.post('/api/sys/start')
        .success((data) => {
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


});
