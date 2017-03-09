'use strict';

angular.module('documentosApp').service('RedirectService', function() {

    var message = '';

    var setMessage = function(val){
        message = val;
    };

    var getMessage = function(){
      return message;
    };

    return {
        setMessage: setMessage,
        getMessage: getMessage,
    };

});