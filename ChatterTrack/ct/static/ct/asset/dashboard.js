$(document).ready( function () {
    
    
});

dashboard = {
    
    ajax : {
        
        deleteStream : function (streamId) {
            "use strict";
            
            var jqxhr = $.get("http://ec2-54-244-189-248.us-west-2.compute.amazonaws.com/ct/deleteStream/", {
                "stream_id" : streamId
            }, function () {location.reload();} ).error(function () {
                    alert("Oops! Unable to delete stream.");
                });
        },
        
        stopStream : function (streamId) {
            "use strict";
            
            var jqxhr = $.get("http://ec2-54-244-189-248.us-west-2.compute.amazonaws.com/ct/stopStream/", {
                "stream_id" : streamId
            }, function () {location.reload();} ).error(function () {
                    alert("Oops! Unable to stop stream.");
                });
        }
        
    }
    
    
}
