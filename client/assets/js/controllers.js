angular.module('tagboardApp.controllers', [])

.controller('AppCtrl', function( $scope, $rootScope ) {
  $rootScope.baseUrl = 'http://127.0.0.1:5000/api/search/';
})

.controller('mainController', function( $scope, $rootScope, $location ){
  $scope.message = 'Nulla vitae elit libero, a pharetra augue';

})

.controller('resultsController', function( $scope, $routeParams, $rootScope, $http ){
  var apiurl = $rootScope.baseUrl;
  $scope.searchHashtag = $routeParams.hashtag;

  $scope.statusMsg = 'Analizando resultados...';

  $http.get(apiurl + $routeParams.hashtag + '/' + $routeParams.resultsCount).success(function(data, status, headers, config) {
    $scope.tweets = data['twitter']['results'];
    $scope.instagramData = data['instagram']['results'];
    $scope.frequentlyWords = data['frequentlyWords'];
    $scope.approval = data['approval'];
    $scope.positiveItens = $scope.approval[0]['positive'];
    $scope.negativeItens = $scope.approval[0]['negative'];

    var totalApproval = $scope.negativeItens + $scope.positiveItens,
        prcPositive = (100 * $scope.positiveItens / totalApproval),
        prcNegative = (100 * $scope.negativeItens / totalApproval);

    /**
     *
     * Bar chart (palavras frequentes)
     *
     */
    var ctx1 = document.getElementById("frequentlyWordsChart").getContext("2d");
    var data = {
        labels: [
          $scope.frequentlyWords[0][0],
          $scope.frequentlyWords[1][0],
          $scope.frequentlyWords[2][0],
          $scope.frequentlyWords[3][0],
          $scope.frequentlyWords[4][0]
        ],
        datasets: [
            {
                label: "Frequently Words dataset",
                fillColor: "rgba(151,187,205,0.5)",
                strokeColor: "rgba(151,187,205,0.8)",
                highlightFill: "rgba(151,187,205,0.75)",
                highlightStroke: "rgba(151,187,205,1)",
                data: [
                  $scope.frequentlyWords[0][1],
                  $scope.frequentlyWords[1][1],
                  $scope.frequentlyWords[2][1],
                  $scope.frequentlyWords[3][1],
                  $scope.frequentlyWords[4][1]
                ]
            }
        ]
    };
    var myBarChart = new Chart(ctx1).Bar(data);

    /**
     *
     * Pie chart (percentual de aprovação)
     *
     */
    var ctx2 = document.getElementById("prcApprovalChart").getContext("2d");
		var data = [
			{
				value: prcNegative.toPrecision(4),
				color:"#F7464A",
				highlight: "#FF5A5E",
				label: "Negativo"
			},
			{
				value: prcPositive.toPrecision(4),
				color: "#67BD89",
				highlight: "#68F7A1",
				label: "Positivo"
			}
		];
    var myPieChart = new Chart(ctx2).Pie(data);
    $scope.statusMsg = 'Resultados analizados!';
  }).
  error(function(data, status, headers, config) {
    console.log('error');
  });
});
