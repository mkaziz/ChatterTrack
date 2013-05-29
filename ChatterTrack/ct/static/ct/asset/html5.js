

ChatterTrack = {
    
    createHighChart : function () { 
                $('#container').highcharts({
                chart: {
                    type: 'column'
                },
                legend: {
                    enabled: true
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
                        },
                        
                        point: {
                            events: {
                                click: function() {
                                    alert ('Category: '+ this.category +', value: '+ this.y);
                                }
                            }
                        }
                    }
                },     
                series: []
            })},
    
    clearChart : function () {
        
        var chart = $("#container").highcharts();
        var series = chart.series;
        
        while (series.length != 0)
        {
            series[0].remove();
        }
        
    },
    
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
            a = data.results.categories.science;
            b = data.results.categories.business;
            c = data.results.categories.sports;
            d = data.results.categories.food;
            e = data.results.categories.politics;
            f = data.results.categories.entertainment;
            g = data.results.categories.technology;
            h = data.results.categories["healthy-living"];
            i = a + b + c + d + e + f + g;
            ap = Math.round(100 * (a / i));
            bp = Math.round(100 * (b / i));
            cp = Math.round(100 * (c / i));
            dp = Math.round(100 * (d / i));
            ep = Math.round(100 * (e / i));
            fp = Math.round(100 * (f / i));
            gp = Math.round(100 * (g / i));
            hp = Math.round(100 * (h / i));

            var chart = $("#container").highcharts()
            chart.addSeries({
                name: data.results.name,
                data: [ap, bp, cp, dp, ep, fp, gp, hp] 
            });
            chart.series[chart.series.length-1].stream_id = data.results.stream_id;
            //return false;
        }
    }
    
    
};

$(document).ready( function () {
    $(function() {
        $('.people').click(function(){
            $('.people').removeClass('highlight');  
            $(this).addClass('highlight');
            $('#vizbox').fadeIn();
            $('html, body').delay(600).animate({scrollTop:$(this.hash).offset().top}, 500);
        });
    });  
    
    ChatterTrack.createHighChart();
});
