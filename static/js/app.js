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
            when('/addtask', {
                templateUrl: '../static/partials/add_task_page.html',
            }).
            when('/files', {
                templateUrl: '../static/partials/files_page.html',
            }).
            when('/res', {
                templateUrl: '../static/partials/res_page.html',
            }).
            otherwise({
                redirectTo: '/'
            });
        }]);

myApp.controller('mainController', ($scope, $http, $timeout) => {

    $scope.formData = {};
    $scope.devData = {};
    $scope.logsData = {};
    $scope.sysData = {};
    $scope.fileData = {};
    $scope.resultsData = {};

    $scope.taskData = {};
    $scope.taskFormData = {};
    $scope.taskFormData.msg = '';
    $scope.verData = {};

    $scope.sel_dev  = {};
    $scope.cmds = {};
    $scope.formCmdData = {};

    $scope.status = 'Current';
    var runtime_ver = 0;

    $scope.addCmd = () => {
        var cmd_str = '';

        if ("sel_cmd_lv1" in $scope.formCmdData) { 
            if ("cmd" in $scope.formCmdData.sel_cmd_lv1) {
                cmd_str += $scope.formCmdData.sel_cmd_lv1.cmd;
                if ("sel_param_lv1" in $scope.formCmdData) {
                    cmd_str += $scope.formCmdData.sel_param_lv1;
                }
            }
        }

        if ("sel_cmd_lv2" in $scope.formCmdData) { 
            if ("cmd" in $scope.formCmdData.sel_cmd_lv2) {
                cmd_str += $scope.formCmdData.sel_cmd_lv2.cmd;
                if ("sel_param_lv2" in $scope.formCmdData) {
                    cmd_str += $scope.formCmdData.sel_param_lv2;
                }
            }
        }

        if ("sel_cmd_lv3" in $scope.formCmdData) { 
            if ("cmd" in $scope.formCmdData.sel_cmd_lv3) {
                cmd_str += $scope.formCmdData.sel_cmd_lv3.cmd;
                if ("sel_param_lv3" in $scope.formCmdData) {
                    cmd_str += $scope.formCmdData.sel_param_lv3;
                }
            }
        }

        $scope.taskFormData.msg += cmd_str+'\n';
        console.log(cmd_str);
    };

    $scope.addEntryPoint = () => {
        var cmd_str = '';

        if ("sel_entry" in $scope.formCmdData) { 
            cmd_str += $scope.formCmdData.sel_entry.name;
            cmd_str += '(';
            if ("sel_entry_arg" in $scope.formCmdData) {
                cmd_str += $scope.formCmdData.sel_entry_arg;
            }
            cmd_str += ')';
            $scope.taskFormData.msg += cmd_str+'\n';
            console.log(cmd_str);
        }
    };

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

    $http.get('/api/results')
    .success((data) => {
        $scope.resultsData = data;
        console.log(data);
    })
    .error((error) => {
        console.log('Error: ' + error);
    });

    $http.get('/api/file')
    .success((data) => {
        $scope.fileData = data;
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

    $http.get('/api/cmds')
    .success((data) => {
        $scope.cmds = data;
        console.log(data);
    })
    .error((error) => {
        console.log('Error: ' + error);
    });
 

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
        $timeout(timer_fun, 1000);
    }

    $timeout(timer_fun, 1000);
    get_data()
 
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

    $scope.checkDev = (devID) => {
        $http.post('/api/checkDev/' + devID)
        .success((data) => {
            console.log(data);
        })
        .error((error) => {
            console.log('Error: ' + error);
        });
    };

    $scope.detectDev = () => {
        $http.post('/api/detectDev', $scope.formData)
        .success((data) => {
            console.log(data);
        })
        .error((error) => {
            console.log('Error: ' + error);
        });
    };

    $scope.stopTask = (taskID) => {
        $http.post('/api/stopTask/' + taskID)
        .success((data) => {
            console.log(data);
        })
        .error((error) => {
            console.log('Error: ' + error);
        });
    };

    $scope.executeTask = (taskID) => {
        $http.post('/api/executeTask/' + taskID)
        .success((data) => {
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

    $scope.deleteRes = (resID) => {
        $http.delete('/api/results/' + resID)
        .success((data) => {
            $scope.resultsData = data;
            console.log(data);
        })
        .error((data) => {
        console.log('Error: ' + data);
        });
    };

    $scope.deleteFile = (name) => {
        $http.delete('/api/file/' + name)
        .success((data) => {
            $scope.fileData = data;
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
