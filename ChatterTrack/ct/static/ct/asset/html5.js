

ChatterTrack = {
    
    createHighChart : function (div) { 
                div.highcharts({
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

                        events: {
                        }
                    }
                },     
                series: []
            })},
    
    clearChart : function (div) {
        
        var chart = div.highcharts();
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
                "category_confidence" : confidence 
            }, ChatterTrack.ajaxFunctions.updateGraph).error(function () {
                    alert("Oops! Unable to fetch stream results.");
                } );
        
        },
        
        getTweets : function (name, category, streamId, confidence) {
            ChatterTrack.clearChart($('#word-count-container'));
            var jqxhr = $.get("http://ec2-54-244-189-248.us-west-2.compute.amazonaws.com/ct/getStreamedTweets/", {
                "stream_id" : streamId,
                "category_confidence" : confidence,
                "category" : category
            }, ChatterTrack.ajaxFunctions.updateWordCountGraph(name, category, streamId)).error(function () {
                    alert("Oops! Unable to fetch word counts.");
                });  
            
        },
        
        getTweetsWithWord : function (name, category, streamId, confidence, word) {
            //ChatterTrack.clearChart($('#word-count-container'));

            var jqxhr = $.get("http://ec2-54-244-189-248.us-west-2.compute.amazonaws.com/ct/getTweetsWithWord/", {
                "stream_id" : streamId,
                "category_confidence" : confidence,
                "category" : category, 
                "word" : word
            }, ChatterTrack.ajaxFunctions.handleTweetsWithWord(name, category, word)).error(function () {
                    alert("Oops! Unable to fetch word counts.");
                });
            
        },
        
        handleTweetsWithWord : function (name,category,word) {
          
            return function (data) {
                
                $("#tweets").html("");
                
                var tweets = data["results"];
                var htmlString = "<center><h3>";
                htmlString += "Followers of: " + name;
                htmlString += "<br/>Category: " + category;
                htmlString += "<br/>Word: " + word; 
                htmlString += "</h3></center>"; 
                
                htmlString += "<ul>"
                
                for (i = 0; i < tweets.length; i++) {
                    htmlString += "<li>"
                    htmlString += tweets[i]["text"];
                    htmlString += "</li>";
                }
                htmlString += "</ul>";
                
                $("#tweets").html(htmlString);
                $('html, body').animate({scrollTop:$('#pp').offset().top}, 700);
                //scroll to tweets
            }
        },
        
        updateGraph : function (data) {
            a = data.results.categories.science;
            b = data.results.categories.business;
            c = data.results.categories.sports;
            d = data.results.categories.food;
            e = data.results.categories.politics;
            f = data.results.categories.entertainment;
            g = data.results.categories["science-technology"];
            h = data.results.categories["healthy-living"];
            i = data.results.categories["education"];
            j = data.results.categories["religion"];
            total = a + b + c + d + e + f + g + h + i + j;
            ap = Math.round(100 * (a / total));
            bp = Math.round(100 * (b / total));
            cp = Math.round(100 * (c / total));
            dp = Math.round(100 * (d / total));
            ep = Math.round(100 * (e / total));
            fp = Math.round(100 * (f / total));
            gp = Math.round(100 * (g / total));
            hp = Math.round(100 * (h / total));
            ip = Math.round(100 * (i / total));
            jp = Math.round(100 * (j / total));

            var chart = $("#container").highcharts()
            chart.addSeries({
                name: data.results.name,
                data: [ap, bp, cp, dp, ep, fp, gp, hp, ip, jp] 
            });
            
            var keys = [];
            for (var key in data.results.categories) {
              if (data.results.categories.hasOwnProperty(key)) { 
                keys.push(key);  
              }
            }
            
            chart.series[chart.series.length-1].stream_id = data.results.stream_id;
        },
        
        updateWordCountGraph : function (name, category, streamId) {
            
            return function (data) {
                chart = $('#word-count-container').highcharts();
                tweets = ""
                for (i = 0; i < data.results.length; i++) {
                    tweets += data.results[i].text + " "
                }
                
                options = {minimumCount: 1, stopWordSets : [], stopWords : [ "t.co", "RT", "http", "https", "a","able","about","across","after","all","almost","also","am","among","an","and","any","are","as","at","be","because","been","but","by","can","cannot","could","dear","did","do","does","either","else","ever","every","for","from","get","got","had","has","have","he","her","hers","him","his","how","however","i","if","in","into","is","it","its","just","least","let","like","likely","may","me","might","most","must","my","neither","no","nor","not","of","off","often","on","only","or","other","our","own","rather","said","say","says","she","should","since","so","some","than","that","the","their","them","then","there","these","they","this","tis","to","too","twas","us","wants","was","we","were","what","when","where","which","while","who","whom","why","will","with","would","yet","you","your", "gt", "ca", "Im", "a's","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","just","keep","keeps","kept","know","knows","known","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","que","quite","qv","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","value","various","very","via","viz","vs","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","wonder","would","would","wouldn't","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","zero" ]};
                w = WordFreqSync(options);
                
                results = w.process(tweets);
                
                keys = [];
                values = [];

                for (i = 0; i < results.length && i < 10; i++) {
                    keys.push(results[i][0]);
                    values.push(results[i][1]);
                }
                
                chart.addSeries({
                    name: name + ": " + category,
                    data: values 
                }, false);
                
                chart.series[chart.series.length-1].stream_id = streamId;
                chart.series[chart.series.length-1].name = name;
                chart.series[chart.series.length-1].category = category;
                
                chart.xAxis[0].categories = keys;
                chart.redraw(); 
                
            }
        }
    }
    
    
};

$(document).ready( function () {
    $(function() {
        $('.people').click(function(){
            $('.people').removeClass('highlight');  
            $(this).addClass('highlight');
            $('#vizbox').fadeIn();
            $('html, body').delay(600).animate({scrollTop:$('#pp').offset().top}, 700);
            return false;
        });
    });  
    
    ChatterTrack.createHighChart($('#container'));
    categoryChart = $('#container').highcharts();
    categoryChart.options.plotOptions.column.events.click = function (e) {  
        $('html, body').animate({scrollTop:$('#highcharts-3').offset().top}, 700);
        ChatterTrack.ajaxFunctions.getTweets(e.point.series.name, e.point.category.toLowerCase(), e.point.series.stream_id, 0.75);
    }; 
    
    categoryChart.xAxis[0].categories = [ 'Science', 'Business', 'Sports', 'Food', 'Politics', 'Entertainment', 'Science-Technology', 'Healthy-living', 'Education', 'Religion' ];
    //chart.redraw();
    
    ChatterTrack.createHighChart($('#word-count-container'));
    wordCountChart = $('#word-count-container').highcharts();
    
    wordCountChart.options.plotOptions.column.events.click = function (e) {  
        
        ChatterTrack.ajaxFunctions.getTweetsWithWord(e.point.series.name, e.point.series.category.toLowerCase(), e.point.series.stream_id, 0.75, e.point.category.toLowerCase());
        // last param is word
    };
    wordCountChart.options.plotOptions.column.dataLabels.formatter = function() {
        return this.y;
    }  
    
});
