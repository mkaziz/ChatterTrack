//show chart area
$(function() {
    $('.people').click(function(){
        $('.people').removeClass('highlight');  
        $(this).addClass('highlight');
        $('#vizbox').fadeIn();
        $('html, body').delay(600).animate({scrollTop:$(this.hash).offset().top}, 500);
    });

// show Bloomberg
 $('.p5').click(function(){ 
        $.getJSON('mb.json', function(data) {
        a = data.results.science;
        b = data.results.business;
        c = data.results.health;
        d = data.results.food;
        e = data.results.politics;
        f = data.results.entertainment;
        g = data.results.technology;
        h = data.results.sports;

        var colors = Highcharts.getOptions().colors,
            categories = ['Science', 'Business', 'Health', 'Food', 'Politics', 'Entertainment', 'Technology', 'Sports'],
            name = null,
            data = [{
                    y: Math.round(100 * (a / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                    
                }, {
                    y: Math.round(100 * (b / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                   
                }, {
                    y: Math.round(100 * (c / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                    
                }, {
                    y: Math.round(100 * (d / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                   
                }, {
                    y: Math.round(100 * (e / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                    drilldown: {
                        name: 'Politics',
                        categories: ['Gun control', 'Education', 'Environment', 'Immigration', 'National Security', 'Gay rights'],
                        data: [ 4, 33, 14, 23, 12, 34],
                        color: '#64AFDA',
                    }
                }, {
                    y: Math.round(100 * (f / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                   
                }, {
                    y: Math.round(100 * (g / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                  
                }, {
                    y: Math.round(100 * (h / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                  
                }
    ];
    
        function setChart(name, categories, data, color) {
            chart.xAxis[0].setCategories(categories, false);
            chart.series[0].remove(false);
            chart.addSeries({
                name: name,
                data: data,
                color: color || 'white'
            }, false);
            chart.redraw();
        }
    
        var chart = $('#container').highcharts({
            chart: {
                type: 'column'
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
            legend: {
                enabled: false
            },
            xAxis: {
                categories: categories
            },
            yAxis: {
                title: {
                    text: null
                }
            },
            plotOptions: {
                column: {
                    cursor: 'pointer',
                    point: {
                        events: {
                            click: function() {
                                var drilldown = this.drilldown;
                                if (drilldown) { // drill down
                                    setChart(drilldown.name, drilldown.categories, drilldown.data, drilldown.color);
                                } else { // restore
                                    setChart(name, categories, data);
                                }
                            }
                        }
                    },
                    dataLabels: {
                        enabled: true,
                        color: colors[0],
                        style: {
                            fontWeight: 'bold'
                        },
                        formatter: function() {
                            return this.y +'%';
                        }
                    }
                }
            },
            tooltip: {
                formatter: function() {
                    var point = this.point,
                        s = this.x +':<b>'+ this.y +'%</b><br/>';
                    if (point.drilldown) {
                        s += 'Click to view detail on '+ point.category;
                    } else {
                        s += '';
                    }
                    return s;
                }
            },
            series: [{
                name: name,
                data: data,
                color: 'white'
            }],
            exporting: {
                enabled: false
            }
        })
        .highcharts(); // return chart
    });
    //show sample tweets for Bloomberg, it's hard coded now.
    $('.side').hide().html('<span class="sidetitle">Sample Tweets</span><br /><br /><span><b>Technology: </b> If you have an internet connection and a mobile phone, you can make money with iLA - http://t.co/J9I845lOKf<br /><br /><b>Food: </b>Do Not Allow an Increase of Harmful Herbicide in Food and Feed - ForceChange http://t.co/64eDbqxYS5<br /><br /><b>Sports: </b> #Women Auburn women’s golfers overcome trying season – USA Today http://t.co/tFolGR6AZN #TonyRocha<br /><br /><b>Politics: </b> @ChuckSchumer please inform #president #Obama , lately he doesn&sbquo;t know what&sbquo;s going on<br /><br /><b>Business: </b> #NZ credit card debt outstanding -0.3% in April 0.1% y/y - consumers remain cautious on higher cost credit card debt (vs housing loans)<br /><br /><b>Health: </b>Shout out to all those who love dance, eat, sleep and dream dance<br /><br /><b>Science: </b>http://t.co/N5ZFPSDuly Advances in 3D Medical Science accelerating. http://t.co/USMVHo2gwP<br /><br /><b>Arts: </b>@edstackartist Dito, I&sbquo;ve got tons of my art around the house. RT @Iancochraneart "if there were a #gallery, #museum, or #private collector"<br /><br /><b>Entertainment: </b>@joshduhamel just watched Safe Haven! Great movie, wasn&sbquo;t expecting the ending! :)').fadeIn();
    $('.compare').hide().html("Compare with Rahm Emanuel").fadeIn();
    return false;
});    



   
//show individual chart

    
    //show Emanuel chart
 $('.p9').click(function(){ 
        $.getJSON('er.json', function(data) {
        a = data.results.science;
        b = data.results.business;
        c = data.results.health;
        d = data.results.food;
        e = data.results.politics;
        f = data.results.entertainment;
        g = data.results.technology;
        h = data.results.sports;

        var colors = Highcharts.getOptions().colors,
            categories = ['Science', 'Business', 'Health', 'Food', 'Politics', 'Entertainment', 'Technology', 'Sports'],
            name = 'Browser brands',
            data = [{
                    y: Math.round(100 * (a / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                    
                }, {
                    y: Math.round(100 * (b / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                   
                }, {
                    y: Math.round(100 * (c / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                    
                }, {
                    y: Math.round(100 * (d / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                   
                }, {
                    y: Math.round(100 * (e / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                    drilldown: {
                       name: 'Politics',
                        categories: ['Gun control', 'Education', 'Environment', 'Immigration', 'National Security', 'Gay rights'],
                        data: [ 4, 33, 14, 23, 12, 34],
                        color: '#64AFDA',
                    }
                }, {
                    y: Math.round(100 * (f / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                   
                }, {
                    y: Math.round(100 * (g / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                  
                }, {
                    y: Math.round(100 * (h / (a+b+c+d+e+f+g+h))),
                    color: colors[0],
                  
                }
    ];
    
        function setChart(name, categories, data, color) {
            chart.xAxis[0].setCategories(categories, false);
            chart.series[0].remove(false);
            chart.addSeries({
                name: name,
                data: data,
                color: color || 'white'
            }, false);
            chart.redraw();
        }
    
        var chart = $('#container').highcharts({
            chart: {
                type: 'column'
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
            legend: {
                enabled: false
            },
            xAxis: {
                categories: categories
            },
            yAxis: {
                title: {
                    text: null
                }
            },
            plotOptions: {
                column: {
                    cursor: 'pointer',
                    point: {
                        events: {
                            click: function() {
                                var drilldown = this.drilldown;
                                if (drilldown) { // drill down
                                    setChart(drilldown.name, drilldown.categories, drilldown.data, drilldown.color);
                                } else { // restore
                                    setChart(name, categories, data);
                                }
                            }
                        }
                    },
                    dataLabels: {
                        enabled: true,
                        color: colors[0],
                        style: {
                            fontWeight: 'bold'
                        },
                        formatter: function() {
                            return this.y +'%';
                        }
                    }
                }
            },
            tooltip: {
                formatter: function() {
                    var point = this.point,
                        s = this.x +':<b>'+ this.y +'%</b><br/>';
                    if (point.drilldown) {
                        s += 'Click to view detail on '+ point.category;
                    } else {
                        s += '';
                    }
                    return s;
                }
            },
            series: [{
                name: name,
                data: data,
                color: 'white'
            }],
            exporting: {
                enabled: false
            }
        })
        .highcharts(); // return chart
    });
    //show sample tweets for Emanuel, it's hard coded now.
     $('.side').hide().html('<span class="sidetitle">Sample Tweets</span><br /><br /><span><b>Technology: </b>Google to launch music streaming service ahead of Apple http://t.co/5iarv57Rsm via @FastCompany<br /><br /><b>Food: </b>@fatherjonathan can still make hot tea....<br /><br /><b>Sports: </b> @mullyhanley #Bulls win to tonight to force the #Heat to make one more trip to Chicago! #SeeRed<br /><br /><b>Politics: </b> The #Catholic Church is for #immigration reform:http://t.co/ytTw6WUwI7<br /><br /><b>Business: </b> @thecrisismag @CharlesMBlow But not unexpected/the more we talk about this/the less we can talk about JOBS/economy<br /><br /><b>Health: </b>Very excited to be offering 2 Yoga for Runners classes in #Elmhurst this summer.  Please join me, and invite your... http://t.co/KH5npmt7t8<br /><br /><b>Science: </b>#JWCC is also holding its STEM prorgam this summer for high school students. It stands for Science Technology Engineering and Math @KHQA<br /><br /><b>Arts: </b>Iranian Artist Paints Large, Playful Murals On The Sides Of Buildings |... http://t.co/wzsgpRLifK<br /><br /><b>Entertainment: </b>I feel bad for JR Smith, feel like he is giving max effort it &sbquo;s just not happening for him. It &sbquo;s more than just him @AnthonyMSG #NYK</span>').fadeIn();
        $('.compare').hide().html("Compare with Michael Bloomberg").fadeIn();
        return false;
});    



 //show compare section
    $('.compare').click(function(){
        $('#vizbox').fadeOut();
        $('.container2').fadeIn();

    });
  //show compare chart
  $('.container2').highcharts({
            chart: {
                type: 'column'
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
                 headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y} %</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
            },
            xAxis: {
                categories: [
                    'Science', 'Business', 'Health', 'Food', 'Politics', 'Entertainment', 'Technology', 'Sports'
                ]
            }, 
            yAxis: {
                min: 0,
                title: {
                    text: null
                }
            }, 
            plotOptions: {
                
                series: {
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
                name: 'Bloomberg',
                data: [3, 8, 13, 9, 18, 4, 38, 8]
    
            }, {
                name: 'Emanuel',
                data: [2, 7, 8, 5, 40, 1, 27, 9]
    
            }],
            legend: {
                enabled: true
            }
    });   

});          
