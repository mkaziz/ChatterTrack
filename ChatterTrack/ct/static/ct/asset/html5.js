$(document).ready( function () {
    $(function() {
        $('.people').click(function(){
            $('.people').removeClass('highlight');  
            $(this).addClass('highlight');
            $('#vizbox').fadeIn();
            $('html, body').delay(600).animate({scrollTop:$(this.hash).offset().top}, 500);
        });
        $('.p5').click(function(){ 
            $('#name').hide().html("Mike Bloomberg's followers are talking about:").fadeIn();
            ChatterTrack.ajaxFunctions.getGraph("dd429a69b5d6284796f43479c9a506a3",0.8);
            return false;
        });

        $('.p9').click(function(){ 
            
            ChatterTrack.ajaxFunctions.getGraph("d21256f37601d2800b0b9604f0e94e1e",0.8);
            return false;
        });
       

    });  
});

ChatterTrack = {
    
    ajaxFunctions : {
        
        getGraph : function (name, streamId, confidence) {
            "use strict";
            $('#name').hide().html(name + "'s followers are talking about:").fadeIn();
            var jqxhr = $.get("http://ec2-54-244-189-248.us-west-2.compute.amazonaws.com/ct/analyzeStream/", {
                "stream_id" : streamId,
                "confidence" : confidence
            }, ChatterTrack.ajaxFunctions.updateGraph).error(function () {
                    alert("Oops! Unable to fetch stream results.");
                });
        
        },
        
        updateGraph : function (data) {
            a = data.results.science;
            b = data.results.business;
            c = data.results.sports;
            d = data.results.food;
            e = data.results.politics;
            f = data.results.entertainment;
            g = data.results.technology;
            h = data.results["healthy-living"];
            i = a + b + c + d + e + f + g;
            ap = Math.round(100 * (a / i));
            bp = Math.round(100 * (b / i));
            cp = Math.round(100 * (c / i));
            dp = Math.round(100 * (d / i));
            ep = Math.round(100 * (e / i));
            fp = Math.round(100 * (f / i));
            gp = Math.round(100 * (g / i));
            hp = Math.round(100 * (h / i));

            $('#container').highcharts({
                chart: {
                    type: 'column'
                },
                legend: {
                    enabled: false
                },
                credits : {
                    enabled : false
                },
                exporting: {
                    enabled: false
                },
                title: {
                    text: null,  
                },
                subtitle: {
                    text: null,  
                },
                tooltip: {
                    enabled: false,
                },
                xAxis: {
                    categories: [
                        'Science', 'Business', 'Sports', 'Food', 'Politics', 'Entertainment', 'Technology', 'Health'
                    ]
                }, 
                yAxis: {
                    min: 0,
                    title: {
                        text: null
                    }
                }, 
                plotOptions: {
                    column: {
                        cursor: 'pointer',
                        
                        dataLabels: {
                            enabled: true,
                            color: '#2F7ED8',
                            style: {
                                fontWeight: 'bold'
                            },
                            formatter: function() {
                                return this.y +'%';
                            }
                        }
                    }
                },     
                series: [{
                    name: 'tweets',
                    data: [ap, bp, cp, dp, ep, fp, gp, hp] 
                }]
            });
            //return false;
        }
    }
    
    
};

