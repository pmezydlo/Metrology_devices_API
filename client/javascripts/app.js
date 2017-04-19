angular.module('node_dev', [])
.controller('mainController', ($scope, $http) => {

    $scope.formData = {};
    $scope.devData = {};
    $scope.logsData = {};
    $scope.taskData = {};

    $scope.deleteLogs = () => {
        $http.delete('/api/v1/logs')
        .success((data) => {
            $scope.logsData = data;
            console.log(data);
        })
        .error((data) => {
        console.log('Error: ' + data);
        });
    };

    $http.get('/api/v1/logs')
    .success((data_logs) => {
        $scope.logsData = data_logs;
        console.log(data_logs);
    })
    .error((error) => {
        console.log('Error: ' + error);
    });

    $http.get('/api/v1/dev')
    .success((data) => {
        $scope.devData = data;
        console.log(data);
    })
    .error((error) => {
        console.log('Error: ' + error);
    });

    $scope.createDev = () => {
        $http.post('/api/v1/dev', $scope.formData)
        .success((data) => {
            $scope.formData = {};
            $scope.devData = data;
            console.log(data);
        })
        .error((error) => {
            console.log('Error: ' + error);
        });
    };

    $scope.deleteDev = (devID) => {
        $http.delete('/api/v1/dev/' + devID)
        .success((data) => {
            $scope.devData = data;
            console.log(data);
        })
        .error((data) => {
        console.log('Error: ' + data);
        });
    };
});
